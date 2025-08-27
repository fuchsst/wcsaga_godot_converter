

## **Section 1: The Workflow Engine: Custom Commands and Markdown-Based State Management**

To elevate qwen-code from an interactive assistant to a true orchestration engine, a system for defining repeatable tasks and managing state is required. This is achieved by combining custom, version-controlled commands with a structured, file-based state management protocol using markdown.

### **1.1 Engineering Repeatability with Custom Commands**

The foundation of a robust automation workflow is the ability to define custom, reusable commands. Drawing from the capabilities of its parent, Gemini CLI, qwen-code can be extended with user-defined slash commands stored in .toml files.1 To ensure that workflow logic is version-controlled alongside the project's source code, these definitions should be stored in a project-local  
.qwen/commands/ directory.  
The .toml file structure is simple yet powerful, requiring only two primary keys:

* description: A brief, human-readable summary of the command's function, which appears in the CLI's interactive help.  
* prompt: The master prompt that contains the core logic and instructions for the agent.

These commands can be parameterized using the {{args}} placeholder, which allows arguments passed on the command line to be dynamically inserted into the prompt.1 For this workflow, a dedicated command namespace,  
/workflow:\*, will be established (e.g., /workflow:plan, /workflow:implement, /workflow:validate). This creates a clean, extensible API for orchestrating the development lifecycle.

### **1.2 A Resilient State Management Protocol**

A reliable orchestration system requires a resilient method for tracking state. A file-based system using markdown is ideal, as it is both human-readable for easy inspection and machine-parsable for agent interaction, a common practice in modern developer tooling.3  
The following directory structure, located at the project root, will serve as the state machine for the workflow:

* .qwen\_workflow/: The root directory for all workflow state files.  
* .qwen\_workflow/tasks/: Contains individual markdown files for each discrete task (e.g., 001-add-user-auth.md).  
* .qwen\_workflow/logs/: Stores output logs from validation and testing runs.  
* PROJECT\_STATUS.md: A high-level dashboard file in the project root, summarizing the status of all tasks.

The agent will interact with this structure using its built-in file system tools, such as ReadFile, WriteFile, and Edit, which are fundamental capabilities inherited from its Gemini CLI origins.5 This approach requires adherence to best practices analogous to those for managing Terraform state: the state files should be treated as a single source of truth, manual edits should be avoided to prevent corruption, and interactions should be designed to be as atomic as possible.7  
To ensure the agent can reliably parse and update task information, a standardized schema for the task files is essential. This schema transforms a simple text file into a structured data object that drives the workflow. The combination of YAML frontmatter for metadata and a markdown body for descriptive content and checklists provides a robust format that serves both the AI agent and human reviewers.  
**Table 1: Proposed Markdown Task File Schema**

| Key | Type | Description | Example |
| :---- | :---- | :---- | :---- |
| id | String | Unique identifier for the task. | TASK-001 |
| title | String | A human-readable title. | Implement User Authentication Endpoint |
| status | Enum | Current state of the task. | pending | in\_progress | blocked | completed | failed |
| dependencies | Array | List of task IDs that must be completed first. | \`\` |
| assignee | String | Identifies the agent responsible (future-proofing for multi-agent setups). | qwen-coder |
| files\_to\_modify | Array | A list of files the agent anticipates changing. | \["src/server.js", "src/auth.js"\] |
| \--- | \--- | \--- | \--- |
| **Markdown Body** |  |  | \#\#\# Description\\nAs a user, I want to be able to log in...\\n\\n\#\#\# Acceptance Criteria\\n- \[ \] Create a POST /login endpoint.\\n- \[ \] Validate email and password.\\n- \[ \] Return a JWT on success. |

## **Section 2: Phase 1 \- Automated Planning and Task Decomposition**

The initial phase of the workflow leverages the agent's reasoning capabilities to transform a high-level requirement into a detailed, actionable plan. This separation of planning from implementation is a critical architectural decision that de-risks the automation process.

### **2.1 The /workflow:plan Command**

This custom command instructs the agent to act as a senior software architect. It takes a high-level user story or feature request as its argument and produces a structured plan for implementation.  
**File: .qwen/commands/workflow/plan.toml**

Ini, TOML

description="Analyzes a user story, inspects the codebase, and breaks it down into a structured plan of implementation tasks."

prompt \= """  
You are a senior software architect. Your role is to devise a comprehensive implementation plan for the following user story: "{{args}}".

Your task is to:  
1\.  Thoroughly analyze the existing codebase. Use your file system tools to read relevant files and understand the current architecture, coding patterns, and dependencies.  
2\.  Break down the user story into a sequence of smaller, verifiable, and logically ordered implementation tasks.  
3\.  For each task, identify any dependencies on other tasks and create a preliminary list of files that are likely to be modified.  
4\.  Output the final plan as a single, well-formed JSON array of task objects. Each object must contain the keys: "id", "title", "dependencies", and "files\_to\_modify".

You MUST NOT write or modify any code. Your sole output is the JSON plan.  
"""

This prompt explicitly guides the agent through a process of code analysis and task breakdown, drawing on established research in applying LLMs to software engineering planning.10 By demanding a structured JSON output, it leverages  
qwen-code's enhanced parser to produce a machine-readable result.12 This "stop and think" step produces a plan that can be reviewed by a human before any code is generated, preventing the agent from pursuing a flawed strategy.

### **2.2 Orchestrating State Transition**

Once the agent generates the plan, a simple orchestration script is used to materialize this plan into the file-based state management system.  
**Example Script: initiate\_workflow.sh**

Bash

\#\!/bin/bash

\# The user story is passed as the first argument to the script  
USER\_STORY="$1"

\# Invoke the agent to create the plan and save it to a file  
qwen /workflow:plan "$USER\_STORY" \> plan.json

\# A helper script (e.g., in Python or Node.js) parses the JSON  
\# and creates the corresponding markdown files in.qwen\_workflow/tasks/  
\# and updates the main PROJECT\_STATUS.md file.  
python parse\_plan.py plan.json

echo "Workflow initialized. Tasks created in.qwen\_workflow/tasks/"

This script invokes the /workflow:plan command and pipes the output to a file. A helper script then parses this structured data to create the individual task files according to the schema defined in Table 1\. This process transforms the agent's abstract plan into a concrete set of stateful artifacts that will drive the rest of the workflow. The resulting markdown files serve as a contract between the human supervisor and the AI agent for the work to be performed.

## **Section 3: Phase 2 \- Agentic Implementation and the Human-in-the-Loop Feedback Cycle**

With a plan in place, the workflow transitions to the implementation phase. This phase is designed as a tight loop, allowing for agent-led coding followed by human review and iterative refinement, all managed within the stateful task files.

### **3.1 The /workflow:implement Command**

This command is the workhorse of the implementation phase. It takes a single task ID as an argument and instructs the agent to execute the steps defined in the corresponding markdown file.  
**File: .qwen/commands/workflow/implement.toml**

Ini, TOML

description="Implements the specified task by reading its markdown file, applying code changes, and updating its status."

prompt \= """  
You are an expert software engineer. Your task is to implement the task with the ID: "{{args}}".

Your process is as follows:  
1\.  Read the markdown file located at \`.qwen\_workflow/tasks/{{args}}.md\`.  
2\.  Update the 'status' in the file's frontmatter to 'in\_progress' and save the file.  
3\.  \*\*CRITICAL\*\*: Check for a "\#\# Feedback" section in the markdown body. If it exists, you MUST prioritize addressing this feedback above all other instructions.  
4\.  Execute the implementation steps outlined in the file's "Acceptance Criteria" checklist. Use your code editing tools to modify the specified files. The \`@\` syntax (e.g., \`edit @src/file.js\`) should be used to scope your changes precisely.  
5\.  After successfully applying all changes, update the markdown file again:  
    \- Mark all completed items in the "Acceptance Criteria" checklist with \`\[x\]\`.  
    \- Change the 'status' in the frontmatter to 'completed'.  
6\.  If you encounter an unrecoverable error, change the 'status' to 'failed' and add a comment explaining the failure.  
"""

This prompt directs the agent to manage the task's lifecycle by updating its state file before and after the implementation. It specifically highlights the use of precise, scoped edits, a known feature for applying changes without impacting unrelated parts of the codebase.13

### **3.2 The Refinement Protocol (The Feedback Loop)**

No AI agent is perfect; a mechanism for human oversight and correction is essential. This workflow implements a robust feedback loop that is both stateful and auditable, aligning with agile development principles.14  
The process is as follows:

1. The agent completes its first implementation pass for a task.  
2. A human developer reviews the generated code changes (e.g., using git diff).

3. ## **If corrections are needed, the reviewer does not modify the code directly. Instead, they open the relevant task file (e.g., .qwen\_workflow/tasks/TASK-001.md) and add a new section:**     **Feedback** 

   * The database query in src/auth.js is vulnerable to SQL injection. Please refactor it to use a parameterized query.  
   * Add JSDoc comments to the new login function.  
4. The /workflow:implement TASK-001 command is executed again.

Because the agent's prompt is explicitly designed to prioritize the "Feedback" section, it will now focus on addressing these new instructions. This cycle can be repeated as many times as necessary. Storing the feedback within the version-controlled markdown file is a superior engineering practice compared to relying on ephemeral, interactive chat history. It creates a persistent, auditable, and asynchronous record of the entire collaborative process between the human and the AI, allowing any team member to understand the full history of implementation attempts and refinements.

## **Section 4: Phase 3 \- Integrated Quality Gates and Automated Remediation**

After implementation, the workflow enters a validation phase where automated quality checks are executed. This phase acts as a "quality gate," ensuring that the agent's contributions adhere to project standards. The system is designed not only to detect failures but also to attempt automated remediation.

### **4.1 The /workflow:validate Command**

This command orchestrates the execution of the project's entire suite of quality checks, including linting, testing, and security scanning. It leverages the CLI's ability to execute arbitrary shell commands, a feature inferred from its Gemini CLI heritage 5, to integrate with existing toolchains.  
**File: .qwen/commands/workflow/validate.toml**

Ini, TOML

description="Runs all project quality gates (linting, tests, etc.) for the changes related to a task and logs the output."

prompt \= """  
You are a quality assurance engineer. Your task is to validate the implementation of task "{{args}}".

Execute the following sequence of quality checks using your shell tool. Capture all \`stdout\` and \`stderr\` from each command.  
1\.  Run the linter: \`\! npx eslint.\`  
2\.  Run unit tests: \`\! npm run test:unit\`  
3\.  Run integration tests: \`\! npm run test:integration\`

If all commands execute successfully (exit code 0), your task is complete.  
If any command fails, save the complete, unabridged output (both \`stdout\` and \`stderr\`) of the failing command to a new log file at \`.qwen\_workflow/logs/{{args}}-failure.log\`.  
"""

This command acts as a bridge between the AI agent and the project's existing CI/CD practices.17 The ability to wrap any command-line tool makes this workflow language-agnostic and highly adaptable.  
**Table 2: Quality Gate Integration Patterns**

| Tool Category | Ecosystem | Tool | qwen Command Example within /workflow:validate |
| :---- | :---- | :---- | :---- |
| **Linting** | JavaScript | ESLint | \! npx eslint. \--format json \--output-file.qwen\_workflow/logs/lint.json |
| **Linting** | Python | Flake8 | \! flake8. \--output-file=.qwen\_workflow/logs/lint.txt |
| **Unit Testing** | JavaScript | Jest | \! npx jest \--json \--outputFile=.qwen\_workflow/logs/jest.json |
| **Unit Testing** | Python | Pytest | \! pytest \--junitxml=.qwen\_workflow/logs/pytest.xml |
| **Security** | General | Semgrep | \! semgrep scan \--json \-o.qwen\_workflow/logs/semgrep.json |

### **4.2 Closing the Quality Loop (Automated Remediation)**

The most advanced stage of this workflow is the self-correcting loop. When a validation check fails, the system automatically attempts to have the agent fix its own errors.  
An orchestration script manages this process:

1. The script executes qwen /workflow:validate TASK-001.  
2. It checks the exit code of the command.  
3. If the validation fails, the script identifies the newly created error log (e.g., .qwen\_workflow/logs/TASK-001-failure.log).  
4. It then appends the content of this error log to the \#\# Feedback section of the corresponding task markdown file.  
5. Finally, it re-invokes qwen /workflow:implement TASK-001.

The agent, following its prompt, will now see the test failures or linting errors as its highest-priority feedback and will attempt to remediate the issues it just introduced. This creates a powerful, automated cycle of implementation, testing, and bug-fixing, significantly increasing the level of autonomy and aligning with research on automated program repair for LLM-generated code.20

## **Section 5: Full Workflow Orchestration and Advanced Strategies**

This final section synthesizes the individual commands and phases into a single, cohesive orchestration script and explores advanced extensions to the framework.

### **5.1 The Master Orchestration Script**

The entire lifecycle can be automated with a master shell script that invokes the custom commands in sequence. This script serves as the tangible implementation of the complete, agent-driven development workflow.  
**Example Script: run\_workflow.sh**

Bash

\#\!/bin/bash  
set \-e \# Exit immediately if a command exits with a non-zero status.

USER\_STORY="$1"  
if; then  
  echo "Usage: $0 \\"\<user\_story\>\\""  
  exit 1  
fi

echo "--- Phase 1: Planning \---"  
qwen /workflow:plan "$USER\_STORY" \> plan.json  
python parse\_plan.py plan.json \# Helper to create task files

\# Get the list of task IDs to process (e.g., from the generated PROJECT\_STATUS.md)  
TASK\_IDS=$(grep \-o 'TASK-\[0-9\]\*' PROJECT\_STATUS.md)

for TASK\_ID in $TASK\_IDS; do  
  echo "--- Processing Task: $TASK\_ID \---"  
    
  MAX\_ATTEMPTS=3  
  for ((i=1; i\<=MAX\_ATTEMPTS; i++)); do  
    echo "--- Phase 2: Implementation (Attempt $i) \---"  
    qwen /workflow:implement "$TASK\_ID"  
      
    echo "--- Phase 3: Validation \---"  
    if qwen /workflow:validate "$TASK\_ID"; then  
      echo "✅ Validation successful for $TASK\_ID"  
      break \# Exit the loop on success  
    else  
      echo "❌ Validation failed for $TASK\_ID. Logging feedback for remediation."  
      \# Append the failure log to the task's feedback section  
      LOG\_FILE=".qwen\_workflow/logs/${TASK\_ID}-failure.log"  
      echo \-e "\\n\#\# Feedback (Automated from Validation Failure)\\n\\\`\\\`\\\`\\n$(cat $LOG\_FILE)\\n\\\`\\\`\\\`" \>\> ".qwen\_workflow/tasks/${TASK\_ID}.md"  
        
      if; then  
        echo "🔥 Maximum attempts reached for $TASK\_ID. Manual intervention required."  
        exit 1  
      fi  
    fi  
  done  
done

echo "🎉 Workflow completed successfully\!"

This script demonstrates a sequential orchestration pattern, executing the plan-implement-validate loop for each task generated in the planning phase.22

### **5.2 Extending the Framework**

The core workflow provides a solid foundation that can be extended with additional capabilities.

* **Git Integration:** The workflow commands can be augmented to interact directly with the version control system. The /workflow:implement command could be modified to automatically create a feature branch (\! git checkout \-b feature/$TASK\_ID). Upon successful validation, the /workflow:validate command could commit the changes and even create a pull request. This leverages the documented ability of qwen-code to automate git-related tasks.24  
* **Automated Documentation:** A new command, /workflow:document, could be created. After a task is successfully validated, this command would instruct the agent to read the code changes (\! git diff) and update relevant documentation, such as README.md files, JSDoc comments, or OpenAPI specifications, another well-documented use case for the tool.13  
* **Multi-Agent Systems:** The assignee field in the task schema provides a hook for future expansion into multi-agent workflows. A more sophisticated orchestrator could route tasks to different specialized agents. For example, a qwen-coder agent could handle implementation, while a dedicated "security-agent" could be invoked for validation tasks that require specialized security analysis tools. This aligns with the direction of more complex agentic frameworks like Qwen-Agent.25

## **Conclusion: The Terminal as the Epicenter of AI-Driven Development**

The workflow architected in this report demonstrates a tangible system for achieving a high degree of automation in the software development lifecycle. By combining the agentic capabilities of the qwen-code CLI with a structured, file-based state management protocol and custom, version-controlled commands, it is possible to build a repeatable, auditable, and resilient engineering system.  
This framework represents a significant step beyond using AI as a simple coding assistant. It operationalizes the central thesis that the next evolution of these tools lies in their capacity as orchestration engines. This shift redefines the role of the developer, moving from a focus on line-by-line implementation to that of a system architect and AI supervisor who designs, monitors, and refines the automated processes. The playbook presented here serves as a foundational blueprint for building these next-generation, AI-native engineering systems, positioning the command-line terminal as the true epicenter of modern, AI-driven development.

#### **Works cited**

1. Gemini CLI: Custom slash commands | Google Cloud Blog, accessed August 27, 2025, [https://cloud.google.com/blog/topics/developers-practitioners/gemini-cli-custom-slash-commands](https://cloud.google.com/blog/topics/developers-practitioners/gemini-cli-custom-slash-commands)  
2. Gemini CLI Tutorial Series — Part 7 : Custom slash commands | by Romin Irani \- Medium, accessed August 27, 2025, [https://medium.com/google-cloud/gemini-cli-tutorial-series-part-7-custom-slash-commands-64c06195294b](https://medium.com/google-cloud/gemini-cli-tutorial-series-part-7-custom-slash-commands-64c06195294b)  
3. MkDocs, accessed August 27, 2025, [https://www.mkdocs.org/](https://www.mkdocs.org/)  
4. 5 Overlooked Markdown Features for Better Project Documentation \- Liatrio, accessed August 27, 2025, [https://www.liatrio.com/resources/blog/5-markdown-features-for-better-documentation](https://www.liatrio.com/resources/blog/5-markdown-features-for-better-documentation)  
5. Gemini CLI Full Tutorial \- DEV Community, accessed August 27, 2025, [https://dev.to/proflead/gemini-cli-full-tutorial-2ab5](https://dev.to/proflead/gemini-cli-full-tutorial-2ab5)  
6. Gemini CLI: A Guide With Practical Examples \- DataCamp, accessed August 27, 2025, [https://www.datacamp.com/tutorial/gemini-cli](https://www.datacamp.com/tutorial/gemini-cli)  
7. State Management in IaC: Best Practices for Handling Terraform State Files \- Firefly, accessed August 27, 2025, [https://www.firefly.ai/academy/state-management-in-iac-best-practices-for-handling-terraform-state-files](https://www.firefly.ai/academy/state-management-in-iac-best-practices-for-handling-terraform-state-files)  
8. Manage resources in Terraform state \- HashiCorp Developer, accessed August 27, 2025, [https://developer.hashicorp.com/terraform/tutorials/state/state-cli](https://developer.hashicorp.com/terraform/tutorials/state/state-cli)  
9. writing a CLI for the first time, where do you store persistent data? : r/rust \- Reddit, accessed August 27, 2025, [https://www.reddit.com/r/rust/comments/176x38m/writing\_a\_cli\_for\_the\_first\_time\_where\_do\_you/](https://www.reddit.com/r/rust/comments/176x38m/writing_a_cli_for_the_first_time_where_do_you/)  
10. arXiv:2308.11396v3 \[cs.SE\] 10 Dec 2024, accessed August 27, 2025, [https://arxiv.org/pdf/2308.11396](https://arxiv.org/pdf/2308.11396)  
11. Automated Business Process Analysis: An LLM-Based Approach to Value Assessment \[Extended version\] \- arXiv, accessed August 27, 2025, [https://arxiv.org/html/2504.06600v1](https://arxiv.org/html/2504.06600v1)  
12. Introducing **Qwen-Code**: Alibaba's Open‑Source CLI for Agentic Coding with Qwen3‑Coder \- NYU Shanghai RITS, accessed August 27, 2025, [https://rits.shanghai.nyu.edu/ai/introducing-qwen-code-alibabas-open%E2%80%91source-cli-for-agentic-coding-with-qwen3%E2%80%91coder/](https://rits.shanghai.nyu.edu/ai/introducing-qwen-code-alibabas-open%E2%80%91source-cli-for-agentic-coding-with-qwen3%E2%80%91coder/)  
13. Qwen Code CLI: A Guide With Examples \- DataCamp, accessed August 27, 2025, [https://www.datacamp.com/tutorial/qwen-code](https://www.datacamp.com/tutorial/qwen-code)  
14. What is a product feedback loop (and how do I implement it)? \- LaunchDarkly, accessed August 27, 2025, [https://launchdarkly.com/blog/product-feedback-loop/](https://launchdarkly.com/blog/product-feedback-loop/)  
15. How to Use Fast Feedback Loops for Agile Development \- GitKraken, accessed August 27, 2025, [https://www.gitkraken.com/blog/feedback-loops-agile-development](https://www.gitkraken.com/blog/feedback-loops-agile-development)  
16. Gemini CLI Tutorial Series \- Google Cloud \- Medium, accessed August 27, 2025, [https://medium.com/google-cloud/gemini-cli-tutorial-series-77da7d494718](https://medium.com/google-cloud/gemini-cli-tutorial-series-77da7d494718)  
17. Continuous Integration \- Martin Fowler, accessed August 27, 2025, [https://martinfowler.com/articles/continuousIntegration.html](https://martinfowler.com/articles/continuousIntegration.html)  
18. Continuous integration \- GitHub Docs, accessed August 27, 2025, [https://docs.github.com/en/actions/get-started/continuous-integration](https://docs.github.com/en/actions/get-started/continuous-integration)  
19. How Unit Testing, Linting, and Continuous Integration in Python Can Improve Open Science | Earth Lab, accessed August 27, 2025, [https://earthdatascience.org/blog/unit-testing-linting-ci-python/](https://earthdatascience.org/blog/unit-testing-linting-ci-python/)  
20. Automatic Programming: Large Language Models and Beyond \- arXiv, accessed August 27, 2025, [https://arxiv.org/html/2405.02213v2](https://arxiv.org/html/2405.02213v2)  
21. \[2405.02213\] Automatic Programming: Large Language Models and Beyond \- arXiv, accessed August 27, 2025, [https://arxiv.org/abs/2405.02213](https://arxiv.org/abs/2405.02213)  
22. Workflow Engine vs. State Machine, accessed August 27, 2025, [https://workflowengine.io/blog/workflow-engine-vs-state-machine/](https://workflowengine.io/blog/workflow-engine-vs-state-machine/)  
23. Efficient Workflow Design Patterns \- Prefect, accessed August 27, 2025, [https://www.prefect.io/blog/workflow-design-patterns](https://www.prefect.io/blog/workflow-design-patterns)  
24. How to Use Qwen3-Coder and Qwen Code \- DEV Community, accessed August 27, 2025, [https://dev.to/therealmrmumba/how-to-use-qwen3-coder-and-qwen-code-4g4p](https://dev.to/therealmrmumba/how-to-use-qwen3-coder-and-qwen-code-4g4p)  
25. Agent framework and applications built upon Qwen\>=3.0, featuring Function Calling, MCP, Code Interpreter, RAG, Chrome extension, etc. \- GitHub, accessed August 27, 2025, [https://github.com/QwenLM/Qwen-Agent](https://github.com/QwenLM/Qwen-Agent)
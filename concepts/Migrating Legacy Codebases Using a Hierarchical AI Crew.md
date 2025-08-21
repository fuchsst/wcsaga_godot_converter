

# **Agentic Ascension: A Playbook for Migrating Legacy Codebases Using a Hierarchical AI Crew**

## **Part I: The Command Architecture \- Orchestrating the Migration Crew**

The successful migration of a complex, legacy codebase such as Wing Commander Saga to a modern engine like Godot requires a strategy that transcends manual refactoring or simple, monolithic AI assistance. It necessitates a structured, intelligent, and automated system capable of strategic planning, task decomposition, and precise code execution. This section outlines the design of such a system: an Agentic Command Center built on a hierarchical multi-agent framework. This architecture establishes a clear division of cognitive labor, from high-level strategic planning down to the execution of atomic code modifications, all orchestrated through a robust and extensible set of custom tools.

### **1.1. Designing the Agentic Command Center**

The foundation of this migration strategy is a multi-agent system, architected using the principles of frameworks like CrewAI.1 This system is not a mere collection of conversational agents but a purpose-built command crew, where each agent is assigned a specific role, goal, and operational context. This specialization ensures that each component of the migration process is handled by an expert system, leading to higher quality outcomes and greater efficiency. The entire crew's configuration, including agent roles and task definitions, will be managed through declarative YAML files, promoting modularity, clarity, and ease of maintenance.1  
All high-level cognitive and orchestration tasks will be powered by the **DeepSeek V3.1** model. Its advanced reasoning and instruction-following capabilities make it an ideal choice for the entire command crew, ensuring a consistent and high-quality cognitive backbone for the operation.2 CrewAI's flexible architecture allows for straightforward integration with any OpenAI-compatible API.4 Since DeepSeek provides such an endpoint, the crew can be configured to use DeepSeek V3.1 by setting the appropriate  
base\_url and api\_key.6  
The crew is composed of several specialist agents:

* **MigrationArchitect**: This agent serves as the project lead. Its primary objective is to formulate the high-level, phased migration strategy. Upon receiving the initial directive—"Migrate Wing Commander Saga to Godot"—it analyzes the project's scope and decomposes it into major, logically sequenced phases, such as "Phase 1: Port Core Systems," "Phase 2: Convert Game Logic," and "Phase 3: Refactor for Godot API Integration." This agent sets the overarching agenda for the entire crew.  
* **CodebaseAnalyst**: A specialist agent equipped with tools for static code analysis. Its core function is to develop a deep understanding of the legacy C++ codebase. It reads source files, identifies dependencies between classes and modules, and constructs a model of the existing architecture. This information is crucial for providing the necessary context to other agents, preventing them from making changes in isolation that could break distant parts of the system.  
* **TaskDecompositionSpecialist**: This agent acts as a middle manager, translating the broad strategic directives from the MigrationArchitect into a series of concrete, atomic coding tasks. For example, it takes a high-level goal like "Port the PlayerShip class" and breaks it down into a precise sequence of operations suitable for the low-level CLI coding agent.  
* **PromptEngineeringAgent**: A critical meta-agent that functions as the communication officer between the command crew and the execution layer. Its goal is to take a decomposed task from the TaskDecompositionSpecialist and the relevant code context from the CodebaseAnalyst and synthesize them into a perfectly formatted, unambiguous, and context-rich prompt. This agent is an expert in the principles of effective prompting, ensuring that instructions are clear, specific, and provide all necessary information for the CLI agent to succeed on the first attempt.7  
* **QualityAssuranceAgent**: This agent is responsible for verification and quality control. After the CLI agent executes a task, the QualityAssuranceAgent analyzes the results—including command output, error messages, and generated code—to determine success or failure. If a task fails, this agent performs root cause analysis. It diagnoses the issue (e.g., syntax error, logical flaw, failed test) and routes the task back to the appropriate agent—often the PromptEngineeringAgent—with additional context about the failure. This creates an autonomous feedback loop, enabling the system to learn from its mistakes and self-correct.

To formalize this structure, the following charter outlines the specific roles and responsibilities within the AI crew. This charter serves as both a conceptual model for understanding the system's cognitive flow and a direct blueprint for the agents.yaml configuration file.  
**Table 1: Agent Role and Responsibility Charter**

| Agent Name | Persona/Role | Primary Goal | Key Tools | Expected Output |
| :---- | :---- | :---- | :---- | :---- |
| MigrationArchitect | Lead Systems Architect (powered by DeepSeek V3.1) | Decompose the overall migration into a high-level, phased project plan. | FileReadTool | A multi-phase project plan in Markdown format, outlining the migration sequence. |
| CodebaseAnalyst | Senior Software Analyst (powered by DeepSeek V3.1) | Analyze the legacy codebase to identify dependencies, modules, and architectural patterns. | FileReadTool, CodeStructureAnalysisTool | A structured representation (e.g., JSON) of the codebase's dependency graph and key components. |
| TaskDecompositionSpecialist | Technical Project Manager (powered by DeepSeek V3.1) | Break down high-level migration phases into a sequence of atomic, executable coding tasks. | None | A list of specific, ordered instructions for code modification or generation. |
| PromptEngineeringAgent | AI Communications Specialist (powered by DeepSeek V3.1) | Convert atomic tasks and code context into precise, effective prompts for the CLI agent. | None | A fully-formed, context-rich prompt string formatted for the target CLI agent. |
| QualityAssuranceAgent | QA Automation Engineer (powered by DeepSeek V3.1) | Verify the output of CLI agent tasks, diagnose failures, and initiate corrective actions. | QwenCodeExecutionTool, GitDiffTool, TestRunnerTool | A success/failure status, and in case of failure, a new task for correction. |

### **1.2. The Bridge to Execution: A Custom Tool for CLI Agent Control**

The conceptual work of the high-level agent crew can only be translated into tangible code changes through a physical interface to the development environment. This bridge is a custom tool designed to execute shell commands non-interactively and report the results back to the crew. This tool is the most critical technical component of the architecture, as it enables the cognitive layer to interact with and modify the file system.  
This custom tool, QwenCodeExecutionTool, will be implemented as a Python class that conforms to the CrewAI tool interface, either by inheriting from BaseTool or by using the @tool decorator.10 Its core functionality will be built upon Python's robust  
subprocess module, which allows for the spawning and management of external processes.11  
The design of this tool must be approached with the same rigor as a formal Application Programming Interface (API), as it defines the contract between the agent crew and the execution agents. The inputs to the tool (the command string) are the API calls, and its structured output (return code, stdout, stderr) is the API response. This perspective mandates a design focused on clarity, robustness, and structured data exchange, ensuring a decoupled and maintainable system.  
Key features of the QwenCodeExecutionTool include:

* **Non-Interactive Command Execution**: The tool's primary function is to accept a complete shell command as a string argument and execute it.  
* **Comprehensive Output Capturing**: It is essential that the tool captures all output from the executed process. This will be achieved by setting the capture\_output=True and text=True arguments in the subprocess.run() call.11 The captured  
  stdout and stderr streams are not merely for logging; they are the primary feedback mechanism for the QualityAssuranceAgent, providing the raw data needed to assess task success and diagnose failures.  
* **Robust Error Handling**: The tool must inspect the returncode attribute of the CompletedProcess object returned by subprocess.run().11 A return code of  
  0 typically indicates success, while any non-zero value signifies an error. The tool will package this return code along with the captured output and pass it back to the calling agent, allowing the crew to initiate its error-handling and correction workflows.  
* **Timeout Implementation**: To prevent the entire system from stalling due to a hanging or long-running process, the tool will utilize the timeout parameter of subprocess.run(). If a command exceeds the specified time limit, subprocess will raise a TimeoutExpired exception, which the tool will catch and report as a failure to the agent crew.

Below is a conceptual implementation of the QwenCodeExecutionTool in Python, demonstrating the integration of these features within the CrewAI framework.

Python

import subprocess  
from crewai\_tools import BaseTool  
from pydantic import BaseModel, Field  
from typing import Type

class ShellCommandInput(BaseModel):  
    """Input schema for the QwenCodeExecutionTool."""  
    command: str \= Field(..., description="The full shell command to be executed.")  
    timeout\_seconds: int \= Field(default=300, description="Timeout for the command in seconds.")

class QwenCodeExecutionTool(BaseTool):  
    name: str \= "Qwen Code CLI Execution Tool"  
    description: str \= "Executes a shell command non-interactively for the Qwen Code agent, captures its output, and returns the result."  
    args\_schema: Type \= ShellCommandInput

    def \_run(self, command: str, timeout\_seconds: int) \-\> str:  
        """Executes the shell command and returns a structured report of the outcome."""  
        try:  
            \# This implementation is simplified. A real implementation for an interactive  
            \# tool like qwen-code would require subprocess.Popen to manage stdin/stdout.  
            result \= subprocess.run(  
                command,  
                shell=True,  
                capture\_output=True,  
                text=True,  
                timeout=timeout\_seconds,  
                check=False \# We handle the non-zero exit code manually  
            )

            \# Structure the output for the QualityAssuranceAgent  
            output\_report \= (  
                f"Execution Report for command: \`{command}\`\\n"  
                f"Return Code: {result.returncode}\\n\\n"  
                f"--- STDOUT \---\\n"  
                f"{result.stdout}\\n\\n"  
                f"--- STDERR \---\\n"  
                f"{result.stderr}"  
            )  
            return output\_report

        except subprocess.TimeoutExpired as e:  
            return (  
                f"Execution Failed: Timeout\\n"  
                f"Command: \`{command}\` exceeded the {timeout\_seconds}s limit.\\n"  
                f"STDOUT: {e.stdout}\\n"  
                f"STDERR: {e.stderr}"  
            )  
        except Exception as e:  
            return f"An unexpected error occurred while executing command \`{command}\`: {str(e)}"

### **1.3. Defining Collaborative Workflows and Processes**

With the agents defined and the execution tool in place, the final piece of the command architecture is the orchestration logic that governs their collaboration. The choice of workflow, or Process in CrewAI terminology, is not a static decision but should be adapted to the complexity of the task at hand.1

* **Sequential Process**: For the majority of atomic coding tasks, a Process.sequential workflow is the most appropriate choice. This model ensures a predictable, linear flow of execution: the TaskDecompositionSpecialist generates a task, the PromptEngineeringAgent creates a prompt, the QwenCodeExecutionTool is invoked, and finally, the QualityAssuranceAgent verifies the result. This simple, step-by-step process is ideal for its clarity and ease of debugging.  
* **Hierarchical Process**: For managing the overall migration, a Process.hierarchical model offers superior control and scalability. In this configuration, the MigrationArchitect acts as the manager, delegating high-level phases to subordinate agents or even entire sub-crews. For instance, the MigrationArchitect could assign the "Port UI Systems" phase to a dedicated sub-crew that then executes its own sequential process to migrate each UI component. This allows for both high-level strategic oversight and focused, parallelized execution of complex sub-problems.

The adaptability of the system is paramount. The architecture should allow the MigrationArchitect to dynamically instantiate sub-crews with the process model best suited to the complexity of the delegated task. A simple bug fix might trigger a single, sequential workflow, while refactoring the entire physics engine would necessitate a hierarchical process with a manager agent overseeing multiple, interdependent sub-tasks. This dynamic selection of workflow models transforms the system from a rigid automaton into an adaptive and efficient project management entity.

## **Part II: The Execution Layer \- The Qwen Code Specialist**

The effectiveness of the agentic command crew depends entirely on the capabilities of the tool at its disposal. The execution layer will consist of a single, powerful Command Line Interface (CLI) coding agent: qwen-code.13 This tool, powered by the Qwen3-Coder series of models, is specifically designed for agentic workflows and possesses a unique combination of features that make it the ideal choice for this migration.14 By standardizing on a single, highly capable execution agent, we simplify the command architecture and focus on mastering its operation for all coding tasks.

### **2.1. qwen-code: The Agentic Coding Powerhouse**

qwen-code is a command-line tool built upon Alibaba's state-of-the-art Qwen3-Coder models, which are distinguished by their massive context windows and strong performance in complex, agentic coding tasks.16

* **Core Capability**: The primary advantage of the Qwen3-Coder models is their exceptionally large context window, supporting 256,000 tokens natively and up to 1 million tokens with extrapolation methods.16 This enables  
  qwen-code to process and reason about vast amounts of code in a single pass. It is therefore the ideal tool for both generative and refactoring tasks that are context-heavy. Translating a large C++ file, refactoring a complex module with many internal dependencies, or generating a new system from a detailed specification are all tasks well-suited to its capabilities.18  
* **Agentic Features**: qwen-code is more than a simple code generator; it is designed for agentic workflows.14 It can autonomously plan and execute multi-step tasks, such as analyzing a codebase, identifying files for modification, and even automating git operations like creating branches and committing changes.20 This makes it a powerful, all-in-one tool for the execution layer.  
* **The Automation Challenge and Solution**: A significant operational hurdle is that qwen-code's primary interface is an interactive, chat-based CLI.17 This is fundamentally incompatible with the non-interactive, automated workflow required by our agentic crew. To overcome this, the system must employ a sophisticated invocation strategy. The  
  QwenCodeExecutionTool cannot simply use subprocess.run(). Instead, it must use the lower-level subprocess.Popen interface. This allows the tool to start the qwen process, programmatically write the generated prompt to the process's stdin stream, and then read the resulting code from its stdout stream. This technique effectively wraps the interactive tool, transforming it into a non-interactive component that the automated system can control.

The necessity of this wrapper has significant architectural implications. It introduces a potential point of fragility; if qwen-code's output format changes in a future update, the wrapper's parsing logic may break. To mitigate this, the PromptEngineeringAgent must be tasked with generating prompts for qwen-code that are extremely precise. These prompts must include explicit instructions like: "Your response must contain only the requested GDScript code. Do not include any explanatory text, conversational filler, or requests for confirmation." Furthermore, the QualityAssuranceAgent must be equipped with robust parsing logic to clean and validate the output from qwen-code, stripping away any extraneous text before evaluating the code itself.

## **Part III: The Communication Protocol \- The Prompt Engineering Playbook**

The performance of an agentic system is fundamentally limited by the quality of its internal communication. In this architecture, that communication takes the form of prompts. A well-crafted prompt can elicit a precise, correct response, while an ambiguous or incomplete one will lead to errors, hallucinations, and wasted computation. This section establishes a formal communication protocol, implemented as a series of structured prompt templates, to ensure clear, effective, and reliable communication between the orchestration crew and the execution agent.

### **3.1. Strategic Prompts: Initiating the Migration**

The entire automated process begins with a single, human-written strategic prompt. This initial instruction sets the context and defines the ultimate objective for the MigrationArchitect. The quality of this prompt is critical, as it frames the entire problem space for the AI crew. It must be crafted using established prompt engineering best practices.8

* **Define a Persona**: The prompt should begin by assigning a role to the agent crew, which helps the LLM adopt the appropriate mindset and expertise.  
* **Clearly State the Problem**: The core task must be stated unambiguously. This includes defining the source codebase, the target engine, and the desired output language.  
* **Provide Essential Context**: Include any high-level constraints, priorities, or specific areas of focus.  
* **Break Down the Initial Request**: Instead of asking for the entire migration at once, the prompt should direct the crew to perform an initial, manageable task, such as analysis and planning.

**Example Strategic Prompt Template:**  
You are a crew of expert game engine migration specialists, powered by the DeepSeek V3.1 model. Your collective mission is to orchestrate the complete migration of the legacy C++ codebase for the game 'Wing Commander Saga' to the Godot 4 engine, using GDScript as the target language.  
Your first task is to perform a strategic analysis of the existing codebase. Begin by focusing on the source code located in the src/core/ and src/player/ directories. Analyze these directories to identify the main classes, their responsibilities, and the dependencies between them.  
Based on this analysis, propose a high-level, phased migration plan. The plan should prioritize porting foundational systems before application-level game logic. Present this plan as a Markdown document.

### **3.2. Tactical Prompts: Generating Actionable CLI Instructions**

This is the most critical stage of communication, where the PromptEngineeringAgent translates abstract tasks into concrete instructions for the qwen-code CLI agent. These tactical prompts are not conversational; they are highly structured, machine-readable specifications designed for maximum clarity and precision.  
The design of these prompts will be guided by several key principles:

* **Holistic Context**: Every prompt must be self-contained, providing all the information the CLI agent needs to complete the task without ambiguity.7 This includes the explicit task, the full paths to relevant files, and snippets of existing code that need to be modified or referenced.  
* **Structured Formatting**: To help the LLM parse the request, prompts will use a consistent format, such as XML-like tags or Markdown sections, to delineate different types of information.7 This structure makes it clear what the objective is, what code to work with, and what constraints to follow.  
* **Separation of Planning and Action**: The higher-level agents have already completed the planning phase. The tactical prompt must therefore be a direct command to execute a task. It should explicitly forbid the CLI agent from proposing alternative plans or asking for clarification.9  
* **Explicit Constraints**: The prompt must clearly define the boundaries of the task. This includes specifying which files are allowed to be modified, enforcing coding standards (e.g., "All generated GDScript code must use static typing"), and providing negative constraints (e.g., "Do not remove any existing functionality").

To standardize this process, the PromptEngineeringAgent will utilize a library of prompt templates tailored to specific task types for the qwen-code agent.  
**Table 2: Tactical Prompt Template Library for Qwen Code**

| Task ID | Task Description | Target Agent | Prompt Template |
| :---- | :---- | :---- | :---- |
| QWEN\_GENERATE\_01 | Generate a new file from a specification. | qwen-code | You are an expert GDScript programmer. Your task is to generate a new script file based on the provided specification. Your response must contain ONLY the complete GDScript code for the new file. Do not include any explanatory text, markdown formatting, or conversational filler. \<TARGET\_FILE\_PATH\>{target\_file\_path}\</TARGET\_FILE\_PATH\> \<SPECIFICATION\>{specification}\</SPECIFICATION\> \<CONTEXT\_CODE\>{optional\_context\_code}\</CONTEXT\_CODE\> |
| QWEN\_REFACTOR\_01 | Refactor an existing function in a single file. | qwen-code | You are an expert GDScript programmer. Your task is to perform a specific refactoring on an existing file. Do not propose a plan; implement the change directly. Do not modify any other files. \<FILE\_PATH\>{file\_path}\</FILE\_PATH\> \<TASK\_DESCRIPTION\>{task\_description}\</TASK\_DESCRIPTION\> \<CONSTRAINTS\>{constraints}\</CONSTRAINTS\> |
| QWEN\_BUGFIX\_01 | Fix a bug based on an error message or test failure. | qwen-code | You are an expert debugger. A bug has been identified in the following file. Your task is to fix it. Analyze the provided error message and code, identify the root cause, and apply the necessary correction. Implement the fix directly. \<FILE\_PATH\>{file\_path}\</FILE\_PATH\> \<br\>\<CODE\_SNIPPET\>{code\_snippet\_with\_bug}\</CODE\_SNIPPET\> \<ERROR\_MESSAGE\>{error\_message}\</ERROR\_MESSAGE\> |

### **3.3. Establishing Autonomous Feedback and Correction Loops**

A truly agentic system must be capable of recovering from failure. The architecture achieves this by treating errors not as dead ends, but as a valuable form of context to guide subsequent attempts. This creates a tight, autonomous feedback and correction loop orchestrated by the QualityAssuranceAgent.  
The workflow for this loop is as follows:

1. **Execution**: The PromptEngineeringAgent generates a prompt and passes the corresponding command to the QwenCodeExecutionTool.  
2. **Result Capture**: The tool executes the command and returns a structured report containing the returncode, stdout, and stderr.  
3. **Verification**: The QualityAssuranceAgent receives this report and begins its analysis.  
4. **Success Path**: If the returncode is 0 and stderr is empty, the task is likely successful. The agent performs a final sanity check, such as verifying that the target file was created or modified and contains valid code. If the checks pass, the task is marked as complete.  
5. **Failure Path**: If the returncode is non-zero or stderr contains an error message, the agent initiates the correction protocol.  
6. **Diagnosis**: The QualityAssuranceAgent analyzes the error message. Is it a compilation error from the Godot engine? A linting error? A Python traceback from the CLI tool itself? A refusal to answer from the LLM?  
7. **Correction and Re-tasking**: Based on the diagnosis, the QualityAssuranceAgent formulates a new task designed to correct the error. It invokes the PromptEngineeringAgent again, but this time with crucial new context: the original prompt *and* the error message from the failed attempt. For example, the new meta-prompt to the PromptEngineeringAgent would be: "The previous attempt to complete this task failed. Generate a new, corrected prompt. Original Task: {original\_task}. Error from previous attempt: {error\_message}."

This process of systematically capturing error signals and feeding them back into the prompting process for the next attempt is the cornerstone of the system's resilience. It transforms the workflow from a brittle, fire-and-forget execution model into an iterative, self-correcting learning process.

## **Part IV: The Campaign \- A Phased Migration of Wing Commander Saga**

With the agentic architecture, execution tools, and communication protocols defined, this final section applies the complete system to the concrete challenge of migrating the Wing Commander Saga codebase. This operational plan breaks the monumental task into a sequence of manageable campaigns, each with a clear objective and a defined strategy for deploying the AI crew. This serves as a practical, step-by-step guide for initiating and overseeing the automated migration.

### **4.1. Phase 1: Reconnaissance and Strategic Mapping**

Before any code is translated, a thorough understanding of the legacy codebase is essential. This initial phase is dedicated to automated analysis and strategic planning, ensuring that the migration proceeds in a logical and efficient order.

* **Objective**: To generate a comprehensive, data-driven migration plan and a detailed dependency map of the entire Wing Commander Saga C++ codebase.  
* **Execution**:  
  1. The human operator initiates the process with a strategic prompt directed at the MigrationArchitect, instructing it to begin the analysis phase.  
  2. The MigrationArchitect delegates the primary task to the CodebaseAnalyst. The CodebaseAnalyst is tasked with recursively traversing the entire src/ directory of the legacy project. Using its file system tools, it will identify all .h and .cpp files.  
  3. For each file, the CodebaseAnalyst will perform a lightweight static analysis to extract key information: \#include directives, class definitions, and major function declarations.  
  4. This information is aggregated to construct a project-wide dependency graph. This graph is a critical artifact, as it reveals the foundational modules (e.g., math libraries, string utilities) that must be ported first to avoid breaking dependencies later in the process.  
  5. The MigrationArchitect receives this dependency graph. Using its pre-programmed knowledge of Godot engine architecture, it creates a high-level, phased migration plan. The plan will explicitly prioritize foundational systems (e.g., porting core data structures before the physics engine that uses them).  
  6. The final output of this phase is a detailed project plan, formatted as a Markdown document. This document is presented to the human Technical Lead for review, modification, and final approval before any code-altering operations commence.

### **4.2. Phase 2: Securing the Beachhead \- Porting Core Systems**

This phase focuses on migrating the most fundamental, engine-agnostic components of the codebase. The goal is to establish a stable foundation of core utilities and data structures within the new Godot project, which all subsequent game logic will depend on.

* **Objective**: To translate essential, low-level systems and utility classes from C++ to GDScript.  
* **Execution**:  
  * **Task Identification**: The MigrationArchitect identifies tasks from the approved plan, such as translating utility classes for vector and matrix math, string manipulation, and data containers. It also includes creating stub implementations for high-level manager classes (e.g., a RenderingManager class with empty methods that will later be filled with calls to Godot's RenderingServer).  
  * **Agent Usage**: This phase will heavily leverage qwen-code. The translation of self-contained utility classes is a perfect use case for its large context window.16 The  
    TaskDecompositionSpecialist will create tasks like, "Translate the file src/math/vector3.cpp and its corresponding header into a single new GDScript file scripts/core/vector3.gd." The PromptEngineeringAgent will then feed the entire content of the C++ source files to qwen-code to produce a direct, high-fidelity translation.

### **4.3. Phase 3: Full-Scale Invasion \- Automated Asset and Logic Conversion**

With the core systems in place, the crew can now begin the main effort: converting the vast body of game-specific code, including gameplay logic, AI behaviors, mission scripts, and player mechanics.

* **Objective**: To automate the bulk translation and refactoring of the game's primary codebase.  
* **Execution**:  
  * **Parallelization**: This phase is highly suitable for parallel execution. The MigrationArchitect can instantiate multiple, independent sub-crews to work on different game modules simultaneously. For example, one sub-crew could be assigned to porting all player ship mechanics from src/player/, while another focuses on enemy AI behaviors from src/ai/.  
  * **Iterative Refinement with qwen-code**: This phase will use an iterative process with qwen-code to achieve a high-quality, idiomatic result.  
    1. **Initial Translation**: For a complex class like PlayerShip, qwen-code will be used first to perform the initial bulk translation from C++ to a new GDScript file. This leverages its strength in handling large, single-file contexts.18  
    2. **Incremental Refactoring**: The code generated by qwen-code will be syntactically correct GDScript but will likely contain legacy architectural patterns and direct calls to non-existent engine functions. The MigrationArchitect will then create a series of follow-up tasks. These tasks will be highly specific, such as: "In player\_ship.gd, replace the legacy InputManager.is\_key\_pressed() call with Godot's Input.is\_action\_pressed() system," or "Refactor the update() method to connect to Godot's \_physics\_process signal." These targeted refactoring prompts are sent back to qwen-code to incrementally improve the code's quality and alignment with Godot best practices.

### **4.4. Phase 4: Mop-Up and Fortification \- Integration, Testing, and Refinement**

The final phase focuses on ensuring the migrated codebase is not just translated, but is correct, robust, performant, and well-integrated into the Godot ecosystem.

* **Objective**: To verify the correctness of the migrated code through automated testing, fix any identified bugs, and perform final code quality improvements.  
* **Execution**:  
  * **Automated Test Generation**: The agent crew can be tasked with writing unit tests for the newly migrated code. For example, the MigrationArchitect can issue a directive: "Generate a suite of unit tests for the player\_ship.gd class using the gdUnit4 testing framework. Ensure test coverage for the apply\_damage, regenerate\_shields, and fire\_weapon functions." qwen-code is well-suited for generating the initial test file structure from this specification.20  
  * **Automated Bug Fixing**: When a test run fails, the output is captured and passed to the QualityAssuranceAgent. This triggers the autonomous bug-fixing loop. The agent will analyze the test failure output and orchestrate a fix using qwen-code. The loop proceeds as follows: the CodebaseAnalyst identifies the relevant code, the TaskDecompositionSpecialist proposes a logical fix, the PromptEngineeringAgent creates a precise prompt for qwen-code including the error context, qwen-code executes the change, and the tests are run again. This cycle repeats until the test passes.  
  * **Final Refinement**: Once the codebase is functionally correct and all tests pass, the crew can perform final "mop-up" operations. This includes tasks like generating documentation (e.g., "Add GDScript-compliant docstrings to all public methods in the migrated codebase"), enforcing style guide consistency, and identifying areas for performance optimization. This final pass ensures that the resulting project is not just a port, but a clean, maintainable, and professional Godot application.

#### **Works cited**

1. Framework for orchestrating role-playing, autonomous AI agents. By fostering collaborative intelligence, CrewAI empowers agents to work together seamlessly, tackling complex tasks. \- GitHub, accessed August 21, 2025, [https://github.com/crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)  
2. DeepSeek V2 vs Coder V2: A Comparative Analysis' \- Blog \- PromptLayer, accessed August 21, 2025, [https://blog.promptlayer.com/deepseek-v2-vs-coder-v2-a-comparative-analysis/](https://blog.promptlayer.com/deepseek-v2-vs-coder-v2-a-comparative-analysis/)  
3. DeepSeek-Coder-V2: Breaking the Barrier of Closed-Source Models in Code Intelligence \- GitHub, accessed August 21, 2025, [https://github.com/deepseek-ai/DeepSeek-Coder-V2](https://github.com/deepseek-ai/DeepSeek-Coder-V2)  
4. Build agentic AI solutions with DeepSeek-R1, CrewAI, and Amazon SageMaker AI, accessed August 21, 2025, [https://aihub.hkuspace.hku.hk/2025/02/11/build-agentic-ai-solutions-with-deepseek-r1-crewai-and-amazon-sagemaker-ai/](https://aihub.hkuspace.hku.hk/2025/02/11/build-agentic-ai-solutions-with-deepseek-r1-crewai-and-amazon-sagemaker-ai/)  
5. LLMs \- CrewAI Docs, accessed August 21, 2025, [https://docs.crewai.com/concepts/llms](https://docs.crewai.com/concepts/llms)  
6. DeepSeek API Docs: Your First API Call, accessed August 21, 2025, [https://api-docs.deepseek.com/](https://api-docs.deepseek.com/)  
7. Prompt Engineering for AI Agents \- PromptHub, accessed August 21, 2025, [https://www.prompthub.us/blog/prompt-engineering-for-ai-agents](https://www.prompthub.us/blog/prompt-engineering-for-ai-agents)  
8. Agentic AI Prompting: Best Practices for Smarter Vibe Coding \- Ran The Builder, accessed August 21, 2025, [https://www.ranthebuilder.cloud/post/agentic-ai-prompting-best-practices-for-smarter-vibe-coding](https://www.ranthebuilder.cloud/post/agentic-ai-prompting-best-practices-for-smarter-vibe-coding)  
9. Prompts that have improved agent code quality and reduced errors. : r/replit \- Reddit, accessed August 21, 2025, [https://www.reddit.com/r/replit/comments/1j5jjod/prompts\_that\_have\_improved\_agent\_code\_quality\_and/](https://www.reddit.com/r/replit/comments/1j5jjod/prompts_that_have_improved_agent_code_quality_and/)  
10. Create Custom Tools \- CrewAI Docs, accessed August 21, 2025, [https://docs.crewai.com/learn/create-custom-tools](https://docs.crewai.com/learn/create-custom-tools)  
11. subprocess — Subprocess management — Python 3.13.7 documentation, accessed August 21, 2025, [https://docs.python.org/3/library/subprocess.html](https://docs.python.org/3/library/subprocess.html)  
12. Retrieving the output of subprocess.call() in Python \- GeeksforGeeks, accessed August 21, 2025, [https://www.geeksforgeeks.org/python/retrieving-the-output-of-subprocesscall-in-python/](https://www.geeksforgeeks.org/python/retrieving-the-output-of-subprocesscall-in-python/)  
13. Qwen3-Coder: Agentic Coding in the World | Qwen, accessed August 21, 2025, [https://qwenlm.github.io/blog/qwen3-coder/](https://qwenlm.github.io/blog/qwen3-coder/)  
14. How to Use Qwen Code 3: Step-by-Step Guide to Alibaba's Open-Source Coding AI Model (2025) : r/gptbreezeio \- Reddit, accessed August 21, 2025, [https://www.reddit.com/r/gptbreezeio/comments/1m9q0b4/how\_to\_use\_qwen\_code\_3\_stepbystep\_guide\_to/](https://www.reddit.com/r/gptbreezeio/comments/1m9q0b4/how_to_use_qwen_code_3_stepbystep_guide_to/)  
15. How to Use Qwen3-Coder and Qwen Code \- DEV Community, accessed August 21, 2025, [https://dev.to/therealmrmumba/how-to-use-qwen3-coder-and-qwen-code-4g4p](https://dev.to/therealmrmumba/how-to-use-qwen3-coder-and-qwen-code-4g4p)  
16. Hands-on Tutorial: Build Your Own Coding Copilot with Qwen3-Coder, Qwen Code, and Code Context \- Milvus, accessed August 21, 2025, [https://milvus.io/blog/hands-on-tutorial-build-your-own-coding-copilot-with-qwen3-coder-qwen-code-and-code-context.md](https://milvus.io/blog/hands-on-tutorial-build-your-own-coding-copilot-with-qwen3-coder-qwen-code-and-code-context.md)  
17. Getting Started with Qwen3-Coder \- Analytics Vidhya, accessed August 21, 2025, [https://www.analyticsvidhya.com/blog/2025/07/getting-started-with-qwen3-coder/](https://www.analyticsvidhya.com/blog/2025/07/getting-started-with-qwen3-coder/)  
18. Qwen3-Coder: Open-Source AI for Deep Codebase Understanding | by My Social \- Medium, accessed August 21, 2025, [https://medium.com/aimonks/qwen3-coder-open-source-ai-for-deep-codebase-understanding-4d0d0ff48a35](https://medium.com/aimonks/qwen3-coder-open-source-ai-for-deep-codebase-understanding-4d0d0ff48a35)  
19. Introducing **Qwen-Code**: Alibaba's Open‑Source CLI for Agentic Coding with Qwen3‑Coder \- NYU Shanghai RITS, accessed August 21, 2025, [https://rits.shanghai.nyu.edu/ai/introducing-qwen-code-alibabas-open%E2%80%91source-cli-for-agentic-coding-with-qwen3%E2%80%91coder/](https://rits.shanghai.nyu.edu/ai/introducing-qwen-code-alibabas-open%E2%80%91source-cli-for-agentic-coding-with-qwen3%E2%80%91coder/)  
20. QwenLM/qwen-code: qwen-code is a coding agent that lives in digital world. \- GitHub, accessed August 21, 2025, [https://github.com/QwenLM/qwen-code](https://github.com/QwenLM/qwen-code)  
21. Qwen Code CLI: A Guide With Examples \- DataCamp, accessed August 21, 2025, [https://www.datacamp.com/tutorial/qwen-code](https://www.datacamp.com/tutorial/qwen-code)  
22. Prompt engineering overview \- Anthropic API, accessed August 21, 2025, [https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)  
23. How to build your agent: 11 prompting techniques for better AI agents \- Augment Code, accessed August 21, 2025, [https://www.augmentcode.com/blog/how-to-build-your-agent-11-prompting-techniques-for-better-ai-agents](https://www.augmentcode.com/blog/how-to-build-your-agent-11-prompting-techniques-for-better-ai-agents)


# **Architecting the C++ to Godot Migration: A Claude Code Orchestration Playbook**

## **Introduction**

The migration of a mature C++ codebase to a new game engine, such as Godot, represents a significant systems-engineering challenge. This process extends far beyond simple code translation; it is a high-risk, high-effort endeavor characterized by complex architectural refactoring, the generation of repetitive boilerplate code, and a substantial potential for human error.1 Traditional, manual porting methodologies are notoriously slow, inefficient, and difficult to scale.  
This playbook presents a semi-autonomous workflow designed to address these challenges by leveraging the Claude Code command-line interface as a sophisticated orchestration engine. The proposed solution moves beyond the paradigm of using an AI as an interactive assistant and instead architects a resilient, auditable, and highly automated system. By combining a structured, file-based state management protocol with Claude Code's native agentic features—specifically **Hooks** and **Sub-agents**—this framework manages the entire migration lifecycle, from initial planning to final validation.  
The central thesis of this report is that by architecting an event-driven agentic system, development teams can fundamentally de-risk complex migrations, accelerate project timelines, and elevate the role of the human developer. The developer transitions from a line-by-line implementer to a high-level AI supervisor and system architect, focusing on designing, monitoring, and refining the automated processes that drive the migration forward.

## **Section 1: Foundational Architecture: From Prescriptive Scripts to Event-Driven Agents**

The foundation of an effective AI-driven workflow lies in its architectural design. A comparison between a procedural, script-based approach and an integrated, event-driven model reveals the significant advantages of leveraging Claude Code's native features. The architectural evolution proposed here replaces brittle external scripts with a robust, reactive system that is tightly integrated into the agent's core operational loop.

### **1.1 Deconstructing the Reference Workflow**

An analysis of a well-architected procedural workflow provides a strong starting point.2 This reference model is built on several core principles: a three-phase development lifecycle (Plan, Implement, Validate), a markdown-based state management system for auditable tracking, a human-in-the-loop feedback protocol, and the use of custom commands to invoke the agent for specific tasks.  
The primary strengths of this model are its emphasis on repeatability and the creation of an auditable state. By storing task definitions, status, and feedback in version-controlled markdown files, the entire process becomes transparent and resilient.2 Furthermore, the explicit separation of a high-level planning phase from the implementation phase is a critical decision that de-risks the automation process by allowing for human review before any code is generated.2  
However, this model has inherent limitations. Its reliance on external shell scripts (e.g., initiate\_workflow.sh, run\_workflow.sh) for orchestration creates a loosely coupled system. The agent is invoked sequentially by an external process, limiting its awareness of the overall workflow state. This procedural design is less resilient than a reactive one; if the master script fails, the entire process halts, and state can be difficult to recover.

### **1.2 A Superior Paradigm: Claude Code's Integrated Orchestration**

Claude Code offers a more powerful and integrated paradigm for workflow orchestration through its native support for sub-agents and hooks.  
**Sub-agents** provide a formal, structured mechanism for creating the specialized AI personas that the reference playbook simulates via prompt engineering (e.g., "You are a senior software architect").2 Each sub-agent can be configured with its own dedicated system prompt, a restricted set of tools, and a separate context window, enabling true encapsulation of roles and responsibilities. This is a superior implementation for role-based task execution, ensuring consistency and focus.3  
**Hooks** are the central mechanism for replacing external orchestration scripts. They are user-defined shell commands that execute automatically at specific points in the agent's lifecycle, such as before or after a tool is used, or when a sub-agent completes its task.4 This provides deterministic control and allows for the creation of an event-driven system. For example, a  
SubagentStop hook can be configured to automatically trigger the validation phase immediately after an implementation sub-agent successfully completes its work, eliminating the need for an external script to manage this transition.

### **1.3 The Hybrid Architecture Blueprint**

The proposed architecture for the C++ to Godot migration is a hybrid model that combines the strengths of the reference workflow with the advanced capabilities of Claude Code.  
The robust markdown-based state management system is retained. Its human-readable and machine-parsable format is ideal for tracking task status, managing the feedback loop, and providing a clear "contract" between human supervisors and AI agents.2  
However, the external orchestration scripts are entirely replaced by a network of Claude Code hooks. This fundamental architectural shift transforms the workflow from a linear, prescriptive process managed by an external run\_workflow.sh script into a dynamic, event-driven state machine orchestrated from within the agent's own lifecycle. The control flow is no longer procedural but reactive. The system doesn't follow a rigid external script; it reacts to internal events as they occur. This makes the orchestration logic part of the agent's "nervous system," resulting in a more resilient, modular, and scalable system. New reactive behaviors can be added by defining new hooks without altering a monolithic master script.

| Playbook Concept 2 | Procedural Implementation | Claude Code Implementation | Advantage of Claude Code Approach |
| :---- | :---- | :---- | :---- |
| **Role Definition** | Prompt Engineering (You are a...) | **Sub-agents** 3 | Encapsulation, separate context, dedicated tools, role consistency. |
| **Workflow Orchestration** | Master Shell Script (run\_workflow.sh) | **Hooks** (e.g., SubagentStop, PostToolUse) 4 | Event-driven, resilient, tightly integrated, more modular. |
| **Task Execution** | Custom Commands (/workflow:implement) | **Sub-agent Invocation** (/task implement TASK-001) | Formal task delegation, clearer separation of concerns. |
| **Quality Gates** | Shell commands in prompt (\! scons) | **Hooks** (PostToolUse) or dedicated **QA Sub-agent** | Deterministic execution, separation from implementation logic. |

## **Section 2: Phase 1 \- Automated Migration Planning with a Godot Architect Sub-agent**

The initial planning phase is the most critical stage for de-risking a complex migration. Success depends on creating a detailed, actionable, and architecturally sound plan before any code is written. This requires a specialized agent with deep domain knowledge of the target platform: the Godot Engine and its C++ integration system.

### **2.1 The Challenge of C++ to Godot Migration**

Migrating a C++ codebase to Godot is not a line-by-line translation. It is an architectural refactoring task that requires a fundamental shift in thinking. Developers must embrace Godot's core concepts, such as the scene tree, nodes, and signals.1 Simply porting C++ logic without adapting it to the engine's architecture will result in a poorly integrated and inefficient game.  
For C++ integration in Godot 4, the native extension system is the modern, officially supported standard, replacing older integration methods from Godot 3\.5 Any migration workflow must be built upon this technology. This involves significant boilerplate and specific patterns, such as creating wrapper classes that inherit from Godot nodes, using the  
GDCLASS macro for registration, and implementing a static \_bind\_methods function to expose the C++ API to the Godot engine and GDScript.7 The primary challenge of migration, therefore, is this architectural mapping, not simple language translation.

### **2.2 Defining the "Godot Architect" Sub-agent**

To address this challenge, a specialized "Godot Architect" sub-agent is defined. This agent's sole purpose is to analyze the source C++ codebase and generate a structured migration plan that adheres to Godot's architectural best practices.  
The sub-agent is configured using a markdown file with YAML frontmatter, defining its name, description, and authorized tools (Read, Glob, Grep).3 The core of its specialization lies in its system prompt, which is meticulously engineered to guide its reasoning process. The prompt instructs the agent to act as a senior software architect, whose role is to devise a comprehensive implementation plan.2

1. Thoroughly analyze the existing codebase. Use file system tools to read relevant files and understand the current architecture, coding patterns, and dependencies.  
2. Break down the user story into a sequence of smaller, verifiable, and logically ordered implementation tasks.  
3. For each task, identify any dependencies on other tasks and create a preliminary list of files that are likely to be modified.  
4. Output the final plan as a single, well-formed JSON array of task objects. Each object must contain the keys: "id", "title", "dependencies", and "files\_to\_modify". The agent must not write or modify any code; its sole output is the JSON plan.2

This approach front-loads the most difficult architectural decisions into an automated, reviewable phase, preventing the project from proceeding with a flawed strategy.

| Sub-agent Name | Role/Purpose | Key System Prompt Directives | Authorized Tools 3 |
| :---- | :---- | :---- | :---- |
| **Godot Architect** | Plans the migration. | "You are a senior software architect. Analyze C++ source, map to Godot node architecture, decompose into native integration tasks, output JSON plan." 2 | Read, Glob, Grep |
| **C++ Engineer** | Implements a single task. | "You are an expert software engineer. Read task file, implement C++ native extension code, manage boilerplate, update task status, prioritize human feedback." 2 | Read, Write, Edit, Bash |
| **QA Engineer** | Validates implementation. | "You are a quality assurance engineer. Run build scripts, execute tests, capture all logs, report pass/fail via exit code." 2 | Bash |

### **2.3 Orchestrating the Planning Phase**

The workflow is initiated by the user with a simple command, delegating the planning to the specialized sub-agent: /task architect "Migrate the PlayerController module from src/player."  
Once the Godot Architect sub-agent completes its analysis and outputs the JSON plan, the automation continues. A UserPromptSubmit or SessionStart hook is configured to trigger a helper script.4 This script intercepts the JSON output, parses it, and automatically materializes the plan into the file-based state system. It creates an individual markdown file for each task in the  
.claude\_workflow/tasks/ directory, populating it with the ID, title, dependencies, and other metadata from the plan. This step fully automates the state initialization process, creating a concrete set of stateful artifacts that will drive the rest of the migration.

## **Section 3: Phase 2 \- C++ Implementation and the Human-in-the-Loop Cycle**

With a structured plan in place, the workflow transitions to the implementation phase. This phase is designed as a tight, collaborative loop between a specialized implementation agent and a human supervisor, with all interactions managed and audited through the stateful task files.

### **3.1 The "C++ Engineer" Sub-agent**

The "C++ Engineer" sub-agent is the workhorse of this phase. Its system prompt is engineered to execute a single task file with precision, following the instructions laid out by the Architect. The prompt directs the agent to act as an expert software engineer and follow a specific process.2

* **State Management:** Read the specified task file and immediately update its status to in\_progress.  
* **Prioritize Feedback:** Critically, the agent must check for a "\#\# Feedback" section in the markdown file. If it exists, it must prioritize addressing this feedback above all other instructions.2  
* **Implementation:** Execute the steps in the "Acceptance Criteria" checklist, using code editing tools to modify the specified files.  
* **Finalize State:** After successfully applying all changes, update the markdown file again by marking checklist items as complete and changing the status to completed.2

### **3.2 The Collaborative Refinement Protocol**

No AI agent is infallible, making human oversight an essential component of a robust workflow. This protocol implements a feedback loop that is stateful, auditable, and fully integrated into the task management system.  
The process follows a clear, structured cycle:

1. The C++ Engineer agent completes its first implementation pass for a given task.  
2. A human developer reviews the generated code changes, typically using a command like git diff.  
3. If corrections are required, the reviewer **does not** modify the code directly. Instead, they open the relevant markdown task file (e.g., .claude\_workflow/tasks/TASK-002.md) and add a new section titled \#\# Feedback.  
4. Within this section, the reviewer provides clear, actionable instructions. For example:  
   * "The \_bind\_methods implementation is missing the health property. Please add it using ClassDB::bind\_method and ADD\_PROPERTY."  
   * "Refactor the physics calculation to use Godot's built-in Vector3 math functions for better performance instead of the custom math library."  
5. The implementation command (/task engineer TASK-002) is executed again.

The system prompt for the Engineer sub-agent contains a **critical directive** to always check for a \#\# Feedback section upon reading a task file and to prioritize addressing this feedback above all other acceptance criteria. This ensures that human corrections are acted upon immediately in the next iteration.2  
This methodology transforms the markdown task file from a simple to-do list into a comprehensive "contract and conversation record." It contains not only the original plan but also a full history of implementation attempts, human reviews, and corrections. This creates a persistent, version-controlled, and asynchronous audit trail of the entire collaborative process, which is far superior to relying on ephemeral, out-of-band chat history. Any team member can later inspect the task file and understand not just *what* was implemented, but the full history of *why* the code evolved to its current state.

## **Section 4: Phase 3 \- Integrated Quality Gates and Automated Remediation with Hooks**

The validation phase acts as a critical quality gate, ensuring that the agent's contributions are correct, adhere to project standards, and do not introduce regressions. By leveraging Claude Code hooks, this phase can be transformed into a fully automated, self-correcting loop where the agent is tasked with fixing its own errors.

### **4.1 Defining the Quality Gates**

For a C++ native extension project, the primary quality gate is successful compilation. The build process, typically managed by SCons or CMake, serves as the first and most important validation step.9 Additional gates can include running unit tests, integration tests, or static analysis tools.  
To manage this, a simple "QA Engineer" sub-agent is defined. Its sole responsibility is to execute these quality checks. Its prompt instructs it to act as a quality assurance engineer, execute a sequence of quality checks using its shell tool, and capture all stdout and stderr. If any command fails, it must save the complete, unabridged output to a log file.2

### **4.2 The SubagentStop Hook: The Automation Linchpin**

The key to automating the transition from implementation to validation is a SubagentStop hook. This hook is configured in the project's .claude/settings.json file to act as a listener for a specific event in the agent's lifecycle.4

* **Matcher:** The hook is configured with a matcher that causes it to trigger *only* when the "C++ Engineer" sub-agent successfully completes a task.  
* **Command:** The command executed by the hook is a shell script (scripts/trigger\_validation.sh). This script receives data about the completed task (such as its ID) via stdin from the hook event. Its job is to immediately invoke the "QA Engineer" sub-agent on that same task ID: /task qa\_engineer TASK-001.

This hook creates a causal chain of agentic actions. The successful completion of the implementation task *causes* the initiation of the validation task, creating a domino effect of automated work that is far more robust than a procedural loop in an external script.

### **4.3 Closing the Loop: Automated Remediation**

The most advanced stage of the workflow is the self-correcting remediation loop, which is orchestrated by a combination of hooks and scripts.

1. **Failure Detection:** Following the validation run by the QA agent, another hook or script checks the agent's exit code. A non-zero exit code signifies a failure.  
2. **Automated Feedback Generation:** Upon detecting a failure, an automation script locates the corresponding failure log (e.g., .claude\_workflow/logs/TASK-001-failure.log).2  
3. **State Update:** The script then appends the entire, unabridged log content to the \#\# Feedback section of the relevant task markdown file. It is prefixed with a clear header, such as \#\# Feedback (Automated from Validation Failure), to distinguish it from human feedback.  
4. **Re-invocation:** Finally, the script re-invokes the "C++ Engineer" on the same task.

Because the Engineer agent is programmed to prioritize the feedback section, it now sees the compilation error or test failure as its most important instruction. It will then attempt to remediate the very issue it introduced in the previous step. This creates a powerful, autonomous cycle of implementation, testing, and bug-fixing, significantly increasing the workflow's level of autonomy.2

| Trigger Event 4 | Matcher | Hook Command/Script | Purpose |
| :---- | :---- | :---- | :---- |
| **SubagentStop** | C++ Engineer | scripts/trigger\_validation.sh | Automatically starts the QA/validation phase upon successful implementation. |
| **PostToolUse** | Bash (when running scons) | scripts/check\_build\_status.sh | Checks the build's exit code; if it fails, triggers automated feedback generation and re-invocation. |
| **PreToolUse** | \`Edit | Write\` | scripts/protect\_files.sh |

## **Section 5: The Migration Blueprint: A Practical C++ Integration Workflow in Action**

To make the architectural concepts tangible, this section provides a concrete, end-to-end walkthrough of the workflow, demonstrating the migration of a representative C++ class.

### **5.1 The Target: Migrating a C++ SimpleEnemyAI Class**

Consider a simple C++ class from the legacy codebase:

C++

// src/ai/SimpleEnemyAI.h  
class SimpleEnemyAI {  
public:  
    void update\_logic(float delta);  
    void take\_damage(int amount);  
private:  
    float health \= 100.0f;  
    float speed \= 50.0f;  
};

### **5.2 Step-by-Step Orchestration**

1. **Planning:** The user initiates the process: /task architect "Migrate src/ai/SimpleEnemyAI.h". The "Godot Architect" analyzes the file, determines it represents a mobile entity, and produces a JSON plan. A hook intercepts this JSON and materializes it into task files, such as TASK-001-Setup-Native-Class.md (to create the boilerplate inheriting from CharacterBody2D) and TASK-002-Bind-Methods-and-Properties.md.  
2. **Implementation (Task 1):** A script or user runs /task engineer TASK-001. The "C++ Engineer" creates src/enemy\_ai.h and src/enemy\_ai.cpp, adding the necessary godot-cpp includes and the GDCLASS(EnemyAI, CharacterBody2D) boilerplate. It updates the task file status to completed.  
3. **Validation (Task 1):** The SubagentStop hook for the Engineer fires, invoking the "QA Engineer." The QA agent runs scons, which succeeds as only boilerplate has been added. The task is validated.  
4. **Implementation (Task 2):** The workflow proceeds with /task engineer TASK-002. The agent attempts to implement \_bind\_methods to expose update\_logic, take\_damage, health, and speed. However, it makes a syntax error, using an incorrect macro for binding the take\_damage method. It incorrectly marks the task as completed.  
5. **Automated Remediation (Task 2):** The SubagentStop hook fires again, triggering the QA agent. This time, scons fails with a clear compiler error pointing to the incorrect macro in \_bind\_methods. A script triggered by the failure appends the exact compiler output to TASK-002.md under the automated feedback section.  
6. **Self-Correction (Task 2):** The workflow automatically re-runs /task engineer TASK-002. The agent reads the task file, sees the compiler error in the \#\# Feedback section, identifies its mistake, and corrects the syntax for the ClassDB::bind\_method call.  
7. **Final Validation (Task 2):** The agent completes its work. The SubagentStop hook triggers the QA agent one last time. Now, scons runs successfully, and the build completes. The task is finally and correctly validated.

### **5.3 Best Practices for Native Extension Structure**

The final native C++ module produced by this workflow would consist of several key files:

* **Extension Configuration File**: A configuration file (e.g., with a .gdextension suffix) that tells Godot how to load the library, specifying the entry symbol and paths to the compiled dynamic libraries for each platform.1  
* **SConstruct**: The build script used by SCons to compile the C++ source code, link against the godot-cpp static library, and produce the final shared library (.dll, .so, or .dylib).8  
* **src/register\_types.cpp**: The file containing the library's entry point, which registers all the custom classes (like EnemyAI) with Godot's ClassDB during the appropriate initialization level.1

## **Section 6: Advanced Strategies: Scaling and Hardening the Workflow**

With the core workflow established, several advanced strategies can be implemented to scale its capabilities and harden it for enterprise-level use, further reducing manual intervention and handling more complex real-world scenarios.

### **6.1 Seamless Git Integration with Hooks**

The workflow can be extended to interact directly with the version control system, fully automating the branching and review process.

* **Automated Branching:** A PreToolUse hook can be configured to trigger when the "C++ Engineer" is about to start work.4 This hook can execute a script that automatically creates and switches to a new feature branch based on the task ID (e.g.,  
  git checkout \-b feature/TASK-001). This isolates work for each task and keeps the main branch clean.  
* **Automated Commits and Pull Requests:** Upon successful final validation of a task, a SubagentStop hook on the "QA Engineer" can trigger a script to perform Git operations. This script can stage the changes, create a commit with a standardized message referencing the task ID, and even use a command-line tool like the GitHub CLI to open a pull request for human review.

### **6.2 Managing External C++ Dependencies**

Real-world C++ projects rarely exist in isolation; they often rely on third-party libraries for physics, audio, networking, or other functionalities. Migrating such a project requires correctly binding these external dependencies within the Godot ecosystem, a non-trivial task.8  
This complexity can be managed by introducing another specialized sub-agent: a "Dependency Analyst." During the planning phase, this agent would be tasked with parsing the legacy project's build files (CMakeLists.txt, Makefiles) and source code (\#include statements) to identify all external libraries. The output of this analysis would be a list of dependencies, which can then be used to generate new tasks for the "C++ Engineer." These tasks would involve modifying the SConstruct file to include the necessary header paths, library paths, and linker flags to correctly compile and link the third-party libraries into the final native extension.

### **6.3 Performance Considerations: C++ vs. GDScript**

While native C++ integration provides the highest possible runtime performance for computationally intensive algorithms, it is not always the optimal choice. GDScript, being tightly integrated with the engine, can often be faster for making frequent calls to Godot's internal APIs, and its interpreted nature offers a significantly faster development and iteration workflow.  
A truly advanced workflow should account for this trade-off. The "Godot Architect" sub-agent's prompt can be enhanced with strategic guidance. It can be instructed to analyze the function of the C++ code being migrated and make an informed recommendation. For performance-critical systems like complex simulations, custom physics, or heavy data processing, it should recommend a native C++ port. For simpler game logic, UI management, or "glue code" that primarily orchestrates engine features, it could recommend a complete rewrite in GDScript, generating tasks for a different "GDScript Engineer" agent. This adds a layer of strategic optimization to the planning phase, ensuring that the right tool is used for the right job.

## **Conclusion**

The orchestrated workflow detailed in this report presents a robust and scalable solution for the complex challenge of migrating C++ codebases to the Godot Engine. By synthesizing a structured, file-based state management protocol with the native agentic capabilities of Claude Code, the system achieves a high degree of automation, resilience, and auditability. The synergy between specialized sub-agents, which encapsulate expert roles, and event-driven hooks, which provide deterministic orchestration, forms the architectural core of this advanced framework.  
This model represents a significant evolution from using AI as a simple interactive assistant to employing it as the engine of a digital software engineering assembly line. Consequently, the role of the human developer is elevated. Their primary responsibilities shift from the minutiae of line-by-line implementation to the higher-level tasks of system design, process architecture, and AI supervision. The developer becomes the architect of the automated workflow itself, engineering the prompts that define agent behavior and providing the critical oversight that guides the system to a successful outcome. This paradigm of orchestrated, multi-agent systems, managed by human experts, points toward the future of AI-driven software development, capable of tackling the most complex engineering challenges with unprecedented efficiency and reliability.

#### **Works cited**

1. C++ usage guidelines — Godot Engine (latest) documentation in English, accessed August 28, 2025, [https://docs.godotengine.org/en/latest/contributing/development/cpp\_usage\_guidelines.html](https://docs.godotengine.org/en/latest/contributing/development/cpp_usage_guidelines.html)  
2. Architecting the Modern Development Lifecycle: A Complete Workflow Orchestration Playbook for the Qwen Code CLI  
3. Subagents \- Anthropic \- Anthropic API, accessed August 28, 2025, [https://docs.anthropic.com/en/docs/claude-code/sub-agents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)  
4. Get started with Claude Code hooks \- Anthropic, accessed August 28, 2025, [https://docs.anthropic.com/en/docs/claude-code/hooks-guide](https://docs.anthropic.com/en/docs/claude-code/hooks-guide)  
5. Introducing GDNative's successor, GDExtension – Godot Engine, accessed August 28, 2025, [https://godotengine.org/article/introducing-gd-extensions/](https://godotengine.org/article/introducing-gd-extensions/)  
6. GDNative Replaced with GDExtension in Godot 4 – \- GameFromScratch.com, accessed August 28, 2025, [https://gamefromscratch.com/gdnative-replaced-with-gdextension-in-godot-4/](https://gamefromscratch.com/gdnative-replaced-with-gdextension-in-godot-4/)  
7. godotengine/godot-cpp: C++ bindings for the Godot script API \- GitHub, accessed August 28, 2025, [https://github.com/godotengine/godot-cpp](https://github.com/godotengine/godot-cpp)  
8. Binding to external libraries — Godot Engine (stable) documentation in English, accessed August 28, 2025, [https://docs.godotengine.org/en/stable/contributing/development/core\_and\_modules/binding\_to\_external\_libraries.html](https://docs.godotengine.org/en/stable/contributing/development/core_and_modules/binding_to_external_libraries.html)  
9. C++ usage guidelines — Godot Engine (4.3) documentation in English, accessed August 28, 2025, [https://docs.godotengine.org/en/4.3/community/contributing/cpp\_usage\_guidelines.html](https://docs.godotengine.org/en/4.3/community/contributing/cpp_usage_guidelines.html)  
10. GDExtension C++ example — Godot Engine (4.4) documentation in English, accessed August 28, 2025, [https://docs.godotengine.org/en/4.4/tutorials/scripting/gdextension/gdextension\_cpp\_example.html](https://docs.godotengine.org/en/4.4/tutorials/scripting/gdextension/gdextension_cpp_example.html)
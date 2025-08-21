

# **The Centurion Blueprint: An Agentic Framework for the Modernization of Wing Commander Saga**

## **Section 1: The Command & Control Architecture: Orchestrating the Migration Crew**

The modernization of a complex, legacy codebase such as *Wing Commander Saga* requires a strategy that transcends manual refactoring or simple, monolithic AI assistance. It necessitates a structured, intelligent, and automated system capable of strategic planning, task decomposition, and precise code execution. This section outlines the design of such a system: an Agentic Command Center built on a hierarchical multi-agent framework. This architecture establishes a clear division of cognitive labor, from high-level strategic planning down to the execution of atomic code modifications, all orchestrated through a robust and extensible set of custom tools.

### **1.1. The Definitive Migration Crew: A Synthesis of Specialized Roles**

The foundation of this migration strategy is a multi-agent system, architected using the principles of frameworks like CrewAI.1 This system is not a mere collection of conversational agents but a purpose-built command crew, where each agent is assigned a specific role, goal, and operational context. This specialization ensures that each component of the migration process is handled by an expert system, leading to higher quality outcomes and greater efficiency.1 The crew is composed of several specialist agents:

* **Migration Architect:** This agent serves as the strategic commander of the crew. Upon receiving the initial human directive—"Migrate Wing Commander Saga to Godot"—it analyzes the project's scope and decomposes it into major, logically sequenced phases, such as "Phase 1: Port Core Systems," "Phase 2: Convert Game Logic," and "Phase 3: Refactor for Godot API Integration." This agent sets the overarching agenda for the entire crew and is responsible for the strategic sequencing of the project.1  
* **Codebase Analyst:** The intelligence officer of the operation. This agent is equipped with custom parsing tools to analyze the unique file formats of the *Wing Commander Saga* / FreeSpace 2 codebase, including .tbl files for game data, .pof files for 3D model metadata, and .fs2 mission files for SEXP-based logic.3 Its primary goal is to produce a structured, machine-readable (JSON) representation of any given game entity, detailing its data, dependencies, and architectural components. This analysis forms the core of the dynamic and task-specific memory layers.  
* **Task Decomposition Specialist:** This agent acts as the operational planner, translating the Architect's high-level phases into a granular backlog of atomic, executable tasks. It performs the "task sharding" function described in the BMAD methodology, breaking down a goal like "Port the GTCv Sobek corvette" into a series of unambiguous, self-contained steps suitable for the execution layer.1  
* **Prompt Engineering Agent:** A critical meta-agent that functions as the communication officer between the command crew and the execution layer. Its goal is to take a decomposed task from the Task Decomposition Specialist and the relevant code context from the Codebase Analyst and synthesize them into a perfectly formatted, unambiguous, and context-rich prompt for the qwen-code CLI tool.1 The separation of this role from the Task Decomposition Specialist is a crucial architectural decision. It decouples the "what to do" (the task) from the "how to ask for it" (the prompt). This modularity ensures that if the execution tool (  
  qwen-code) is ever updated or replaced, only the PromptEngineeringAgent's templates and logic need to be modified, leaving the entire strategic and planning layer of the crew untouched. This applies the software engineering principle of "separation of concerns" to the agentic architecture itself, enhancing maintainability and adaptability.  
* **Refactoring Specialist (Execution Layer):** This is not a cognitive agent within the crew but rather the role fulfilled by the qwen-code CLI tool itself.2 It is the "hands" of the operation, receiving precise prompts from the crew and performing the actual file modifications and code generation.  
* **Quality Assurance Agent:** The verification and control officer. This agent receives the structured output from the execution tool, analyzes the results (return code, stdout, stderr), diagnoses failures, and orchestrates the self-correction loop by re-engaging the Prompt Engineering Agent with detailed error context.1

### **1.2. The Orchestration Process Model: Hybrid Control in CrewAI**

The choice of an orchestration framework must balance the need for predictable, repeatable execution with the flexibility to handle the unforeseen complexities of legacy code.2 CrewAI is the optimal choice for this project due to its hybrid process model, which allows for both deterministic flows and autonomous collaboration.1

* **Hierarchical Process for Strategic Oversight:** The overall project will be managed using a Process.hierarchical model. In this configuration, the Migration Architect acts as the manager, delegating high-level phases to subordinate agents or even instantiating entire sub-crews to work on different modules in parallel (e.g., a "UI Crew" and a "Physics Crew").1 This structure provides the scalability and high-level control necessary for a project of this magnitude.  
* **Sequential Process for Tactical Execution:** Each atomic migration task, termed a "bolt," will be executed using a Process.sequential workflow.1 This ensures a deterministic, auditable sequence for every unit of work:  
  Analysis \-\> Task Decomposition \-\> Prompt Engineering \-\> Execution \-\> QA Validation. This mirrors the structured, process-driven approach of the BMAD framework, ensuring consistency and predictability at the micro-level.4

### **1.3. The Execution Bridge: A Robust Interface for the Qwen3 Coder**

The conceptual work of the high-level agent crew can only be translated into tangible code changes through a physical interface to the development environment. This bridge is a custom tool designed to execute shell commands non-interactively and report the results back to the crew.1  
A significant operational hurdle is that qwen-code's primary interface is an interactive, chat-based CLI, which is fundamentally incompatible with the non-interactive, automated workflow required by the agentic crew.1 A simple  
subprocess.run command is insufficient. To overcome this, the custom QwenCodeExecutionTool must use the lower-level subprocess.Popen interface. This allows the tool to start the qwen-code process, programmatically write the generated prompt to the process's stdin stream, and then read the resulting code from its stdout stream. This technique effectively wraps the interactive tool, transforming it into a controllable, non-interactive component that the automated system can control.1  
This tool is not merely a utility; it is the system's actuator and sensor. Its design directly defines the bandwidth and fidelity of the agent crew's interaction with the file system. A poorly designed tool that only returns a success/fail boolean would blind the Quality Assurance Agent. The QwenCodeExecutionTool will be designed to return a structured string or JSON object containing the returncode, stdout, and stderr.1 This structured data is not just for logging; it is the essential sensory input for the Quality Assurance Agent's diagnostic and self-correction logic. This rich data is what enables sophisticated, autonomous error diagnosis and correction, meaning investment in the robustness of this single tool has a multiplicative effect on the intelligence and resilience of the entire system.  
The following table provides a comprehensive, at-a-glance reference for the entire agentic system, detailing each agent's role, primary goal, key tools, and the recommended underlying AI model.  
**Table 1: The Definitive Migration Crew Configuration**

| Agent Role | Persona/Goal | Key Tools | Recommended Model |
| :---- | :---- | :---- | :---- |
| **Migration Architect** | The "Strategic Commander" responsible for creating the high-level, multi-phase migration plan. | File System API | Claude 3.5 Sonnet |
| **Codebase Analyst** | The "Intelligence Officer" responsible for parsing legacy files (.tbl, .pof, .fs2) and creating structured JSON reports. | Custom Parsers, File System API | Claude 3.5 Sonnet |
| **Task Decomposition Specialist** | The "Operational Planner" responsible for sharding high-level phases into a granular backlog of atomic tasks. | Task Management API | Claude 3.5 Sonnet |
| **Prompt Engineering Agent** | The "Communications Specialist" responsible for converting tasks and context into precise prompts for the execution layer. | Template Engine | Claude 3.5 Sonnet |
| **Refactoring Specialist** | The "Developer" role fulfilled by the execution tool, responsible for all code generation and modification. | qwen-code CLI | Qwen3 Coder |
| **Quality Assurance Agent** | The "Verification Officer" responsible for validating results and orchestrating the self-correction loop. | QwenCodeExecutionTool, Godot CLI, SAST Tool CLI | Claude 3.5 Sonnet |

## **Section 2: The System's Cognition: A Multi-Layered Memory Strategy for Consistency**

A successful migration is impossible if the agents operate with incomplete or inconsistent context. A critical flaw in many multi-agent systems is context truncation or the loss of conversation history, leading to repeated steps and flawed reasoning.5 This blueprint addresses that challenge directly by defining a three-tiered memory architecture that ensures coherence from the project's foundational principles down to the execution of a single line of code. This structure forms a cognitive hierarchy that mirrors human problem-solving. By separating memory into distinct layers, the system prevents cognitive overload on the LLMs; the  
qwen-code agent, for instance, does not need to know the entire project's dependency graph to refactor a single function, it only needs its specific task package. This is a crucial strategy for managing context windows and reducing API costs.

### **2.1. Static Memory: The Immutable Guidance Layer**

This layer comprises the human-engineered "guidance artifacts" that form the project's constitution. They are written once during the initial context engineering phase and are injected into the prompts of the relevant agents to ensure every action aligns with the project's architectural vision.2

* **STYLE\_GUIDE.md:** The definitive rulebook for GDScript conventions (e.g., PascalCase for classes, snake\_case for functions), mandatory static typing, file system structure, and scene composition rules.2  
* **Scaffolding Templates:** Parameterized templates for Godot files (.tscn, .tres, .gd) that enforce correct syntax and structure. This transforms a generative task into a less error-prone "fill-in-the-blanks" task for the AI.2  
* **"Gold Standard" Examples:** A curated set of manually migrated, perfect code examples. These serve as powerful few-shot prompts for the qwen-code agent and as a baseline for automated quality validation by the Quality Assurance Agent.2  
* **The "WCS-to-Godot Architectural Mapping Table":** The project's "Rosetta Stone," providing a definitive, machine-readable mapping from legacy C++/FS2 concepts to their idiomatic Godot equivalents. This is the single most important artifact for ensuring architectural consistency.2

### **2.2. Dynamic Memory: The Evolving Codebase Model**

This layer represents the system's long-term, evolving understanding of the entire project. It is created and updated by the Codebase Analyst and serves as the shared context for all high-level planning and dependency management.

* **Initial Codebase Analysis:** In the project's first phase, the Codebase Analyst will perform a full scan of the *Wing Commander Saga* C++ source code to generate a comprehensive dependency graph.1 This graph reveals foundational modules (e.g., math libraries, core data structures) that must be migrated first to prevent cascading failures.  
* **Persistent Architectural Model:** This dependency graph will be persisted (e.g., as a graph database file or a structured JSON/YAML file). As the migration progresses and files are converted to GDScript, this model will be updated. This provides the Migration Architect with an always-current view of the project's state, allowing it to make intelligent decisions about task sequencing and identify potential integration issues before they arise.

### **2.3. Ephemeral Memory: The Task-Specific Context Package**

This is the short-term, "working memory" assembled by the planning agents for a single, atomic "bolt" cycle. It is a self-contained package of information that provides the execution layer with everything it needs to complete one task, ensuring context is not lost during execution.1 For each task, the system will assemble a package containing:

1. The full source code of the C++ file(s) to be migrated.  
2. The structured JSON report from the Codebase Analyst, which includes parsed data from relevant .tbl, .pof, and .fs2 files.3  
3. Pointers to, or snippets from, the relevant static memory artifacts (e.g., a specific rule from the Mapping Table).  
4. In the case of a retry, the full error log (stdout and stderr) from the previous failed attempt.1

The "Gold Standard" examples in the static memory layer are not just prompts; they are the seeds of a self-improving system. When the Quality Assurance Agent escalates an intractable problem to the "human intervention required" queue, the human's solution should be captured. The final step of the human's intervention process should be to convert their fix into a new "Gold Standard" example and add it to the static memory. This creates a feedback loop where human expertise is used to programmatically and permanently upgrade the AI's knowledge base, reducing the likelihood of similar failures in the future. The system does not just get work done; it gets smarter over time.  
The "Rosetta Stone" table below is the most critical piece of static memory, providing a definitive rulebook that translates every key concept from the legacy architecture to its idiomatic Godot equivalent.  
**Table 2: WCS-to-Godot Architectural Mapping Table**

| C++ / FS2 Concept | Godot Idiomatic Equivalent | Agentic Implementation Rule |
| :---- | :---- | :---- |
| ships.tbl Entry | Custom ShipData.tres Resource | **MUST** create a ShipData.gd script extending Resource with @export variables for all relevant stats (hull, shields, speed, etc.). For each entry in ships.tbl, parse the data and generate a corresponding .tres file. |
| .pof Model File | A Ship.tscn Scene | **MUST** create a new Scene. The root node **MUST** be a CharacterBody3D. Geometry **MUST** be imported as a child MeshInstance3D. Subsystems, gun points, and thrusters from .pof metadata **MUST** be created as child Node3D markers. |
| C++ Singleton Manager | Autoload Singleton | **MUST** identify singleton patterns. Create a corresponding GDScript (e.g., AudioManager.gd) and add it to the project's Autoload list. All static calls **MUST** be replaced with direct calls to the Autoload's global name. |
| Direct Method Calls | Decoupled communication via Signals | **MUST** analyze object interactions. Direct method calls between distinct objects **MUST** be refactored. The calling object emits a signal (e.g., hit\_detected), and the target object connects its damage() method to that signal. |
| SEXP Mission Script (.fs2) | Godot Scene with a MissionLogic.gd script | **MUST** parse the .fs2 file. Initial ship placements become PackedScene.instantiate() calls in the \_ready() function. SEXP event triggers **MUST** be translated into connections to Godot signals (e.g., tree\_exiting for a destroyed ship). |

## **Section 3: The Migration Engine: Persistent Task Management and the Automated "Bolt" Cycle**

This section details the operational heart of the system. It provides a formal specification for the task management and persistence layer and provides a granular, step-by-step walkthrough of the core execution loop that drives the migration.

### **3.1. Task Sharding and the Persistent Task Queue**

A robust system for task management is essential for an operation of this scale. The system moves from the abstract concept of "task sharding" 4 to a persistent, auditable system.

* **The Sharding Process:** The Task Decomposition Specialist agent will consume the Migration Architect's plan and break it down into atomic tasks. An atomic task is defined as "the migration of a single, self-contained WCS/FS2 entity" (e.g., one ship class, one weapon type).  
* **The Persistent Queue:** All sharded tasks will be written to a central, persistent file, task\_queue.yaml. This file serves as the single source of truth for the project's status. The system will read from and write to this file, ensuring that progress is saved and the migration can be paused and resumed. The choice of a human-readable format like YAML is strategic; it allows human operators to monitor the AI's progress in real-time and manually intervene by editing priorities or adding context to a failing task. This file becomes the primary human-machine interface for managing the project's low-level execution.  
* **Task Schema:** Each entry in task\_queue.yaml will follow a defined schema, tracking not just the task itself but also its state and history.

The following table defines the precise YAML structure for a single task entry, providing a concrete, implementable schema for the core task management system.  
**Table 3: Persistent Task Queue Schema (task\_queue.yaml)**

| Field | Type | Description |
| :---- | :---- | :---- |
| task\_id | String | A unique identifier for the task (e.g., SHIP-GTC\_FENRIS). |
| description | String | A human-readable description of the task (e.g., "Migrate the GTC Fenris cruiser"). |
| source\_files | List | A list of all source file paths required for this task (e.g., ships.tbl, fenris.pof). |
| dependencies | List | A list of task\_ids that must be completed before this task can start. |
| status | String | The current state of the task: pending, in\_progress, completed, failed, escalated\_human\_review. |
| retry\_count | Integer | The number of times this task has been attempted. |
| failure\_logs | List\[Object\] | A list of structured logs from previous failed attempts, including the prompt and the full error output. |

### **3.2. The Anatomy of a "Bolt": A Single Execution Cycle**

The migration proceeds in a series of discrete, automated "bolts," each targeting a single task from the persistent queue. This workflow ensures a methodical and verifiable process for each component of the codebase.1 A single bolt follows this precise sequence:

1. **Task Selection:** The Orchestrator polls task\_queue.yaml and selects the next task with status: pending. It updates the status to in\_progress.  
2. **Context Assembly:** The Orchestrator assembles the ephemeral memory package for the selected task.  
3. **Analysis & Decomposition:** The task is passed to the Codebase Analyst and Task Decomposition Specialist.  
4. **Prompt Engineering:** The Prompt Engineering Agent receives the task details and context, and generates the precise, tactical prompt for qwen-code.  
5. **Execution:** The command is passed to the QwenCodeExecutionTool, which invokes qwen-code and captures the structured result.  
6. **Validation:** The Quality Assurance Agent receives the result, runs validation checks (compilation, tests, linting, security scans), and determines success or failure. If successful, the task status is updated to completed.

### **3.3. The Self-Correction Loop and the Circuit Breaker**

The system's resilience is built upon an autonomous feedback mechanism, which is triggered upon validation failure.1

* **Failure as Data:** A failure is not an end state but a data point. The QA Agent's primary role upon failure is to diagnose the root cause from the execution tool's output.  
* **Contextual Retry:** The QA Agent formulates a new meta-task for the Prompt Engineering Agent, which includes the original context *plus* the specific error message from the failed attempt. The retry\_count for the task in task\_queue.yaml is incremented, and the error log is appended to the failure\_logs list.  
* **The Circuit Breaker:** The Orchestrator will enforce a max\_retries limit (e.g., 3). If retry\_count exceeds this limit, the circuit breaker trips. The task's status in task\_queue.yaml is changed to escalated\_human\_review, and it is moved to a separate queue for human intervention.2 This pattern is more than just an error-handling mechanism; it is an automated data-gathering tool. By analyzing the tasks that consistently get escalated, the engineering team can identify systemic weaknesses in the agentic system. The human review queue is therefore not just a bug list; it is a prioritized, data-driven roadmap for improving the entire agentic system itself.

## **Section 4: Strategic Governance and Performance Measurement**

This final section addresses the critical human-AI interface and establishes a framework for measuring the project's success. It defines the elevated role of human engineers and proposes a set of Key Performance Indicators (KPIs) tailored to the unique dynamics of an AI-driven migration.

### **4.1. The Elevated Role of Human-in-the-Loop Governance**

In this agentic workflow, the role of the human engineer is fundamentally transformed from tactical implementer to strategic overseer. The agents handle the 80% of migration work that is repetitive and pattern-based, freeing experienced engineers to focus on the 20% that requires deep expertise and creative problem-solving.2 Their primary responsibilities become:

* **Upfront Strategy:** The initial, human-led creation of the guidance artifacts in the static memory layer. This is the highest-leverage activity in the entire project.  
* **Expert Review & Approval:** The final review of successful, AI-generated pull requests. The focus is on architectural integrity, subtle logic bugs, and overall quality, not on trivial syntax.  
* **Edge Case Intervention:** Acting as "level two support" by diagnosing and fixing the complex problems escalated by the circuit breaker. This role includes improving the system's static memory based on the solutions, thereby training the system.  
* **Final Authorization:** Maintaining ultimate human accountability by providing the final sign-off for merging and deploying code.

### **4.2. Measuring Success: A New KPI Framework for Agentic Migration**

To accurately measure the return on investment (ROI) and overall success of this initiative, traditional software development metrics are insufficient. A new set of KPIs must be adopted to reflect the unique value drivers of an agentic approach.2  
The "Idiomatic Score" KPI is not just a quality metric; it is a direct measure of the effectiveness of the static memory layer. A consistently high score indicates that the style guides, templates, and gold standard examples are clear and effective. A declining or low score provides a clear signal to the human team that the guidance artifacts are insufficient or ambiguous and need to be improved. This KPI creates a direct feedback loop for the quality of the human-led context engineering phase.  
The entire agentic system, as designed, is a prototype for a permanent, in-house "Automated Refactoring and Modernization (ARM)" platform.2 The true, long-term ROI of this project is not just the successful migration of  
*Wing Commander Saga*. It is the creation of a reusable strategic asset—the crew, the tools, the processes, and the refined guidance artifacts. This platform can be re-tasked for future modernizations (e.g., Godot 4 to Godot 5, GDScript to C\#), turning a one-off technical debt payment into a perpetual engineering capability. This reframes the entire project from a cost center to a strategic investment in the organization's future development velocity.  
The following table summarizes the key performance indicators, providing a clear dashboard for project stakeholders to track success.  
**Table 4: KPI Framework for Agentic Migration**

| KPI | Measurement | Strategic Question Answered |
| :---- | :---- | :---- |
| **Migration Velocity** | Number of WCS entities/C++ classes successfully migrated, validated, and merged per week. | How fast is the system completing the project? |
| **AI Contribution Rate** | Percentage of lines of code in the final merged project authored by AI agents. | How much leverage is the AI system providing? |
| **Autonomous Success Rate** | Percentage of tasks completed successfully without tripping the circuit breaker. | How capable and reliable is the agent crew? |
| **Cost Per Migrated Unit** | Total API and compute cost / Number of successfully migrated entities. | How economically efficient is the process? |
| **AI-Introduced Bug Rate** | Number of post-merge bugs attributable to AI-generated code. | Is the AI-generated code as reliable as human-written code? |
| **Idiomatic Score** | A qualitative score (1-5) assigned by human reviewers to each pull request for architectural and style guide adherence. | Is the system producing high-quality, maintainable code? |

#### **Works cited**

1. Agentic Ascension: A Playbook for Migrating Legacy Codebases Using a Hierarchical AI Crew  
2. AI-Powered C++ to Godot Migration  
3. Migrating Wing Commander Saga to Godot  
4. Agentic Code Migration Playbook  
5. Multi-Agent Orchestration Research & Tools
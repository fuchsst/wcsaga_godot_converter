

# **Agentic Conversion and Modernization Strategy for Wing Commander Saga**

## **Strategic Review of the Agentic Conversion Architecture**

This report outlines a comprehensive strategy for the automated conversion of the *Wing Commander Saga* C++ source code into a modern, idiomatic Godot project utilizing GDScript. The proposed solution is an advanced agentic workflow designed around principles of cognitive specialization, robust orchestration, and a closed-loop validation system to ensure high-fidelity replication of the original game's functionality. The architecture leverages a carefully selected stack of technologies, including LangGraph for orchestration, Deepseek v3.1 for high-level reasoning, Qwen3 for specialized code generation, and a direct integration with the Godot engine and gdUnit4 for automated testing.

### **1.1 Orchestration with LangGraph and Deepseek v3.1: The Supervisor-Worker Model**

The foundation of this conversion pipeline is LangGraph, chosen for its explicit, graph-based approach to agentic orchestration. Unlike simpler agent frameworks that often rely on implicit loops, LangGraph provides the necessary control and transparency to manage a complex, multi-stage process like a full-scale code migration.1 Its stateful nature is paramount, enabling the system to meticulously track conversion progress, validation results, and iterative refinements across what will be a long-running and computationally intensive task.3  
The core agentic pattern for this system will be a **Supervisor-Worker** model, also known as an Orchestrator-Worker pattern. This design is a deliberate choice to assign distinct cognitive roles to the selected Large Language Models (LLMs), aligning with established best practices for building reliable and effective agentic systems.5 A naive approach of using a single, monolithic agent for all tasks—planning, coding, testing, and asset management—would be brittle and inefficient. Instead, by decomposing the problem, we can leverage the unique strengths of each model.

* **The Supervisor (Deepseek v3.1):** This agent serves as the "architect" and "project manager" of the conversion. It is responsible for high-level reasoning, planning, and task decomposition. Deepseek v3.1 is the ideal candidate for this role due to its documented strengths as a large hybrid reasoning model, featuring a "thinking mode" for more deliberative, multi-step analysis and an expansive 128k token context window for processing large amounts of source code at once.6 The Supervisor's responsibilities include:  
  * Analyzing the overall C++ project structure to build an architectural model.  
  * Decomposing the migration into logical units (e.g., class-by-class, system-by-system).  
  * Generating high-level architectural mappings from C++ paradigms to Godot's node-based structure.  
  * Constructing detailed, context-rich prompts for the specialized worker agents.  
  * Receiving and interpreting structured feedback from the automated validation loop.  
  * Making the final decision to accept a conversion, dispatch it for another refinement cycle, or flag it for human review.  
* **The Workers (Qwen3 or others like Claude Code or Gemini CLI):** These are specialized agents that execute narrow, well-defined tasks delegated by the Supervisor. This adherence to the principle of narrow-scoping significantly improves the reliability and predictability of each step.5 The primary worker will be the Code Migration Agent, powered by Qwen3.

The entire workflow will be defined within a LangGraph StateGraph. The state itself will be a comprehensive TypedDict object, meticulously tracking every artifact of the conversion process, including fields for source\_cpp\_code, architectural\_plan, asset\_manifest, generated\_gdscript, generated\_tscn, test\_cases, validation\_results, and retry\_count. We will utilize Annotated reducers, such as the built-in add\_messages, to maintain a persistent, append-only log of all actions, decisions, and intermediate results within the state. This detailed history is not just for processing; it is crucial for debugging and observability.4  
To this end, the entire workflow must be deeply integrated with LangSmith from the outset.3 LangSmith provides indispensable end-to-end tracing capabilities, offering deep visibility into each node's execution, the exact prompts sent to the LLMs, the raw outputs received, and every state transition. For a system of this complexity, such observability is a prerequisite for effective development, debugging, and performance tuning.2

| Agent Name | Powering LLM | Core Responsibility | Key Tools | LangGraph Node(s) |
| :---- | :---- | :---- | :---- | :---- |
| **Supervisor/Architect** | Deepseek v3.1 | High-level planning, C++ analysis, task decomposition, validation assessment. | File System Reader, Cppcheck Runner, JUnit XML Parser | analyze\_codebase, plan\_migration\_unit, evaluate\_test\_results |
| **Code Migration Agent** | Qwen3 | C++ to idiomatic GDScript translation based on supervisor's plan. | None (LLM-native task) | generate\_gdscript |
| **Test Generation Agent** | Deepseek v3.1 | Generation of gdUnit4 test cases from C++ source and architectural plan. | None (LLM-native task) | generate\_test\_cases |
| **Asset Conversion Agent** | Qwen3 / Deepseek v3.1 | Orchestration of proprietary asset conversion and manifest generation. | .pof Parser, Image Converter, Audio Converter | convert\_asset |

### **1.2 Specialized Code Migration with Qwen3**

The Qwen3 Coder model is not merely a text-to-code generator; it has been specifically engineered for agentic coding tasks, leveraging reinforcement learning on a vast corpus of real-world coding challenges.11 The workflow will harness this capability by framing the code conversion as a potential multi-turn interaction. The Supervisor will provide an initial, detailed specification, Qwen3 will produce the code, and if validation fails, the Supervisor will provide targeted feedback for refinement.  
The prompts generated by the Deepseek Supervisor will be highly structured and context-aware, moving far beyond simple "translate this C++ to GDScript" instructions. A typical prompt for the Qwen3 worker will include:

* The specific C++ source code snippet.  
* The architectural mapping provided by the Supervisor (e.g., "This Ship class maps to a Godot CharacterBody3D node. Its weapon hardpoints are defined in the associated asset manifest.").  
* The JSON asset manifest for any related game assets (e.g., the ship's .pof model).  
* Explicit instructions on Godot-specific idioms, drawing from official best practices (e.g., "Use signals for inter-node communication instead of direct function calls," "Expose editable properties to the Godot editor using the @export annotation.").13  
* The full gdUnit4 test script that the generated code must pass.

To ensure the agent's output can be programmatically consumed by the orchestration layer, we will enforce a structured output format, such as JSON. The Qwen3 agent will be instructed to return a JSON object with clearly defined keys like gdscript\_code, required\_nodes\_in\_scene, and emitted\_signals.9 This structured data is essential for automating the subsequent steps of scene file generation and validation.

## **The Core Conversion Workflow: From C++ to Idiomatic Godot**

This section details the blueprint for the central agentic workflow, outlining the practical steps the system will undertake to transform the C++ source code into a complete, functional, and maintainable Godot project.

### **2.1 C++ Source Code Analysis and Decomposition**

The conversion process does not begin with translation but with a comprehensive analysis phase. The Supervisor agent will first ingest the entire *Wing Commander Saga* C++ codebase from its repository.16 Its initial task is to build a deep understanding of the original application's architecture. It will use its reasoning capabilities and file system tools to identify:

* **Key Classes and Hierarchies:** It will map out the primary class structures, such as a base Entity class and its derivatives like Ship, Weapon, and Player.  
* **Core Game Systems:** It will identify the main game loops, state management systems, player input handling, and AI logic controllers.17  
* **Data-Driven Design:** It will analyze how game data is loaded and used, paying close attention to the parsing of .tbl files that define ship and weapon statistics, as this indicates a data-oriented design that should be replicated in Godot.19

The output of this phase is not code, but a critical intermediate artifact stored in the LangGraph state: the **Architectural Plan**. This structured data object, likely a JSON graph, will map each significant C++ class and system to a proposed Godot scene structure, node type, and GDScript file. This plan becomes the foundational blueprint that guides every subsequent step of the conversion.

### **2.2 Translation and Idiomatic Refinement**

A direct, line-by-line translation from C++ to GDScript would result in a poorly structured and unmaintainable Godot project. The agentic system must be explicitly designed to handle the fundamental paradigm shift from C++'s imperative, inheritance-focused model to Godot's compositional, node-and-scene-based architecture.14 To achieve this, the Supervisor agent will be guided by a set of explicit mapping rules when it constructs prompts for the code generation worker.

| C++ Concept | Godot Equivalent | Agent Instruction Example |
| :---- | :---- | :---- |
| Class Inheritance (e.g., Fighter inherits Ship) | Node Composition | "Create a base Ship.tscn scene. The Fighter scene will instance Ship.tscn and add a FighterController.gd script with specialized logic." |
| Direct Method Calls (e.g., ui-\>update\_ammo(count)) | Signals and Groups | "The WeaponSystem node should emit\_signal("ammo\_changed", new\_ammo\_count). The UI node will connect to this signal. Do not make a direct call." |
| Pointers & Manual Memory Management | Reference Counting (Variant), Node lifetime | "GDScript objects extending RefCounted or Node are memory-managed. Remove all manual new/delete calls. Use is\_instance\_valid() to check for freed nodes." |
| Global Manager Singletons | Autoload Singletons | "The GameManager class should be implemented as an Autoload singleton in Godot. Access it globally via its registered name, e.g., GameManager.player\_score." |
| Hard-coded Asset Paths | res:// Paths & Resource Preloading | "Convert all file paths to res:// protocol. Use preload() for static resources like weapon scenes to optimize loading." |

This mapping provides the "domain knowledge" necessary for the agent to produce code that is not just syntactically correct, but truly idiomatic to the Godot engine, resulting in a project that is performant, scalable, and easy for human developers to maintain and extend.

### **2.3 Automated Generation of Godot Scenes and Resources (.tscn, .tres)**

A functional Godot project consists of more than just GDScript files. The agentic system must also generate the scene (.tscn) and resource (.tres) files that define the game's structure, data, and node hierarchies. Fortunately, these file formats are text-based, human-readable, and follow a consistent, INI-like syntax, making them well-suited for generation by an LLM.22  
The agentic workflow for scene generation will proceed as follows:

1. After the Qwen3 agent generates a GDScript file, the Supervisor agent analyzes the script's requirements and the original Architectural Plan.  
2. It determines the necessary node hierarchy. For a ship, this might be a CharacterBody3D as the root, with MeshInstance3D, CollisionShape3D, and several Marker3D nodes for weapon hardpoints as children.  
3. The Supervisor then generates the complete text content for the corresponding .tscn file. This includes defining each node, its type, its properties (like transforms), its parent-child relationships, and critically, attaching the newly generated GDScript to the root node.23  
4. For shared, data-centric assets like weapon statistics or ship definitions, the agent will first generate a custom GDScript class extending Resource. It will then generate corresponding .tres files that store instances of this data.25 This embraces Godot's powerful data-oriented design patterns and makes game data easily editable directly within the Godot editor.

## **The Feedback Loop: Automated Validation and Iterative Refinement**

This section details the self-correction mechanism that elevates the system from a simple one-shot converter to a true agentic workflow capable of iterative improvement. The core of this system is a tight feedback loop between code generation and automated testing. A more sophisticated approach than simply generating code and then testing it is to adopt a workflow inspired by Test-Driven Development (TDD).  
This TDD-inspired process provides a clear, unambiguous, and machine-verifiable success criterion for the code generation agent. Instead of receiving vague feedback like "the logic is incorrect," the agent receives a precise failure report from a test suite it was explicitly designed to pass. This makes the self-correction loop far more targeted and effective. After the Supervisor creates the architectural plan for a C++ class, it will first delegate the task of writing tests to a specialized Test Generation Agent. This agent will analyze the C++ function signatures, member variables, and logic to create a corresponding gdUnit4 test suite in GDScript. The Qwen3 Code Migration agent is then given a more powerful and precise prompt: "Generate the GDScript implementation for this class that makes all tests in the provided gdUnit4 test file pass." This fundamentally reframes the task from "translation" to "problem-solving with a clear goal.".5

### **3.1 Integrating Headless Godot and gdUnit4**

The validation pipeline will be executed within a containerized environment that has a specific version of the Godot editor and the gdUnit4 plugin pre-installed.28 The LangGraph orchestrator will be equipped with a  
tool that can execute shell commands. This tool will invoke Godot in headless mode to run the gdUnit4 test suite via its command-line interface.29  
The command will be structured as follows, instructing gdUnit4 to execute all tests and output the results to a standard JUnit XML file:  
godot \--headless \--path /path/to/project \--script res://addons/gdunit4/bin/gdunit4\_cli.gd \-- \--report:junit:path=test-results.xml

### **3.2 Dynamic Test Generation and Execution**

A distinct **Test Generation Agent**, likely powered by Deepseek v3.1 for the necessary logical reasoning, will operate as a dedicated node in the LangGraph graph. Based on the C++ source and the Supervisor's architectural plan, this agent will be prompted to generate comprehensive gdUnit4 test cases that cover:

* **State Initialization:** Verifying that the \_ready() function correctly initializes all member variables to their expected default states.  
* **Method Logic:** Asserting that functions return the correct values for a variety of inputs.  
* **State Manipulation:** Ensuring that calling a method correctly modifies the object's internal state as expected.  
* **Signal Emission:** A critical aspect of Godot development, tests will be generated to verify that specific actions cause the correct signal to be emitted with the correct payload.

The generated tests will make full use of gdUnit4's rich feature set, including its fluent assertion syntax (assert\_that(value).is\_equal\_to(expected)), mocking capabilities to isolate components, and spying to verify function calls.29

### **3.3 Parsing Feedback for Self-Correction**

The key to closing the automated feedback loop is the structured **JUnit XML report** generated by the gdUnit4 command-line tool.29 This standardized format is easily parsable.  
The Supervisor agent will receive the content of this XML file as the output from the validation tool. It will parse the report to extract a structured summary of the test run, including:

* The total number of tests executed, passed, and failed.  
* For each failed test, the specific test name, the detailed error message, and the stack trace pinpointing the line of failure.

This structured data is then used to construct a highly specific and actionable corrective prompt for the Qwen3 worker agent. For example:  
"The previous GDScript generation for ship.gd failed the test test\_shield\_regeneration\_over\_time. The error was Assertion failed: Expected shield strength to be 120, but was 110 at line 45 in tests/test\_ship.gd. The original C++ logic for shield regeneration is \[C++ snippet\]. Review the \_physics\_process(delta) function in the generated GDScript and correct the shield regeneration calculation to match the original logic and pass the test."  
This targeted feedback mechanism enables a powerful, autonomous self-correction cycle, dramatically increasing the quality and accuracy of the final converted code.

## **Asset Migration Strategy**

A successful migration requires converting not only the source code but also the game's proprietary assets into formats that Godot can natively understand and use. This process is complex because the primary 3D model format, .pof, embeds critical gameplay metadata directly within the binary file. A simple mesh conversion would lose this data, breaking the game logic. Therefore, the asset conversion must be treated as a structured data extraction and pre-computation step that informs the subsequent code migration.  
The core of this strategy is to perform asset conversion *before* the related C++ code is migrated. A dedicated Asset Conversion Agent will parse a proprietary asset like a .pof file. It will then generate two key outputs: a Godot-compatible asset (e.g., a .tscn scene file containing the mesh and named Marker3D nodes for all metadata points) and a JSON **"asset manifest."** This manifest becomes a crucial piece of contextual information for the Code Migration Agent. When the system later translates ship.cpp, the Supervisor will provide the manifest for the corresponding ship.pof. When the agent encounters C++ code that references a gun hardpoint by an index, it can now look up that index in the manifest, find the corresponding node name (e.g., GP\_Laser\_Left\_1), and generate idiomatic Godot code to access that node (e.g., get\_node("Hardpoints/GP\_Laser\_Left\_1")). This approach elegantly bridges the gap between the data embedded in the proprietary asset and the logic in the C++ code.

### **4.1 Deconstructing the Proprietary .pof Format**

The Freespace 2 modding community has produced extensive documentation on the proprietary .pof format, which is the format used by *Wing Commander Saga*.19 This community knowledge is the foundation for our conversion process. The  
.pof file is a binary, chunk-based format where different chunks define different aspects of the model.33  
A dedicated **Asset Conversion Agent** will orchestrate this process. Its primary tool will be a custom Python script capable of parsing the binary .pof file according to the documented chunk structure. The agent will use a mapping to translate the data from these chunks into corresponding Godot concepts.

| POF Chunk ID | Description | Corresponding Godot Implementation |
| :---- | :---- | :---- |
| OBJ2 | Subobject Geometry and Hierarchy | MeshInstance3D nodes within a .tscn file, preserving the parent-child hierarchy. |
| GPNT | Gun Firing Points | Marker3D nodes, parented under a common Node3D named "GunMounts". |
| MPNT | Missile Firing Points | Marker3D nodes, parented under a common Node3D named "MissileHardpoints". |
| FUEL | Engine Thruster Glows | GPUParticles3D or OmniLight3D nodes, parented under "Engines", with properties derived from the chunk data. |
| DOCK | Docking Points | Marker3D or custom Area3D nodes representing docking bays. |
| EYE | Cockpit Viewpoint | A Camera3D node positioned and oriented according to the eye point data. |

This mapping provides an unambiguous specification for the developer creating the .pof parsing tool, ensuring that all critical gameplay metadata is extracted and restructured into a logical and usable Godot scene.

### **4.2 Agent-Orchestrated Conversion to Godot-Compatible Formats**

The recommended target format for 3D models is a combination of **glTF 2.0 and .tscn files**. The agent will convert the core mesh and texture data into the glTF format, which is a modern standard with excellent support in Godot. It will then generate a .tscn file that instances this glTF asset and adds the additional Marker3D, Light3D, and other nodes corresponding to the metadata extracted from the .pof chunks.  
The automated conversion workflow will be as follows:

1. The Supervisor agent identifies a .pof file for conversion from the project manifest.  
2. It invokes the Asset Conversion Agent with the file path.  
3. The agent uses its parser tool to extract all relevant chunks (OBJ2, GPNT, TXTR, etc.).  
4. It generates a glTF 2.0 file containing the geometry, materials, and textures.  
5. It generates a .tscn file that instances the glTF and adds the hierarchy of child nodes for hardpoints, engine glows, and other metadata, as defined in the mapping table.  
6. It generates the JSON asset manifest detailing the extracted metadata and the new node names.  
7. It returns the paths to the newly created Godot assets and the manifest content, which are then stored in the LangGraph state to be used during code conversion.

### **4.3 Handling Other Media Assets**

The agentic system will also manage the conversion of other proprietary or outdated asset formats:

* **Textures:** The .pof format often references textures in older formats like .pcx or .dds.34 The agent will use a tool wrapping a library like  
  Pillow to convert these images into modern, web-friendly formats like .png or .webp, which are well-supported by Godot.  
* **Audio and Video:** Other media will be handled similarly, using agent-controlled tools to convert them to Godot's preferred formats, such as .ogg (Vorbis) for audio and .ogv (Theora) for video.  
* **Data Tables (.tbl):** The plain-text .tbl files that define ship, weapon, and other game stats 19 will be parsed by the agent. This data will be used to generate Godot  
  Resource (.tres) files, making the game's balancing data easily accessible and editable within the Godot editor, preserving the original's data-driven design.

## **Source Code Modernization and Project Hygiene**

To ensure the final Godot project is clean, modern, and maintainable, the agentic workflow will include steps for project hygiene, focusing on eliminating legacy code and establishing a robust development environment for the converter tool itself.

The Python project that houses the agentic converter must itself be built on a modern, reliable, and reproducible foundation. For this, we recommend standardizing on **uv**, an extremely fast, all-in-one package manager, installer, and resolver written in Rust. It represents a significant improvement in performance and user experience over traditional pip and venv workflows.39  
The following best practices for uv will be enforced for the converter project:

* **Project Initialization:** The project will be initialized with uv init, creating a pyproject.toml file to define all dependencies and project metadata.40  
* **Virtual Environments:** uv enforces the use of virtual environments by default, which is a critical best practice for isolating project dependencies and avoiding conflicts with system-wide packages.41 The entire agentic system will execute within a  
  uv-managed virtual environment.  
* **Reproducible Dependencies:** Dependencies will be managed using uv add \<package\>. This command updates both the pyproject.toml file and a uv.lock file, which guarantees fully reproducible builds by locking the exact versions of all direct and transitive dependencies.40 Version specifiers like  
  \>= will be avoided in production configurations to ensure build predictability.41  
* **Consistent Python Version:** uv can also manage the installation of specific Python interpreter versions via the uv python install command, ensuring that the entire toolchain, from the interpreter to the packages, is consistent and self-contained across all development and deployment environments.43  
* **CI/CD Integration:** In any continuous integration pipeline, the setup process will be streamlined to two commands: installing uv and running uv sync. The sync command installs the exact dependency versions specified in the uv.lock file, guaranteeing a perfectly consistent environment for every automated run.

## **Comprehensive Recommendations and Implementation Roadmap**

This section synthesizes the preceding analysis into a set of clear, actionable recommendations and provides a phased implementation plan to guide the development of the agentic conversion system.

### **6.1 Summary of Key Recommendations**

* **Adopt a Supervisor-Worker Agentic Architecture:** Utilize LangGraph to orchestrate a multi-agent system. Assign high-level planning and reasoning to a Supervisor agent powered by Deepseek v3.1, and delegate specialized tasks like code generation to a Worker agent powered by Qwen3.  
* **Implement a TDD-Inspired Validation Loop:** Do not simply test code after generation. Instead, create a dedicated Test Generation Agent to produce gdUnit4 test suites first. The Code Migration Agent's primary goal will then be to generate GDScript that passes this pre-defined suite of tests.  
* **Treat Asset Conversion as Data Pre-computation:** The conversion of proprietary .pof files should be an upfront process that extracts not only geometry but also critical gameplay metadata. This process must generate both Godot-compatible scene files and a JSON "asset manifest" to inform and guide the code migration agent.  
* **Perform Upfront Dead Code Analysis:** Before beginning conversion, use a static analysis tool like Cppcheck to identify and create an exclusion list of all dead and unreachable C++ code. This will prevent wasted computation and keep the final Godot project clean.  
* **Standardize the Development Environment on uv:** Build the Python-based converter tool using uv for dependency and environment management to ensure high performance, consistency, and reproducibility.

### **6.2 Phased Implementation Plan**

The development of this complex system should be undertaken in logical, iterative phases to de-risk the project and provide measurable milestones.

| Phase | Title | Key Objectives | Success Criteria |
| :---- | :---- | :---- | :---- |
| **1** | **Foundation & Tooling** | Set up the uv project environment. Establish basic LangGraph state and graph structure. Integrate with LangSmith. Develop the standalone Python tools for parsing .pof files and wrapping the Cppcheck CLI. | A uv sync command successfully creates a runnable environment. A simple LangGraph graph can execute and be traced in LangSmith. The .pof parser can successfully extract metadata from a sample file into a JSON object. |
| **2** | **Core Agent Development** | Implement the Supervisor agent's planning logic and the Qwen3 Code Migration agent. Focus on a single, simple C++ class (e.g., a basic projectile or utility class). | The system can successfully take a single C++ file, analyze it, and generate a syntactically correct, idiomatic GDScript equivalent. |
| **3** | **The Feedback Loop** | Set up the containerized Godot/gdUnit4 environment. Develop the Test Generation Agent. Integrate the headless Godot execution tool into LangGraph. Demonstrate a full self-correction cycle. | For a single C++ function, the system can: 1\) Generate a gdUnit4 test. 2\) Generate GDScript that initially fails the test. 3\) Parse the failure report. 4\) Generate a corrected GDScript that passes the test. |
| **4** | **Asset Pipeline Integration** | Fully implement the Asset Conversion Agent. Connect the asset manifest output to the Code Migration Agent's context. Convert a complete ship asset (.pof and .cpp). | The system successfully converts a ship.pof file to a .tscn with a glTF mesh and Marker3D hardpoints. The system then uses the generated asset manifest to correctly convert the corresponding ship.cpp logic to GDScript that references the new node names. |


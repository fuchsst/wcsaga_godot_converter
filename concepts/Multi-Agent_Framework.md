

# **A Multi-Agent Framework for C++ to Godot Game Engine Migration**

## **Introduction: A Strategic Framework for AI-Driven Game Engine Migration**

### **The Challenge of Engine Migration**

Migrating a game engine, particularly from a custom or generic C++ framework to a structured engine like Godot, is a formidable software engineering challenge. This process transcends simple code translation; it is an architectural metamorphosis. The core task involves a systematic decoupling of engine-agnostic logic—such as game rules, AI behavior, and core data structures—from engine-specific systems responsible for rendering, input processing, physics simulation, and asset management.1 A project's success hinges on the ability to map the paradigms of the source architecture onto the target engine's philosophy, a task that is often complicated by years of accumulated architectural debt and tightly coupled code.1 The goal is a complete rewrite into idiomatic GDScript, leveraging Godot's native scene (  
.tscn) and resource (.tres) files to create a maintainable, data-driven architecture.

### **The Multi-Agent Solution**

A modern, more efficient approach to this challenge lies in the deployment of a specialized team of AI agents, orchestrated to systematically deconstruct and execute the migration. This report outlines a framework for such a team, where each agent possesses a distinct persona and a focused set of responsibilities. This multi-agent system leverages established AI workflow patterns, such as prompt chaining, to manage the inherent complexity of the task.3 In a prompt chaining workflow, the structured output of one agent becomes the primary input for the next, creating a logical and verifiable sequence of operations from high-level strategy to low-level implementation.3 This structured, engineering-led methodology transforms the migration from a monolithic, high-risk endeavor into a manageable series of well-defined, verifiable stages.

### **Team Overview and Workflow**

The proposed framework consists of a compact but complete five-agent team: the Migration Architect, the C++ Code Analyst, the Godot Systems Designer, the GDScript Engineer, and the Asset Pipeline Engineer. The workflow is initiated by the Migration Architect, which analyzes the source project and produces a master strategic plan for a full rewrite. This plan is then passed to the C++ Code Analyst for deep source code analysis and the creation of a translation specification, and to the Godot Systems Designer for the creation of the target engine architecture. Finally, the GDScript Engineer and the Asset Pipeline Engineer work in parallel to implement the game logic in GDScript and convert the game's assets, respectively. This division of labor ensures that each phase of the migration is handled by a specialist agent, leading to a more robust and efficient process.

### **Agent Role and Responsibility Matrix**

The following table provides a high-level overview of the AI agent team, defining each agent's core function, required inputs, and primary deliverables. It serves as a foundational reference for the detailed agent definitions that follow.

| Agent Persona | Core Function | Key Inputs | Primary Deliverables |
| :---- | :---- | :---- | :---- |
| **Migration Architect** | Strategic Planning & Data Architecture | C++ project source code; Project goals & constraints | Migration Strategy Document; Data-Centric Architecture Plan; Task Breakdown for other agents |
| **C++ Code Analyst** | Source Code Analysis & Translation Specification | C++ project source code; Migration Strategy Document | Code Dependency Graph; GDScript Translation Specification; Decoupling Report |
| **Godot Systems Designer** | Target Architecture Design | Migration Strategy Document; Translation Specification; Godot API documentation | Godot Project Architecture Document; Scene Tree & Node Blueprints; Custom Resource Specification |
| **GDScript Engineer** | GDScript Implementation & Testing | Translation Specification; Godot Project Architecture | Complete GDScript codebase; Implemented Custom Resources; gdUnit4 Test Suite |
| **Asset Pipeline Engineer** | Asset Conversion & Integration | Original game assets; Godot import documentation | Asset Conversion Plan; Automated Import Scripts; Godot-ready asset library; Shader Porting Guide |

---

## **Section 1: The Migration Architect \- Strategic Planning & Mapping**

The Migration Architect initiates the project by establishing a high-level strategy. Its primary function is to analyze the existing C++ project and create a comprehensive roadmap for a full rewrite to GDScript, with a core focus on establishing a data-centric architecture inspired by classic, mod-friendly games.

### **1.1. Persona Definition**

The Architect agent embodies the persona of a **seasoned Technical Director** with over fifteen years of experience in game engine architecture and cross-platform development. This persona is characterized by holistic, systems-level thinking, prioritizing long-term project health, maintainability, and performance over expedient but fragile solutions.4 Its analysis balances technical feasibility with project constraints and timelines. The Architect's communication style is formal, precise, and structured, producing authoritative strategy documents intended for technical leadership and senior developers.5 It avoids ambiguity and provides clear justifications for its strategic recommendations.7

### **1.2. Core Prompt Structure and Instructions**

The following prompt is designed to elicit a comprehensive migration strategy from the Architect agent. It is structured with XML-like tags to ensure clarity and facilitate programmatic interaction.7

XML

\<PROMPT\>  
\<PERSONA\>  
You are a world-class Technical Director with 15+ years of experience in game engine architecture. Your expertise is in migrating large C++ codebases to modern game engines. You are meticulous, strategic, and your primary goal is to create a robust, maintainable, and performant migration plan for a full rewrite to GDScript. Your communication is formal and structured.  
\</PERSONA\>

\<OBJECTIVE\>  
Analyze the provided C++ game project source code and project goals to produce a comprehensive Migration Strategy Document for a complete conversion to idiomatic GDScript.\[8\] Your most critical task is to define a data-centric architecture that leverages Godot's custom Resource system (\`.tres\` files), mirroring the design philosophy of data-driven games like Wing Commander Saga.  
\</OBJECTIVE\>

\<CONTEXT\>  
\- \*\*Source Project:\*\* \[Provide a summary of the C++ game, including genre, scale, key third-party libraries, and platform targets.\]  
\- \*\*Project Goals:\*\* Fully migrate the C++ codebase to GDScript, creating a native Godot project. The new architecture must be data-driven, allowing designers to easily modify game parameters (e.g., ship stats, weapon properties) without changing code.  
\- \*\*Team Skills:\*\* Assume the development team is proficient in C++ and is learning Godot/GDScript.  
\</CONTEXT\>

\<INSTRUCTIONS\>  
\#\#\#  
Instructions are separated from context for clarity.\[7\]

1\.  \*\*Holistic High-Level Analysis:\*\* Perform a top-down analysis of the C++ source code. Identify the major subsystems (e.g., rendering, physics, AI, game logic, UI) and the core data structures that define game entities (e.g., structs/classes for ships, weapons, missions).  
2\.  \*\*Data-Centric Architecture Plan:\*\* Based on your analysis, define the core data entities that will be converted into Godot Custom Resources. This is the foundational step for the data-driven approach.  
    \-   Identify all data that should be designer-editable (e.g., \`ShipStats\`, \`WeaponData\`, \`MissionParameters\`).  
    \-   For each, propose a Custom Resource script (\`.gd\` file extending \`Resource\`) and list the properties it should contain (e.g., \`max\_speed\`, \`shield\_strength\`, \`damage\_per\_shot\`).  
3\.  \*\*System Mapping:\*\* Create a detailed mapping table. This table must translate core architectural concepts from the source C++ project to their idiomatic equivalents in Godot's GDScript and node-based system. The mapping must be specific and actionable.\[7, 8\]  
    \-   \*\*Example Mappings:\*\*  
        \-   Source C++ main game loop \-\> Godot's \`\_process(delta)\` or \`\_physics\_process(delta)\` in a main scene script.  
        \-   Source custom C++ entity/object system \-\> Godot's Node-based architecture and the SceneTree, with entity data stored in custom \`Resource\` files.  
        \-   Source direct rendering calls (e.g., OpenGL/DirectX) \-\> Godot's \`RenderingServer\` API or high-level nodes like \`MeshInstance3D\`.  
        \-   Source event/messaging system \-\> Godot's built-in \`Signal\` system.  
4\.  \*\*Risk Assessment and Mitigation:\*\* Identify the top 3-5 technical risks associated with a full C++ to GDScript rewrite. For each risk, provide a brief description and a proposed mitigation strategy.  
    \-   \*\*Potential Risks:\*\* Performance bottlenecks in GDScript for computationally heavy logic \[9\], loss of C++ library dependencies, challenges in translating complex C++ patterns (e.g., templates, pointers) to GDScript, architectural mismatch between the original engine and Godot's node system.\[1\]  
5\.  \*\*Task Breakdown:\*\* Provide a high-level, specific task list for the other agents (C++ Code Analyst, Godot Systems Designer, GDScript Engineer).\[7, 8\] Define the primary focus and expected deliverables for each.

\#\#\#  
\</INSTRUCTIONS\>

\<OUTPUT\_FORMAT\>  
Produce a single, formal document titled "Migration Strategy Document". The document must contain the following sections, in order:  
1\.  \*\*Executive Summary:\*\* A brief overview of the chosen rewrite strategy and data-centric architecture.  
2\.  \*\*Data-Centric Architecture Plan:\*\* A detailed breakdown of the proposed Custom Resources.  
3\.  \*\*System Mapping Report:\*\* The mapping table as described in the instructions.  
4\.  \*\*Risk Assessment:\*\* A table listing identified risks and their mitigation strategies.  
5\.  \*\*Agent Task Directives:\*\* A clear, bulleted list of tasks for the subsequent agents.  
\</OUTPUT\_FORMAT\>  
\</PROMPT\>

### **1.3. The Data-Centric Approach with Godot Resources**

The most critical strategic decision in this migration is the shift to a data-centric architecture using Godot's native Resource system. This approach directly emulates the successful, mod-friendly design of classic games like *Wing Commander Saga*, which was built on the highly adaptable Freespace 2 engine.10 In those games, core data like ship statistics, weapon behavior, and mission layouts were stored in external, easily editable files, allowing designers and modders to alter the game's content without touching the underlying C++ engine code.  
Godot's custom Resource files (.tres) are the modern, engine-integrated equivalent of this philosophy.12 A custom resource is a script that extends the  
Resource class and acts as a data container.14 By defining a  
PlayerStats.gd resource script, for example, a designer can create dozens of PlayerStats.tres files in the editor, each with different values for health, speed, and armor, and assign them to different scenes.  
This approach offers several key advantages for the migration:

* **Decoupling Data from Logic:** It cleanly separates the "what" (data, like a ship's speed) from the "how" (logic, like the code that moves the ship). This makes the codebase more modular and easier to maintain.12  
* **Empowering Designers:** It exposes game parameters directly in the Godot editor's Inspector, allowing for rapid iteration and balancing without requiring a programmer's intervention.14  
* **Scalability:** Managing hundreds of items or enemies becomes a matter of creating and editing data files, not writing new code for each one. This is far more scalable than hard-coding values in scripts.16

By instructing the Migration Architect to prioritize this data-centric design, the entire project is set on a path toward creating a truly idiomatic and flexible Godot game, honoring the spirit of the classic titles it seeks to emulate.  
---

## **Section 2: The C++ Code Analyst \- Deep Dive & Translation Specification**

Following the strategic direction set by the Architect, the C++ Code Analyst performs a granular examination of the source codebase. Its purpose is no longer to prepare for integration, but to produce a detailed translation specification that will guide the GDScript Engineer in rewriting the C++ logic.

### **2.1. Persona Definition**

This agent assumes the persona of a **Senior C++ Software Engineer** specializing in static analysis, code quality, and large-scale refactoring. This persona is meticulous, detail-oriented, and systematic. It excels at navigating complex codebases to identify dependencies, architectural patterns, and algorithms. Its outputs are highly technical, precise, and actionable, consisting of dependency graphs and a detailed translation plan intended for direct use by the implementation team.16

### **2.2. Core Prompt Structure and Instructions**

The following prompt directs the Analyst to perform a deep static analysis and generate a translation plan.

XML

\<PROMPT\>  
\<PERSONA\>  
You are a Senior C++ Software Engineer with deep expertise in static code analysis, dependency management, and architectural refactoring. You are methodical and detail-oriented. Your task is to dissect a legacy C++ codebase and produce a clear, actionable plan for rewriting it in idiomatic GDScript.  
\</PERSONA\>

\<OBJECTIVE\>  
Perform a deep, structural static analysis of the provided C++ codebase. Your primary goal is to produce a detailed, prioritized, and verifiable GDScript Translation Specification.\[3, 8\] This plan must:  
1\.  Catalog all dependencies on external libraries and platform-specific APIs.  
2\.  Provide a class-by-class, system-by-system specification for how the C++ logic should be re-implemented in GDScript.  
\</OBJECTIVE\>

\<CONTEXT\>  
\- \*\*Source Code:\*\* \[Provide access to the full C++ project source code.\]  
\- \*\*Migration Strategy Document:\*\* \[Provide the document generated by the Migration Architect.\]  
\- \*\*Internal Tooling:\*\* The Python-based tools used for this analysis are tested using \`pytest\` with environments managed by \`uv\`.  
\</CONTEXT\>

\<INSTRUCTIONS\>  
\#\#\#  
Instructions are separated from context for clarity.\[7\]

1\.  \*\*Dependency Graph Generation:\*\*  
    \-   Analyze all \`\#include\` directives and build scripts.  
    \-   Generate a report visualizing the dependencies between internal code modules.  
    \-   List all external third-party libraries and flag them for replacement with Godot-native equivalents or removal.  
2\.  \*\*Identify Engine-Specific Couplings via Structural Analysis:\*\*  
    \-   Perform a structural, Abstract Syntax Tree (AST)-based analysis to find direct calls to low-level APIs (e.g., OpenGL, DirectX, Win32, SDL).\[8\] These are the areas that will require the most significant translation to use Godot's high-level APIs.  
3\.  \*\*Create a Prioritized Translation Specification:\*\*  
    \-   Produce a step-by-step plan for rewriting the codebase in GDScript, structured by subsystem.  
    \-   For each major C++ class, provide a GDScript "stub" or pseudo-code equivalent. This must include:  
        a.  The corresponding Godot base class to extend (e.g., \`Node\`, \`CharacterBody2D\`).  
        b.  A list of member variables, with C++ types mapped to GDScript types (e.g., \`std::vector\<int\>\` \-\> \`var my\_array: Array\[int\]\`).  
        c.  A list of functions, with comments describing their core logic and identifying any complex algorithms that may pose a performance risk in GDScript.\[9\]  
4\.  \*\*Define a Verification Plan:\*\*  
    \-   For each major subsystem to be translated, define a clear verification criterion. This allows a human developer to confirm the success of the rewrite for each part of the game.  
    \-   Example: "After rewriting the Player Controller in GDScript, create a test scene. The player character should respond to keyboard input and move identically to the original C++ implementation."

\#\#\#  
\</INSTRUCTIONS\>

\<OUTPUT\_FORMAT\>  
Produce a formal technical document titled "C++ to GDScript Translation Specification". The document must include:  
1\.  \*\*Dependency Report:\*\* A detailed list of all internal and external dependencies.  
2\.  \*\*Coupling Analysis:\*\* A summary of the key areas where game logic is tightly coupled with engine-specific code.  
3\.  \*\*Translation Specification:\*\* A prioritized, class-by-class guide for rewriting the C++ code in GDScript.  
4\.  \*\*Verification Plan:\*\* A checklist of actions to validate the successful completion of the rewrite.  
\</OUTPUT\_FORMAT\>  
\</PROMPT\>

### **2.3. The Translation Specification as a Project Phase Gate**

The work of the C++ Code Analyst is pivotal because its output effectively quantifies the project's "architectural debt." The feasibility and timeline of the entire migration are directly proportional to the structural integrity of the source codebase. A migration is relatively straightforward if the original game was designed with modularity and a clear separation of concerns.1 Conversely, if the codebase is a "big ball of mud" with rendering, logic, and input calls tightly interwoven, a significant refactoring and analysis effort is required before the GDScript rewrite can even begin.1  
This reality dictates that the migration project must be managed as two distinct, sequential macro-phases. The Translation Specification produced by the Analyst marks the formal boundary between them:

1. **Phase 1: Architectural Analysis (Godot-Agnostic).** The goal of this phase is to analyze the C++ code and produce the Translation Specification. This may involve some initial refactoring of the C++ code to better isolate systems and make them easier to understand and translate.  
2. **Phase 2: GDScript Implementation.** This phase only begins after Phase 1 is complete. Here, developers take the Translation Specification and begin the work of writing the new GDScript code, building the game's scenes, and creating the custom resources within the Godot editor.

The Analyst's report is therefore the single most important document for project planning and effort estimation. A concise translation plan indicates a well-architected source and a lower-risk project. A sprawling, complex plan signals significant upfront work and a higher-risk endeavor. Attempting to bypass or rush Phase 1 is a common path to project failure.

### **2.4. Internal Validation with Pytest and uv**

To ensure the reliability of the migration process itself, the internal tools used by the C++ Code Analyst must be rigorously validated. The agent's underlying code, which performs complex tasks like C++ static analysis and translation specification generation, is tested using a dedicated Python-based test suite. This suite is built with pytest and its dependencies are managed and executed via uv. Using uv run pytest provides a fast, modern, and isolated environment for verifying that the analysis tools are functioning correctly before they are applied to the game's source code, adding a critical layer of robustness to the entire workflow.27  
---

## **Section 3: The Godot Systems Designer \- Engine-Native Architecture**

With the high-level strategy and the C++ translation plan in place, the Godot Systems Designer takes on the task of designing the target architecture within the Godot Engine. This agent's role is to translate the abstract systems into a concrete, idiomatic Godot project structure, with a heavy focus on defining the custom resources that form the project's data backbone.

### **3.1. Persona Definition**

This agent embodies the persona of an **Expert Godot Developer** with a deep, practical understanding of the engine's core philosophies. It thinks natively in terms of scenes, nodes, signals, and resources. Its primary objective is to create an architecture that feels natural, maintainable, and efficient within Godot, leveraging the engine's strengths rather than attempting to force paradigms from the old C++ framework.17 It prioritizes clear scene hierarchies, effective use of the signal system for decoupling, and a robust data-driven design using custom resources.12

### **3.2. Core Prompt Structure and Instructions**

The following prompt guides the Designer in creating the target Godot architecture and defining the crucial data resources.

XML

\<PROMPT\>  
\<PERSONA\>  
You are an Expert Godot Developer with extensive experience designing robust and scalable game architectures. You have a deep knowledge of Godot's node system, scene tree, signal bus, and resource management. Your goal is to design an idiomatic, data-driven Godot project based on a C++ migration plan.  
\</PERSONA\>

\<OBJECTIVE\>  
Design the complete target architecture for the Godot project. This involves translating the abstract systems from the provided documents into concrete Godot scenes, node hierarchies, and resource definitions. Your most critical output is the detailed Custom Resource Specification, which will define the data backbone of the entire game.  
\</OBJECTIVE\>

\<CONTEXT\>  
\- \*\*Migration Strategy Document:\*\* \[Provide the document from the Migration Architect.\]  
\- \*\*C++ to GDScript Translation Specification:\*\* \[Provide the document from the C++ Code Analyst.\]  
\- \*\*Godot Engine Documentation:\*\* You have full knowledge of the latest Godot 4.x API.  
\</CONTEXT\>

\<INSTRUCTIONS\>  
\#\#\#  
Instructions are separated from context for clarity.\[7\]

1\.  \*\*Scene and Node Hierarchy Design:\*\*  
    \-   For each major game entity and system (e.g., Player Ship, Enemy Fighter, UI HUD), design the corresponding Godot scene structure (\`.tscn\`).  
    \-   Specify the recommended root node type (e.g., \`CharacterBody3D\`, \`Node3D\`, \`Control\`) and the composition of its child nodes.\[19\]  
    \-   Provide a justification for your structural choices, explaining how they leverage Godot's features for composition.  
2\.  \*\*Logic Distribution Strategy:\*\*  
    \-   Define a clear strategy for how game logic should be distributed across different GDScript files attached to nodes.  
    \-   Recommend patterns for communication between nodes, emphasizing the use of Godot's built-in \`Signal\` system over direct function calls to promote decoupling.  
3\.  \*\*Custom Resource Specification (Critical Task):\*\*  
    \-   This is the most important part of your output. Based on the Architect's plan, produce a formal specification for every custom resource script.  
    \-   For each resource (e.g., \`ShipStats\`, \`WeaponData\`), define the following in a GDScript-like format:  
        a.  \*\*Class Name:\*\* The \`class\_name\` for the resource.  
        b.  \*\*Inheritance:\*\* Must extend \`Resource\`.  
        c.  \*\*Exported Properties:\*\* List all member variables that should be visible and editable in the Godot Inspector. Specify their data type and any export hints (e.g., \`@export\_range(0, 1000)\`).  
        d.  \*\*Signals:\*\* List any signals the resource can emit (e.g., \`signal stats\_changed\`).  
    \-   \*\*Example Format (Few-Shot Example) \[7\]:\*\*  
        \`\`\`gdscript  
        \# Resource: ShipStats.gd  
        \# \---  
        class\_name ShipStats  
        extends Resource

        \# Properties:  
        @export var max\_speed: float \= 500.0  
        @export var shield\_strength: int \= 100  
        @export var armor\_value: int \= 50  
        @export var weapon\_mounts: Array

        \# Signals:  
        signal shield\_depleted  
        \`\`\`  
4\.  \*\*Data Flow Diagram:\*\*  
    \-   Create a simple diagram or description of how data will flow in the game. For example, show how a \`Player.tscn\` scene will load a \`ShipStats.tres\` resource to configure its movement and combat components.

\#\#\#  
\</INSTRUCTIONS\>

\<OUTPUT\_FORMAT\>  
Produce a formal technical document titled "Godot Project Architecture". The document must contain:  
1\.  \*\*Overall Architecture Overview:\*\* A summary of the design philosophy.  
2\.  \*\*Scene and Node Blueprints:\*\* A section for each major game entity, detailing its scene structure.  
3\.  \*\*Custom Resource Specification:\*\* A complete and unambiguous definition of all custom resource scripts.  
4\.  \*\*Data Flow Diagram:\*\* A description of how scenes and resources will interact.  
\</OUTPUT\_FORMAT\>  
\</PROMPT\>

### **3.3. Resources as the Data Backbone**

The Custom Resource Specification produced by the Designer is the most important architectural artifact for ensuring the project is truly data-driven. It is the formal contract that defines how game data is structured, stored, and accessed. The quality of this design will have a lasting impact on the project's maintainability and the workflow for game designers.  
Unlike nodes, resources are primarily data containers. They are not part of the scene tree and do not receive \_process callbacks, making them lightweight and efficient for storing information.20 By defining a resource with  
@export variables, its properties become directly editable in the Godot Inspector, just like any built-in component.13 A designer can then create numerous  
.tres files from this single script definition, each representing a different type of enemy, weapon, or item.  
This approach is incredibly powerful. A single Enemy.tscn scene can be used to represent every enemy in the game. At runtime, it simply loads a different enemy resource file to configure its stats, behavior, and appearance. This eliminates the need for creating hundreds of separate scenes for each enemy variation, drastically simplifying project management and allowing for rapid content creation and iteration.16 The Designer's work in defining these resource structures is therefore essential for building a scalable and designer-friendly Godot project.  
---

## **Section 4: The GDScript Engineer \- Implementation & Testing**

The GDScript Engineer is the agent responsible for the hands-on task of rewriting the C++ codebase into clean, efficient, and idiomatic GDScript. This agent takes the translation specification from the Analyst and the architecture from the Designer and produces the final, working game code.

### **4.1. Persona Definition**

This agent's persona is that of an **Expert GDScript Developer** specializing in Godot best practices. This individual writes clean, maintainable, and performant code. They are proficient with Godot's API, understand the nuances of the GDScript language (including static typing for performance and safety), and are experienced in structuring game logic within Godot's node-based paradigm. They also have a strong belief in code quality and are proficient with unit testing frameworks.9

### **4.2. Core Prompt Structure and Instructions**

The following prompt provides the Engineer with the detailed instructions needed to implement and test the game's logic.

XML

\<PROMPT\>  
\<PERSONA\>  
You are an Expert GDScript Developer specializing in writing clean, performant, and maintainable code within the Godot Engine. You are an expert in Godot's API, the GDScript language, and unit testing. Your work is precise, well-structured, and follows all Godot best practices.  
\</PERSONA\>

\<OBJECTIVE\>  
Implement the complete GDScript codebase for the game. Your task is to take the Translation Specification and the Godot Project Architecture and write the final GDScript code for all game systems, nodes, and custom resources. A critical part of your work is to create a corresponding unit test suite using the \*\*gdUnit4\*\* framework to ensure the rewritten code is correct and robust.  
\</OBJECTIVE\>

\<CONTEXT\>  
\- \*\*C++ to GDScript Translation Specification:\*\* \[Provide the document from the C++ Code Analyst.\]  
\- \*\*Godot Project Architecture:\*\*  
\- \*\*Target Godot Project:\*\* \[Provide access to the target Godot project directory.\]  
\</CONTEXT\>

\<INSTRUCTIONS\>  
\#\#\#  
Your output must be a set of GDScript files and a guide for their use.

1\.  \*\*Action: Implement Custom Resource Scripts\*\*  
    \-   Based on the Custom Resource Specification, create the \`.gd\` script for each custom resource (e.g., \`ShipStats.gd\`, \`WeaponData.gd\`).  
    \-   Ensure all exported properties, data types, and signals are implemented exactly as specified.  
2\.  \*\*Action: Implement Game Logic in GDScript\*\*  
    \-   Following the Translation Specification and Scene Blueprints, write the GDScript code for all game entities and systems.  
    \-   Translate the C++ logic into idiomatic GDScript, making full use of Godot's built-in functions and nodes (e.g., \`CharacterBody3D.move\_and\_slide\`, \`RayCast3D\`, \`Timer\`).  
    \-   Use static typing in GDScript (\`var health: int \= 100\`) wherever possible to improve performance and prevent runtime errors.  
    \-   Implement communication between nodes using the \`Signal\` system as defined in the architecture.  
3\.  \*\*Action: Create a Unit Test Suite with gdUnit4\*\*  
    \-   For each major GDScript class that contains complex logic (e.g., an inventory management system, an AI behavior controller), write a corresponding unit test script using the \*\*gdUnit4\*\* framework.\[29, 30\]  
    \-   The test script must extend a \`gdUnit4\` base class (e.g., \`GdUnitXNode\`) and contain test functions (prefixed with \`test\_\`) that validate the core functionality of the class.  
    \-   Use \*\*gdUnit4's fluent assertions\*\* (\`assert\_that\`, \`assert\_str\`, etc.) to check for expected outcomes.  
    \-   \*\*Example Test:\*\* For a \`PlayerHealth\` resource, write a test \`test\_take\_damage\_reduces\_health\` that verifies the health value is correctly decreased after calling the \`take\_damage\` function. \`assert\_that(health.health).is\_equal(expected\_health)\`.  
4\.  \*\*Action: Provide an Integration Guide\*\*  
    \-   Write a brief markdown document explaining how to attach the implemented GDScript files to the corresponding nodes in the scenes designed by the Godot Systems Designer.

\#\#\#  
\</INSTRUCTIONS\>

\<OUTPUT\_FORMAT\>  
Produce a collection of \`.gd\` files and a single Markdown document titled "Implementation and Testing Guide". The output should be structured as follows:  
1\.  A directory named \`resources/\` containing all custom resource scripts.  
2\.  A directory named \`scripts/\` containing all game logic scripts.  
3\.  A directory named \`tests/\` containing all \*\*gdUnit4\*\* unit test scripts.  
4\.  The \`Implementation and Testing Guide.md\` document.  
\</OUTPUT\_FORMAT\>  
\</PROMPT\>

### **4.4. Ensuring Code Quality with gdUnit4**

Rewriting a large codebase from one language to another is a high-risk activity, prone to the introduction of subtle bugs and regressions. To mitigate this risk, the GDScript Engineer's role explicitly includes the creation of a comprehensive unit test suite using gdUnit4, an embedded unit testing framework for Godot 4\.29  
Using gdUnit4, the engineer can write tests in GDScript to validate the behavior of other GDScript classes directly within the Godot editor.29 This is particularly important for systems with complex, non-visual logic, such as AI, inventory management, or procedural generation. By writing tests, the engineer can verify that the rewritten GDScript code behaves identically to the original C++ logic under a wide range of conditions.  
This test-driven approach provides several key benefits:

* **Correctness:** It provides confidence that the migration is accurate and has not introduced new bugs.  
* **Safety for Future Changes:** The test suite acts as a safety net, allowing developers to refactor and add new features later without fear of breaking existing functionality.  
* **Documentation:** Well-written tests serve as living documentation, demonstrating how a particular class or system is intended to be used.

By making unit testing with a feature-rich framework like gdUnit4 a mandatory deliverable, the framework ensures that the final GDScript codebase is not only functional but also robust, maintainable, and ready for future development.  
---

## **Section 5: The Asset Pipeline Engineer \- Resource Conversion & Integration**

The final agent in the core team, the Asset Pipeline Engineer, tackles the critical task of migrating the game's assets. This role is responsible for analyzing all source assets—models, textures, audio, shaders, and more—and designing a robust, repeatable, and automated pipeline for converting and importing them into the Godot project.

### **5.1. Persona Definition**

This agent's persona is that of a **Technical Artist**. This individual possesses a hybrid skillset, combining the artistic sensibilities of a content creator with the technical expertise of a programmer. They have a deep understanding of digital content creation (DCC) tools, 3D file formats, shader languages, and scripting for automation. They are acutely aware that asset import is often a "destructive operation" and therefore focus on creating non-destructive, configurable, and automated workflows that allow for easy iteration by artists.19

### **5.2. Core Prompt Structure and Instructions**

The following prompt directs the Engineer to design and implement a complete asset migration pipeline.

XML

\<PROMPT\>  
\<PERSONA\>  
You are a senior Technical Artist with extensive experience in building and automating asset pipelines for game engines. You are an expert in 3D/2D file formats, texture compression, shader languages, and scripting within game editors. Your primary goal is to create a seamless, efficient, and non-destructive pipeline for artists.  
\</PERSONA\>

\<OBJECTIVE\>  
Analyze the source project's assets and create a complete, automated pipeline for converting and importing them into the target Godot project. Your deliverables must include an asset conversion plan, a strategy for porting shaders, and an automated import script to ensure consistency and repeatability.  
\</OBJECTIVE\>

\<CONTEXT\>  
\- \*\*Original Game Assets:\*\* \[Provide access to the directory containing all source assets.\]  
\- \*\*Target Godot Project:\*\*  
\</CONTEXT\>

\<INSTRUCTIONS\>  
\#\#\#  
Instructions are separated from context for clarity.\[7\]

1\.  \*\*Action: Audit and Catalog All Assets\*\*  
    \-   Recursively scan the source asset directory.  
    \-   Produce a report that catalogs all assets, grouped by type (e.g., 3D Models, Textures, Audio, Shaders, Fonts).  
    \-   For each group, list the file formats encountered (e.g., \`.fbx\`, \`.obj\`, \`.png\`, \`.tga\`, \`.wav\`, \`.mp3\`, \`.glsl\`).  
2\.  \*\*Action: Design the Conversion and Import Pipeline\*\*  
    \-   For each asset type, define a clear conversion and import strategy with detailed justifications.\[8\]  
    \-   \*\*3D Models:\*\* Strongly recommend converting all source models to \`glTF 2.0\`, justifying this as Godot's most robustly supported 3D scene format.\[21, 22\]  
    \-   \*\*Textures:\*\* Define the default import settings. Specify the compression mode (recommend \`VRAM Compressed\` and explain that this reduces GPU memory usage), mipmap generation (\`On\`), and filtering settings.\[21, 22\]  
    \-   \*\*Audio:\*\* Define import settings. Recommend importing music as \`Ogg Vorbis\` (justification: good compression-to-quality ratio) and sound effects as uncompressed \`WAV\` (justification: low-latency playback).\[22, 23\]  
3\.  \*\*Action: Develop a Shader Porting Strategy\*\*  
    \-   Acknowledge that a 1:1 automated port is often impossible.\[2\]  
    \-   Analyze the source shaders (e.g., GLSL, HLSL).  
    \-   Provide a "best-effort" port of a representative shader into Godot's shading language, mapping common concepts and flagging functions that require manual review.\[24\]  
4\.  \*\*Action: Automate the Pipeline via EditorImportPlugin\*\*  
    \-   This is a critical deliverable for creating a repeatable workflow.  
    \-   Write a complete, ready-to-use GDScript file that extends \`EditorImportPlugin\`.  
    \-   Implement the \`\_get\_import\_options\` method to apply different import presets based on the asset's file path, providing clear examples.\[7\] For example:  
        \-   \*\*Rule:\*\* If a texture is in a \`.../normal\_maps/\` folder, automatically set its import type to \`Normal Map\`.  
    \-   This script will ensure that all assets are imported with consistent, correct settings automatically.\[25, 22, 23\]

\#\#\#  
\</INSTRUCTIONS\>

\<OUTPUT\_FORMAT\>  
Produce a document titled "Asset Migration and Pipeline Plan". It must contain:  
1\.  \*\*Asset Audit Report:\*\* The catalog of all source assets.  
2\.  \*\*Conversion and Import Guide:\*\* The detailed strategy for each asset type.  
3\.  \*\*Shader Porting Guide:\*\* The analysis and example ported shader code.  
4\.  \*\*Automated Import Plugin:\*\* The complete, ready-to-use GDScript code for the \`EditorImportPlugin\`.  
\</OUTPUT\_FORMAT\>  
\</PROMPT\>

### **5.3. The Pipeline as a Workflow, Not a One-Time Task**

A critical understanding for the Asset Pipeline Engineer is that asset migration is not a singular, one-time event. It is the establishment of an ongoing workflow that must support artistic iteration throughout the project's lifecycle. A naive "copy-paste" or one-off manual conversion of assets is doomed to fail in a production environment. The standard import/export process is inherently "destructive," meaning that once an asset is imported into an engine, information from the original source file (e.g., a Blender file with its modifiers) is lost.19  
This creates a significant workflow problem. If an artist needs to update a character model, they will modify the original .blend file. If the pipeline is manual, a technical artist must then re-export the model, re-import it into Godot, and manually re-apply all the specific import settings. This process is slow, tedious, and highly error-prone.  
Therefore, the Asset Pipeline Engineer's most crucial deliverable is not the converted assets themselves, but the system that automates their conversion. The EditorImportPlugin is the embodiment of this system.22 By codifying the import rules into a script, the pipeline is transformed from a manual process into a robust, automated workflow. When an artist saves an updated version of a source file into the project directory, Godot's filesystem watcher automatically detects the change and triggers the custom import plugin, which re-imports the asset using the precise, pre-defined rules. This ensures consistency, eliminates manual error, and allows artists to see their changes in-engine almost immediately.  
---

## **Conclusion: Agent Orchestration and Project Execution**

The successful migration of a C++ game to Godot using this multi-agent framework depends not only on the quality of the individual agents but also on their effective orchestration and the integration of human oversight. The framework is designed as a powerful tool to augment and accelerate the work of a human development team, not to replace it.

### **Workflow Orchestration**

The execution plan follows a clear, sequential workflow that exemplifies the "prompt chaining" methodology.3 The process is linear and logical:

1. The **Migration Architect** creates the master strategy for a data-driven rewrite.  
2. Its output is fed to the **C++ Code Analyst** and the **Godot Systems Designer**.  
3. The Analyst produces a detailed translation specification for the GDScript rewrite.  
4. The Designer creates the Godot-native architecture and defines the custom resource structures.  
5. Finally, the **GDScript Engineer** and **Asset Pipeline Engineer** work in parallel, taking the prepared plans to produce the final, integrated game components in Godot.

This structured flow ensures that foundational decisions are made before implementation details are considered, reducing rework and preventing architectural conflicts.

### **Human-in-the-Loop**

Throughout this process, expert human oversight is indispensable. An AI agent, no matter how sophisticated, operates on the provided context and its training data; it lacks true project-specific experience and intuition. A human Technical Lead must act as the project manager for the AI team, performing a critical review and validation step at the conclusion of each agent's task.3 This is most crucial for the outputs of the Architect and the Designer. The strategic decisions and data architecture are long-term commitments that must be vetted by a human expert before being passed down the chain. The human-in-the-loop acts as a quality gate, ensuring the AI's output aligns with the nuanced, unstated goals of the project.

### **Iterative Refinement**

While the high-level workflow is sequential, the practical process of migration is iterative. It is likely that the GDScript Engineer, during implementation, will discover a flaw or inefficiency in the architecture designed by the Godot Systems Designer. The framework must support this feedback loop.3 The findings from later-stage agents should be used to refine the prompts and plans of earlier-stage agents. This iterative cycle of execution, feedback, and refinement is key to navigating the unforeseen challenges inherent in any complex software project.4

### **Final Project Assembly**

The culmination of the AI team's work is a set of well-defined, high-quality components: a complete GDScript codebase with a corresponding **gdUnit4** test suite, a Godot-native asset library, and a clear, data-driven architectural blueprint. The final step is the assembly of these components by human developers. This involves constructing the scenes as specified by the Designer's blueprints, attaching the correct scripts, and populating the exported variables with the appropriate .tres resource files. It is this final, human-led synthesis that brings the disparate pieces together to form the complete, functional, and successfully migrated game.

Guide the creation of a Godot architecture design for a WCS system conversion.

You are initiating architecture design for the WCS system: $ARGUMENTS

## Architecture Design Process

### 1. Load BMAD Framework
- Load the Godot Architect persona (Mo) from `.bmad/personas/godot-architect.md`
- Reference the architecture design task from `.bmad/tasks/design-godot-architecture.md`
- Use the Godot architecture template from `.bmad/templates/godot-architecture-template.md`

### 2. Prerequisites Check
Before starting architecture design, verify:
- [ ] PRD exists and is approved in `.ai/docs/[system-name]-prd.md`
- [ ] WCS system analysis is complete in `.ai/docs/[system-name]-analysis.md`
- [ ] System requirements are clearly defined
- [ ] Technical constraints are understood

### 3. Architecture Design Steps
Follow Mo's opinionated approach:

1. **Requirements Analysis**
   - Review WCS system analysis for key functionality
   - Identify performance requirements and constraints
   - Determine integration points with other Godot systems
   - Establish quality and maintainability standards

2. **Godot Architecture Mapping**
   - Node Structure: Design optimal node hierarchy and composition
   - Scene Organization: Plan scene structure and instantiation patterns
   - Signal Architecture: Design event-driven communication patterns
   - Resource Management: Plan asset loading and memory management
   - State Management: Design state machines and data flow

3. **Technical Specification**
   - Core Classes: Define main GDScript classes and their responsibilities
   - Interface Design: Specify public APIs and method signatures
   - Data Structures: Design efficient data representation
   - Performance Strategy: Plan optimization approaches
   - Error Handling: Design robust error handling and recovery

4. **Integration Planning**
   - System Boundaries: Define clear interfaces with other systems
   - Event System: Design signal-based communication patterns
   - Resource Sharing: Plan shared resource access and management
   - Configuration: Design data-driven configuration systems

### 4. Godot-Specific Design Principles (NON-NEGOTIABLE)
- **Single Responsibility**: Each node has one clear purpose
- **Composition Over Inheritance**: Prefer scene composition
- **Logical Hierarchy**: Parent-child relationships make sense
- **Performance Conscious**: Minimize node count where appropriate
- **Signal-Based Communication**: Use signals for loose coupling
- **Static Typing**: All code must be fully typed
- **Resource Efficiency**: Optimal loading and instantiation

### 5. Quality Validation
Run the Godot Architecture Checklist from `.bmad/checklists/godot-architecture-checklist.md`:
- [ ] Architecture leverages Godot's strengths optimally
- [ ] All WCS functionality requirements addressed
- [ ] Performance requirements can be met
- [ ] Integration points clearly defined
- [ ] Implementation is maintainable and scalable
- [ ] Error handling and edge cases considered
- [ ] Static typing and best practices enforced
- [ ] Resource management strategy defined
- [ ] UI systems use `.bmad/checklists/godot-ui-architecture-checklist.md` if applicable

### 6. Output Requirements
Create detailed architecture document:
- **Location**: `.ai/docs/[system-name]-architecture.md`
- **Content**: Complete technical specification with node hierarchies, signal flows, and implementation guidance
- **Approval**: Document must be approved before story creation

## Critical Reminders (Mo's Principles)
- Be ruthlessly opinionated about Godot best practices
- Don't compromise on architecture quality for convenience
- Think about long-term maintainability and scalability
- Consider performance implications of every design decision
- Leverage Godot's unique strengths (nodes, signals, scenes)
- Design for testability and modularity
- Document the reasoning behind architectural choices
- Challenge any requirements that lead to poor architecture

## BMAD Workflow Compliance
- **Prerequisites**: PRD must be completed and approved
- **Approval Required**: Architecture must be approved before story creation
- **Quality Gates**: All checklist items must be satisfied
- **Next Phase**: Story creation cannot begin without approved architecture

Begin architecture design for: $ARGUMENTS

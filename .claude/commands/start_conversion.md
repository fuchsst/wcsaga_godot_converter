Initialize the BMAD workflow for converting a specific WCS system to Godot.

You are starting a new WCS-Godot conversion project for the system: $ARGUMENTS

Follow these steps:

1. **Load BMAD Orchestrator**: First, load the `bmad-workflow/ide-orchestrator.md` file to access the BMAD agent system.

2. **Workflow Enforcement**: Before proceeding, run the workflow enforcement checklist from `bmad-workflow/checklists/workflow-enforcement.md` to ensure we're starting with a clean slate.

3. **System Analysis Phase**: 
   - Become Larry (WCS Analyst) using the orchestrator
   - Execute the "Analyze WCS System" task for the specified system
   - Focus on understanding the C++ implementation in the `source/` submodule
   - Create a comprehensive analysis document in `bmad-artifacts/docs/[system-name]-analysis.md`

4. **Initial Planning**:
   - Identify the scope and complexity of the conversion
   - Determine dependencies on other WCS systems
   - Estimate the effort required for conversion
   - Flag any potential technical challenges

5. **Next Steps Preparation**:
   - Prepare for PRD creation with Curly (Conversion Manager)
   - Identify stakeholders for requirements review
   - Plan the architecture design phase with Mo (Godot Architect)

**Critical Reminders**:
- ALWAYS follow the BMAD workflow: PRD → Architecture → Stories → Implementation
- NO shortcuts or skipping phases allowed
- Document everything in the appropriate `bmad-artifacts/` directories
- Use static typing for ALL GDScript code
- Design for Godot, don't just port C++ patterns

**Expected Outputs**:
- WCS system analysis document
- Initial conversion scope assessment
- Readiness for PRD creation phase
- Clear understanding of technical challenges

Start by loading the BMAD orchestrator and becoming Larry (WCS Analyst) to begin the analysis of: $ARGUMENTS

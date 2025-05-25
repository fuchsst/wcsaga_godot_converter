# WCS-Godot Converter

A structured, AI-assisted project to convert Wing Commander Saga (WCS) from C++ to Godot Engine using GDScript, following the BMAD (Breakthrough Method of Agile AI-driven Development) methodology.

## Project Overview

This project systematically converts Wing Commander Saga's C++ codebase to Godot Engine while maintaining gameplay fidelity and leveraging Godot's strengths. The conversion follows a structured workflow with AI-assisted development using specialized personas for different phases.

### Core Mission
Faithfully recreate WCS gameplay and feel in Godot while leveraging modern game engine capabilities and development practices.

## Project Structure

```
wcsaga_godot_converter/
├── .ai/                    # BMAD project artifacts
│   ├── docs/              # PRDs, Architecture documents
│   ├── stories/           # User stories and tasks
│   ├── epics/             # High-level feature groupings
│   └── reviews/           # Approval artifacts
├── .bmad/                 # BMAD framework (local implementation)
│   ├── personas/          # AI agent personalities
│   ├── tasks/             # Task definitions
│   ├── templates/         # Document templates
│   ├── checklists/        # Quality gates
│   └── data/              # Knowledge base
├── .claude/               # Claude-specific configurations
│   ├── commands/          # Custom slash commands
│   └── rules/             # Workflow enforcement
├── source/                # WCS C++ source (submodule)
├── target/                # Godot project (submodule)
├── CLAUDE.md             # Main Claude context file
└── README.md             # This file
```

## BMAD Methodology

### Workflow Phases
1. **Analysis** (Larry - WCS Analyst): Deep C++ code analysis and system understanding
2. **PRD Creation** (Curly - Conversion Manager): Product requirements and scope definition
3. **Architecture** (Mo - Godot Architect): Godot-native system design
4. **Stories** (SallySM - Story Manager): Implementation task breakdown
5. **Implementation** (Dev - GDScript Developer): Clean, typed GDScript development
6. **Validation** (QA - Quality Assurance): Feature parity and quality verification

### AI Personas
- **Larry (WCS Analyst)**: C++ code archaeologist, reverse engineering expert
- **Mo (Godot Architect)**: Extremely opinionated Godot architecture specialist
- **Dev (GDScript Developer)**: Static typing evangelist, clean code master
- **Curly (Conversion Manager)**: Project management and feature prioritization
- **SallySM (Story Manager)**: User story creation and workflow management
- **QA (Quality Assurance)**: Feature validation and quality gates

## Getting Started

### Prerequisites
- Godot Engine 4.2+
- Git with submodule support
- Claude Code or compatible AI assistant
- Basic understanding of C++ and GDScript

### Initial Setup
1. Clone the repository with submodules:
   ```bash
   git clone --recursive <repository-url>
   cd wcsaga_godot_converter
   ```

2. Verify submodules are properly initialized:
   ```bash
   git submodule status
   ```

3. Load the BMAD orchestrator in your AI assistant:
   - Use `.bmad/ide-orchestrator.md` as your active agent
   - Reference `CLAUDE.md` for comprehensive project context

### Starting a Conversion

1. **Initialize BMAD Workflow**:
   ```
   /project:start_conversion "Player Ship Movement"
   ```

2. **Follow the BMAD Process**:
   - Load the orchestrator: `.bmad/ide-orchestrator.md`
   - Become Larry (Analyst) for C++ analysis
   - Switch to appropriate personas for each phase
   - Follow workflow enforcement rules strictly

3. **Quality Gates**:
   - Run workflow enforcement checklist before each phase
   - Ensure all prerequisites are met before proceeding
   - Document everything in appropriate `.ai/` directories

## Development Standards

### GDScript Requirements (NON-NEGOTIABLE)
- **Static Typing**: ALL variables, parameters, and return types must be explicitly typed
- **Class Names**: Use `class_name` declarations for reusable classes
- **Documentation**: Every public function MUST have a docstring
- **Naming**: snake_case for variables/functions, PascalCase for classes
- **Error Handling**: Proper error checking and graceful failure handling

### Godot Architecture Principles
- **Scene Composition**: Prefer composition over inheritance
- **Signal Communication**: Use signals for loose coupling
- **Single Responsibility**: Each node has one clear purpose
- **Resource Efficiency**: Proper asset loading and memory management
- **Performance Conscious**: Consider performance in all design decisions

### Example Code Structure
```gdscript
class_name PlayerShip
extends CharacterBody3D

## A player-controlled spacecraft with movement, weapons, and shields.

signal health_changed(new_health: float)
signal weapon_fired(weapon_type: String)

@export var max_speed: float = 100.0
@export var max_health: float = 100.0

var current_health: float
var is_alive: bool = true

func _ready() -> void:
    current_health = max_health

func take_damage(damage: float) -> void:
    current_health = max(0.0, current_health - damage)
    health_changed.emit(current_health)
```

## Workflow Enforcement

### Critical Rules
1. **Sequential Workflow**: Must follow PRD → Architecture → Stories → Implementation
2. **Single Epic Focus**: Only one epic in progress at a time
3. **Quality Gates**: Cannot skip approval checkpoints
4. **Documentation**: All artifacts must be documented and approved
5. **No Shortcuts**: Workflow violations will halt development

### Quality Checklists
The project includes comprehensive quality checklists for each phase:

- **`.bmad/checklists/workflow-enforcement.md`**: Overall BMAD workflow compliance
- **`.bmad/checklists/conversion-prd-quality-checklist.md`**: PRD quality validation (Curly)
- **`.bmad/checklists/godot-architecture-checklist.md`**: Architecture quality validation (Mo)
- **`.bmad/checklists/godot-ui-architecture-checklist.md`**: UI architecture validation (Mo)
- **`.bmad/checklists/story-readiness-checklist.md`**: Story readiness validation (SallySM)
- **`.bmad/checklists/story-definition-of-done-checklist.md`**: Implementation completion (Dev/QA)
- **`.bmad/checklists/change-management-checklist.md`**: Change impact management (All personas)

**Quality Gate Requirements:**
- **Before Architecture**: PRD completed + run conversion PRD quality checklist
- **Before Stories**: Architecture completed + run Godot architecture checklist
- **Before Implementation**: Stories approved + run story readiness checklist
- **Before Completion**: All acceptance criteria met + run definition of done checklist

## Git Workflow & Version Control

### Critical Git Practices
**IMPORTANT**: All generated artifacts and code must be committed regularly to maintain project integrity and track progress.

### Commit Schedule (MANDATORY)
Commit changes after each major BMAD workflow step:

1. **After Analysis Phase**: Commit analysis documents in `.ai/docs/`
2. **After PRD Creation**: Commit PRD documents in `.ai/docs/`
3. **After Architecture Design**: Commit architecture documents in `.ai/docs/`
4. **After Story Creation**: Commit user stories in `.ai/stories/`
5. **After Implementation**: Commit GDScript code in `target/` submodule + package docs
6. **After Validation**: Commit review documents in `.ai/reviews/`

### Git Commands for BMAD Workflow
```bash
# Commit main repository artifacts (.ai/ directory changes)
git add .ai/
git commit -m "feat: [phase] - [system-name] [brief description]"

# Commit target submodule (Godot project changes)
cd target/
git add .
git commit -m "feat: implement [feature-name] - [brief description]"
cd ..
git add target/
git commit -m "chore: update target submodule - [feature-name]"

# Push both repositories
git push origin main
cd target/
git push origin main
cd ..
```

### Commit Message Conventions
- **Analysis**: `docs: analyze [system-name] - [key findings]`
- **PRD**: `docs: create PRD for [system-name] - [scope summary]`
- **Architecture**: `docs: design architecture for [system-name] - [approach]`
- **Stories**: `docs: create stories for [epic-name] - [story count] stories`
- **Implementation**: `feat: implement [feature-name] - [functionality]`
- **Validation**: `docs: validate [feature-name] - [test results]`
- **Package Docs**: `docs: add CLAUDE.md for [package-name] - [purpose]`

## Common Commands

### Project Operations
```bash
# Run Godot project
godot --path target/

# Run specific scene
godot --path target/ --main-scene scenes/main_menu.tscn

# Run tests (if using GUT framework)
godot --path target/ -s addons/gut/gut_cmdln.gd
```

### BMAD Workflow
```
# Load orchestrator and become specific persona
/analyst          # Become Larry for C++ analysis
/architect        # Become Mo for Godot design
/dev             # Become Dev for implementation
/manager         # Become Curly for project management
/sm              # Become SallySM for story management
/qa              # Become QA for validation
```

## Documentation Templates

The project includes comprehensive templates for consistent documentation:

- **`.bmad/templates/conversion-prd-template.md`**: Product Requirements Documents (Curly)
- **`.bmad/templates/wcs-conversion-brief-template.md`**: High-level project briefs (Larry/Curly)
- **`.bmad/templates/godot-architecture-template.md`**: Technical architecture specifications (Mo)
- **`.bmad/templates/wcs-story-template.md`**: User story creation (SallySM)

### Package Documentation Standard
For each significant code package/module in `target/`, create a `CLAUDE.md` file containing:
- **Package Purpose**: What this package does and why it exists
- **Key Classes**: Main classes and their responsibilities
- **Usage Examples**: How other developers should use this package
- **Architecture Notes**: Important design decisions and patterns
- **Integration Points**: How this package connects with other systems
- **Performance Considerations**: Any performance-critical aspects
- **Testing Notes**: How to test this package and any special considerations

## File Organization

### Analysis Phase
- **Input**: C++ source code in `source/` submodule
- **Output**: Analysis documents in `.ai/docs/[system]-analysis.md`
- **Templates**: Use `.bmad/templates/wcs-conversion-brief-template.md`
- **Focus**: Understanding WCS systems and their functionality

### Architecture Phase
- **Input**: Analysis documents and requirements
- **Output**: Architecture documents in `.ai/docs/[system]-architecture.md`
- **Templates**: Use `.bmad/templates/godot-architecture-template.md`
- **Focus**: Godot-native system design and technical specifications

### Implementation Phase
- **Input**: Architecture specifications and user stories
- **Output**: GDScript code in `target/` submodule + `CLAUDE.md` package docs
- **Templates**: Follow package documentation standards
- **Focus**: Clean, typed, tested implementation with comprehensive documentation

### Quality Assurance
- **Input**: Implemented features and acceptance criteria
- **Output**: Validation reports and approval documentation
- **Focus**: Feature parity, performance, and code quality

## Success Metrics

- **Feature Parity**: Converted systems maintain WCS gameplay feel
- **Code Quality**: All code meets static typing and documentation standards
- **Performance**: Godot implementation meets or exceeds WCS performance
- **Maintainability**: Code is clean, well-documented, and testable
- **Architecture**: Systems are Godot-native and leverage engine strengths

## Contributing

### Workflow Compliance
- Always follow the BMAD workflow phases
- Use the appropriate AI persona for each task
- Run quality checklists before phase transitions
- Document all decisions and rationale

### Code Standards
- Follow GDScript static typing requirements
- Use Godot best practices and patterns
- Write comprehensive tests for all functionality
- Maintain clear, actionable documentation

### Quality Gates
- No untyped GDScript code
- No implementation without approved architecture
- No architecture without approved PRD
- No shortcuts or workflow violations

## License

[License information to be added]

## Acknowledgments

- Wing Commander Saga development team for the original C++ codebase
- Godot Engine community for excellent documentation and best practices
- BMAD methodology for structured AI-assisted development approach

---

**Remember**: This is not just a code conversion - it's a complete reimagining of WCS systems using Godot's strengths while preserving the original gameplay experience. Quality and methodology matter more than speed.

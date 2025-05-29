# WCS-Godot Converter Project

## Project Overview
This project converts Wing Commander Saga (WCS) from C++ to Godot Engine using GDScript, following the BMAD (Breakthrough Method of Agile AI-driven Development) methodology for structured, AI-assisted development.

**Core Mission**: Faithfully recreate WCS gameplay and feel in Godot while leveraging the engine's strengths and modern development practices.

## BMAD Agent System Integration

### Orchestrator Access
- **Main Orchestrator**: `.bmad/ide-orchestrator.md`
- **Configuration**: `.bmad/orchestrator-config.md`
- **Usage**: Load the orchestrator to access specialized personas for different development phases

### Available Personas
- **Larry (WCS Analyst)**: C++ code analysis, reverse engineering, system documentation
- **Mo (Godot Architect)**: Godot architecture design, extremely opinionated about best practices
- **Dev (GDScript Developer)**: Master of static typing, clean GDScript implementation
- **Curly (Conversion Manager)**: Project management, feature prioritization, PRD creation
- **SallySM (Story Manager)**: User story creation, workflow management, quality gates
- **QA (Quality Assurance)**: Feature validation, performance testing, final approval

### BMAD Workflow (CRITICAL - MUST FOLLOW)
```
1. PRD Creation (Curly) → 2. Architecture Design (Mo) → 3. Story Creation (SallySM) → 4. Implementation (Dev) → 5. Validation (QA)
```

**WORKFLOW ENFORCEMENT**: 
- NO architecture without approved PRD
- NO stories without approved architecture  
- NO implementation without approved stories
- ALWAYS run quality checklists before approval

## Project Structure

### Directory Organization
```
wcsaga_godot_converter/
├── .ai/                    # BMAD project artifacts
│   ├── docs/              # PRDs, Architecture documents (organized by epic)
│   │   ├── epic-001-core-foundation-infrastructure/
│   │   ├── epic-002-asset-structures-management/
│   │   └── [epic-name]/   # Analysis, PRD, Architecture docs per epic
│   ├── stories/           # User stories and tasks (organized by epic)
│   │   ├── epic-001-core-foundation-infrastructure/
│   │   ├── epic-002-asset-structures-management/
│   │   └── [epic-name]/   # Story files per epic
│   ├── epics/             # High-level epic definitions
│   └── reviews/           # Approval artifacts (organized by epic)
│       ├── epic-001-core-foundation-infrastructure/
│       ├── epic-002-asset-structures-management/
│       └── [epic-name]/   # Review documents per epic
├── .bmad/                 # BMAD framework (local copy)
│   ├── personas/          # Agent personalities
│   ├── tasks/             # Task definitions
│   ├── templates/         # Document templates
│   ├── checklists/        # Quality gates
│   └── data/              # Knowledge base
├── .claude/               # Claude-specific configurations
│   ├── commands/          # Custom slash commands
│   └── rules/             # Workflow enforcement
├── source/                # WCS C++ source (submodule)
├── target/                # Godot project (submodule)
└── CLAUDE.md             # This file
```

## Epic-Based Organization (MANDATORY)

### Folder Structure Rules
All BMAD artifacts MUST be organized by epic to maintain project clarity and enable effective tracking:

- **Analysis Documents**: `.ai/docs/[epic-name]/analysis.md`
- **PRD Documents**: `.ai/docs/[epic-name]/prd.md` 
- **Architecture Documents**: `.ai/docs/[epic-name]/architecture.md`
- **User Stories**: `.ai/stories/[epic-name]/[STORY-ID]-[story-name].md`
- **Review Documents**: `.ai/reviews/[epic-name]/[review-type].md`
- **Epic Definitions**: `.ai/epics/[epic-name].md`

### Epic Naming Convention
Epic folders follow the pattern: `epic-XXX-{main-component}-{sub-system}-{category}`

Examples:
- `epic-001-core-foundation-infrastructure`
- `epic-002-asset-structures-management`
- `epic-003-data-migration-conversion`

### Agent Responsibilities
Each BMAD agent MUST:
1. **Create artifacts in the correct epic folder**
2. **Update the parent epic document** with status/progress after completing work
3. **Reference epic context** when working on analysis, architecture, or stories
4. **Maintain epic boundaries** - don't mix work across different epics

### Epic Lifecycle Tracking
The epic document (`.ai/epics/[epic-name].md`) serves as the central hub for:
- Epic status and progress tracking
- Links to all related artifacts
- Summary of key findings and decisions
- Dependencies and relationships with other epics

## Godot Development Standards (OPINIONATED & NON-NEGOTIABLE)

### GDScript Coding Standards
- **ALWAYS use static typing** - Every variable, parameter, and return type must be explicitly typed
- **Class naming**: Use `class_name` declarations for all reusable classes
- **Naming conventions**: snake_case for variables/functions, PascalCase for classes, UPPER_CASE for constants
- **Documentation**: Every public function MUST have a docstring
- **Error handling**: Proper error checking and graceful failure handling

### Godot Architecture Principles
- **Scene composition over inheritance** - Prefer composition and scene instancing
- **Signal-based communication** - Use signals for loose coupling between systems
- **Single responsibility nodes** - Each node should have one clear purpose
- **Resource efficiency** - Preload small assets, load() dynamically for large ones
- **Proper node hierarchy** - Logical parent-child relationships

### Example GDScript Structure
```gdscript
class_name PlayerShip
extends CharacterBody3D

## A player-controlled spacecraft with movement, weapons, and shields.
## Handles input processing, physics movement, and combat systems.

signal health_changed(new_health: float)
signal shield_depleted()
signal weapon_fired(weapon_type: String)

@export var max_speed: float = 100.0
@export var acceleration: float = 50.0
@export var max_health: float = 100.0

var current_health: float
var shield_strength: float
var is_alive: bool = true

func _ready() -> void:
    current_health = max_health
    
func take_damage(damage: float) -> void:
    current_health = max(0.0, current_health - damage)
    health_changed.emit(current_health)
    
    if current_health <= 0.0:
        _handle_destruction()
```

## Common Development Commands

### Project Setup
```bash
# Run Godot project
Godot_v4.4.1-stable_win64.exe --path target/

# Run specific scene
Godot_v4.4.1-stable_win64 --path target/ --main-scene scenes/main_menu.tscn

# Run tests (if using GUT framework)
Godot_v4.4.1-stable_win64 --path target/ -s addons/gut/gut_cmdln.gd

# Export project for testing
Godot_v4.4.1-stable_win64 --path target/ --export-release "Windows Desktop" build/wcs_godot.exe

# Run headless for CI/testing
Godot_v4.4.1-stable_win64 --path target/ --headless --script scripts/run_tests.gd

# Check project for errors
Godot_v4.4.1-stable_win64 --path target/ --check-only --headless --script-editor=false --quit 
```

### BMAD Workflow Commands
- Load `.bmad/ide-orchestrator.md` as your active agent
- Use `/analyst` to become Larry for C++ analysis
- Use `/architect` to become Mo for Godot design
- Use `/dev` to become Dev for GDScript implementation
- Use `/bmad:create_prd {system_name}` to initiate PRD creation
- Use `/bmad:design_architecture {system_name}` to start architecture design
- Use `/bmad:create_story {epic_name}` to generate user stories
- Use `/bmad:implement_story {story_id}` to begin implementation
- Use `/bmad:validate_feature {feature_name}` to start QA validation
- Use `/bmad:run_checklist {checklist_name}` to execute quality gates

## WCS-Godot Conversion Guidelines

### Analysis Phase (Larry)
- Always examine actual C++ source code in `source/` submodule
- Focus on gameplay-critical systems first
- Document data flow and system interactions
- Identify performance-critical sections
- Create detailed analysis reports in `.ai/docs/`

### Architecture Phase (Mo)
- Design Godot-native solutions, not direct C++ ports
- Leverage Godot's node system and signals
- Plan for maintainability
- Create detailed technical specifications
- Challenge any non-optimal architectural decisions

### Implementation Phase (Dev)
- Follow architecture specifications exactly
- Use static typing for ALL code
- Write comprehensive unit tests
- Document all public APIs
- Optimize for readability
- **Create Package Documentation**: For each significant code package/module in `target/`, create a short `CLAUDE.md` file explaining the package's purpose, key classes, usage examples, architecture notes, integration points, performance considerations, and testing notes

### Quality Assurance (QA)
- Validate feature parity with original WCS
- We do not need explicit performance tests
- Verify code quality standards
- Ensure proper documentation
- Final approval before feature completion

## Key Integration Points

### Source Code Analysis
- **Location**: `source/` submodule contains WCS C++ code
- **Focus Areas**: `source/code/` directory structure
- **Key Systems**: Ship movement, weapons, AI, UI, missions
- **Analysis Output**: Store in `.ai/docs/[epic-name]/[system]-analysis.md`

### Godot Implementation
- **Location**: `target/` submodule contains Godot project
- **Scene Organization**: Logical separation of systems
- **Script Location**: Follow Godot project structure
- **Asset Management**: Efficient resource loading patterns

### BMAD Artifacts (Epic-Based Organization)
- **PRDs**: Product requirements in `.ai/docs/[epic-name]/`
- **Architecture**: Technical specifications in `.ai/docs/[epic-name]/`
- **Stories**: Implementation tasks in `.ai/stories/[epic-name]/`
- **Reviews**: Approval documentation in `.ai/reviews/[epic-name]/`
- **Epic Tracking**: Epic definitions and status in `.ai/epics/[epic-name].md`

## Quality Gates & Checklists

### Available Quality Checklists
- **`.bmad/checklists/workflow-enforcement.md`**: Overall BMAD workflow compliance
- **`.bmad/checklists/conversion-prd-quality-checklist.md`**: PRD quality validation (Curly)
- **`.bmad/checklists/godot-architecture-checklist.md`**: Architecture quality validation (Mo)
- **`.bmad/checklists/godot-ui-architecture-checklist.md`**: UI architecture validation (Mo)
- **`.bmad/checklists/story-readiness-checklist.md`**: Story readiness validation (SallySM)
- **`.bmad/checklists/story-definition-of-done-checklist.md`**: Implementation completion (Dev/QA)
- **`.bmad/checklists/change-management-checklist.md`**: Change impact management (Curly/SallySM)

### Before Architecture Design
- [ ] WCS system analysis completed and approved
- [ ] System requirements clearly defined
- [ ] Dependencies identified and documented
- [ ] Run `.bmad/checklists/conversion-prd-quality-checklist.md`

### Before Story Creation
- [ ] Architecture document completed and approved
- [ ] Technical specifications are detailed and actionable
- [ ] Integration points clearly defined
- [ ] Run `.bmad/checklists/godot-architecture-checklist.md`

### Before Implementation
- [ ] User stories have clear acceptance criteria
- [ ] Architecture specifications are complete
- [ ] Dependencies are resolved or planned
- [ ] Run `.bmad/checklists/story-readiness-checklist.md`

### Before Feature Completion
- [ ] All acceptance criteria met
- [ ] Unit tests written and passing
- [ ] Code review completed
- [ ] Documentation updated
- [ ] Performance validated
- [ ] Run `.bmad/checklists/story-definition-of-done-checklist.md`

## Critical Rules (ENFORCED BY BMAD)

1. **Sequential Workflow**: Must follow PRD → Architecture → Stories → Implementation
2. **Single Epic Focus**: Only one epic in progress at a time
3. **Quality Gates**: Cannot skip approval checkpoints
4. **Documentation**: All artifacts must be documented and approved
5. **Epic-Based Organization**: All docs/stories organized under respective epic folders
6. **Epic Updates**: Agents must update parent epic documents with status/progress
7. **Static Typing**: No untyped GDScript code allowed
8. **Godot Best Practices**: Architecture must be Godot-native, not ported C++
9. **Version Control**: MUST commit after each major workflow phase completion

## Git Workflow (MANDATORY)

### Commit Requirements
**CRITICAL**: All generated artifacts and code must be committed after each major BMAD workflow step to maintain project integrity and track progress.

### Commit Schedule
- **After Analysis**: Commit `.ai/docs/[system]-analysis.md` and related documents
- **After PRD Creation**: Commit `.ai/docs/[system]-prd.md` and project briefs
- **After Architecture**: Commit `.ai/docs/[system]-architecture.md` and specifications
- **After Story Creation**: Commit `.ai/stories/[story-files].md` and epic updates
- **After Implementation**: Commit `target/` submodule code + `CLAUDE.md` package docs
- **After Validation**: Commit `.ai/reviews/[validation-reports].md` and approvals

### Git Commands for Each Phase
```bash
# Main repository (BMAD artifacts)
git add .ai/
git commit -m "[phase]: [system-name] - [description]"

# Target submodule (Godot project)
cd target/
git add .
git commit -m "feat: implement [feature] - [description]"
cd ..
git add target/
git commit -m "chore: update target submodule - [feature]"

# Push both repositories
git push origin main
cd target/ && git push origin main && cd ..
```

### Commit Message Conventions
- **Analysis**: `docs: analyze [system] - [findings]`
- **PRD**: `docs: create PRD for [system] - [scope]`
- **Architecture**: `docs: design architecture for [system] - [approach]`
- **Stories**: `docs: create stories for [epic] - [count] stories`
- **Implementation**: `feat: implement [feature] - [functionality]`
- **Validation**: `docs: validate [feature] - [results]`

## Custom Slash Commands (Planned)

- `/project:start_conversion {system_name}` - Initialize BMAD workflow for WCS system
- `/project:analyze_cpp {file_or_system}` - Deep C++ code analysis with Larry
- `/project:design_godot {wcs_system}` - Architect Godot implementation with Mo
- `/project:implement_feature {story_name}` - GDScript implementation with Dev
- `/project:validate_conversion {feature_name}` - Quality validation with QA
- `/project:check_workflow` - Verify BMAD workflow compliance

## Success Metrics

- **Feature Parity**: Converted systems maintain WCS gameplay feel
- **Code Quality**: All code meets static typing and documentation standards
- **Performance**: Godot implementation meets or exceeds WCS performance
- **Maintainability**: Code is clean, well-documented, and testable
- **Architecture**: Systems are Godot-native and leverage engine strengths

## Important Notes

- **Source Reference**: Always reference specific files in `source/` when analyzing
- **Target Implementation**: All Godot code goes in `target/` submodule
- **BMAD Compliance**: Follow workflow strictly - no shortcuts allowed
- **Quality First**: Never compromise on code quality for speed
- **Godot Native**: Design for Godot, don't just port C++ patterns

Remember: This is not just a code conversion - it's a complete reimagining of WCS systems using Godot's strengths while preserving the original gameplay experience.

# Claude Code Orchestration System for Wing Commander Saga to Godot Migration

This directory contains the configuration and scripts for orchestrating the AI-assisted migration of Wing Commander Saga from C++ to Godot using Claude Code's native agentic features.

## System Overview

The orchestration system implements the workflow using:

1. **Specialized Agents** - AI personas with distinct expertise for different roles in the migration process
2. **Hooks** - Event-driven automation that triggers actions based on agent lifecycle events
3. **File-based State Management** - Markdown files that track task status and feedback
4. **Custom Commands** - Workflow commands for planning, implementation, and validation

## Workflow Commands

The system uses custom workflow commands:

- `/workflow:plan` - Analyzes user stories and breaks them down into detailed implementation tasks
- `/workflow:implement` - Implements specified tasks by reading markdown files and applying code changes
- `/workflow:validate` - Runs comprehensive validation of implementations with quality gates
- `/workflow:breakdown` - Breaks down user stories into detailed implementation tasks
- `/workflow:refine` - Refines and optimizes implemented features with performance tuning
- `/workflow:status` - Provides comprehensive project status reports with analytics

## Components

### 1. Specialized Agents
Created specialized agents in `.claude/agents/` for different aspects of the migration:

- **Godot Architect** - Plans Godot project structure and creates implementation plans
- **QA Engineer** - Validates implementations through testing and quality checks
- **Migration Architect** - Creates high-level migration strategies with data-centric architecture
- **C++ Code Analyst** - Analyzes existing C++ codebases and creates translation specifications
- **Godot Systems Designer** - Designs Godot-specific architectures following best practices
- **GDScript Engineer** - Implements game logic in GDScript with unit testing
- **Asset Pipeline Engineer** - Handles asset conversion and integration with automated pipelines
- **Lead Developer** - Provides oversight, technical guidance, and architectural review

### 2. Hook System
Created comprehensive event-driven automation in `.claude/hooks/` with full toolchain integration:

- `trigger_validation.sh` - Triggers QA validation after implementation with toolchain detection
- `process_architect_plan.sh` - Processes architectural plans into tasks using Python toolchain
- `check_build_status.sh` - Checks build status with toolchain-specific analysis and generates automated feedback
- `check_test_status.sh` - Checks test status with framework-specific analysis and generates automated feedback
- `run_validation.sh` - Runs comprehensive quality checks across all toolchains
- `process_asset_pipeline.sh` - Processes asset pipeline plans with Godot headless mode integration
- `process_code_analysis.sh` - Processes code analysis reports with comprehensive toolchain analysis
- `generate_feedback.sh` - Generates toolchain-aware automated feedback based on failure types
- `validate_file_structure.sh` - Validates file structure and manages project state updates when agents stop
- `session_start.sh` - Loads project state and context at session initialization
- `state_update.sh` - Updates project state JSON file with task completion information
- `process_plan.py` - Python script to convert JSON plans to task files

### 3. Custom Commands
Implemented workflow commands in `.claude/commands/`:

- `plan.md` - Creates and manages project planning artifacts (PRDs, Epics, Stories)
- `breakdown.md` - Breaks down user stories into detailed implementation tasks
- `implement.md` - Implements migration tasks using specialized agents
- `validate.md` - Comprehensive validation of migration tasks with quality gates
- `refine.md` - Refinement and optimization of implemented features
- `status.md` - Provides comprehensive project status report with analytics

### 4. Configuration
- `.claude/settings.json` - Defines hook triggers and commands (with relative paths)
- `.claude/settings.local.json` - Maintains existing permissions

### 5. Workflow Directories
- `.workflow/tasks/` - Storage for task files
- `.workflow/logs/` - Storage for log files
- `.workflow/prds/` - Storage for Product Requirement Documents
- `.workflow/epics/` - Storage for Epics
- `.workflow/stories/` - Storage for User Stories

## Directory Structure

```
.claude/
├── agents/                 # Specialized agent configurations
├── commands/               # Custom workflow commands
├── hooks/                  # Hook scripts for automation
├── settings.json           # Claude Code hook configuration
└── settings.local.json     # Local permissions configuration

.workflow/
├── tasks/                  # Individual task files in markdown format
├── logs/                   # Log files from validation and other processes
├── prds/                   # Product Requirement Documents
├── epics/                  # Epics
└── stories/                # User Stories
```

## Specialized Agents

The system uses several specialized agents with distinct expertise:

1. **Godot Architect** - Breaks down user stories into implementation tasks with Godot migration patterns
2. **QA Engineer** - Validates GDScript implementations with comprehensive quality gates
3. **Migration Architect** - Creates data-centric architecture plans using Godot's Resource system
4. **C++ Code Analyst** - Performs deep static analysis and creates translation specifications
5. **Godot Systems Designer** - Designs Godot-specific architectures and custom resource specifications
6. **GDScript Engineer** - Implements game logic in GDScript with unit testing
7. **Asset Pipeline Engineer** - Builds automated asset conversion pipelines with EditorImportPlugin
8. **Lead Developer** - Provides architectural oversight and technical guidance

## Hooks

The system uses comprehensive hooks to automate workflow transitions with full toolchain integration:

1. **SubagentStop (godot_architect)** - Processes architectural plans and creates task files
2. **SubagentStop (gdscript-engineer)** - Triggers comprehensive validation after implementation
3. **SubagentStop (asset-pipeline-engineer)** - Processes asset pipeline plans with Godot integration
4. **SubagentStop (cpp-code-analyst)** - Processes code analysis reports with toolchain analysis
5. **SubagentStop (qa_engineer)** - Checks test status and generates feedback
6. **PostToolUse (Bash)** - Checks build status and generates automated feedback
7. **PreToolUse (Write)** - Validates file structure and naming conventions
8. **SessionStart** - Loads project state and context at session initialization

## Workflow Process

1. **Planning**: Create PRDs, Epics, and Stories using the planning command
2. **Breakdown**: Break down stories into implementation tasks using the breakdown command
3. **Analysis**: C++ Code Analyst examines source code and creates translation specification
4. **Design**: Godot Systems Designer creates target architecture and resource specifications
5. **Implementation**: GDScript Engineer implements tasks with unit tests
6. **Validation**: QA Engineer automatically validates implementations through hooks
7. **Refinement**: Optimize and improve implemented features based on performance metrics
8. **Status Monitoring**: Track progress and identify blockers with status reports

## Key Features

- **AI-Orchestrated Development**: Workflow follows structured methodology with specialized agents
- **Event-Driven Automation**: Hooks automatically trigger next steps based on agent completion
- **File-Based State Management**: Markdown files track task status and feedback with YAML frontmatter
- **Automated Remediation**: Failed validations automatically generate detailed feedback
- **Specialized Roles**: Granular agent specialization for technical domains
- **Hierarchical Planning**: PRDs → Epics → Stories → Tasks structure for project organization
- **Toolchain Integration**: Full integration with Godot, Python, and GDScript development tools
- **Quality Gates**: Automated validation at every step with comprehensive testing

## Task File Format

Tasks are stored as markdown files with YAML frontmatter:

```markdown
---
id: TASK-001
title: Setup native class boilerplate
status: pending
dependencies: []
assignee: gdscript-engineer
files_to_modify:
  - src/file.gd
---

# Task: Setup native class boilerplate

## Description
Brief description of what needs to be done following Godot best practices.

## Acceptance Criteria
- [ ] Checklist of requirements
- [ ] Each item should be verifiable
- [ ] Follows Godot project structure conventions

## Implementation Notes
Additional context for the implementer.

## Feedback
Human or automated feedback goes here.
```

## Usage

To use the orchestration system:

1. Create planning artifacts using the `/workflow:plan` command
2. Break down stories into tasks with the `/workflow:breakdown` command
3. Use C++ Code Analyst to analyze source code and create translation specifications
4. Use Godot Systems Designer to create target architecture and resource specifications
5. Implement tasks using the GDScript Engineer agent via `/workflow:implement`
6. Validation happens automatically through hooks with QA Engineer
7. Refine implementations using the `/workflow:refine` command
8. Monitor progress with the `/workflow:status` command

## Development Toolchain Integration

The system features comprehensive integration with the full development toolchain:

### Core Toolchain Integration:
- **Godot Headless Mode** - Automated asset processing and validation
- **GDScript Toolkit** - `gdformat` for formatting and `gdlint` for code quality
- **Python Environment** - `uv` for high-performance dependency management
- **Python Linting/Formatting** - `ruff` for comprehensive Python code quality
- **Python Testing** - `pytest` for unit testing and test automation
- **Pattern Analysis** - Sophisticated `grep` usage for log analysis and validation

### Framework-Specific Analysis:
- **Python Builds** - Dependency validation, import checking, and package management
- **Godot Builds** - Export configuration validation, asset import checking, and template verification
- **Test Frameworks** - Support for pytest, gdunit4, and unittest with framework-specific error analysis
- **Code Quality** - Multi-language linting and formatting validation

### Automated Feedback Generation:
- Toolchain-aware feedback based on failure types (build, test, validation)
- Framework-specific recommendations for remediation
- Priority-based issue categorization (high, medium, low severity)
- Comprehensive log analysis with context-aware error extraction

This orchestration system enables a semi-autonomous workflow that de-risks complex migrations while maintaining human oversight through the feedback loop.

## Testing

The system has been comprehensively tested with full toolchain integration:
- All hook scripts execute properly with relative paths and toolchain detection
- Python scripts for processing architectural plans work correctly with uv integration
- Task files are generated with proper YAML frontmatter and toolchain-aware content
- Log files are created with comprehensive toolchain analysis and error categorization
- Framework-specific validation works for Python, GDScript, and Godot toolchains
- Automated feedback generation provides context-aware recommendations
- File structure validation enforces Godot project conventions and naming standards

## Next Steps

The system is ready for use. To begin a migration task:
1. Create planning artifacts using the `/workflow:plan` command
2. Use C++ Code Analyst to analyze the source code
3. Use Godot Systems Designer to create the target architecture
4. Break down stories into tasks with the `/workflow:breakdown` command
5. Implement tasks using the GDScript Engineer agent via `/workflow:implement`
6. Validation will happen automatically through hooks with QA Engineer

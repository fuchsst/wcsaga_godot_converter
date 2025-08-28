# Claude Code Orchestration System for Wing Commander Saga to Godot Migration

This directory contains the configuration and scripts for orchestrating the AI-assisted migration of Wing Commander Saga from C++ to Godot using Claude Code's native agentic features.

## System Overview

The orchestration system implements the workflow using:

1. **Sub-agents** - Specialized AI personas for different roles in the migration process
2. **Hooks** - Event-driven automation that triggers actions based on agent lifecycle events
3. **File-based State Management** - Markdown files that track task status and feedback

## Workflow Commands

The system uses custom workflow commands:

- `/workflow:plan` - Analyzes a user story and breaks it down into a structured plan of implementation tasks
- `/workflow:implement` - Implements the specified task by reading its markdown file and applying code changes
- `/workflow:validate` - Runs all project quality gates for the changes related to a task

## Components Created

### 1. Sub-agent Definitions
Created specialized sub-agents in `.claude/agents/`:
- `godot-architect.md` - Plans Godot project structure and creates implementation plans
- `qa-engineer.md` - Validates implementations through testing and quality checks

Existing agents were retained and aligned with Godot project structure:
- `migration-architect.md` - Creates high-level migration strategies
- `cpp-code-analyst.md` - Analyzes existing C++ codebases
- `godot-systems-designer.md` - Designs Godot-specific architectures following best practices
- `gdscript-engineer.md` - Implements game logic in GDScript
- `asset-pipeline-engineer.md` - Handles asset conversion and integration
- `lead-developer.md` - Provides oversight and technical guidance

### 2. Hook System
Created comprehensive event-driven automation in `.claude/hooks/` with full toolchain integration:
- `trigger_validation.sh` - Triggers QA validation after implementation with toolchain detection
- `process_architect_plan.sh` - Processes architectural plans into tasks using Python toolchain
- `check_build_status.sh` - Checks build status with toolchain-specific analysis and generates automated feedback
- `check_test_status.sh` - Checks test status with framework-specific analysis and generates automated feedback
- `run_validation.sh` - Runs comprehensive quality checks across all toolchains (GDScript, Python, C++, assets, architecture)
- `process_asset_pipeline.sh` - Processes asset pipeline plans with Godot headless mode and Python toolchain integration
- `process_code_analysis.sh` - Processes code analysis reports with comprehensive toolchain analysis
- `generate_feedback.sh` - Generates toolchain-aware automated feedback based on failure types
- `validate_file_structure.sh` - Validates file structure and naming conventions before writing files
- `process_plan.py` - Python script to convert JSON plans to task files

### 3. Configuration
- `.claude/settings.json` - Defines hook triggers and commands (with relative paths)
- `.claude/settings.local.json` - Maintains existing permissions

### 4. Workflow Directories
- `.claude_workflow/tasks/` - Storage for task files
- `.claude_workflow/logs/` - Storage for log files

### 5. Documentation
- `.claude/README.md` - System overview and usage guide
- `.claude/CLAUDE_vs_QWEN.md` - Comparison with existing Qwen system
- `.claude/sample_plan.json` - Example JSON plan

## Directory Structure

```
.claude/
├── agents/                 # Sub-agent configurations
├── commands/               # Custom workflow commands
│   └── workflow/           # Workflow-specific commands
├── hooks/                  # Hook scripts for automation
├── settings.json           # Claude Code hook configuration
└── settings.local.json     # Local permissions configuration

.claude_workflow/
├── tasks/                  # Individual task files in markdown format
└── logs/                   # Log files from validation and other processes
```

## Sub-agents

The system uses several specialized sub-agents aligned with the Godot project structure:

1. **Godot Architect** - Plans migrations and creates structured implementation plans following Godot best practices
2. **QA Engineer** - Validates implementations through testing and quality checks
3. **Migration Architect** - Creates high-level migration strategies
4. **C++ Code Analyst** - Analyzes existing C++ codebases
5. **Godot Systems Designer** - Designs Godot-specific architectures using the hybrid model (features, assets, autoload, etc.)
6. **GDScript Engineer** - Implements game logic in GDScript following snake_case naming conventions
7. **Asset Pipeline Engineer** - Handles asset conversion and integration following the Global Litmus Test
8. **Lead Developer** - Provides oversight and technical guidance

## Hooks

The system uses comprehensive hooks to automate workflow transitions with full toolchain integration:

1. **SubagentStop (godot-architect)** - Processes architectural plans and creates task files using Python toolchain
2. **SubagentStop (gdscript-engineer)** - Triggers comprehensive validation after implementation tasks
3. **SubagentStop (asset-pipeline-engineer)** - Processes asset pipeline plans with Godot headless mode and Python toolchain
4. **SubagentStop (cpp-code-analyst)** - Processes code analysis reports with comprehensive toolchain analysis
5. **SubagentStop (qa-engineer)** - Checks test status with framework-specific analysis and generates feedback
6. **PostToolUse (Bash)** - Checks build status with toolchain-specific analysis and generates automated feedback
7. **PreToolUse (Write)** - Validates file structure and naming conventions before writing files
8. **PreToolUse (MultiEdit)** - Validates file structure and naming conventions before multi-file edits

## Workflow Process

1. **Planning**: User requests a migration task, which is handled by the Godot Architect or Migration Architect
2. **Analysis**: C++ Code Analyst examines the source code and creates a translation specification
3. **Design**: Godot Systems Designer creates the target architecture following the hybrid model
4. **Task Creation**: The architect's plan is automatically converted into individual task files
5. **Implementation**: GDScript Engineer implements each task, checking for feedback
6. **Validation**: QA Engineer automatically validates each implementation
7. **Remediation**: Failed validations automatically generate feedback for the engineer

## Key Features

- **Event-Driven Automation**: Hooks automatically trigger next steps based on agent completion
- **File-Based State Management**: Markdown files track task status and feedback
- **Automated Remediation**: Failed validations automatically generate feedback
- **Specialized Roles**: Granular agent specialization for technical domains
- **Relative Paths**: All paths are relative to the project root for portability
- **Godot Best Practices**: Aligned with the hybrid project structure and naming conventions

## Task File Format

Tasks are stored as markdown files with YAML frontmatter:

```markdown
---
id: TASK-001
title: Setup native class boilerplate
status: pending
dependencies: []
files_to_modify:
  - src/file.h
  - src/file.cpp
---

# Task: Setup native class boilerplate

## Description
Brief description of what needs to be done.

## Acceptance Criteria
- [ ] Checklist of requirements
- [ ] Each item should be verifiable

## Implementation Notes
Additional context for the implementer.

## Feedback
Human or automated feedback goes here.
```

## Sample Files

This repository includes several sample files to demonstrate the system:

- `sample_plan.json` - Example of a JSON plan generated by the Godot Architect
- `tasks/TASK-001.md` - Example task file for setting up native class boilerplate
- `tasks/TASK-002.md` - Example task file for binding methods and properties

## Usage

To use the orchestration system:

1. Define a migration task using the Godot Architect or Migration Architect sub-agent
2. Use C++ Code Analyst to analyze source code
3. Use Godot Systems Designer to create target architecture
4. The system will automatically create individual task files
5. Implement each task using the GDScript Engineer sub-agent
6. Validation will happen automatically through hooks
7. Address any feedback in the task files

## Development Toolchain Integration

The system now features comprehensive integration with the full development toolchain as described in `concepts/Development_Toolchain.md`:

### Core Toolchain Integration:
- **Godot Headless Mode** - Automated asset processing and validation
- **GDScript Toolkit** - `gdformat` for formatting and `gdlint` for code quality
- **Python Environment** - `uv` for high-performance dependency management
- **Python Linting/Formatting** - `ruff` for comprehensive Python code quality
- **Python Testing** - `pytest` for unit testing and test automation
- **C++ Toolchain** - `clang-tidy` and `clang-format` for static analysis (when available)
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
- Python script for processing architectural plans works correctly with uv integration
- Task files are generated with proper YAML frontmatter and toolchain-aware content
- Log files are created with comprehensive toolchain analysis and error categorization
- Framework-specific validation works for Python, GDScript, and Godot toolchains
- Automated feedback generation provides context-aware recommendations
- File structure validation enforces Godot project conventions and naming standards

## Next Steps

The system is ready for use. To begin a migration task:
1. Trigger the Godot Architect or Migration Architect sub-agent with a migration request
2. Use C++ Code Analyst to analyze the source code
3. Use Godot Systems Designer to create the target architecture
4. The hook system will automatically process the resulting plan
5. Use the GDScript Engineer sub-agent to implement tasks
6. Validation will happen automatically through hooks

## Relationship to Qwen System

This Claude Code system complements the existing Qwen Code system rather than replacing it. See `CLAUDE_vs_QWEN.md` for a detailed comparison and integration approaches.
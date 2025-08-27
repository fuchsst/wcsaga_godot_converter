# Qwen CLI Commands for Wing Commander Saga to Godot Migration

This directory contains custom Qwen CLI commands that trigger workflows using the AI agents defined in `.claude/agents/**`.

## Command Structure

Commands are organized in two namespaces:
- `/agent:` - Direct agent commands
- `/workflow:` - Orchestration workflow commands

## Available Commands

### Individual Agent Commands
- `/agent:migration-architect` - Triggers the Migration Architect agent
- `/agent:cpp-code-analyst` - Triggers the C++ Code Analyst agent
- `/agent:godot-systems-designer` - Triggers the Godot Systems Designer agent
- `/agent:gdscript-engineer` - Triggers the GDScript Engineer agent
- `/agent:asset-pipeline-engineer` - Triggers the Asset Pipeline Engineer agent
- `/agent:lead-developer` - Triggers the Lead Developer agent

### Workflow Orchestration Commands
- `/workflow:plan` - Analyzes a user story and breaks it down into a structured plan of implementation tasks
- `/workflow:implement` - Implements the specified task by reading its markdown file and applying code changes
- `/workflow:validate` - Runs all project quality gates for the changes related to a task
- `/workflow:list` - Lists all available workflow commands

## Workflow Orchestration Principles

The workflow follows the principles outlined in `concepts/Workflow_Orchestration.md`:

1. **Planning** - Use `/workflow:plan` to break down user stories into structured tasks
2. **Implementation** - Use `/workflow:implement` to execute tasks with appropriate agents
3. **Validation** - Use `/workflow:validate` to run quality checks and ensure code quality

## State Management

Tasks are tracked in the `.qwen_workflow/tasks/` directory with markdown files that include:
- Task metadata in YAML frontmatter
- Description and acceptance criteria
- Status tracking
- Feedback section for human review

Logs are stored in the `.qwen_workflow/logs/` directory.

## Usage

To use these commands, simply type them in the Qwen Code CLI:

```
/workflow:plan "Implement player ship movement with Newtonian physics"
```

```
/workflow:implement TASK-001
```

```
/workflow:validate TASK-001
```

## Agent Workflow

The agents work together in a structured workflow:

1. **Migration Architect** creates the master strategy for a data-driven rewrite
2. Its output feeds to both **C++ Code Analyst** and **Godot Systems Designer**
3. **C++ Code Analyst** produces detailed translation specification for GDScript rewrite
4. **Godot Systems Designer** creates Godot-native architecture and custom resources
5. **GDScript Engineer** and **Asset Pipeline Engineer** work in parallel to implement:
   - Game logic in GDScript with unit tests
   - Asset conversion and integration pipeline
6. **Lead Developer** provides oversight and validation throughout the process

Each agent is designed to integrate with the development toolchain:
- `grep` for searching and validation
- `run_shell_command` for executing commands
- `pytest` and `uv` for Python tooling
- `gdformat`, `gdlint`, and `gdUnit4` for GDScript quality assurance
- Godot headless mode for automated processes
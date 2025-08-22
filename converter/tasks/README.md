# Task Definitions

This directory contains the task definitions and templates for the migration system.

## Task Configuration Files

- `analysis_task.yaml` - Configuration for codebase analysis tasks
- `decomposition_task.yaml` - Configuration for task decomposition tasks
- `planning_task.yaml` - Configuration for migration planning tasks
- `refactoring_task.yaml` - Configuration for code refactoring tasks
- `testing_task.yaml` - Configuration for testing tasks
- `validation_task.yaml` - Configuration for validation tasks

## Task Templates

The `task_templates/` directory contains structured prompt templates specifically designed for qwen-code:

- `qwen_prompt_templates.py` - Specific templates for different qwen-code task types

## Task Structure

Each task configuration file defines:

1. **Task Name** - Human-readable name for the task
2. **Description** - Detailed description of what the task should accomplish
3. **Expected Output** - Description of the expected output format
4. **Assigned Agent** - Which agent is responsible for executing the task
5. **Context** - Any prerequisite tasks or context needed

## Usage

The task definitions are used by the Orchestrator to create and manage the migration workflow.
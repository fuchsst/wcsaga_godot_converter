# Project Status Dashboard

This file provides a high-level overview of all tasks in the workflow.

## Task Summary

| Task ID | Title | Status | Assignee |
| ------- | ----- | ------ | -------- |
| TEMPLATE | Sample Task Template | pending | qwen-coder |

## Workflow Commands

To manage the workflow, use the following commands:

- `/workflow:plan` - Create a plan from a user story
- `/workflow:implement` - Implement a specific task
- `/workflow:validate` - Validate implementation with quality checks
- `/workflow:list` - List all available workflow commands

## State Management

Tasks are tracked in the `.qwen_workflow/tasks/` directory with markdown files that include:
- Task metadata in YAML frontmatter
- Description and acceptance criteria
- Status tracking
- Feedback section for human review

Logs are stored in the `.qwen_workflow/logs/` directory.
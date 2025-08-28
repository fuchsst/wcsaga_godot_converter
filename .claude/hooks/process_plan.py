#!/usr/bin/env python3

# This script processes a Godot Architect's JSON plan
# and converts it into individual task files following the Godot project structure

import json
import os
from datetime import datetime

def create_task_file(task_data, tasks_dir):
    """Create a markdown task file from task data"""
    task_id = task_data["id"]
    title = task_data["title"]
    dependencies = task_data["dependencies"]
    files_to_modify = task_data["files_to_modify"]
    
    # Create the YAML frontmatter
    frontmatter = f'''---
id: {task_id}
title: {title}
status: pending
dependencies: {dependencies}
assignee: claude-code
files_to_modify:
'''
    
    for file in files_to_modify:
        frontmatter += f'  - {file}\n'
    
    frontmatter += '---\n'
    
    # Create the task content
    content = f'''# Task: {title}

## Description
TODO: Add detailed description of what needs to be done following Godot best practices.

## Acceptance Criteria
- [ ] TODO: Add specific acceptance criteria
- [ ] Each item should be verifiable
- [ ] Follows Godot project structure (features, assets, autoload, etc.)
- [ ] Uses snake_case naming conventions

## Implementation Notes
TODO: Add additional context for the implementer.

## Feedback
'''
    
    # Write the task file
    task_file_path = os.path.join(tasks_dir, f"{task_id}.md")
    with open(task_file_path, 'w') as f:
        f.write(frontmatter)
        f.write(content)
    
    print(f"Created task file: {task_file_path}")

def process_architect_plan(plan_file, tasks_dir):
    """Process an architect's JSON plan and create task files"""
    # Read the JSON plan
    with open(plan_file, 'r') as f:
        plan = json.load(f)
    
    print(f"Processing plan with {len(plan)} tasks...")
    
    # Create task files for each task in the plan
    for task_data in plan:
        create_task_file(task_data, tasks_dir)
    
    print("Plan processing complete!")

if __name__ == "__main__":
    # In a real implementation, these would come from the hook environment
    plan_file = "./.claude/sample_plan.json"
    tasks_dir = "./.claude_workflow/tasks"
    
    # Ensure the tasks directory exists
    os.makedirs(tasks_dir, exist_ok=True)
    
    # Process the plan
    process_architect_plan(plan_file, tasks_dir)
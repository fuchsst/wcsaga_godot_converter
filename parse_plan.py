#!/usr/bin/env python3
"""
Helper script to parse JSON plan and create task files
"""
import json
import sys
import os
import re
from datetime import datetime

def convert_text_to_json(content):
    """Convert text work package breakdown to JSON format"""
    tasks = []
    task_counter = 1
    
    # Extract work packages using regex
    work_package_pattern = r'### Work Package \d+: (.+?)\n\*\*Priority: (.+?)\*\*\n(.*?)(?=### Work Package|\n## |$)'
    matches = re.findall(work_package_pattern, content, re.DOTALL)
    
    for title, priority, description in matches:
        # Extract individual tasks from bullet points
        bullet_points = re.findall(r'^- (.+?)$', description, re.MULTILINE)
        
        if bullet_points:
            # Create a task for the work package
            task_id = f"TASK-{task_counter:03d}"
            task = {
                "id": task_id,
                "title": title.strip(),
                "dependencies": [],
                "files_to_modify": []
            }
            tasks.append(task)
            task_counter += 1
        else:
            # If no bullet points, create a single task from the title
            task_id = f"TASK-{task_counter:03d}"
            task = {
                "id": task_id,
                "title": title.strip(),
                "dependencies": [],
                "files_to_modify": []
            }
            tasks.append(task)
            task_counter += 1
    
    # If no work packages found, try to extract from any numbered or bulleted list
    if not tasks:
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if re.match(r'^\d+\.', line) or line.startswith('- '):
                title = re.sub(r'^\d+\.?\s*|\-\s*', '', line).strip()
                if title and len(title) > 3:  # Skip very short titles
                    task_id = f"TASK-{task_counter:03d}"
                    task = {
                        "id": task_id,
                        "title": title,
                        "dependencies": [],
                        "files_to_modify": []
                    }
                    tasks.append(task)
                    task_counter += 1
    
    return tasks if tasks else None

def parse_plan_and_create_tasks(plan_file):
    """Parse the JSON plan and create individual task files"""
    with open(plan_file, 'r') as f:
        content = f.read().strip()
    
    # Try to parse as JSON first
    try:
        plan = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"JSON parsing failed: {e}")
        print("Attempting to convert text output to JSON format...")
        plan = convert_text_to_json(content)
        if not plan:
            print("Failed to convert text to JSON. Exiting.")
            sys.exit(1)
    
    # Create tasks directory if it doesn't exist
    tasks_dir = ".qwen_workflow/tasks"
    os.makedirs(tasks_dir, exist_ok=True)
    
    # Create task files
    task_list = []
    for task in plan:
        task_id = task["id"]
        title = task["title"]
        dependencies = task["dependencies"]
        files_to_modify = task["files_to_modify"]
        
        # Create task content with YAML frontmatter
        task_content = f"""---
id: {task_id}
title: "{title}"
status: pending
dependencies: {dependencies}
assignee: qwen-coder
files_to_modify: {files_to_modify}
---

## Description
{title}

## Acceptance Criteria
- [ ] Implement the functionality
- [ ] Test the implementation
- [ ] Document the changes

## Feedback
"""
        
        # Write task file
        task_filename = f"{tasks_dir}/{task_id}.md"
        with open(task_filename, 'w') as f:
            f.write(task_content)
        
        task_list.append({
            "id": task_id,
            "title": title,
            "status": "pending",
            "assignee": "qwen-coder"
        })
        
        print(f"Created task file: {task_filename}")
    
    # Update project status dashboard
    update_project_status(task_list)
    
    print(f"Successfully created {len(task_list)} task files")

def update_project_status(task_list):
    """Update the project status dashboard"""
    status_file = "PROJECT_STATUS.md"
    
    # Read existing content
    with open(status_file, 'r') as f:
        lines = f.readlines()
    
    # Find the task summary section
    task_summary_start = -1
    for i, line in enumerate(lines):
        if line.strip() == "## Task Summary":
            task_summary_start = i
            break
    
    if task_summary_start == -1:
        print("Could not find task summary section in PROJECT_STATUS.md")
        return
    
    # Find the end of the task summary table
    task_summary_end = len(lines)
    for i in range(task_summary_start + 1, len(lines)):
        if lines[i].startswith("## "):
            task_summary_end = i
            break
    
    # Generate new task summary table
    task_table = ["\n| Task ID | Title | Status | Assignee |\n",
                  "| ------- | ----- | ------ | -------- |\n"]
    
    # Add new tasks
    for task in task_list:
        task_table.append(f"| {task['id']} | {task['title']} | {task['status']} | {task['assignee']} |\n")
    
    # Replace the task summary section (keep only the header and new tasks)
    new_lines = lines[:task_summary_start + 3] + task_table + lines[task_summary_end:]
    
    # Write updated content
    with open(status_file, 'w') as f:
        f.writelines(new_lines)
    
    print("Updated project status dashboard")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python parse_plan.py <plan.json>")
        sys.exit(1)
    
    plan_file = sys.argv[1]
    if not os.path.exists(plan_file):
        print(f"Plan file {plan_file} does not exist")
        sys.exit(1)
    
    parse_plan_and_create_tasks(plan_file)
#!/bin/bash

# This script is triggered when the Godot Architect sub-agent completes a task
# It processes the JSON plan and materializes it into individual task files

set -e

# Read the hook event data from stdin
HOOK_DATA=$(cat)

# Create log and task directories if they don't exist
mkdir -p ./.claude_workflow/logs
mkdir -p ./.claude_workflow/tasks

# Log that plan processing is being triggered
echo "$(date): Plan processing triggered" >> ./.claude_workflow/logs/hook.log

# Try to extract JSON plan from hook data
JSON_PLAN=""
if echo "$HOOK_DATA" | grep -q "```json"; then
    JSON_PLAN=$(echo "$HOOK_DATA" | sed -n '/```json/,/```/p' | grep -v '```')
elif echo "$HOOK_DATA" | grep -q '\[{'; then
    # Try to find JSON array directly
    JSON_PLAN=$(echo "$HOOK_DATA" | grep -o '\[{.*}\]' | head -1)
fi

# Validate the JSON plan using Python's json.tool if available
if [ -n "$JSON_PLAN" ]; then
    echo "$(date): Found JSON plan in hook data, validating format" >> ./.claude_workflow/logs/hook.log
    # Use Python's built-in JSON validation
    if echo "$JSON_PLAN" | python -m json.tool > /dev/null 2>&1; then
        echo "$(date): JSON format is valid" >> ./.claude_workflow/logs/hook.log
    else
        echo "$(date): JSON format is invalid, attempting to fix" >> ./.claude_workflow/logs/hook.log
        # Try to fix common JSON issues
        JSON_PLAN=$(echo "$JSON_PLAN" | sed 's/\\'/\\\\"/g')
    fi
fi

if [ -n "$JSON_PLAN" ]; then
    echo "$(date): Found JSON plan in hook data" >> ./.claude_workflow/logs/hook.log
    
    # Save the JSON plan to a temporary file
    echo "$JSON_PLAN" > ./.claude_workflow/temp_plan.json
    
    # Run the Python script to process the plan
    echo "$(date): Running process_plan.py on extracted plan" >> ./.claude_workflow/logs/hook.log
    if uv run python ./.claude/hooks/process_plan.py ./.claude_workflow/temp_plan.json; then
        echo "$(date): Plan processing successful" >> ./.claude_workflow/logs/hook.log
        
        # Extract plan entities and update project state
        echo "$(date): Updating project state with plan entities" >> ./.claude_workflow/logs/hook.log
        
        # Parse JSON and create hierarchical entities
        if command -v python3 &> /dev/null; then
            python3 -c "
import json
import sys
import subprocess
import datetime

try:
    with open('./.claude_workflow/temp_plan.json', 'r') as f:
        plan = json.load(f)
    
    # Generate PRD from plan context
    plan_title = 'Architect Plan - ' + datetime.datetime.now().strftime('%Y-%m-%d')
    prd_id = 'PRD-ARCHITECT-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    
    subprocess.run(['./.claude/hooks/state_update.sh', 'update', 'add_prd', prd_id, plan_title], 
                   capture_output=True, text=True)
    
    # If plan contains structured tasks, create epics and stories
    if isinstance(plan, list):
        for i, task in enumerate(plan):
            if isinstance(task, dict) and 'title' in task:
                epic_id = f'EPIC-{i+1:03d}'
                epic_title = task.get('title', f'Epic {i+1}')
                
                subprocess.run(['./.claude/hooks/state_update.sh', 'update', 'add_epic', 
                               epic_id, epic_title, prd_id], capture_output=True, text=True)
                
                # Create story for the task
                story_id = f'STORY-{i+1:03d}'
                story_title = task.get('description', epic_title)
                
                subprocess.run(['./.claude/hooks/state_update.sh', 'update', 'add_story', 
                               story_id, story_title, epic_id], capture_output=True, text=True)
    
    print('Project state updated with plan entities')
    
except Exception as e:
    print(f'Error updating project state: {e}', file=sys.stderr)
    sys.exit(1)
" 2>>./.claude_workflow/logs/hook.log || true
        fi
        
        # Clean up temporary file
        rm -f ./.claude_workflow/temp_plan.json
    else
        echo "$(date): Plan processing failed" >> ./.claude_workflow/logs/hook.log
        exit 1
    fi
else
    echo "$(date): No JSON plan found in hook data, running with sample plan" >> ./.claude_workflow/logs/hook.log
    
    # Fallback to processing with sample plan if available
    if [ -f "./.claude/sample_plan.json" ]; then
        # Validate the sample plan before processing
        if python -m json.tool ./.claude/sample_plan.json > /dev/null 2>&1; then
            echo "$(date): Sample plan JSON format is valid" >> ./.claude_workflow/logs/hook.log
            uv run python ./.claude/hooks/process_plan.py ./.claude/sample_plan.json
        else
            echo "$(date): Sample plan JSON format is invalid" >> ./.claude_workflow/logs/hook.log
            exit 1
        fi
    else
        echo "$(date): No sample plan available" >> ./.claude_workflow/logs/hook.log
    fi
fi

echo "$(date): Plan processing complete" >> ./.claude_workflow/logs/hook.log
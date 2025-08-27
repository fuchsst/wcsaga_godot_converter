#!/bin/bash
# Master orchestration script for the Wing Commander Saga to Godot migration workflow

set -e  # Exit immediately if a command exits with a non-zero status

# Function to display usage
usage() {
    echo "Usage: $0 <user_story>"
    echo "Example: $0 \"Implement player ship movement with Newtonian physics\""
    exit 1
}

# Check if user story is provided
USER_STORY="$1"
if [ -z "$USER_STORY" ]; then
    usage
fi

echo "========================================"
echo "Wing Commander Saga to Godot Migration Workflow"
echo "========================================"

echo ""
echo "--- Phase 1: Planning ---"
echo "Creating implementation plan for: $USER_STORY"
qwen -p "/workflow:plan $USER_STORY - IMPORTANT: Output ONLY valid JSON format as an array of task objects with fields: id, title, dependencies, files_to_modify. No markdown, no explanations, just JSON." > plan.json
uv run python parse_plan.py plan.json  # Helper to create task files

# Get the list of task IDs to process
TASK_IDS=$(grep -o 'TASK-[0-9]*' PROJECT_STATUS.md | head -n 5)  # Limit to first 5 tasks for demo

echo ""
echo "Processing tasks: $TASK_IDS"

for TASK_ID in $TASK_IDS; do
    echo ""
    echo "========================================"
    echo "Processing Task: $TASK_ID"
    echo "========================================"
    
    MAX_ATTEMPTS=3
    for ((i=1; i<=MAX_ATTEMPTS; i++)); do
        echo ""
        echo "--- Phase 2: Implementation (Attempt $i) ---"
        qwen -p "/workflow:implement $TASK_ID"
        
        echo ""
        echo "--- Phase 3: Validation ---"
        if qwen -p "/workflow:validate $TASK_ID"; then
            echo "✅ Validation successful for $TASK_ID"
            break  # Exit the loop on success
        else
            echo "❌ Validation failed for $TASK_ID. Logging feedback for remediation."
            # Append the failure log to the task's feedback section
            LOG_FILE=".qwen_workflow/logs/${TASK_ID}-failure.log"
            if [ -f "$LOG_FILE" ]; then
                echo -e "\n## Feedback (Automated from Validation Failure)\n\`\`\`\n$(cat $LOG_FILE)\n\`\`\`" >> ".qwen_workflow/tasks/${TASK_ID}.md"
            fi
            
            if [ $i -eq $MAX_ATTEMPTS ]; then
                echo "🔥 Maximum attempts reached for $TASK_ID. Manual intervention required."
                exit 1
            fi
        fi
    done
done

echo ""
echo "🎉 Workflow completed successfully!"
echo "Check the task files in .qwen_workflow/tasks/ for details."
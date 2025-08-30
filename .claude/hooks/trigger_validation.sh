#!/bin/bash

# This script is triggered when sub-agents complete tasks
# It automatically invokes validation using the appropriate development toolchain

set -e

# Read the hook event data from stdin
HOOK_DATA=$(cat)

# Create log directory if it doesn't exist
mkdir -p ./.workflow/logs

# Parse agent name, task context, and toolchain commands from hook data
AGENT_NAME=$(echo "$HOOK_DATA" | grep -o '"name":"[^"]*"' | cut -d'"' -f4 2>/dev/null || echo "unknown")
TASK_CONTEXT=$(echo "$HOOK_DATA" | grep -o '"prompt":"[^"]*"' | head -1 | cut -d'"' -f4 2>/dev/null || echo "")

# Extract task ID from task context if available
TASK_ID=$(echo "$TASK_CONTEXT" | grep -o "TASK-[0-9]*" | head -1 || echo "TASK-001")

# Detect toolchain commands used in the task
TOOLCHAIN_COMMANDS=$(echo "$HOOK_DATA" | grep -E "(godot.*--headless|uv.*run|ruff.*check|gdformat|gdlint|pytest|grep)" || true)

# Log that validation is being triggered
echo "$(date): Validation triggered for agent: $AGENT_NAME, task: $TASK_ID" >> ./.workflow/logs/hook.log

# Log detected toolchain commands
if [ -n "$TOOLCHAIN_COMMANDS" ]; then
    echo "$(date): Detected toolchain commands: $TOOLCHAIN_COMMANDS" >> ./.workflow/logs/hook.log
fi

# Update project state - mark story as starting validation
# Only update if we have a valid task ID
if [ -n "$TASK_ID" ] && [ "$TASK_ID" != "TASK-001" ]; then
    ./.claude/hooks/state_update.sh update update_validation "$TASK_ID" "running" 2>/dev/null || true
fi

# Run the validation based on agent type and toolchain usage
VALIDATION_RESULT=0
case "$AGENT_NAME" in
    "gdscript-engineer")
        echo "$(date): Running GDScript validation for $TASK_ID" >> ./.workflow/logs/hook.log
        ./.claude/hooks/run_validation.sh "$TASK_ID" "gdscript" "$TOOLCHAIN_COMMANDS"
        VALIDATION_RESULT=$?
        ;;
    "cpp-code-analyst")
        echo "$(date): Running C++ validation for $TASK_ID" >> ./.workflow/logs/hook.log
        ./.claude/hooks/run_validation.sh "$TASK_ID" "cpp" "$TOOLCHAIN_COMMANDS"
        VALIDATION_RESULT=$?
        ;;
    "asset-pipeline-engineer")
        echo "$(date): Running asset pipeline validation for $TASK_ID" >> ./.workflow/logs/hook.log
        ./.claude/hooks/run_validation.sh "$TASK_ID" "assets" "$TOOLCHAIN_COMMANDS"
        VALIDATION_RESULT=$?
        ;;
    "migration-architect" | "godot_architect")
        echo "$(date): Running architectural validation for $TASK_ID" >> ./.workflow/logs/hook.log
        ./.claude/hooks/run_validation.sh "$TASK_ID" "architecture" "$TOOLCHAIN_COMMANDS"
        VALIDATION_RESULT=$?
        ;;
    *)
        echo "$(date): Running comprehensive toolchain validation for $TASK_ID" >> ./.workflow/logs/hook.log
        ./.claude/hooks/run_validation.sh "$TASK_ID" "comprehensive" "$TOOLCHAIN_COMMANDS"
        VALIDATION_RESULT=$?
        ;;
esac

echo "$(date): Validation complete for $TASK_ID" >> ./.workflow/logs/hook.log

# Update project state based on validation result
# Only update if we have a valid task ID
if [ -n "$TASK_ID" ] && [ "$TASK_ID" != "TASK-001" ]; then
    if [ $VALIDATION_RESULT -eq 0 ]; then
        ./.claude/hooks/state_update.sh update update_validation "$TASK_ID" "passed" 2>/dev/null || true
        ./.claude/hooks/state_update.sh update update_status "story" "$TASK_ID" "completed" 2>/dev/null || true
    else
        ./.claude/hooks/state_update.sh update update_validation "$TASK_ID" "failed" 2>/dev/null || true
        ./.claude/hooks/state_update.sh update update_status "story" "$TASK_ID" "failed" 2>/dev/null || true
    fi
fi
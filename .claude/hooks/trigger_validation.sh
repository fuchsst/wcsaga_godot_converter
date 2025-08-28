#!/bin/bash

# This script is triggered when sub-agents complete tasks
# It automatically invokes validation using the appropriate development toolchain

set -e

# Read the hook event data from stdin
HOOK_DATA=$(cat)

# Create log directory if it doesn't exist
mkdir -p ./.claude_workflow/logs

# Parse agent name, task context, and toolchain commands from hook data
AGENT_NAME=$(echo "$HOOK_DATA" | grep -o '"name":"[^"]*"' | cut -d'"' -f4 2>/dev/null || echo "unknown")
TASK_CONTEXT=$(echo "$HOOK_DATA" | grep -o '"prompt":"[^"]*"' | head -1 | cut -d'"' -f4 2>/dev/null || echo "")

# Extract task ID from task context if available
TASK_ID=$(echo "$TASK_CONTEXT" | grep -o "TASK-[0-9]*" | head -1 || echo "TASK-001")

# Detect toolchain commands used in the task
TOOLCHAIN_COMMANDS=$(echo "$HOOK_DATA" | grep -E "(godot.*--headless|uv.*run|ruff.*check|gdformat|gdlint|pytest|grep)" || true)

# Log that validation is being triggered
echo "$(date): Validation triggered for agent: $AGENT_NAME, task: $TASK_ID" >> ./.claude_workflow/logs/hook.log

# Log detected toolchain commands
if [ -n "$TOOLCHAIN_COMMANDS" ]; then
    echo "$(date): Detected toolchain commands: $TOOLCHAIN_COMMANDS" >> ./.claude_workflow/logs/hook.log
fi

# Run the validation based on agent type and toolchain usage
case "$AGENT_NAME" in
    "gdscript-engineer")
        echo "$(date): Running GDScript validation for $TASK_ID" >> ./.claude_workflow/logs/hook.log
        ./.claude/hooks/run_validation.sh "$TASK_ID" "gdscript" "$TOOLCHAIN_COMMANDS"
        ;;
    "cpp-code-analyst")
        echo "$(date): Running C++ validation for $TASK_ID" >> ./.claude_workflow/logs/hook.log
        ./.claude/hooks/run_validation.sh "$TASK_ID" "cpp" "$TOOLCHAIN_COMMANDS"
        ;;
    "asset-pipeline-engineer")
        echo "$(date): Running asset pipeline validation for $TASK_ID" >> ./.claude_workflow/logs/hook.log
        ./.claude/hooks/run_validation.sh "$TASK_ID" "assets" "$TOOLCHAIN_COMMANDS"
        ;;
    "migration-architect" | "godot-architect")
        echo "$(date): Running architectural validation for $TASK_ID" >> ./.claude_workflow/logs/hook.log
        ./.claude/hooks/run_validation.sh "$TASK_ID" "architecture" "$TOOLCHAIN_COMMANDS"
        ;;
    *)
        echo "$(date): Running comprehensive toolchain validation for $TASK_ID" >> ./.claude_workflow/logs/hook.log
        ./.claude/hooks/run_validation.sh "$TASK_ID" "comprehensive" "$TOOLCHAIN_COMMANDS"
        ;;
esac

echo "$(date): Validation complete for $TASK_ID" >> ./.claude_workflow/logs/hook.log
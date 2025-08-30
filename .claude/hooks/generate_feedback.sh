#!/bin/bash

# This script generates automated feedback from validation failures
# and appends it to the task's markdown file
# Enhanced with comprehensive toolchain analysis from Development_Toolchain.md

set -e

TASK_ID=$1
LOG_FILE=$2

if [ -z "$TASK_ID" ] || [ -z "$LOG_FILE" ]; then
    echo "Usage: $0 <task_id> <log_file>"
    exit 1
fi

TASK_FILE="./.workflow/tasks/${TASK_ID}.md"

# Check if task file exists
if [ ! -f "$TASK_FILE" ]; then
    echo "Task file not found: $TASK_FILE"
    exit 1
fi

# Check if log file exists
if [ ! -f "$LOG_FILE" ]; then
    echo "Log file not found: $LOG_FILE"
    exit 1
fi

echo "$(date): Generating toolchain-aware automated feedback for $TASK_ID" >> ./.workflow/logs/hook.log

# Analyze the failure type based on log file name and content
FAILURE_TYPE="unknown"
TOOLCHAIN_TYPE="unknown"
RECOMMENDATIONS=""

# Detect failure and toolchain types from log file name and content
if echo "$LOG_FILE" | grep -q "test-failure"; then
    FAILURE_TYPE="test"
elif echo "$LOG_FILE" | grep -q "build-failure"; then
    FAILURE_TYPE="build"
elif echo "$LOG_FILE" | grep -q "validation"; then
    FAILURE_TYPE="validation"
fi

# Detect toolchain type from log content
if grep -q "pytest\|python.*test\|unittest" "$LOG_FILE"; then
    TOOLCHAIN_TYPE="python"
elif grep -q "gdunit\|godot.*test\|runtest" "$LOG_FILE"; then
    TOOLCHAIN_TYPE="gdscript"
elif grep -q "godot.*--headless\|--export" "$LOG_FILE"; then
    TOOLCHAIN_TYPE="godot_build"
elif grep -q "gcc\|g++\|clang\|cmake\|make" "$LOG_FILE"; then
    TOOLCHAIN_TYPE="cpp"
elif grep -q "ruff\|gdformat\|gdlint" "$LOG_FILE"; then
    TOOLCHAIN_TYPE="linting"
fi

echo "$(date): Detected failure type: $FAILURE_TYPE, toolchain: $TOOLCHAIN_TYPE" >> ./.workflow/logs/hook.log

# Generate toolchain-specific recommendations
case "$TOOLCHAIN_TYPE" in
    "python")
        case "$FAILURE_TYPE" in
            "test")
                RECOMMENDATIONS="
### Python Test Failure Recommendations:
- Run \`uv run pytest -v\` for detailed test output
- Check for import errors or missing dependencies
- Verify test fixtures and setup/teardown methods
- Use \`uv run pytest --tb=short\` for concise traceback
- Consider running specific failed tests: \`uv run pytest path/to/test_file.py::test_name\`"
                ;;
            "validation")
                RECOMMENDATIONS="
### Python Code Quality Recommendations:
- Run \`uv run ruff check .\` to identify linting issues
- Use \`uv run ruff format .\` to auto-format code
- Check \`uv pip check\` for dependency conflicts
- Verify Python version compatibility in pyproject.toml"
                ;;
            "build")
                RECOMMENDATIONS="
### Python Build Recommendations:
- Check \`uv sync\` for dependency resolution
- Verify all required packages are in pyproject.toml
- Run \`uv run python -c \"import module_name\"\` to test imports
- Check for circular import issues"
                ;;
        esac
        ;;
    "gdscript")
        case "$FAILURE_TYPE" in
            "test")
                RECOMMENDATIONS="
### GDScript Test Failure Recommendations:
- Check for orphan node warnings in test output
- Verify scene loading and node instantiation
- Use \`await get_tree().process_frame\` for timing issues
- Check signal connections and timeout values
- Ensure proper cleanup in test teardown"
                ;;
            "validation")
                RECOMMENDATIONS="
### GDScript Code Quality Recommendations:
- Run \`uv run gdformat --check .\` for formatting issues
- Use \`uv run gdlint .\` to identify code style problems
- Follow snake_case naming conventions
- Check for proper type annotations
- Verify export variable declarations"
                ;;
        esac
        ;;
    "godot_build")
        RECOMMENDATIONS="
### Godot Build Recommendations:
- Verify export_presets.cfg configuration
- Check export templates are installed
- Use \`godot --headless --export-debug\` for debugging
- Verify all required assets are included
- Check for asset import errors in .godot/imported/"
        ;;
    "linting")
        RECOMMENDATIONS="
### Code Quality Recommendations:
- Address formatting issues with auto-formatters
- Review linting rules and adjust if necessary
- Check for unused imports and variables
- Verify proper documentation strings
- Consider suppressing specific rules if justified"
        ;;
    *)
        RECOMMENDATIONS="
### General Recommendations:
- Review the detailed error log below
- Check the Development_Toolchain.md for relevant tools
- Verify all dependencies are properly installed
- Run validation commands manually for debugging"
        ;;
esac

# Extract key errors for summary
KEY_ERRORS=""
if grep -q -i "error\|failed\|exception" "$LOG_FILE"; then
    KEY_ERRORS=$(grep -i -A1 -B1 "error\|failed\|exception" "$LOG_FILE" | head -10)
fi

# Create comprehensive feedback section in the task file
echo "" >> "$TASK_FILE"
echo "## Automated Feedback - $FAILURE_TYPE Failure ($TOOLCHAIN_TYPE toolchain)" >> "$TASK_FILE"
echo "" >> "$TASK_FILE"
echo "**Timestamp:** $(date)" >> "$TASK_FILE"
echo "**Failure Type:** $FAILURE_TYPE" >> "$TASK_FILE"
echo "**Toolchain:** $TOOLCHAIN_TYPE" >> "$TASK_FILE"
echo "" >> "$TASK_FILE"

if [ -n "$KEY_ERRORS" ]; then
    echo "### Key Errors Detected:" >> "$TASK_FILE"
    echo "\`\`\`" >> "$TASK_FILE"
    echo "$KEY_ERRORS" >> "$TASK_FILE"
    echo "\`\`\`" >> "$TASK_FILE"
    echo "" >> "$TASK_FILE"
fi

echo "$RECOMMENDATIONS" >> "$TASK_FILE"
echo "" >> "$TASK_FILE"

echo "### Full Validation Log:" >> "$TASK_FILE"
echo "" >> "$TASK_FILE"
echo "<details>" >> "$TASK_FILE"
echo "<summary>Click to expand full log</summary>" >> "$TASK_FILE"
echo "" >> "$TASK_FILE"
echo "\`\`\`" >> "$TASK_FILE"
cat "$LOG_FILE" >> "$TASK_FILE"
echo "\`\`\`" >> "$TASK_FILE"
echo "" >> "$TASK_FILE"
echo "</details>" >> "$TASK_FILE"
echo "" >> "$TASK_FILE"

echo "### Next Steps:" >> "$TASK_FILE"
echo "1. Address the issues identified above" >> "$TASK_FILE"
echo "2. Run the relevant toolchain commands to verify fixes" >> "$TASK_FILE"
echo "3. Re-run validation to ensure all checks pass" >> "$TASK_FILE"
echo "4. Update task status once validation succeeds" >> "$TASK_FILE"

echo "$(date): Toolchain-aware automated feedback generated for $TASK_ID" >> ./.workflow/logs/hook.log

# Update task status to indicate intervention needed
echo "$(date): Task $TASK_ID requires attention due to $FAILURE_TYPE failures in $TOOLCHAIN_TYPE toolchain" >> ./.workflow/logs/hook.log
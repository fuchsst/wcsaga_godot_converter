#!/bin/bash

# Comprehensive validation script using the full development toolchain
# Based on concepts/Development_Toolchain.md specifications

set -e

TASK_ID=$1
VALIDATION_TYPE=${2:-"comprehensive"}
TOOLCHAIN_COMMANDS=$3
LOG_FILE="./.claude_workflow/logs/${TASK_ID}-validation.log"

# Create log directory if it doesn't exist
mkdir -p ./.claude_workflow/logs

echo "Running $VALIDATION_TYPE validation for task: $TASK_ID" > "$LOG_FILE"
echo "Timestamp: $(date)" >> "$LOG_FILE"
echo "Toolchain commands detected: $TOOLCHAIN_COMMANDS" >> "$LOG_FILE"
echo "==================================================" >> "$LOG_FILE"

VALIDATION_FAILED=0

# Function to run toolchain command with proper error handling
run_toolchain_command() {
    local command_name=$1
    local command=$2
    local description=$3
    
    echo "" >> "$LOG_FILE"
    echo "=== $description ===" >> "$LOG_FILE"
    
    if command -v $command_name &> /dev/null; then
        echo "Running: $command" >> "$LOG_FILE"
        if eval "$command" >> "$LOG_FILE" 2>&1; then
            echo "✓ $description successful" >> "$LOG_FILE"
            return 0
        else
            echo "✗ $description failed" >> "$LOG_FILE"
            return 1
        fi
    else
        echo "⚠ $command_name not available, skipping $description" >> "$LOG_FILE"
        return 2
    fi
}

case "$VALIDATION_TYPE" in
    "gdscript")
        echo "Running comprehensive GDScript validation..." >> "$LOG_FILE"
        
        # GDScript formatting check with uv run
        run_toolchain_command "gdformat" "uv run gdformat --check ." "GDScript formatting check"
        [ $? -eq 1 ] && VALIDATION_FAILED=1
        
        # GDScript linting
        run_toolchain_command "gdlint" "uv run gdlint ." "GDScript linting"
        [ $? -eq 1 ] && VALIDATION_FAILED=1
        
        # Check for FIXME/TODO comments using grep
        echo "" >> "$LOG_FILE"
        echo "=== Checking for FIXME/TODO comments in GDScript files ===" >> "$LOG_FILE"
        if find . -name "*.gd" -type f -exec grep -l "FIXME\|TODO" {} \; > /dev/null 2>&1; then
            echo "⚠ FIXME/TODO comments found in GDScript files:" >> "$LOG_FILE"
            find . -name "*.gd" -type f -exec grep -l "FIXME\|TODO" {} \; >> "$LOG_FILE"
            echo "" >> "$LOG_FILE"
            echo "Detailed comments:" >> "$LOG_FILE"
            find . -name "*.gd" -type f -exec grep -n "FIXME\|TODO" {} \; >> "$LOG_FILE"
        else
            echo "✓ No FIXME/TODO comments found in GDScript files" >> "$LOG_FILE"
        fi
        
        # Check for Godot headless export capability
        echo "" >> "$LOG_FILE"
        echo "=== Checking Godot headless export capability ===" >> "$LOG_FILE"
        if command -v godot &> /dev/null; then
            echo "Godot engine available" >> "$LOG_FILE"
            if godot --help | grep -q "headless"; then
                echo "✓ Godot headless mode supported" >> "$LOG_FILE"
            else
                echo "⚠ Godot headless mode not available" >> "$LOG_FILE"
            fi
        else
            echo "⚠ Godot engine not available" >> "$LOG_FILE"
        fi
        ;;
        
    "cpp")
        echo "Running C++ validation..." >> "$LOG_FILE"
        
        # C++ compilation check (placeholder for actual C++ toolchain)
        echo "C++ validation would run clang-tidy, clang-format, and build tests here" >> "$LOG_FILE"
        echo "⚠ C++ toolchain not fully configured" >> "$LOG_FILE"
        ;;
        
    "python")
        echo "Running Python validation..." >> "$LOG_FILE"
        
        # Python formatting check with ruff
        run_toolchain_command "ruff" "uv run ruff format --check ." "Python formatting check"
        [ $? -eq 1 ] && VALIDATION_FAILED=1
        
        # Python linting
        run_toolchain_command "ruff" "uv run ruff check ." "Python linting"
        [ $? -eq 1 ] && VALIDATION_FAILED=1
        
        # Python tests with pytest
        run_toolchain_command "pytest" "uv run pytest" "Python unit tests"
        [ $? -eq 1 ] && VALIDATION_FAILED=1
        
        # Check Python dependencies
        echo "" >> "$LOG_FILE"
        echo "=== Checking Python dependencies ===" >> "$LOG_FILE"
        if [ -f "requirements.txt" ]; then
            echo "requirements.txt found, checking dependency consistency" >> "$LOG_FILE"
            if uv pip check >> "$LOG_FILE" 2>&1; then
                echo "✓ Python dependencies are consistent" >> "$LOG_FILE"
            else
                echo "✗ Python dependency issues found" >> "$LOG_FILE"
                VALIDATION_FAILED=1
            fi
        else
            echo "⚠ No requirements.txt found" >> "$LOG_FILE"
        fi
        ;;
        
    "assets")
        echo "Running asset pipeline validation..." >> "$LOG_FILE"
        
        # Check if Godot can import assets
        echo "Checking asset import capability..." >> "$LOG_FILE"
        if command -v godot &> /dev/null; then
            echo "Godot available for asset validation" >> "$LOG_FILE"
            # This would run actual asset validation in a real implementation
            echo "⚠ Asset validation not fully implemented" >> "$LOG_FILE"
        else
            echo "⚠ Godot not available for asset validation" >> "$LOG_FILE"
        fi
        ;;
        
    "architecture")
        echo "Running architectural validation..." >> "$LOG_FILE"
        
        # Check project structure consistency
        echo "Checking project structure..." >> "$LOG_FILE"
        if [ -f "project.godot" ]; then
            echo "✓ project.godot found" >> "$LOG_FILE"
        else
            echo "✗ project.godot not found" >> "$LOG_FILE"
            VALIDATION_FAILED=1
        fi
        
        # Check for export presets
        if [ -f "export_presets.cfg" ]; then
            echo "✓ export_presets.cfg found" >> "$LOG_FILE"
        else
            echo "⚠ export_presets.cfg not found (needed for builds)" >> "$LOG_FILE"
        fi
        ;;
        
    "comprehensive" | *)
        echo "Running comprehensive toolchain validation..." >> "$LOG_FILE"
        
        # Run all validation types
        ./.claude/hooks/run_validation.sh "$TASK_ID" "gdscript" "$TOOLCHAIN_COMMANDS"
        gdscript_result=$?
        
        ./.claude/hooks/run_validation.sh "$TASK_ID" "python" "$TOOLCHAIN_COMMANDS"
        python_result=$?
        
        ./.claude/hooks/run_validation.sh "$TASK_ID" "architecture" "$TOOLCHAIN_COMMANDS"
        arch_result=$?
        
        if [ $gdscript_result -eq 1 ] || [ $python_result -eq 1 ] || [ $arch_result -eq 1 ]; then
            VALIDATION_FAILED=1
        fi
        ;;
esac

echo "" >> "$LOG_FILE"
echo "==================================" >> "$LOG_FILE"
if [ $VALIDATION_FAILED -eq 0 ]; then
    echo "✓ Validation completed successfully" >> "$LOG_FILE"
    exit 0
else
    echo "✗ Validation failed with errors" >> "$LOG_FILE"
    # Generate automated feedback
    ./.claude/hooks/generate_feedback.sh "$TASK_ID" "$LOG_FILE"
    exit 1
fi
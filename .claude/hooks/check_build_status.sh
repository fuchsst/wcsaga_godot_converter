#!/bin/bash

# This script checks build status and generates automated feedback
# It is triggered by a PostToolUse hook when build commands are executed
# Enhanced with comprehensive toolchain analysis from Development_Toolchain.md

set -e

# Create log directory if it doesn't exist
mkdir -p ./.workflow/logs

echo "$(date): Build status check triggered" >> ./.workflow/logs/hook.log

# Check the exit code of the last command
LAST_EXIT_CODE=$?

# Read hook data to understand what command was executed
HOOK_DATA=$(cat)
COMMAND_EXECUTED=$(echo "$HOOK_DATA" | grep -o '"command":"[^"]*"' | cut -d'"' -f4 2>/dev/null || echo "unknown")

# Detect toolchain type from command
TOOLCHAIN_TYPE="unknown"
if echo "$COMMAND_EXECUTED" | grep -q "godot.*--headless\|--export"; then
    TOOLCHAIN_TYPE="godot_build"
elif echo "$COMMAND_EXECUTED" | grep -q "uv.*run\|pip.*install\|pip.*sync"; then
    TOOLCHAIN_TYPE="python_build"
elif echo "$COMMAND_EXECUTED" | grep -q "make\|cmake\|gcc\|g++\|clang"; then
    TOOLCHAIN_TYPE="cpp_build"
fi

echo "$(date): Command executed: $COMMAND_EXECUTED, Exit code: $LAST_EXIT_CODE, Toolchain: $TOOLCHAIN_TYPE" >> ./.workflow/logs/hook.log

if [ $LAST_EXIT_CODE -eq 0 ]; then
    echo "$(date): Build command successful" >> ./.workflow/logs/hook.log
    
    # Enhanced warning detection using grep with toolchain-specific patterns
    echo "$(date): Performing comprehensive build output analysis" >> ./.workflow/logs/hook.log
    
    # Check for warnings using toolchain-specific patterns
    WARNING_PATTERNS="warning\|deprecated\|obsolete\|legacy\|experimental"
    if echo "$HOOK_DATA" | grep -i "$WARNING_PATTERNS" > /dev/null; then
        echo "$(date): Warnings found in build output" >> ./.workflow/logs/hook.log
        
        # Extract warnings with context for better analysis
        WARNINGS=$(echo "$HOOK_DATA" | grep -i -A2 -B2 "$WARNING_PATTERNS")
        echo "Warnings detected during build:" >> ./.workflow/logs/hook.log
        echo "$WARNINGS" >> ./.workflow/logs/hook.log
        
        # Toolchain-specific warning analysis
        case "$TOOLCHAIN_TYPE" in
            "godot_build")
                echo "Godot build warnings analysis:" >> ./.workflow/logs/hook.log
                # Check for asset import warnings
                if echo "$HOOK_DATA" | grep -i "texture\|mesh\|import\|asset" | grep -i "warning" > /dev/null; then
                    echo "⚠ Asset-related warnings detected" >> ./.workflow/logs/hook.log
                fi
                ;;
            "python_build")
                echo "Python build warnings analysis:" >> ./.workflow/logs/hook.log
                # Check for dependency warnings
                if echo "$HOOK_DATA" | grep -i "dependency\|version\|requirement" | grep -i "warning" > /dev/null; then
                    echo "⚠ Dependency-related warnings detected" >> ./.workflow/logs/hook.log
                fi
                ;;
        esac
    else
        echo "$(date): No warnings found in build output" >> ./.workflow/logs/hook.log
    fi
    
    # Check for successful build artifacts based on toolchain
    echo "$(date): Checking for build artifacts" >> ./.workflow/logs/hook.log
    case "$TOOLCHAIN_TYPE" in
        "godot_build")
            # Check for Godot export artifacts
            if echo "$COMMAND_EXECUTED" | grep -q "--export" && find . -name "*.exe" -o -name "*.x86_64" -o -name "*.app" -o -path "*/web/*" | head -1 > /dev/null; then
                echo "✓ Godot export artifacts found" >> ./.workflow/logs/hook.log
            fi
            ;;
        "python_build")
            # Check for Python package artifacts
            if find . -name "*.whl" -o -name "*.tar.gz" -o -name "dist" -type d | head -1 > /dev/null; then
                echo "✓ Python build artifacts found" >> ./.workflow/logs/hook.log
            fi
            ;;
    esac
    
else
    echo "$(date): Build command failed with exit code $LAST_EXIT_CODE" >> ./.workflow/logs/hook.log
    
    # Try to identify the current task context
    CURRENT_TASK=$(ls -t ./.workflow/tasks/*.md 2>/dev/null | head -1 | xargs basename -s .md 2>/dev/null || echo "TASK-001")
    
    # Generate failure log
    FAILURE_LOG="./.workflow/logs/${CURRENT_TASK}-build-failure.log"
    echo "Build failed at $(date)" > "$FAILURE_LOG"
    echo "Command: $COMMAND_EXECUTED" >> "$FAILURE_LOG"
    echo "Exit code: $LAST_EXIT_CODE" >> "$FAILURE_LOG"
    echo "Toolchain type: $TOOLCHAIN_TYPE" >> "$FAILURE_LOG"
    echo "" >> "$FAILURE_LOG"
    
    # Enhanced error extraction with toolchain-specific patterns
    echo "Error analysis:" >> "$FAILURE_LOG"
    
    # Extract errors with context
    ERRORS=$(echo "$HOOK_DATA" | grep -i -A3 -B1 "error\|failed\|exception\|traceback\|syntax" || true)
    if [ -n "$ERRORS" ]; then
        echo "Errors found in build output:" >> "$FAILURE_LOG"
        echo "$ERRORS" >> "$FAILURE_LOG"
        echo "" >> "$FAILURE_LOG"
    fi
    
    # Toolchain-specific error analysis
    case "$TOOLCHAIN_TYPE" in
        "godot_build")
            echo "Godot-specific error analysis:" >> "$FAILURE_LOG"
            # Check for common Godot build errors
            if echo "$HOOK_DATA" | grep -i "export\|preset\|template" | grep -i "error" > /dev/null; then
                echo "• Export configuration error detected" >> "$FAILURE_LOG"
            fi
            if echo "$HOOK_DATA" | grep -i "asset\|texture\|import" | grep -i "error" > /dev/null; then
                echo "• Asset import error detected" >> "$FAILURE_LOG"
            fi
            ;;
        "python_build")
            echo "Python-specific error analysis:" >> "$FAILURE_LOG"
            # Check for common Python build errors
            if echo "$HOOK_DATA" | grep -i "dependency\|module\|import" | grep -i "error" > /dev/null; then
                echo "• Dependency error detected" >> "$FAILURE_LOG"
            fi
            if echo "$HOOK_DATA" | grep -i "syntax\|indent" | grep -i "error" > /dev/null; then
                echo "• Syntax error detected" >> "$FAILURE_LOG"
            fi
            ;;
    esac
    
    echo "" >> "$FAILURE_LOG"
    echo "Check the command output above for specific error details." >> "$FAILURE_LOG"
    
    # Generate automated feedback
    ./.claude/hooks/generate_feedback.sh "$CURRENT_TASK" "$FAILURE_LOG"
    
    echo "$(date): Automated feedback generated for build failure" >> ./.workflow/logs/hook.log
fi
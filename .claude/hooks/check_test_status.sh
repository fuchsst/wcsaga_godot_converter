#!/bin/bash

# This script checks test status and generates automated feedback
# It is triggered by a PostToolUse hook when test commands are executed
# Enhanced with comprehensive testing toolchain analysis from Development_Toolchain.md

set -e

# Create log directory if it doesn't exist
mkdir -p ./.workflow/logs

echo "$(date): Test status check triggered" >> ./.workflow/logs/hook.log

# Check the exit code of the last command
LAST_EXIT_CODE=$?

# Read hook data to understand what command was executed
HOOK_DATA=$(cat)
COMMAND_EXECUTED=$(echo "$HOOK_DATA" | grep -o '"command":"[^"]*"' | cut -d'"' -f4 2>/dev/null || echo "unknown")

# Detect testing framework from command
TEST_FRAMEWORK="unknown"
if echo "$COMMAND_EXECUTED" | grep -q "pytest\|uv run pytest"; then
    TEST_FRAMEWORK="pytest"
elif echo "$COMMAND_EXECUTED" | grep -q "gdunit\|runtest\|godot.*test"; then
    TEST_FRAMEWORK="gdunit4"
elif echo "$COMMAND_EXECUTED" | grep -q "unittest\|python.*test"; then
    TEST_FRAMEWORK="unittest"
fi

echo "$(date): Test command executed: $COMMAND_EXECUTED, Exit code: $LAST_EXIT_CODE, Framework: $TEST_FRAMEWORK" >> ./.workflow/logs/hook.log

if [ $LAST_EXIT_CODE -eq 0 ]; then
    echo "$(date): Test command successful" >> ./.workflow/logs/hook.log
    
    # Comprehensive test output analysis using grep with framework-specific patterns
    echo "$(date): Performing comprehensive test output analysis" >> ./.workflow/logs/hook.log
    
    # Check for warnings, skipped tests, or other issues
    TEST_ISSUE_PATTERNS="warning\|skip\|xfail\|slow\|performance\|deprecated"
    if echo "$HOOK_DATA" | grep -i "$TEST_ISSUE_PATTERNS" > /dev/null; then
        echo "$(date): Test issues found in output" >> ./.workflow/logs/hook.log
        
        # Extract issues with context for better analysis
        ISSUES=$(echo "$HOOK_DATA" | grep -i -A2 -B1 "$TEST_ISSUE_PATTERNS")
        echo "Test issues detected:" >> ./.workflow/logs/hook.log
        echo "$ISSUES" >> ./.workflow/logs/hook.log
        
        # Framework-specific issue analysis
        case "$TEST_FRAMEWORK" in
            "pytest")
                echo "Pytest-specific analysis:" >> ./.workflow/logs/hook.log
                # Check for common pytest issues
                if echo "$HOOK_DATA" | grep -i "skip" > /dev/null; then
                    echo "⚠ Skipped tests detected" >> ./.workflow/logs/hook.log
                fi
                if echo "$HOOK_DATA" | grep -i "xfail" > /dev/null; then
                    echo "⚠ Expected failures detected" >> ./.workflow/logs/hook.log
                fi
                if echo "$HOOK_DATA" | grep -i "slow" > /dev/null; then
                    echo "⚠ Slow tests detected" >> ./.workflow/logs/hook.log
                fi
                ;;
            "gdunit4")
                echo "GdUnit4-specific analysis:" >> ./.workflow/logs/hook.log
                # Check for common gdunit4 issues
                if echo "$HOOK_DATA" | grep -i "orphan\|leak" > /dev/null; then
                    echo "⚠ Orphan node warnings detected" >> ./.workflow/logs/hook.log
                fi
                ;;
        esac
    else
        echo "$(date): No test issues found in output" >> ./.workflow/logs/hook.log
    fi
    
    # Check test coverage and results metrics
    echo "$(date): Analyzing test results metrics" >> ./.workflow/logs/hook.log
    
    # Extract test statistics using grep
    if echo "$HOOK_DATA" | grep -E "[0-9]+ passed\|[0-9]+ failed\|[0-9]+ skipped" > /dev/null; then
        TEST_STATS=$(echo "$HOOK_DATA" | grep -E "[0-9]+ passed\|[0-9]+ failed\|[0-9]+ skipped" | head -1)
        echo "Test statistics: $TEST_STATS" >> ./.workflow/logs/hook.log
    fi
    
    # Check for coverage reports
    if echo "$HOOK_DATA" | grep -i "coverage\|%" > /dev/null; then
        COVERAGE_INFO=$(echo "$HOOK_DATA" | grep -i "coverage\|%" | head -2)
        echo "Coverage information:" >> ./.workflow/logs/hook.log
        echo "$COVERAGE_INFO" >> ./.workflow/logs/hook.log
    fi
    
else
    echo "$(date): Test command failed with exit code $LAST_EXIT_CODE" >> ./.workflow/logs/hook.log
    
    # Try to identify the current task context
    CURRENT_TASK=$(ls -t ./.workflow/tasks/*.md 2>/dev/null | head -1 | xargs basename -s .md 2>/dev/null || echo "TASK-001")
    
    # Generate failure log
    FAILURE_LOG="./.workflow/logs/${CURRENT_TASK}-test-failure.log"
    echo "Tests failed at $(date)" > "$FAILURE_LOG"
    echo "Command: $COMMAND_EXECUTED" >> "$FAILURE_LOG"
    echo "Exit code: $LAST_EXIT_CODE" >> "$FAILURE_LOG"
    echo "Test framework: $TEST_FRAMEWORK" >> "$FAILURE_LOG"
    echo "" >> "$FAILURE_LOG"
    
    # Enhanced error extraction with framework-specific patterns
    echo "Test failure analysis:" >> "$FAILURE_LOG"
    
    # Extract errors with context
    ERRORS=$(echo "$HOOK_DATA" | grep -i -A3 -B1 "error\|failed\|exception\|traceback\|assertion\|timeout" || true)
    if [ -n "$ERRORS" ]; then
        echo "Errors found in test output:" >> "$FAILURE_LOG"
        echo "$ERRORS" >> "$FAILURE_LOG"
        echo "" >> "$FAILURE_LOG"
    fi
    
    # Framework-specific error analysis
    case "$TEST_FRAMEWORK" in
        "pytest")
            echo "Pytest-specific error analysis:" >> "$FAILURE_LOG"
            # Check for common pytest failure patterns
            if echo "$HOOK_DATA" | grep -i "assertion" | grep -i "error\|failed" > /dev/null; then
                echo "• Assertion failures detected" >> "$FAILURE_LOG"
            fi
            if echo "$HOOK_DATA" | grep -i "fixture\|setup" | grep -i "error" > /dev/null; then
                echo "• Test fixture errors detected" >> "$FAILURE_LOG"
            fi
            if echo "$HOOK_DATA" | grep -i "import\|module" | grep -i "error" > /dev/null; then
                echo "• Import errors detected" >> "$FAILURE_LOG"
            fi
            ;;
        "gdunit4")
            echo "GdUnit4-specific error analysis:" >> "$FAILURE_LOG"
            # Check for common gdunit4 failure patterns
            if echo "$HOOK_DATA" | grep -i "scene\|node" | grep -i "error" > /dev/null; then
                echo "• Scene/node related errors detected" >> "$FAILURE_LOG"
            fi
            if echo "$HOOK_DATA" | grep -i "signal\|timeout" | grep -i "error" > /dev/null; then
                echo "• Signal/timeout errors detected" >> "$FAILURE_LOG"
            fi
            ;;
    esac
    
    # Try to capture detailed test output from various sources
    echo "" >> "$FAILURE_LOG"
    echo "Detailed test output analysis:" >> "$FAILURE_LOG"
    
    # Check for various test output files
    if [ -f "pytest.log" ]; then
        echo "Recent pytest output:" >> "$FAILURE_LOG"
        tail -30 "pytest.log" >> "$FAILURE_LOG"
        
        # Extract specific error information
        if grep -i -A5 -B2 "error\|failed\|exception" "pytest.log" > /dev/null; then
            echo "" >> "$FAILURE_LOG"
            echo "Detailed error context:" >> "$FAILURE_LOG"
            grep -i -A5 -B2 "error\|failed\|exception" "pytest.log" | head -20 >> "$FAILURE_LOG"
        fi
    elif [ -f "test.log" ]; then
        echo "Recent test output:" >> "$FAILURE_LOG"
        tail -30 "test.log" >> "$FAILURE_LOG"
    elif [ -f ".pytest_cache/v/cache/lastfailed" ]; then
        echo "Last failed tests:" >> "$FAILURE_LOG"
        cat ".pytest_cache/v/cache/lastfailed" >> "$FAILURE_LOG"
    else
        echo "No detailed test output files available." >> "$FAILURE_LOG"
        echo "Check the command output above for specific error details." >> "$FAILURE_LOG"
    fi
    
    # Generate automated feedback
    ./.claude/hooks/generate_feedback.sh "$CURRENT_TASK" "$FAILURE_LOG"
    
    echo "$(date): Automated feedback generated for test failure" >> ./.workflow/logs/hook.log
fi
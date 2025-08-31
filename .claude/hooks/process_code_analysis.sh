#!/bin/bash

# This script is triggered when the C++ Code Analyst sub-agent completes a task
# It processes the code analysis report and materializes it into individual task files
# Enhanced with comprehensive toolchain integration from Development_Toolchain.md

set -e

# Read the hook event data from stdin
HOOK_DATA=$(cat)

# Create log and task directories if they don't exist
mkdir -p ./.workflow/logs
mkdir -p ./.workflow/tasks/ANALYSIS

# Log that code analysis processing is being triggered
echo "$(date): Code analysis processing triggered with comprehensive toolchain integration" >> ./.workflow/logs/hook.log

# Comprehensive code analysis toolchain check
check_analysis_toolchain() {
    echo "$(date): Checking code analysis toolchain availability" >> ./.workflow/logs/hook.log
    
    local tools_available=0
    
    # Python analysis tools
    if command -v ruff &> /dev/null; then
        echo "$(date): ✓ ruff is available for Python code analysis" >> ./.workflow/logs/hook.log
        tools_available=$((tools_available + 1))
    else
        echo "$(date): ⚠ ruff is not available for Python code analysis" >> ./.workflow/logs/hook.log
    fi
    
    # GDScript analysis tools
    if command -v gdlint &> /dev/null; then
        echo "$(date): ✓ gdlint is available for GDScript code analysis" >> ./.workflow/logs/hook.log
        tools_available=$((tools_available + 1))
    else
        echo "$(date): ⚠ gdlint is not available for GDScript code analysis" >> ./.workflow/logs/hook.log
    fi
    
    if command -v gdformat &> /dev/null; then
        echo "$(date): ✓ gdformat is available for GDScript formatting analysis" >> ./.workflow/logs/hook.log
        tools_available=$((tools_available + 1))
    else
        echo "$(date): ⚠ gdformat is not available for GDScript formatting analysis" >> ./.workflow/logs/hook.log
    fi
    
    # Python environment
    if command -v uv &> /dev/null; then
        echo "$(date): ✓ uv is available for Python environment management" >> ./.workflow/logs/hook.log
        tools_available=$((tools_available + 1))
    else
        echo "$(date): ⚠ uv is not available, using system Python" >> ./.workflow/logs/hook.log
    fi
    
    # Generic analysis tools
    if command -v grep &> /dev/null; then
        echo "$(date): ✓ grep is available for pattern-based analysis" >> ./.workflow/logs/hook.log
        tools_available=$((tools_available + 1))
    fi
    
    echo "$(date): Analysis toolchain summary: $tools_available tools available" >> ./.workflow/logs/hook.log
    return $tools_available
}

# Extract and categorize code analysis findings
analyze_code_report() {
    local hook_data=$1
    
    echo "$(date): Performing comprehensive code analysis report parsing" >> ./.workflow/logs/hook.log
    
    # Look for different types of issues using sophisticated grep patterns
    local severity_high=""
    local severity_medium=""
    local severity_low=""
    
    # High severity issues
    if echo "$hook_data" | grep -iE "error|critical|security|vulnerability|segfault|crash|leak" > /dev/null; then
        severity_high=$(echo "$hook_data" | grep -iE "error|critical|security|vulnerability|segfault|crash|leak")
        echo "$(date): High severity issues found" >> ./.workflow/logs/hook.log
    fi
    
    # Medium severity issues
    if echo "$hook_data" | grep -iE "warning|deprecated|performance|inefficient|todo|fixme" > /dev/null; then
        severity_medium=$(echo "$hook_data" | grep -iE "warning|deprecated|performance|inefficient|todo|fixme")
        echo "$(date): Medium severity issues found" >> ./.workflow/logs/hook.log
    fi
    
    # Low severity issues
    if echo "$hook_data" | grep -iE "style|format|convention|naming|comment" > /dev/null; then
        severity_low=$(echo "$hook_data" | grep -iE "style|format|convention|naming|comment")
        echo "$(date): Low severity issues found" >> ./.workflow/logs/hook.log
    fi
    
    # Create analysis summary
    local analysis_summary=""
    if [ -n "$severity_high" ]; then
        analysis_summary="${analysis_summary}High Priority Issues:\n$severity_high\n\n"
    fi
    if [ -n "$severity_medium" ]; then
        analysis_summary="${analysis_summary}Medium Priority Issues:\n$severity_medium\n\n"
    fi
    if [ -n "$severity_low" ]; then
        analysis_summary="${analysis_summary}Low Priority Issues:\n$severity_low\n\n"
    fi
    
    if [ -n "$analysis_summary" ]; then
        echo -e "$analysis_summary" >> ./.workflow/logs/hook.log
        return 0
    else
        echo "$(date): No categorizable issues found in code analysis report" >> ./.workflow/logs/hook.log
        return 1
    fi
}

# Run toolchain-specific code analysis
run_toolchain_analysis() {
    echo "$(date): Running toolchain-specific code analysis" >> ./.workflow/logs/hook.log
    
    # Python analysis
    if command -v ruff &> /dev/null; then
        echo "$(date): Running ruff analysis on Python files" >> ./.workflow/logs/hook.log
        if find . -name "*.py" -type f | head -1 > /dev/null; then
            if command -v uv &> /dev/null; then
                uv run ruff check . --output-format=text >> ./.workflow/logs/hook.log 2>&1 || true
            else
                ruff check . --output-format=text >> ./.workflow/logs/hook.log 2>&1 || true
            fi
        fi
    fi
    
    # GDScript analysis
    if command -v gdlint &> /dev/null; then
        echo "$(date): Running gdlint analysis on GDScript files" >> ./.workflow/logs/hook.log
        if find . -name "*.gd" -type f | head -1 > /dev/null; then
            if command -v uv &> /dev/null; then
                uv run gdlint . >> ./.workflow/logs/hook.log 2>&1 || true
            else
                gdlint . >> ./.workflow/logs/hook.log 2>&1 || true
            fi
        fi
    fi
    
    # C++ analysis (if available)
    if command -v clang-tidy &> /dev/null; then
        echo "$(date): C++ analysis tools available" >> ./.workflow/logs/hook.log
        if find . -name "*.cpp" -o -name "*.h" | head -1 > /dev/null; then
            echo "$(date): C++ files found - would run clang-tidy analysis" >> ./.workflow/logs/hook.log
        fi
    fi
}

# Create code analysis tasks from findings
create_analysis_tasks() {
    local findings_file=$1
    
    echo "$(date): Creating code analysis tasks from findings" >> ./.workflow/logs/hook.log
    
    local task_count=1
    
    # Create high priority tasks
    if grep -q "High Priority Issues" "$findings_file"; then
        local task_id="ANALYSIS-$(printf "%03d" $task_count)"
        cat > "./.workflow/tasks/ANALYSIS/${task_id}.md" << EOF
---
id: $task_id
title: Fix High Priority Code Analysis Issues
status: pending
dependencies: []
assignee: cpp-code-analyst
priority: high
---

# Task: Fix High Priority Code Analysis Issues

## Description
Address critical code quality issues identified by static analysis tools. These issues may include security vulnerabilities, errors, or performance problems.

## Acceptance Criteria
- [ ] All high priority issues resolved
- [ ] Code passes toolchain validation: \`uv run ruff check .\` (Python)
- [ ] Code passes toolchain validation: \`uv run gdlint .\` (GDScript)
- [ ] No regression in existing functionality
- [ ] Documentation updated where necessary

## Implementation Notes
Use the following toolchain commands for validation:
- \`uv run ruff check --fix .\` for Python auto-fixes
- \`uv run gdformat .\` for GDScript auto-formatting
- \`grep -r "TODO\|FIXME" .\` to find remaining issues

## Feedback
EOF
        echo "$(date): Created high priority analysis task: ${task_id}.md" >> ./.workflow/logs/hook.log
        task_count=$((task_count + 1))
    fi
    
    # Create medium priority tasks
    if grep -q "Medium Priority Issues" "$findings_file"; then
        local task_id="ANALYSIS-$(printf "%03d" $task_count)"
        cat > "./.workflow/tasks/ANALYSIS/${task_id}.md" << EOF
---
id: $task_id
title: Address Medium Priority Code Analysis Issues
status: pending
dependencies: []
assignee: cpp-code-analyst
priority: medium
---

# Task: Address Medium Priority Code Analysis Issues

## Description
Resolve warnings and performance issues identified by code analysis tools.

## Acceptance Criteria
- [ ] Medium priority warnings addressed
- [ ] Code quality metrics improved
- [ ] Toolchain validation passes
- [ ] Performance issues resolved where applicable

## Implementation Notes
Focus on improving code maintainability and following best practices.

## Feedback
EOF
        echo "$(date): Created medium priority analysis task: ${task_id}.md" >> ./.workflow/logs/hook.log
        task_count=$((task_count + 1))
    fi
}

# Main analysis workflow
check_analysis_toolchain

# Extract and analyze the code analysis report
ANALYSIS_REPORT_FILE="./.workflow/temp_analysis_report.txt"
echo "$HOOK_DATA" > "$ANALYSIS_REPORT_FILE"

echo "$(date): Analyzing code analysis report for potential issues" >> ./.workflow/logs/hook.log

if analyze_code_report "$HOOK_DATA"; then
    echo "$(date): Issues found in code analysis report, creating tasks" >> ./.workflow/logs/hook.log
    
    # Extract findings to a structured file
    FINDINGS_FILE="./.workflow/temp_findings.txt"
    
    # Create findings summary
    echo "Code Analysis Findings Summary" > "$FINDINGS_FILE"
    echo "Generated: $(date)" >> "$FINDINGS_FILE"
    echo "==============================" >> "$FINDINGS_FILE"
    
    # Extract and categorize findings
    if echo "$HOOK_DATA" | grep -iE "error|critical|security|vulnerability" > /dev/null; then
        echo "" >> "$FINDINGS_FILE"
        echo "High Priority Issues:" >> "$FINDINGS_FILE"
        echo "$HOOK_DATA" | grep -iE "error|critical|security|vulnerability" >> "$FINDINGS_FILE"
    fi
    
    if echo "$HOOK_DATA" | grep -iE "warning|deprecated|performance" > /dev/null; then
        echo "" >> "$FINDINGS_FILE"
        echo "Medium Priority Issues:" >> "$FINDINGS_FILE"
        echo "$HOOK_DATA" | grep -iE "warning|deprecated|performance" >> "$FINDINGS_FILE"
    fi
    
    # Create tasks based on findings
    create_analysis_tasks "$FINDINGS_FILE"
    
    # Clean up temporary files
    rm -f "$FINDINGS_FILE"
else
    echo "$(date): No significant issues found in code analysis report" >> ./.workflow/logs/hook.log
fi

# Run additional toolchain analysis
run_toolchain_analysis

# Clean up
rm -f "$ANALYSIS_REPORT_FILE"

echo "$(date): Code analysis processing complete with toolchain integration" >> ./.workflow/logs/hook.log
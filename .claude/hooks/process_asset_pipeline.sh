#!/bin/bash

# This script is triggered when the Asset Pipeline Engineer sub-agent completes a task
# It processes the asset pipeline plan and materializes it into individual task files
# Enhanced with comprehensive toolchain integration from Development_Toolchain.md

set -e

# Read the hook event data from stdin
HOOK_DATA=$(cat)

# Create log and task directories if they don't exist
mkdir -p ./.claude_workflow/logs
mkdir -p ./.claude_workflow/tasks

# Log that asset pipeline processing is being triggered
echo "$(date): Asset pipeline processing triggered" >> ./.claude_workflow/logs/hook.log

# Comprehensive toolchain availability check
check_toolchain_availability() {
    echo "$(date): Checking asset pipeline toolchain availability" >> ./.claude_workflow/logs/hook.log
    
    # Python environment management
    if command -v uv &> /dev/null; then
        echo "$(date): ✓ uv is available for Python environment management" >> ./.claude_workflow/logs/hook.log
    else
        echo "$(date): ⚠ uv is not available, using system Python" >> ./.claude_workflow/logs/hook.log
    fi
    
    # Godot engine for asset processing
    if command -v godot &> /dev/null; then
        echo "$(date): ✓ Godot engine is available for asset processing" >> ./.claude_workflow/logs/hook.log
        
        # Check for headless mode support
        if godot --help | grep -q "headless"; then
            echo "$(date): ✓ Godot headless mode supported for automated asset processing" >> ./.claude_workflow/logs/hook.log
        else
            echo "$(date): ⚠ Godot headless mode not available" >> ./.claude_workflow/logs/hook.log
        fi
    else
        echo "$(date): ⚠ Godot engine not available for asset processing" >> ./.claude_workflow/logs/hook.log
    fi
    
    # Asset processing tools
    if command -v ruff &> /dev/null; then
        echo "$(date): ✓ ruff is available for Python asset script linting" >> ./.claude_workflow/logs/hook.log
    else
        echo "$(date): ⚠ ruff not available for Python linting" >> ./.claude_workflow/logs/hook.log
    fi
    
    # Check for common asset processing libraries
    if command -v python &> /dev/null; then
        echo "$(date): Checking Python asset processing libraries..." >> ./.claude_workflow/logs/hook.log
        
        # Check for Pillow (image processing)
        if python -c "import PIL" 2>/dev/null; then
            echo "$(date): ✓ Pillow available for image processing" >> ./.claude_workflow/logs/hook.log
        else
            echo "$(date): ⚠ Pillow not available for image processing" >> ./.claude_workflow/logs/hook.log
        fi
        
        # Check for other useful libraries
        for lib in "numpy" "json" "pathlib"; do
            if python -c "import $lib" 2>/dev/null; then
                echo "$(date): ✓ $lib available" >> ./.claude_workflow/logs/hook.log
            else
                echo "$(date): ⚠ $lib not available" >> ./.claude_workflow/logs/hook.log
            fi
        done
    fi
}

# Validate asset pipeline plan structure
validate_pipeline_plan() {
    local plan_data=$1
    local plan_file=$2
    
    echo "$(date): Validating asset pipeline plan structure" >> ./.claude_workflow/logs/hook.log
    
    # Use Python's json.tool for validation
    if echo "$plan_data" | python -m json.tool > /dev/null 2>&1; then
        echo "$(date): ✓ Asset pipeline JSON format is valid" >> ./.claude_workflow/logs/hook.log
        
        # Additional validation using grep for required fields
        if echo "$plan_data" | grep -q '"id".*"title".*"assets"'; then
            echo "$(date): ✓ Required asset pipeline fields found" >> ./.claude_workflow/logs/hook.log
            return 0
        else
            echo "$(date): ⚠ Asset pipeline plan missing required fields (id, title, assets)" >> ./.claude_workflow/logs/hook.log
            return 1
        fi
    else
        echo "$(date): ✗ Asset pipeline JSON format is invalid" >> ./.claude_workflow/logs/hook.log
        return 1
    fi
}

# Process asset pipeline with toolchain integration
process_asset_pipeline() {
    local plan_file=$1
    
    echo "$(date): Processing asset pipeline plan with toolchain integration" >> ./.claude_workflow/logs/hook.log
    
    # Use uv if available, otherwise fall back to system Python
    if command -v uv &> /dev/null; then
        echo "$(date): Using uv to run asset pipeline processor" >> ./.claude_workflow/logs/hook.log
        
        # Create asset pipeline processor if it exists
        if [ -f "./.claude/hooks/process_asset_plan.py" ]; then
            uv run python ./.claude/hooks/process_asset_plan.py "$plan_file"
        else
            echo "$(date): Asset pipeline processor script not found, creating placeholder tasks" >> ./.claude_workflow/logs/hook.log
            create_placeholder_asset_tasks "$plan_file"
        fi
    else
        echo "$(date): Using system Python for asset pipeline processing" >> ./.claude_workflow/logs/hook.log
        if [ -f "./.claude/hooks/process_asset_plan.py" ]; then
            python ./.claude/hooks/process_asset_plan.py "$plan_file"
        else
            create_placeholder_asset_tasks "$plan_file"
        fi
    fi
}

# Create placeholder asset tasks when processor doesn't exist
create_placeholder_asset_tasks() {
    local plan_file=$1
    
    echo "$(date): Creating placeholder asset pipeline tasks" >> ./.claude_workflow/logs/hook.log
    
    # Extract basic information using grep and create simple tasks
    local task_count=1
    while IFS= read -r line; do
        if echo "$line" | grep -q '"title"'; then
            local title=$(echo "$line" | grep -o '"title":"[^"]*"' | cut -d'"' -f4)
            local task_id="ASSET-$(printf "%03d" $task_count)"
            
            # Create task file
            cat > "./.claude_workflow/tasks/${task_id}.md" << EOF
---
id: $task_id
title: $title
status: pending
dependencies: []
assignee: asset-pipeline-engineer
asset_types: []
---

# Task: $title

## Description
Asset pipeline task extracted from automated plan. This task involves processing and converting assets for the Godot project following the toolchain requirements.

## Acceptance Criteria
- [ ] Assets are properly converted to Godot-compatible formats
- [ ] Asset import settings are configured correctly
- [ ] Validation passes using Godot headless mode
- [ ] No asset import errors in .godot/imported/
- [ ] Asset file sizes are optimized appropriately

## Implementation Notes
Use the following toolchain commands:
- \`godot --headless --import\` for asset validation
- \`uv run python\` for any Python-based asset processing
- Verify asset quality and compression settings

## Feedback
EOF
            
            echo "$(date): Created placeholder task: ${task_id}.md" >> ./.claude_workflow/logs/hook.log
            task_count=$((task_count + 1))
        fi
    done < "$plan_file"
}

# Run toolchain checks
check_toolchain_availability

# Try to extract asset pipeline plan from hook data
PIPELINE_PLAN=""
if echo "$HOOK_DATA" | grep -q "```json"; then
    PIPELINE_PLAN=$(echo "$HOOK_DATA" | sed -n '/```json/,/```/p' | grep -v '```')
elif echo "$HOOK_DATA" | grep -q '\[{'; then
    # Try to find JSON array directly
    PIPELINE_PLAN=$(echo "$HOOK_DATA" | grep -o '\[{.*}\]' | head -1)
fi

# Process the pipeline plan if found
if [ -n "$PIPELINE_PLAN" ]; then
    echo "$(date): Found asset pipeline plan in hook data" >> ./.claude_workflow/logs/hook.log
    
    # Save the pipeline plan to a temporary file
    TEMP_PLAN_FILE="./.claude_workflow/temp_asset_pipeline.json"
    echo "$PIPELINE_PLAN" > "$TEMP_PLAN_FILE"
    
    # Validate and process the plan
    if validate_pipeline_plan "$PIPELINE_PLAN" "$TEMP_PLAN_FILE"; then
        echo "$(date): Asset pipeline plan validation passed" >> ./.claude_workflow/logs/hook.log
        
        # Process the asset pipeline
        if process_asset_pipeline "$TEMP_PLAN_FILE"; then
            echo "$(date): Asset pipeline processing successful" >> ./.claude_workflow/logs/hook.log
        else
            echo "$(date): Asset pipeline processing failed" >> ./.claude_workflow/logs/hook.log
        fi
    else
        echo "$(date): Asset pipeline plan validation failed" >> ./.claude_workflow/logs/hook.log
    fi
    
    # Clean up temporary file
    rm -f "$TEMP_PLAN_FILE"
else
    echo "$(date): No asset pipeline plan found in hook data" >> ./.claude_workflow/logs/hook.log
    
    # Check for sample asset pipeline plan
    if [ -f "./.claude/sample_asset_pipeline.json" ]; then
        echo "$(date): Processing sample asset pipeline plan" >> ./.claude_workflow/logs/hook.log
        if validate_pipeline_plan "$(cat ./.claude/sample_asset_pipeline.json)" "./.claude/sample_asset_pipeline.json"; then
            process_asset_pipeline "./.claude/sample_asset_pipeline.json"
        fi
    else
        echo "$(date): No sample asset pipeline plan available" >> ./.claude_workflow/logs/hook.log
    fi
fi

echo "$(date): Asset pipeline processing complete" >> ./.claude_workflow/logs/hook.log
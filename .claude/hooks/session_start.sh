#!/bin/bash

# SessionStart hook - Loads project state and context at session initialization
# Integrated with existing toolchain infrastructure from Development_Toolchain.md

set -e

# Load environment variables if .env exists
if [ -f "./.env" ]; then
    set -a  # automatically export all variables
    source ./.env
    set +a  # stop auto-exporting
fi

# Create log directory if it doesn't exist
mkdir -p ./.workflow/logs

echo "$(date): SessionStart hook triggered" >> ./.workflow/logs/hook.log

# Load project state if available
if [ -f "./project_state.json" ]; then
    echo "$(date): Loading project_state.json" >> ./.workflow/logs/hook.log
    
    # Extract basic project info for context using jq
    PROJECT_NAME=$(jq -r '.project_name // "Wing Commander Saga Godot Converter"' ./project_state.json 2>/dev/null || echo "Wing Commander Saga Godot Converter")
    SCHEMA_VERSION=$(jq -r '.schema_version // "2.0.0"' ./project_state.json 2>/dev/null || echo "2.0.0")
    
    # Count active artifacts using jq
    PRD_COUNT=$(jq '.prds | length' ./project_state.json 2>/dev/null || echo 0)
    EPIC_COUNT=$(jq '.epics | length' ./project_state.json 2>/dev/null || echo 0)
    STORY_COUNT=$(jq '.stories | length' ./project_state.json 2>/dev/null || echo 0)
    
    echo "=== PROJECT STATE LOADED ==="
    echo "Date: $(date)"
    echo "Project: $PROJECT_NAME"
    echo "Schema: $SCHEMA_VERSION"
    echo "PRDs: $PRD_COUNT, Epics: $EPIC_COUNT, Stories: $STORY_COUNT"
    echo ""
    
else
    echo "$(date): No project_state.json found - will create default structure" >> ./.workflow/logs/hook.log
    echo "⚠ No project state file found. Use /prd command to start planning."
    echo ""
fi

echo "=== MAIN CONCEPT DOCUMENTS ==="
echo "@concepts/target_structure/directory_structure.md"
echo "@concepts/target_structure/module_relationships.md"
echo "@concepts/source_module_hierarchy/module_mapping_summary.md"
echo "@concepts/data_converter.md"
echo "@concepts/data_converter/source_to_target_mapping.md"
echo "@concepts/data_converter/godot_integration_mapping.md"


# Display available agents, hooks, and commands by name
echo "=== AI ORCHESTRATION SYSTEM ==="
echo "Agents:"
for agent in .claude/agents/*.md; do
    if [ -f "$agent" ]; then
        basename "$agent" .md
    fi
done | sed 's/^/  • /'
echo ""

echo "Hooks:"
for hook in .claude/hooks/*.sh; do
    if [ -f "$hook" ]; then
        basename "$hook" .sh
    fi
done | sed 's/^/  • /'
echo ""

echo "Commands:"
for command in .claude/commands/*.md; do
    if [ -f "$command" ]; then
        basename "$command" .md
    fi
done | sed 's/^/  • /'
echo ""

# Check toolchain availability
echo "$(date): Checking toolchain availability" >> ./.workflow/logs/hook.log

TOOLS_AVAILABLE=0
if command -v uv &> /dev/null; then
    echo "✓ uv available for Python environment management"
    TOOLS_AVAILABLE=$((TOOLS_AVAILABLE + 1))
else
    echo "⚠ uv not available - using system Python"
fi

# Check for Godot from environment variable or command
if [ -n "${GODOT_BIN:-}" ] && [ -x "${GODOT_BIN}" ]; then
    echo "✓ Godot engine available for asset processing (${GODOT_BIN})"
    TOOLS_AVAILABLE=$((TOOLS_AVAILABLE + 1))
elif command -v godot &> /dev/null; then
    echo "✓ Godot engine available for asset processing"
    TOOLS_AVAILABLE=$((TOOLS_AVAILABLE + 1))
else
    echo "⚠ Godot not available - asset processing limited"
fi

if command -v ruff &> /dev/null; then
    echo "✓ ruff available for Python linting/formatting"
    TOOLS_AVAILABLE=$((TOOLS_AVAILABLE + 1))
fi

if command -v gdformat &> /dev/null; then
    echo "✓ gdformat available for GDScript formatting"
    TOOLS_AVAILABLE=$((TOOLS_AVAILABLE + 1))
fi

if command -v gdlint &> /dev/null; then
    echo "✓ gdlint available for GDScript linting"
    TOOLS_AVAILABLE=$((TOOLS_AVAILABLE + 1))
fi

if command -v jq &> /dev/null; then
    echo "✓ jq available for JSON processing"
    TOOLS_AVAILABLE=$((TOOLS_AVAILABLE + 1))
else
    echo "⚠ jq not available - JSON processing limited"
fi

echo ""
echo "Toolchain: $TOOLS_AVAILABLE tools available"
echo ""

# Display recent task status if available
if [ -d "./.workflow/tasks/" ]; then
    # Find task files in subdirectories
    RECENT_TASKS=$(find ./.workflow/tasks/ -name "*.md" -type f 2>/dev/null | head -3 || true)
    if [ -n "$RECENT_TASKS" ]; then
        echo "=== RECENT TASKS ==="
        for task_file in $RECENT_TASKS; do
            TASK_ID=$(basename "$task_file" .md)
            STATUS=$(grep -o 'status:[[:space:]]*[^[:space:]]*' "$task_file" | cut -d: -f2 | tr -d ' ' || echo "unknown")
            TITLE=$(grep -o 'title:[[:space:]]*[^[:space:]]*' "$task_file" | cut -d: -f2- | sed 's/^[[:space:]]*//' || echo "No title")
            
            case "$STATUS" in
                "completed") STATUS_ICON="✓" ;;
                "in_progress") STATUS_ICON="🔄" ;;
                "failed") STATUS_ICON="✗" ;;
                *) STATUS_ICON="📋" ;;
            esac
            
            echo "$STATUS_ICON $TASK_ID: $TITLE ($STATUS)"
        done
        echo ""
    fi
fi

# Provide guidance based on project state
if [ ! -f "./project_state.json" ]; then
    echo "=== GETTING STARTED ==="
    echo "To begin, use these commands:"
    echo "  /prd <description>    - Create Product Requirement Document"
    echo "  /epic <description>   - Create Epic from PRD"
    echo "  /story <description>  - Create User Story from Epic"
    echo ""
    echo "Or use workflow commands:"
    echo "  /workflow:plan       - Analyze and plan migration tasks"
    echo "  /workflow:implement  - Implement specific tasks"
    echo "  /workflow:validate   - Run comprehensive validation"
    echo ""
fi

echo "$(date): SessionStart hook completed" >> ./.workflow/logs/hook.log
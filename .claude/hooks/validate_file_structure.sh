#!/bin/bash

# This script validates file structure and manages project state updates when agents stop
# It is triggered by a Stop hook when sub-agents complete tasks
# Enhanced with comprehensive toolchain validation from Development_Toolchain.md

set -e

# Create log directory if it doesn't exist
mkdir -p ./.workflow/logs

echo "$(date): Agent stop validation triggered" >> ./.workflow/logs/hook.log

# Read hook data to understand which agent stopped and what they were doing
HOOK_DATA=$(cat)

# Parse agent name and context from hook data
AGENT_NAME=$(echo "$HOOK_DATA" | grep -o '"name":"[^"]*"' | cut -d'"' -f4 2>/dev/null || echo "unknown")
AGENT_PROMPT=$(echo "$HOOK_DATA" | grep -o '"prompt":"[^"]*"' | head -1 | cut -d'"' -f4 2>/dev/null || echo "")

echo "$(date): Agent '$AGENT_NAME' stopped with prompt context" >> ./.workflow/logs/hook.log

# Function to update project state when stories are completed
update_project_state_on_completion() {
    echo "$(date): Checking for completed stories to compact" >> ./.workflow/logs/hook.log
    
    # Check if project_state.json exists
    if [ ! -f "./project_state.json" ]; then
        echo "$(date): project_state.json not found, skipping state update" >> ./.workflow/logs/hook.log
        return 0
    fi
    
    # Use Python to handle complex JSON manipulation for story compaction
    uv run python -c "
import json
import sys
import datetime
import copy

try:
    # Read current project state
    with open('project_state.json', 'r') as f:
        state = json.load(f)
    
    state_changed = False
    
    # Group stories by their epic dependencies
    epic_to_stories = {}
    
    # Collect all stories that belong to each epic
    for story in state.get('stories', []):
        dependencies = story.get('dependencies', [])
        for dep in dependencies:
            if dep.startswith('EPIC-'):
                if dep not in epic_to_stories:
                    epic_to_stories[dep] = []
                epic_to_stories[dep].append(story)
    
    # Check each epic to see if all its stories are completed
    for epic_id, stories in epic_to_stories.items():
        # Check if all stories for this epic are completed
        all_stories_completed = len(stories) > 0
        for story in stories:
            if story.get('status') != 'completed':
                all_stories_completed = False
                break
        
        # If all stories are completed, compact them
        if all_stories_completed and len(stories) > 0:
            print(f'All stories completed for epic {epic_id}')
            
            # Create compacted stories with only essential fields
            compacted_stories = []
            for story in stories:
                compacted_story = {
                    'id': story.get('id'),
                    'title': story.get('title'),
                    'file_path': story.get('file_path'),
                    'status': story.get('status', 'completed')
                }
                compacted_stories.append(compacted_story)
            
            # Replace the stories in the state with compacted versions
            # We need to find and replace the stories in the original array
            new_stories = []
            for story in state.get('stories', []):
                # Check if this story belongs to the epic we're compacting
                if epic_id in story.get('dependencies', []):
                    # Find the compacted version
                    compacted = None
                    for cs in compacted_stories:
                        if cs['id'] == story['id']:
                            compacted = cs
                            break
                    if compacted:
                        new_stories.append(compacted)
                    else:
                        new_stories.append(story)
                else:
                    new_stories.append(story)
            
            state['stories'] = new_stories
            state_changed = True
            
            print(f'Compacted {len(stories)} stories for epic {epic_id}')
    
    # Update statistics if stories were compacted
    if state_changed:
        # Update last_updated timestamp
        state['last_updated'] = datetime.datetime.now().isoformat()
        
        # Create backup before modification
        import shutil
        shutil.copyfile('project_state.json', 'project_state.json.backup')
        
        # Write updated state
        with open('project_state.json', 'w') as f:
            json.dump(state, f, indent=2)
        
        print('Project state updated with compacted stories')
    else:
        print('No stories to compact')
        
except Exception as e:
    print(f'Error updating project state: {e}', file=sys.stderr)
    sys.exit(1)
" 2>>./.workflow/logs/hook.log || true
    
    echo "$(date): Project state update check completed" >> ./.workflow/logs/hook.log
}

# Function to add warning
add_warning() {
    WARNINGS="$WARNINGS\n⚠ $1"
    echo "$(date): WARNING: $1" >> ./.workflow/logs/hook.log
}

# Function to add error
add_error() {
    ERRORS="$ERRORS\n✗ $1"
    echo "$(date): ERROR: $1" >> ./.workflow/logs/hook.log
    VALIDATION_PASSED=0
}

# Validate recent file modifications if any
validate_recent_files() {
    echo "$(date): Checking for recently modified files" >> ./.workflow/logs/hook.log
    
    # Check for files created or modified in the last minute in workflow directories
    RECENT_FILES=$(find ./.workflow -type f -name "*.md" -mmin -1 2>/dev/null | head -10 || true)
    
    if [ -n "$RECENT_FILES" ]; then
        echo "$(date): Recently modified workflow files detected:" >> ./.workflow/logs/hook.log
        echo "$RECENT_FILES" >> ./.workflow/logs/hook.log
        
        # Basic validation of markdown files
        for file in $RECENT_FILES; do
            if [ -f "$file" ]; then
                # Check if it's a valid markdown file with frontmatter
                if head -1 "$file" | grep -q "^---"; then
                    echo "$(date): Valid markdown file with frontmatter: $file" >> ./.workflow/logs/hook.log
                else
                    add_warning "Markdown file missing frontmatter: $file"
                fi
            fi
        done
    fi
}

# Main execution
VALIDATION_PASSED=1
WARNINGS=""
ERRORS=""

# Perform project state update for completed stories
update_project_state_on_completion

# Validate recent file modifications
validate_recent_files

# Generate summary
echo "$(date): Agent stop validation completed for agent: $AGENT_NAME" >> ./.workflow/logs/hook.log

if [ $VALIDATION_PASSED -eq 1 ]; then
    echo "$(date): ✓ Agent stop validation passed" >> ./.workflow/logs/hook.log
    if [ -n "$WARNINGS" ]; then
        echo "$(date): Warnings generated:" >> ./.workflow/logs/hook.log
        echo -e "$WARNINGS" >> ./.workflow/logs/hook.log
        
        # Output warnings to stderr so they're visible
        echo "Agent stop validation warnings:" >&2
        echo -e "$WARNINGS" >&2
    fi
    exit 0
else
    echo "$(date): ✗ Agent stop validation failed" >> ./.workflow/logs/hook.log
    echo "$(date): Errors:" >> ./.workflow/logs/hook.log
    echo -e "$ERRORS" >> ./.workflow/logs/hook.log
    
    if [ -n "$WARNINGS" ]; then
        echo "$(date): Warnings:" >> ./.workflow/logs/hook.log
        echo -e "$WARNINGS" >> ./.workflow/logs/hook.log
    fi
    
    # Output errors to stderr so they're visible
    echo "Agent stop validation failed:" >&2
    echo -e "$ERRORS" >&2
    if [ -n "$WARNINGS" ]; then
        echo -e "$WARNINGS" >&2
    fi
    exit 1
fi
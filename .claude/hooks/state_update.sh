#!/bin/bash

# State update utility for project_state.json
# Used by existing hooks to maintain state consistency
# Integrated with existing toolchain infrastructure

set -e

# Create log directory if it doesn't exist
mkdir -p ./.workflow/logs

# Function to update project state
update_project_state() {
    local ACTION=$1
    local ENTITY_TYPE=$2
    local ENTITY_ID=$3
    local STATUS=$4
    local ADDITIONAL_DATA=$5
    
    # Validate required parameters
    if [ -z "$ACTION" ] || [ -z "$ENTITY_TYPE" ]; then
        echo "$(date): Missing required parameters for state update" >> ./.workflow/logs/hook.log
        return 1
    fi
    
    echo "$(date): State update - $ACTION $ENTITY_TYPE $ENTITY_ID -> $STATUS" >> ./.workflow/logs/hook.log
    
    # Check if project_state.json exists
    if [ ! -f "./project_state.json" ]; then
        echo "$(date): project_state.json not found, skipping state update" >> ./.workflow/logs/hook.log
        return 1
    fi
    
    # Use Python for JSON manipulation (more reliable than shell)
    local result=$(uv run python -c "
import json
import sys
import datetime
from pathlib import Path
import copy

# Read current state
try:
    with open('project_state.json', 'r') as f:
        original_state = json.load(f)
        state = copy.deepcopy(original_state)
except FileNotFoundError:
    print('project_state.json not found')
    sys.exit(1)

# Update last_updated timestamp
state['last_updated'] = datetime.datetime.now().isoformat()

action = sys.argv[1]
entity_type = sys.argv[2]
entity_id = sys.argv[3] if len(sys.argv) > 3 else None
status = sys.argv[4] if len(sys.argv) > 4 else None

# Validate required parameters
if not action or not entity_type:
    print('Missing required parameters for state update')
    sys.exit(1)

state_changed = False

if action == 'add_prd':
    # Add new PRD
    new_prd = {
        'id': entity_id,
        'title': status,  # Using status as title for new PRDs
        'description': '',
        'status': 'draft',
        'created': datetime.datetime.now().isoformat(),
        'epics': []
    }
    state['prds'].append(new_prd)
    state['statistics']['total_prds'] = len(state['prds'])
    state_changed = True
    
elif action == 'add_epic':
    # Add new Epic to specified PRD
    prd_id = sys.argv[5] if len(sys.argv) > 5 else None
    for prd in state['prds']:
        if prd['id'] == prd_id:
            new_epic = {
                'id': entity_id,
                'title': status,  # Using status as title for new epics
                'description': '',
                'status': 'planned',
                'created': datetime.datetime.now().isoformat(),
                'prd_id': prd_id,
                'stories': []
            }
            prd['epics'].append(new_epic)
            state['statistics']['total_epics'] = len([e for prd in state['prds'] for e in prd['epics']])
            state_changed = True
            break
    
elif action == 'add_story':
    # Add new Story to specified Epic
    epic_id = sys.argv[5] if len(sys.argv) > 5 else None
    for prd in state['prds']:
        for epic in prd['epics']:
            if epic['id'] == epic_id:
                new_story = {
                    'id': entity_id,
                    'title': status,  # Using status as title for new stories
                    'description': '',
                    'status': 'pending',
                    'created': datetime.datetime.now().isoformat(),
                    'epic_id': epic_id,
                    'prd_id': prd['id'],
                    'validation_status': 'not_started',
                    'last_validation': None,
                    'validation_pass_count': 0,
                    'validation_fail_count': 0
                }
                epic['stories'].append(new_story)
                state['statistics']['total_stories'] = len([s for prd in state['prds'] for epic in prd['epics'] for s in epic['stories']])
                state_changed = True
                break

elif action == 'update_status':
    # Update status of existing entity
    for prd in state['prds']:
        if entity_type == 'prd' and prd['id'] == entity_id:
            if prd['status'] != status:
                prd['status'] = status
                state_changed = True
            break
        for epic in prd['epics']:
            if entity_type == 'epic' and epic['id'] == entity_id:
                if epic['status'] != status:
                    epic['status'] = status
                    state_changed = True
                break
            for story in epic['stories']:
                if entity_type == 'story' and story['id'] == entity_id:
                    old_status = story['status']
                    if story['status'] != status:
                        story['status'] = status
                        state_changed = True
                        
                        # Update statistics
                        if old_status == 'completed' and status != 'completed':
                            state['statistics']['completed_stories'] -= 1
                        elif old_status != 'completed' and status == 'completed':
                            state['statistics']['completed_stories'] += 1
                        
                        if old_status == 'in_progress' and status != 'in_progress':
                            state['statistics']['in_progress_stories'] -= 1
                        elif old_status != 'in_progress' and status == 'in_progress':
                            state['statistics']['in_progress_stories'] += 1
                        
                        if old_status == 'failed' and status != 'failed':
                            state['statistics']['failed_stories'] -= 1
                        elif old_status != 'failed' and status == 'failed':
                            state['statistics']['failed_stories'] += 1
                    break

elif action == 'update_validation':
    # Update validation status for a story
    for prd in state['prds']:
        for epic in prd['epics']:
            for story in epic['stories']:
                if story['id'] == entity_id:
                    if story['validation_status'] != status:
                        story['validation_status'] = status
                        story['last_validation'] = datetime.datetime.now().isoformat()
                        
                        if status == 'passed':
                            story['validation_pass_count'] += 1
                            state['statistics']['validation_passed'] += 1
                        elif status == 'failed':
                            story['validation_fail_count'] += 1
                            state['statistics']['validation_failed'] += 1
                        
                        state_changed = True
                    break

# Add to recent activity only if different from previous activity
if state_changed:
    activity_entry = {
        'timestamp': datetime.datetime.now().isoformat(),
        'action': action,
        'entity_type': entity_type,
        'entity_id': entity_id,
        'status': status
    }
    
    # Check if this activity is different from the last one
    should_add_activity = True
    if state['recent_activity']:
        last_activity = state['recent_activity'][-1]
        if (last_activity['action'] == action and 
            last_activity['entity_type'] == entity_type and 
            last_activity['entity_id'] == entity_id and 
            last_activity['status'] == status):
            should_add_activity = False
    
    if should_add_activity:
        state['recent_activity'].append(activity_entry)
        # Keep only last 50 activities
        state['recent_activity'] = state['recent_activity'][-50:]

# Write updated state only if there are changes
if state_changed:
    # Create backup before modification
    import shutil
    shutil.copyfile('project_state.json', 'project_state.json.backup')
    
    with open('project_state.json', 'w') as f:
        json.dump(state, f, indent=2)
    
    print('State updated successfully')
else:
    print('No changes to state')
" "$@")

    echo "$result"
    
    # Check if state was actually updated
    if [[ "$result" == *"State updated successfully"* ]]; then
        echo "$(date): State update operation completed" >> ./.workflow/logs/hook.log
    elif [[ "$result" == *"No changes to state"* ]]; then
        echo "$(date): No changes to state, skipping update" >> ./.workflow/logs/hook.log
    elif [[ "$result" == *"Missing required parameters"* ]]; then
        echo "$(date): State update skipped due to missing parameters" >> ./.workflow/logs/hook.log
        return 1
    else
        echo "$(date): State update operation failed" >> ./.workflow/logs/hook.log
        return 1
    fi
}

# Function to get current state information
get_state_info() {
    local ENTITY_TYPE=$1
    local ENTITY_ID=$2
    
    if [ ! -f "./project_state.json" ]; then
        return 1
    fi

    uv run python -c "
import json
import sys

try:
    with open('project_state.json', 'r') as f:
        state = json.load(f)
    
    entity_type = sys.argv[1] if len(sys.argv) > 1 else None
    entity_id = sys.argv[2] if len(sys.argv) > 2 else None
    
    if entity_type and entity_id:
        # Find specific entity
        for prd in state['prds']:
            if entity_type == 'prd' and prd['id'] == entity_id:
                print(json.dumps(prd))
                break
            for epic in prd['epics']:
                if entity_type == 'epic' and epic['id'] == entity_id:
                    print(json.dumps(epic))
                    break
                for story in epic['stories']:
                    if entity_type == 'story' and story['id'] == entity_id:
                        print(json.dumps(story))
                        break
    else:
        # Return summary
        summary = {
            'total_prds': state['statistics']['total_prds'],
            'total_epics': state['statistics']['total_epics'],
            'total_stories': state['statistics']['total_stories'],
            'completed_stories': state['statistics']['completed_stories'],
            'in_progress_stories': state['statistics']['in_progress_stories'],
            'project_status': state['status']
        }
        print(json.dumps(summary))
        
except Exception as e:
    print(f'Error reading state: {e}')
    sys.exit(1)
" "$ENTITY_TYPE" "$ENTITY_ID"
}

# Main execution
case "${1:-}" in
    "update")
        shift
        update_project_state "$@"
        ;;
    "get")
        shift
        get_state_info "$@"
        ;;
    "summary")
        get_state_info
        ;;
    *)
        echo "Usage: $0 {update|get|summary} [args]"
        echo "  update add_prd <prd_id> <title>"
        echo "  update add_epic <epic_id> <title> <prd_id>"
        echo "  update add_story <story_id> <title> <epic_id>"
        echo "  update update_status <entity_type> <entity_id> <status>"
        echo "  update update_validation <story_id> <status>"
        echo "  get [entity_type] [entity_id]"
        echo "  summary"
        exit 1
        ;;
esac
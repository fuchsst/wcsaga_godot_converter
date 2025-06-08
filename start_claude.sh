#!/bin/bash

PROMPT_TEXT="Today is $(date). Please list the following available tasks with a brief description for each:"
COMMANDS_DIR=".claude/commands"

for f in "$COMMANDS_DIR"/*; do
    # Extract filename without extension
    filename=$(basename -- "$f")
    extension="${filename##*.}"
    filename="${filename%.*}"
    PROMPT_TEXT="$PROMPT_TEXT $filename,"
done

# Remove the trailing comma
PROMPT_TEXT=${PROMPT_TEXT%,}

claude "$PROMPT_TEXT"

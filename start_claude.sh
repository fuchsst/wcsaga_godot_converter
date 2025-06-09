#!/bin/bash

PROMPT_TEXT="Today is $(date). We have the the following tasks available:\n"
COMMANDS_DIR=".claude/commands"

for f in "$COMMANDS_DIR"/*; do
    # Extract filename without extension
    filename=$(basename -- "$f")
    extension="${filename##*.}"
    filename="${filename%.*}"
    PROMPT_TEXT="$PROMPT_TEXT\n* $filename"
done

# Remove the trailing comma
PROMPT_TEXT=${PROMPT_TEXT%,}

claude "$PROMPT_TEXT"

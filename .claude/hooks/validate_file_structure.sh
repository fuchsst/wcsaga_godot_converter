#!/bin/bash

# This script validates file structure before writing files
# It is triggered by a PreToolUse hook when WriteFile tool is used
# Enhanced with comprehensive toolchain validation from Development_Toolchain.md

set -e

# Create log directory if it doesn't exist
mkdir -p ./.claude_workflow/logs

echo "$(date): File structure validation triggered" >> ./.claude_workflow/logs/hook.log

# Read hook data to understand what file operation is being performed
HOOK_DATA=$(cat)
FILE_PATH=$(echo "$HOOK_DATA" | grep -o '"file_path":"[^"]*"' | cut -d'"' -f4 2>/dev/null || echo "")

if [ -z "$FILE_PATH" ]; then
    echo "$(date): No file path found in hook data" >> ./.claude_workflow/logs/hook.log
    exit 0
fi

echo "$(date): Validating file structure for: $FILE_PATH" >> ./.claude_workflow/logs/hook.log

VALIDATION_PASSED=1
WARNINGS=""
ERRORS=""

# Function to add warning
add_warning() {
    WARNINGS="$WARNINGS\n⚠ $1"
    echo "$(date): WARNING: $1" >> ./.claude_workflow/logs/hook.log
}

# Function to add error
add_error() {
    ERRORS="$ERRORS\n✗ $1"
    echo "$(date): ERROR: $1" >> ./.claude_workflow/logs/hook.log
    VALIDATION_PASSED=0
}

# Validate Godot project structure
validate_godot_structure() {
    local file_path=$1
    
    # Check if file is in appropriate Godot directory structure
    case "$file_path" in
        # Core Godot directories
        "./features/"*|"./assets/"*|"./autoload/"*|"./scenes/"*|"./scripts/"*)
            echo "$(date): File in valid Godot structure directory" >> ./.claude_workflow/logs/hook.log
            ;;
        # Data converter directories
        "./data_converter/"*|"./converter/"*)
            echo "$(date): File in converter directory structure" >> ./.claude_workflow/logs/hook.log
            ;;
        # Root level files
        "./project.godot"|"./export_presets.cfg"|"./README.md"|"./QWEN.md"|"./CLAUDE.md")
            echo "$(date): Valid root level file" >> ./.claude_workflow/logs/hook.log
            ;;
        # Configuration and documentation
        "./.claude/"*|"./.qwen/"*|"./concepts/"*|"./docs/"*)
            echo "$(date): Configuration or documentation file" >> ./.claude_workflow/logs/hook.log
            ;;
        # Build and cache directories (should be warnings)
        "./.godot/"*|"./.pytest_cache/"*|"./build/"*|"./dist/"*)
            add_warning "Writing to build/cache directory: $file_path"
            ;;
        *)
            add_warning "File not in standard Godot project structure: $file_path"
            ;;
    esac
}

# Validate naming conventions
validate_naming_conventions() {
    local file_path=$1
    local filename=$(basename "$file_path")
    local extension="${filename##*.}"
    local basename="${filename%.*}"
    
    # Check for snake_case in GDScript files
    if [ "$extension" = "gd" ]; then
        if echo "$basename" | grep -q "^[a-z][a-z0-9_]*$"; then
            echo "$(date): GDScript file follows snake_case: $filename" >> ./.claude_workflow/logs/hook.log
        else
            add_error "GDScript file '$filename' does not follow snake_case naming convention"
        fi
    fi
    
    # Check for PascalCase in scene files
    if [ "$extension" = "tscn" ]; then
        if echo "$basename" | grep -q "^[A-Z][A-Za-z0-9]*$"; then
            echo "$(date): Scene file follows PascalCase: $filename" >> ./.claude_workflow/logs/hook.log
        else
            add_warning "Scene file '$filename' should follow PascalCase naming convention"
        fi
    fi
    
    # Check Python files follow snake_case
    if [ "$extension" = "py" ]; then
        if echo "$basename" | grep -q "^[a-z][a-z0-9_]*$"; then
            echo "$(date): Python file follows snake_case: $filename" >> ./.claude_workflow/logs/hook.log
        else
            add_warning "Python file '$filename' should follow snake_case naming convention"
        fi
    fi
    
    # Check for invalid characters using grep
    if echo "$filename" | grep -q "[[:space:]]"; then
        add_error "Filename contains spaces: $filename (use underscores instead)"
    fi
    
    if echo "$filename" | grep -q "[^a-zA-Z0-9._-]"; then
        add_warning "Filename contains special characters: $filename"
    fi
}

# Validate file type and location consistency
validate_file_type_location() {
    local file_path=$1
    local extension="${file_path##*.}"
    
    case "$extension" in
        "gd")
            # GDScript files should be in scripts/ or alongside scenes
            if ! echo "$file_path" | grep -q "scripts/\|scenes/\|features/\|autoload/"; then
                add_warning "GDScript file outside recommended directories: $file_path"
            fi
            ;;
        "tscn"|"tres")
            # Scene and resource files should be in scenes/ or features/
            if ! echo "$file_path" | grep -q "scenes/\|features/\|assets/"; then
                add_warning "Scene/resource file outside recommended directories: $file_path"
            fi
            ;;
        "py")
            # Python files should be in converter or data_converter directories
            if ! echo "$file_path" | grep -q "converter/\|data_converter/\|.claude/\|.qwen/"; then
                add_warning "Python file outside converter directories: $file_path"
            fi
            ;;
        "md")
            # Documentation files should be in docs/ or root
            if ! echo "$file_path" | grep -q "docs/\|concepts/\|^./[^/]*\.md$"; then
                add_warning "Documentation file outside docs directories: $file_path"
            fi
            ;;
    esac
}

# Check for protected directories
validate_protected_directories() {
    local file_path=$1
    
    # Prevent writing to Godot's generated directories
    if echo "$file_path" | grep -q "^\./.godot/"; then
        add_error "Cannot write to Godot's generated .godot directory: $file_path"
    fi
    
    # Prevent writing to cache directories
    if echo "$file_path" | grep -q "^\./.pytest_cache/\|^./\.cache/"; then
        add_error "Cannot write to cache directories: $file_path"
    fi
    
    # Warn about writing to system directories
    if echo "$file_path" | grep -q "^/usr/\|^/etc/\|^/var/\|^/tmp/"; then
        add_error "Cannot write to system directories: $file_path"
    fi
}

# Validate against toolchain requirements
validate_toolchain_requirements() {
    local file_path=$1
    local extension="${file_path##*.}"
    
    # Check if toolchain tools are available for the file type
    case "$extension" in
        "gd")
            if ! command -v gdformat &> /dev/null; then
                add_warning "gdformat not available - GDScript formatting may not work"
            fi
            if ! command -v gdlint &> /dev/null; then
                add_warning "gdlint not available - GDScript linting may not work"
            fi
            ;;
        "py")
            if ! command -v ruff &> /dev/null; then
                add_warning "ruff not available - Python linting/formatting may not work"
            fi
            if ! command -v uv &> /dev/null; then
                add_warning "uv not available - Python environment management may not work"
            fi
            ;;
    esac
}

# Run all validations
validate_godot_structure "$FILE_PATH"
validate_naming_conventions "$FILE_PATH"
validate_file_type_location "$FILE_PATH"
validate_protected_directories "$FILE_PATH"
validate_toolchain_requirements "$FILE_PATH"

# Generate summary
echo "$(date): File structure validation completed for: $FILE_PATH" >> ./.claude_workflow/logs/hook.log

if [ $VALIDATION_PASSED -eq 1 ]; then
    echo "$(date): ✓ File structure validation passed" >> ./.claude_workflow/logs/hook.log
    if [ -n "$WARNINGS" ]; then
        echo "$(date): Warnings generated:" >> ./.claude_workflow/logs/hook.log
        echo -e "$WARNINGS" >> ./.claude_workflow/logs/hook.log
        
        # Output warnings to stderr so they're visible
        echo "File structure warnings for $FILE_PATH:" >&2
        echo -e "$WARNINGS" >&2
    fi
    exit 0
else
    echo "$(date): ✗ File structure validation failed" >> ./.claude_workflow/logs/hook.log
    echo "$(date): Errors:" >> ./.claude_workflow/logs/hook.log
    echo -e "$ERRORS" >> ./.claude_workflow/logs/hook.log
    
    if [ -n "$WARNINGS" ]; then
        echo "$(date): Warnings:" >> ./.claude_workflow/logs/hook.log
        echo -e "$WARNINGS" >> ./.claude_workflow/logs/hook.log
    fi
    
    # Output errors to stderr so they're visible
    echo "File structure validation failed for $FILE_PATH:" >&2
    echo -e "$ERRORS" >&2
    if [ -n "$WARNINGS" ]; then
        echo -e "$WARNINGS" >&2
    fi
    exit 1
fi
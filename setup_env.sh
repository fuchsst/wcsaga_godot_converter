#!/bin/bash

# Wing Commander Saga Godot Converter - Environment Setup Script
# This script sets up the complete development environment including:
# - uv for Python package management
# - GDScript Toolkit (gdformat, gdlint)
# - Python code quality tools (ruff, pytest)
# - Godot Engine validation and setup instructions

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check system dependencies
check_system_deps() {
    log_info "Checking system dependencies..."
    
    local missing_deps=()
    
    for cmd in curl wget git; do
        if ! command_exists "$cmd"; then
            missing_deps+=("$cmd")
        fi
    done
    
    if [ ${#missing_deps[@]} -gt 0 ]; then
        log_error "Missing system dependencies: ${missing_deps[*]}"
        log_info "Please install them using your system package manager:"
        log_info "  Ubuntu/Debian: sudo apt update && sudo apt install ${missing_deps[*]}"
        log_info "  CentOS/RHEL: sudo yum install ${missing_deps[*]}"
        log_info "  Arch: sudo pacman -S ${missing_deps[*]}"
        exit 1
    fi
    
    log_success "All system dependencies are available"
}

# Install uv if not present
install_uv() {
    log_info "Setting up uv (Python package manager)..."
    
    if command_exists uv; then
        local uv_version=$(uv --version 2>/dev/null | head -n1)
        log_success "uv is already installed: $uv_version"
        return 0
    fi
    
    log_info "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Add uv to PATH for current session
    export PATH="$HOME/.cargo/bin:$PATH"
    
    if command_exists uv; then
        log_success "uv installed successfully: $(uv --version)"
    else
        log_error "Failed to install uv. Please install manually from https://github.com/astral-sh/uv"
        exit 1
    fi
}

# Setup Python environment with uv
setup_python_env() {
    log_info "Setting up Python virtual environment..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -d ".venv" ]; then
        log_info "Creating virtual environment with uv..."
        uv venv
    else
        log_success "Virtual environment already exists"
    fi
    
    # Install production dependencies
    log_info "Installing production dependencies..."
    uv pip install -e .
    
    # Install development dependencies
    log_info "Installing development dependencies..."
    uv pip install -e ".[dev]"
    
    log_success "Python environment setup complete"
}

# Install GDScript development tools
install_gdscript_tools() {
    log_info "Installing GDScript Toolkit (gdformat, gdlint)..."
    
    # Install gdtoolkit which contains gdformat and gdlint
    uv pip install "gdtoolkit>=4.0"
    
    # Verify installation
    if uv run gdformat --version >/dev/null 2>&1 && uv run gdlint --version >/dev/null 2>&1; then
        log_success "GDScript Toolkit installed successfully"
        log_info "  - gdformat: $(uv run gdformat --version 2>/dev/null || echo 'installed')"
        log_info "  - gdlint: $(uv run gdlint --version 2>/dev/null || echo 'installed')"
    else
        log_error "Failed to install or verify GDScript Toolkit"
        exit 1
    fi
}

# Install Python code quality tools
install_python_tools() {
    log_info "Installing Python code quality tools..."
    
    # Install ruff and pytest
    uv pip install ruff pytest pytest-cov pytest-mock
    
    # Verify installation
    if uv run ruff --version >/dev/null 2>&1 && uv run pytest --version >/dev/null 2>&1; then
        log_success "Python code quality tools installed successfully"
        log_info "  - ruff: $(uv run ruff --version)"
        log_info "  - pytest: $(uv run pytest --version)"
    else
        log_error "Failed to install or verify Python code quality tools"
        exit 1
    fi
}

# Get latest Godot version from GitHub API
get_latest_godot_version() {
    local latest_version
    latest_version=$(curl -s https://api.github.com/repos/godotengine/godot/releases/latest | grep '"tag_name"' | cut -d'"' -f4)
    
    if [ -z "$latest_version" ]; then
        log_error "Failed to fetch latest Godot version from GitHub API"
        exit 1
    fi
    
    echo "$latest_version"
}

# Install Godot Engine
install_godot() {
    log_info "Installing Godot Engine..."
    
    # Check if already installed and working
    if [ -f ".env" ]; then
        set -a
        source .env
        set +a
        
        if [ -n "$GODOT_BIN" ] && [ -x "$GODOT_BIN" ] && $GODOT_BIN --version >/dev/null 2>&1; then
            local godot_version=$($GODOT_BIN --version 2>/dev/null | head -n1)
            log_success "Godot Engine is already installed: $godot_version"
            return 0
        fi
    fi
    
    # Get latest version
    log_info "Fetching latest Godot version..."
    local version
    version=$(get_latest_godot_version)
    log_info "Latest Godot version: $version"
    
    # Create godot directory
    local godot_dir="$HOME/.local/bin"
    mkdir -p "$godot_dir"
    
    # Determine architecture
    local arch
    case $(uname -m) in
        x86_64) arch="linux.x86_64" ;;
        arm64|aarch64) arch="linux.arm64" ;;
        *) log_error "Unsupported architecture: $(uname -m)"; exit 1 ;;
    esac
    
    # Clean version string and construct URL
    # Version comes as "4.4.1-stable", we need to use it as-is
    local clean_version="${version}"
    local godot_url="https://github.com/godotengine/godot/releases/download/${clean_version}/Godot_v${clean_version}_${arch}.zip"
    
    local godot_binary="$godot_dir/godot"
    
    # Download and install Godot binary
    log_info "Downloading Godot binary..."
    local temp_dir=$(mktemp -d)
    
    if wget -q "$godot_url" -O "$temp_dir/godot.zip"; then
        cd "$temp_dir"
        unzip -q godot.zip
        
        # Find the binary (name varies by version)
        local binary_name=$(find . -name "Godot_v*" -type f -executable | head -n1)
        if [ -n "$binary_name" ]; then
            mv "$binary_name" "$godot_binary"
            chmod +x "$godot_binary"
            log_success "Godot installed: $godot_binary"
        else
            log_error "Could not find Godot binary in downloaded archive"
            exit 1
        fi
    else
        log_error "Failed to download Godot from $godot_url"
        exit 1
    fi
    
    # Clean up
    rm -rf "$temp_dir"
    
    # Update .env file
    update_env_file "$godot_binary"
    
    # Add to PATH if not already there
    if [[ ":$PATH:" != *":$godot_dir:"* ]]; then
        export PATH="$godot_dir:$PATH"
        log_info "Added $godot_dir to PATH for current session"
        
        # Add to shell profile for permanent PATH update
        local shell_profile=""
        if [ -n "$BASH_VERSION" ]; then
            shell_profile="$HOME/.bashrc"
        elif [ -n "$ZSH_VERSION" ]; then
            shell_profile="$HOME/.zshrc"
        fi
        
        if [ -n "$shell_profile" ] && [ -f "$shell_profile" ]; then
            if ! grep -q "$godot_dir" "$shell_profile"; then
                echo "export PATH=\"$godot_dir:\$PATH\"" >> "$shell_profile"
                log_success "Added Godot to PATH in $shell_profile"
            fi
        fi
    fi
    
    # Verify installation
    if "$godot_binary" --version >/dev/null 2>&1; then
        local installed_version=$("$godot_binary" --version 2>/dev/null | head -n1)
        log_success "Godot installation verified: $installed_version"
        log_info "Note: Use --headless flag for CI/CD and validation scripts"
        log_info "Godot is now available as 'godot' command"
    else
        log_error "Godot installation verification failed"
        exit 1
    fi
}

# Update .env file with Godot path
update_env_file() {
    local godot_binary="$1"
    
    log_info "Updating .env file with Godot path..."
    
    # Create .env if it doesn't exist
    if [ ! -f ".env" ]; then
        touch .env
    fi
    
    # Remove existing GODOT_BIN entry (preserve other GODOT_ entries like API keys)
    grep -v '^GODOT_BIN=' .env > .env.tmp && mv .env.tmp .env || true
    
    # Add new entry
    echo "GODOT_BIN=\"$godot_binary\"" >> .env
    
    log_success ".env file updated with Godot path"
}

# Validate Godot installation
validate_godot_installation() {
    log_info "Validating Godot installation..."
    
    # Source .env to get GODOT_BIN
    if [ -f ".env" ]; then
        set -a
        source .env
        set +a
        
        if [ -n "$GODOT_BIN" ] && [ -x "$GODOT_BIN" ]; then
            if $GODOT_BIN --version >/dev/null 2>&1; then
                local godot_version=$($GODOT_BIN --version 2>/dev/null | head -n1)
                log_success "Godot Engine validation successful: $godot_version"
                return 0
            fi
        fi
    fi
    
    log_error "Godot validation failed"
    return 1
}

# Validate all tools
validate_installation() {
    log_info "Validating complete installation..."
    
    local validation_failed=false
    
    # Test uv
    if ! command_exists uv; then
        log_error "uv validation failed"
        validation_failed=true
    fi
    
    # Test Python environment
    if ! uv run python -c "import sys; print(f'Python {sys.version}')" >/dev/null 2>&1; then
        log_error "Python environment validation failed"
        validation_failed=true
    fi
    
    # Test GDScript tools
    if ! uv run gdformat --version >/dev/null 2>&1; then
        log_error "gdformat validation failed"
        validation_failed=true
    fi
    
    if ! uv run gdlint --version >/dev/null 2>&1; then
        log_error "gdlint validation failed"
        validation_failed=true
    fi
    
    # Test Python tools
    if ! uv run ruff --version >/dev/null 2>&1; then
        log_error "ruff validation failed"
        validation_failed=true
    fi
    
    if ! uv run pytest --version >/dev/null 2>&1; then
        log_error "pytest validation failed"
        validation_failed=true
    fi
    
    # Test Godot installation
    if ! validate_godot_installation; then
        log_error "Godot validation failed"
        validation_failed=true
    fi
    
    if [ "$validation_failed" = true ]; then
        log_error "Some tools failed validation. Please check the installation."
        exit 1
    fi
    
    log_success "All tools validated successfully!"
}

# Run basic quality checks
run_basic_checks() {
    log_info "Running basic code quality checks..."
    
    # Run Python formatting check (if there are Python files)
    if find . -name "*.py" -not -path "./.venv/*" | grep -q .; then
        log_info "Checking Python code formatting..."
        if uv run ruff format --check . >/dev/null 2>&1; then
            log_success "Python code formatting is correct"
        else
            log_warning "Python code formatting issues found. Run 'uv run ruff format .' to fix"
        fi
        
        log_info "Checking Python code with ruff linter..."
        if uv run ruff check . >/dev/null 2>&1; then
            log_success "Python code passes ruff linting"
        else
            log_warning "Python linting issues found. Run 'uv run ruff check .' for details"
        fi
    fi
    
    # Run GDScript formatting check (if there are GDScript files)
    if find . -name "*.gd" | grep -q .; then
        log_info "Checking GDScript code formatting..."
        if uv run gdformat --check . >/dev/null 2>&1; then
            log_success "GDScript code formatting is correct"
        else
            log_warning "GDScript formatting issues found. Run 'uv run gdformat .' to fix"
        fi
        
        log_info "Checking GDScript code with gdlint..."
        if uv run gdlint . >/dev/null 2>&1; then
            log_success "GDScript code passes gdlint"
        else
            log_warning "GDScript linting issues found. Run 'uv run gdlint .' for details"
        fi
    fi
}

# Print summary
print_summary() {
    echo
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  SETUP COMPLETE - ENVIRONMENT SUMMARY"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo
    log_success "Development environment is ready!"
    echo
    echo "Available commands:"
    echo "  Python Environment:"
    echo "    uv run python <script>     - Run Python scripts"
    echo "    uv run pytest              - Run Python tests"
    echo "    uv pip install <package>   - Install Python packages"
    echo
    echo "  Code Quality:"
    echo "    uv run ruff format .        - Format Python code"
    echo "    uv run ruff check .         - Lint Python code"
    echo "    uv run gdformat .           - Format GDScript code"
    echo "    uv run gdlint .             - Lint GDScript code"
    echo
    echo "  Project Commands (via Makefile):"
    echo "    make install-dev            - Install development dependencies"
    echo "    make test                   - Run all tests"
    echo "    make quality                - Run all quality checks"
    echo "    make format                 - Format all code"
    echo "    make lint                   - Lint all code"
    echo
    # Source .env for current session
    if [ -f ".env" ]; then
        set -a
        source .env
        set +a
    fi
    
    if [ -n "$GODOT_BIN" ] && [ -x "$GODOT_BIN" ]; then
        local godot_version=$($GODOT_BIN --version 2>/dev/null | head -n1 || echo "unknown")
        echo "  Godot Engine ($godot_version):"
        echo "    \$GODOT_BIN --version       - Check Godot version"
        echo "    \$GODOT_BIN --headless      - Run in headless mode for CI/CD"
        echo "    \$GODOT_BIN --script <file> - Run GDScript validation"
    else
        echo "  ⚠️  Godot Engine: Installation failed or not accessible"
    fi
    echo
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# Main execution
main() {
    echo "Wing Commander Saga Godot Converter - Environment Setup"
    echo "========================================================"
    echo
    
    check_system_deps
    install_uv
    setup_python_env
    install_gdscript_tools
    install_python_tools
    install_godot
    validate_installation
    run_basic_checks
    print_summary
}

# Run main function
main "$@"
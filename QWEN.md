# Qwen Code - Project Context for wcsaga-code

## Project Type
This is a **code project** for an agentic migration system that converts the Wing Commander Saga game engine from C++ to Godot/GDScript.

## Project Overview
The Wing Commander Saga to Godot Converter is an agentic migration system that implements a hierarchical multi-agent framework for migrating the Wing Commander Saga game engine from C++ to Godot. It uses specialized AI agents to automate the complex process of code translation, refactoring, and validation.

### Key Technologies
- **Python** as the primary programming language
- **uv** to to manage dependecies and the virtual environment
- **CrewAI** framework for multi-agent orchestration
- **DeepSeek V3.1** model for high-level cognitive tasks (planning, analysis, decomposition)
- **qwen-code** CLI agent for code generation tasks (built on Qwen3-Coder models)
- **Godot Engine** as the target game engine
- **GDScript** as the target scripting language

### Architecture
The system is organized around five specialized AI agents:
1. **MigrationArchitect** (DeepSeek V3.1) - Lead Systems Architect responsible for high-level planning
2. **CodebaseAnalyst** (DeepSeek V3.1) - Senior Software Analyst who analyzes the legacy codebase
3. **TaskDecompositionSpecialist** (DeepSeek V3.1) - Technical Project Manager who breaks down tasks
4. **PromptEngineeringAgent** (DeepSeek V3.1) - AI Communications Specialist who creates precise prompts
5. **QualityAssuranceAgent** (DeepSeek V3.1) - QA Automation Engineer who verifies results

All code generation tasks are handled by the **qwen-code** CLI agent.

## Directory Structure
```
wcsaga_godot_converter/
├── converter/              # Main migration system code
│   ├── agents/             # Agent definitions and configurations (DeepSeek V3.1)
│   ├── analyst/            # Code Analyst agent implementation
│   ├── config/             # Configuration files
│   ├── context/            # Guidance artifacts (style guides, rules, templates)
│   ├── orchestrator/       # Orchestrator agent implementation (DeepSeek V3.1)
│   ├── prompt_engineering/ # Prompt Engineering agent implementation
│   ├── refactoring/        # Refactoring Specialist agent implementation (qwen-code)
│   ├── scripts/            # Utility scripts
│   ├── tasks/              # Task definitions and templates
│   ├── test_generator/    # Test Generator agent implementation (qwen-code)
│   ├── tests/             # System tests
│   ├── tools/             # Custom tools for CLI agent control (qwen-code)
│   ├── validation/        # Validation Engineer agent implementation (qwen-code)
│   └── workflows/          # Process definitions
├── pyproject.toml          # Modern Python project configuration
├── setup_environment.py    # Environment setup script
├── analyze_source_codebase.py # Codebase analysis script
└── README.md              # Project documentation
```

## Building and Running

### Dependencies
- Python 3.9+
- CrewAI framework
- DeepSeek API access for cognitive agents
- qwen-code CLI agent installed and accessible in PATH
- [uv](https://github.com/astral-sh/uv) for dependency management

### Installation
```bash
# Create virtual environment with uv
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install package in editable mode
uv pip install -e .

# For development dependencies
uv pip install -e ".[dev]"
```

### Configuration
1. Set environment variables for DeepSeek API:
   ```bash
   export DEEPSEEK_API_KEY="your-api-key-here"
   export DEEPSEEK_BASE_URL="https://api.deepseek.com/v1"
   ```

## Development Conventions

### Code Structure
- Each agent has its own directory with implementation files
- Context engineering artifacts are stored in the `context/` directory
- Prompt templates are specifically designed for the qwen-code agent
- All agents use the DeepSeek V3.1 model for consistent cognitive performance
- Code generation is exclusively handled by the qwen-code CLI agent

### Agent Communication
- Agents communicate through structured prompts
- Prompt templates ensure consistent formatting for qwen-code
- Quality assurance is built into the workflow through validation agents

### Context Engineering
The `context/` directory contains essential guidance artifacts:
- `STYLE_GUIDE.md` - Architectural style guide for Godot/GDScript
- `RULES.md` - Virtual constitution with strict principles
- `TEMPLATES/` - Scaffolding templates for common file types
- `GOLD_STANDARDS/` - Curated examples of perfect implementations

### Workflow Process
The system operates in "bolts" - intense work cycles that follow this sequence:
1. **Targeting** - Select atomic task from backlog
2. **Analysis** - Code Analyst examines source files
3. **Generation** - Refactoring Specialist creates Godot files using qwen-code
4. **Testing** - Test Generator creates unit tests
5. **Validation** - Validation Engineer runs tests
6. **Review** - Successful tasks are packaged for human review

## Key Files

### Agent Configuration
- `converter/agents/` - Contains agent definitions and configurations
- All agents are powered by DeepSeek V3.1 for consistent cognitive performance

### Prompt Templates
- `converter/tasks/task_templates/qwen_prompt_templates.py` - Contains structured prompt templates specifically designed for qwen-code

### CLI Tools
- `converter/tools/` - Contains wrappers for the qwen-code CLI agent

## Governance and Quality Assurance
The system includes built-in governance mechanisms:
- Automated feedback loops for self-correction
- Circuit breaker pattern for intractable problems
- Integrated security scanning
- Comprehensive logging and monitoring

The system is designed with strategic human oversight:
- Upfront strategy and context engineering
- Expert review of AI-generated pull requests
- Edge case intervention for complex problems
- Final authorization for merging changes

## Development Tooling

### Modern Python Tooling
The project now uses industry-standard Python development tools:
- **pyproject.toml** - Modern Python project configuration
- **uv** - Ultra-fast Python package installer and resolver
- **pytest** - Testing framework with comprehensive coverage
- **black** - Code formatter for consistent style
- **flake8** - Linting for code quality
- **mypy** - Static type checking
- **isort** - Import sorting

### Testing
The project includes a comprehensive test suite:
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=converter

# Run specific test module
pytest converter/tests/test_agents.py
```

### Code Quality
```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 .

# Type check
mypy .
```

## Recent Improvements

### Enhanced Security
- Sensitive configuration values are now loaded from environment variables
- Configuration manager properly secures API keys and other secrets
- No hardcoded credentials in configuration files

### Comprehensive Test Coverage
- Added unit tests for all major components
- Test infrastructure with proper mocking and fixtures
- Continuous integration ready test suite

### Professional Python Packaging
- Modern `pyproject.toml` based packaging
- Proper CLI entry points for helper scripts
- Development and production dependency separation
- Industry-standard project structure

### Improved Code Quality
- Consistent code formatting with Black
- Proper import organization with isort
- Linting with flake8 for code quality
- Static type checking with mypy
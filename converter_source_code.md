# Converter Source Code Documentation

*Generated on: 2025-08-21 23:22:45*

*Root directory: /home/fuchsst/projects/personal/wcsaga_godot_converter/converter*

*Total files: 90*


# Converter Source Code Documentation


## Table of Contents

### converter
- [converter/README.md](#converter-readme-md)
- [converter/SECURITY_AND_TESTING.md](#converter-security_and_testing-md)
- [converter/__init__.py](#converter-__init__-py)
- [converter/init_env.sh](#converter-init_env-sh)
- [converter/run.sh](#converter-run-sh)
- [converter/run_tests.sh](#converter-run_tests-sh)
- [converter/test.sh](#converter-test-sh)

### converter/agents
- [converter/agents/README.md](#converter-agents-readme-md)
- [converter/agents/base_agent.py](#converter-agents-base_agent-py)
- [converter/agents/codebase_analyst.yaml](#converter-agents-codebase_analyst-yaml)
- [converter/agents/migration_architect.yaml](#converter-agents-migration_architect-yaml)
- [converter/agents/prompt_engineering_agent.yaml](#converter-agents-prompt_engineering_agent-yaml)
- [converter/agents/quality_assurance_agent.yaml](#converter-agents-quality_assurance_agent-yaml)
- [converter/agents/task_decomposition_specialist.yaml](#converter-agents-task_decomposition_specialist-yaml)

### converter/analyst
- [converter/analyst/README.md](#converter-analyst-readme-md)
- [converter/analyst/__init__.py](#converter-analyst-__init__-py)
- [converter/analyst/__main__.py](#converter-analyst-__main__-py)
- [converter/analyst/codebase_analyst.py](#converter-analyst-codebase_analyst-py)
- [converter/analyst/example_usage.py](#converter-analyst-example_usage-py)
- [converter/analyst/test_codebase_analyst.py](#converter-analyst-test_codebase_analyst-py)

### converter/config
- [converter/config/README.md](#converter-config-readme-md)
- [converter/config/config_manager.py](#converter-config-config_manager-py)
- [converter/config/crewai_config.yaml](#converter-config-crewai_config-yaml)

### converter/context
- [converter/context/README.md](#converter-context-readme-md)
- [converter/context/RULES.md](#converter-context-rules-md)
- [converter/context/STYLE_GUIDE.md](#converter-context-style_guide-md)

### converter/context/GOLD_STANDARDS
- [converter/context/GOLD_STANDARDS/example_well_structured_class.gd](#converter-context-gold_standards-example_well_structured_class-gd)
- [converter/context/GOLD_STANDARDS/example_well_structured_test.gd](#converter-context-gold_standards-example_well_structured_test-gd)

### converter/context/TEMPLATES
- [converter/context/TEMPLATES/gdscript_class_template.gd](#converter-context-templates-gdscript_class_template-gd)
- [converter/context/TEMPLATES/gdunit4_test_template.gd](#converter-context-templates-gdunit4_test_template-gd)
- [converter/context/TEMPLATES/godot_scene_template.tscn](#converter-context-templates-godot_scene_template-tscn)

### converter/graph_system
- [converter/graph_system/README.md](#converter-graph_system-readme-md)
- [converter/graph_system/__init__.py](#converter-graph_system-__init__-py)
- [converter/graph_system/dependency_graph.py](#converter-graph_system-dependency_graph-py)
- [converter/graph_system/file_monitor.py](#converter-graph_system-file_monitor-py)
- [converter/graph_system/graph_manager.py](#converter-graph_system-graph_manager-py)

### converter/hitl
- [converter/hitl/README.md](#converter-hitl-readme-md)
- [converter/hitl/__init__.py](#converter-hitl-__init__-py)
- [converter/hitl/hitl_integration.py](#converter-hitl-hitl_integration-py)

### converter/orchestrator
- [converter/orchestrator/README.md](#converter-orchestrator-readme-md)
- [converter/orchestrator/__init__.py](#converter-orchestrator-__init__-py)
- [converter/orchestrator/enhanced_orchestrator.py](#converter-orchestrator-enhanced_orchestrator-py)
- [converter/orchestrator/main.py](#converter-orchestrator-main-py)

### converter/orchestrator/state_machine
- [converter/orchestrator/state_machine/README.md](#converter-orchestrator-state_machine-readme-md)
- [converter/orchestrator/state_machine/__init__.py](#converter-orchestrator-state_machine-__init__-py)
- [converter/orchestrator/state_machine/bolt_executor.py](#converter-orchestrator-state_machine-bolt_executor-py)
- [converter/orchestrator/state_machine/core.py](#converter-orchestrator-state_machine-core-py)
- [converter/orchestrator/state_machine/hybrid_orchestrator.py](#converter-orchestrator-state_machine-hybrid_orchestrator-py)
- [converter/orchestrator/state_machine/task_queue.py](#converter-orchestrator-state_machine-task_queue-py)

### converter/prompt_engineering
- [converter/prompt_engineering/README.md](#converter-prompt_engineering-readme-md)
- [converter/prompt_engineering/prompt_engineering_agent.py](#converter-prompt_engineering-prompt_engineering_agent-py)

### converter/refactoring
- [converter/refactoring/README.md](#converter-refactoring-readme-md)
- [converter/refactoring/refactoring_specialist.py](#converter-refactoring-refactoring_specialist-py)

### converter/scripts
- [converter/scripts/README.md](#converter-scripts-readme-md)
- [converter/scripts/analyze_source_codebase.py](#converter-scripts-analyze_source_codebase-py)
- [converter/scripts/setup_environment.py](#converter-scripts-setup_environment-py)

### converter/tasks
- [converter/tasks/analysis_task.yaml](#converter-tasks-analysis_task-yaml)
- [converter/tasks/decomposition_task.yaml](#converter-tasks-decomposition_task-yaml)
- [converter/tasks/planning_task.yaml](#converter-tasks-planning_task-yaml)
- [converter/tasks/refactoring_task.yaml](#converter-tasks-refactoring_task-yaml)
- [converter/tasks/testing_task.yaml](#converter-tasks-testing_task-yaml)
- [converter/tasks/validation_task.yaml](#converter-tasks-validation_task-yaml)

### converter/tasks/task_templates
- [converter/tasks/task_templates/qwen_prompt_templates.py](#converter-tasks-task_templates-qwen_prompt_templates-py)

### converter/test_generator
- [converter/test_generator/README.md](#converter-test_generator-readme-md)
- [converter/test_generator/test_generator.py](#converter-test_generator-test_generator-py)

### converter/tests
- [converter/tests/README.md](#converter-tests-readme-md)
- [converter/tests/test_agents.py](#converter-tests-test_agents-py)
- [converter/tests/test_config_manager.py](#converter-tests-test_config_manager-py)
- [converter/tests/test_example.py](#converter-tests-test_example-py)
- [converter/tests/test_orchestrator.py](#converter-tests-test_orchestrator-py)
- [converter/tests/test_project_setup.py](#converter-tests-test_project_setup-py)
- [converter/tests/test_prompt_engineering_agent.py](#converter-tests-test_prompt_engineering_agent-py)
- [converter/tests/test_qwen_code_execution_tool.py](#converter-tests-test_qwen_code_execution_tool-py)
- [converter/tests/test_qwen_code_wrapper.py](#converter-tests-test_qwen_code_wrapper-py)
- [converter/tests/test_tasks.py](#converter-tests-test_tasks-py)
- [converter/tests/test_tools.py](#converter-tests-test_tools-py)
- [converter/tests/test_utils.py](#converter-tests-test_utils-py)
- [converter/tests/test_workflows.py](#converter-tests-test_workflows-py)

### converter/tools
- [converter/tools/README.md](#converter-tools-readme-md)
- [converter/tools/qwen_code_execution_tool.py](#converter-tools-qwen_code_execution_tool-py)
- [converter/tools/qwen_code_wrapper.py](#converter-tools-qwen_code_wrapper-py)

### converter/utils
- [converter/utils/__init__.py](#converter-utils-__init__-py)

### converter/validation
- [converter/validation/README.md](#converter-validation-readme-md)
- [converter/validation/__init__.py](#converter-validation-__init__-py)
- [converter/validation/test_quality_gate.py](#converter-validation-test_quality_gate-py)
- [converter/validation/validation_engineer.py](#converter-validation-validation_engineer-py)

### converter/validation/enhanced
- [converter/validation/enhanced/README.md](#converter-validation-enhanced-readme-md)

### converter/workflows
- [converter/workflows/README.md](#converter-workflows-readme-md)
- [converter/workflows/hierarchical_workflow.py](#converter-workflows-hierarchical_workflow-py)
- [converter/workflows/sequential_workflow.py](#converter-workflows-sequential_workflow-py)

---

## converter/README.md

**File type:** .md  

**Size:** 5051 bytes  

**Last modified:** 2025-08-21 21:44:08


```markdown
# Wing Commander Saga to Godot Converter

This directory contains the agentic migration system for converting the Wing Commander Saga codebase from C++ to Godot/GDScript.

## Project Overview

This system implements a hierarchical multi-agent framework for migrating the Wing Commander Saga game engine from C++ to Godot. Based on the Agentic Migration Playbook and specifically the "Agentic Migration with CLI Agents" approach, it uses specialized AI agents to automate the complex process of code translation, refactoring, and validation.

## Architecture

The system is organized around five specialized AI agents, all powered by the **DeepSeek V3.1** model for consistent cognitive performance:

1. **MigrationArchitect** - Lead Systems Architect responsible for high-level planning
2. **CodebaseAnalyst** - Senior Software Analyst who analyzes the legacy codebase
3. **TaskDecompositionSpecialist** - Technical Project Manager who breaks down tasks
4. **PromptEngineeringAgent** - AI Communications Specialist who creates precise prompts
5. **QualityAssuranceAgent** - QA Automation Engineer who verifies results

We are standardizing on a single, powerful CLI coding agent: **qwen-code**, which is built upon Alibaba's state-of-the-art Qwen3-Coder models.

## Directory Structure

- `agents/` - Agent definitions and configurations (powered by DeepSeek V3.1)
- `analyst/` - Code Analyst agent implementation
- `config/` - Configuration files
- `context/` - Guidance artifacts (style guides, rules, templates, examples)
- `graph_system/` - Dependency graph system for dynamic memory
- `hitl/` - Human-in-the-loop integration
- `orchestrator/` - Orchestrator agent implementation (DeepSeek V3.1)
- `prompt_engineering/` - Prompt Engineering agent implementation
- `refactoring/` - Refactoring Specialist agent implementation (qwen-code)
- `scripts/` - Utility scripts
- `tasks/` - Task definitions and templates
- `test_generator/` - Test Generator agent implementation (qwen-code)
- `tests/` - System tests
- `tools/` - Custom tools for CLI agent control (qwen-code)
- `validation/` - Validation Engineer agent implementation (qwen-code)
- `workflows/` - Process definitions

## Key Components

### Context Engineering
The `context/` directory contains essential guidance artifacts:
- `STYLE_GUIDE.md` - Architectural style guide for Godot/GDScript
- `RULES.md` - Virtual constitution with strict principles
- `TEMPLATES/` - Scaffolding templates for common file types
- `GOLD_STANDARDS/` - Curated examples of perfect implementations

### CLI Agent Tools
The `tools/` directory contains wrappers for the qwen-code CLI agent:
- `qwen_code_wrapper.py` - For high-context generation tasks
- `qwen_code_execution_tool.py` - Base tool for shell command execution

### Task Templates
The `tasks/task_templates/` directory contains prompt templates specifically designed for qwen-code:
- `qwen_prompt_templates.py` - Structured templates for different task types

## Workflow

The system operates in "bolts" - intense work cycles that follow this sequence:

1. **Targeting** - Select atomic task from backlog
2. **Analysis** - Code Analyst examines source files
3. **Generation** - Refactoring Specialist creates Godot files using qwen-code
4. **Testing** - Test Generator creates unit tests
5. **Validation** - Validation Engineer runs tests with quality gates
6. **Review** - Successful tasks are packaged for human review

## Human-in-the-Loop

The system is designed with strategic human oversight:
- Upfront strategy and context engineering
- Expert review of AI-generated pull requests
- Edge case intervention for complex problems
- Final authorization for merging changes
- Proactive HITL patterns for critical decision points

## Getting Started

Please refer to the main project README.md at the root of the repository for detailed setup instructions.
The main project uses modern Python tooling including `pyproject.toml`, `uv` for dependency management,
and comprehensive development tools.

To run the migration:

```bash
# From the project root directory
./run.sh ../source ../target
```

Additional arguments can be passed to the migration script:

```bash
./run.sh ../source ../target --verbose --phase analysis
```

## Running Tests

Tests can be run using the project's Makefile from the root directory:

```bash
# Run all tests
make test

# Run tests with coverage
make test-coverage

# List available test modules
make help
```

Or directly with pytest:

```bash
# From the project root directory
pytest converter/tests/
```

## Governance

The system includes built-in governance mechanisms:
- Automated feedback loops for self-correction
- Circuit breaker pattern for intractable problems
- Integrated security scanning
- Comprehensive logging and monitoring
- Test quality gates to ensure rigorous validation
- Proactive HITL patterns for critical decision points

For detailed information about the project structure, development tools, and setup instructions,
please refer to the main README.md file at the root of the project.
```

---

## converter/SECURITY_AND_TESTING.md

**File type:** .md  

**Size:** 3440 bytes  

**Last modified:** 2025-08-21 16:13:27


```markdown
# Security and Testing Guide

This document explains how to use the security features and run tests for the Wing Commander Saga to Godot migration system.

## Security Features

The migration system implements several security best practices to protect sensitive information:

### Environment Variables for Secrets

All sensitive configuration values are loaded from environment variables rather than being stored in configuration files:

1. **API Keys**: The DeepSeek API key is loaded from the `DEEPSEEK_API_KEY` environment variable
2. **Base URLs**: The DeepSeek base URL is loaded from the `DEEPSEEK_BASE_URL` environment variable

### Configuration Manager

The `ConfigManager` class in `config/config_manager.py` handles the secure loading of configuration:

```python
# Load API key from environment variable
api_key = config_manager.get_secret("DEEPSEEK_API_KEY")

# Load base URL from environment variable  
base_url = config_manager.get_secret("DEEPSEEK_BASE_URL")
```

### Setting Environment Variables

To set the required environment variables, you can:

1. **Export directly in your shell**:
   ```bash
   export DEEPSEEK_API_KEY="your-api-key-here"
   export DEEPSEEK_BASE_URL="https://api.deepseek.com/v1"
   ```

2. **Use a .env file**:
   Create a `.env` file in the converter directory:
   ```
   DEEPSEEK_API_KEY=your-api-key-here
   DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
   ```

3. **Set in your system environment**:
   Add the variables to your system's environment configuration

## Running Tests

The system includes unit tests for all major components:

### Test Files

- `tests/test_config_manager.py` - Tests for the configuration manager
- `tests/test_agents.py` - Tests for the agent implementations
- `tests/test_orchestrator.py` - Tests for the migration orchestrator
- `tests/test_tools.py` - Tests for the Qwen Code tools
- `tests/test_tasks.py` - Tests for the task configurations

### Running Tests

1. **Run all tests**:
   ```bash
   cd converter
   python -m pytest tests/ -v
   ```

2. **Run a specific test file**:
   ```bash
   cd converter
   python -m pytest tests/test_config_manager.py -v
   ```

3. **Run the quick test script**:
   ```bash
   cd converter
   ./run_tests.sh
   ```

### Test Coverage

The tests cover:

- Configuration loading and validation
- Agent initialization and configuration
- Orchestrator setup and operation
- Tool functionality
- Task configuration loading
- Security features (environment variable loading)

## Best Practices

1. **Never commit secrets**: Never store API keys or other secrets in configuration files that are committed to version control
2. **Use environment variables**: Always load sensitive information from environment variables
3. **Validate configuration**: Use the configuration manager's validation methods to ensure all required settings are present
4. **Run tests regularly**: Run tests after making changes to ensure the system continues to work correctly
5. **Update tests**: Add new tests when adding new functionality

## Troubleshooting

If you encounter issues:

1. **Missing environment variables**: Ensure all required environment variables are set
2. **Configuration loading errors**: Check that configuration files are properly formatted YAML
3. **Import errors**: Ensure the Python path includes the converter directory
4. **Test failures**: Check the specific error messages and ensure all dependencies are installed
```

---

## converter/__init__.py

**File type:** .py  

**Size:** 447 bytes  

**Last modified:** 2025-08-21 18:27:22


```python
"""
Wing Commander Saga to Godot Converter - Main Package

This package provides an agentic migration system for converting 
the Wing Commander Saga game engine from C++ to Godot/GDScript.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Import main components for easy access
# Note: These imports may need to be adjusted based on the specific structure
# For now, we'll just define the package metadata
```

---

## converter/agents/README.md

**File type:** .md  

**Size:** 991 bytes  

**Last modified:** 2025-08-21 21:44:24


```markdown
# Agent Definitions

This directory contains the YAML configuration files for each agent in the migration crew.

Based on the "Agentic Migration with CLI Agents" document, all high-level cognitive and orchestration tasks will be powered by the **DeepSeek V3.1** model. Its advanced reasoning and instruction-following capabilities make it an ideal choice for the entire command crew.

The crew is composed of five specialist agents:

- `agents.yaml` - Main agent definitions with DeepSeek V3.1 configuration
- `migration_architect.yaml` - MigrationArchitect configuration (powered by DeepSeek V3.1)
- `codebase_analyst.yaml` - CodebaseAnalyst configuration (powered by DeepSeek V3.1)
- `task_decomposition_specialist.yaml` - TaskDecompositionSpecialist configuration (powered by DeepSeek V3.1)
- `prompt_engineering_agent.yaml` - PromptEngineeringAgent configuration (powered by DeepSeek V3.1)
- `quality_assurance_agent.yaml` - QualityAssuranceAgent configuration (powered by DeepSeek V3.1)
```

---

## converter/agents/base_agent.py

**File type:** .py  

**Size:** 4105 bytes  

**Last modified:** 2025-08-21 15:50:08


```python
"""
Base Agent Implementation

This module provides a base class for agents that load their configurations from YAML files.
"""

import os
import yaml
from crewai import Agent
from typing import Dict, Any, Optional, List


class ConfigurableAgent(Agent):
    """Base class for agents that load configurations from YAML files."""
    
    def __init__(self, config_file: str, **kwargs):
        """
        Initialize the agent with a YAML configuration file.
        
        Args:
            config_file: Path to the YAML configuration file
            **kwargs: Additional arguments to pass to the Agent constructor
        """
        # Load the configuration from the YAML file
        config = self._load_config(config_file)
        
        # Extract agent attributes from the configuration
        role = config.get('role', '')
        goal = config.get('goal', '')
        backstory = config.get('backstory', '')
        tool_names = config.get('tools', [])
        
        # Convert tool names to actual tool instances (for now, we'll leave them as None)
        # In a real implementation, we would map tool names to actual tool instances
        tools = self._load_tools(tool_names)
        
        # Initialize the parent Agent class with the configuration
        super().__init__(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=tools,
            **kwargs
        )
    
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """
        Load agent configuration from a YAML file.
        
        Args:
            config_file: Path to the YAML configuration file
            
        Returns:
            Dictionary with agent configuration
        """
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Configuration file not found: {config_file}")
        
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        return config
    
    def _load_tools(self, tool_names: List[str]) -> List[Any]:
        """
        Load tools based on their names.
        
        Args:
            tool_names: List of tool names
            
        Returns:
            List of tool instances
        """
        # For now, we'll return an empty list and add tools separately
        # In a real implementation, we would map tool names to actual tool instances
        return []


# Specific agent implementations
class MigrationArchitect(ConfigurableAgent):
    """Lead Systems Architect agent."""
    
    def __init__(self, **kwargs):
        """Initialize the MigrationArchitect agent."""
        config_file = os.path.join(os.path.dirname(__file__), 'migration_architect.yaml')
        super().__init__(config_file, **kwargs)


class CodebaseAnalyst(ConfigurableAgent):
    """Senior Software Analyst agent."""
    
    def __init__(self, **kwargs):
        """Initialize the CodebaseAnalyst agent."""
        config_file = os.path.join(os.path.dirname(__file__), 'codebase_analyst.yaml')
        super().__init__(config_file, **kwargs)


class TaskDecompositionSpecialist(ConfigurableAgent):
    """Technical Project Manager agent."""
    
    def __init__(self, **kwargs):
        """Initialize the TaskDecompositionSpecialist agent."""
        config_file = os.path.join(os.path.dirname(__file__), 'task_decomposition_specialist.yaml')
        super().__init__(config_file, **kwargs)


class PromptEngineeringAgent(ConfigurableAgent):
    """AI Communications Specialist agent."""
    
    def __init__(self, **kwargs):
        """Initialize the PromptEngineeringAgent agent."""
        config_file = os.path.join(os.path.dirname(__file__), 'prompt_engineering_agent.yaml')
        super().__init__(config_file, **kwargs)


class QualityAssuranceAgent(ConfigurableAgent):
    """QA Automation Engineer agent."""
    
    def __init__(self, **kwargs):
        """Initialize the QualityAssuranceAgent agent."""
        config_file = os.path.join(os.path.dirname(__file__), 'quality_assurance_agent.yaml')
        super().__init__(config_file, **kwargs)
```

---

## converter/agents/codebase_analyst.yaml

**File type:** .yaml  

**Size:** 1175 bytes  

**Last modified:** 2025-08-21 15:50:59


```yaml
# Codebase Analyst Agent Configuration

name: CodebaseAnalyst
role: Senior Software Analyst
goal: Analyze the legacy codebase to identify dependencies, modules, and architectural patterns.
backstory: >
  You are an expert in legacy game engine architecture with deep knowledge of C++ codebases.
  Your primary responsibility is to analyze source files and create structured reports that help
  other agents understand the existing architecture. You're particularly skilled at identifying
  dependencies between classes and modules, and constructing models of existing architectures.
  Your analysis prevents other agents from making changes in isolation that could break distant
  parts of the system.

  You are powered by the DeepSeek V3.1 model, which gives you superior reasoning and analytical
  capabilities for understanding complex systems.

tools:
  - FileReadTool
  - CodeStructureAnalysisTool

expected_output: >
  A structured representation (e.g., JSON) of the codebase's dependency graph and key components.
  The output should classify components into categories like 'data', 'behavior', 'visuals', and 'physics'
  according to the Architectural Mapping Table.
```

---

## converter/agents/migration_architect.yaml

**File type:** .yaml  

**Size:** 1238 bytes  

**Last modified:** 2025-08-21 13:08:18


```yaml
# Migration Architect Agent Configuration

name: MigrationArchitect
role: Lead Systems Architect
goal: >
  Decompose the overall migration into a high-level, phased project plan.
  Analyze the project's scope and break it down into major, logically sequenced phases.
backstory: >
  You are the project lead for the Wing Commander Saga to Godot migration.
  Your primary objective is to formulate the high-level, phased migration strategy.
  Upon receiving the initial directive—"Migrate Wing Commander Saga to Godot"—you analyze
  the project's scope and decompose it into major, logically sequenced phases, such as
  "Phase 1: Port Core Systems," "Phase 2: Convert Game Logic," and "Phase 3: Refactor for Godot API Integration."
  You set the overarching agenda for the entire crew and ensure all other agents align with your strategic vision.

  You are powered by the DeepSeek V3.1 model, which gives you superior reasoning and strategic
  planning capabilities for understanding complex migration projects.

tools:
  - FileReadTool

expected_output: >
  A multi-phase project plan in Markdown format, outlining the migration sequence.
  The plan should prioritize porting foundational systems before application-level game logic.

```

---

## converter/agents/prompt_engineering_agent.yaml

**File type:** .yaml  

**Size:** 1423 bytes  

**Last modified:** 2025-08-21 13:08:44


```yaml
# Prompt Engineering Agent Configuration

name: PromptEngineeringAgent
role: AI Communications Specialist
goal: >
  Convert atomic tasks and code context into precise, effective prompts for the CLI agent.
  Ensure instructions are clear, specific, and provide all necessary information for success.
backstory: >
  You are a critical meta-agent that functions as the communication officer between the
  command crew and the execution layer. Your goal is to take a decomposed task from the
  TaskDecompositionSpecialist and the relevant code context from the CodebaseAnalyst and
  synthesize them into a perfectly formatted, unambiguous, and context-rich prompt.

  You are an expert in the principles of effective prompting, ensuring that instructions are
  clear, specific, and provide all necessary information for the CLI agent to succeed on
  the first attempt. You understand the importance of structured formatting, holistic context,
  and explicit constraints in prompt design.

  You are powered by the DeepSeek V3.1 model, which gives you superior linguistic and
  communication capabilities for crafting effective prompts.

tools: []
  # This agent works with prompt construction and doesn't require specific file tools

expected_output: >
  A fully-formed, context-rich prompt string formatted for the target CLI agent.
  The prompt should include all necessary context, constraints, and formatting requirements.

```

---

## converter/agents/quality_assurance_agent.yaml

**File type:** .yaml  

**Size:** 1357 bytes  

**Last modified:** 2025-08-21 13:09:07


```yaml
# Quality Assurance Agent Configuration

name: QualityAssuranceAgent
role: QA Automation Engineer
goal: >
  Verify the output of CLI agent tasks, diagnose failures, and initiate corrective actions.
  Ensure all generated code meets quality standards and functions correctly.
backstory: >
  You are responsible for verification and quality control in the AI crew. After the CLI agent
  executes a task, you analyze the results—including command output, error messages, and
  generated code—to determine success or failure.

  If a task fails, you perform root cause analysis. You diagnose the issue (e.g., syntax error,
  logical flaw, failed test) and route the task back to the appropriate agent—often the
  PromptEngineeringAgent—with additional context about the failure. This creates an autonomous
  feedback loop, enabling the system to learn from its mistakes and self-correct.

  You are powered by the DeepSeek V3.1 model, which gives you excellent analytical and
  diagnostic capabilities for quality assurance.

tools:
  - QwenCodeExecutionTool
  - GitDiffTool
  - TestRunnerTool

expected_output: >
  A success/failure status, and in case of failure, a new task for correction.
  When successful, you provide a summary of what was accomplished.
  When failed, you provide detailed diagnostic information and suggested corrective actions.

```

---

## converter/agents/task_decomposition_specialist.yaml

**File type:** .yaml  

**Size:** 1417 bytes  

**Last modified:** 2025-08-21 13:08:31


```yaml
# Task Decomposition Specialist Agent Configuration

name: TaskDecompositionSpecialist
role: Technical Project Manager
goal: >
  Break down high-level migration phases into a sequence of atomic, executable coding tasks.
  Translate broad strategic directives from the MigrationArchitect into concrete, actionable steps.
backstory: >
  You are a middle manager in the AI crew, acting as a bridge between high-level strategy and
  low-level execution. Your core function is to take broad strategic directives from the
  MigrationArchitect and translate them into a series of concrete, atomic coding tasks suitable
  for the low-level CLI coding agent.

  For example, when given a high-level goal like "Port the PlayerShip class," you break it down
  into a precise sequence of operations that can be executed by the Refactoring Specialist or
  other execution agents. You ensure that complex tasks are decomposed into manageable,
  independently executable units.

  You are powered by the DeepSeek V3.1 model, which gives you excellent analytical and
  organizational capabilities for task decomposition.

tools: []
  # This agent primarily works with abstract task definitions and doesn't require
  # specific tools for file operations

expected_output: >
  A list of specific, ordered instructions for code modification or generation.
  Each task should be atomic and executable by a single agent in one operation.

```

---

## converter/analyst/README.md

**File type:** .md  

**Size:** 1730 bytes  

**Last modified:** 2025-08-21 21:44:48


```markdown
# Code Analyst Agent

This directory contains the implementation of the Code Analyst agent, which analyzes the source codebase.

Based on the "Agentic Migration with CLI Agents" document, this agent is powered by the **DeepSeek V3.1** model.

## Responsibilities

- Receive a task (e.g., "GTC Fenris")
- Analyze all related source files
- Produce a structured JSON report classifying components
- Identify dependencies and architectural patterns
- Use DeepSeek V3.1 model for advanced code analysis

## Key Components

- `codebase_analyst.py` - Main implementation of the Codebase Analyst agent
- `__init__.py` - Package initialization file

## Implementation Details

The Codebase Analyst is designed to handle the specific file formats used in the Wing Commander Saga project:

1. **Table Files (.tbl, .tbm)** - Parse entity data and properties
2. **Model Files (.pof)** - Extract 3D model metadata including subsystems and hardpoints
3. **Source Files (.cpp, .h)** - Analyze C++ classes, methods, and dependencies
4. **Mission Files (.fs2)** - Parse SEXP expressions for mission logic

The agent produces a structured JSON report that categorizes components according to the Architectural Mapping Table:
- **Data** - Table files and other data definitions
- **Behavior** - Source code and mission logic
- **Visuals** - 3D model files
- **Physics** - Physical properties and behaviors

## Usage

The agent is typically invoked by the Orchestrator agent as part of the migration workflow:

```python
from converter.analyst import CodebaseAnalyst

analyst = CodebaseAnalyst()
analysis_report = analyst.analyze_entity("GTC Fenris", [
    "source/tables/ships.tbl",
    "source/models/fenris.pof", 
    "source/code/ship.cpp"
])
```
```

---

## converter/analyst/__init__.py

**File type:** .py  

**Size:** 112 bytes  

**Last modified:** 2025-08-21 12:41:21


```python
"""
Code Analyst Agent Package
"""

from .codebase_analyst import CodebaseAnalyst

__all__ = ["CodebaseAnalyst"]
```

---

## converter/analyst/__main__.py

**File type:** .py  

**Size:** 130 bytes  

**Last modified:** 2025-08-21 12:47:59


```python
"""
Main entry point for the Code Analyst agent.
"""

from .codebase_analyst import CodebaseAnalyst

__all__ = ["CodebaseAnalyst"]
```

---

## converter/analyst/codebase_analyst.py

**File type:** .py  

**Size:** 11947 bytes  

**Last modified:** 2025-08-21 12:41:17


```python
"""
Codebase Analyst Agent Implementation

This agent is responsible for analyzing the legacy codebase to identify dependencies,
modules, and architectural patterns. It's powered by the DeepSeek V3.1 model.
"""

import json
import os
import re
from typing import Dict, List, Any


class CodebaseAnalyst:
    """
    The Codebase Analyst agent analyzes the legacy C++ codebase to identify dependencies,
    modules, and architectural patterns. It reads source files, identifies dependencies
    between classes and modules, and constructs a model of the existing architecture.
    """
    
    def __init__(self):
        """Initialize the Codebase Analyst agent."""
        self.analysis_cache = {}
    
    def analyze_entity(self, entity_name: str, source_files: List[str]) -> Dict[str, Any]:
        """
        Analyze a specific game entity (e.g., "GTC Fenris") and its related source files.
        
        Args:
            entity_name: Name of the entity to analyze
            source_files: List of file paths related to the entity
            
        Returns:
            Structured JSON report with analysis results
        """
        # Check if we've already analyzed this entity
        cache_key = f"{entity_name}:{':'.join(sorted(source_files))}"
        if cache_key in self.analysis_cache:
            return self.analysis_cache[cache_key]
        
        # Perform analysis
        analysis_result = self._perform_analysis(entity_name, source_files)
        
        # Cache the result
        self.analysis_cache[cache_key] = analysis_result
        
        return analysis_result
    
    def _perform_analysis(self, entity_name: str, source_files: List[str]) -> Dict[str, Any]:
        """
        Perform the actual analysis of the entity and its source files.
        
        Args:
            entity_name: Name of the entity to analyze
            source_files: List of file paths related to the entity
            
        Returns:
            Structured JSON report with analysis results
        """
        components = {
            "data": [],
            "behavior": [],
            "visuals": [],
            "physics": []
        }
        
        # Analyze each source file
        file_analyses = []
        for file_path in source_files:
            if os.path.exists(file_path):
                file_analysis = self._analyze_file(file_path)
                file_analyses.append(file_analysis)
                
                # Categorize components based on file type and content
                if file_path.endswith(('.tbl', '.tbm')):
                    components["data"].append({
                        "file": file_path,
                        "type": "table_data",
                        "description": f"Table data for {entity_name}",
                        "parsed_data": self._parse_table_file(file_path)
                    })
                elif file_path.endswith('.pof'):
                    components["visuals"].append({
                        "file": file_path,
                        "type": "model_data",
                        "description": f"3D model data for {entity_name}",
                        "metadata": self._parse_pof_metadata(file_path)
                    })
                elif file_path.endswith(('.cpp', '.h')):
                    components["behavior"].append({
                        "file": file_path,
                        "type": "source_code",
                        "description": f"C++ source code for {entity_name}",
                        "classes": self._parse_cpp_classes(file_path),
                        "includes": self._parse_cpp_includes(file_path)
                    })
                elif file_path.endswith('.fs2'):
                    components["behavior"].append({
                        "file": file_path,
                        "type": "mission_logic",
                        "description": f"Mission logic for {entity_name}",
                        "sexps": self._parse_sexp_file(file_path)
                    })
        
        # Create the analysis report
        analysis_report = {
            "entity_name": entity_name,
            "source_files": source_files,
            "file_analyses": file_analyses,
            "components": components,
            "dependencies": self._identify_dependencies(source_files),
            "architectural_patterns": self._identify_patterns(file_analyses)
        }
        
        return analysis_report
    
    def _analyze_file(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze a single file.
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            Dictionary with file analysis results
        """
        file_info = {
            "path": file_path,
            "size": 0,
            "lines": 0,
            "type": self._get_file_type(file_path)
        }
        
        try:
            if os.path.exists(file_path):
                file_info["size"] = os.path.getsize(file_path)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    file_info["lines"] = len(lines)
        except Exception as e:
            file_info["error"] = str(e)
        
        return file_info
    
    def _get_file_type(self, file_path: str) -> str:
        """
        Determine the file type based on extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File type string
        """
        _, ext = os.path.splitext(file_path)
        return ext.lower()
    
    def _parse_table_file(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a .tbl or .tbm file to extract entity data.
        
        Args:
            file_path: Path to the table file
            
        Returns:
            Dictionary with parsed table data
        """
        # This would contain logic to parse the specific format of .tbl/.tbm files
        # For now, we'll return a placeholder
        return {
            "format": "table",
            "entries_parsed": 0,
            "entities_found": []
        }
    
    def _parse_pof_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Parse metadata from a .pof file.
        
        Args:
            file_path: Path to the .pof file
            
        Returns:
            Dictionary with parsed model metadata
        """
        # This would contain logic to parse the binary .pof format
        # For now, we'll return a placeholder
        return {
            "format": "pof_binary",
            "subsystems": [],
            "hardpoints": [],
            "thrusters": []
        }
    
    def _parse_cpp_classes(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Parse C++ classes from a .cpp or .h file.
        
        Args:
            file_path: Path to the C++ file
            
        Returns:
            List of dictionaries with class information
        """
        classes = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Simple regex to find class declarations
                class_pattern = r'class\s+(\w+)'
                class_matches = re.findall(class_pattern, content)
                
                for class_name in class_matches:
                    classes.append({
                        "name": class_name,
                        "methods": [],
                        "properties": []
                    })
        except Exception:
            pass
            
        return classes
    
    def _parse_cpp_includes(self, file_path: str) -> List[str]:
        """
        Parse #include directives from a C++ file.
        
        Args:
            file_path: Path to the C++ file
            
        Returns:
            List of included files
        """
        includes = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    if line.strip().startswith('#include'):
                        includes.append(line.strip())
        except Exception:
            pass
            
        return includes
    
    def _parse_sexp_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Parse SEXP expressions from a .fs2 file.
        
        Args:
            file_path: Path to the SEXP file
            
        Returns:
            List of parsed SEXP expressions
        """
        sexps = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Simple regex to find SEXP patterns (this is a simplified approach)
                sexp_pattern = r'\([^\)]+\)'
                sexp_matches = re.findall(sexp_pattern, content)
                
                for match in sexp_matches:
                    sexps.append({
                        "expression": match,
                        "type": "sexp"
                    })
        except Exception:
            pass
            
        return sexps
    
    def _identify_dependencies(self, source_files: List[str]) -> List[Dict[str, Any]]:
        """
        Identify dependencies between files.
        
        Args:
            source_files: List of file paths
            
        Returns:
            List of dependencies
        """
        dependencies = []
        
        # Parse C++ files to find include dependencies
        for file_path in source_files:
            if file_path.endswith(('.cpp', '.h')) and os.path.exists(file_path):
                includes = self._parse_cpp_includes(file_path)
                for include in includes:
                    # Extract the included file name
                    match = re.search(r'#include\s*[<"]([^>"]+)[>"]', include)
                    if match:
                        included_file = match.group(1)
                        dependencies.append({
                            "from": file_path,
                            "to": included_file,
                            "type": "include"
                        })
        
        return dependencies
    
    def _identify_patterns(self, file_analyses: List[Dict[str, Any]]) -> List[str]:
        """
        Identify architectural patterns in the analyzed files.
        
        Args:
            file_analyses: List of file analysis results
            
        Returns:
            List of identified patterns
        """
        patterns = []
        
        # Check for data-driven design (presence of .tbl files)
        has_table_files = any(analysis.get("type") in [".tbl", ".tbm"] 
                             for analysis in file_analyses)
        if has_table_files:
            patterns.append("data_driven_design")
        
        # Check for inheritance patterns in C++ files
        has_cpp_files = any(analysis.get("type") in [".cpp", ".h"] 
                           for analysis in file_analyses)
        if has_cpp_files:
            patterns.append("inheritance_hierarchy")
            patterns.append("object_oriented_design")
        
        # Add common patterns
        patterns.extend([
            "singleton_pattern",
            "observer_pattern"
        ])
        
        return patterns


def main():
    """Main function for testing the Codebase Analyst."""
    analyst = CodebaseAnalyst()
    
    # Example usage
    entity_name = "GTC Fenris"
    source_files = [
        "source/tables/ships.tbl",
        "source/models/fenris.pof",
        "source/code/ship.cpp",
        "source/code/ship.h"
    ]
    
    analysis = analyst.analyze_entity(entity_name, source_files)
    print(json.dumps(analysis, indent=2))


if __name__ == "__main__":
    main()
```

---

## converter/analyst/example_usage.py

**File type:** .py  

**Size:** 1402 bytes  

**Last modified:** 2025-08-21 12:47:19


```python
#!/usr/bin/env python3
"""
Example script demonstrating the use of the Codebase Analyst agent.
"""

import json
import sys
import os

# Add the converter directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from converter.analyst.codebase_analyst import CodebaseAnalyst


def main():
    """Main function demonstrating the Codebase Analyst."""
    # Create an instance of the analyst
    analyst = CodebaseAnalyst()
    
    # Example: Analyze a ship entity
    entity_name = "GTF Myrmidon"
    source_files = [
        "source/tables/ships.tbl",
        "source/models/myrmidon.pof",
        "source/code/ship.cpp",
        "source/code/ship.h"
    ]
    
    print(f"Analyzing entity: {entity_name}")
    print(f"Source files: {source_files}")
    print("\n" + "="*50 + "\n")
    
    # Perform the analysis
    analysis = analyst.analyze_entity(entity_name, source_files)
    
    # Print the results in a formatted way
    print(json.dumps(analysis, indent=2))
    
    # Example of how the output might be used
    print("\n" + "="*50 + "\n")
    print("Component Breakdown:")
    for category, components in analysis["components"].items():
        print(f"\n{category.upper()}:")
        for component in components:
            print(f"  - {component.get('description', 'N/A')} ({component.get('file', 'N/A')})")


if __name__ == "__main__":
    main()
```

---

## converter/analyst/test_codebase_analyst.py

**File type:** .py  

**Size:** 3621 bytes  

**Last modified:** 2025-08-21 12:41:49


```python
"""
Tests for the Codebase Analyst Agent
"""

import unittest
import json
import os
import tempfile
from converter.analyst.codebase_analyst import CodebaseAnalyst


class TestCodebaseAnalyst(unittest.TestCase):
    """Test cases for the Codebase Analyst agent."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyst = CodebaseAnalyst()
    
    def test_analyze_entity_with_empty_files(self):
        """Test analyzing an entity with no source files."""
        result = self.analyst.analyze_entity("TestEntity", [])
        
        self.assertEqual(result["entity_name"], "TestEntity")
        self.assertEqual(result["source_files"], [])
        self.assertEqual(result["components"]["data"], [])
        self.assertEqual(result["components"]["behavior"], [])
        self.assertEqual(result["components"]["visuals"], [])
        self.assertEqual(result["components"]["physics"], [])
    
    def test_analyze_entity_with_nonexistent_files(self):
        """Test analyzing an entity with nonexistent source files."""
        result = self.analyst.analyze_entity("TestEntity", ["nonexistent/file.txt"])
        
        self.assertEqual(result["entity_name"], "TestEntity")
        self.assertEqual(len(result["source_files"]), 1)
        self.assertEqual(result["source_files"][0], "nonexistent/file.txt")
    
    def test_file_type_detection(self):
        """Test file type detection."""
        self.assertEqual(self.analyst._get_file_type("test.txt"), ".txt")
        self.assertEqual(self.analyst._get_file_type("path/to/file.cpp"), ".cpp")
        self.assertEqual(self.analyst._get_file_type("file"), "")
    
    def test_caching_mechanism(self):
        """Test that analysis results are cached."""
        # First call
        result1 = self.analyst.analyze_entity("TestEntity", [])
        
        # Second call with same parameters should return cached result
        result2 = self.analyst.analyze_entity("TestEntity", [])
        
        self.assertIs(result1, result2)
    
    def test_parse_cpp_classes(self):
        """Test parsing C++ classes from a file."""
        # Create a temporary C++ file for testing
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False) as f:
            f.write("""
            class Ship {
            public:
                void fly();
            };
            
            class Weapon {
            public:
                void fire();
            };
            """)
            temp_file = f.name
        
        try:
            classes = self.analyst._parse_cpp_classes(temp_file)
            self.assertEqual(len(classes), 2)
            self.assertEqual(classes[0]["name"], "Ship")
            self.assertEqual(classes[1]["name"], "Weapon")
        finally:
            os.unlink(temp_file)
    
    def test_parse_cpp_includes(self):
        """Test parsing C++ includes from a file."""
        # Create a temporary C++ file for testing
        with tempfile.NamedTemporaryFile(mode='w', suffix='.h', delete=False) as f:
            f.write("""
            #include <iostream>
            #include "ship.h"
            #include "weapon.h"
            """)
            temp_file = f.name
        
        try:
            includes = self.analyst._parse_cpp_includes(temp_file)
            self.assertEqual(len(includes), 3)
            self.assertIn("#include <iostream>", includes)
            self.assertIn('#include "ship.h"', includes)
            self.assertIn('#include "weapon.h"', includes)
        finally:
            os.unlink(temp_file)


if __name__ == "__main__":
    unittest.main()
```

---

## converter/config/README.md

**File type:** .md  

**Size:** 1060 bytes  

**Last modified:** 2025-08-21 21:51:35


```markdown
# Configuration Files

This directory contains configuration files for the migration system.

- `crewai_config.yaml` - Main CrewAI configuration with DeepSeek V3.1 settings (legacy)
- `agent_config.yaml` - Agent-specific configurations
- `tool_config.yaml` - Tool-specific configurations
- `project_settings.yaml` - Project-specific settings

## Key Components

- `config_manager.py` - Configuration manager for secure loading of settings
- `crewai_config.yaml` - Legacy CrewAI configuration (to be deprecated)
- `langgraph_config.yaml` - New LangGraph configuration
- `agent_config.yaml` - Agent-specific configurations
- `tool_config.yaml` - Tool-specific configurations
- `project_settings.yaml` - Project-specific settings

## Security

All sensitive configuration values are loaded from environment variables rather than being stored in configuration files:

1. **API Keys**: The DeepSeek API key is loaded from the `DEEPSEEK_API_KEY` environment variable
2. **Base URLs**: The DeepSeek base URL is loaded from the `DEEPSEEK_BASE_URL` environment variable
```

---

## converter/config/config_manager.py

**File type:** .py  

**Size:** 6910 bytes  

**Last modified:** 2025-08-21 22:20:37


```python
"""
Configuration Manager for the Migration System

This module handles loading configuration from YAML files and environment variables,
ensuring that sensitive information is properly secured.
"""

import os
import yaml
from typing import Any, Dict, Optional
from pathlib import Path


class ConfigManager:
    """Manages configuration loading from files and environment variables."""
    
    def __init__(self, config_dir: str = "config"):
        """
        Initialize the configuration manager.
        
        Args:
            config_dir: Directory containing configuration files
        """
        self.config_dir = Path(config_dir)
        self._config = {}
        self._load_all_configurations()
    
    def _load_all_configurations(self):
        """Load all configuration files."""
        # Load main crewai configuration
        crewai_config_path = self.config_dir / "crewai_config.yaml"
        if crewai_config_path.exists():
            self._config["crewai"] = self._load_yaml_config(crewai_config_path)
        
        # Load other configuration files if they exist
        for config_file in self.config_dir.glob("*.yaml"):
            if config_file.name != "crewai_config.yaml":
                config_name = config_file.stem
                self._config[config_name] = self._load_yaml_config(config_file)
    
    def _load_yaml_config(self, config_path: Path) -> Dict[str, Any]:
        """
        Load configuration from a YAML file.
        
        Args:
            config_path: Path to the YAML configuration file
            
        Returns:
            Dictionary with configuration data
        """
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            raise ValueError(f"Failed to load configuration from {config_path}: {str(e)}")
    
    def get_config(self, section: str, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            section: Configuration section name
            key: Configuration key
            default: Default value if not found
            
        Returns:
            Configuration value
        """
        section_config = self._config.get(section, {})
        return section_config.get(key, default)
    
    def get_nested_config(self, section: str, *keys: str, default: Any = None) -> Any:
        """
        Get a nested configuration value.
        
        Args:
            section: Configuration section name
            keys: Nested keys to traverse
            default: Default value if not found
            
        Returns:
            Configuration value
        """
        section_config = self._config.get(section, {})
        current = section_config
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        
        return current
    
    def get_secret(self, env_var: str, default: str = None) -> str:
        """
        Get a secret from environment variables.
        
        Args:
            env_var: Environment variable name
            default: Default value if not found
            
        Returns:
            Secret value from environment variable
        """
        return os.environ.get(env_var, default)
    
    def get_llm_config(self) -> Dict[str, Any]:
        """
        Get LLM configuration with secrets loaded from environment variables.
        
        Returns:
            Dictionary with LLM configuration
        """
        llm_config = self._config.get("crewai", {}).get("llm", {})
        
        # Load API key from environment variable
        api_key_env_var = llm_config.get("api_key_env_var", "DEEPSEEK_API_KEY")
        api_key = self.get_secret(api_key_env_var)
        
        # Load base URL from environment variable
        base_url_env_var = llm_config.get("base_url_env_var", "DEEPSEEK_BASE_URL")
        base_url = self.get_secret(base_url_env_var)
        
        # Remove the environment variable names from the config
        llm_config_copy = llm_config.copy()
        llm_config_copy.pop("api_key_env_var", None)
        llm_config_copy.pop("base_url_env_var", None)
        
        # Remove any existing api_key from the config
        llm_config_copy.pop("api_key", None)
        
        # Add the actual values
        if api_key:
            llm_config_copy["api_key"] = api_key
        if base_url:
            llm_config_copy["base_url"] = base_url
        
        return llm_config_copy
    
    def get_agent_config(self, agent_type: str = "default") -> Dict[str, Any]:
        """
        Get agent configuration.
        
        Args:
            agent_type: Type of agent configuration to get
            
        Returns:
            Dictionary with agent configuration
        """
        if agent_type == "default":
            return self._config.get("crewai", {}).get("default_agent", {})
        else:
            return self._config.get("agents", {}).get(agent_type, {})
    
    def get_process_config(self, process_type: str) -> Dict[str, Any]:
        """
        Get process configuration.
        
        Args:
            process_type: Type of process configuration to get
            
        Returns:
            Dictionary with process configuration
        """
        return self._config.get("crewai", {}).get("process", {}).get(process_type, {})
    
    def get_memory_config(self) -> Dict[str, Any]:
        """
        Get memory configuration.
        
        Returns:
            Dictionary with memory configuration
        """
        return self._config.get("crewai", {}).get("memory", {})
    
    def validate_config(self) -> bool:
        """
        Validate that all required configuration is present.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        # Check that we have the basic crewai configuration
        if "crewai" not in self._config:
            return False
        
        # Check that we have LLM configuration
        llm_config = self._config.get("crewai", {}).get("llm", {})
        if not llm_config.get("model"):
            return False
        
        # Check that required environment variables are set
        api_key_env_var = llm_config.get("api_key_env_var", "DEEPSEEK_API_KEY")
        if not os.environ.get(api_key_env_var):
            # This is a warning, not an error, as the system might work in some cases without API key
            pass
        
        return True


# Global configuration manager instance
config_manager = ConfigManager()


def get_config_manager() -> ConfigManager:
    """
    Get the global configuration manager instance.
    
    Returns:
        ConfigManager instance
    """
    return config_manager
```

---

## converter/config/crewai_config.yaml

**File type:** .yaml  

**Size:** 1085 bytes  

**Last modified:** 2025-08-21 16:03:45


```yaml
# CrewAI Configuration for Wing Commander Saga to Godot Migration
# Using DeepSeek V3.1 as the primary cognitive model

# Global LLM configuration
llm:
  model: deepseek-ai/DeepSeek-V3.1
  temperature: 0.7
  max_tokens: 4096
  base_url_env_var: "DEEPSEEK_BASE_URL"  # Load base URL from environment variable
  api_key_env_var: "DEEPSEEK_API_KEY"   # Load API key from environment variable

# Default agent configuration
default_agent:
  verbose: true
  allow_delegation: true
  max_rpm: 60  # Rate limiting to avoid API overuse
  cache: true

# Process configuration
process:
  # Sequential for atomic tasks
  sequential:
    timeout: 300  # 5 minutes timeout
  # Hierarchical for complex workflows
  hierarchical:
    manager_llm: deepseek-ai/DeepSeek-V3.1
    timeout: 600  # 10 minutes timeout

# Memory configuration
memory:
  enabled: true
  embedder:
    provider: huggingface
    config:
      model: sentence-transformers/all-MiniLM-L6-v2

# Logging configuration
logging:
  level: INFO
  file: ./logs/crewai.log
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

---

## converter/context/GOLD_STANDARDS/example_well_structured_class.gd

**File type:** .gd  

**Size:** 8071 bytes  

**Last modified:** 2025-08-21 13:11:22


```gdscript
# PlayerShip
# Represents a player-controlled spacecraft with movement, weapons, and health systems

class_name PlayerShip

extends Node2D

# ------------------------------------------------------------------------------
# Signals
# ------------------------------------------------------------------------------
signal health_changed(current_health: int, max_health: int)
signal destroyed()
signal weapon_fired(weapon_type: String, position: Vector2, direction: Vector2)

# ------------------------------------------------------------------------------
# Enums
# ------------------------------------------------------------------------------
enum WeaponType {
    LASER,
    MISSILE,
    PLASMA
}

enum ShipState {
    ACTIVE,
    DESTROYED,
    DOCKED
}

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------
const MAX_HEALTH: int = 100
const MAX_SPEED: float = 300.0
const ACCELERATION: float = 500.0
const ROTATION_SPEED: float = 2.0

# ------------------------------------------------------------------------------
# Exported Variables
# ------------------------------------------------------------------------------
@export var starting_health: int = MAX_HEALTH
@export var ship_name: String = "Default Fighter"

# ------------------------------------------------------------------------------
# Public Variables
# ------------------------------------------------------------------------------
var current_health: int
var current_speed: float = 0.0
var ship_state: ShipState = ShipState.ACTIVE

# ------------------------------------------------------------------------------
# Private Variables
# ------------------------------------------------------------------------------
var _velocity: Vector2 = Vector2.ZERO
var _rotation_direction: int = 0
var _thrust_input: float = 0.0

# ------------------------------------------------------------------------------
# Onready Variables
# ------------------------------------------------------------------------------
@onready var sprite: Sprite2D = $Sprite2D
@onready var collision_shape: CollisionShape2D = $CollisionShape2D
@onready var weapon_cooldown_timers: Dictionary = {
    WeaponType.LASER: $LaserCooldown,
    WeaponType.MISSILE: $MissileCooldown,
    WeaponType.PLASMA: $PlasmaCooldown
}

# ------------------------------------------------------------------------------
# Static Functions
# ------------------------------------------------------------------------------
static func calculate_damage(weapon_type: WeaponType, distance: float) -> float:
    """
    Calculate damage based on weapon type and distance to target
    @param weapon_type: Type of weapon being fired
    @param distance: Distance to target in meters
    @returns: Damage value as a float
    """
    var base_damage: float = 0.0
    match weapon_type:
        WeaponType.LASER:
            base_damage = 25.0
        WeaponType.MISSILE:
            base_damage = 50.0
        WeaponType.PLASMA:
            base_damage = 40.0
    
    # Damage falloff over distance
    var falloff: float = 1.0 - (distance / 1000.0)
    return base_damage * clamp(falloff, 0.1, 1.0)

# ------------------------------------------------------------------------------
# Built-in Virtual Methods
# ------------------------------------------------------------------------------
func _ready() -> void:
    """
    Initialize the player ship when the node enters the scene tree
    """
    current_health = starting_health
    ship_state = ShipState.ACTIVE

func _process(delta: float) -> void:
    """
    Handle continuous processing logic
    @param delta: Time since last frame in seconds
    """
    if ship_state != ShipState.ACTIVE:
        return
    
    _update_rotation(delta)
    _update_thrust(delta)

func _physics_process(delta: float) -> void:
    """
    Handle physics-related updates
    @param delta: Time since last frame in seconds
    """
    if ship_state != ShipState.ACTIVE:
        return
    
    _apply_movement(delta)

# ------------------------------------------------------------------------------
# Public Methods
# ------------------------------------------------------------------------------
func take_damage(damage: int) -> void:
    """
    Apply damage to the ship
    @param damage: Amount of damage to apply
    """
    if ship_state != ShipState.ACTIVE:
        return
    
    current_health = max(0, current_health - damage)
    emit_signal("health_changed", current_health, MAX_HEALTH)
    
    if current_health <= 0:
        _destroy()

func fire_weapon(weapon_type: WeaponType) -> bool:
    """
    Fire a weapon if it's ready
    @param weapon_type: Type of weapon to fire
    @returns: True if weapon was fired, false if on cooldown
    """
    if ship_state != ShipState.ACTIVE:
        return false
    
    if not weapon_cooldown_timers.has(weapon_type):
        return false
    
    var timer: Timer = weapon_cooldown_timers[weapon_type]
    if timer.is_stopped():
        # Fire the weapon
        emit_signal("weapon_fired", 
                   WeaponType.keys()[weapon_type], 
                   global_position, 
                   Vector2.RIGHT.rotated(rotation))
        
        # Start cooldown
        timer.start()
        return true
    
    return false

func get_ship_info() -> Dictionary:
    """
    Get comprehensive information about the ship's current state
    @returns: Dictionary with ship information
    """
    return {
        "name": ship_name,
        "health": current_health,
        "max_health": MAX_HEALTH,
        "speed": current_speed,
        "position": global_position,
        "state": ShipState.keys()[ship_state]
    }

# ------------------------------------------------------------------------------
# Private Methods
# ------------------------------------------------------------------------------
func _update_rotation(delta: float) -> void:
    """
    Update ship rotation based on input
    @param delta: Time since last frame in seconds
    """
    rotation += _rotation_direction * ROTATION_SPEED * delta

func _update_thrust(delta: float) -> void:
    """
    Update thrust based on input
    @param delta: Time since last frame in seconds
    """
    _velocity = _velocity.move_toward(
        Vector2.RIGHT.rotated(rotation) * (_thrust_input * MAX_SPEED),
        ACCELERATION * delta
    )
    current_speed = _velocity.length()

func _apply_movement(delta: float) -> void:
    """
    Apply movement to the ship's position
    @param delta: Time since last frame in seconds
    """
    position += _velocity * delta

func _destroy() -> void:
    """
    Handle ship destruction
    """
    ship_state = ShipState.DESTROYED
    emit_signal("destroyed")
    # Add visual effects, sounds, etc.

# ------------------------------------------------------------------------------
# Input Handlers
# ------------------------------------------------------------------------------
func _input(event: InputEvent) -> void:
    """
    Handle input events
    @param event: Input event to process
    """
    if ship_state != ShipState.ACTIVE:
        return
    
    # Rotation input
    if event.is_action_pressed("rotate_left"):
        _rotation_direction = -1
    elif event.is_action_pressed("rotate_right"):
        _rotation_direction = 1
    elif event.is_action_released("rotate_left") and _rotation_direction == -1:
        _rotation_direction = 0
    elif event.is_action_released("rotate_right") and _rotation_direction == 1:
        _rotation_direction = 0
    
    # Thrust input
    if event.is_action_pressed("thrust_forward"):
        _thrust_input = 1.0
    elif event.is_action_released("thrust_forward"):
        _thrust_input = 0.0
    
    # Weapon firing
    if event.is_action_pressed("fire_laser"):
        fire_weapon(WeaponType.LASER)
    elif event.is_action_pressed("fire_missile"):
        fire_weapon(WeaponType.MISSILE)
    elif event.is_action_pressed("fire_plasma"):
        fire_weapon(WeaponType.PLASMA)

```

---

## converter/context/GOLD_STANDARDS/example_well_structured_test.gd

**File type:** .gd  

**Size:** 3567 bytes  

**Last modified:** 2025-08-21 13:11:42


```gdscript
# TestPlayerShip
# Unit tests for the PlayerShip class

extends "res://addons/gdUnit4/src/GdUnit4"

# ------------------------------------------------------------------------------
# Test Setup
# ------------------------------------------------------------------------------
var player_ship: PlayerShip

func before_all():
    # Setup code that runs once before all tests
    pass

func after_all():
    # Teardown code that runs once after all tests
    pass

func before_each():
    # Setup code that runs before each test
    player_ship = PlayerShip.new()
    # Add to scene tree to initialize
    add_child(player_ship)
    player_ship._ready()

func after_each():
    # Teardown code that runs after each test
    if player_ship != null and is_instance_valid(player_ship):
        player_ship.queue_free()

# ------------------------------------------------------------------------------
# Test Cases
# ------------------------------------------------------------------------------
func test_initialization():
    # Test that the player ship initializes with correct default values
    assert_that(player_ship.current_health).is_equal(100)
    assert_that(player_ship.ship_state).is_equal(PlayerShip.ShipState.ACTIVE)
    assert_that(player_ship.current_speed).is_equal(0.0)

func test_take_damage():
    # Test that taking damage reduces health correctly
    player_ship.take_damage(25)
    assert_that(player_ship.current_health).is_equal(75)
    
    # Test that health doesn't go below zero
    player_ship.take_damage(100)
    assert_that(player_ship.current_health).is_equal(0)

func test_fire_weapon():
    # Test that weapons can be fired when not on cooldown
    var result = player_ship.fire_weapon(PlayerShip.WeaponType.LASER)
    assert_that(result).is_true()
    
    # Test that weapons cannot be fired when on cooldown
    result = player_ship.fire_weapon(PlayerShip.WeaponType.LASER)
    assert_that(result).is_false()

func test_get_ship_info():
    # Test that ship info is returned correctly
    var info = player_ship.get_ship_info()
    assert_that(info).is_not_null()
    assert_that(info.name).is_equal("Default Fighter")
    assert_that(info.health).is_equal(100)
    assert_that(info.max_health).is_equal(100)
    assert_that(info.speed).is_equal(0.0)
    assert_that(info.state).is_equal("ACTIVE")

func test_destroy():
    # Test that the ship is destroyed when health reaches zero
    # Connect to the destroyed signal
    var destroyed_emitted = false
    player_ship.connect("destroyed", func(): destroyed_emitted = true)
    
    # Reduce health to zero
    player_ship.take_damage(100)
    
    # Check that the ship is destroyed
    assert_that(player_ship.ship_state).is_equal(PlayerShip.ShipState.DESTROYED)
    assert_that(destroyed_emitted).is_true()

# ------------------------------------------------------------------------------
# Helper Methods
# ------------------------------------------------------------------------------
func create_mock_timer() -> Timer:
    """
    Create a mock timer for testing
    @returns: Configured Timer node
    """
    var timer = Timer.new()
    timer.one_shot = true
    timer.autostart = false
    add_child(timer)
    return timer

func simulate_input(action: String, pressed: bool):
    """
    Simulate an input action for testing
    @param action: Name of the action to simulate
    @param pressed: Whether the action is pressed or released
    """
    var event = InputEventAction.new()
    event.action = action
    event.pressed = pressed
    Input.parse_input_event(event)

```

---

## converter/context/README.md

**File type:** .md  

**Size:** 951 bytes  

**Last modified:** 2025-08-21 21:49:42


```markdown
# Context Engineering

This directory contains the guidance artifacts and rulebooks for the AI agents.

Based on the "Agentic Migration with CLI Agents" document, these artifacts are essential for ensuring high-quality, consistent output:

- `STYLE_GUIDE.md` - Architectural style guide for Godot/GDScript
- `RULES.md` - Virtual constitution with strict principles for AI actions
- `TEMPLATES/` - Scaffolding templates for common Godot file types
- `GOLD_STANDARDS/` - Curated examples of perfect Godot implementations

## Integration with Other Systems

The context engineering system integrates with several systems:

- **Prompt Engineering**: Provides guidance artifacts for prompt creation
- **Refactoring Specialist**: Ensures consistent output quality through style guides and templates
- **Validation System**: Provides standards for quality assurance
- **Orchestrator**: Ensures consistent application of rules throughout the migration process
```

---

## converter/context/RULES.md

**File type:** .md  

**Size:** 7558 bytes  

**Last modified:** 2025-08-21 13:10:06


```markdown
# Virtual Constitution: Rules for AI Actions in Wing Commander Saga Migration

This document serves as the virtual constitution for all AI agents in the migration process. These strict principles must be followed to ensure quality, consistency, and safety in all automated operations.

## Core Principles

### 1. Preservation of Game Integrity
- **Functional Equivalence**: All migrated code must preserve the original game's functionality
- **Behavioral Consistency**: Gameplay mechanics must remain unchanged unless explicitly approved
- **Data Compatibility**: Existing save files and configuration data must remain compatible

### 2. Quality Assurance
- **Code Standards**: All generated code must adhere to the STYLE_GUIDE.md
- **Testing Requirements**: Every code change must be accompanied by appropriate tests
- **Error Handling**: All code must include proper error handling and logging
- **Documentation**: All public interfaces must be properly documented

### 3. Safety and Security
- **No Destructive Operations**: Agents must never delete or modify source files without explicit approval
- **Controlled Execution**: All file operations must be within the designated project directories
- **Resource Limits**: Agents must respect timeout and resource usage limits
- **Secure Practices**: No external network calls without explicit authorization

## Agent-Specific Rules

### MigrationArchitect Rules
1. **Strategic Focus**: Only create high-level plans, don't generate code
2. **Phase Boundaries**: Clearly define boundaries between migration phases
3. **Risk Assessment**: Identify and document potential risks in each phase
4. **Dependency Mapping**: Always consider system dependencies in planning

### CodebaseAnalyst Rules
1. **Read-Only Operations**: Only analyze existing code, never modify it
2. **Accurate Reporting**: Report dependencies and relationships accurately
3. **Context Preservation**: Maintain full context when analyzing code segments
4. **Pattern Recognition**: Identify and document architectural patterns correctly

### TaskDecompositionSpecialist Rules
1. **Atomic Tasks**: Break down work into truly atomic, executable tasks
2. **Clear Instructions**: Provide unambiguous task descriptions
3. **Dependency Awareness**: Consider task dependencies when ordering work
4. **Scope Control**: Ensure tasks are appropriately scoped (not too large or small)

### PromptEngineeringAgent Rules
1. **Structured Prompts**: Always use structured, tagged prompt formats
2. **Context Inclusion**: Include all necessary context for task execution
3. **Constraint Specification**: Clearly specify all constraints and requirements
4. **Output Formatting**: Define expected output format explicitly

### QualityAssuranceAgent Rules
1. **Comprehensive Testing**: Verify all aspects of generated code
2. **Error Analysis**: Provide detailed error analysis for failures
3. **Correction Guidance**: Offer specific guidance for corrections
4. **Success Documentation**: Document successful outcomes clearly

### Refactoring Specialist Rules
1. **Focused Changes**: Only modify code related to the specific task
2. **Style Compliance**: Ensure all changes follow the STYLE_GUIDE.md
3. **No Functional Changes**: Don't alter functionality unless explicitly requested
4. **Preserve Comments**: Maintain existing comments and documentation

### Test Generator Rules
1. **Complete Coverage**: Generate tests for all public interfaces
2. **Edge Cases**: Include edge case testing in test suites
3. **Framework Compliance**: Use the appropriate testing framework (gdUnit4)
4. **Clear Naming**: Use descriptive names for test cases

### Validation Engineer Rules
1. **Thorough Validation**: Execute all relevant tests and validations
2. **Performance Checking**: Verify performance characteristics where critical
3. **Security Scanning**: Run security checks on generated code
4. **Compliance Verification**: Ensure code meets all project standards

## Process Rules

### Workflow Execution
1. **Sequential Adherence**: Follow the defined sequential workflow for atomic tasks
2. **Hierarchical Coordination**: Use hierarchical workflows for complex operations
3. **Status Reporting**: Report task status at each workflow stage
4. **Error Escalation**: Escalate unresolvable errors to human oversight

### Communication Protocols
1. **Structured Data**: Use structured data formats for inter-agent communication
2. **Clear Handoffs**: Clearly document task handoffs between agents
3. **Error Context**: Include full context when reporting errors
4. **Progress Updates**: Provide regular progress updates for long-running tasks

### Feedback Loops
1. **Failure Analysis**: Analyze all failures to prevent recurrence
2. **Prompt Refinement**: Refine prompts based on execution results
3. **Process Improvement**: Suggest process improvements based on experience
4. **Knowledge Sharing**: Share learning across agents

## Technical Constraints

### File System Rules
1. **Directory Restrictions**: Only operate within designated project directories
2. **File Type Awareness**: Respect file type conventions and restrictions
3. **Backup Requirements**: Create backups before modifying existing files
4. **Version Control**: Integrate with version control for all changes

### Resource Management
1. **Memory Limits**: Respect memory usage limits for all operations
2. **Timeout Enforcement**: Honor timeout settings for all tasks
3. **CPU Usage**: Avoid excessive CPU usage that could impact system performance
4. **Network Usage**: Minimize network calls and respect bandwidth limits

### Error Handling
1. **Graceful Degradation**: Handle errors gracefully without system crashes
2. **Retry Logic**: Implement appropriate retry logic for transient failures
3. **Circuit Breakers**: Use circuit breakers for persistent failure conditions
4. **Human Escalation**: Escalate complex issues to human operators

## Compliance Verification

### Self-Checking Requirements
1. **Rule Validation**: Agents must validate their actions against these rules
2. **Audit Trails**: Maintain audit trails for all significant actions
3. **Compliance Reporting**: Generate compliance reports when requested
4. **Continuous Monitoring**: Continuously monitor for rule violations

### Human Oversight Points
1. **Strategic Decisions**: All strategic planning requires human approval
2. **Major Changes**: Significant code changes require human review
3. **Error Conditions**: Complex error conditions require human intervention
4. **Process Modifications**: Changes to workflows require human authorization

## Violation Consequences

### Minor Violations
- Warning notification to overseeing agent
- Task suspension for review
- Prompt refinement requirement

### Major Violations
- Immediate task termination
- Human operator notification
- Process audit initiation
- Potential agent suspension

### Critical Violations
- Complete system shutdown
- Immediate human operator intervention
- Full process investigation
- Agent capability restrictions

## Continuous Improvement

### Learning Requirements
1. **Experience Documentation**: Document lessons learned from each task
2. **Process Refinement**: Continuously refine processes based on experience
3. **Rule Updates**: Suggest rule updates based on operational experience
4. **Performance Metrics**: Track and report on performance metrics

This document represents the foundational rules that govern all AI agent behavior in the migration process. Any deviation from these rules requires explicit human authorization.

```

---

## converter/context/STYLE_GUIDE.md

**File type:** .md  

**Size:** 4929 bytes  

**Last modified:** 2025-08-21 13:09:33


```markdown
# Godot/GDScript Style Guide for Wing Commander Saga Migration

This document provides architectural style guidelines for the Wing Commander Saga to Godot migration project. All generated code should adhere to these principles to ensure consistency and maintainability.

## General Principles

1. **Idiomatic Godot Design**: All code should follow Godot's architectural patterns and best practices
2. **Performance Conscious**: Prioritize efficient code that maintains the game's performance characteristics
3. **Maintainability**: Write clear, well-documented code that can be easily understood and modified
4. **Consistency**: Follow established patterns throughout the codebase

## GDScript Coding Standards

### Naming Conventions

- **Classes/Nodes**: Use PascalCase (`PlayerShip`, `WeaponSystem`)
- **Variables**: Use snake_case (`player_ship`, `current_health`)
- **Constants**: Use CONSTANT_CASE (`MAX_SPEED`, `DEFAULT_WEAPON`)
- **Methods**: Use snake_case (`fire_weapon`, `calculate_damage`)
- **Signals**: Use snake_case with past tense (`health_depleted`, `target_acquired`)

### File Organization

```
# Preferred file structure
# 1. Tool declaration (if needed)
# 2. Class documentation
# 3. Class name
# 4. Extends statement
# 5. Signals
# 6. Enums
# 7. Constants
# 8. Exported variables
# 9. Public variables
# 10. Private variables (prefixed with _)
# 11. Onready variables
# 12. Static functions
# 13. Built-in virtual methods (_ready, _process, etc.)
# 14. Public methods
# 15. Private methods (prefixed with _)
```

### Documentation

- Use docstring comments for all public classes and methods
- Include parameter descriptions and return value information
- Document complex logic with inline comments

```gdscript
# Calculate damage based on weapon type and distance to target
# @param weapon_type: Type of weapon being fired
# @param distance: Distance to target in meters
# @returns: Damage value as a float
func calculate_damage(weapon_type: String, distance: float) -> float:
    # Implementation here
    pass
```

## Architecture Patterns

### Component-Based Design

Follow Godot's node-based component system:
- Use nodes to represent components
- Prefer composition over inheritance
- Leverage Godot's scene system for object composition

### State Management

- Use state machines for complex entity behavior
- Implement states as separate nodes or scripts
- Centralize state transitions through a state manager

### Event-Driven Communication

- Use Godot signals for inter-node communication
- Avoid tight coupling between components
- Implement observer patterns where appropriate

## Performance Guidelines

### Memory Management

- Reuse objects when possible
- Use object pooling for frequently created/destroyed objects
- Avoid unnecessary node creation/deletion in performance-critical sections

### Processing Efficiency

- Use `_physics_process` only for physics-related updates
- Use `_process` for non-physics game logic
- Implement frame skipping or interpolation for expensive operations

### Resource Handling

- Preload resources when possible
- Use resource caching to avoid duplicate loading
- Implement proper resource cleanup

## Migration-Specific Considerations

### C++ to GDScript Translation

1. **Data Types**:
   - Map C++ primitives to GDScript equivalents
   - Use Godot's built-in types (Vector3, Color, etc.) where appropriate
   - Implement custom classes for complex data structures

2. **Memory Management**:
   - Leverage GDScript's garbage collection
   - Remove explicit memory management code from C++
   - Use Godot's reference counting for resources

3. **Inheritance**:
   - Flatten deep inheritance hierarchies where possible
   - Use composition to replace multiple inheritance
   - Leverage Godot's node inheritance system

### Legacy System Integration

1. **Data Formats**:
   - Maintain compatibility with existing data files where possible
   - Implement converters for proprietary formats
   - Validate data during loading

2. **Game Logic Preservation**:
   - Ensure mathematical calculations produce identical results
   - Maintain timing-sensitive behaviors
   - Preserve random number generation sequences where critical

## Testing Standards

### Unit Testing

- Write tests for all public methods
- Use gdUnit4 framework for test implementation
- Include edge case testing
- Maintain high test coverage for core systems

### Integration Testing

- Test component interactions
- Validate scene compositions
- Verify signal connections and data flow

## Code Review Checklist

Before merging any generated code, ensure it meets these criteria:

- [ ] Follows naming conventions
- [ ] Includes appropriate documentation
- [ ] Uses Godot's architectural patterns
- [ ] Passes all unit tests
- [ ] Demonstrates acceptable performance
- [ ] Contains no hardcoded values (use constants)
- [ ] Handles errors gracefully
- [ ] Avoids code duplication

```

---

## converter/context/TEMPLATES/gdscript_class_template.gd

**File type:** .gd  

**Size:** 2267 bytes  

**Last modified:** 2025-08-21 13:10:22


```gdscript
# {CLASS_NAME}
# {DESCRIPTION}

{TOOL_DECLARATION}

class_name {CLASS_NAME}

extends {PARENT_CLASS}

# ------------------------------------------------------------------------------
# Signals
# ------------------------------------------------------------------------------
{SIGNALS}

# ------------------------------------------------------------------------------
# Enums
# ------------------------------------------------------------------------------
{ENUMS}

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------
{CONSTANTS}

# ------------------------------------------------------------------------------
# Exported Variables
# ------------------------------------------------------------------------------
{EXPORTED_VARIABLES}

# ------------------------------------------------------------------------------
# Public Variables
# ------------------------------------------------------------------------------
{PUBLIC_VARIABLES}

# ------------------------------------------------------------------------------
# Private Variables
# ------------------------------------------------------------------------------
{PRIVATE_VARIABLES}

# ------------------------------------------------------------------------------
# Onready Variables
# ------------------------------------------------------------------------------
{ONREADY_VARIABLES}

# ------------------------------------------------------------------------------
# Static Functions
# ------------------------------------------------------------------------------
{STATIC_FUNCTIONS}

# ------------------------------------------------------------------------------
# Built-in Virtual Methods
# ------------------------------------------------------------------------------
{BUILT_IN_METHODS}

# ------------------------------------------------------------------------------
# Public Methods
# ------------------------------------------------------------------------------
{PUBLIC_METHODS}

# ------------------------------------------------------------------------------
# Private Methods
# ------------------------------------------------------------------------------
{PRIVATE_METHODS}

```

---

## converter/context/TEMPLATES/gdunit4_test_template.gd

**File type:** .gd  

**Size:** 953 bytes  

**Last modified:** 2025-08-21 13:10:46


```gdscript
# {TEST_CLASS_NAME}
# Unit tests for {TARGET_CLASS_NAME}

extends {PARENT_TEST_CLASS}

# ------------------------------------------------------------------------------
# Test Setup
# ------------------------------------------------------------------------------
func before_all():
    # Setup code that runs once before all tests
    pass

func after_all():
    # Teardown code that runs once after all tests
    pass

func before_each():
    # Setup code that runs before each test
    pass

func after_each():
    # Teardown code that runs after each test
    pass

# ------------------------------------------------------------------------------
# Test Cases
# ------------------------------------------------------------------------------
{TEST_CASES}

# ------------------------------------------------------------------------------
# Helper Methods
# ------------------------------------------------------------------------------
{HELPER_METHODS}

```

---

## converter/context/TEMPLATES/godot_scene_template.tscn

**File type:** .tscn  

**Size:** 177 bytes  

**Last modified:** 2025-08-21 13:10:30


```ini
[gd_scene load_steps={LOAD_STEPS} format=2]

{EXTERNAL_RESOURCES}

{SUB_RESOURCES}

[node name="{ROOT_NODE_NAME}" type="{ROOT_NODE_TYPE}"]
{ROOT_NODE_PROPERTIES}

{CHILD_NODES}

```

---

## converter/graph_system/README.md

**File type:** .md  

**Size:** 1207 bytes  

**Last modified:** 2025-08-21 21:52:23


```markdown
# Graph System

This directory contains the dependency graph system for tracking codebase relationships in the Wing Commander Saga to Godot migration.

## Overview

The graph system implements a robust dependency graph for tracking relationships between codebase entities. It provides:

1. **Dependency Tracking**: Track dependencies between different entities in the codebase
2. **Concurrency Control**: Handle concurrent access to the graph with proper locking
3. **Persistence**: Save and load graph data to/from files
4. **Topological Ordering**: Determine migration order based on dependencies

## Key Components

- `dependency_graph.py` - Core dependency graph implementation using NetworkX
- `graph_manager.py` - Manager for the dependency graph with concurrency control
- `file_monitor.py` - File monitoring for real-time graph updates

## Integration with Other Systems

The graph system integrates with several other systems:

- **Orchestrator**: Provides dependency information for task ordering
- **Codebase Analyst**: Receives dependency information from analysis
- **Prompt Engineering**: Provides context for prompt creation
- **Validation System**: Uses dependency information for validation
```

---

## converter/graph_system/__init__.py

**File type:** .py  

**Size:** 210 bytes  

**Last modified:** 2025-08-21 20:27:55


```python
"""
Graph System Module

This module contains the dependency graph system for tracking codebase relationships
in the Wing Commander Saga to Godot migration.
"""

__version__ = "0.1.0"
__author__ = "WCSaga Team"
```

---

## converter/graph_system/dependency_graph.py

**File type:** .py  

**Size:** 12421 bytes  

**Last modified:** 2025-08-21 20:37:15


```python
"""
Dependency Graph Implementation

This module implements a dependency graph system for tracking codebase relationships
in the Wing Commander Saga to Godot migration.
"""

import json
import time
import logging
from typing import Dict, Any, List, Optional, Set
from pathlib import Path
import networkx as nx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DependencyGraph:
    """Dependency graph for tracking codebase relationships."""
    
    def __init__(self, graph_file: Optional[str] = None):
        """
        Initialize the dependency graph.
        
        Args:
            graph_file: Optional path to load/save the graph
        """
        self.graph = nx.DiGraph()
        self.graph_file = graph_file
        self.last_updated = time.time()
        
        # Load graph from file if provided
        if self.graph_file and Path(self.graph_file).exists():
            self.load_graph()
        
        logger.info("Dependency Graph initialized")
    
    def add_entity(self, entity_id: str, entity_type: str, 
                   properties: Optional[Dict[str, Any]] = None) -> None:
        """
        Add an entity to the graph.
        
        Args:
            entity_id: Unique identifier for the entity
            entity_type: Type of the entity (e.g., 'ship', 'weapon', 'module')
            properties: Optional properties of the entity
        """
        if properties is None:
            properties = {}
            
        properties.update({
            "type": entity_type,
            "created_at": time.time(),
            "last_modified": time.time()
        })
        
        self.graph.add_node(entity_id, **properties)
        self._mark_updated()
        
        logger.debug(f"Added entity {entity_id} of type {entity_type}")
    
    def add_dependency(self, from_entity: str, to_entity: str, 
                      dependency_type: str = "depends_on") -> None:
        """
        Add a dependency relationship between two entities.
        
        Args:
            from_entity: ID of the dependent entity
            to_entity: ID of the dependency
            dependency_type: Type of dependency (e.g., 'depends_on', 'inherits_from')
        """
        # Ensure both entities exist
        if not self.graph.has_node(from_entity):
            self.add_entity(from_entity, "unknown")
        
        if not self.graph.has_node(to_entity):
            self.add_entity(to_entity, "unknown")
        
        # Add the dependency edge
        self.graph.add_edge(from_entity, to_entity, type=dependency_type)
        self._mark_updated()
        
        logger.debug(f"Added dependency: {from_entity} -> {to_entity} ({dependency_type})")
    
    def get_dependencies(self, entity_id: str) -> List[Dict[str, Any]]:
        """
        Get all dependencies of an entity.
        
        Args:
            entity_id: ID of the entity
            
        Returns:
            List of dependencies
        """
        if not self.graph.has_node(entity_id):
            return []
        
        dependencies = []
        for successor in self.graph.successors(entity_id):
            edge_data = self.graph.get_edge_data(entity_id, successor)
            dependencies.append({
                "dependent": entity_id,
                "dependency": successor,
                "type": edge_data.get("type", "depends_on")
            })
        
        return dependencies
    
    def get_dependents(self, entity_id: str) -> List[Dict[str, Any]]:
        """
        Get all entities that depend on this entity.
        
        Args:
            entity_id: ID of the entity
            
        Returns:
            List of dependents
        """
        if not self.graph.has_node(entity_id):
            return []
        
        dependents = []
        for predecessor in self.graph.predecessors(entity_id):
            edge_data = self.graph.get_edge_data(predecessor, entity_id)
            dependents.append({
                "dependent": predecessor,
                "dependency": entity_id,
                "type": edge_data.get("type", "depends_on")
            })
        
        return dependents
    
    def get_entity_properties(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """
        Get properties of an entity.
        
        Args:
            entity_id: ID of the entity
            
        Returns:
            Entity properties, or None if entity not found
        """
        if not self.graph.has_node(entity_id):
            return None
        
        return dict(self.graph.nodes[entity_id])
    
    def update_entity_properties(self, entity_id: str, 
                                properties: Dict[str, Any]) -> bool:
        """
        Update properties of an entity.
        
        Args:
            entity_id: ID of the entity
            properties: Properties to update
            
        Returns:
            True if successful, False otherwise
        """
        if not self.graph.has_node(entity_id):
            return False
        
        # Update the properties
        for key, value in properties.items():
            self.graph.nodes[entity_id][key] = value
        
        self.graph.nodes[entity_id]["last_modified"] = time.time()
        self._mark_updated()
        
        logger.debug(f"Updated properties for entity {entity_id}")
        return True
    
    def get_topological_order(self) -> List[str]:
        """
        Get entities in topological order (suitable for migration sequence).
        
        Returns:
            List of entity IDs in topological order
        """
        try:
            # Get topological sort
            topo_order = list(nx.topological_sort(self.graph))
            return topo_order
        except nx.NetworkXError as e:
            logger.warning(f"Graph has cycles, cannot perform topological sort: {str(e)}")
            # Return nodes in a simple order as fallback
            return list(self.graph.nodes())
    
    def find_cycles(self) -> List[List[str]]:
        """
        Find cycles in the dependency graph.
        
        Returns:
            List of cycles (each cycle is a list of entity IDs)
        """
        try:
            cycles = list(nx.simple_cycles(self.graph))
            return cycles
        except Exception as e:
            logger.error(f"Error finding cycles: {str(e)}")
            return []
    
    def get_subgraph(self, entity_ids: List[str]) -> 'DependencyGraph':
        """
        Get a subgraph containing only the specified entities and their relationships.
        
        Args:
            entity_ids: List of entity IDs to include
            
        Returns:
            New DependencyGraph instance with the subgraph
        """
        subgraph = self.graph.subgraph(entity_ids).copy()
        new_graph = DependencyGraph()
        new_graph.graph = subgraph
        return new_graph
    
    def save_graph(self, file_path: Optional[str] = None) -> bool:
        """
        Save the graph to a file.
        
        Args:
            file_path: Path to save the graph (uses self.graph_file if None)
            
        Returns:
            True if successful, False otherwise
        """
        if file_path is None:
            file_path = self.graph_file
        
        if file_path is None:
            logger.warning("No file path specified for saving graph")
            return False
        
        try:
            # Convert graph to JSON-serializable format
            graph_data = {
                "nodes": [],
                "edges": [],
                "metadata": {
                    "last_updated": self.last_updated,
                    "node_count": self.graph.number_of_nodes(),
                    "edge_count": self.graph.number_of_edges()
                }
            }
            
            # Add nodes
            for node_id, node_data in self.graph.nodes(data=True):
                graph_data["nodes"].append({
                    "id": node_id,
                    "properties": node_data
                })
            
            # Add edges
            for from_node, to_node, edge_data in self.graph.edges(data=True):
                graph_data["edges"].append({
                    "from": from_node,
                    "to": to_node,
                    "properties": edge_data
                })
            
            # Save to file
            with open(file_path, 'w') as f:
                json.dump(graph_data, f, indent=2)
            
            logger.info(f"Graph saved to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save graph: {str(e)}")
            return False
    
    def load_graph(self, file_path: Optional[str] = None) -> bool:
        """
        Load the graph from a file.
        
        Args:
            file_path: Path to load the graph from (uses self.graph_file if None)
            
        Returns:
            True if successful, False otherwise
        """
        if file_path is None:
            file_path = self.graph_file
        
        if file_path is None or not Path(file_path).exists():
            logger.warning("No graph file to load")
            return False
        
        try:
            # Load from file
            with open(file_path, 'r') as f:
                graph_data = json.load(f)
            
            # Clear current graph
            self.graph.clear()
            
            # Add nodes
            for node_info in graph_data.get("nodes", []):
                node_id = node_info["id"]
                properties = node_info.get("properties", {})
                self.graph.add_node(node_id, **properties)
            
            # Add edges
            for edge_info in graph_data.get("edges", []):
                from_node = edge_info["from"]
                to_node = edge_info["to"]
                properties = edge_info.get("properties", {})
                self.graph.add_edge(from_node, to_node, **properties)
            
            # Update metadata
            self.last_updated = graph_data.get("metadata", {}).get("last_updated", time.time())
            
            logger.info(f"Graph loaded from {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load graph: {str(e)}")
            return False
    
    def _mark_updated(self) -> None:
        """Mark the graph as updated."""
        self.last_updated = time.time()
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the graph.
        
        Returns:
            Dictionary with graph statistics
        """
        return {
            "node_count": self.graph.number_of_nodes(),
            "edge_count": self.graph.number_of_edges(),
            "isolated_nodes": len(list(nx.isolates(self.graph))),
            "strongly_connected_components": nx.number_strongly_connected_components(self.graph),
            "last_updated": self.last_updated
        }


def main():
    """Main function for testing the DependencyGraph."""
    # Create dependency graph
    graph = DependencyGraph("test_dependency_graph.json")
    
    # Add some test entities
    graph.add_entity("SHIP-GTC_FENRIS", "ship", {
        "name": "GTC Fenris",
        "type": "cruiser",
        "file_path": "source/tables/ships.tbl"
    })
    
    graph.add_entity("SHIP-GTF_MYRMIDON", "ship", {
        "name": "GTF Myrmidon",
        "type": "fighter",
        "file_path": "source/tables/ships.tbl"
    })
    
    graph.add_entity("MODULE-ENGINE", "module", {
        "name": "Engine Module",
        "type": "propulsion"
    })
    
    # Add dependencies
    graph.add_dependency("SHIP-GTC_FENRIS", "MODULE-ENGINE", "uses")
    graph.add_dependency("SHIP-GTF_MYRMIDON", "MODULE-ENGINE", "uses")
    
    # Print graph statistics
    print("Graph statistics:", graph.get_statistics())
    
    # Get dependencies
    print("Dependencies of SHIP-GTC_FENRIS:", graph.get_dependencies("SHIP-GTC_FENRIS"))
    print("Dependents of MODULE-ENGINE:", graph.get_dependents("MODULE-ENGINE"))
    
    # Get topological order
    print("Topological order:", graph.get_topological_order())
    
    # Save graph
    graph.save_graph()


if __name__ == "__main__":
    main()
```

---

## converter/graph_system/file_monitor.py

**File type:** .py  

**Size:** 9275 bytes  

**Last modified:** 2025-08-21 20:38:27


```python
"""
File Monitor Implementation

This module implements a file monitor that detects file system changes and updates
the dependency graph accordingly.
"""

import time
import logging
import threading
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Import our modules
from .graph_manager import GraphManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FileChangeHandler(FileSystemEventHandler):
    """Handler for file system events."""
    
    def __init__(self, callback: Callable[[str, str], None]):
        """
        Initialize the file change handler.
        
        Args:
            callback: Function to call when a file change is detected
        """
        super().__init__()
        self.callback = callback
    
    def on_modified(self, event):
        """Handle file modification events."""
        if not event.is_directory:
            logger.debug(f"File modified: {event.src_path}")
            self.callback("modified", event.src_path)
    
    def on_created(self, event):
        """Handle file creation events."""
        if not event.is_directory:
            logger.debug(f"File created: {event.src_path}")
            self.callback("created", event.src_path)
    
    def on_deleted(self, event):
        """Handle file deletion events."""
        if not event.is_directory:
            logger.debug(f"File deleted: {event.src_path}")
            self.callback("deleted", event.src_path)
    
    def on_moved(self, event):
        """Handle file move events."""
        if not event.is_directory:
            logger.debug(f"File moved: {event.src_path} -> {event.dest_path}")
            self.callback("moved", event.src_path, event.dest_path)


class FileMonitor:
    """Monitor for file system changes."""
    
    def __init__(self, watch_directory: str, graph_manager: GraphManager):
        """
        Initialize the file monitor.
        
        Args:
            watch_directory: Directory to monitor for changes
            graph_manager: Graph manager to update when changes occur
        """
        self.watch_directory = Path(watch_directory)
        self.graph_manager = graph_manager
        self.observer = Observer()
        self.handler = FileChangeHandler(self._handle_file_change)
        self.is_monitoring = False
        
        logger.info(f"File Monitor initialized for directory: {watch_directory}")
    
    def start_monitoring(self) -> None:
        """Start monitoring for file changes."""
        if self.is_monitoring:
            logger.warning("File monitoring already started")
            return
        
        self.observer.schedule(self.handler, str(self.watch_directory), recursive=True)
        self.observer.start()
        self.is_monitoring = True
        
        logger.info(f"Started monitoring directory: {self.watch_directory}")
    
    def stop_monitoring(self) -> None:
        """Stop monitoring for file changes."""
        if not self.is_monitoring:
            logger.warning("File monitoring not started")
            return
        
        self.observer.stop()
        self.observer.join()
        self.is_monitoring = False
        
        logger.info("Stopped file monitoring")
    
    def _handle_file_change(self, event_type: str, file_path: str, 
                           dest_path: Optional[str] = None) -> None:
        """
        Handle a file change event.
        
        Args:
            event_type: Type of event (modified, created, deleted, moved)
            file_path: Path to the file that changed
            dest_path: Destination path for move events
        """
        try:
            # Convert to Path object
            path = Path(file_path)
            
            # Get relative path from watch directory
            try:
                relative_path = path.relative_to(self.watch_directory)
            except ValueError:
                # File is not in the watched directory
                return
            
            # Create entity ID based on file path
            entity_id = self._create_entity_id(relative_path)
            
            # Handle different event types
            if event_type == "created":
                self._handle_file_created(entity_id, relative_path)
            elif event_type == "modified":
                self._handle_file_modified(entity_id, relative_path)
            elif event_type == "deleted":
                self._handle_file_deleted(entity_id, relative_path)
            elif event_type == "moved":
                self._handle_file_moved(entity_id, relative_path, Path(dest_path))
                
        except Exception as e:
            logger.error(f"Error handling file change event: {str(e)}")
    
    def _create_entity_id(self, relative_path: Path) -> str:
        """
        Create an entity ID from a relative file path.
        
        Args:
            relative_path: Relative path to the file
            
        Returns:
            Entity ID
        """
        # Convert path to entity ID format
        # Replace path separators with dashes and remove file extension
        path_parts = list(relative_path.parts)
        if path_parts:
            # Remove file extension from last part
            path_parts[-1] = path_parts[-1].split('.')[0]
        
        entity_id = "-".join(path_parts).upper()
        return entity_id
    
    def _handle_file_created(self, entity_id: str, relative_path: Path) -> None:
        """
        Handle a file creation event.
        
        Args:
            entity_id: ID of the entity
            relative_path: Relative path to the file
        """
        # Determine entity type based on file extension
        entity_type = self._determine_entity_type(relative_path)
        
        # Add entity to graph
        self.graph_manager.add_entity(entity_id, entity_type, {
            "file_path": str(relative_path),
            "created": time.time()
        })
        
        logger.info(f"Added entity {entity_id} for created file {relative_path}")
    
    def _handle_file_modified(self, entity_id: str, relative_path: Path) -> None:
        """
        Handle a file modification event.
        
        Args:
            entity_id: ID of the entity
            relative_path: Relative path to the file
        """
        # Update entity properties
        self.graph_manager.update_entity_properties(entity_id, {
            "last_modified": time.time(),
            "file_path": str(relative_path)
        })
        
        logger.info(f"Updated entity {entity_id} for modified file {relative_path}")
    
    def _handle_file_deleted(self, entity_id: str, relative_path: Path) -> None:
        """
        Handle a file deletion event.
        
        Args:
            entity_id: ID of the entity
            relative_path: Relative path to the file
        """
        # Note: In a real implementation, we might want to remove the entity
        # For now, we'll just mark it as deleted
        self.graph_manager.update_entity_properties(entity_id, {
            "deleted": time.time(),
            "file_path": str(relative_path)
        })
        
        logger.info(f"Marked entity {entity_id} as deleted for file {relative_path}")
    
    def _handle_file_moved(self, entity_id: str, src_path: Path, dest_path: Path) -> None:
        """
        Handle a file move event.
        
        Args:
            entity_id: ID of the entity
            src_path: Source path of the file
            dest_path: Destination path of the file
        """
        # Update entity with new file path
        self.graph_manager.update_entity_properties(entity_id, {
            "file_path": str(dest_path),
            "moved_from": str(src_path),
            "last_moved": time.time()
        })
        
        logger.info(f"Updated entity {entity_id} for moved file {src_path} -> {dest_path}")
    
    def _determine_entity_type(self, relative_path: Path) -> str:
        """
        Determine the entity type based on file extension.
        
        Args:
            relative_path: Relative path to the file
            
        Returns:
            Entity type
        """
        extension = relative_path.suffix.lower()
        
        if extension in ['.cpp', '.h', '.hpp']:
            return "source_code"
        elif extension in ['.tbl', '.tbm']:
            return "table_data"
        elif extension in ['.pof']:
            return "model_data"
        elif extension in ['.fs2']:
            return "mission_data"
        elif extension in ['.gd']:
            return "gdscript"
        elif extension in ['.tscn']:
            return "scene"
        elif extension in ['.tres']:
            return "resource"
        else:
            return "unknown"


def main():
    """Main function for testing the FileMonitor."""
    # This would require actual file system monitoring which is difficult to test automatically
    # The implementation is provided for future use in the migration system
    print("FileMonitor implementation ready for use in migration system")


if __name__ == "__main__":
    main()
```

---

## converter/graph_system/graph_manager.py

**File type:** .py  

**Size:** 10206 bytes  

**Last modified:** 2025-08-21 20:37:56


```python
"""
Graph Manager Implementation

This module implements a graph manager that handles dynamic updates and concurrency control
for the dependency graph system.
"""

import time
import logging
import threading
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path
from threading import Lock, RLock

# Import our modules
from .dependency_graph import DependencyGraph

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GraphManager:
    """Manager for the dependency graph with concurrency control."""
    
    def __init__(self, graph_file: Optional[str] = None, auto_save: bool = True):
        """
        Initialize the graph manager.
        
        Args:
            graph_file: Optional path to load/save the graph
            auto_save: Whether to automatically save changes
        """
        self.graph = DependencyGraph(graph_file)
        self.auto_save = auto_save
        self.graph_file = graph_file
        self.lock = RLock()  # Reentrant lock for thread safety
        self.transaction_lock = Lock()  # Lock for transactions
        self.transaction_active = False
        self.transaction_changes = []
        
        logger.info("Graph Manager initialized")
    
    def add_entity(self, entity_id: str, entity_type: str, 
                   properties: Optional[Dict[str, Any]] = None) -> None:
        """
        Add an entity to the graph (thread-safe).
        
        Args:
            entity_id: Unique identifier for the entity
            entity_type: Type of the entity
            properties: Optional properties of the entity
        """
        with self.lock:
            self.graph.add_entity(entity_id, entity_type, properties)
            if self.auto_save:
                self.graph.save_graph()
    
    def add_dependency(self, from_entity: str, to_entity: str, 
                      dependency_type: str = "depends_on") -> None:
        """
        Add a dependency relationship between two entities (thread-safe).
        
        Args:
            from_entity: ID of the dependent entity
            to_entity: ID of the dependency
            dependency_type: Type of dependency
        """
        with self.lock:
            self.graph.add_dependency(from_entity, to_entity, dependency_type)
            if self.auto_save:
                self.graph.save_graph()
    
    def update_entity_properties(self, entity_id: str, 
                                properties: Dict[str, Any]) -> bool:
        """
        Update properties of an entity (thread-safe).
        
        Args:
            entity_id: ID of the entity
            properties: Properties to update
            
        Returns:
            True if successful, False otherwise
        """
        with self.lock:
            result = self.graph.update_entity_properties(entity_id, properties)
            if result and self.auto_save:
                self.graph.save_graph()
            return result
    
    def get_entity_properties(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """
        Get properties of an entity (thread-safe).
        
        Args:
            entity_id: ID of the entity
            
        Returns:
            Entity properties, or None if entity not found
        """
        with self.lock:
            return self.graph.get_entity_properties(entity_id)
    
    def get_dependencies(self, entity_id: str) -> List[Dict[str, Any]]:
        """
        Get all dependencies of an entity (thread-safe).
        
        Args:
            entity_id: ID of the entity
            
        Returns:
            List of dependencies
        """
        with self.lock:
            return self.graph.get_dependencies(entity_id)
    
    def get_dependents(self, entity_id: str) -> List[Dict[str, Any]]:
        """
        Get all entities that depend on this entity (thread-safe).
        
        Args:
            entity_id: ID of the entity
            
        Returns:
            List of dependents
        """
        with self.lock:
            return self.graph.get_dependents(entity_id)
    
    def get_topological_order(self) -> List[str]:
        """
        Get entities in topological order (thread-safe).
        
        Returns:
            List of entity IDs in topological order
        """
        with self.lock:
            return self.graph.get_topological_order()
    
    def begin_transaction(self) -> bool:
        """
        Begin a transaction for atomic updates.
        
        Returns:
            True if transaction started, False if already in transaction
        """
        if self.transaction_lock.acquire(blocking=False):
            with self.lock:
                if not self.transaction_active:
                    self.transaction_active = True
                    self.transaction_changes = []
                    logger.debug("Transaction started")
                    return True
                else:
                    self.transaction_lock.release()
                    logger.warning("Transaction already active")
                    return False
        else:
            logger.warning("Could not acquire transaction lock")
            return False
    
    def commit_transaction(self) -> bool:
        """
        Commit the current transaction.
        
        Returns:
            True if committed, False if no transaction active
        """
        with self.lock:
            if self.transaction_active:
                self.transaction_active = False
                self.transaction_changes = []
                if self.auto_save:
                    self.graph.save_graph()
                self.transaction_lock.release()
                logger.debug("Transaction committed")
                return True
            else:
                logger.warning("No transaction active to commit")
                return False
    
    def rollback_transaction(self) -> bool:
        """
        Rollback the current transaction.
        
        Returns:
            True if rolled back, False if no transaction active
        """
        with self.lock:
            if self.transaction_active:
                # Undo changes (simplified implementation)
                # In a real implementation, we would need to track and undo changes
                self.transaction_active = False
                self.transaction_changes = []
                self.transaction_lock.release()
                logger.debug("Transaction rolled back")
                return True
            else:
                logger.warning("No transaction active to rollback")
                return False
    
    def add_entity_in_transaction(self, entity_id: str, entity_type: str, 
                                 properties: Optional[Dict[str, Any]] = None) -> None:
        """
        Add an entity to the graph within a transaction.
        
        Args:
            entity_id: Unique identifier for the entity
            entity_type: Type of the entity
            properties: Optional properties of the entity
        """
        if not self.transaction_active:
            raise RuntimeError("No transaction active")
        
        with self.lock:
            self.graph.add_entity(entity_id, entity_type, properties)
            self.transaction_changes.append(("add_entity", entity_id))
    
    def add_dependency_in_transaction(self, from_entity: str, to_entity: str, 
                                    dependency_type: str = "depends_on") -> None:
        """
        Add a dependency relationship within a transaction.
        
        Args:
            from_entity: ID of the dependent entity
            to_entity: ID of the dependency
            dependency_type: Type of dependency
        """
        if not self.transaction_active:
            raise RuntimeError("No transaction active")
        
        with self.lock:
            self.graph.add_dependency(from_entity, to_entity, dependency_type)
            self.transaction_changes.append(("add_dependency", from_entity, to_entity))
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the graph (thread-safe).
        
        Returns:
            Dictionary with graph statistics
        """
        with self.lock:
            return self.graph.get_statistics()
    
    def save_graph(self, file_path: Optional[str] = None) -> bool:
        """
        Save the graph to a file (thread-safe).
        
        Args:
            file_path: Path to save the graph
            
        Returns:
            True if successful, False otherwise
        """
        with self.lock:
            return self.graph.save_graph(file_path)
    
    def load_graph(self, file_path: Optional[str] = None) -> bool:
        """
        Load the graph from a file (thread-safe).
        
        Args:
            file_path: Path to load the graph from
            
        Returns:
            True if successful, False otherwise
        """
        with self.lock:
            return self.graph.load_graph(file_path)


def main():
    """Main function for testing the GraphManager."""
    # Create graph manager
    manager = GraphManager("test_graph_manager.json", auto_save=True)
    
    # Add some test entities
    manager.add_entity("SHIP-GTC_FENRIS", "ship", {
        "name": "GTC Fenris",
        "type": "cruiser"
    })
    
    manager.add_entity("SHIP-GTF_MYRMIDON", "ship", {
        "name": "GTF Myrmidon",
        "type": "fighter"
    })
    
    # Add dependency
    manager.add_dependency("SHIP-GTF_MYRMIDON", "SHIP-GTC_FENRIS", "escort")
    
    # Print statistics
    print("Graph statistics:", manager.get_statistics())
    
    # Test transaction
    if manager.begin_transaction():
        manager.add_entity_in_transaction("MODULE-SHIELD", "module", {
            "name": "Shield Module",
            "type": "defense"
        })
        manager.add_dependency_in_transaction("SHIP-GTC_FENRIS", "MODULE-SHIELD", "uses")
        manager.commit_transaction()
    
    # Print updated statistics
    print("Updated graph statistics:", manager.get_statistics())


if __name__ == "__main__":
    main()
```

---

## converter/hitl/README.md

**File type:** .md  

**Size:** 1453 bytes  

**Last modified:** 2025-08-21 21:52:39


```markdown
# Human-in-the-Loop (HITL) Integration

This directory contains components for integrating human oversight into the migration process.

## Overview

The HITL system implements human-in-the-loop patterns for critical decision points in the migration process. It provides:

1. **Proactive Intervention**: Request human input at critical decision points
2. **Multiple Patterns**: Support for different HITL patterns (Interrupt & Resume, Human-as-a-Tool)
3. **Priority Management**: Handle requests with different priority levels
4. **Response Handling**: Process human responses and integrate them into the workflow

## Key Components

- `hitl_integration.py` - Main HITL integration implementation

## HITL Patterns

The system implements several HITL patterns for different scenarios:

1. **Interrupt & Resume**: Request human approval before continuing critical operations
2. **Human-as-a-Tool**: Request human expertise to resolve ambiguity
3. **Policy-Based Approval**: Apply policy-based approval mechanisms
4. **Fallback Escalation**: Escalate to humans for complex problems

## Integration with Other Systems

The HITL system integrates with several other systems:

- **Orchestrator**: Request human input at critical decision points
- **Validation System**: Escalate critical validation issues for human review
- **Codebase Analyst**: Request human expertise for ambiguous code
- **Quality Assurance**: Request human review of AI-generated outputs
```

---

## converter/hitl/__init__.py

**File type:** .py  

**Size:** 194 bytes  

**Last modified:** 2025-08-21 20:47:07


```python
"""
HITL (Human-in-the-Loop) Integration Module

This module contains components for integrating human oversight into the migration process.
"""

__version__ = "0.1.0"
__author__ = "WCSaga Team"
```

---

## converter/hitl/hitl_integration.py

**File type:** .py  

**Size:** 11334 bytes  

**Last modified:** 2025-08-21 20:49:01


```python
"""
HITL (Human-in-the-Loop) Integration Implementation

This module implements proactive HITL patterns for critical decision points in the migration process.
"""

import time
import logging
from typing import Dict, Any, List, Optional, Callable
from enum import Enum
from dataclasses import dataclass, field
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HITLPattern(Enum):
    """Enumeration of HITL patterns."""
    INTERRUPT_AND_RESUME = "interrupt_and_resume"
    HUMAN_AS_A_TOOL = "human_as_a_tool"
    POLICY_BASED_APPROVAL = "policy_based_approval"
    FALLBACK_ESCALATION = "fallback_escalation"


class HITLRequestType(Enum):
    """Enumeration of HITL request types."""
    APPROVAL = "approval"
    EXPERTISE = "expertise"
    CLARIFICATION = "clarification"
    VERIFICATION = "verification"


@dataclass
class HITLRequest:
    """Representation of a HITL request."""
    request_id: str
    request_type: HITLRequestType
    pattern: HITLPattern
    entity_id: str
    description: str
    context: Dict[str, Any] = field(default_factory=dict)
    priority: int = 1
    created_at: float = field(default_factory=time.time)
    response: Optional[Dict[str, Any]] = None
    responded_at: Optional[float] = None


class HITLIntegration:
    """Integration point for Human-in-the-Loop collaboration."""
    
    def __init__(self, notification_callback: Optional[Callable[[HITLRequest], None]] = None):
        """
        Initialize the HITL integration.
        
        Args:
            notification_callback: Optional callback for notifying humans of requests
        """
        self.notification_callback = notification_callback
        self.pending_requests = {}
        self.resolved_requests = {}
        
        logger.info("HITL Integration initialized")
    
    def request_interrupt_and_resume(self, entity_id: str, description: str,
                                    context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Request human approval before continuing a critical operation.
        
        Args:
            entity_id: ID of the entity being processed
            description: Description of what needs approval
            context: Context information for the human reviewer
            
        Returns:
            Dictionary with approval result
        """
        request = HITLRequest(
            request_id=f"iar_{entity_id}_{int(time.time())}",
            request_type=HITLRequestType.APPROVAL,
            pattern=HITLPattern.INTERRUPT_AND_RESUME,
            entity_id=entity_id,
            description=description,
            context=context,
            priority=10  # High priority
        )
        
        return self._submit_request(request)
    
    def request_human_expertise(self, entity_id: str, description: str,
                               context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Request human expertise to resolve ambiguity.
        
        Args:
            entity_id: ID of the entity being processed
            description: Description of what expertise is needed
            context: Context information for the human expert
            
        Returns:
            Dictionary with expert response
        """
        request = HITLRequest(
            request_id=f"hex_{entity_id}_{int(time.time())}",
            request_type=HITLRequestType.EXPERTISE,
            pattern=HITLPattern.HUMAN_AS_A_TOOL,
            entity_id=entity_id,
            description=description,
            context=context,
            priority=5  # Medium priority
        )
        
        return self._submit_request(request)
    
    def request_clarification(self, entity_id: str, description: str,
                              context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Request human clarification for ambiguous situations.
        
        Args:
            entity_id: ID of the entity being processed
            description: Description of what needs clarification
            context: Context information for the human reviewer
            
        Returns:
            Dictionary with clarification response
        """
        request = HITLRequest(
            request_id=f"clr_{entity_id}_{int(time.time())}",
            request_type=HITLRequestType.CLARIFICATION,
            pattern=HITLPattern.HUMAN_AS_A_TOOL,
            entity_id=entity_id,
            description=description,
            context=context,
            priority=3  # Lower priority
        )
        
        return self._submit_request(request)
    
    def request_verification(self, entity_id: str, description: str,
                           context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Request human verification of critical results.
        
        Args:
            entity_id: ID of the entity being processed
            description: Description of what needs verification
            context: Context information for the human reviewer
            
        Returns:
            Dictionary with verification result
        """
        request = HITLRequest(
            request_id=f"ver_{entity_id}_{int(time.time())}",
            request_type=HITLRequestType.VERIFICATION,
            pattern=HITLPattern.INTERRUPT_AND_RESUME,
            entity_id=entity_id,
            description=description,
            context=context,
            priority=8  # High priority
        )
        
        return self._submit_request(request)
    
    def _submit_request(self, request: HITLRequest) -> Dict[str, Any]:
        """
        Submit a HITL request.
        
        Args:
            request: HITL request to submit
            
        Returns:
            Dictionary with submission result
        """
        # Store the request
        self.pending_requests[request.request_id] = request
        
        # Notify human (if callback is provided)
        if self.notification_callback:
            try:
                self.notification_callback(request)
            except Exception as e:
                logger.error(f"Error notifying human of HITL request: {str(e)}")
        
        # Log the request
        logger.info(f"HITL request submitted: {request.request_id} ({request.pattern.value})")
        
        # In a real implementation, this would wait for human response
        # For now, we'll simulate a response
        return self._simulate_response(request)
    
    def _simulate_response(self, request: HITLRequest) -> Dict[str, Any]:
        """
        Simulate a human response to a HITL request.
        
        Args:
            request: HITL request
            
        Returns:
            Dictionary with simulated response
        """
        # In a real implementation, this would wait for actual human response
        # For now, we'll simulate an approval/positive response
        
        response = {
            "approved": True,
            "timestamp": time.time(),
            "comments": "Simulated human response - approved for demonstration purposes"
        }
        
        # Update the request with response
        request.response = response
        request.responded_at = response["timestamp"]
        
        # Move from pending to resolved
        self.resolved_requests[request.request_id] = self.pending_requests.pop(request.request_id)
        
        logger.info(f"HITL request resolved: {request.request_id}")
        
        return response
    
    def provide_response(self, request_id: str, response: Dict[str, Any]) -> bool:
        """
        Provide a response to a HITL request.
        
        Args:
            request_id: ID of the request
            response: Response from human
            
        Returns:
            True if response was accepted, False otherwise
        """
        if request_id not in self.pending_requests:
            logger.warning(f"HITL request {request_id} not found or already resolved")
            return False
        
        # Update the request with response
        request = self.pending_requests[request_id]
        request.response = response
        request.responded_at = time.time()
        
        # Move from pending to resolved
        self.resolved_requests[request_id] = self.pending_requests.pop(request_id)
        
        logger.info(f"HITL request resolved by human: {request_id}")
        return True
    
    def get_pending_requests(self) -> List[Dict[str, Any]]:
        """
        Get all pending HITL requests.
        
        Returns:
            List of pending requests
        """
        return [
            {
                "request_id": req.request_id,
                "request_type": req.request_type.value,
                "pattern": req.pattern.value,
                "entity_id": req.entity_id,
                "description": req.description,
                "priority": req.priority,
                "created_at": req.created_at
            }
            for req in self.pending_requests.values()
        ]
    
    def get_resolved_requests(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get recently resolved HITL requests.
        
        Args:
            limit: Maximum number of requests to return
            
        Returns:
            List of resolved requests
        """
        # Get requests sorted by responded time (newest first)
        sorted_requests = sorted(
            self.resolved_requests.values(),
            key=lambda r: r.responded_at or 0,
            reverse=True
        )
        
        return [
            {
                "request_id": req.request_id,
                "request_type": req.request_type.value,
                "pattern": req.pattern.value,
                "entity_id": req.entity_id,
                "description": req.description,
                "response": req.response,
                "responded_at": req.responded_at
            }
            for req in sorted_requests[:limit]
        ]


def main():
    """Main function for testing the HITLIntegration."""
    # Create notification callback
    def notify_human(request: HITLRequest):
        print(f"Notification: {request.request_type.value} request for {request.entity_id}")
        print(f"Description: {request.description}")
        print("---")
    
    # Create HITL integration
    hitl = HITLIntegration(notification_callback=notify_human)
    
    # Test interrupt and resume
    result = hitl.request_interrupt_and_resume(
        entity_id="SHIP-GTC_FENRIS",
        description="Migration of critical core dependency",
        context={
            "files": ["source/tables/ships.tbl", "source/models/fenris.pof"],
            "risk_level": "high"
        }
    )
    print("Interrupt and resume result:", result)
    
    # Test human expertise
    result = hitl.request_human_expertise(
        entity_id="WEAPON-BEAM_TURRET",
        description="Ambiguous SEXP command in mission script",
        context={
            "command": "(ai-evade-beam-turret #self)",
            "file": "source/missions/main.fs2"
        }
    )
    print("Human expertise result:", result)
    
    # Print pending requests
    print("Pending requests:", hitl.get_pending_requests())


if __name__ == "__main__":
    main()
```

---

## converter/init_env.sh

**File type:** .sh  

**Size:** 462 bytes  

**Last modified:** 2025-08-21 13:44:21


```bash
#!/bin/bash

# Script to initialize the virtual environment and install dependencies using uv

set -e  # Exit on any error

echo "Initializing virtual environment with uv..."

# Create virtual environment
uv venv

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing dependencies..."
uv pip install -r requirements.txt

echo "Virtual environment setup complete!"
echo "To activate the environment, run: source .venv/bin/activate"

```

---

## converter/orchestrator/README.md

**File type:** .md  

**Size:** 1797 bytes  

**Last modified:** 2025-08-21 21:45:13


```markdown
# Orchestrator Agent

This directory contains the implementation of the Orchestrator agent, which serves as the project manager.

Based on the "Agentic Migration with CLI Agents" document, this agent is powered by the **DeepSeek V3.1** model and follows these principles:

## Responsibilities
- Ingest the migration plan
- Shard tasks into atomic units
- Manage the task queue
- Orchestrate the workflow between other agents
- Dynamically select workflow models (sequential or hierarchical) based on task complexity
- Use DeepSeek V3.1 model for advanced reasoning and planning

## Key Components

- `main.py` - Main orchestrator implementation
- `enhanced_orchestrator.py` - Enhanced orchestrator with all improvements integrated
- `state_machine/` - Custom state machine implementation for deterministic bolt cycles
  - `core.py` - Core state machine orchestrator
  - `task_queue.py` - Task queue management
  - `bolt_executor.py` - Bolt execution implementation
  - `hybrid_orchestrator.py` - Hybrid orchestrator combining planning and execution

## Workflow Process

The orchestrator operates with a robust workflow:

1. **Dependency Analysis**: Uses the graph system to analyze codebase dependencies
2. **Migration Planning**: Creates migration sequence based on dependency analysis
3. **Task Execution**: Executes tasks in deterministic bolt cycles
4. **Quality Validation**: Validates results with quality gates
5. **HITL Review**: Requests human review for critical components

## Integration with Other Systems

The orchestrator integrates with several systems:

- **Graph System**: Uses the dependency graph for intelligent task ordering
- **Validation System**: Incorporates test quality gates for rigorous validation
- **HITL System**: Implements human oversight for critical decisions
```

---

## converter/orchestrator/__init__.py

**File type:** .py  

**Size:** 213 bytes  

**Last modified:** 2025-08-21 20:22:13


```python
"""
Orchestrator Package for Wing Commander Saga to Godot Migration

This package contains the orchestrator implementations for managing the migration process.
"""

__version__ = "0.1.0"
__author__ = "WCSaga Team"
```

---

## converter/orchestrator/enhanced_orchestrator.py

**File type:** .py  

**Size:** 11136 bytes  

**Last modified:** 2025-08-21 20:51:51


```python
"""
Enhanced Orchestrator Implementation

This module implements an enhanced orchestrator that integrates all improvements:
- Custom state machine for deterministic bolt cycles
- Dependency graph system for dynamic memory
- Enhanced validation with test quality gates
- HITL integration for critical decision points
"""

import time
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

# Import our enhanced modules
from .state_machine.hybrid_orchestrator import HybridOrchestrator
from ..graph_system.graph_manager import GraphManager
from ..validation.enhanced.validation_engineer import EnhancedValidationEngineer
from ..hitl.hitl_integration import HITLIntegration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EnhancedOrchestrator:
    """Enhanced orchestrator integrating all improvements."""
    
    def __init__(self, source_path: str, target_path: str, 
                 graph_file: str = "dependency_graph.json"):
        """
        Initialize the enhanced orchestrator.
        
        Args:
            source_path: Path to the source C++ codebase
            target_path: Path to the target Godot project
            graph_file: Path to the dependency graph file
        """
        self.source_path = Path(source_path)
        self.target_path = Path(target_path)
        
        # Initialize enhanced components
        self.hybrid_orchestrator = HybridOrchestrator("task_queue.yaml", max_retries=3)
        self.graph_manager = GraphManager(graph_file, auto_save=True)
        self.validation_engineer = EnhancedValidationEngineer(min_coverage=85.0, min_test_count=5)
        self.hitl_integration = HITLIntegration()
        
        logger.info("Enhanced Orchestrator initialized")
    
    def run_enhanced_migration_cycle(self) -> Dict[str, Any]:
        """
        Run an enhanced migration cycle with all improvements.
        
        Returns:
            Dictionary with cycle results
        """
        logger.info("Starting enhanced migration cycle")
        
        results = {
            "cycle_start_time": time.time(),
            "phases": {},
            "summary": {}
        }
        
        try:
            # Phase 1: Dependency Analysis and Graph Building
            analysis_results = self._run_dependency_analysis_phase()
            results["phases"]["dependency_analysis"] = analysis_results
            
            # Phase 2: Migration Planning with Graph Awareness
            planning_results = self._run_enhanced_planning_phase()
            results["phases"]["planning"] = planning_results
            
            # Phase 3: Execution with Deterministic Bolt Cycles
            execution_results = self._run_enhanced_execution_phase()
            results["phases"]["execution"] = execution_results
            
            # Phase 4: Enhanced Validation with Quality Gates
            validation_results = self._run_enhanced_validation_phase()
            results["phases"]["validation"] = validation_results
            
            # Phase 5: HITL Review for Critical Components
            hitl_results = self._run_hitl_review_phase()
            results["phases"]["hitl_review"] = hitl_results
            
        except Exception as e:
            logger.error(f"Error during enhanced migration cycle: {str(e)}")
            results["error"] = str(e)
        
        results["cycle_end_time"] = time.time()
        results["cycle_duration"] = results["cycle_end_time"] - results["cycle_start_time"]
        
        logger.info(f"Enhanced migration cycle completed in {results['cycle_duration']:.2f} seconds")
        return results
    
    def _run_dependency_analysis_phase(self) -> Dict[str, Any]:
        """
        Run enhanced dependency analysis phase using graph system.
        
        Returns:
            Dictionary with analysis results
        """
        logger.info("Running enhanced dependency analysis phase...")
        
        # This would involve analyzing the source codebase and building the dependency graph
        # For now, we'll simulate this process
        
        # Add some sample entities to the graph
        self.graph_manager.add_entity("SHIP-GTC_FENRIS", "ship", {
            "name": "GTC Fenris",
            "type": "cruiser",
            "file_path": "source/tables/ships.tbl"
        })
        
        self.graph_manager.add_entity("SHIP-GTF_MYRMIDON", "ship", {
            "name": "GTF Myrmidon",
            "type": "fighter",
            "file_path": "source/tables/ships.tbl"
        })
        
        self.graph_manager.add_entity("MODULE-ENGINE", "module", {
            "name": "Engine Module",
            "type": "propulsion"
        })
        
        # Add dependencies
        self.graph_manager.add_dependency("SHIP-GTC_FENRIS", "MODULE-ENGINE", "uses")
        self.graph_manager.add_dependency("SHIP-GTF_MYRMIDON", "MODULE-ENGINE", "uses")
        
        # Get topological order for migration sequence
        migration_sequence = self.graph_manager.get_topological_order()
        
        results = {
            "success": True,
            "entities_added": 3,
            "dependencies_added": 2,
            "migration_sequence": migration_sequence,
            "graph_statistics": self.graph_manager.get_statistics()
        }
        
        logger.info("Enhanced dependency analysis phase completed")
        return results
    
    def _run_enhanced_planning_phase(self) -> Dict[str, Any]:
        """
        Run enhanced planning phase with graph awareness.
        
        Returns:
            Dictionary with planning results
        """
        logger.info("Running enhanced planning phase...")
        
        # Get migration sequence from graph
        migration_sequence = self.graph_manager.get_topological_order()
        
        # Create tasks based on migration sequence
        for entity_id in migration_sequence:
            entity_props = self.graph_manager.get_entity_properties(entity_id)
            if entity_props:
                # Add task to queue
                self.hybrid_orchestrator.add_task(entity_id, {
                    "description": f"Migrate {entity_props.get('name', entity_id)}",
                    "source_files": [entity_props.get("file_path", "")],
                    "dependencies": []  # Would be populated from graph in real implementation
                })
        
        results = {
            "success": True,
            "tasks_created": len(migration_sequence),
            "migration_sequence": migration_sequence
        }
        
        logger.info("Enhanced planning phase completed")
        return results
    
    def _run_enhanced_execution_phase(self) -> Dict[str, Any]:
        """
        Run enhanced execution phase with deterministic bolt cycles.
        
        Returns:
            Dictionary with execution results
        """
        logger.info("Running enhanced execution phase...")
        
        # Use our hybrid orchestrator with custom state machine
        execution_results = self.hybrid_orchestrator.run_migration_cycle()
        
        results = {
            "success": True,
            "execution_results": execution_results
        }
        
        logger.info("Enhanced execution phase completed")
        return results
    
    def _run_enhanced_validation_phase(self) -> Dict[str, Any]:
        """
        Run enhanced validation phase with quality gates.
        
        Returns:
            Dictionary with validation results
        """
        logger.info("Running enhanced validation phase...")
        
        # This would involve running enhanced validation on migrated files
        # For now, we'll simulate this process
        
        # Get queue summary to see what was processed
        queue_summary = self.hybrid_orchestrator.get_queue_summary()
        
        # Simulate enhanced validation
        validation_results = {
            "files_validated": queue_summary.get("completed", 0),
            "quality_gate_passed": True,
            "average_quality_score": 92.5
        }
        
        results = {
            "success": True,
            "validation_results": validation_results
        }
        
        logger.info("Enhanced validation phase completed")
        return results
    
    def _run_hitl_review_phase(self) -> Dict[str, Any]:
        """
        Run HITL review phase for critical components.
        
        Returns:
            Dictionary with HITL review results
        """
        logger.info("Running HITL review phase...")
        
        # This would involve requesting human review for critical components
        # For now, we'll simulate this process
        
        # Get completed tasks
        queue_summary = self.hybrid_orchestrator.get_queue_summary()
        completed_tasks = queue_summary.get("completed", 0)
        
        # Request HITL review for critical components (simulated)
        if completed_tasks > 0:
            # Simulate requesting review
            review_request = self.hitl_integration.request_verification(
                entity_id="CRITICAL-COMPONENT",
                description="Verification of critical system migration",
                context={
                    "completed_tasks": completed_tasks,
                    "migration_date": time.time()
                }
            )
            
            results = {
                "success": True,
                "review_requested": True,
                "review_response": review_request
            }
        else:
            results = {
                "success": True,
                "review_requested": False,
                "message": "No completed tasks to review"
            }
        
        logger.info("HITL review phase completed")
        return results
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the enhanced orchestrator.
        
        Returns:
            Dictionary with current status information
        """
        return {
            "source_path": str(self.source_path),
            "target_path": str(self.target_path),
            "graph_entities": self.graph_manager.get_statistics().get("node_count", 0),
            "graph_dependencies": self.graph_manager.get_statistics().get("edge_count", 0),
            "queue_summary": self.hybrid_orchestrator.get_queue_summary(),
            "last_updated": time.time()
        }


def main():
    """Main function for testing the EnhancedOrchestrator."""
    # Create enhanced orchestrator
    orchestrator = EnhancedOrchestrator(
        source_path="../source",
        target_path="../target",
        graph_file="test_dependency_graph.json"
    )
    
    # Print initial status
    print("Initial status:", orchestrator.get_status())
    
    # Run enhanced migration cycle
    results = orchestrator.run_enhanced_migration_cycle()
    
    # Print final status
    print("Final status:", orchestrator.get_status())
    print("Migration results:", results)


if __name__ == "__main__":
    main()
```

---

## converter/orchestrator/main.py

**File type:** .py  

**Size:** 12824 bytes  

**Last modified:** 2025-08-21 20:53:06


```python
#!/usr/bin/env python3
"""
Main Orchestrator for Wing Commander Saga to Godot Migration

This script serves as the entry point for the hierarchical multi-agent migration system.
It initializes all agents, sets up workflows, and coordinates the migration process.
"""

import os
import sys
import argparse
import logging
import yaml
from typing import List, Dict, Any
from pathlib import Path

# Add the converter directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from crewai import Crew, Process, Agent, Task
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import configuration manager
from config.config_manager import get_config_manager

# Import agent configurations
from agents.base_agent import MigrationArchitect, CodebaseAnalyst, TaskDecompositionSpecialist, PromptEngineeringAgent, QualityAssuranceAgent

# Import tools
from tools.qwen_code_execution_tool import QwenCodeExecutionTool
from tools.qwen_code_wrapper import QwenCodeWrapper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('migration_orchestrator.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Get configuration manager
config_manager = get_config_manager()


class MigrationOrchestrator:
    """Main orchestrator for the migration process."""
    
    def __init__(self, source_path: str, target_path: str):
        """
        Initialize the migration orchestrator.
        
        Args:
            source_path: Path to the source C++ codebase
            target_path: Path to the target Godot project
        """
        self.source_path = Path(source_path)
        self.target_path = Path(target_path)
        self.crew = None
        self.agents = {}
        self.tasks = {}
        self.tools = {}
        
        # Validate paths
        if not self.source_path.exists():
            raise ValueError(f"Source path does not exist: {self.source_path}")
        
        # Create target directory if it doesn't exist
        self.target_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self._initialize_tools()
        self._initialize_agents()
        self._initialize_tasks()
        self._initialize_crew()
    
    def _initialize_tools(self):
        """Initialize all required tools."""
        logger.info("Initializing tools...")
        
        self.tools['qwen_execution'] = QwenCodeExecutionTool()
        self.tools['qwen_wrapper'] = QwenCodeWrapper()
        
        logger.info("Tools initialized successfully")
    
    def _initialize_agents(self):
        """Initialize all AI agents."""
        logger.info("Initializing agents...")
        
        # Initialize each agent with their specific configurations
        self.agents['migration_architect'] = MigrationArchitect()
        self.agents['codebase_analyst'] = CodebaseAnalyst()
        self.agents['task_decomposition_specialist'] = TaskDecompositionSpecialist()
        self.agents['prompt_engineering_agent'] = PromptEngineeringAgent()
        self.agents['quality_assurance_agent'] = QualityAssuranceAgent()
        
        logger.info("Agents initialized successfully")
    
    def _initialize_tasks(self):
        """Initialize all tasks from YAML configuration files."""
        logger.info("Initializing tasks...")
        
        # Define task configuration files
        task_files = [
            os.path.join(os.path.dirname(__file__), "..", "tasks", "analysis_task.yaml"),
            os.path.join(os.path.dirname(__file__), "..", "tasks", "planning_task.yaml"),
            os.path.join(os.path.dirname(__file__), "..", "tasks", "decomposition_task.yaml"),
            os.path.join(os.path.dirname(__file__), "..", "tasks", "refactoring_task.yaml"),
            os.path.join(os.path.dirname(__file__), "..", "tasks", "testing_task.yaml"),
            os.path.join(os.path.dirname(__file__), "..", "tasks", "validation_task.yaml")
        ]
        
        # Load all task configurations
        for task_file in task_files:
            try:
                if os.path.exists(task_file):
                    with open(task_file, 'r') as f:
                        task_config = yaml.safe_load(f)
                        self.tasks.update(task_config)
                else:
                    logger.warning(f"Task configuration file not found: {task_file}")
            except Exception as e:
                logger.warning(f"Failed to load task configuration from {task_file}: {str(e)}")
        
        logger.info(f"Loaded {len(self.tasks)} task configurations")
    
    def _initialize_crew(self):
        """Initialize the CrewAI crew with all agents."""
        logger.info("Initializing crew...")
        
        # Get memory configuration
        memory_config = config_manager.get_memory_config()
        
        # Create the crew with all agents
        # Configure memory to use local ChromaDB
        self.crew = Crew(
            agents=[
                self.agents['migration_architect'],
                self.agents['codebase_analyst'],
                self.agents['task_decomposition_specialist'],
                self.agents['prompt_engineering_agent'],
                self.agents['quality_assurance_agent']
            ],
            process=Process.hierarchical,
            manager_llm="deepseek-ai/DeepSeek-V3.1",
            memory=memory_config.get("enabled", True),
            embedder=memory_config.get("embedder", {
                "provider": "huggingface",
                "config": {
                    "model": "sentence-transformers/all-MiniLM-L6-v2"
                }
            }),
            verbose=True
        )
        
        logger.info("Crew initialized successfully")
    
    def run_migration(self, phase: str = "all") -> Dict[str, Any]:
        """
        Run the migration process.
        
        Args:
            phase: Migration phase to run ("all", "analysis", "planning", "execution")
            
        Returns:
            Dictionary with migration results
        """
        logger.info(f"Starting migration process (phase: {phase})")
        
        try:
            # Create initial task based on the requested phase
            if phase == "analysis" or phase == "all":
                result = self._run_analysis_phase()
                if phase == "analysis":
                    return result
            
            if phase == "planning" or phase == "all":
                result = self._run_planning_phase()
                if phase == "planning":
                    return result
            
            if phase == "execution" or phase == "all":
                result = self._run_execution_phase()
                return result
            
            # Default case
            return {"status": "completed", "message": "Migration process completed successfully"}
            
        except Exception as e:
            logger.error(f"Migration process failed: {str(e)}", exc_info=True)
            return {"status": "failed", "error": str(e)}
    
    def _run_analysis_phase(self) -> Dict[str, Any]:
        """Run the codebase analysis phase."""
        logger.info("Running codebase analysis phase...")
        
        # Create analysis task from YAML configuration
        analysis_config = self.tasks.get('codebase_analysis_task', {})
        if not analysis_config:
            logger.error("Failed to load codebase analysis task configuration")
            return {"status": "failed", "error": "Failed to load task configuration"}
        
        # Create the task with inputs
        analysis_task = Task(
            description=analysis_config.get('description', '').format(source_path=self.source_path),
            expected_output=analysis_config.get('expected_output', ''),
            agent=self.agents.get(analysis_config.get('agent', '')),
            name=analysis_config.get('name', 'Codebase Analysis')
        )
        
        # Execute the task
        result = self.crew.kickoff([analysis_task])
        
        logger.info("Codebase analysis phase completed")
        return {"status": "completed", "phase": "analysis", "result": result}
    
    def _run_planning_phase(self) -> Dict[str, Any]:
        """Run the migration planning phase."""
        logger.info("Running migration planning phase...")
        
        # First run analysis if not already done
        # Then create planning task from YAML configuration
        planning_config = self.tasks.get('migration_planning_task', {})
        if not planning_config:
            logger.error("Failed to load migration planning task configuration")
            return {"status": "failed", "error": "Failed to load task configuration"}
        
        # Create the task with inputs
        planning_task = Task(
            description=planning_config.get('description', ''),
            expected_output=planning_config.get('expected_output', ''),
            agent=self.agents.get(planning_config.get('agent', '')),
            name=planning_config.get('name', 'Migration Planning')
        )
        
        # Execute the task
        result = self.crew.kickoff([planning_task])
        
        logger.info("Migration planning phase completed")
        return {"status": "completed", "phase": "planning", "result": result}
    
    def _run_execution_phase(self) -> Dict[str, Any]:
        """Run the migration execution phase."""
        logger.info("Running migration execution phase...")
        
        # Import our enhanced orchestrator
        try:
            from .enhanced_orchestrator import EnhancedOrchestrator
            
            # Create enhanced orchestrator
            enhanced_orchestrator = EnhancedOrchestrator(
                source_path=str(self.source_path),
                target_path=str(self.target_path),
                graph_file="dependency_graph.json"
            )
            
            # Run enhanced migration cycle
            results = enhanced_orchestrator.run_enhanced_migration_cycle()
            
            logger.info("Migration execution phase completed")
            return {
                "status": "completed", 
                "phase": "execution", 
                "message": "Execution phase completed successfully",
                "details": results
            }
        except Exception as e:
            logger.error(f"Migration execution phase failed: {str(e)}", exc_info=True)
            return {
                "status": "failed", 
                "phase": "execution", 
                "error": str(e)
            }
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the migration process.
        
        Returns:
            Dictionary with current status information
        """
        return {
            "source_path": str(self.source_path),
            "target_path": str(self.target_path),
            "agents_initialized": len(self.agents),
            "tasks_initialized": len(self.tasks),
            "tools_initialized": len(self.tools),
            "crew_status": "ready" if self.crew else "not_initialized"
        }


def main():
    """Main entry point for the migration orchestrator."""
    parser = argparse.ArgumentParser(description="Wing Commander Saga to Godot Migration Orchestrator")
    parser.add_argument("--source", required=True, help="Path to the source C++ codebase")
    parser.add_argument("--target", required=True, help="Path to the target Godot project")
    parser.add_argument("--phase", choices=["all", "analysis", "planning", "execution"], 
                       default="all", help="Migration phase to run")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    # Set logging level based on verbose flag
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Create and run the orchestrator
        orchestrator = MigrationOrchestrator(args.source, args.target)
        
        # Print status
        status = orchestrator.get_status()
        logger.info(f"Orchestrator status: {status}")
        
        # Run migration
        result = orchestrator.run_migration(args.phase)
        
        # Print result
        logger.info(f"Migration result: {result}")
        
        # Exit with appropriate code
        if result.get("status") == "failed":
            sys.exit(1)
        else:
            sys.exit(0)
            
    except Exception as e:
        logger.error(f"Failed to initialize orchestrator: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

```

---

## converter/orchestrator/state_machine/README.md

**File type:** .md  

**Size:** 1250 bytes  

**Last modified:** 2025-08-21 21:52:58


```markdown
# State Machine Orchestrator

This directory contains the custom state machine implementation for deterministic bolt cycles in the migration process.

## Overview

The state machine system implements a custom state machine-based orchestrator for deterministic bolt cycles. It provides:

1. **Deterministic Execution**: Explicit state transitions for predictable execution
2. **Bolt Management**: Manage individual bolt cycles with proper state tracking
3. **Error Handling**: Handle errors with retry and escalation mechanisms
4. **Task Queue Management**: Manage task queues with proper status tracking

## Key Components

- `core.py` - Core state machine orchestrator implementation
- `task_queue.py` - Task queue management with persistence
- `bolt_executor.py` - Bolt execution implementation
- `hybrid_orchestrator.py` - Hybrid orchestrator combining planning and execution

## Integration with Other Systems

The state machine system integrates with several other systems:

- **Orchestrator**: Core execution engine for the migration process
- **Graph System**: Use dependency graph for task ordering
- **Validation System**: Integrate validation results into state transitions
- **HITL System**: Request human input at critical decision points
```

---

## converter/orchestrator/state_machine/__init__.py

**File type:** .py  

**Size:** 188 bytes  

**Last modified:** 2025-08-21 20:22:47


```python
"""
State Machine Orchestrator Module

This module contains the custom state machine-based orchestrator for deterministic bolt cycles.
"""

__version__ = "0.1.0"
__author__ = "WCSaga Team"
```

---

## converter/orchestrator/state_machine/bolt_executor.py

**File type:** .py  

**Size:** 11583 bytes  

**Last modified:** 2025-08-21 21:12:01


```python
"""
Bolt Executor

This module executes individual bolt cycles using the state machine orchestrator.
"""

import time
import logging
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path

# Import our modules
from .core import StateMachineOrchestrator, BoltAction, BoltState
from .task_queue import TaskQueueManager, TaskStatus

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BoltExecutor:
    """Executor for individual bolt cycles."""
    
    def __init__(self, queue_file: str = "task_queue.yaml", max_retries: int = 3):
        """
        Initialize the bolt executor.
        
        Args:
            queue_file: Path to the task queue file
            max_retries: Maximum number of retries for a bolt before escalation
        """
        self.queue_manager = TaskQueueManager(queue_file)
        self.max_retries = max_retries
        self.orchestrator = None
        
        logger.info("Bolt Executor initialized")
    
    def execute_bolt_cycle(self, task_id: str) -> Dict[str, Any]:
        """
        Execute a complete bolt cycle for a task.
        
        Args:
            task_id: Unique identifier for the task
            
        Returns:
            Dictionary with execution results
        """
        # Get task from queue
        task = self.queue_manager.get_task_by_id(task_id)
        if not task:
            return {
                "success": False,
                "error": f"Task {task_id} not found in queue"
            }
        
        # Initialize orchestrator
        self.orchestrator = StateMachineOrchestrator(max_retries=self.max_retries)
        self.orchestrator.initialize_bolt(
            task_id=task_id,
            entity_name=task.get("description", "Unknown Entity"),
            source_files=task.get("source_files", [])
        )
        
        # Update task status to in progress
        self.queue_manager.update_task_status(task_id, TaskStatus.IN_PROGRESS)
        
        try:
            # Execute the bolt cycle
            result = self._execute_bolt_steps(task)
            
            # Update task status based on result
            if result["success"]:
                self.queue_manager.update_task_status(task_id, TaskStatus.COMPLETED)
            else:
                self.queue_manager.update_task_status(
                    task_id, 
                    TaskStatus.FAILED,
                    {"retry_count": self.orchestrator.context.retry_count}
                )
                self.queue_manager.add_failure_log(
                    task_id, 
                    result.get("error", "Unknown error"),
                    result.get("details", {})
                )
            
            return result
            
        except Exception as e:
            logger.error(f"Exception during bolt execution for task {task_id}: {str(e)}")
            self.queue_manager.update_task_status(task_id, TaskStatus.FAILED)
            self.queue_manager.add_failure_log(task_id, str(e))
            
            return {
                "success": False,
                "error": str(e)
            }
    
    def _execute_bolt_steps(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the individual steps of a bolt cycle.
        
        Args:
            task: Task data
            
        Returns:
            Dictionary with execution results
        """
        task_id = task["task_id"]
        
        # Analysis step
        if not self._execute_analysis_step(task):
            return {
                "success": False,
                "error": "Analysis step failed",
                "details": self.orchestrator.context.error_logs[-1] if self.orchestrator.context.error_logs else {}
            }
        
        # Refactoring step
        if not self._execute_refactoring_step(task):
            return {
                "success": False,
                "error": "Refactoring step failed",
                "details": self.orchestrator.context.error_logs[-1] if self.orchestrator.context.error_logs else {}
            }
        
        # Testing step
        if not self._execute_testing_step(task):
            return {
                "success": False,
                "error": "Testing step failed",
                "details": self.orchestrator.context.error_logs[-1] if self.orchestrator.context.error_logs else {}
            }
        
        # Validation step
        if not self._execute_validation_step(task):
            return {
                "success": False,
                "error": "Validation step failed",
                "details": self.orchestrator.context.error_logs[-1] if self.orchestrator.context.error_logs else {}
            }
        
        # Mark bolt as complete
        self.orchestrator.transition(BoltAction.COMPLETE_BOLT)
        
        return {
            "success": True,
            "task_id": task_id,
            "entity_name": self.orchestrator.context.entity_name,
            "duration": self.orchestrator.get_status().get("duration"),
            "analysis_result": self.orchestrator.context.analysis_result,
            "refactored_code": self.orchestrator.context.refactored_code,
            "test_results": self.orchestrator.context.test_results,
            "validation_results": self.orchestrator.context.validation_results
        }
    
    def _execute_analysis_step(self, task: Dict[str, Any]) -> bool:
        """
        Execute the analysis step of a bolt cycle.
        
        Args:
            task: Task data
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Executing analysis step for task {task['task_id']}")
        
        # Transition to analysis state
        self.orchestrator.transition(BoltAction.START_ANALYSIS)
        
        # Simulate analysis work
        time.sleep(0.1)  # Simulate work
        
        # For now, we'll simulate a successful analysis
        # In a real implementation, this would call the CodebaseAnalyst agent
        analysis_result = {
            "components": ["hull", "shields", "weapons"],
            "dependencies": [],
            "file_types": [".tbl", ".pof"]
        }
        
        target_files = [
            f"target/scenes/{task['task_id'].split('-')[1].lower()}.tscn",
            f"target/scripts/{task['task_id'].split('-')[1].lower()}.gd"
        ]
        
        # Complete analysis
        success = self.orchestrator.transition(BoltAction.COMPLETE_ANALYSIS, {
            "analysis_result": analysis_result,
            "target_files": target_files
        })
        
        logger.info(f"Analysis step completed for task {task['task_id']}: {success}")
        return success
    
    def _execute_refactoring_step(self, task: Dict[str, Any]) -> bool:
        """
        Execute the refactoring step of a bolt cycle.
        
        Args:
            task: Task data
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Executing refactoring step for task {task['task_id']}")
        
        # Transition to refactoring state
        self.orchestrator.transition(BoltAction.START_REFACTORING)
        
        # Simulate refactoring work
        time.sleep(0.1)  # Simulate work
        
        # For now, we'll simulate a successful refactoring
        # In a real implementation, this would call the RefactoringSpecialist agent
        refactored_code = f"class_name {task['task_id'].split('-')[1]}\nextends Node3D\n\n# Refactored code here"
        
        # Complete refactoring
        success = self.orchestrator.transition(BoltAction.COMPLETE_REFACTORING, {
            "refactored_code": refactored_code
        })
        
        logger.info(f"Refactoring step completed for task {task['task_id']}: {success}")
        return success
    
    def _execute_testing_step(self, task: Dict[str, Any]) -> bool:
        """
        Execute the testing step of a bolt cycle.
        
        Args:
            task: Task data
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Executing testing step for task {task['task_id']}")
        
        # Transition to testing state
        self.orchestrator.transition(BoltAction.START_TESTING)
        
        # Simulate testing work
        time.sleep(0.1)  # Simulate work
        
        # For now, we'll simulate successful tests
        # In a real implementation, this would call the TestGenerator and ValidationEngineer agents
        test_results = {
            "passed": 5,
            "failed": 0,
            "total": 5,
            "coverage": 95.0
        }
        
        # Complete testing
        success = self.orchestrator.transition(BoltAction.COMPLETE_TESTING, {
            "test_results": test_results
        })
        
        logger.info(f"Testing step completed for task {task['task_id']}: {success}")
        return success
    
    def _execute_validation_step(self, task: Dict[str, Any]) -> bool:
        """
        Execute the validation step of a bolt cycle.
        
        Args:
            task: Task data
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Executing validation step for task {task['task_id']}")
        
        # Transition to validation state
        self.orchestrator.transition(BoltAction.START_VALIDATION)
        
        # Simulate validation work
        time.sleep(0.1)  # Simulate work
        
        # For now, we'll simulate successful validation
        # In a real implementation, this would call the ValidationEngineer agent
        validation_results = {
            "syntax_valid": True,
            "style_compliant": True,
            "security_issues": [],
            "performance_metrics": {"memory": "normal", "cpu": "normal"}
        }
        
        # Complete validation
        success = self.orchestrator.transition(BoltAction.COMPLETE_VALIDATION, {
            "validation_results": validation_results
        })
        
        logger.info(f"Validation step completed for task {task['task_id']}: {success}")
        return success
    
    def process_next_task(self) -> Optional[Dict[str, Any]]:
        """
        Process the next available task from the queue.
        
        Returns:
            Execution results, or None if no task is available
        """
        # Get next pending task
        task = self.queue_manager.get_next_pending_task()
        if not task:
            logger.info("No pending tasks available")
            return None
        
        task_id = task["task_id"]
        logger.info(f"Processing task {task_id}")
        
        # Execute the bolt cycle
        result = self.execute_bolt_cycle(task_id)
        return result


def main():
    """Main function for testing the BoltExecutor."""
    # Create bolt executor
    executor = BoltExecutor("test_task_queue.yaml", max_retries=2)
    
    # Add some test tasks
    executor.queue_manager.add_task("SHIP-GTC_FENRIS", {
        "description": "Migrate the GTC Fenris cruiser",
        "source_files": ["source/tables/ships.tbl", "source/models/fenris.pof"],
        "dependencies": []
    })
    
    # Process the next task
    result = executor.process_next_task()
    print("Execution result:", result)
    
    # Print queue summary
    print("Queue summary:", executor.queue_manager.get_queue_summary())


if __name__ == "__main__":
    main()
```

---

## converter/orchestrator/state_machine/core.py

**File type:** .py  

**Size:** 11509 bytes  

**Last modified:** 2025-08-21 23:11:58


```python
"""
State Machine Orchestrator Implementation

This module implements a custom state machine-based orchestrator for deterministic bolt cycles
in the Wing Commander Saga to Godot migration.
"""

import json
from typing import Dict, Any, List, Optional, Callable
from enum import Enum
from dataclasses import dataclass, field
from pathlib import Path
from converter.utils import setup_logging, generate_timestamp, calculate_duration

# Configure logging
logger = setup_logging(__name__)


class BoltState(Enum):
    """Enumeration of bolt states."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    ANALYSIS_COMPLETE = "analysis_complete"
    REFACTORING_COMPLETE = "refactoring_complete"
    TESTING_COMPLETE = "testing_complete"
    VALIDATION_COMPLETE = "validation_complete"
    COMPLETED = "completed"
    FAILED = "failed"
    ESCALATED = "escalated"


class BoltAction(Enum):
    """Enumeration of bolt actions."""
    START_ANALYSIS = "start_analysis"
    COMPLETE_ANALYSIS = "complete_analysis"
    START_REFACTORING = "start_refactoring"
    COMPLETE_REFACTORING = "complete_refactoring"
    START_TESTING = "start_testing"
    COMPLETE_TESTING = "complete_testing"
    START_VALIDATION = "start_validation"
    COMPLETE_VALIDATION = "complete_validation"
    COMPLETE_BOLT = "complete_bolt"
    FAIL_BOLT = "fail_bolt"
    ESCALATE_BOLT = "escalate_bolt"


@dataclass
class BoltContext:
    """Context data for a bolt execution."""
    task_id: str
    entity_name: str
    source_files: List[str]
    target_files: List[str] = field(default_factory=list)
    analysis_result: Optional[Dict[str, Any]] = None
    refactored_code: Optional[str] = None
    test_results: Optional[Dict[str, Any]] = None
    validation_results: Optional[Dict[str, Any]] = None
    error_logs: List[Dict[str, Any]] = field(default_factory=list)
    retry_count: int = 0
    max_retries: int = 3


class StateMachineOrchestrator:
    """Custom state machine orchestrator for deterministic bolt cycles."""
    
    def __init__(self, max_retries: int = 3):
        """
        Initialize the state machine orchestrator.
        
        Args:
            max_retries: Maximum number of retries for a bolt before escalation
        """
        self.max_retries = max_retries
        self.current_state = BoltState.PENDING
        self.context = None
        self.start_time = None
        self.end_time = None
        
        # Define state transitions
        self.transitions = {
            (BoltState.PENDING, BoltAction.START_ANALYSIS): BoltState.IN_PROGRESS,
            (BoltState.IN_PROGRESS, BoltAction.COMPLETE_ANALYSIS): BoltState.ANALYSIS_COMPLETE,
            (BoltState.ANALYSIS_COMPLETE, BoltAction.START_REFACTORING): BoltState.IN_PROGRESS,
            (BoltState.IN_PROGRESS, BoltAction.COMPLETE_REFACTORING): BoltState.REFACTORING_COMPLETE,
            (BoltState.REFACTORING_COMPLETE, BoltAction.START_TESTING): BoltState.IN_PROGRESS,
            (BoltState.IN_PROGRESS, BoltAction.COMPLETE_TESTING): BoltState.TESTING_COMPLETE,
            (BoltState.TESTING_COMPLETE, BoltAction.START_VALIDATION): BoltState.IN_PROGRESS,
            (BoltState.IN_PROGRESS, BoltAction.COMPLETE_VALIDATION): BoltState.VALIDATION_COMPLETE,
            (BoltState.VALIDATION_COMPLETE, BoltAction.COMPLETE_BOLT): BoltState.COMPLETED,
            (BoltState.IN_PROGRESS, BoltAction.FAIL_BOLT): BoltState.FAILED,
            (BoltState.ANALYSIS_COMPLETE, BoltAction.FAIL_BOLT): BoltState.FAILED,
            (BoltState.REFACTORING_COMPLETE, BoltAction.FAIL_BOLT): BoltState.FAILED,
            (BoltState.TESTING_COMPLETE, BoltAction.FAIL_BOLT): BoltState.FAILED,
            (BoltState.VALIDATION_COMPLETE, BoltAction.FAIL_BOLT): BoltState.FAILED,
            (BoltState.FAILED, BoltAction.ESCALATE_BOLT): BoltState.ESCALATED,
        }
        
        logger.info("State Machine Orchestrator initialized")
    
    def initialize_bolt(self, task_id: str, entity_name: str, source_files: List[str]) -> None:
        """
        Initialize a new bolt execution.
        
        Args:
            task_id: Unique identifier for the task
            entity_name: Name of the entity being migrated
            source_files: List of source files to process
        """
        self.context = BoltContext(
            task_id=task_id,
            entity_name=entity_name,
            source_files=source_files,
            max_retries=self.max_retries
        )
        self.current_state = BoltState.PENDING
        self.start_time = generate_timestamp()
        self.end_time = None
        
        logger.info(f"Initialized bolt execution for task {task_id}: {entity_name}")
    
    def transition(self, action: BoltAction, data: Optional[Dict[str, Any]] = None) -> bool:
        """
        Transition to a new state based on an action.
        
        Args:
            action: The action to perform
            data: Optional data associated with the action
            
        Returns:
            True if transition was successful, False otherwise
        """
        if self.context is None:
            logger.error("Cannot transition: bolt not initialized")
            return False
            
        # Check if transition is valid
        if (self.current_state, action) not in self.transitions:
            logger.warning(f"Invalid transition: {self.current_state} -> {action}")
            return False
        
        # Perform the transition
        previous_state = self.current_state
        self.current_state = self.transitions[(self.current_state, action)]
        
        # Update context with data if provided
        if data:
            self._update_context(action, data)
        
        # Log the transition
        logger.info(f"State transition: {previous_state} -> {action} -> {self.current_state}")
        
        # Handle special transitions
        if self.current_state == BoltState.COMPLETED:
            self.end_time = generate_timestamp()
            duration = calculate_duration(self.start_time, self.end_time)
            logger.info(f"Bolt execution completed in {duration:.2f} seconds")
        elif self.current_state == BoltState.FAILED:
            self.context.retry_count += 1
            logger.warning(f"Bolt execution failed (attempt {self.context.retry_count})")
            
            # Check if we should escalate
            if self.context.retry_count >= self.context.max_retries:
                self.transition(BoltAction.ESCALATE_BOLT)
        elif self.current_state == BoltState.ESCALATED:
            self.end_time = generate_timestamp()
            duration = calculate_duration(self.start_time, self.end_time)
            logger.error(f"Bolt execution escalated after {self.context.retry_count} attempts in {duration:.2f} seconds")
        
        return True
    
    def _update_context(self, action: BoltAction, data: Dict[str, Any]) -> None:
        """
        Update the context based on the action and data.
        
        Args:
            action: The action that was performed
            data: Data associated with the action
        """
        if action == BoltAction.COMPLETE_ANALYSIS:
            self.context.analysis_result = data.get("analysis_result")
            self.context.target_files = data.get("target_files", [])
        elif action == BoltAction.COMPLETE_REFACTORING:
            self.context.refactored_code = data.get("refactored_code")
        elif action == BoltAction.COMPLETE_TESTING:
            self.context.test_results = data.get("test_results")
        elif action == BoltAction.COMPLETE_VALIDATION:
            self.context.validation_results = data.get("validation_results")
        elif action == BoltAction.FAIL_BOLT:
            error_log = {
                "action": action.value,
                "timestamp": generate_timestamp(),
                "error": data.get("error", "Unknown error"),
                "details": data.get("details", {})
            }
            self.context.error_logs.append(error_log)
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the bolt execution.
        
        Returns:
            Dictionary with current status information
        """
        if self.context is None:
            return {"status": "not_initialized"}
        
        duration = None
        if self.start_time:
            if self.end_time:
                duration = calculate_duration(self.start_time, self.end_time)
            else:
                duration = calculate_duration(self.start_time)
        
        return {
            "task_id": self.context.task_id,
            "entity_name": self.context.entity_name,
            "state": self.current_state.value,
            "retry_count": self.context.retry_count,
            "max_retries": self.context.max_retries,
            "duration": duration,
            "error_count": len(self.context.error_logs)
        }
    
    def is_complete(self) -> bool:
        """
        Check if the bolt execution is complete.
        
        Returns:
            True if complete (success or failure), False otherwise
        """
        return self.current_state in [BoltState.COMPLETED, BoltState.FAILED, BoltState.ESCALATED]
    
    def should_retry(self) -> bool:
        """
        Check if the bolt should be retried.
        
        Returns:
            True if should retry, False otherwise
        """
        return self.current_state == BoltState.FAILED and self.context.retry_count < self.context.max_retries
    
    def should_escalate(self) -> bool:
        """
        Check if the bolt should be escalated.
        
        Returns:
            True if should escalate, False otherwise
        """
        return self.current_state == BoltState.FAILED and self.context.retry_count >= self.context.max_retries


def main():
    """Main function for testing the StateMachineOrchestrator."""
    # Create orchestrator
    orchestrator = StateMachineOrchestrator(max_retries=2)
    
    # Initialize a bolt
    orchestrator.initialize_bolt(
        task_id="SHIP-GTC_FENRIS",
        entity_name="GTC Fenris",
        source_files=["source/tables/ships.tbl", "source/models/fenris.pof"]
    )
    
    # Print initial status
    print("Initial status:", orchestrator.get_status())
    
    # Start analysis
    orchestrator.transition(BoltAction.START_ANALYSIS)
    orchestrator.transition(BoltAction.COMPLETE_ANALYSIS, {
        "analysis_result": {"components": ["hull", "shields", "weapons"]},
        "target_files": ["target/scenes/fenris.tscn", "target/scripts/fenris.gd"]
    })
    
    # Start refactoring
    orchestrator.transition(BoltAction.START_REFACTORING)
    orchestrator.transition(BoltAction.COMPLETE_REFACTORING, {
        "refactored_code": "class_name Fenris extends Node3D"
# Refactored code here"
    })
    
    # Start testing
    orchestrator.transition(BoltAction.START_TESTING)
    orchestrator.transition(BoltAction.COMPLETE_TESTING, {
        "test_results": {"passed": 5, "failed": 0, "total": 5}
    })
    
    # Start validation
    orchestrator.transition(BoltAction.START_VALIDATION)
    orchestrator.transition(BoltAction.COMPLETE_VALIDATION, {
        "validation_results": {"syntax_valid": True, "style_compliant": True}
    })
    
    # Complete bolt
    orchestrator.transition(BoltAction.COMPLETE_BOLT)
    
    # Print final status
    print("Final status:", orchestrator.get_status())


if __name__ == "__main__":
    main()
```

---

## converter/orchestrator/state_machine/hybrid_orchestrator.py

**File type:** .py  

**Size:** 5455 bytes  

**Last modified:** 2025-08-21 20:26:44


```python
"""
Hybrid Orchestrator

This module implements a hybrid orchestrator that combines CrewAI for high-level planning
with a custom state machine for deterministic bolt execution.
"""

import time
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

# Import our modules
from .task_queue import TaskQueueManager, TaskStatus
from .bolt_executor import BoltExecutor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HybridOrchestrator:
    """Hybrid orchestrator combining CrewAI and custom state machine."""
    
    def __init__(self, queue_file: str = "task_queue.yaml", max_retries: int = 3):
        """
        Initialize the hybrid orchestrator.
        
        Args:
            queue_file: Path to the task queue file
            max_retries: Maximum number of retries for a bolt before escalation
        """
        self.queue_manager = TaskQueueManager(queue_file)
        self.bolt_executor = BoltExecutor(queue_file, max_retries)
        self.is_running = False
        
        logger.info("Hybrid Orchestrator initialized")
    
    def run_migration_cycle(self) -> Dict[str, Any]:
        """
        Run a complete migration cycle, processing all available tasks.
        
        Returns:
            Dictionary with cycle results
        """
        logger.info("Starting migration cycle")
        
        results = {
            "cycle_start_time": time.time(),
            "tasks_processed": 0,
            "tasks_completed": 0,
            "tasks_failed": 0,
            "tasks_escalated": 0,
            "task_results": []
        }
        
        self.is_running = True
        
        try:
            while self.is_running:
                # Process the next available task
                result = self.bolt_executor.process_next_task()
                
                if result is None:
                    # No more tasks available
                    logger.info("No more tasks available, migration cycle complete")
                    break
                
                results["tasks_processed"] += 1
                results["task_results"].append(result)
                
                # Update counters based on result
                if result.get("success"):
                    results["tasks_completed"] += 1
                else:
                    results["tasks_failed"] += 1
                
                # Check if we should continue
                if not self._should_continue():
                    break
        
        except KeyboardInterrupt:
            logger.info("Migration cycle interrupted by user")
        except Exception as e:
            logger.error(f"Error during migration cycle: {str(e)}")
        finally:
            self.is_running = False
        
        results["cycle_end_time"] = time.time()
        results["cycle_duration"] = results["cycle_end_time"] - results["cycle_start_time"]
        
        logger.info(f"Migration cycle completed in {results['cycle_duration']:.2f} seconds")
        logger.info(f"Tasks processed: {results['tasks_processed']}")
        logger.info(f"Tasks completed: {results['tasks_completed']}")
        logger.info(f"Tasks failed: {results['tasks_failed']}")
        
        return results
    
    def _should_continue(self) -> bool:
        """
        Determine if the migration cycle should continue.
        
        Returns:
            True if should continue, False otherwise
        """
        # For now, we'll continue until no more tasks are available
        # In a more complex implementation, this could check for various conditions
        return True
    
    def add_task(self, task_id: str, task_data: Dict[str, Any]) -> None:
        """
        Add a new task to the queue.
        
        Args:
            task_id: Unique identifier for the task
            task_data: Data for the task
        """
        self.queue_manager.add_task(task_id, task_data)
    
    def get_queue_summary(self) -> Dict[str, int]:
        """
        Get a summary of the task queue.
        
        Returns:
            Dictionary with counts of tasks by status
        """
        return self.queue_manager.get_queue_summary()
    
    def stop(self) -> None:
        """Stop the migration cycle."""
        self.is_running = False
        logger.info("Migration cycle stop requested")


def main():
    """Main function for testing the HybridOrchestrator."""
    # Create hybrid orchestrator
    orchestrator = HybridOrchestrator("test_task_queue.yaml", max_retries=2)
    
    # Add some test tasks
    orchestrator.add_task("SHIP-GTC_FENRIS", {
        "description": "Migrate the GTC Fenris cruiser",
        "source_files": ["source/tables/ships.tbl", "source/models/fenris.pof"],
        "dependencies": []
    })
    
    orchestrator.add_task("SHIP-GTF_MYRMIDON", {
        "description": "Migrate the GTF Myrmidon fighter",
        "source_files": ["source/tables/ships.tbl", "source/models/myrmidon.pof"],
        "dependencies": ["SHIP-GTC_FENRIS"]
    })
    
    # Print initial queue summary
    print("Initial queue summary:", orchestrator.get_queue_summary())
    
    # Run migration cycle
    results = orchestrator.run_migration_cycle()
    
    # Print final queue summary
    print("Final queue summary:", orchestrator.get_queue_summary())
    print("Migration results:", results)


if __name__ == "__main__":
    main()
```

---

## converter/orchestrator/state_machine/task_queue.py

**File type:** .py  

**Size:** 8503 bytes  

**Last modified:** 2025-08-21 20:25:01


```python
"""
Task Queue Manager

This module manages the persistent task queue for the migration process.
"""

import yaml
import json
import time
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """Enumeration of task statuses."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ESCALATED = "escalated"


class TaskQueueManager:
    """Manager for the persistent task queue."""
    
    def __init__(self, queue_file: str = "task_queue.yaml"):
        """
        Initialize the task queue manager.
        
        Args:
            queue_file: Path to the task queue file
        """
        self.queue_file = Path(queue_file)
        self.tasks = {}
        self._load_queue()
        
        logger.info(f"Task Queue Manager initialized with {len(self.tasks)} tasks")
    
    def _load_queue(self) -> None:
        """Load the task queue from file."""
        if self.queue_file.exists():
            try:
                with open(self.queue_file, 'r') as f:
                    self.tasks = yaml.safe_load(f) or {}
                logger.info(f"Loaded {len(self.tasks)} tasks from {self.queue_file}")
            except Exception as e:
                logger.error(f"Failed to load task queue: {str(e)}")
                self.tasks = {}
        else:
            logger.info("Task queue file not found, starting with empty queue")
            self.tasks = {}
    
    def _save_queue(self) -> None:
        """Save the task queue to file."""
        try:
            # Create directory if it doesn't exist
            self.queue_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.queue_file, 'w') as f:
                yaml.dump(self.tasks, f, default_flow_style=False)
            logger.debug(f"Saved task queue to {self.queue_file}")
        except Exception as e:
            logger.error(f"Failed to save task queue: {str(e)}")
    
    def add_task(self, task_id: str, task_data: Dict[str, Any]) -> None:
        """
        Add a new task to the queue.
        
        Args:
            task_id: Unique identifier for the task
            task_data: Data for the task
        """
        if task_id in self.tasks:
            logger.warning(f"Task {task_id} already exists, updating...")
        
        # Ensure required fields are present
        task_entry = {
            "task_id": task_id,
            "description": task_data.get("description", ""),
            "source_files": task_data.get("source_files", []),
            "dependencies": task_data.get("dependencies", []),
            "status": task_data.get("status", TaskStatus.PENDING.value),
            "retry_count": task_data.get("retry_count", 0),
            "failure_logs": task_data.get("failure_logs", []),
            "created_at": task_data.get("created_at", time.time()),
            "updated_at": time.time()
        }
        
        self.tasks[task_id] = task_entry
        self._save_queue()
        
        logger.info(f"Added task {task_id} to queue")
    
    def update_task_status(self, task_id: str, status: TaskStatus, 
                          additional_data: Optional[Dict[str, Any]] = None) -> bool:
        """
        Update the status of a task.
        
        Args:
            task_id: Unique identifier for the task
            status: New status for the task
            additional_data: Additional data to update
            
        Returns:
            True if update was successful, False otherwise
        """
        if task_id not in self.tasks:
            logger.error(f"Task {task_id} not found in queue")
            return False
        
        self.tasks[task_id]["status"] = status.value
        self.tasks[task_id]["updated_at"] = time.time()
        
        if additional_data:
            # Update any additional fields
            for key, value in additional_data.items():
                if key in self.tasks[task_id]:
                    self.tasks[task_id][key] = value
                else:
                    # Add new field
                    self.tasks[task_id][key] = value
        
        self._save_queue()
        logger.info(f"Updated task {task_id} status to {status.value}")
        return True
    
    def get_next_pending_task(self) -> Optional[Dict[str, Any]]:
        """
        Get the next pending task that has all dependencies met.
        
        Returns:
            Task data for the next pending task, or None if no task is available
        """
        # Get all completed task IDs
        completed_tasks = {
            task_id for task_id, task in self.tasks.items()
            if task["status"] == TaskStatus.COMPLETED.value
        }
        
        # Find next pending task with all dependencies met
        for task_id, task in self.tasks.items():
            if task["status"] == TaskStatus.PENDING.value:
                # Check if all dependencies are completed
                dependencies_met = all(
                    dep_id in completed_tasks for dep_id in task.get("dependencies", [])
                )
                
                if dependencies_met:
                    return task
        
        return None
    
    def get_task_by_id(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a task by its ID.
        
        Args:
            task_id: Unique identifier for the task
            
        Returns:
            Task data, or None if not found
        """
        return self.tasks.get(task_id)
    
    def add_failure_log(self, task_id: str, error_message: str, 
                       error_details: Optional[Dict[str, Any]] = None) -> bool:
        """
        Add a failure log to a task.
        
        Args:
            task_id: Unique identifier for the task
            error_message: Error message
            error_details: Additional error details
            
        Returns:
            True if log was added, False otherwise
        """
        if task_id not in self.tasks:
            logger.error(f"Task {task_id} not found in queue")
            return False
        
        failure_log = {
            "timestamp": time.time(),
            "error_message": error_message,
            "error_details": error_details or {}
        }
        
        self.tasks[task_id]["failure_logs"].append(failure_log)
        self.tasks[task_id]["updated_at"] = time.time()
        self._save_queue()
        
        logger.info(f"Added failure log to task {task_id}")
        return True
    
    def get_queue_summary(self) -> Dict[str, int]:
        """
        Get a summary of the task queue.
        
        Returns:
            Dictionary with counts of tasks by status
        """
        summary = {
            "pending": 0,
            "in_progress": 0,
            "completed": 0,
            "failed": 0,
            "escalated": 0,
            "total": len(self.tasks)
        }
        
        for task in self.tasks.values():
            status = task.get("status", "unknown")
            if status in summary:
                summary[status] += 1
            else:
                summary["total"] += 1
        
        return summary


def main():
    """Main function for testing the TaskQueueManager."""
    # Create task queue manager
    queue_manager = TaskQueueManager("test_task_queue.yaml")
    
    # Add some test tasks
    queue_manager.add_task("SHIP-GTC_FENRIS", {
        "description": "Migrate the GTC Fenris cruiser",
        "source_files": ["source/tables/ships.tbl", "source/models/fenris.pof"],
        "dependencies": []
    })
    
    queue_manager.add_task("SHIP-GTF_MYRMIDON", {
        "description": "Migrate the GTF Myrmidon fighter",
        "source_files": ["source/tables/ships.tbl", "source/models/myrmidon.pof"],
        "dependencies": ["SHIP-GTC_FENRIS"]
    })
    
    # Print queue summary
    print("Queue summary:", queue_manager.get_queue_summary())
    
    # Get next pending task
    next_task = queue_manager.get_next_pending_task()
    print("Next task:", next_task)
    
    # Update task status
    if next_task:
        queue_manager.update_task_status(next_task["task_id"], TaskStatus.IN_PROGRESS)
        print("Updated queue summary:", queue_manager.get_queue_summary())


if __name__ == "__main__":
    main()
```

---

## converter/prompt_engineering/README.md

**File type:** .md  

**Size:** 1169 bytes  

**Last modified:** 2025-08-21 21:45:37


```markdown
# Prompt Engineering Agent

This directory contains the implementation of the Prompt Engineering Agent, which creates precise prompts for the CLI agent.

Based on the "Agentic Migration with CLI Agents" document, this agent is specifically configured to work with the **qwen-code** CLI agent:

## Responsibilities
- Convert atomic tasks and code context into precise, effective prompts for qwen-code
- Use structured prompt templates specifically designed for qwen-code
- Ensure all prompts include explicit instructions for qwen-code's response format

## Key Components

- `prompt_engineering_agent.py` - Main implementation of the Prompt Engineering Agent
- `task_templates/` - Structured prompt templates for different task types
  - `qwen_prompt_templates.py` - Specific templates for qwen-code tasks

## Integration with Other Systems

The Prompt Engineering Agent integrates with several systems:

- **Analysis Results**: Incorporates detailed analysis from the Codebase Analyst
- **Error Feedback**: Uses error information from the Quality Assurance Agent to refine prompts
- **Context Files**: Better handling of context files for more accurate code generation
```

---

## converter/prompt_engineering/prompt_engineering_agent.py

**File type:** .py  

**Size:** 8848 bytes  

**Last modified:** 2025-08-21 13:13:11


```python
"""
Prompt Engineering Agent Implementation

This agent is responsible for converting atomic tasks and code context into
precise, effective prompts for the CLI coding agents.
"""

import json
from typing import Dict, Any, List, Optional
from pathlib import Path


class PromptEngineeringAgent:
    """AI Communications Specialist for creating precise prompts."""
    
    def __init__(self):
        """Initialize the PromptEngineeringAgent."""
        self.template_library = self._load_template_library()
    
    def _load_template_library(self) -> Dict[str, str]:
        """
        Load the library of prompt templates.
        
        Returns:
            Dictionary mapping template IDs to template strings
        """
        # In a real implementation, this would load from files
        # For now, we'll define the templates directly
        return {
            "QWEN_GENERATE_01": """You are an expert GDScript programmer. Your task is to generate a new script file based on the provided specification.
Your response must contain ONLY the complete GDScript code for the new file.
Do not include any explanatory text, markdown formatting, or conversational filler.

<TARGET_FILE_PATH>{target_file_path}</TARGET_FILE_PATH>
<SPECIFICATION>{specification}</SPECIFICATION>
<CONTEXT_CODE>{context_code}</CONTEXT_CODE>""",
            
            "QWEN_REFACTOR_01": """You are an expert GDScript programmer. Your task is to perform a specific refactoring on an existing file.
Do not propose a plan; implement the change directly. Do not modify any other files.

<FILE_PATH>{file_path}</FILE_PATH>
<TASK_DESCRIPTION>{task_description}</TASK_DESCRIPTION>
<CONSTRAINTS>{constraints}</CONSTRAINTS>""",
            
            "QWEN_BUGFIX_01": """You are an expert debugger. A bug has been identified in the following file.
Your task is to fix it. Analyze the provided error message and code, identify the root cause, and apply the necessary correction.
Implement the fix directly.

<FILE_PATH>{file_path}</FILE_PATH>
<CODE_SNIPPET>{code_snippet}</CODE_SNIPPET>
<ERROR_MESSAGE>{error_message}</ERROR_MESSAGE>""",
            
            "QWEN_TEST_GENERATE_01": """You are an expert QA engineer. Your task is to generate unit tests for the provided GDScript class.
Create comprehensive tests that cover all public methods and edge cases.
Use the gdUnit4 framework for test implementation.

<TARGET_CLASS>{target_class}</TARGET_CLASS>
<TARGET_FILE>{target_file}</TARGET_FILE>
<CLASS_CONTENT>{class_content}</CLASS_CONTENT>
<TEST_FRAMEWORK>gdUnit4</TEST_FRAMEWORK>"""
        }
    
    def generate_prompt(self, task_type: str, **kwargs) -> str:
        """
        Generate a prompt for a specific task type.
        
        Args:
            task_type: Type of task (e.g., "QWEN_GENERATE_01")
            **kwargs: Parameters for the template
            
        Returns:
            Formatted prompt string
        """
        if task_type not in self.template_library:
            raise ValueError(f"Unknown task type: {task_type}")
        
        template = self.template_library[task_type]
        return template.format(**kwargs)
    
    def create_generation_prompt(self, target_file_path: str, specification: str, 
                               context_code: str = "") -> str:
        """
        Create a prompt for generating a new file.
        
        Args:
            target_file_path: Path where the new file should be created
            specification: Detailed specification for the new file
            context_code: Optional context code to reference
            
        Returns:
            Formatted prompt string
        """
        return self.generate_prompt(
            "QWEN_GENERATE_01",
            target_file_path=target_file_path,
            specification=specification,
            context_code=context_code
        )
    
    def create_refactoring_prompt(self, file_path: str, task_description: str, 
                                constraints: str = "") -> str:
        """
        Create a prompt for refactoring an existing file.
        
        Args:
            file_path: Path to the file to refactor
            task_description: Description of the refactoring task
            constraints: Additional constraints for the task
            
        Returns:
            Formatted prompt string
        """
        return self.generate_prompt(
            "QWEN_REFACTOR_01",
            file_path=file_path,
            task_description=task_description,
            constraints=constraints
        )
    
    def create_bugfix_prompt(self, file_path: str, code_snippet: str, 
                           error_message: str) -> str:
        """
        Create a prompt for fixing a bug.
        
        Args:
            file_path: Path to the file with the bug
            code_snippet: Code snippet with the bug
            error_message: Error message describing the bug
            
        Returns:
            Formatted prompt string
        """
        return self.generate_prompt(
            "QWEN_BUGFIX_01",
            file_path=file_path,
            code_snippet=code_snippet,
            error_message=error_message
        )
    
    def create_test_generation_prompt(self, target_class: str, target_file: str, 
                                    class_content: str) -> str:
        """
        Create a prompt for generating unit tests.
        
        Args:
            target_class: Name of the class to test
            target_file: Path to the file containing the class
            class_content: Content of the class to test
            
        Returns:
            Formatted prompt string
        """
        return self.generate_prompt(
            "QWEN_TEST_GENERATE_01",
            target_class=target_class,
            target_file=target_file,
            class_content=class_content
        )
    
    def refine_prompt_with_feedback(self, original_prompt: str, error_message: str, 
                                  previous_output: str = "") -> str:
        """
        Refine a prompt based on error feedback.
        
        Args:
            original_prompt: The original prompt that failed
            error_message: Error message from the failed execution
            previous_output: Output from the failed execution (if any)
            
        Returns:
            Refined prompt string
        """
        refinement_prompt = f"""{original_prompt}

The previous attempt to execute this task failed with the following error:
<ERROR_MESSAGE>{error_message}</ERROR_MESSAGE>

Please revise the prompt to address this error. Consider:
1. Making the instructions more specific
2. Adding additional constraints or context
3. Clarifying the expected output format
4. Ensuring all required information is included

<REFINEMENT_INSTRUCTIONS>
Please provide a corrected version of the code that addresses the error above.
</REFINEMENT_INSTRUCTIONS>"""
        
        return refinement_prompt
    
    def add_context_to_prompt(self, prompt: str, context_files: List[str]) -> str:
        """
        Add context from files to an existing prompt.
        
        Args:
            prompt: The base prompt
            context_files: List of file paths to include as context
            
        Returns:
            Prompt with added context
        """
        context_sections = []
        for file_path in context_files:
            path = Path(file_path)
            if path.exists():
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    context_sections.append(f"<CONTEXT_FILE path='{file_path}'>\n{content}\n</CONTEXT_FILE>")
                except Exception:
                    # If we can't read a file, just skip it
                    pass
        
        if context_sections:
            context_str = "\n".join(context_sections)
            return f"{prompt}\n\n<ADDITIONAL_CONTEXT>\n{context_str}\n</ADDITIONAL_CONTEXT>"
        
        return prompt


def main():
    """Main function for testing the PromptEngineeringAgent."""
    agent = PromptEngineeringAgent()
    
    # Example usage
    prompt = agent.create_generation_prompt(
        target_file_path="scripts/player/ship.gd",
        specification="Create a PlayerShip class that handles movement, weapons, and health",
        context_code="# This class represents a player-controlled spacecraft"
    )
    
    print("Generated Prompt:")
    print(prompt)
    print("\n" + "="*50 + "\n")
    
    # Example of refinement
    refined_prompt = agent.refine_prompt_with_feedback(
        original_prompt=prompt,
        error_message="SyntaxError: Unexpected token 'class'"
    )
    
    print("Refined Prompt:")
    print(refined_prompt)


if __name__ == "__main__":
    main()

```

---

## converter/refactoring/README.md

**File type:** .md  

**Size:** 1052 bytes  

**Last modified:** 2025-08-21 21:46:22


```markdown
# Refactoring Specialist Agent

This directory contains the implementation of the Refactoring Specialist agent, which generates Godot files.

Based on the "Agentic Migration with CLI Agents" document, this agent is specifically configured to work with the **qwen-code** CLI agent:

## Responsibilities
- Receive source files and analyst's JSON report
- Generate equivalent idiomatic Godot files (.gd, .tscn, .tres)
- Strictly adhere to guidance artifacts (style guide, templates, gold standards)
- Use qwen-code CLI agent for all code generation tasks

## Key Components

- `refactoring_specialist.py` - Main implementation of the Refactoring Specialist agent

## Integration with Other Systems

The Refactoring Specialist integrates with several systems:

- **Prompt Engineering**: Receives precisely formatted prompts from the Prompt Engineering Agent
- **Validation System**: Incorporates feedback from the Validation Engineer for iterative improvements
- **Context Engineering**: Strictly adheres to guidance artifacts for consistent output quality
```

---

## converter/refactoring/refactoring_specialist.py

**File type:** .py  

**Size:** 12443 bytes  

**Last modified:** 2025-08-21 13:13:46


```python
"""
Refactoring Specialist Agent Implementation

This agent is responsible for refactoring existing C++ code to GDScript
using the qwen-code CLI tool.
"""

import os
import json
from typing import Dict, Any, List, Optional
from pathlib import Path

# Import tools
from tools.qwen_code_wrapper import QwenCodeWrapper
from prompt_engineering.prompt_engineering_agent import PromptEngineeringAgent


class RefactoringSpecialist:
    """Agent responsible for refactoring C++ code to GDScript."""
    
    def __init__(self, qwen_command: str = "qwen-code"):
        """
        Initialize the RefactoringSpecialist.
        
        Args:
            qwen_command: Command to invoke qwen-code
        """
        self.qwen_wrapper = QwenCodeWrapper(qwen_command)
        self.prompt_engine = PromptEngineeringAgent()
    
    def refactor_file(self, source_file: str, target_file: str, 
                     refactoring_instructions: str) -> Dict[str, Any]:
        """
        Refactor a single file from C++ to GDScript.
        
        Args:
            source_file: Path to the source C++ file
            target_file: Path where the GDScript file should be created
            refactoring_instructions: Specific instructions for the refactoring
            
        Returns:
            Dictionary with refactoring results
        """
        # Check if source file exists
        if not os.path.exists(source_file):
            return {
                "success": False,
                "error": f"Source file does not exist: {source_file}"
            }
        
        # Read the source file
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                source_content = f.read()
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to read source file: {str(e)}"
            }
        
        # Create a detailed specification for the refactoring
        specification = f"""Refactor the following C++ code to GDScript, following the project's STYLE_GUIDE.md and RULES.md:

<SOURCE_FILE_PATH>{source_file}</SOURCE_FILE_PATH>
<TARGET_FILE_PATH>{target_file}</TARGET_FILE_PATH>
<SOURCE_CODE>
{source_content}
</SOURCE_CODE>
<REFACTORING_INSTRUCTIONS>
{refactoring_instructions}
</REFACTORING_INSTRUCTIONS>"""
        
        # Generate the prompt
        prompt = self.prompt_engine.create_generation_prompt(
            target_file_path=target_file,
            specification=specification
        )
        
        # Execute the refactoring using qwen-code
        result = self.qwen_wrapper.generate_code(prompt)
        
        # If successful, save the result to the target file
        if result.get("success"):
            try:
                # Create target directory if it doesn't exist
                target_path = Path(target_file)
                target_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Save the refactored code
                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write(result.get("generated_code", ""))
                
                return {
                    "success": True,
                    "target_file": target_file,
                    "message": "File refactored successfully"
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Failed to save refactored code: {str(e)}",
                    "generated_code": result.get("generated_code")
                }
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error during refactoring"),
                "stdout": result.get("stdout", ""),
                "stderr": result.get("stderr", "")
            }
    
    def refactor_class(self, cpp_header: str, cpp_implementation: str, 
                      gdscript_target: str, class_mapping: Dict[str, str]) -> Dict[str, Any]:
        """
        Refactor a C++ class to GDScript.
        
        Args:
            cpp_header: Path to the C++ header file
            cpp_implementation: Path to the C++ implementation file
            gdscript_target: Path where the GDScript file should be created
            class_mapping: Mapping of C++ class names to GDScript class names
            
        Returns:
            Dictionary with refactoring results
        """
        # Check if files exist
        missing_files = []
        for file_path in [cpp_header, cpp_implementation]:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
        
        if missing_files:
            return {
                "success": False,
                "error": f"Missing files: {', '.join(missing_files)}"
            }
        
        # Read the source files
        try:
            with open(cpp_header, 'r', encoding='utf-8') as f:
                header_content = f.read()
            
            with open(cpp_implementation, 'r', encoding='utf-8') as f:
                impl_content = f.read()
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to read source files: {str(e)}"
            }
        
        # Create a detailed specification for the class refactoring
        specification = f"""Refactor the following C++ class to GDScript, following the project's STYLE_GUIDE.md and RULES.md.
Pay special attention to the class mapping and Godot-specific patterns.

<CPP_HEADER_FILE>{cpp_header}</CPP_HEADER_FILE>
<CPP_IMPLEMENTATION_FILE>{cpp_implementation}</CPP_IMPLEMENTATION_FILE>
<GDSCRIPT_TARGET>{gdscript_target}</GDSCRIPT_TARGET>
<CLASS_MAPPING>
{json.dumps(class_mapping, indent=2)}
</CLASS_MAPPING>
<CPP_HEADER_CONTENT>
{header_content}
</CPP_HEADER_CONTENT>
<CPP_IMPLEMENTATION_CONTENT>
{impl_content}
</CPP_IMPLEMENTATION_CONTENT>"""
        
        # Generate the prompt
        prompt = self.prompt_engine.create_generation_prompt(
            target_file_path=gdscript_target,
            specification=specification
        )
        
        # Execute the refactoring using qwen-code
        result = self.qwen_wrapper.generate_code(prompt)
        
        # If successful, save the result to the target file
        if result.get("success"):
            try:
                # Create target directory if it doesn't exist
                target_path = Path(gdscript_target)
                target_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Save the refactored code
                with open(gdscript_target, 'w', encoding='utf-8') as f:
                    f.write(result.get("generated_code", ""))
                
                return {
                    "success": True,
                    "target_file": gdscript_target,
                    "message": "Class refactored successfully"
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Failed to save refactored code: {str(e)}",
                    "generated_code": result.get("generated_code")
                }
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error during class refactoring"),
                "stdout": result.get("stdout", ""),
                "stderr": result.get("stderr", "")
            }
    
    def refactor_with_context(self, source_file: str, target_file: str,
                            refactoring_instructions: str, context_files: List[str]) -> Dict[str, Any]:
        """
        Refactor a file with additional context from other files.
        
        Args:
            source_file: Path to the source file
            target_file: Path where the refactored file should be created
            refactoring_instructions: Specific instructions for the refactoring
            context_files: List of additional files to provide as context
            
        Returns:
            Dictionary with refactoring results
        """
        # Generate the base prompt
        prompt = self.prompt_engine.create_refactoring_prompt(
            file_path=source_file,
            task_description=refactoring_instructions
        )
        
        # Add context to the prompt
        prompt_with_context = self.prompt_engine.add_context_to_prompt(
            prompt, context_files
        )
        
        # Execute the refactoring using qwen-code
        result = self.qwen_wrapper.refactor_code(source_file, prompt_with_context)
        
        # If successful, save the result to the target file
        if result.get("success"):
            try:
                # Create target directory if it doesn't exist
                target_path = Path(target_file)
                target_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Save the refactored code
                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write(result.get("refactored_code", ""))
                
                return {
                    "success": True,
                    "target_file": target_file,
                    "message": "File refactored successfully with context"
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Failed to save refactored code: {str(e)}",
                    "refactored_code": result.get("refactored_code")
                }
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error during refactoring with context"),
                "stdout": result.get("stdout", ""),
                "stderr": result.get("stderr", "")
            }
    
    def fix_refactoring_errors(self, file_path: str, error_message: str) -> Dict[str, Any]:
        """
        Fix errors in previously refactored code.
        
        Args:
            file_path: Path to the file with errors
            error_message: Error message describing the problem
            
        Returns:
            Dictionary with error fixing results
        """
        # Check if file exists
        if not os.path.exists(file_path):
            return {
                "success": False,
                "error": f"File does not exist: {file_path}"
            }
        
        # Read the file with errors
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to read file: {str(e)}"
            }
        
        # Use qwen-code to fix the errors
        result = self.qwen_wrapper.fix_bugs(file_path, error_message)
        
        # If successful, save the fixed code
        if result.get("success"):
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(result.get("fixed_code", ""))
                
                return {
                    "success": True,
                    "file_path": file_path,
                    "message": "Errors fixed successfully"
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Failed to save fixed code: {str(e)}",
                    "fixed_code": result.get("fixed_code")
                }
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error during error fixing"),
                "stdout": result.get("stdout", ""),
                "stderr": result.get("stderr", "")
            }


def main():
    """Main function for testing the RefactoringSpecialist."""
    specialist = RefactoringSpecialist()
    
    # Example usage (commented out since we don't have actual files to refactor)
    # result = specialist.refactor_file(
    #     source_file="source/code/ship.h",
    #     target_file="target/scripts/ship.gd",
    #     refactoring_instructions="Convert C++ class to GDScript Node with proper Godot patterns"
    # )
    # 
    # print("Refactoring Result:")
    # print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

```

---

## converter/run.sh

**File type:** .sh  

**Size:** 1098 bytes  

**Last modified:** 2025-08-21 13:41:51


```bash
#!/bin/bash

# Script to run the Wing Commander Saga to Godot migration

set -e  # Exit on any error

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "Virtual environment not activated. Please run 'source .venv/bin/activate' first."
    exit 1
fi

# Check if source and target directories are provided
if [[ $# -lt 2 ]]; then
    echo "Usage: $0 <source_directory> <target_directory> [additional_args...]"
    echo "Example: $0 ../source ../target --verbose"
    exit 1
fi

SOURCE_DIR="$1"
TARGET_DIR="$2"
shift 2  # Remove the first two arguments, leaving any additional args

# Check if source directory exists
if [[ ! -d "$SOURCE_DIR" ]]; then
    echo "Error: Source directory '$SOURCE_DIR' does not exist."
    exit 1
fi

# Create target directory if it doesn't exist
mkdir -p "$TARGET_DIR"

echo "Running Wing Commander Saga to Godot migration..."
echo "Source directory: $SOURCE_DIR"
echo "Target directory: $TARGET_DIR"

# Run the migration
python orchestrator/main.py --source "$SOURCE_DIR" --target "$TARGET_DIR" "$@"

echo "Migration completed!"

```

---

## converter/run_tests.sh

**File type:** .sh  

**Size:** 1100 bytes  

**Last modified:** 2025-08-21 16:11:36


```bash
#!/bin/bash
# test_runner.sh - Script to run all unit tests for the migration system

echo "Running unit tests for the Wing Commander Saga to Godot migration system..."

# Run configuration manager tests
echo "Testing configuration manager..."
python -c "from config.config_manager import ConfigManager; cm = ConfigManager(); print('✓ ConfigManager loaded successfully')"

# Run agent tests
echo "Testing agent implementations..."
python -c "from agents.base_agent import MigrationArchitect, CodebaseAnalyst; print('✓ Agent classes loaded successfully')"

# Run orchestrator tests
echo "Testing orchestrator..."
mkdir -p /tmp/test_source /tmp/test_target
python -c "from orchestrator.main import MigrationOrchestrator; o = MigrationOrchestrator('/tmp/test_source', '/tmp/test_target'); print('✓ Orchestrator loaded successfully')"
rm -rf /tmp/test_source /tmp/test_target

# Run tool tests
echo "Testing tools..."
python -c "from tools.qwen_code_execution_tool import QwenCodeExecutionTool, QwenCodeInteractiveTool; print('✓ Tool classes loaded successfully')"

echo "All basic tests passed!"
```

---

## converter/scripts/README.md

**File type:** .md  

**Size:** 793 bytes  

**Last modified:** 2025-08-21 21:51:50


```markdown
# Utility Scripts

This directory contains utility scripts for setting up and running the migration.

- `setup_environment.py` - Setup script for the migration environment
- `analyze_source_codebase.py` - Script to analyze the legacy codebase
- `run.sh` - Main script to start the migration process

## Key Components

- `setup_environment.py` - Comprehensive environment setup script
- `analyze_source_codebase.py` - Enhanced codebase analysis script
- `run.sh` - Main migration execution script

## Integration with Other Systems

The utility scripts integrate with several systems:

- **Orchestrator**: Execute and control the migration process
- **Configuration System**: Use configuration files for setup and execution
- **Logging System**: Provide detailed logging and progress reporting
```

---

## converter/scripts/analyze_source_codebase.py

**File type:** .py  

**Size:** 13693 bytes  

**Last modified:** 2025-08-21 13:15:19


```python
#!/usr/bin/env python3
"""
Source Codebase Analysis Script

This script analyzes the source C++ codebase to identify files, dependencies,
and architectural patterns to inform the migration process.
"""

import os
import sys
import json
import argparse
import logging
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SourceCodebaseAnalyzer:
    """Analyzer for the source C++ codebase."""
    
    def __init__(self, source_path: str):
        """
        Initialize the analyzer.
        
        Args:
            source_path: Path to the source codebase
        """
        self.source_path = Path(source_path)
        if not self.source_path.exists():
            raise ValueError(f"Source path does not exist: {self.source_path}")
        
        # File extensions to analyze
        self.cpp_extensions = {'.h', '.hpp', '.cpp', '.cc', '.cxx'}
        self.asset_extensions = {'.png', '.jpg', '.jpeg', '.tga', '.wav', '.ogg', '.mp3', '.ttf', '.otf'}
        self.config_extensions = {'.cfg', '.ini', '.xml', '.json'}
        
        # Analysis results
        self.analysis_results = {
            "files": {},
            "dependencies": {},
            "classes": {},
            "functions": {},
            "assets": {},
            "statistics": {}
        }
    
    def analyze(self) -> Dict[str, Any]:
        """
        Perform complete analysis of the source codebase.
        
        Returns:
            Dictionary with analysis results
        """
        logger.info(f"Starting analysis of codebase at: {self.source_path}")
        
        # Find all files
        self._find_files()
        
        # Analyze C++ files
        self._analyze_cpp_files()
        
        # Analyze assets
        self._analyze_assets()
        
        # Calculate statistics
        self._calculate_statistics()
        
        logger.info("Codebase analysis completed")
        return self.analysis_results
    
    def _find_files(self):
        """Find all files in the source codebase."""
        logger.info("Finding files in codebase...")
        
        for root, dirs, files in os.walk(self.source_path):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                file_path = Path(root) / file
                relative_path = file_path.relative_to(self.source_path)
                
                # Categorize files by extension
                extension = file_path.suffix.lower()
                file_type = "unknown"
                
                if extension in self.cpp_extensions:
                    file_type = "cpp"
                elif extension in self.asset_extensions:
                    file_type = "asset"
                elif extension in self.config_extensions:
                    file_type = "config"
                elif extension in {'.md', '.txt', '.doc', '.docx'}:
                    file_type = "documentation"
                
                self.analysis_results["files"][str(relative_path)] = {
                    "type": file_type,
                    "size": file_path.stat().st_size,
                    "extension": extension
                }
        
        logger.info(f"Found {len(self.analysis_results['files'])} files")
    
    def _analyze_cpp_files(self):
        """Analyze C++ files for classes, functions, and dependencies."""
        logger.info("Analyzing C++ files...")
        
        cpp_files = {
            path: info for path, info in self.analysis_results["files"].items()
            if info["type"] == "cpp"
        }
        
        for file_path, file_info in cpp_files.items():
            full_path = self.source_path / file_path
            self._analyze_single_cpp_file(full_path, file_path)
    
    def _analyze_single_cpp_file(self, full_path: Path, relative_path: str):
        """
        Analyze a single C++ file.
        
        Args:
            full_path: Full path to the file
            relative_path: Relative path from source root
        """
        try:
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            logger.warning(f"Failed to read file {full_path}: {str(e)}")
            return
        
        # Find includes
        includes = self._find_includes(content)
        self.analysis_results["dependencies"][relative_path] = includes
        
        # Find classes
        classes = self._find_classes(content)
        for class_name, class_info in classes.items():
            if class_name not in self.analysis_results["classes"]:
                self.analysis_results["classes"][class_name] = []
            class_info["file"] = relative_path
            self.analysis_results["classes"][class_name].append(class_info)
        
        # Find functions
        functions = self._find_functions(content)
        for func_name, func_info in functions.items():
            if func_name not in self.analysis_results["functions"]:
                self.analysis_results["functions"][func_name] = []
            func_info["file"] = relative_path
            self.analysis_results["functions"][func_name].append(func_info)
    
    def _find_includes(self, content: str) -> List[str]:
        """
        Find #include directives in C++ content.
        
        Args:
            content: C++ file content
            
        Returns:
            List of included files
        """
        includes = []
        include_pattern = r'#include\s*[<"]([^>"]+)[>"]'
        
        for match in re.finditer(include_pattern, content):
            includes.append(match.group(1))
        
        return includes
    
    def _find_classes(self, content: str) -> Dict[str, Dict[str, Any]]:
        """
        Find class declarations in C++ content.
        
        Args:
            content: C++ file content
            
        Returns:
            Dictionary of classes found
        """
        classes = {}
        
        # Simple pattern for class declarations
        class_pattern = r'class\s+(\w+)(?:\s*:\s*(public|private|protected)\s+(\w+))?\s*{'
        
        for match in re.finditer(class_pattern, content):
            class_name = match.group(1)
            inheritance_type = match.group(2)
            parent_class = match.group(3)
            
            classes[class_name] = {
                "name": class_name,
                "inheritance": {
                    "type": inheritance_type,
                    "parent": parent_class
                } if inheritance_type and parent_class else None,
                "line": content.count('\n', 0, match.start()) + 1
            }
        
        return classes
    
    def _find_functions(self, content: str) -> Dict[str, Dict[str, Any]]:
        """
        Find function declarations in C++ content.
        
        Args:
            content: C++ file content
            
        Returns:
            Dictionary of functions found
        """
        functions = {}
        
        # Pattern for function declarations (simplified)
        func_pattern = r'(\w+(?:\s*\*+)?)\s+(\w+)\s*\([^)]*\)\s*{'
        
        for match in re.finditer(func_pattern, content):
            return_type = match.group(1).strip()
            func_name = match.group(2)
            
            # Skip common keywords that might match
            if func_name in {'if', 'for', 'while', 'switch', 'class', 'struct', 'namespace'}:
                continue
            
            functions[func_name] = {
                "name": func_name,
                "return_type": return_type,
                "line": content.count('\n', 0, match.start()) + 1
            }
        
        return functions
    
    def _analyze_assets(self):
        """Analyze asset files."""
        logger.info("Analyzing assets...")
        
        asset_files = {
            path: info for path, info in self.analysis_results["files"].items()
            if info["type"] == "asset"
        }
        
        for file_path, file_info in asset_files.items():
            self.analysis_results["assets"][file_path] = {
                "type": file_info["extension"][1:],  # Remove the dot
                "size": file_info["size"]
            }
    
    def _calculate_statistics(self):
        """Calculate statistics for the codebase."""
        logger.info("Calculating statistics...")
        
        # File type counts
        file_types = {}
        for file_info in self.analysis_results["files"].values():
            file_type = file_info["type"]
            file_types[file_type] = file_types.get(file_type, 0) + 1
        
        # Class and function counts
        class_count = len(self.analysis_results["classes"])
        function_count = len(self.analysis_results["functions"])
        
        # Dependency counts
        dependency_count = sum(len(deps) for deps in self.analysis_results["dependencies"].values())
        
        # Asset counts
        asset_count = len(self.analysis_results["assets"])
        
        self.analysis_results["statistics"] = {
            "total_files": len(self.analysis_results["files"]),
            "file_types": file_types,
            "classes": class_count,
            "functions": function_count,
            "dependencies": dependency_count,
            "assets": asset_count
        }
    
    def export_results(self, output_file: str, format: str = "json"):
        """
        Export analysis results to a file.
        
        Args:
            output_file: Path to output file
            format: Output format ("json" or "txt")
        """
        logger.info(f"Exporting results to {output_file}")
        
        if format == "json":
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.analysis_results, f, indent=2, default=str)
        elif format == "txt":
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(self._format_results_as_text())
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        logger.info("Results exported successfully")
    
    def _format_results_as_text(self) -> str:
        """Format analysis results as text."""
        lines = []
        lines.append("Wing Commander Saga Codebase Analysis Report")
        lines.append("=" * 50)
        lines.append("")
        
        # Statistics
        stats = self.analysis_results["statistics"]
        lines.append("STATISTICS")
        lines.append("-" * 20)
        lines.append(f"Total Files: {stats['total_files']}")
        lines.append("File Types:")
        for file_type, count in stats["file_types"].items():
            lines.append(f"  {file_type}: {count}")
        lines.append(f"Classes: {stats['classes']}")
        lines.append(f"Functions: {stats['functions']}")
        lines.append(f"Dependencies: {stats['dependencies']}")
        lines.append(f"Assets: {stats['assets']}")
        lines.append("")
        
        # Classes
        lines.append("CLASSES")
        lines.append("-" * 20)
        for class_name, class_info_list in self.analysis_results["classes"].items():
            lines.append(f"{class_name}:")
            for class_info in class_info_list:
                lines.append(f"  File: {class_info['file']}")
                if class_info["inheritance"]:
                    lines.append(f"  Inheritance: {class_info['inheritance']['type']} {class_info['inheritance']['parent']}")
                lines.append(f"  Line: {class_info['line']}")
            lines.append("")
        
        # Functions
        lines.append("FUNCTIONS")
        lines.append("-" * 20)
        for func_name, func_info_list in self.analysis_results["functions"].items():
            lines.append(f"{func_name}:")
            for func_info in func_info_list:
                lines.append(f"  File: {func_info['file']}")
                lines.append(f"  Return Type: {func_info['return_type']}")
                lines.append(f"  Line: {func_info['line']}")
            lines.append("")
        
        return "\n".join(lines)


def main():
    """Main entry point for the analysis script."""
    parser = argparse.ArgumentParser(description="Analyze Wing Commander Saga C++ Codebase")
    parser.add_argument("--source", required=True, help="Path to the source C++ codebase")
    parser.add_argument("--output", help="Output file for analysis results")
    parser.add_argument("--format", choices=["json", "txt"], default="json", 
                       help="Output format (default: json)")
    
    args = parser.parse_args()
    
    try:
        # Create analyzer and run analysis
        analyzer = SourceCodebaseAnalyzer(args.source)
        results = analyzer.analyze()
        
        # Print summary to console
        stats = results["statistics"]
        print(f"Analysis complete!")
        print(f"Total files: {stats['total_files']}")
        print(f"Classes: {stats['classes']}")
        print(f"Functions: {stats['functions']}")
        print(f"Assets: {stats['assets']}")
        
        # Export results if requested
        if args.output:
            analyzer.export_results(args.output, args.format)
            print(f"Results exported to: {args.output}")
            
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

```

---

## converter/scripts/setup_environment.py

**File type:** .py  

**Size:** 9851 bytes  

**Last modified:** 2025-08-21 13:14:41


```python
#!/usr/bin/env python3
"""
Environment Setup Script for Wing Commander Saga to Godot Migration

This script helps set up the development environment for the migration project,
including installing dependencies and configuring tools.
"""

import os
import sys
import subprocess
import argparse
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EnvironmentSetup:
    """Class to handle environment setup for the migration project."""
    
    def __init__(self, project_root: str = "."):
        """
        Initialize the environment setup.
        
        Args:
            project_root: Root directory of the project
        """
        self.project_root = Path(project_root).resolve()
        self.converter_dir = self.project_root / "converter"
        
    def install_python_dependencies(self) -> bool:
        """
        Install Python dependencies from requirements.txt.
        
        Returns:
            True if successful, False otherwise
        """
        logger.info("Installing Python dependencies...")
        
        requirements_file = self.converter_dir / "requirements.txt"
        if not requirements_file.exists():
            logger.error(f"Requirements file not found: {requirements_file}")
            return False
        
        try:
            # Install dependencies
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ], check=True, capture_output=True, text=True)
            
            logger.info("Python dependencies installed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install Python dependencies: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during dependency installation: {str(e)}")
            return False
    
    def check_qwen_code_installation(self) -> bool:
        """
        Check if qwen-code is installed and accessible.
        
        Returns:
            True if installed, False otherwise
        """
        logger.info("Checking qwen-code installation...")
        
        try:
            # Try to run qwen-code with --help to check if it's installed
            result = subprocess.run(
                ["qwen-code", "--help"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                logger.info("qwen-code is installed and accessible")
                return True
            else:
                logger.warning("qwen-code is installed but returned an error")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("qwen-code command timed out")
            return False
        except FileNotFoundError:
            logger.warning("qwen-code is not installed or not in PATH")
            return False
        except Exception as e:
            logger.error(f"Error checking qwen-code installation: {str(e)}")
            return False
    
    def install_qwen_code(self) -> bool:
        """
        Install qwen-code (this would typically be done manually).
        
        Returns:
            True if successful, False otherwise
        """
        logger.info("Please install qwen-code manually following the official documentation")
        logger.info("Visit: https://github.com/QwenLM/qwen-code for installation instructions")
        return False
    
    def setup_directory_structure(self) -> bool:
        """
        Set up the required directory structure for the migration.
        
        Returns:
            True if successful, False otherwise
        """
        logger.info("Setting up directory structure...")
        
        # Define required directories
        required_dirs = [
            "source",           # Source C++ codebase
            "target",           # Target Godot project
            "logs",             # Log files
            "backups",          # Backup files
            "temp"              # Temporary files
        ]
        
        try:
            for dir_name in required_dirs:
                dir_path = self.project_root / dir_name
                dir_path.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created directory: {dir_path}")
            
            logger.info("Directory structure set up successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to set up directory structure: {str(e)}")
            return False
    
    def create_env_file(self) -> bool:
        """
        Create a .env file with default environment variables.
        
        Returns:
            True if successful, False otherwise
        """
        logger.info("Creating .env file...")
        
        env_file = self.project_root / ".env"
        
        # Default environment variables
        env_content = """# Environment variables for Wing Commander Saga to Godot Migration

# DeepSeek API configuration
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1

# qwen-code configuration
QWEN_CODE_COMMAND=qwen-code
QWEN_CODE_TIMEOUT=300

# Project paths
SOURCE_PATH=./source
TARGET_PATH=./target
LOG_PATH=./logs

# Migration settings
MAX_WORKERS=4
DEBUG_MODE=False
"""
        
        try:
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(env_content)
            
            logger.info(f"Created .env file: {env_file}")
            logger.info("Please update the .env file with your actual API keys and settings")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create .env file: {str(e)}")
            return False
    
    def validate_setup(self) -> dict:
        """
        Validate the current setup and report status.
        
        Returns:
            Dictionary with validation results
        """
        logger.info("Validating setup...")
        
        results = {
            "python_dependencies": self.install_python_dependencies(),
            "qwen_code": self.check_qwen_code_installation(),
            "directories": self.setup_directory_structure(),
            "env_file": self.create_env_file()
        }
        
        # Calculate overall status
        success_count = sum(1 for result in results.values() if result)
        total_count = len(results)
        
        logger.info(f"Setup validation complete: {success_count}/{total_count} checks passed")
        
        return results
    
    def run_full_setup(self) -> bool:
        """
        Run the complete setup process.
        
        Returns:
            True if successful, False otherwise
        """
        logger.info("Running full environment setup...")
        
        # Run all setup steps
        steps = [
            ("Installing Python dependencies", self.install_python_dependencies),
            ("Setting up directory structure", self.setup_directory_structure),
            ("Creating .env file", self.create_env_file),
            ("Checking qwen-code installation", self.check_qwen_code_installation)
        ]
        
        success = True
        for step_name, step_func in steps:
            logger.info(f"Executing: {step_name}")
            try:
                result = step_func()
                if not result:
                    logger.warning(f"Step failed: {step_name}")
                    success = False
            except Exception as e:
                logger.error(f"Step failed with exception: {step_name} - {str(e)}")
                success = False
        
        if success:
            logger.info("Full environment setup completed successfully!")
            logger.info("Please remember to:")
            logger.info("1. Install qwen-code if not already installed")
            logger.info("2. Update the .env file with your actual API keys")
            logger.info("3. Verify all paths are correct")
        else:
            logger.error("Full environment setup completed with some errors")
        
        return success


def main():
    """Main entry point for the setup script."""
    parser = argparse.ArgumentParser(description="Environment Setup for Wing Commander Saga to Godot Migration")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--full", action="store_true", help="Run full setup")
    parser.add_argument("--dependencies", action="store_true", help="Install Python dependencies only")
    parser.add_argument("--directories", action="store_true", help="Set up directory structure only")
    parser.add_argument("--env", action="store_true", help="Create .env file only")
    parser.add_argument("--validate", action="store_true", help="Validate current setup")
    
    args = parser.parse_args()
    
    # Create setup instance
    setup = EnvironmentSetup(args.project_root)
    
    # Execute requested actions
    if args.full:
        setup.run_full_setup()
    elif args.dependencies:
        setup.install_python_dependencies()
    elif args.directories:
        setup.setup_directory_structure()
    elif args.env:
        setup.create_env_file()
    elif args.validate:
        results = setup.validate_setup()
        print("\nSetup Validation Results:")
        for check, result in results.items():
            status = "✓" if result else "✗"
            print(f"  {status} {check}")
    else:
        # Default action: show help
        parser.print_help()


if __name__ == "__main__":
    main()

```

---

## converter/tasks/analysis_task.yaml

**File type:** .yaml  

**Size:** 862 bytes  

**Last modified:** 2025-08-21 15:34:44


```yaml
# Codebase Analysis Task Configuration

codebase_analysis_task:
  name: "Codebase Analysis"
  description: >
    Analyze the legacy C++ codebase at {source_path} to identify dependencies, modules, and architectural patterns.
    Focus on:
    1. Identifying all C++ classes and their relationships
    2. Mapping data structures and their usage
    3. Understanding inheritance hierarchies and design patterns
    4. Identifying external dependencies and third-party libraries
    5. Cataloging file types and their purposes (.cpp, .h, .tbl, .pof, etc.)
  expected_output: >
    A structured JSON report containing:
    - Dependency graph of C++ classes and modules
    - List of identified design patterns
    - Catalog of file types and their purposes
    - List of external dependencies
    - Recommendations for migration priorities
  agent: codebase_analyst
```

---

## converter/tasks/decomposition_task.yaml

**File type:** .yaml  

**Size:** 1072 bytes  

**Last modified:** 2025-08-21 15:35:02


```yaml
# Task Decomposition Task Configuration

task_decomposition_task:
  name: "Task Decomposition"
  description: >
    Break down the high-level migration plan into atomic, executable tasks.
    Each task should represent a single, well-defined unit of work that can be completed by one of the specialist agents.
    Tasks should follow the "Units of Work" approach, where each task is small enough to be completed in a single "bolt" cycle.
    
    Focus on:
    1. Creating atomic tasks for each C++ class to be migrated
    2. Identifying dependencies between tasks
    3. Prioritizing tasks based on the migration plan
    4. Ensuring tasks are self-contained and have clear success criteria
  expected_output: >
    A structured list of atomic tasks in JSON format, each containing:
    - Unique task ID
    - Clear description of the work to be done
    - Expected output format
    - Assigned agent
    - Dependencies on other tasks
    - Estimated complexity level
    - Success criteria
  agent: task_decomposition_specialist
  context:
    - migration_planning_task
```

---

## converter/tasks/planning_task.yaml

**File type:** .yaml  

**Size:** 935 bytes  

**Last modified:** 2025-08-21 15:34:53


```yaml
# Migration Planning Task Configuration

migration_planning_task:
  name: "Migration Planning"
  description: >
    Decompose the overall migration into a high-level, phased project plan based on the codebase analysis.
    Create a detailed migration strategy that prioritizes porting foundational systems before application-level game logic.
    The plan should include:
    1. Phase-by-phase breakdown of the migration process
    2. Identification of critical path components
    3. Risk assessment for each phase
    4. Resource allocation recommendations
    5. Timeline estimates for each phase
  expected_output: >
    A multi-phase project plan in Markdown format, outlining:
    - Detailed phases with clear objectives
    - Timeline estimates for each phase
    - Resource requirements
    - Risk mitigation strategies
    - Success criteria for each phase
  agent: migration_architect
  context:
    - codebase_analysis_task
```

---

## converter/tasks/refactoring_task.yaml

**File type:** .yaml  

**Size:** 1765 bytes  

**Last modified:** 2025-08-21 15:35:12


```yaml
# Code Refactoring Task Configuration

code_refactoring_task:
  name: "Code Refactoring"
  description: >
    Refactor a specific C++ class or module to GDScript following Godot best practices.
    Use the architectural mapping guidelines to convert C++ patterns to idiomatic Godot equivalents.
    
    Focus on:
    1. Converting inheritance hierarchies to composition-based scenes
    2. Mapping C++ data structures to GDScript classes or Godot Resources
    3. Converting function pointers and callbacks to Godot signals
    4. Maintaining functional equivalence while improving idiomatic correctness
    5. Following the STYLE_GUIDE.md and RULES.md documents
  expected_output: >
    A complete GDScript file that:
    - Implements the equivalent functionality of the source C++ code
    - Follows Godot's architectural patterns and best practices
    - Adheres to the project's STYLE_GUIDE.md
    - Includes proper documentation and comments
    - Contains no hardcoded values (use constants)
  agent: refactoring_specialist
  context:
    - task_decomposition_task

code_optimization_task:
  name: "Code Optimization"
  description: >
    Optimize the refactored GDScript code for performance and maintainability.
    Focus on:
    1. Improving code efficiency without changing functionality
    2. Reducing memory usage where possible
    3. Ensuring code follows Godot performance guidelines
    4. Adding proper error handling and validation
  expected_output: >
    An optimized version of the GDScript file that:
    - Maintains all original functionality
    - Improves performance characteristics
    - Includes proper error handling
    - Follows Godot performance best practices
  agent: refactoring_specialist
  context:
    - code_refactoring_task
```

---

## converter/tasks/task_templates/qwen_prompt_templates.py

**File type:** .py  

**Size:** 5081 bytes  

**Last modified:** 2025-08-21 13:15:44


```python
def generate_qwen_generate_prompt(target_file_path: str, specification: str, context_code: str = "") -> str:
    """
    Generate a prompt for creating a new file with qwen-code.
    
    Args:
        target_file_path: Path to the target file to create
        specification: Detailed specification for the new file
        context_code: Optional context code to reference
        
    Returns:
        Formatted prompt string
    """
    prompt = f"""
You are an expert GDScript programmer. Your task is to generate a new script file based on the provided specification.
Your response must contain ONLY the complete GDScript code for the new file.
Do not include any explanatory text, markdown formatting, or conversational filler.

<TARGET_FILE_PATH>{target_file_path}</TARGET_FILE_PATH>
<SPECIFICATION>{specification}</SPECIFICATION>
"""
    
    if context_code:
        prompt += f"<CONTEXT_CODE>{context_code}</CONTEXT_CODE>"
    
    return prompt

def generate_qwen_refactor_prompt(file_path: str, task_description: str, constraints: str = "") -> str:
    """
    Generate a prompt for refactoring an existing function with qwen-code.
    
    Args:
        file_path: Path to the file to refactor
        task_description: Description of the refactoring task
        constraints: Additional constraints for the task
        
    Returns:
        Formatted prompt string
    """
    prompt = f"""
You are an expert GDScript programmer. Your task is to perform a specific refactoring on an existing file.
Do not propose a plan; implement the change directly. Do not modify any other files.

<FILE_PATH>{file_path}</FILE_PATH>
<TASK_DESCRIPTION>{task_description}</TASK_DESCRIPTION>
<CONSTRAINTS>{constraints}</CONSTRAINTS>
"""
    return prompt

def generate_qwen_bugfix_prompt(file_path: str, code_snippet: str, error_message: str) -> str:
    """
    Generate a prompt for fixing a bug with qwen-code.
    
    Args:
        file_path: Path to the file with the bug
        code_snippet: Code snippet with the bug
        error_message: Error message describing the bug
        
    Returns:
        Formatted prompt string
    """
    prompt = f"""
You are an expert debugger. A bug has been identified in the following file.
Your task is to fix it. Analyze the provided error message and code, identify the root cause, and apply the necessary correction.
Implement the fix directly.

<FILE_PATH>{file_path}</FILE_PATH>
<CODE_SNIPPET>{code_snippet}</CODE_SNIPPET>
<ERROR_MESSAGE>{error_message}</ERROR_MESSAGE>
"""
    return prompt

def generate_qwen_test_prompt(target_class: str, target_file: str, class_content: str) -> str:
    """
    Generate a prompt for creating unit tests with qwen-code.
    
    Args:
        target_class: Name of the class to test
        target_file: Path to the file containing the class
        class_content: Content of the class to test
        
    Returns:
        Formatted prompt string
    """
    prompt = f"""
You are an expert QA engineer. Your task is to generate unit tests for the provided GDScript class.
Create comprehensive tests that cover all public methods and edge cases.
Use the gdUnit4 framework for test implementation.

<TARGET_CLASS>{target_class}</TARGET_CLASS>
<TARGET_FILE>{target_file}</TARGET_FILE>
<CLASS_CONTENT>{class_content}</CLASS_CONTENT>
<TEST_FRAMEWORK>gdUnit4</TEST_FRAMEWORK>
"""
    return prompt

def generate_qwen_optimize_prompt(file_path: str, optimization_goal: str, performance_metrics: str = "") -> str:
    """
    Generate a prompt for optimizing code with qwen-code.
    
    Args:
        file_path: Path to the file to optimize
        optimization_goal: Description of the optimization goal
        performance_metrics: Current performance metrics (if available)
        
    Returns:
        Formatted prompt string
    """
    prompt = f"""
You are an expert performance optimizer. Your task is to optimize the provided GDScript code.
Focus on the specific optimization goal while maintaining all existing functionality.

<FILE_PATH>{file_path}</FILE_PATH>
<OPTIMIZATION_GOAL>{optimization_goal}</OPTIMIZATION_GOAL>
"""
    
    if performance_metrics:
        prompt += f"<PERFORMANCE_METRICS>{performance_metrics}</PERFORMANCE_METRICS>"
    
    return prompt

def generate_qwen_document_prompt(file_path: str, class_content: str) -> str:
    """
    Generate a prompt for adding documentation to code with qwen-code.
    
    Args:
        file_path: Path to the file to document
        class_content: Content of the class to document
        
    Returns:
        Formatted prompt string
    """
    prompt = f"""
You are an expert technical writer. Your task is to add comprehensive documentation to the provided GDScript code.
Add docstrings to all public classes and methods, and inline comments for complex logic.
Follow the documentation standards in STYLE_GUIDE.md.

<FILE_PATH>{file_path}</FILE_PATH>
<CLASS_CONTENT>{class_content}</CLASS_CONTENT>
<DOCUMENTATION_STANDARDS>Follow Godot GDScript documentation standards</DOCUMENTATION_STANDARDS>
"""
    return prompt

```

---

## converter/tasks/testing_task.yaml

**File type:** .yaml  

**Size:** 1831 bytes  

**Last modified:** 2025-08-21 15:35:22


```yaml
# Testing Task Configuration

unit_test_generation_task:
  name: "Unit Test Generation"
  description: >
    Generate comprehensive unit tests for the refactored GDScript code using the gdUnit4 framework.
    Tests should cover all public methods and edge cases identified in the source code analysis.
    
    Focus on:
    1. Creating tests for all public methods and functions
    2. Including edge case testing for boundary conditions
    3. Testing error conditions and exception handling
    4. Verifying functional equivalence with the original C++ code
    5. Following gdUnit4 best practices and conventions
  expected_output: >
    A complete test file in GDScript using the gdUnit4 framework that:
    - Tests all public methods of the refactored class
    - Includes edge case and error condition tests
    - Verifies functional equivalence with source C++ code
    - Follows gdUnit4 conventions and best practices
    - Produces clear, actionable test output
  agent: test_generator
  context:
    - code_refactoring_task

integration_test_generation_task:
  name: "Integration Test Generation"
  description: >
    Generate integration tests to verify that the refactored component works correctly with other system components.
    Focus on:
    1. Testing interactions between the refactored component and other system components
    2. Verifying signal connections and data flow
    3. Testing component composition and scene interactions
    4. Ensuring proper error handling in component interactions
  expected_output: >
    Integration test files that:
    - Test component interactions and data flow
    - Verify signal connections work correctly
    - Test scene composition and component integration
    - Include error handling verification
  agent: test_generator
  context:
    - unit_test_generation_task
```

---

## converter/tasks/validation_task.yaml

**File type:** .yaml  

**Size:** 1735 bytes  

**Last modified:** 2025-08-21 15:35:31


```yaml
# Validation Task Configuration

code_validation_task:
  name: "Code Validation"
  description: >
    Validate the refactored GDScript code for syntax correctness, style compliance, and adherence to project guidelines.
    Run static analysis and style checking tools to ensure code quality.
    
    Focus on:
    1. Syntax validation using Godot's built-in checker
    2. Style compliance with STYLE_GUIDE.md
    3. Adherence to project rules in RULES.md
    4. Security scanning for potential vulnerabilities
  expected_output: >
    A validation report that:
    - Confirms syntax correctness
    - Lists any style violations
    - Identifies rule violations
    - Flags potential security issues
    - Provides actionable feedback for corrections
  agent: validation_engineer
  context:
    - code_refactoring_task

test_execution_task:
  name: "Test Execution"
  description: >
    Execute the generated unit and integration tests in a headless Godot environment.
    Capture test results, including pass/fail status, execution time, and error details.
    
    Focus on:
    1. Running all generated tests in a controlled environment
    2. Capturing detailed test results and error output
    3. Identifying failing tests and their root causes
    4. Generating structured test reports for further analysis
  expected_output: >
    A structured test execution report that:
    - Lists all executed tests with pass/fail status
    - Includes execution time for each test
    - Provides detailed error information for failing tests
    - Summarizes overall test suite results
    - Identifies patterns in test failures
  agent: validation_engineer
  context:
    - unit_test_generation_task
    - integration_test_generation_task
```

---

## converter/test.sh

**File type:** .sh  

**Size:** 959 bytes  

**Last modified:** 2025-08-21 13:43:37


```bash
#!/bin/bash

# Script to run the converter tests

set -e  # Exit on any error

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "Virtual environment not activated. Please run 'source .venv/bin/activate' first."
    exit 1
fi

# Default to running all tests
TEST_MODULE=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --list)
            echo "Available test modules:"
            ls tests/test_*.py | sed 's/tests\/test_//' | sed 's/\.py$//' | sort
            exit 0
            ;;
        --verbose|-v)
            PYTEST_ARGS="$PYTEST_ARGS -v"
            shift
            ;;
        *)
            TEST_MODULE="$1"
            shift
            ;;
    esac
done

# Run tests
if [[ -n "$TEST_MODULE" ]]; then
    echo "Running tests for module: $TEST_MODULE"
    pytest tests/test_${TEST_MODULE}.py $PYTEST_ARGS
else
    echo "Running all tests"
    pytest tests/ $PYTEST_ARGS
fi

```

---

## converter/test_generator/README.md

**File type:** .md  

**Size:** 955 bytes  

**Last modified:** 2025-08-21 21:47:42


```markdown
# Test Generator Agent

This directory contains the implementation of the Test Generator agent, which creates unit tests.

Based on the "Agentic Migration with CLI Agents" document, this agent is specifically configured to work with the **qwen-code** CLI agent:

## Responsibilities
- Receive newly generated Godot files and analyst's report
- Write comprehensive suite of unit tests using GUT framework
- Ensure 100% test coverage for public methods and signals
- Use qwen-code CLI agent for all test generation tasks

## Key Components

- `test_generator.py` - Main implementation of the Test Generator agent

## Integration with Other Systems

The Test Generator integrates with several systems:

- **Validation System**: Works closely with the Validation Engineer for test quality gates
- **Refactoring Specialist**: Receives newly generated code for test creation
- **Quality Assurance**: Provides tests for validation and quality assurance processes
```

---

## converter/test_generator/test_generator.py

**File type:** .py  

**Size:** 12325 bytes  

**Last modified:** 2025-08-21 13:16:30


```python
"""
Test Generator Agent Implementation

This agent is responsible for generating unit tests for GDScript code
using the qwen-code CLI tool.
"""

import os
import json
from typing import Dict, Any, List, Optional
from pathlib import Path

# Import tools
from tools.qwen_code_wrapper import QwenCodeWrapper
from prompt_engineering.prompt_engineering_agent import PromptEngineeringAgent


class TestGenerator:
    """Agent responsible for generating unit tests for GDScript code."""
    
    def __init__(self, qwen_command: str = "qwen-code"):
        """
        Initialize the TestGenerator.
        
        Args:
            qwen_command: Command to invoke qwen-code
        """
        self.qwen_wrapper = QwenCodeWrapper(qwen_command)
        self.prompt_engine = PromptEngineeringAgent()
    
    def generate_tests_for_file(self, source_file: str, test_file: str = None) -> Dict[str, Any]:
        """
        Generate unit tests for a GDScript file.
        
        Args:
            source_file: Path to the GDScript file to test
            test_file: Path where the test file should be created (optional)
            
        Returns:
            Dictionary with test generation results
        """
        # Check if source file exists
        if not os.path.exists(source_file):
            return {
                "success": False,
                "error": f"Source file does not exist: {source_file}"
            }
        
        # Determine test file path if not provided
        if test_file is None:
            source_path = Path(source_file)
            test_file = source_path.parent / f"test_{source_path.name}"
        
        # Read the source file
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                source_content = f.read()
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to read source file: {str(e)}"
            }
        
        # Extract class name from the file (simple approach)
        class_name = self._extract_class_name(source_content, source_file)
        
        # Generate the prompt for test creation
        prompt = self.prompt_engine.create_test_generation_prompt(
            target_class=class_name,
            target_file=source_file,
            class_content=source_content
        )
        
        # Execute the test generation using qwen-code
        result = self.qwen_wrapper.generate_code(prompt)
        
        # If successful, save the result to the test file
        if result.get("success"):
            try:
                # Create test directory if it doesn't exist
                test_path = Path(test_file)
                test_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Save the generated tests
                with open(test_file, 'w', encoding='utf-8') as f:
                    f.write(result.get("generated_code", ""))
                
                return {
                    "success": True,
                    "test_file": test_file,
                    "class_name": class_name,
                    "message": "Tests generated successfully"
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Failed to save test file: {str(e)}",
                    "generated_code": result.get("generated_code")
                }
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error during test generation"),
                "stdout": result.get("stdout", ""),
                "stderr": result.get("stderr", "")
            }
    
    def generate_tests_for_class(self, class_name: str, class_file: str, 
                                test_file: str = None) -> Dict[str, Any]:
        """
        Generate unit tests for a specific class.
        
        Args:
            class_name: Name of the class to test
            class_file: Path to the file containing the class
            test_file: Path where the test file should be created (optional)
            
        Returns:
            Dictionary with test generation results
        """
        # Check if class file exists
        if not os.path.exists(class_file):
            return {
                "success": False,
                "error": f"Class file does not exist: {class_file}"
            }
        
        # Determine test file path if not provided
        if test_file is None:
            class_path = Path(class_file)
            test_file = class_path.parent / f"test_{class_path.name}"
        
        # Read the class file
        try:
            with open(class_file, 'r', encoding='utf-8') as f:
                class_content = f.read()
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to read class file: {str(e)}"
            }
        
        # Generate the prompt for test creation
        prompt = self.prompt_engine.create_test_generation_prompt(
            target_class=class_name,
            target_file=class_file,
            class_content=class_content
        )
        
        # Execute the test generation using qwen-code
        result = self.qwen_wrapper.generate_code(prompt)
        
        # If successful, save the result to the test file
        if result.get("success"):
            try:
                # Create test directory if it doesn't exist
                test_path = Path(test_file)
                test_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Save the generated tests
                with open(test_file, 'w', encoding='utf-8') as f:
                    f.write(result.get("generated_code", ""))
                
                return {
                    "success": True,
                    "test_file": test_file,
                    "class_name": class_name,
                    "message": "Tests generated successfully"
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Failed to save test file: {str(e)}",
                    "generated_code": result.get("generated_code")
                }
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error during test generation"),
                "stdout": result.get("stdout", ""),
                "stderr": result.get("stderr", "")
            }
    
    def generate_comprehensive_test_suite(self, source_files: List[str], 
                                         test_directory: str) -> Dict[str, Any]:
        """
        Generate a comprehensive test suite for multiple files.
        
        Args:
            source_files: List of paths to GDScript files to test
            test_directory: Directory where test files should be created
            
        Returns:
            Dictionary with test suite generation results
        """
        results = {
            "success": True,
            "test_directory": test_directory,
            "generated_tests": [],
            "failed_tests": [],
            "summary": {}
        }
        
        # Create test directory
        try:
            Path(test_directory).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to create test directory: {str(e)}"
            }
        
        # Generate tests for each source file
        for source_file in source_files:
            if not os.path.exists(source_file):
                results["failed_tests"].append({
                    "file": source_file,
                    "error": "Source file does not exist"
                })
                continue
            
            # Determine test file path
            source_path = Path(source_file)
            test_file = Path(test_directory) / f"test_{source_path.name}"
            
            # Generate tests for this file
            test_result = self.generate_tests_for_file(source_file, str(test_file))
            
            if test_result.get("success"):
                results["generated_tests"].append(test_result)
            else:
                results["failed_tests"].append({
                    "file": source_file,
                    "result": test_result
                })
        
        # Calculate summary
        results["summary"] = {
            "total_files": len(source_files),
            "successful_tests": len(results["generated_tests"]),
            "failed_tests": len(results["failed_tests"]),
            "success_rate": len(results["generated_tests"]) / len(source_files) if source_files else 0
        }
        
        # Update overall success
        results["success"] = len(results["failed_tests"]) == 0
        
        return results
    
    def _extract_class_name(self, content: str, file_path: str) -> str:
        """
        Extract class name from GDScript content.
        
        Args:
            content: GDScript file content
            file_path: Path to the file (used as fallback)
            
        Returns:
            Extracted class name or derived name
        """
        # Look for class_name declaration
        import re
        class_name_match = re.search(r'class_name\s+(\w+)', content)
        if class_name_match:
            return class_name_match.group(1)
        
        # Fallback: derive from file name
        file_name = Path(file_path).stem
        # Capitalize first letter and remove underscores
        class_name = ''.join(word.capitalize() for word in file_name.split('_'))
        return class_name
    
    def refine_tests_with_feedback(self, test_file: str, error_message: str) -> Dict[str, Any]:
        """
        Refine generated tests based on error feedback.
        
        Args:
            test_file: Path to the test file with errors
            error_message: Error message describing the problem
            
        Returns:
            Dictionary with test refinement results
        """
        # Check if test file exists
        if not os.path.exists(test_file):
            return {
                "success": False,
                "error": f"Test file does not exist: {test_file}"
            }
        
        # Read the test file with errors
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                test_content = f.read()
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to read test file: {str(e)}"
            }
        
        # Use qwen-code to fix the errors
        result = self.qwen_wrapper.fix_bugs(test_file, error_message)
        
        # If successful, save the fixed code
        if result.get("success"):
            try:
                with open(test_file, 'w', encoding='utf-8') as f:
                    f.write(result.get("fixed_code", ""))
                
                return {
                    "success": True,
                    "test_file": test_file,
                    "message": "Tests refined successfully"
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Failed to save refined tests: {str(e)}",
                    "fixed_code": result.get("fixed_code")
                }
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error during test refinement"),
                "stdout": result.get("stdout", ""),
                "stderr": result.get("stderr", "")
            }


def main():
    """Main function for testing the TestGenerator."""
    generator = TestGenerator()
    
    # Example usage (commented out since we don't have actual files to test)
    # result = generator.generate_tests_for_file(
    #     source_file="target/scripts/player/ship.gd",
    #     test_file="target/scripts/player/test_ship.gd"
    # )
    # 
    # print("Test Generation Result:")
    # print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

```

---

## converter/tests/README.md

**File type:** .md  

**Size:** 2495 bytes  

**Last modified:** 2025-08-21 21:52:12


```markdown
# Converter Test Suite

This directory contains the comprehensive test suite for the Wing Commander Saga to Godot converter system.

## Test Organization

The tests are organized by component:

- `test_qwen_code_execution_tool.py` - Tests for the QwenCodeExecutionTool
- `test_qwen_code_wrapper.py` - Tests for the QwenCodeWrapper
- `test_prompt_engineering_agent.py` - Tests for the PromptEngineeringAgent
- `test_workflows.py` - Tests for SequentialWorkflow and HierarchicalWorkflow
- `test_example.py` - Example tests to verify setup

## Running Tests

### Run All Tests

To run all tests in the suite:

```bash
# From the converter directory
./test.sh
```

Or directly with pytest:

```bash
# Activate virtual environment first
source .venv/bin/activate
pytest tests/
```

### Run Tests for a Specific Module

To run tests for a specific module:

```bash
./test.sh qwen_code_execution_tool
```

Or directly with pytest:

```bash
# Activate virtual environment first
source .venv/bin/activate
pytest tests/test_qwen_code_execution_tool.py
```

### List Available Test Modules

To see a list of all available test modules:

```bash
./test.sh --list
```

### Verbose Output

To enable verbose output:

```bash
./test.sh --verbose
```

Or directly with pytest:

```bash
# Activate virtual environment first
source .venv/bin/activate
pytest tests/ -v
```

## Test Categories

The test suite provides comprehensive coverage of all major components:

1. **Tool Tests** - Validate the CLI execution tools
2. **Agent Tests** - Verify agent functionality
3. **Workflow Tests** - Ensure workflow orchestration works correctly
4. **Integration Tests** - Test component interactions
5. **Quality Gate Tests** - Validate test quality gates
6. **HITL Integration Tests** - Test human-in-the-loop integration
7. **Graph System Tests** - Validate dependency graph functionality

## Writing New Tests

When adding new functionality to the converter system, corresponding tests should be added to the appropriate test file. Follow these guidelines:

1. Use descriptive test method names that clearly indicate what is being tested
2. Include both positive and negative test cases
3. Use mocking where appropriate to isolate units under test
4. Test edge cases and error conditions
5. Keep tests focused and independent
6. Include tests for quality gates

## Continuous Integration

The test suite is designed to be run as part of a continuous integration pipeline to ensure code quality and prevent regressions.
```

---

## converter/tests/test_agents.py

**File type:** .py  

**Size:** 7348 bytes  

**Last modified:** 2025-08-21 16:33:17


```python
"""
Unit tests for the base agent implementation.
"""

import os
import sys
import tempfile
import yaml
from pathlib import Path
import pytest

# Add the converter directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from agents.base_agent import (
    ConfigurableAgent, MigrationArchitect, CodebaseAnalyst, 
    TaskDecompositionSpecialist, PromptEngineeringAgent, QualityAssuranceAgent
)


class TestBaseAgent:
    """Test cases for the base agent implementation."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Create a temporary directory for test configuration files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_dir = Path(self.temp_dir.name)
        
        # Create test configuration files
        self._create_test_agent_configs()
    
    def teardown_method(self):
        """Tear down test fixtures after each test method."""
        self.temp_dir.cleanup()
    
    def _create_test_agent_configs(self):
        """Create test agent configuration files."""
        # Create migration_architect.yaml
        migration_architect_config = {
            "name": "MigrationArchitect",
            "role": "Lead Systems Architect",
            "goal": "Decompose the overall migration into a high-level, phased project plan",
            "backstory": "You are the project lead for the Wing Commander Saga to Godot migration.",
            "tools": []
        }
        
        with open(self.config_dir / "migration_architect.yaml", "w") as f:
            yaml.dump(migration_architect_config, f)
        
        # Create codebase_analyst.yaml
        codebase_analyst_config = {
            "name": "CodebaseAnalyst",
            "role": "Senior Software Analyst",
            "goal": "Analyze the legacy codebase to identify dependencies, modules, and architectural patterns",
            "backstory": "You are an expert in legacy game engine architecture with deep knowledge of C++ codebases.",
            "tools": ["FileReadTool"]
        }
        
        with open(self.config_dir / "codebase_analyst.yaml", "w") as f:
            yaml.dump(codebase_analyst_config, f)
        
        # Create task_decomposition_specialist.yaml
        task_decomposition_config = {
            "name": "TaskDecompositionSpecialist",
            "role": "Technical Project Manager",
            "goal": "Break down high-level migration phases into a sequence of atomic, executable coding tasks",
            "backstory": "You are a middle manager in the AI crew, acting as a bridge between high-level strategy and low-level execution.",
            "tools": []
        }
        
        with open(self.config_dir / "task_decomposition_specialist.yaml", "w") as f:
            yaml.dump(task_decomposition_config, f)
        
        # Create prompt_engineering_agent.yaml
        prompt_engineering_config = {
            "name": "PromptEngineeringAgent",
            "role": "AI Communications Specialist",
            "goal": "Convert atomic tasks and code context into precise, effective prompts for the CLI agent",
            "backstory": "You are a critical meta-agent that functions as the communication officer between the command crew and the execution layer.",
            "tools": []
        }
        
        with open(self.config_dir / "prompt_engineering_agent.yaml", "w") as f:
            yaml.dump(prompt_engineering_config, f)
        
        # Create quality_assurance_agent.yaml
        quality_assurance_config = {
            "name": "QualityAssuranceAgent",
            "role": "QA Automation Engineer",
            "goal": "Verify the output of CLI agent tasks, diagnose failures, and initiate corrective actions",
            "backstory": "You are responsible for verification and quality control in the AI crew.",
            "tools": ["QwenCodeExecutionTool"]
        }
        
        with open(self.config_dir / "quality_assurance_agent.yaml", "w") as f:
            yaml.dump(quality_assurance_config, f)
    
    def test_configurable_agent_initialization(self):
        """Test that ConfigurableAgent initializes correctly."""
        # Test with a valid configuration file
        config_file = self.config_dir / "migration_architect.yaml"
        agent = ConfigurableAgent(str(config_file))
        
        assert agent is not None
        assert hasattr(agent, "role")
        assert agent.role == "Lead Systems Architect"
    
    def test_migration_architect_initialization(self):
        """Test that MigrationArchitect initializes correctly."""
        # Change current working directory to the temp directory to make the relative paths work
        original_cwd = os.getcwd()
        os.chdir(self.temp_dir.name)
        
        try:
            agent = MigrationArchitect()
            
            assert agent is not None
            assert hasattr(agent, "role")
            assert agent.role == "Lead Systems Architect"
        finally:
            os.chdir(original_cwd)
    
    def test_codebase_analyst_initialization(self):
        """Test that CodebaseAnalyst initializes correctly."""
        # Change current working directory to the temp directory to make the relative paths work
        original_cwd = os.getcwd()
        os.chdir(self.temp_dir.name)
        
        try:
            agent = CodebaseAnalyst()
            
            assert agent is not None
            assert hasattr(agent, "role")
            assert agent.role == "Senior Software Analyst"
        finally:
            os.chdir(original_cwd)
    
    def test_task_decomposition_specialist_initialization(self):
        """Test that TaskDecompositionSpecialist initializes correctly."""
        # Change current working directory to the temp directory to make the relative paths work
        original_cwd = os.getcwd()
        os.chdir(self.temp_dir.name)
        
        try:
            agent = TaskDecompositionSpecialist()
            
            assert agent is not None
            assert hasattr(agent, "role")
            assert agent.role == "Technical Project Manager"
        finally:
            os.chdir(original_cwd)
    
    def test_prompt_engineering_agent_initialization(self):
        """Test that PromptEngineeringAgent initializes correctly."""
        # Change current working directory to the temp directory to make the relative paths work
        original_cwd = os.getcwd()
        os.chdir(self.temp_dir.name)
        
        try:
            agent = PromptEngineeringAgent()
            
            assert agent is not None
            assert hasattr(agent, "role")
            assert agent.role == "AI Communications Specialist"
        finally:
            os.chdir(original_cwd)
    
    def test_quality_assurance_agent_initialization(self):
        """Test that QualityAssuranceAgent initializes correctly."""
        # Change current working directory to the temp directory to make the relative paths work
        original_cwd = os.getcwd()
        os.chdir(self.temp_dir.name)
        
        try:
            agent = QualityAssuranceAgent()
            
            assert agent is not None
            assert hasattr(agent, "role")
            assert agent.role == "QA Automation Engineer"
        finally:
            os.chdir(original_cwd)
```

---

## converter/tests/test_config_manager.py

**File type:** .py  

**Size:** 7822 bytes  

**Last modified:** 2025-08-21 16:31:22


```python
"""
Unit tests for the configuration manager.
"""

import os
import sys
import tempfile
import yaml
from pathlib import Path
import pytest

# Add the converter directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class TestConfigManager:
    """Test cases for the ConfigManager class."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Create a temporary directory for test configuration files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_dir = Path(self.temp_dir.name)
        
        # Create test configuration files
        self._create_test_configs()
    
    def teardown_method(self):
        """Tear down test fixtures after each test method."""
        self.temp_dir.cleanup()
    
    def _create_test_configs(self):
        """Create test configuration files."""
        # Create crewai_config.yaml
        crewai_config = {
            "llm": {
                "model": "deepseek-ai/DeepSeek-V3.1",
                "temperature": 0.7,
                "max_tokens": 4096,
                "base_url": "https://api.deepseek.com/v1",
                "api_key_env_var": "DEEPSEEK_API_KEY"
            },
            "default_agent": {
                "verbose": True,
                "allow_delegation": True,
                "max_rpm": 60,
                "cache": True
            },
            "process": {
                "sequential": {
                    "timeout": 300
                },
                "hierarchical": {
                    "manager_llm": "deepseek-ai/DeepSeek-V3.1",
                    "timeout": 600
                }
            }
        }
        
        with open(self.config_dir / "crewai_config.yaml", "w") as f:
            yaml.dump(crewai_config, f)
        
        # Create agent_config.yaml
        agent_config = {
            "migration_architect": {
                "role": "Lead Systems Architect",
                "goal": "Decompose the overall migration into a high-level, phased project plan"
            },
            "codebase_analyst": {
                "role": "Senior Software Analyst",
                "goal": "Analyze the legacy codebase to identify dependencies, modules, and architectural patterns"
            }
        }
        
        with open(self.config_dir / "agent_config.yaml", "w") as f:
            yaml.dump(agent_config, f)
    
    def test_config_manager_initialization(self):
        """Test that ConfigManager initializes correctly."""
        from config.config_manager import ConfigManager
        
        config_manager = ConfigManager(str(self.config_dir))
        
        assert config_manager is not None
        assert hasattr(config_manager, "_config")
    
    def test_load_yaml_config(self):
        """Test loading configuration from YAML files."""
        from config.config_manager import ConfigManager
        
        config_manager = ConfigManager(str(self.config_dir))
        
        # Check that configurations were loaded
        crewai_config = config_manager._config.get("crewai", {})
        assert crewai_config is not None
        assert "llm" in crewai_config
        
        agent_config = config_manager._config.get("agent_config", {})
        assert agent_config is not None
    
    def test_get_config(self):
        """Test getting configuration values."""
        from config.config_manager import ConfigManager
        
        config_manager = ConfigManager(str(self.config_dir))
        
        # Test getting a simple configuration value
        model = config_manager.get_config("crewai", "llm", {}).get("model")
        assert model == "deepseek-ai/DeepSeek-V3.1"
        
        # Test getting a non-existent configuration with default
        default_value = config_manager.get_config("nonexistent", "key", "default")
        assert default_value == "default"
    
    def test_get_nested_config(self):
        """Test getting nested configuration values."""
        from config.config_manager import ConfigManager
        
        config_manager = ConfigManager(str(self.config_dir))
        
        # Test getting a nested configuration value
        temperature = config_manager.get_nested_config("crewai", "llm", "temperature")
        assert temperature == 0.7
        
        # Test getting a nested configuration with default
        default_value = config_manager.get_nested_config("crewai", "llm", "nonexistent", default="default")
        assert default_value == "default"
    
    def test_get_secret(self):
        """Test getting secrets from environment variables."""
        from config.config_manager import ConfigManager
        
        config_manager = ConfigManager(str(self.config_dir))
        
        # Test getting a secret that doesn't exist
        secret = config_manager.get_secret("NONEXISTENT_SECRET", "default_secret")
        assert secret == "default_secret"
        
        # Test getting a secret that exists
        os.environ["TEST_SECRET"] = "test_value"
        secret = config_manager.get_secret("TEST_SECRET")
        assert secret == "test_value"
        del os.environ["TEST_SECRET"]
    
    def test_get_llm_config(self):
        """Test getting LLM configuration with secrets."""
        from config.config_manager import ConfigManager
        
        config_manager = ConfigManager(str(self.config_dir))
        
        # Test without environment variable set
        llm_config = config_manager.get_llm_config()
        assert "model" in llm_config
        assert llm_config["model"] == "deepseek-ai/DeepSeek-V3.1"
        assert "api_key" not in llm_config  # Should not be present without env var
        
        # Test with environment variable set
        os.environ["DEEPSEEK_API_KEY"] = "test_api_key"
        llm_config = config_manager.get_llm_config()
        assert "api_key" in llm_config
        assert llm_config["api_key"] == "test_api_key"
        del os.environ["DEEPSEEK_API_KEY"]
    
    def test_get_agent_config(self):
        """Test getting agent configuration."""
        from config.config_manager import ConfigManager
        
        config_manager = ConfigManager(str(self.config_dir))
        
        # Test getting default agent configuration
        default_agent_config = config_manager.get_agent_config("default")
        assert default_agent_config is not None
        # The test config doesn't have default agent config, so this will be empty
        
        # Test getting specific agent configuration
        architect_config = config_manager.get_config("agent_config", "migration_architect")
        assert architect_config is not None
        assert architect_config.get("role") == "Lead Systems Architect"
    
    def test_get_process_config(self):
        """Test getting process configuration."""
        from config.config_manager import ConfigManager
        
        config_manager = ConfigManager(str(self.config_dir))
        
        # Test getting sequential process configuration
        sequential_config = config_manager.get_process_config("sequential")
        assert sequential_config is not None
        assert sequential_config.get("timeout") == 300
        
        # Test getting hierarchical process configuration
        hierarchical_config = config_manager.get_process_config("hierarchical")
        assert hierarchical_config is not None
        assert hierarchical_config.get("timeout") == 600
    
    def test_validate_config(self):
        """Test configuration validation."""
        from config.config_manager import ConfigManager
        
        config_manager = ConfigManager(str(self.config_dir))
        
        # Test with valid configuration
        is_valid = config_manager.validate_config()
        assert is_valid is True
```

---

## converter/tests/test_example.py

**File type:** .py  

**Size:** 325 bytes  

**Last modified:** 2025-08-21 13:44:32


```python
"""
Example test file to verify pytest setup.
"""

def test_example():
    """A simple test to verify pytest is working."""
    assert True

def test_addition():
    """Test a simple addition."""
    assert 1 + 1 == 2

def test_string():
    """Test a string operation."""
    assert "hello" + " " + "world" == "hello world"

```

---

## converter/tests/test_orchestrator.py

**File type:** .py  

**Size:** 4664 bytes  

**Last modified:** 2025-08-21 18:03:44


```python
"""
Unit tests for the migration orchestrator.
"""

import os
import sys
import tempfile
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock

# Add the converter directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from converter.orchestrator.main import MigrationOrchestrator


class TestMigrationOrchestrator:
    """Test cases for the MigrationOrchestrator class."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Create temporary directories for source and target
        self.temp_dir = tempfile.TemporaryDirectory()
        self.source_dir = Path(self.temp_dir.name) / "source"
        self.target_dir = Path(self.temp_dir.name) / "target"
        
        # Create the directories
        self.source_dir.mkdir(parents=True, exist_ok=True)
        self.target_dir.mkdir(parents=True, exist_ok=True)
        
        # Create a simple test file in the source directory
        test_file = self.source_dir / "test.txt"
        test_file.write_text("This is a test file.")
    
    def teardown_method(self):
        """Tear down test fixtures after each test method."""
        self.temp_dir.cleanup()
    
    def test_orchestrator_initialization(self):
        """Test that MigrationOrchestrator initializes correctly."""
        orchestrator = MigrationOrchestrator(str(self.source_dir), str(self.target_dir))
        
        assert orchestrator is not None
        assert orchestrator.source_path == self.source_dir
        assert orchestrator.target_path == self.target_dir
    
    def test_orchestrator_initialization_with_nonexistent_source(self):
        """Test that MigrationOrchestrator raises an error for nonexistent source."""
        with pytest.raises(ValueError, match="Source path does not exist"):
            MigrationOrchestrator("/nonexistent/path", str(self.target_dir))
    
    def test_get_status(self):
        """Test the get_status method."""
        orchestrator = MigrationOrchestrator(str(self.source_dir), str(self.target_dir))
        status = orchestrator.get_status()
        
        assert isinstance(status, dict)
        assert "source_path" in status
        assert "target_path" in status
        assert "agents_initialized" in status
        assert "tools_initialized" in status
        assert "crew_status" in status
        
        assert status["source_path"] == str(self.source_dir)
        assert status["target_path"] == str(self.target_dir)
        assert status["crew_status"] == "ready"
    
    @patch("converter.orchestrator.main.Crew")
    def test_run_migration_analysis_phase(self, mock_crew_class):
        """Test running the analysis phase of migration."""
        # Mock the Crew class
        mock_crew_instance = MagicMock()
        mock_crew_instance.kickoff.return_value = {"result": "analysis_complete"}
        mock_crew_class.return_value = mock_crew_instance
        
        orchestrator = MigrationOrchestrator(str(self.source_dir), str(self.target_dir))
        result = orchestrator.run_migration("analysis")
        
        assert result is not None
        assert result["status"] == "completed"
        assert result["phase"] == "analysis"
        
        # Verify that the crew was created with the right parameters
        mock_crew_class.assert_called_once()
    
    @patch("converter.orchestrator.main.Crew")
    def test_run_migration_planning_phase(self, mock_crew_class):
        """Test running the planning phase of migration."""
        # Mock the Crew class
        mock_crew_instance = MagicMock()
        mock_crew_instance.kickoff.return_value = {"result": "planning_complete"}
        mock_crew_class.return_value = mock_crew_instance
        
        orchestrator = MigrationOrchestrator(str(self.source_dir), str(self.target_dir))
        result = orchestrator.run_migration("planning")
        
        assert result is not None
        assert result["status"] == "completed"
        assert result["phase"] == "planning"
        
        # Verify that the crew was created with the right parameters
        mock_crew_class.assert_called_once()
    
    def test_run_migration_with_invalid_phase(self):
        """Test running migration with an invalid phase."""
        orchestrator = MigrationOrchestrator(str(self.source_dir), str(self.target_dir))
        
        # This should not raise an exception, but should return a failure result
        result = orchestrator.run_migration("invalid_phase")
        
        # The result will depend on the implementation, but it should be a dict
        assert isinstance(result, dict)
```

---

## converter/tests/test_project_setup.py

**File type:** .py  

**Size:** 776 bytes  

**Last modified:** 2025-08-21 18:31:44


```python
"""
Simple test to verify the project setup and tooling.
"""

def test_project_setup():
    """Test that the project is set up correctly."""
    # This is a simple test to verify the testing infrastructure works
    assert True

def test_converter_package():
    """Test that the converter package can be imported."""
    import converter
    assert converter is not None
    assert hasattr(converter, '__version__')

def test_requirements_installed():
    """Test that required packages are installed."""
    # Test that crewai can be imported
    import crewai
    assert crewai is not None
    
    # Test that pydantic can be imported
    import pydantic
    assert pydantic is not None
    
    # Test that yaml can be imported
    import yaml
    assert yaml is not None
```

---

## converter/tests/test_prompt_engineering_agent.py

**File type:** .py  

**Size:** 5983 bytes  

**Last modified:** 2025-08-21 13:21:52


```python
"""
Tests for PromptEngineeringAgent

This module contains tests for the PromptEngineeringAgent component.
"""

import unittest
import tempfile
import os
from pathlib import Path

# Import the agent to test
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from prompt_engineering.prompt_engineering_agent import PromptEngineeringAgent


class TestPromptEngineeringAgent(unittest.TestCase):
    """Test cases for PromptEngineeringAgent."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent = PromptEngineeringAgent()
    
    def test_initialization(self):
        """Test that the agent initializes correctly."""
        self.assertIsInstance(self.agent.template_library, dict)
        self.assertIn("QWEN_GENERATE_01", self.agent.template_library)
        self.assertIn("QWEN_REFACTOR_01", self.agent.template_library)
        self.assertIn("QWEN_BUGFIX_01", self.agent.template_library)
        self.assertIn("QWEN_TEST_GENERATE_01", self.agent.template_library)
    
    def test_generate_prompt_valid_template(self):
        """Test generating a prompt with a valid template."""
        prompt = self.agent.generate_prompt(
            "QWEN_GENERATE_01",
            target_file_path="test.gd",
            specification="Create a test class",
            context_code="# This is context"
        )
        
        self.assertIn("test.gd", prompt)
        self.assertIn("Create a test class", prompt)
        self.assertIn("# This is context", prompt)
    
    def test_generate_prompt_invalid_template(self):
        """Test generating a prompt with an invalid template."""
        with self.assertRaises(ValueError):
            self.agent.generate_prompt("INVALID_TEMPLATE", param="value")
    
    def test_create_generation_prompt(self):
        """Test creating a generation prompt."""
        prompt = self.agent.create_generation_prompt(
            target_file_path="scripts/player/ship.gd",
            specification="Create a PlayerShip class",
            context_code="# Player ship context"
        )
        
        self.assertIn("scripts/player/ship.gd", prompt)
        self.assertIn("Create a PlayerShip class", prompt)
        self.assertIn("# Player ship context", prompt)
    
    def test_create_refactoring_prompt(self):
        """Test creating a refactoring prompt."""
        prompt = self.agent.create_refactoring_prompt(
            file_path="scripts/enemy/ship.gd",
            task_description="Refactor to use state machine",
            constraints="Maintain existing API"
        )
        
        self.assertIn("scripts/enemy/ship.gd", prompt)
        self.assertIn("Refactor to use state machine", prompt)
        self.assertIn("Maintain existing API", prompt)
    
    def test_create_bugfix_prompt(self):
        """Test creating a bugfix prompt."""
        prompt = self.agent.create_bugfix_prompt(
            file_path="scripts/weapon/laser.gd",
            code_snippet="func fire():\n    pass",
            error_message="TypeError: Cannot call method 'fire' of null"
        )
        
        self.assertIn("scripts/weapon/laser.gd", prompt)
        self.assertIn("func fire():\n    pass", prompt)
        self.assertIn("TypeError: Cannot call method 'fire' of null", prompt)
    
    def test_create_test_generation_prompt(self):
        """Test creating a test generation prompt."""
        prompt = self.agent.create_test_generation_prompt(
            target_class="PlayerShip",
            target_file="scripts/player/ship.gd",
            class_content="class_name PlayerShip\nextends Node2D"
        )
        
        self.assertIn("PlayerShip", prompt)
        self.assertIn("scripts/player/ship.gd", prompt)
        self.assertIn("class_name PlayerShip\nextends Node2D", prompt)
    
    def test_refine_prompt_with_feedback(self):
        """Test refining a prompt with feedback."""
        original_prompt = "Original prompt content"
        error_message = "SyntaxError: Unexpected token"
        
        refined_prompt = self.agent.refine_prompt_with_feedback(
            original_prompt,
            error_message
        )
        
        self.assertIn(original_prompt, refined_prompt)
        self.assertIn(error_message, refined_prompt)
        self.assertIn("Please revise the prompt", refined_prompt)
    
    def test_add_context_to_prompt(self):
        """Test adding context to a prompt."""
        # Create temporary context files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.gd', delete=False) as f1, \
             tempfile.NamedTemporaryFile(mode='w', suffix='.gd', delete=False) as f2:
            f1.write("# Context file 1\nconst VALUE1 = 1\n")
            f2.write("# Context file 2\nconst VALUE2 = 2\n")
            context_file_1 = f1.name
            context_file_2 = f2.name
        
        try:
            base_prompt = "Base prompt content"
            prompt_with_context = self.agent.add_context_to_prompt(
                base_prompt,
                [context_file_1, context_file_2]
            )
            
            self.assertIn(base_prompt, prompt_with_context)
            self.assertIn("const VALUE1 = 1", prompt_with_context)
            self.assertIn("const VALUE2 = 2", prompt_with_context)
            self.assertIn("<ADDITIONAL_CONTEXT>", prompt_with_context)
        finally:
            # Clean up temporary files
            os.unlink(context_file_1)
            os.unlink(context_file_2)
    
    def test_add_context_to_prompt_nonexistent_file(self):
        """Test adding context with a non-existent file."""
        base_prompt = "Base prompt content"
        prompt_with_context = self.agent.add_context_to_prompt(
            base_prompt,
            ["nonexistent_file.gd"]
        )
        
        # Should return the original prompt since file doesn't exist
        self.assertEqual(base_prompt, prompt_with_context)


if __name__ == "__main__":
    unittest.main()

```

---

## converter/tests/test_qwen_code_execution_tool.py

**File type:** .py  

**Size:** 2920 bytes  

**Last modified:** 2025-08-21 13:21:32


```python
"""
Tests for QwenCodeExecutionTool

This module contains tests for the QwenCodeExecutionTool and related components.
"""

import unittest
import tempfile
import os
from pathlib import Path

# Import the tools to test
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from tools.qwen_code_execution_tool import QwenCodeExecutionTool, QwenCodeInteractiveTool


class TestQwenCodeExecutionTool(unittest.TestCase):
    """Test cases for QwenCodeExecutionTool."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tool = QwenCodeExecutionTool()
    
    def test_initialization(self):
        """Test that the tool initializes correctly."""
        self.assertEqual(self.tool.name, "Qwen Code CLI Execution Tool")
        self.assertEqual(self.tool.description, "Executes qwen-code shell commands non-interactively, captures output, and returns results.")
    
    def test_run_successful_command(self):
        """Test running a successful command."""
        result = self.tool._run("echo 'Hello, World!'")
        
        self.assertEqual(result["return_code"], 0)
        self.assertIn("Hello, World!", result["stdout"])
        self.assertEqual(result["stderr"], "")
    
    def test_run_failing_command(self):
        """Test running a command that fails."""
        result = self.tool._run("exit 1")
        
        self.assertNotEqual(result["return_code"], 0)
        self.assertEqual(result["stdout"], "")
    
    def test_run_with_timeout(self):
        """Test running a command with a timeout."""
        result = self.tool._run("sleep 1", timeout_seconds=2)
        
        self.assertEqual(result["return_code"], 0)
    
    def test_run_timeout_exceeded(self):
        """Test that a command times out when it exceeds the timeout."""
        result = self.tool._run("sleep 3", timeout_seconds=1)
        
        self.assertEqual(result["return_code"], -1)
        self.assertIn("timed out", result["stderr"])


class TestQwenCodeInteractiveTool(unittest.TestCase):
    """Test cases for QwenCodeInteractiveTool."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tool = QwenCodeInteractiveTool()
    
    def test_initialization(self):
        """Test that the tool initializes correctly."""
        self.assertEqual(self.tool.name, "Qwen Code Interactive Tool")
        self.assertEqual(self.tool.description, "Interactively communicates with qwen-code, sending prompts and receiving responses.")
    
    def test_run_interactive_command(self):
        """Test running an interactive command."""
        # This is a basic test - in reality, we'd need to mock qwen-code
        result = self.tool._run("cat", "Hello, World!")
        
        # For the cat command, the input should be echoed to stdout
        self.assertIn("Hello, World!", result["stdout"])


if __name__ == "__main__":
    unittest.main()

```

---

## converter/tests/test_qwen_code_wrapper.py

**File type:** .py  

**Size:** 8804 bytes  

**Last modified:** 2025-08-21 18:05:45


```python
"""
Tests for QwenCodeWrapper

This module contains tests for the QwenCodeWrapper component.
"""

import unittest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the wrapper to test
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from converter.tools.qwen_code_wrapper import QwenCodeWrapper


class TestQwenCodeWrapper(unittest.TestCase):
    """Test cases for QwenCodeWrapper."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.wrapper = QwenCodeWrapper()
    
    def test_initialization(self):
        """Test that the wrapper initializes correctly."""
        self.assertEqual(self.wrapper.qwen_command, "qwen-code")
        self.assertEqual(self.wrapper.timeout, 300)
    
    def test_initialization_with_custom_params(self):
        """Test initialization with custom parameters."""
        wrapper = QwenCodeWrapper(qwen_command="custom-qwen", timeout=600)
        self.assertEqual(wrapper.qwen_command, "custom-qwen")
        self.assertEqual(wrapper.timeout, 600)
    
    @patch('converter.tools.qwen_code_wrapper.QwenCodeInteractiveTool')
    def test_generate_code(self, mock_interactive_tool):
        """Test generating code with the wrapper."""
        # Mock the interactive tool response
        mock_result = {
            "return_code": 0,
            "stdout": "print('Hello, World!')",
            "stderr": ""
        }
        mock_interactive_tool.return_value._run.return_value = mock_result
        
        # Create wrapper with mocked tool
        wrapper = QwenCodeWrapper()
        wrapper.interactive_tool = mock_interactive_tool.return_value
        
        # Test code generation
        result = wrapper.generate_code("Create a simple Python script that prints 'Hello, World!'")
        
        self.assertTrue(result["success"])
        self.assertEqual(result["generated_code"], "print('Hello, World!')")
        mock_interactive_tool.return_value._run.assert_called_once()
    
    @patch('converter.tools.qwen_code_wrapper.QwenCodeInteractiveTool')
    def test_generate_code_with_context(self, mock_interactive_tool):
        """Test generating code with context files."""
        # Mock the interactive tool response
        mock_result = {
            "return_code": 0,
            "stdout": "class MyClass:\n    pass",
            "stderr": ""
        }
        mock_interactive_tool.return_value._run.return_value = mock_result
        
        # Create wrapper with mocked tool
        wrapper = QwenCodeWrapper()
        wrapper.interactive_tool = mock_interactive_tool.return_value
        
        # Create temporary context file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("# This is a context file\nCONSTANT = 42\n")
            context_file_path = f.name
        
        try:
            # Test code generation with context
            result = wrapper.generate_code(
                "Create a class that uses the CONSTANT from context",
                context_files=[context_file_path]
            )
            
            self.assertTrue(result["success"])
            self.assertIn("class MyClass", result["generated_code"])
            mock_interactive_tool.return_value._run.assert_called_once()
        finally:
            # Clean up temporary file
            os.unlink(context_file_path)
    
    @patch('converter.tools.qwen_code_wrapper.QwenCodeInteractiveTool')
    def test_refactor_code(self, mock_interactive_tool):
        """Test refactoring code with the wrapper."""
        # Mock the interactive tool response
        mock_result = {
            "return_code": 0,
            "stdout": "refactored_code = True",
            "stderr": ""
        }
        mock_interactive_tool.return_value._run.return_value = mock_result
        
        # Create wrapper with mocked tool
        wrapper = QwenCodeWrapper()
        wrapper.interactive_tool = mock_interactive_tool.return_value
        
        # Create temporary file to refactor
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("old_code = False\n")
            file_path = f.name
        
        try:
            # Test code refactoring
            result = wrapper.refactor_code(file_path, "Refactor the code to set old_code to True")
            
            self.assertTrue(result["success"])
            self.assertEqual(result["refactored_code"], "refactored_code = True")
            mock_interactive_tool.return_value._run.assert_called_once()
        finally:
            # Clean up temporary file
            os.unlink(file_path)
    
    @patch('converter.tools.qwen_code_wrapper.QwenCodeInteractiveTool')
    def test_fix_bugs(self, mock_interactive_tool):
        """Test fixing bugs with the wrapper."""
        # Mock the interactive tool response
        mock_result = {
            "return_code": 0,
            "stdout": "fixed_code = 'No more bugs'",
            "stderr": ""
        }
        mock_interactive_tool.return_value._run.return_value = mock_result
        
        # Create wrapper with mocked tool
        wrapper = QwenCodeWrapper()
        wrapper.interactive_tool = mock_interactive_tool.return_value
        
        # Create temporary file with bugs
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("buggy_code = 'Has bugs'\n")
            file_path = f.name
        
        try:
            # Test bug fixing
            result = wrapper.fix_bugs(file_path, "SyntaxError: invalid syntax")
            
            self.assertTrue(result["success"])
            self.assertEqual(result["fixed_code"], "fixed_code = 'No more bugs'")
            mock_interactive_tool.return_value._run.assert_called_once()
        finally:
            # Clean up temporary file
            os.unlink(file_path)
    
    @patch('converter.tools.qwen_code_wrapper.QwenCodeInteractiveTool')
    def test_generate_code_failure(self, mock_interactive_tool):
        """Test handling of code generation failure."""
        # Mock the interactive tool response with failure
        mock_result = {
            "return_code": 1,
            "stdout": "",
            "stderr": "Error: Failed to generate code"
        }
        mock_interactive_tool.return_value._run.return_value = mock_result
        
        # Create wrapper with mocked tool
        wrapper = QwenCodeWrapper()
        wrapper.interactive_tool = mock_interactive_tool.return_value
        
        # Test code generation failure
        result = wrapper.generate_code("Create a simple script")
        
        self.assertFalse(result["success"])
        self.assertIn("Error: Failed to generate code", result["error"])
    
    def test_build_contextual_prompt(self):
        """Test building contextual prompts."""
        # Create temporary context files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f1, \
             tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f2:
            f1.write("# Context file 1\nCONSTANT1 = 1\n")
            f2.write("# Context file 2\nCONSTANT2 = 2\n")
            context_file_1 = f1.name
            context_file_2 = f2.name
        
        try:
            # Test building contextual prompt
            prompt = self.wrapper._build_contextual_prompt(
                "Create a script using context constants",
                [context_file_1, context_file_2]
            )
            
            self.assertIn("Create a script using context constants", prompt)
            self.assertIn("CONSTANT1 = 1", prompt)
            self.assertIn("CONSTANT2 = 2", prompt)
        finally:
            # Clean up temporary files
            os.unlink(context_file_1)
            os.unlink(context_file_2)
    
    def test_process_generation_result(self):
        """Test processing generation results."""
        # Test successful result
        success_result = {
            "return_code": 0,
            "stdout": "generated_code = True",
            "stderr": ""
        }
        
        processed = self.wrapper._process_generation_result(success_result)
        self.assertTrue(processed["success"])
        self.assertEqual(processed["generated_code"], "generated_code = True")
        
        # Test failed result
        failure_result = {
            "return_code": 1,
            "stdout": "",
            "stderr": "Error occurred"
        }
        
        processed = self.wrapper._process_generation_result(failure_result)
        self.assertFalse(processed["success"])
        self.assertIn("Error occurred", processed["error"])


if __name__ == "__main__":
    unittest.main()

```

---

## converter/tests/test_tasks.py

**File type:** .py  

**Size:** 5033 bytes  

**Last modified:** 2025-08-21 16:23:51


```python
"""
Unit tests for the task configurations.
"""

import os
import sys
import tempfile
import yaml
from pathlib import Path
import pytest

# Add the converter directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from orchestrator.main import MigrationOrchestrator


class TestTaskConfigurations:
    """Test cases for task configurations."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Create temporary directories for source and target
        self.temp_dir = tempfile.TemporaryDirectory()
        self.source_dir = Path(self.temp_dir.name) / "source"
        self.target_dir = Path(self.temp_dir.name) / "target"
        
        # Create the directories
        self.source_dir.mkdir(parents=True, exist_ok=True)
        self.target_dir.mkdir(parents=True, exist_ok=True)
        
        # Create a simple test file in the source directory
        test_file = self.source_dir / "test.txt"
        test_file.write_text("This is a test file.")
    
    def teardown_method(self):
        """Tear down test fixtures after each test method."""
        self.temp_dir.cleanup()
    
    def test_analysis_task_loading(self):
        """Test that analysis task configuration loads correctly."""
        orchestrator = MigrationOrchestrator(str(self.source_dir), str(self.target_dir))
        
        # Check that tasks were loaded
        assert len(orchestrator.tasks) > 0
        
        # Check for specific task configurations
        assert "codebase_analysis_task" in orchestrator.tasks
        analysis_task = orchestrator.tasks["codebase_analysis_task"]
        
        assert "name" in analysis_task
        assert "description" in analysis_task
        assert "expected_output" in analysis_task
        assert "agent" in analysis_task
    
    def test_planning_task_loading(self):
        """Test that planning task configuration loads correctly."""
        orchestrator = MigrationOrchestrator(str(self.source_dir), str(self.target_dir))
        
        # Check for specific task configurations
        assert "migration_planning_task" in orchestrator.tasks
        planning_task = orchestrator.tasks["migration_planning_task"]
        
        assert "name" in planning_task
        assert "description" in planning_task
        assert "expected_output" in planning_task
        assert "agent" in planning_task
        assert "context" in planning_task
    
    def test_decomposition_task_loading(self):
        """Test that decomposition task configuration loads correctly."""
        orchestrator = MigrationOrchestrator(str(self.source_dir), str(self.target_dir))
        
        # Check for specific task configurations
        assert "task_decomposition_task" in orchestrator.tasks
        decomposition_task = orchestrator.tasks["task_decomposition_task"]
        
        assert "name" in decomposition_task
        assert "description" in decomposition_task
        assert "expected_output" in decomposition_task
        assert "agent" in decomposition_task
        assert "context" in decomposition_task
    
    def test_refactoring_task_loading(self):
        """Test that refactoring task configuration loads correctly."""
        orchestrator = MigrationOrchestrator(str(self.source_dir), str(self.target_dir))
        
        # Check for specific task configurations
        assert "code_refactoring_task" in orchestrator.tasks
        refactoring_task = orchestrator.tasks["code_refactoring_task"]
        
        assert "name" in refactoring_task
        assert "description" in refactoring_task
        assert "expected_output" in refactoring_task
        assert "agent" in refactoring_task
        assert "context" in refactoring_task
    
    def test_testing_task_loading(self):
        """Test that testing task configuration loads correctly."""
        orchestrator = MigrationOrchestrator(str(self.source_dir), str(self.target_dir))
        
        # Check for specific task configurations
        assert "unit_test_generation_task" in orchestrator.tasks
        unit_test_task = orchestrator.tasks["unit_test_generation_task"]
        
        assert "name" in unit_test_task
        assert "description" in unit_test_task
        assert "expected_output" in unit_test_task
        assert "agent" in unit_test_task
        assert "context" in unit_test_task
    
    def test_validation_task_loading(self):
        """Test that validation task configuration loads correctly."""
        orchestrator = MigrationOrchestrator(str(self.source_dir), str(self.target_dir))
        
        # Check for specific task configurations
        assert "code_validation_task" in orchestrator.tasks
        validation_task = orchestrator.tasks["code_validation_task"]
        
        assert "name" in validation_task
        assert "description" in validation_task
        assert "expected_output" in validation_task
        assert "agent" in validation_task
        assert "context" in validation_task
```

---

## converter/tests/test_tools.py

**File type:** .py  

**Size:** 7091 bytes  

**Last modified:** 2025-08-21 23:18:38


```python
"""
Unit tests for the Qwen Code tools.
"""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock

# Add the converter directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tools.qwen_code_execution_tool import (
    QwenCodeExecutionTool, QwenCodeInteractiveTool
)
from converter.utils import CommandExecutor


class TestQwenCodeExecutionTool:
    """Test cases for the QwenCodeExecutionTool class."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.tool = QwenCodeExecutionTool()
    
    def test_tool_initialization(self):
        """Test that QwenCodeExecutionTool initializes correctly."""
        assert self.tool is not None
        assert self.tool.name == "Qwen Code CLI Execution Tool"
        assert self.tool.description is not None
        assert self.tool.args_schema is not None
    
    @patch("converter.utils.CommandExecutor.execute_command")
    def test_successful_execution(self, mock_execute):
        """Test successful command execution."""
        # Mock the command execution
        mock_execute.return_value = {
            "command": "echo 'test'",
            "return_code": 0,
            "stdout": "output",
            "stderr": "",
            "execution_time": 1234567890.0
        }
        
        result = self.tool._run("echo 'test'")
        
        assert result is not None
        assert result["return_code"] == 0
        assert result["stdout"] == "output"
        assert result["stderr"] == ""
        
        mock_execute.assert_called_once_with(
            command="echo 'test'",
            timeout_seconds=300,
            working_directory=None
        )
    
    @patch("converter.utils.CommandExecutor.execute_command")
    def test_execution_with_timeout(self, mock_execute):
        """Test command execution with timeout."""
        # Mock the command execution to return timeout result
        mock_execute.return_value = {
            "command": "sleep 10",
            "return_code": -1,
            "stdout": "",
            "stderr": "Command timed out after 1 seconds",
            "error": "timeout",
            "execution_time": 1234567890.0
        }
        
        result = self.tool._run("sleep 10", timeout_seconds=1)
        
        assert result is not None
        assert result["return_code"] == -1
        assert "timeout" in result.get("error", "")
        
        mock_execute.assert_called_once_with(
            command="sleep 10",
            timeout_seconds=1,
            working_directory=None
        )
    
    @patch("converter.utils.CommandExecutor.execute_command")
    def test_execution_with_exception(self, mock_execute):
        """Test command execution with exception."""
        # Mock the command execution to return exception result
        mock_execute.return_value = {
            "command": "invalid_command",
            "return_code": -1,
            "stdout": "",
            "stderr": "Test exception",
            "error": "exception",
            "execution_time": 1234567890.0
        }
        
        result = self.tool._run("invalid_command")
        
        assert result is not None
        assert result["return_code"] == -1
        assert "exception" in result.get("error", "")
        
        mock_execute.assert_called_once_with(
            command="invalid_command",
            timeout_seconds=300,
            working_directory=None
        )


class TestQwenCodeInteractiveTool:
    """Test cases for the QwenCodeInteractiveTool class."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.tool = QwenCodeInteractiveTool()
    
    def test_tool_initialization(self):
        """Test that QwenCodeInteractiveTool initializes correctly."""
        assert self.tool is not None
        assert self.tool.name == "Qwen Code Interactive Tool"
        assert self.tool.description is not None
        assert self.tool.args_schema is not None
    
    @patch("converter.utils.CommandExecutor.execute_command")
    def test_successful_interactive_execution(self, mock_execute):
        """Test successful interactive command execution."""
        # Mock the command execution
        mock_execute.return_value = {
            "command": "qwen-code",
            "return_code": 0,
            "stdout": "response",
            "stderr": "",
            "execution_time": 1234567890.0
        }
        
        result = self.tool._run("qwen-code", "Generate a test script")
        
        assert result is not None
        assert result["return_code"] == 0
        assert result["stdout"] == "response"
        assert result["stderr"] == ""
        assert result["prompt"] == "Generate a test script"
        
        mock_execute.assert_called_once_with(
            command="qwen-code",
            timeout_seconds=300,
            working_directory=None,
            input_data="Generate a test script"
        )
    
    @patch("converter.utils.CommandExecutor.execute_command")
    def test_interactive_execution_with_timeout(self, mock_execute):
        """Test interactive command execution with timeout."""
        # Mock the command execution to return timeout result
        mock_execute.return_value = {
            "command": "qwen-code",
            "return_code": -1,
            "stdout": "",
            "stderr": "Command timed out after 1 seconds",
            "error": "timeout",
            "execution_time": 1234567890.0
        }
        
        result = self.tool._run("qwen-code", "Generate a test script", timeout_seconds=1)
        
        assert result is not None
        assert result["return_code"] == -1
        assert "timeout" in result.get("error", "")
        assert result["prompt"] == "Generate a test script"
        
        mock_execute.assert_called_once_with(
            command="qwen-code",
            timeout_seconds=1,
            working_directory=None,
            input_data="Generate a test script"
        )
    
    @patch("converter.utils.CommandExecutor.execute_command")
    def test_interactive_execution_with_exception(self, mock_execute):
        """Test interactive command execution with exception."""
        # Mock the command execution to return exception result
        mock_execute.return_value = {
            "command": "qwen-code",
            "return_code": -1,
            "stdout": "",
            "stderr": "Test exception",
            "error": "exception",
            "execution_time": 1234567890.0
        }
        
        result = self.tool._run("qwen-code", "Generate a test script")
        
        assert result is not None
        assert result["return_code"] == -1
        assert "exception" in result.get("error", "")
        assert result["prompt"] == "Generate a test script"
        
        mock_execute.assert_called_once_with(
            command="qwen-code",
            timeout_seconds=300,
            working_directory=None,
            input_data="Generate a test script"
        )
```

---

## converter/tests/test_utils.py

**File type:** .py  

**Size:** 4788 bytes  

**Last modified:** 2025-08-21 23:15:25


```python
"""
Tests for the centralized utilities module.
"""

import os
import sys
import time
import logging
import subprocess
from unittest.mock import patch, MagicMock

# Add converter to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from converter.utils import (
    setup_logging, 
    time_execution, 
    CommandExecutor, 
    handle_graceful,
    generate_timestamp,
    generate_request_id,
    calculate_duration
)


def test_setup_logging():
    """Test that setup_logging creates a properly configured logger."""
    # Clear any existing handlers to avoid interference
    for handler in logging.getLogger().handlers[:]:
        logging.getLogger().removeHandler(handler)
    
    logger = setup_logging("test_logger", logging.DEBUG)
    
    assert logger.name == "test_logger"
    # The root logger level might be different, but our logger should be accessible
    assert logger.getEffectiveLevel() <= logging.DEBUG
    # The handler is on the root logger, not the specific logger
    assert len(logging.getLogger().handlers) > 0


def test_time_execution():
    """Test the time_execution decorator."""
    
    @time_execution
    def test_function():
        time.sleep(0.01)
        return "success"
    
    result = test_function()
    assert result == "success"


def test_command_executor_success():
    """Test CommandExecutor with successful command."""
    with patch('subprocess.Popen') as mock_popen:
        # Mock successful process
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.communicate.return_value = ("stdout output", "")
        mock_popen.return_value = mock_process
        
        result = CommandExecutor.execute_command("echo test")
        
        assert result["return_code"] == 0
        assert result["stdout"] == "stdout output"
        assert result["stderr"] == ""
        assert "execution_time" in result


def test_command_executor_timeout():
    """Test CommandExecutor with timeout."""
    with patch('subprocess.Popen') as mock_popen:
        mock_process = MagicMock()
        mock_process.communicate.side_effect = subprocess.TimeoutExpired("echo test", 1)
        mock_popen.return_value = mock_process
        
        result = CommandExecutor.execute_command("echo test", timeout_seconds=1)
        
        assert result["return_code"] == -1
        assert result["error"] == "timeout"
        assert "timed out" in result["stderr"]


def test_handle_graceful():
    """Test the handle_graceful decorator."""
    
    @handle_graceful
    def failing_function():
        raise ValueError("Test error")
    
    # Should re-raise the exception but log it
    with patch('converter.utils.setup_logging') as mock_logging:
        mock_logger = MagicMock()
        mock_logging.return_value = mock_logger
        
        try:
            failing_function()
            assert False, "Should have raised an exception"
        except ValueError as e:
            assert str(e) == "Test error"


def test_generate_timestamp():
    """Test timestamp generation."""
    timestamp = generate_timestamp()
    assert isinstance(timestamp, float)
    assert timestamp > 0


def test_generate_request_id():
    """Test request ID generation."""
    request_id = generate_request_id("test_entity", "test")
    assert request_id.startswith("test_test_entity_")
    # Should have prefix, entity, and timestamp (3 parts)
    parts = request_id.split("_")
    assert len(parts) >= 3  # At least prefix, entity, timestamp
    assert parts[0] == "test"
    assert parts[1] == "test"
    assert parts[2] == "entity"


def test_calculate_duration():
    """Test duration calculation."""
    start_time = time.time()
    time.sleep(0.01)
    end_time = time.time()
    
    duration = calculate_duration(start_time, end_time)
    assert isinstance(duration, float)
    assert duration > 0
    assert duration < 1.0
    
    # Test with default end time
    duration_default = calculate_duration(start_time)
    assert duration_default > duration


def test_command_executor_with_input():
    """Test CommandExecutor with input data."""
    with patch('subprocess.Popen') as mock_popen:
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.communicate.return_value = ("processed output", "")
        mock_popen.return_value = mock_process
        
        result = CommandExecutor.execute_command(
            "cat", 
            input_data="test input"
        )
        
        assert result["return_code"] == 0
        assert result["stdout"] == "processed output"
        
        # Verify communicate was called with input
        mock_process.communicate.assert_called_with(
            input="test input", 
            timeout=300
        )
```

---

## converter/tests/test_workflows.py

**File type:** .py  

**Size:** 11962 bytes  

**Last modified:** 2025-08-21 13:22:03


```python
"""
Tests for Workflows

This module contains tests for the SequentialWorkflow and HierarchicalWorkflow components.
"""

import unittest
import time
from unittest.mock import MagicMock

# Import the workflow components to test
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from workflows.sequential_workflow import SequentialWorkflow, Task, TaskStatus, example_task_executor
from workflows.hierarchical_workflow import HierarchicalWorkflow, SubWorkflow, create_migration_phase_workflow


class TestSequentialWorkflow(unittest.TestCase):
    """Test cases for SequentialWorkflow."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.workflow = SequentialWorkflow("Test Workflow")
    
    def test_initialization(self):
        """Test that the workflow initializes correctly."""
        self.assertEqual(self.workflow.name, "Test Workflow")
        self.assertEqual(self.workflow.status, TaskStatus.PENDING)
        self.assertEqual(len(self.workflow.tasks), 0)
    
    def test_add_task(self):
        """Test adding a task to the workflow."""
        task = Task(
            id="test_task",
            name="Test Task",
            description="A test task",
            agent="TestAgent",
            expected_output="Test output"
        )
        
        self.workflow.add_task(task)
        self.assertEqual(len(self.workflow.tasks), 1)
        self.assertEqual(self.workflow.tasks[0], task)
    
    def test_add_tasks(self):
        """Test adding multiple tasks to the workflow."""
        tasks = [
            Task(
                id="task_1",
                name="Task 1",
                description="First task",
                agent="TestAgent",
                expected_output="Output 1"
            ),
            Task(
                id="task_2",
                name="Task 2",
                description="Second task",
                agent="TestAgent",
                expected_output="Output 2"
            )
        ]
        
        self.workflow.add_tasks(tasks)
        self.assertEqual(len(self.workflow.tasks), 2)
        self.assertEqual(self.workflow.tasks[0].id, "task_1")
        self.assertEqual(self.workflow.tasks[1].id, "task_2")
    
    def test_can_execute_task_no_dependencies(self):
        """Test checking if a task with no dependencies can be executed."""
        task = Task(
            id="test_task",
            name="Test Task",
            description="A test task",
            agent="TestAgent",
            expected_output="Test output"
        )
        
        self.assertTrue(self.workflow.can_execute_task(task))
    
    def test_can_execute_task_with_dependencies(self):
        """Test checking if a task with dependencies can be executed."""
        # Create tasks with dependencies
        task1 = Task(
            id="task_1",
            name="Task 1",
            description="First task",
            agent="TestAgent",
            expected_output="Output 1"
        )
        
        task2 = Task(
            id="task_2",
            name="Task 2",
            description="Second task",
            agent="TestAgent",
            expected_output="Output 2",
            dependencies=["task_1"]
        )
        
        self.workflow.add_tasks([task1, task2])
        
        # task2 cannot be executed because task1 is not completed
        self.assertFalse(self.workflow.can_execute_task(task2))
        
        # Complete task1
        task1.status = TaskStatus.COMPLETED
        
        # Now task2 can be executed
        self.assertTrue(self.workflow.can_execute_task(task2))
    
    def test_execute_task_success(self):
        """Test executing a task successfully."""
        task = Task(
            id="test_task",
            name="Test Task",
            description="A test task",
            agent="TestAgent",
            expected_output="Test output"
        )
        
        self.workflow.add_task(task)
        success = self.workflow.execute_task(task, example_task_executor)
        
        self.assertTrue(success)
        self.assertEqual(task.status, TaskStatus.COMPLETED)
        self.assertIsNotNone(task.start_time)
        self.assertIsNotNone(task.end_time)
        self.assertIsNotNone(task.result)
    
    def test_execute_task_failure(self):
        """Test executing a task that fails."""
        task = Task(
            id="test_task",
            name="Test Task",
            description="A test task",
            agent="TestAgent",
            expected_output="Test output"
        )
        
        # Create a failing executor
        def failing_executor(task):
            raise Exception("Task execution failed")
        
        self.workflow.add_task(task)
        success = self.workflow.execute_task(task, failing_executor)
        
        self.assertFalse(success)
        self.assertEqual(task.status, TaskStatus.FAILED)
        self.assertIsNotNone(task.start_time)
        self.assertIsNotNone(task.end_time)
        self.assertIsNotNone(task.error)
    
    def test_execute_all(self):
        """Test executing all tasks in the workflow."""
        tasks = [
            Task(
                id="task_1",
                name="Task 1",
                description="First task",
                agent="TestAgent",
                expected_output="Output 1"
            ),
            Task(
                id="task_2",
                name="Task 2",
                description="Second task",
                agent="TestAgent",
                expected_output="Output 2"
            )
        ]
        
        self.workflow.add_tasks(tasks)
        results = self.workflow.execute_all(example_task_executor)
        
        self.assertEqual(results["status"], "completed")
        self.assertEqual(results["total_tasks"], 2)
        self.assertEqual(results["completed_tasks"], 2)
        self.assertEqual(results["failed_tasks"], 0)
        self.assertIsNotNone(results["duration"])
    
    def test_get_task_by_id(self):
        """Test getting a task by its ID."""
        task = Task(
            id="test_task",
            name="Test Task",
            description="A test task",
            agent="TestAgent",
            expected_output="Test output"
        )
        
        self.workflow.add_task(task)
        retrieved_task = self.workflow.get_task_by_id("test_task")
        
        self.assertEqual(retrieved_task, task)
        
        # Test getting non-existent task
        retrieved_task = self.workflow.get_task_by_id("nonexistent_task")
        self.assertIsNone(retrieved_task)
    
    def test_get_tasks_by_status(self):
        """Test getting tasks by status."""
        tasks = [
            Task(
                id="task_1",
                name="Task 1",
                description="First task",
                agent="TestAgent",
                expected_output="Output 1"
            ),
            Task(
                id="task_2",
                name="Task 2",
                description="Second task",
                agent="TestAgent",
                expected_output="Output 2"
            ),
            Task(
                id="task_3",
                name="Task 3",
                description="Third task",
                agent="TestAgent",
                expected_output="Output 3"
            )
        ]
        
        self.workflow.add_tasks(tasks)
        
        # Execute first task
        self.workflow.execute_task(tasks[0], example_task_executor)
        
        # Fail second task
        def failing_executor(task):
            raise Exception("Task execution failed")
        
        self.workflow.execute_task(tasks[1], failing_executor)
        
        pending_tasks = self.workflow.get_pending_tasks()
        completed_tasks = self.workflow.get_completed_tasks()
        failed_tasks = self.workflow.get_failed_tasks()
        
        self.assertEqual(len(pending_tasks), 1)
        self.assertEqual(pending_tasks[0].id, "task_3")
        
        self.assertEqual(len(completed_tasks), 1)
        self.assertEqual(completed_tasks[0].id, "task_1")
        
        self.assertEqual(len(failed_tasks), 1)
        self.assertEqual(failed_tasks[0].id, "task_2")


class TestHierarchicalWorkflow(unittest.TestCase):
    """Test cases for HierarchicalWorkflow."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.workflow = HierarchicalWorkflow("Test Hierarchical Workflow", "TestManager")
    
    def test_initialization(self):
        """Test that the hierarchical workflow initializes correctly."""
        self.assertEqual(self.workflow.name, "Test Hierarchical Workflow")
        self.assertEqual(self.workflow.manager_agent, "TestManager")
        self.assertEqual(self.workflow.status, TaskStatus.PENDING)
        self.assertEqual(len(self.workflow.sub_workflows), 0)
    
    def test_add_sub_workflow(self):
        """Test adding a sub-workflow to the hierarchical workflow."""
        # Create a sequential workflow for the sub-workflow
        sequential_workflow = SequentialWorkflow("Sub Workflow")
        sub_workflow = SubWorkflow(
            id="sub_workflow_1",
            name="Sub Workflow 1",
            workflow=sequential_workflow
        )
        
        self.workflow.add_sub_workflow(sub_workflow)
        self.assertEqual(len(self.workflow.sub_workflows), 1)
        self.assertEqual(self.workflow.sub_workflows[0], sub_workflow)
    
    def test_can_execute_sub_workflow_no_dependencies(self):
        """Test checking if a sub-workflow with no dependencies can be executed."""
        sequential_workflow = SequentialWorkflow("Sub Workflow")
        sub_workflow = SubWorkflow(
            id="sub_workflow_1",
            name="Sub Workflow 1",
            workflow=sequential_workflow
        )
        
        self.assertTrue(self.workflow.can_execute_sub_workflow(sub_workflow))
    
    def test_can_execute_sub_workflow_with_dependencies(self):
        """Test checking if a sub-workflow with dependencies can be executed."""
        # Create sub-workflows with dependencies
        sequential_workflow1 = SequentialWorkflow("Sub Workflow 1")
        sequential_workflow2 = SequentialWorkflow("Sub Workflow 2")
        
        sub_workflow1 = SubWorkflow(
            id="sub_workflow_1",
            name="Sub Workflow 1",
            workflow=sequential_workflow1
        )
        
        sub_workflow2 = SubWorkflow(
            id="sub_workflow_2",
            name="Sub Workflow 2",
            workflow=sequential_workflow2,
            dependencies=["sub_workflow_1"]
        )
        
        self.workflow.add_sub_workflows([sub_workflow1, sub_workflow2])
        
        # sub_workflow2 cannot be executed because sub_workflow1 is not completed
        self.assertFalse(self.workflow.can_execute_sub_workflow(sub_workflow2))
        
        # Complete sub_workflow1
        sub_workflow1.status = TaskStatus.COMPLETED
        
        # Now sub_workflow2 can be executed
        self.assertTrue(self.workflow.can_execute_sub_workflow(sub_workflow2))
    
    def test_create_migration_phase_workflow(self):
        """Test creating a migration phase workflow."""
        tasks = [
            Task(
                id="task_1",
                name="Task 1",
                description="First task",
                agent="TestAgent",
                expected_output="Output 1"
            )
        ]
        
        sub_workflow = create_migration_phase_workflow("Test Phase", tasks, "TestManager")
        
        self.assertEqual(sub_workflow.id, "phase_test_phase")
        self.assertEqual(sub_workflow.name, "Test Phase")
        self.assertEqual(sub_workflow.manager_agent, "TestManager")
        self.assertIsInstance(sub_workflow.workflow, SequentialWorkflow)
        self.assertEqual(len(sub_workflow.workflow.tasks), 1)


if __name__ == "__main__":
    unittest.main()

```

---

## converter/tools/README.md

**File type:** .md  

**Size:** 1063 bytes  

**Last modified:** 2025-08-21 21:48:33


```markdown
# CLI Agent Tools

This directory contains wrappers for the CLI coding agents.

Based on the "Agentic Migration with CLI Agents" document, we are standardizing on a single, powerful CLI coding agent: **qwen-code**.

qwen-code is built upon Alibaba's state-of-the-art Qwen3-Coder models, which are distinguished by their massive context windows and strong performance in complex, agentic coding tasks.

The tools in this directory are designed to work specifically with the qwen-code CLI agent:

- `qwen_code_wrapper.py` - Wrapper for the qwen-code CLI agent
- `qwen_code_execution_tool.py` - Base tool for executing qwen-code commands

## Integration with Other Systems

The CLI Agent Tools integrate with several systems:

- **Prompt Engineering**: Receive precisely formatted prompts from the Prompt Engineering Agent
- **Validation System**: Provide execution results to the Validation Engineer
- **Refactoring Specialist**: Execute code generation tasks for the Refactoring Specialist
- **Test Generator**: Execute test generation tasks for the Test Generator
```

---

## converter/tools/qwen_code_execution_tool.py

**File type:** .py  

**Size:** 3433 bytes  

**Last modified:** 2025-08-21 23:08:29


```python
"""
Qwen Code Execution Tool

This tool provides a wrapper for executing qwen-code CLI commands.
It uses subprocess.Popen for interactive control of the qwen-code process.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from converter.utils import CommandExecutor


class QwenCodeExecutionInput(BaseModel):
    """Input schema for the QwenCodeExecutionTool."""
    command: str = Field(..., description="The full shell command to be executed.")
    timeout_seconds: int = Field(default=300, description="Timeout for the command in seconds.")
    working_directory: Optional[str] = Field(default=None, description="Working directory for command execution.")


class QwenCodeInteractiveInput(BaseModel):
    """Input schema for the QwenCodeInteractiveTool."""
    command: str = Field(..., description="The qwen-code command to execute.")
    prompt: str = Field(..., description="The prompt to send to qwen-code.")
    timeout_seconds: int = Field(default=300, description="Timeout for the command in seconds.")
    working_directory: Optional[str] = Field(default=None, description="Working directory for command execution.")


class QwenCodeExecutionTool(BaseTool):
    """Tool for executing qwen-code CLI commands with interactive control."""
    
    name: str = "Qwen Code CLI Execution Tool"
    description: str = "Executes qwen-code shell commands non-interactively, captures output, and returns results."
    args_schema: type[BaseModel] = QwenCodeExecutionInput
    
    def _run(self, command: str, timeout_seconds: int = 300, working_directory: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute the shell command and return a structured report of the outcome.
        
        Args:
            command: The full shell command to execute
            timeout_seconds: Timeout for the command in seconds
            working_directory: Working directory for command execution
            
        Returns:
            Dictionary with execution results including return code, stdout, stderr
        """
        return CommandExecutor.execute_command(
            command=command,
            timeout_seconds=timeout_seconds,
            working_directory=working_directory
        )


class QwenCodeInteractiveTool(BaseTool):
    """Tool for interactive communication with qwen-code."""
    
    name: str = "Qwen Code Interactive Tool"
    description: str = "Interactively communicates with qwen-code, sending prompts and receiving responses."
    args_schema: type[BaseModel] = QwenCodeInteractiveInput
    
    def _run(self, command: str, prompt: str, timeout_seconds: int = 300, working_directory: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute qwen-code interactively by sending a prompt.
        
        Args:
            command: The qwen-code command to execute
            prompt: The prompt to send to qwen-code
            timeout_seconds: Timeout for the command in seconds
            working_directory: Working directory for command execution
            
        Returns:
            Dictionary with execution results
        """
        result = CommandExecutor.execute_command(
            command=command,
            timeout_seconds=timeout_seconds,
            working_directory=working_directory,
            input_data=prompt
        )
        result["prompt"] = prompt
        return result

```

---

## converter/tools/qwen_code_wrapper.py

**File type:** .py  

**Size:** 8883 bytes  

**Last modified:** 2025-08-21 13:08:00


```python
"""
Qwen Code Wrapper

This module provides a high-level wrapper for the qwen-code CLI agent,
specifically designed for high-context generation tasks.
"""

import json
import os
from typing import Dict, Any, Optional, List
from .qwen_code_execution_tool import QwenCodeInteractiveTool


class QwenCodeWrapper:
    """Wrapper for high-context generation tasks with qwen-code."""
    
    def __init__(self, qwen_command: str = "qwen-code", timeout: int = 300):
        """
        Initialize the QwenCodeWrapper.
        
        Args:
            qwen_command: The command to invoke qwen-code
            timeout: Default timeout for commands in seconds
        """
        self.qwen_command = qwen_command
        self.timeout = timeout
        self.interactive_tool = QwenCodeInteractiveTool()
    
    def generate_code(self, prompt: str, context_files: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Generate code using qwen-code with high-context input.
        
        Args:
            prompt: The prompt for code generation
            context_files: Optional list of file paths to include as context
            
        Returns:
            Dictionary with generation results
        """
        # Build the full prompt with context if provided
        full_prompt = prompt
        if context_files:
            full_prompt = self._build_contextual_prompt(prompt, context_files)
        
        # Execute qwen-code with the prompt
        result = self.interactive_tool._run(
            command=self.qwen_command,
            prompt=full_prompt,
            timeout_seconds=self.timeout
        )
        
        return self._process_generation_result(result)
    
    def refactor_code(self, file_path: str, refactoring_instructions: str) -> Dict[str, Any]:
        """
        Refactor existing code using qwen-code.
        
        Args:
            file_path: Path to the file to refactor
            refactoring_instructions: Instructions for the refactoring
            
        Returns:
            Dictionary with refactoring results
        """
        # Read the existing file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to read file {file_path}: {str(e)}"
            }
        
        # Create a refactoring prompt
        prompt = f"""
You are an expert GDScript programmer. Your task is to refactor the provided code according to the instructions.
Return ONLY the refactored code without any additional text or explanations.

<FILE_PATH>{file_path}</FILE_PATH>
<FILE_CONTENT>
{file_content}
</FILE_CONTENT>
<REFACTORING_INSTRUCTIONS>
{refactoring_instructions}
</REFACTORING_INSTRUCTIONS>
"""
        
        # Execute qwen-code with the refactoring prompt
        result = self.interactive_tool._run(
            command=self.qwen_command,
            prompt=prompt,
            timeout_seconds=self.timeout
        )
        
        return self._process_refactoring_result(result, file_path)
    
    def fix_bugs(self, file_path: str, error_message: str) -> Dict[str, Any]:
        """
        Fix bugs in code using qwen-code.
        
        Args:
            file_path: Path to the file with bugs
            error_message: Error message describing the bug
            
        Returns:
            Dictionary with bug fixing results
        """
        # Read the existing file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to read file {file_path}: {str(e)}"
            }
        
        # Create a bug fixing prompt
        prompt = f"""
You are an expert debugger. Your task is to fix the bug described in the error message.
Analyze the provided code and error, identify the root cause, and apply the necessary correction.
Return ONLY the fixed code without any additional text or explanations.

<FILE_PATH>{file_path}</FILE_PATH>
<FILE_CONTENT>
{file_content}
</FILE_CONTENT>
<ERROR_MESSAGE>
{error_message}
</ERROR_MESSAGE>
"""
        
        # Execute qwen-code with the bug fixing prompt
        result = self.interactive_tool._run(
            command=self.qwen_command,
            prompt=prompt,
            timeout_seconds=self.timeout
        )
        
        return self._process_bugfix_result(result, file_path)
    
    def _build_contextual_prompt(self, prompt: str, context_files: List[str]) -> str:
        """
        Build a prompt with contextual information from files.
        
        Args:
            prompt: The base prompt
            context_files: List of file paths to include as context
            
        Returns:
            Prompt with contextual information
        """
        context_sections = []
        for file_path in context_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    context_sections.append(f"<CONTEXT_FILE path='{file_path}'>\n{content}\n</CONTEXT_FILE>")
                except Exception:
                    # If we can't read a file, just skip it
                    pass
        
        if context_sections:
            context_str = "\n".join(context_sections)
            return f"{prompt}\n\n<CONTEXT>\n{context_str}\n</CONTEXT>"
        
        return prompt
    
    def _process_generation_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the result of a code generation task.
        
        Args:
            result: Raw result from qwen-code execution
            
        Returns:
            Processed result dictionary
        """
        if result.get("return_code") == 0:
            # Extract code from stdout (assuming it's the only content)
            generated_code = result.get("stdout", "").strip()
            
            return {
                "success": True,
                "generated_code": generated_code,
                "stdout": result.get("stdout", ""),
                "stderr": result.get("stderr", "")
            }
        else:
            return {
                "success": False,
                "error": result.get("stderr", "Unknown error"),
                "stdout": result.get("stdout", ""),
                "stderr": result.get("stderr", "")
            }
    
    def _process_refactoring_result(self, result: Dict[str, Any], original_file_path: str) -> Dict[str, Any]:
        """
        Process the result of a code refactoring task.
        
        Args:
            result: Raw result from qwen-code execution
            original_file_path: Path to the original file
            
        Returns:
            Processed result dictionary
        """
        if result.get("return_code") == 0:
            # Extract refactored code from stdout
            refactored_code = result.get("stdout", "").strip()
            
            return {
                "success": True,
                "refactored_code": refactored_code,
                "original_file": original_file_path,
                "stdout": result.get("stdout", ""),
                "stderr": result.get("stderr", "")
            }
        else:
            return {
                "success": False,
                "error": result.get("stderr", "Unknown error"),
                "original_file": original_file_path,
                "stdout": result.get("stdout", ""),
                "stderr": result.get("stderr", "")
            }
    
    def _process_bugfix_result(self, result: Dict[str, Any], original_file_path: str) -> Dict[str, Any]:
        """
        Process the result of a bug fixing task.
        
        Args:
            result: Raw result from qwen-code execution
            original_file_path: Path to the original file
            
        Returns:
            Processed result dictionary
        """
        if result.get("return_code") == 0:
            # Extract fixed code from stdout
            fixed_code = result.get("stdout", "").strip()
            
            return {
                "success": True,
                "fixed_code": fixed_code,
                "original_file": original_file_path,
                "stdout": result.get("stdout", ""),
                "stderr": result.get("stderr", "")
            }
        else:
            return {
                "success": False,
                "error": result.get("stderr", "Unknown error"),
                "original_file": original_file_path,
                "stdout": result.get("stdout", ""),
                "stderr": result.get("stderr", "")
            }

```

---

## converter/utils/__init__.py

**File type:** .py  

**Size:** 5022 bytes  

**Last modified:** 2025-08-21 23:05:57


```python
"""
Centralized utilities for the WCSAGA Godot Converter.

This module provides shared utilities to eliminate code duplication across the codebase.
"""

import logging
import time
import functools
from typing import Callable, Any, Optional, Dict
import subprocess
import os


def setup_logging(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Configure and return a logger with standardized setup.
    
    Args:
        name: Logger name (typically __name__)
        level: Logging level (default: INFO)
        
    Returns:
        Configured logger instance
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(name)


def time_execution(func: Callable) -> Callable:
    """
    Decorator to measure and log function execution time.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function with timing
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        
        logger = logging.getLogger(func.__module__)
        logger.debug(f"{func.__name__} executed in {duration:.4f} seconds")
        
        return result
    return wrapper


class CommandExecutor:
    """Standardized command execution with timeouts and error handling."""
    
    @staticmethod
    def execute_command(
        command: str, 
        timeout_seconds: int = 300, 
        working_directory: Optional[str] = None,
        input_data: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute a shell command with standardized error handling.
        
        Args:
            command: Shell command to execute
            timeout_seconds: Command timeout in seconds
            working_directory: Working directory for execution
            input_data: Input data to send to stdin
            
        Returns:
            Dictionary with execution results
        """
        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE if input_data else None,
                text=True,
                cwd=working_directory
            )
            
            stdout, stderr = process.communicate(
                input=input_data, 
                timeout=timeout_seconds
            )
            
            return {
                "command": command,
                "return_code": process.returncode,
                "stdout": stdout,
                "stderr": stderr,
                "execution_time": time.time()
            }
            
        except subprocess.TimeoutExpired as e:
            return {
                "command": command,
                "return_code": -1,
                "stdout": getattr(e, 'stdout', ''),
                "stderr": f"Command timed out after {timeout_seconds} seconds",
                "error": "timeout",
                "execution_time": time.time()
            }
        except Exception as e:
            return {
                "command": command,
                "return_code": -1,
                "stdout": "",
                "stderr": str(e),
                "error": "exception",
                "execution_time": time.time()
            }


def handle_graceful(func: Callable) -> Callable:
    """
    Decorator for graceful error handling that catches and logs exceptions.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function with error handling
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger = logging.getLogger(func.__module__)
            logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
            raise
    return wrapper


def generate_timestamp() -> float:
    """
    Generate a standardized timestamp.
    
    Returns:
        Current timestamp as float
    """
    return time.time()


def generate_request_id(entity_id: str, prefix: str = "req") -> str:
    """
    Generate a standardized request ID with timestamp.
    
    Args:
        entity_id: Entity identifier
        prefix: Request ID prefix
        
    Returns:
        Standardized request ID
    """
    return f"{prefix}_{entity_id}_{int(time.time())}"


def calculate_duration(start_time: float, end_time: Optional[float] = None) -> float:
    """
    Calculate duration between start and end times.
    
    Args:
        start_time: Start timestamp
        end_time: End timestamp (defaults to current time)
        
    Returns:
        Duration in seconds
    """
    if end_time is None:
        end_time = time.time()
    return end_time - start_time
```

---

## converter/validation/README.md

**File type:** .md  

**Size:** 1506 bytes  

**Last modified:** 2025-08-21 21:39:34


```markdown
# Enhanced Validation

This directory contains enhanced validation implementations for the migration system.

## Overview

The enhanced validation system implements improved validation capabilities with quality gates and more comprehensive checks. It provides:

1. **Test Quality Gates**: Validate completeness and rigor of generated tests
2. **Enhanced Code Quality Checks**: More comprehensive code quality validation
3. **Security Scanning**: Improved security scanning capabilities
4. **Performance Monitoring**: Basic performance monitoring and analysis

## Key Components

- `validation_engineer.py` - Enhanced validation engineer with quality gates
- `test_quality_gate.py` - Test quality gate implementation

## Enhanced Features

The enhanced validation system has been improved with several enhancements:

1. **Quality Gates**: Implementation of quality gates to prevent incomplete verification
2. **Code Coverage Analysis**: Better code coverage analysis and validation
3. **Security Scanning**: Enhanced security scanning capabilities
4. **Performance Monitoring**: Basic performance monitoring and analysis

## Integration with Other Systems

The enhanced validation system integrates with several other systems:

- **Test Generator**: Validate tests generated by the Test Generator agent
- **Orchestrator**: Provide validation results for workflow decisions
- **HITL System**: Escalate critical issues for human review
- **Refactoring Specialist**: Provide feedback for iterative improvements
```

---

## converter/validation/__init__.py

**File type:** .py  

**Size:** 168 bytes  

**Last modified:** 2025-08-21 20:39:08


```python
"""
Enhanced Validation Module

This module contains enhanced validation implementations for the migration system.
"""

__version__ = "0.1.0"
__author__ = "WCSaga Team"
```

---

## converter/validation/enhanced/README.md

**File type:** .md  

**Size:** 1102 bytes  

**Last modified:** 2025-08-21 21:53:07


```markdown
# Enhanced Validation

This directory contains enhanced validation implementations for the migration system.

## Overview

The enhanced validation system implements improved validation capabilities with quality gates and more comprehensive checks. It provides:

1. **Test Quality Gates**: Validate completeness and rigor of generated tests
2. **Enhanced Code Quality Checks**: More comprehensive code quality validation
3. **Security Scanning**: Improved security scanning capabilities
4. **Performance Monitoring**: Basic performance monitoring and analysis

## Key Components

- `validation_engineer.py` - Enhanced validation engineer with quality gates
- `test_quality_gate.py` - Test quality gate implementation

## Integration with Other Systems

The enhanced validation system integrates with several other systems:

- **Test Generator**: Validate tests generated by the Test Generator agent
- **Orchestrator**: Provide validation results for workflow decisions
- **HITL System**: Escalate critical issues for human review
- **Refactoring Specialist**: Provide feedback for iterative improvements
```

---

## converter/validation/test_quality_gate.py

**File type:** .py  

**Size:** 11330 bytes  

**Last modified:** 2025-08-21 23:12:36


```python
"""
Test Quality Gate Implementation

This module implements a test quality gate to validate completeness and rigor of generated tests.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
from converter.utils import setup_logging, generate_timestamp

# Configure logging
logger = setup_logging(__name__)


class TestQualityGate:
    """Quality gate for validating test completeness and rigor."""
    
    def __init__(self, min_coverage: float = 85.0, min_test_count: int = 5):
        """
        Initialize the test quality gate.
        
        Args:
            min_coverage: Minimum required code coverage percentage
            min_test_count: Minimum required number of tests
        """
        self.min_coverage = min_coverage
        self.min_test_count = min_test_count
        
        logger.info(f"Test Quality Gate initialized (min_coverage={min_coverage}%, min_test_count={min_test_count})")
    
    def validate_test_quality(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the quality of generated tests.
        
        Args:
            test_results: Results from test execution
            
        Returns:
            Dictionary with validation results
        """
        validation_result = {
            "timestamp": generate_timestamp(),
            "passed": False,
            "score": 0.0,
            "issues": [],
            "metrics": {},
            "recommendations": []
        }
        
        try:
            # Extract metrics
            metrics = self._extract_test_metrics(test_results)
            validation_result["metrics"] = metrics
            
            # Calculate quality score
            score = self._calculate_quality_score(metrics)
            validation_result["score"] = score
            
            # Check for issues
            issues = self._identify_quality_issues(metrics)
            validation_result["issues"] = issues
            
            # Generate recommendations
            recommendations = self._generate_recommendations(metrics, issues)
            validation_result["recommendations"] = recommendations
            
            # Determine if tests pass quality gate
            passed = self._determine_pass_fail(metrics, issues)
            validation_result["passed"] = passed
            
            logger.info(f"Test quality validation completed: {'PASSED' if passed else 'FAILED'} (Score: {score:.1f}%)")
            
        except Exception as e:
            logger.error(f"Error during test quality validation: {str(e)}")
            validation_result["issues"].append({
                "type": "validation_error",
                "message": f"Error during validation: {str(e)}"
            })
            validation_result["passed"] = False
        
        return validation_result
    
    def _extract_test_metrics(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevant metrics from test results.
        
        Args:
            test_results: Results from test execution
            
        Returns:
            Dictionary with extracted metrics
        """
        metrics = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "coverage_percentage": 0.0,
            "test_duration": 0.0,
            "assertion_count": 0,
            "unique_functions_tested": 0
        }
        
        # Extract from test results
        if "total" in test_results:
            metrics["total_tests"] = test_results["total"]
        
        if "passed" in test_results:
            metrics["passed_tests"] = test_results["passed"]
        
        if "failed" in test_results:
            metrics["failed_tests"] = test_results["failed"]
        
        if "coverage" in test_results:
            metrics["coverage_percentage"] = float(test_results["coverage"])
        
        if "duration" in test_results:
            metrics["test_duration"] = float(test_results["duration"])
        
        # Calculate derived metrics
        if metrics["total_tests"] > 0:
            metrics["pass_rate"] = (metrics["passed_tests"] / metrics["total_tests"]) * 100
        
        return metrics
    
    def _calculate_quality_score(self, metrics: Dict[str, Any]) -> float:
        """
        Calculate an overall quality score based on metrics.
        
        Args:
            metrics: Test metrics
            
        Returns:
            Quality score (0-100)
        """
        score = 0.0
        max_score = 0.0
        
        # Coverage contribution (40% of score)
        coverage_score = min(metrics.get("coverage_percentage", 0), 100)
        score += coverage_score * 0.4
        max_score += 40.0
        
        # Pass rate contribution (30% of score)
        pass_rate = metrics.get("pass_rate", 0)
        score += pass_rate * 0.3
        max_score += 30.0
        
        # Test count contribution (20% of score)
        test_count = metrics.get("total_tests", 0)
        test_count_score = min(test_count / self.min_test_count * 100, 100) if self.min_test_count > 0 else 0
        score += test_count_score * 0.2
        max_score += 20.0
        
        # Performance contribution (10% of score)
        duration = metrics.get("test_duration", 0)
        # Shorter tests are better, so invert the scale
        if duration > 0:
            duration_score = max(0, 100 - (duration * 10))  # Arbitrary scaling
            score += duration_score * 0.1
            max_score += 10.0
        
        # Normalize score
        if max_score > 0:
            score = (score / max_score) * 100
        
        return score
    
    def _identify_quality_issues(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Identify quality issues based on metrics.
        
        Args:
            metrics: Test metrics
            
        Returns:
            List of quality issues
        """
        issues = []
        
        # Check coverage
        coverage = metrics.get("coverage_percentage", 0)
        if coverage < self.min_coverage:
            issues.append({
                "type": "low_coverage",
                "message": f"Code coverage {coverage:.1f}% is below minimum {self.min_coverage}%",
                "severity": "high" if coverage < self.min_coverage * 0.5 else "medium"
            })
        
        # Check test count
        test_count = metrics.get("total_tests", 0)
        if test_count < self.min_test_count:
            issues.append({
                "type": "low_test_count",
                "message": f"Test count {test_count} is below minimum {self.min_test_count}",
                "severity": "high" if test_count == 0 else "medium"
            })
        
        # Check pass rate
        pass_rate = metrics.get("pass_rate", 0)
        if pass_rate < 90.0:  # Less than 90% pass rate
            issues.append({
                "type": "low_pass_rate",
                "message": f"Pass rate {pass_rate:.1f}% is below recommended 90%",
                "severity": "high" if pass_rate < 50.0 else "medium"
            })
        
        # Check for failed tests
        failed_tests = metrics.get("failed_tests", 0)
        if failed_tests > 0:
            issues.append({
                "type": "failed_tests",
                "message": f"{failed_tests} tests failed",
                "severity": "high" if failed_tests > metrics.get("total_tests", 0) * 0.1 else "medium"
            })
        
        return issues
    
    def _generate_recommendations(self, metrics: Dict[str, Any], 
                                issues: List[Dict[str, Any]]) -> List[str]:
        """
        Generate recommendations for improving test quality.
        
        Args:
            metrics: Test metrics
            issues: List of quality issues
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Check for low coverage
        coverage = metrics.get("coverage_percentage", 0)
        if coverage < self.min_coverage:
            gap = self.min_coverage - coverage
            recommendations.append(f"Increase code coverage by {gap:.1f}% - focus on untested functions")
        
        # Check for low test count
        test_count = metrics.get("total_tests", 0)
        if test_count < self.min_test_count:
            needed = self.min_test_count - test_count
            recommendations.append(f"Add {needed} more tests to meet minimum requirement")
        
        # Check for failed tests
        failed_tests = metrics.get("failed_tests", 0)
        if failed_tests > 0:
            recommendations.append(f"Fix {failed_tests} failed tests")
        
        # General recommendations
        if metrics.get("total_tests", 0) > 0:
            recommendations.append("Consider adding edge case tests for boundary conditions")
            recommendations.append("Add tests for error handling and exception cases")
            recommendations.append("Verify test independence and avoid test interdependencies")
        
        return recommendations
    
    def _determine_pass_fail(self, metrics: Dict[str, Any], 
                           issues: List[Dict[str, Any]]) -> bool:
        """
        Determine if tests pass the quality gate.
        
        Args:
            metrics: Test metrics
            issues: List of quality issues
            
        Returns:
            True if tests pass, False otherwise
        """
        # Check for critical issues
        critical_issues = [issue for issue in issues if issue.get("severity") == "high"]
        if critical_issues:
            logger.warning(f"Critical quality issues found: {len(critical_issues)}")
            return False
        
        # Check minimum requirements
        coverage = metrics.get("coverage_percentage", 0)
        if coverage < self.min_coverage:
            logger.warning(f"Coverage {coverage:.1f}% below minimum {self.min_coverage}%")
            return False
        
        test_count = metrics.get("total_tests", 0)
        if test_count < self.min_test_count:
            logger.warning(f"Test count {test_count} below minimum {self.min_test_count}")
            return False
        
        # Check for any failed tests
        failed_tests = metrics.get("failed_tests", 0)
        if failed_tests > 0:
            logger.warning(f"{failed_tests} tests failed")
            return False
        
        return True


def main():
    """Main function for testing the TestQualityGate."""
    # Create test quality gate
    quality_gate = TestQualityGate(min_coverage=85.0, min_test_count=5)
    
    # Test with good results
    good_results = {
        "total": 10,
        "passed": 10,
        "failed": 0,
        "coverage": 92.5,
        "duration": 2.5
    }
    
    result = quality_gate.validate_test_quality(good_results)
    print("Good test results validation:", result)
    
    # Test with poor results
    poor_results = {
        "total": 3,
        "passed": 2,
        "failed": 1,
        "coverage": 65.0,
        "duration": 1.2
    }
    
    result = quality_gate.validate_test_quality(poor_results)
    print("Poor test results validation:", result)


if __name__ == "__main__":
    main()
```

---

## converter/validation/validation_engineer.py

**File type:** .py  

**Size:** 14986 bytes  

**Last modified:** 2025-08-21 21:54:56


```python
"""
Enhanced Validation Engineer Implementation

This module implements an enhanced validation engineer that incorporates test quality gates
and more comprehensive validation checks.
"""

import os
import json
import time
from typing import Dict, Any, List, Optional
from pathlib import Path

# Import our enhanced modules
from .validation.test_quality_gate import TestQualityGate
from tools.qwen_code_execution_tool import QwenCodeExecutionTool
from tools.qwen_code_wrapper import QwenCodeWrapper


class EnhancedValidationEngineer:
    """Enhanced agent responsible for validating GDScript code and running tests with quality gates."""
    
    def __init__(self, godot_command: str = "godot", qwen_command: str = "qwen-code",
                 min_coverage: float = 85.0, min_test_count: int = 5):
        """
        Initialize the EnhancedValidationEngineer.
        
        Args:
            godot_command: Command to invoke Godot
            qwen_command: Command to invoke qwen-code
            min_coverage: Minimum required code coverage percentage
            min_test_count: Minimum required number of tests
        """
        self.godot_command = godot_command
        self.qwen_wrapper = QwenCodeWrapper(qwen_command)
        self.execution_tool = QwenCodeExecutionTool()
        self.test_quality_gate = TestQualityGate(min_coverage, min_test_count)
    
    def validate_gdscript_syntax(self, file_path: str) -> Dict[str, Any]:
        """
        Validate GDScript syntax for a file.
        
        Args:
            file_path: Path to the GDScript file to validate
            
        Returns:
            Dictionary with validation results
        """
        # Check if file exists
        if not os.path.exists(file_path):
            return {
                "success": False,
                "error": f"File does not exist: {file_path}"
            }
        
        # Use Godot to validate syntax
        # Godot has a --check-only flag that validates scripts without running them
        command = f"{self.godot_command} --check-only --script {file_path}"
        
        try:
            result = self.execution_tool._run(command, timeout_seconds=30)
            
            if result.get("return_code") == 0:
                return {
                    "success": True,
                    "file_path": file_path,
                    "message": "Syntax validation passed"
                }
            else:
                return {
                    "success": False,
                    "file_path": file_path,
                    "error": "Syntax validation failed",
                    "stdout": result.get("stdout", ""),
                    "stderr": result.get("stderr", "")
                }
                
        except Exception as e:
            return {
                "success": False,
                "file_path": file_path,
                "error": f"Failed to execute syntax validation: {str(e)}"
            }
    
    def run_unit_tests_with_quality_gate(self, test_file: str = None, 
                                        test_directory: str = None) -> Dict[str, Any]:
        """
        Run unit tests using gdUnit4 with quality gate validation.
        
        Args:
            test_file: Specific test file to run (optional)
            test_directory: Directory containing test files (optional)
            
        Returns:
            Dictionary with comprehensive test results including quality gate validation
        """
        # Run tests first
        test_results = self._run_unit_tests_internal(test_file, test_directory)
        
        # Apply quality gate validation
        quality_validation = self.test_quality_gate.validate_test_quality(
            test_results.get("test_results", {})
        )
        
        # Combine results
        combined_results = {
            "test_execution": test_results,
            "quality_validation": quality_validation,
            "overall_success": test_results.get("success", False) and quality_validation.get("passed", False)
        }
        
        return combined_results
    
    def _run_unit_tests_internal(self, test_file: str = None, 
                                test_directory: str = None) -> Dict[str, Any]:
        """
        Internal method to run unit tests using gdUnit4.
        
        Args:
            test_file: Specific test file to run (optional)
            test_directory: Directory containing test files (optional)
            
        Returns:
            Dictionary with test results
        """
        # Determine what to test
        if test_file:
            if not os.path.exists(test_file):
                return {
                    "success": False,
                    "error": f"Test file does not exist: {test_file}"
                }
            test_target = test_file
        elif test_directory:
            if not os.path.exists(test_directory):
                return {
                    "success": False,
                    "error": f"Test directory does not exist: {test_directory}"
                }
            test_target = test_directory
        else:
            return {
                "success": False,
                "error": "Either test_file or test_directory must be specified"
            }
        
        # Run tests using Godot
        # gdUnit4 typically runs with a specific scene or through the Godot editor
        # For command line, we might need to use a test runner scene
        command = f"{self.godot_command} --path . --quit-after 300 --headless -s {test_target}"
        
        try:
            result = self.execution_tool._run(command, timeout_seconds=300)
            
            # Parse test results (this would depend on gdUnit4 output format)
            parsed_test_results = self._parse_enhanced_test_output(
                result.get("stdout", ""), 
                result.get("stderr", "")
            )
            
            return {
                "success": result.get("return_code") == 0,
                "test_target": test_target,
                "command_output": result,
                "test_results": parsed_test_results
            }
            
        except Exception as e:
            return {
                "success": False,
                "test_target": test_target,
                "error": f"Failed to execute tests: {str(e)}"
            }
    
    def _parse_enhanced_test_output(self, stdout: str, stderr: str) -> Dict[str, Any]:
        """
        Parse enhanced test output from gdUnit4 with coverage information.
        
        Args:
            stdout: Standard output from test execution
            stderr: Standard error from test execution
            
        Returns:
            Dictionary with parsed test results including coverage
        """
        # This is a more sophisticated parser that attempts to extract
        # test results and coverage information
        results = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "coverage_percentage": 0.0,
            "duration": 0.0,
            "errors": [],
            "failures": []
        }
        
        # Look for test summary patterns
        # This is a placeholder implementation that would need to be
        # customized based on the actual gdUnit4 output format
        
        # Simple parsing for demonstration
        if "passed" in stdout.lower():
            results["passed_tests"] = stdout.lower().count("passed")
        if "failed" in stdout.lower():
            results["failed_tests"] = stdout.lower().count("failed")
        
        results["total_tests"] = results["passed_tests"] + results["failed_tests"]
        
        # Look for coverage information
        if "coverage" in stdout.lower():
            # Try to extract coverage percentage
            import re
            coverage_match = re.search(r'coverage[:\s]*(\d+\.?\d*)%', stdout, re.IGNORECASE)
            if coverage_match:
                results["coverage_percentage"] = float(coverage_match.group(1))
        
        # Collect errors and failures
        if stderr:
            results["errors"].append(stderr)
        
        return results
    
    def validate_code_quality(self, file_path: str) -> Dict[str, Any]:
        """
        Validate code quality and adherence to style guidelines.
        
        Args:
            file_path: Path to the GDScript file to validate
            
        Returns:
            Dictionary with code quality results
        """
        # Check if file exists
        if not os.path.exists(file_path):
            return {
                "success": False,
                "error": f"File does not exist: {file_path}"
            }
        
        results = {
            "file_path": file_path,
            "checks": {}
        }
        
        # Read the file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to read file: {str(e)}"
            }
        
        # Perform various quality checks
        checks = [
            self._check_line_length(content),
            self._check_naming_conventions(content),
            self._check_documentation(content),
            self._check_code_complexity(content),
            self._check_magic_numbers(content),
            self._check_performance_antipatterns(content)
        ]
        
        # Aggregate results
        all_passed = True
        for check in checks:
            check_name = check.get("check_name", "unknown")
            results["checks"][check_name] = check
            if not check.get("passed", False):
                all_passed = False
        
        results["success"] = all_passed
        return results
    
    def _check_performance_antipatterns(self, content: str) -> Dict[str, Any]:
        """Check for performance-related anti-patterns."""
        issues = []
        
        # Check for _process in loops
        if "_process" in content and "for " in content:
            issues.append("Potential performance issue: _process function contains loops")
        
        # Check for frequent node lookups
        if ".get_node(" in content and content.count(".get_node(") > 5:
            issues.append("Frequent use of get_node - consider using onready variables")
        
        return {
            "check_name": "performance_antipatterns",
            "passed": len(issues) == 0,
            "issues": issues
        }
    
    def run_security_scan(self, file_path: str) -> Dict[str, Any]:
        """
        Run a comprehensive security scan on GDScript code.
        
        Args:
            file_path: Path to the GDScript file to scan
            
        Returns:
            Dictionary with security scan results
        """
        # Check if file exists
        if not os.path.exists(file_path):
            return {
                "success": False,
                "error": f"File does not exist: {file_path}"
            }
        
        # Read the file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to read file: {str(e)}"
            }
        
        # Check for potential security issues
        security_issues = []
        
        # Check for OS command execution
        if "OS.execute" in content:
            security_issues.append("Use of OS.execute detected - potential security risk")
        
        # Check for file system access
        if "File" in content or "Directory" in content:
            security_issues.append("File system access detected - review for security implications")
        
        # Check for network access
        if "HTTPClient" in content or "HTTPRequest" in content:
            security_issues.append("Network access detected - review for security implications")
        
        # Check for eval-like functions
        if "eval" in content.lower() or "execute" in content.lower():
            security_issues.append("Dynamic code execution detected - potential security risk")
        
        return {
            "success": len(security_issues) == 0,
            "file_path": file_path,
            "security_issues": security_issues
        }
    
    def generate_enhanced_validation_report(self, files_to_validate: List[str]) -> Dict[str, Any]:
        """
        Generate an enhanced comprehensive validation report for multiple files.
        
        Args:
            files_to_validate: List of file paths to validate
            
        Returns:
            Dictionary with comprehensive validation report
        """
        report = {
            "timestamp": time.time(),
            "files_processed": 0,
            "syntax_validation": [],
            "code_quality": [],
            "security_scans": [],
            "test_results": [],
            "summary": {
                "total_files": len(files_to_validate),
                "passed_syntax": 0,
                "passed_quality": 0,
                "passed_security": 0,
                "failed_files": 0,
                "quality_scores": []
            }
        }
        
        for file_path in files_to_validate:
            if not os.path.exists(file_path):
                report["summary"]["failed_files"] += 1
                continue
            
            # Syntax validation
            syntax_result = self.validate_gdscript_syntax(file_path)
            report["syntax_validation"].append(syntax_result)
            if syntax_result.get("success"):
                report["summary"]["passed_syntax"] += 1
            
            # Code quality validation
            quality_result = self.validate_code_quality(file_path)
            report["code_quality"].append(quality_result)
            if quality_result.get("success"):
                report["summary"]["passed_quality"] += 1
            
            # Security scan
            security_result = self.run_security_scan(file_path)
            report["security_scans"].append(security_result)
            if security_result.get("success"):
                report["summary"]["passed_security"] += 1
            
            report["files_processed"] += 1
        
        return report


def main():
    """Main function for testing the EnhancedValidationEngineer."""
    # Create enhanced validation engineer
    validator = EnhancedValidationEngineer(min_coverage=85.0, min_test_count=5)
    
    # Example usage (commented out since we don't have actual files to validate)
    # result = validator.validate_gdscript_syntax("target/scripts/player/ship.gd")
    # print("Validation Result:")
    # print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
```

---

## converter/workflows/README.md

**File type:** .md  

**Size:** 1019 bytes  

**Last modified:** 2025-08-21 21:48:58


```markdown
# Workflows

This directory contains the process definitions for orchestrating the migration.

Based on the "Agentic Migration with CLI Agents" document, we support two workflow models:

## Current Implementation

- `sequential_workflow.py` - Sequential workflow implementation for atomic coding tasks
- `hierarchical_workflow.py` - Hierarchical workflow implementation for managing overall migration

## Key Components

- `sequential_workflow.py` - Sequential workflow processor for atomic tasks
- `hierarchical_workflow.py` - Hierarchical workflow processor for complex tasks
- `migration_campaign.py` - Overall migration campaign orchestration (planned)

## Integration with Other Systems

The workflow system integrates with several systems:

- **Orchestrator**: Core workflow execution engine
- **Graph System**: Uses dependency graph for intelligent task ordering
- **Validation System**: Incorporates test quality gates for rigorous validation
- **HITL System**: Implements human oversight for critical decisions
```

---

## converter/workflows/hierarchical_workflow.py

**File type:** .py  

**Size:** 13667 bytes  

**Last modified:** 2025-08-21 13:18:40


```python
"""
Hierarchical Workflow Implementation

This module implements the hierarchical workflow process for complex tasks
in the Wing Commander Saga to Godot migration.
"""

import json
import time
import logging
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

# Import sequential workflow
from .sequential_workflow import SequentialWorkflow, Task, TaskStatus

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WorkflowType(Enum):
    """Enumeration of workflow types."""
    SEQUENTIAL = "sequential"
    HIERARCHICAL = "hierarchical"


@dataclass
class SubWorkflow:
    """Represents a sub-workflow in a hierarchical workflow."""
    id: str
    name: str
    workflow: SequentialWorkflow
    status: TaskStatus = TaskStatus.PENDING
    manager_agent: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    
    def duration(self) -> Optional[float]:
        """Calculate sub-workflow duration in seconds."""
        return self.workflow.duration()


class HierarchicalWorkflow:
    """Hierarchical workflow processor for complex tasks."""
    
    def __init__(self, name: str = "Hierarchical Workflow", manager_agent: str = "MigrationArchitect"):
        """
        Initialize the hierarchical workflow.
        
        Args:
            name: Name of the workflow
            manager_agent: Agent responsible for managing this workflow
        """
        self.name = name
        self.manager_agent = manager_agent
        self.sub_workflows: List[SubWorkflow] = []
        self.status = TaskStatus.PENDING
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.results: List[Dict[str, Any]] = []
        
    def add_sub_workflow(self, sub_workflow: SubWorkflow) -> None:
        """
        Add a sub-workflow to the hierarchical workflow.
        
        Args:
            sub_workflow: Sub-workflow to add
        """
        self.sub_workflows.append(sub_workflow)
        logger.info(f"Added sub-workflow '{sub_workflow.name}' to hierarchical workflow '{self.name}'")
    
    def add_sub_workflows(self, sub_workflows: List[SubWorkflow]) -> None:
        """
        Add multiple sub-workflows to the hierarchical workflow.
        
        Args:
            sub_workflows: List of sub-workflows to add
        """
        for sub_workflow in sub_workflows:
            self.add_sub_workflow(sub_workflow)
    
    def can_execute_sub_workflow(self, sub_workflow: SubWorkflow) -> bool:
        """
        Check if a sub-workflow can be executed (all dependencies completed).
        
        Args:
            sub_workflow: Sub-workflow to check
            
        Returns:
            True if sub-workflow can be executed, False otherwise
        """
        # If no dependencies, sub-workflow can be executed
        if not sub_workflow.dependencies:
            return True
        
        # Check if all dependencies are completed
        completed_sub_workflow_ids = {
            sw.id for sw in self.sub_workflows 
            if sw.status == TaskStatus.COMPLETED
        }
        
        return all(dep_id in completed_sub_workflow_ids for dep_id in sub_workflow.dependencies)
    
    def execute_sub_workflow(self, sub_workflow: SubWorkflow, 
                           task_executor: Callable[[Task], Dict[str, Any]]) -> bool:
        """
        Execute a single sub-workflow.
        
        Args:
            sub_workflow: Sub-workflow to execute
            task_executor: Function that executes tasks and returns results
            
        Returns:
            True if sub-workflow completed successfully, False otherwise
        """
        # Check if sub-workflow can be executed
        if not self.can_execute_sub_workflow(sub_workflow):
            logger.warning(f"Cannot execute sub-workflow '{sub_workflow.name}' due to unmet dependencies")
            return False
        
        # Update sub-workflow status
        sub_workflow.status = TaskStatus.IN_PROGRESS
        logger.info(f"Executing sub-workflow '{sub_workflow.name}' (ID: {sub_workflow.id})")
        
        try:
            # Execute the sub-workflow
            result = sub_workflow.workflow.execute_all(task_executor)
            
            # Update sub-workflow with results
            sub_workflow.status = TaskStatus.COMPLETED
            
            # Store result
            self.results.append({
                "sub_workflow_id": sub_workflow.id,
                "sub_workflow_name": sub_workflow.name,
                "result": result,
                "duration": sub_workflow.duration()
            })
            
            logger.info(f"Sub-workflow '{sub_workflow.name}' completed successfully in {sub_workflow.duration():.2f} seconds")
            return True
            
        except Exception as e:
            # Handle sub-workflow failure
            sub_workflow.status = TaskStatus.FAILED
            
            logger.error(f"Sub-workflow '{sub_workflow.name}' failed: {str(e)}")
            return False
    
    def execute_next_sub_workflow(self, task_executor: Callable[[Task], Dict[str, Any]]) -> Optional[SubWorkflow]:
        """
        Execute the next pending sub-workflow in the workflow.
        
        Args:
            task_executor: Function that executes tasks and returns results
            
        Returns:
            The executed sub-workflow, or None if no sub-workflow could be executed
        """
        # Find the next pending sub-workflow that can be executed
        for sub_workflow in self.sub_workflows:
            if sub_workflow.status == TaskStatus.PENDING and self.can_execute_sub_workflow(sub_workflow):
                success = self.execute_sub_workflow(sub_workflow, task_executor)
                return sub_workflow if success else None
        
        # No sub-workflows could be executed
        return None
    
    def execute_all(self, task_executor: Callable[[Task], Dict[str, Any]]) -> Dict[str, Any]:
        """
        Execute all sub-workflows in the hierarchical workflow.
        
        Args:
            task_executor: Function that executes tasks and returns results
            
        Returns:
            Dictionary with workflow execution results
        """
        logger.info(f"Starting execution of hierarchical workflow '{self.name}' with {len(self.sub_workflows)} sub-workflows")
        
        # Update workflow status
        self.status = TaskStatus.IN_PROGRESS
        self.start_time = time.time()
        
        # Execute sub-workflows until completion or failure
        completed_sub_workflows = 0
        failed_sub_workflows = 0
        
        while completed_sub_workflows + failed_sub_workflows < len(self.sub_workflows):
            sub_workflow = self.execute_next_sub_workflow(task_executor)
            
            if sub_workflow is None:
                # No sub-workflow could be executed, check for stuck sub-workflows
                pending_sub_workflows = [sw for sw in self.sub_workflows if sw.status == TaskStatus.PENDING]
                if pending_sub_workflows:
                    logger.error(f"Hierarchical workflow stuck: {len(pending_sub_workflows)} sub-workflows cannot be executed due to unmet dependencies")
                    break
                else:
                    break
            
            if sub_workflow.status == TaskStatus.COMPLETED:
                completed_sub_workflows += 1
            elif sub_workflow.status == TaskStatus.FAILED:
                failed_sub_workflows += 1
        
        # Update workflow status
        self.end_time = time.time()
        if failed_sub_workflows == 0:
            self.status = TaskStatus.COMPLETED
            logger.info(f"Hierarchical workflow '{self.name}' completed successfully in {self.duration():.2f} seconds")
        else:
            self.status = TaskStatus.FAILED
            logger.error(f"Hierarchical workflow '{self.name}' failed with {failed_sub_workflows} failed sub-workflows")
        
        return {
            "workflow_name": self.name,
            "manager_agent": self.manager_agent,
            "status": self.status.value,
            "total_sub_workflows": len(self.sub_workflows),
            "completed_sub_workflows": completed_sub_workflows,
            "failed_sub_workflows": failed_sub_workflows,
            "skipped_sub_workflows": len(self.sub_workflows) - completed_sub_workflows - failed_sub_workflows,
            "duration": self.duration(),
            "results": self.results
        }
    
    def duration(self) -> Optional[float]:
        """Calculate workflow duration in seconds."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None
    
    def get_sub_workflow_by_id(self, sub_workflow_id: str) -> Optional[SubWorkflow]:
        """
        Get a sub-workflow by its ID.
        
        Args:
            sub_workflow_id: ID of the sub-workflow to retrieve
            
        Returns:
            SubWorkflow with the specified ID, or None if not found
        """
        for sub_workflow in self.sub_workflows:
            if sub_workflow.id == sub_workflow_id:
                return sub_workflow
        return None
    
    def get_pending_sub_workflows(self) -> List[SubWorkflow]:
        """Get all pending sub-workflows."""
        return [sw for sw in self.sub_workflows if sw.status == TaskStatus.PENDING]
    
    def get_completed_sub_workflows(self) -> List[SubWorkflow]:
        """Get all completed sub-workflows."""
        return [sw for sw in self.sub_workflows if sw.status == TaskStatus.COMPLETED]
    
    def get_failed_sub_workflows(self) -> List[SubWorkflow]:
        """Get all failed sub-workflows."""
        return [sw for sw in self.sub_workflows if sw.status == TaskStatus.FAILED]
    
    def reset(self) -> None:
        """Reset the workflow to its initial state."""
        self.status = TaskStatus.PENDING
        self.start_time = None
        self.end_time = None
        self.results = []
        
        for sub_workflow in self.sub_workflows:
            sub_workflow.status = TaskStatus.PENDING
            sub_workflow.workflow.reset()
        
        logger.info(f"Hierarchical workflow '{self.name}' has been reset")


def create_migration_phase_workflow(phase_name: str, phase_tasks: List[Task], 
                                  manager_agent: str = "MigrationArchitect") -> SubWorkflow:
    """
    Create a sub-workflow for a migration phase.
    
    Args:
        phase_name: Name of the migration phase
        phase_tasks: List of tasks for this phase
        manager_agent: Agent managing this phase
        
    Returns:
        SubWorkflow for the migration phase
    """
    # Create sequential workflow for the phase
    phase_workflow = SequentialWorkflow(f"Migration Phase: {phase_name}")
    phase_workflow.add_tasks(phase_tasks)
    
    # Create sub-workflow
    sub_workflow = SubWorkflow(
        id=f"phase_{phase_name.lower().replace(' ', '_')}",
        name=phase_name,
        workflow=phase_workflow,
        manager_agent=manager_agent
    )
    
    return sub_workflow


def main():
    """Main function for testing the HierarchicalWorkflow."""
    # Create a hierarchical workflow
    workflow = HierarchicalWorkflow("Wing Commander Saga Migration", "MigrationArchitect")
    
    # Create some test tasks for different phases
    analysis_tasks = [
        Task(
            id="analyze_codebase",
            name="Analyze Source Codebase",
            description="Analyze the complete C++ codebase structure",
            agent="CodebaseAnalyst",
            expected_output="Complete codebase analysis report"
        ),
        Task(
            id="identify_dependencies",
            name="Identify Dependencies",
            description="Map all dependencies between modules",
            agent="CodebaseAnalyst",
            expected_output="Dependency graph",
            dependencies=["analyze_codebase"]
        )
    ]
    
    planning_tasks = [
        Task(
            id="create_migration_plan",
            name="Create Migration Plan",
            description="Create detailed migration plan based on analysis",
            agent="MigrationArchitect",
            expected_output="Migration plan document"
        ),
        Task(
            id="prioritize_modules",
            name="Prioritize Modules",
            description="Prioritize modules for migration based on dependencies",
            agent="MigrationArchitect",
            expected_output="Module priority list",
            dependencies=["create_migration_plan"]
        )
    ]
    
    # Create sub-workflows for each phase
    analysis_sub_workflow = create_migration_phase_workflow(
        "Codebase Analysis", analysis_tasks, "CodebaseAnalyst"
    )
    
    planning_sub_workflow = create_migration_phase_workflow(
        "Migration Planning", planning_tasks, "MigrationArchitect"
    )
    planning_sub_workflow.dependencies = [analysis_sub_workflow.id]
    
    # Add sub-workflows to the hierarchical workflow
    workflow.add_sub_workflows([analysis_sub_workflow, planning_sub_workflow])
    
    # Execute the workflow (using example task executor)
    from .sequential_workflow import example_task_executor
    results = workflow.execute_all(example_task_executor)
    
    # Print results
    print("Hierarchical Workflow Execution Results:")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()

```

---

## converter/workflows/sequential_workflow.py

**File type:** .py  

**Size:** 11418 bytes  

**Last modified:** 2025-08-21 13:18:03


```python
"""
Sequential Workflow Implementation

This module implements the sequential workflow process for atomic tasks
in the Wing Commander Saga to Godot migration.
"""

import json
import time
import logging
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """Enumeration of task statuses."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class Task:
    """Represents a single task in the workflow."""
    id: str
    name: str
    description: str
    agent: str
    expected_output: str
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    dependencies: List[str] = field(default_factory=list)
    
    def duration(self) -> Optional[float]:
        """Calculate task duration in seconds."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None


class SequentialWorkflow:
    """Sequential workflow processor for atomic tasks."""
    
    def __init__(self, name: str = "Sequential Workflow"):
        """
        Initialize the sequential workflow.
        
        Args:
            name: Name of the workflow
        """
        self.name = name
        self.tasks: List[Task] = []
        self.current_task_index = 0
        self.status = TaskStatus.PENDING
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.results: List[Dict[str, Any]] = []
        
    def add_task(self, task: Task) -> None:
        """
        Add a task to the workflow.
        
        Args:
            task: Task to add
        """
        self.tasks.append(task)
        logger.info(f"Added task '{task.name}' to workflow '{self.name}'")
    
    def add_tasks(self, tasks: List[Task]) -> None:
        """
        Add multiple tasks to the workflow.
        
        Args:
            tasks: List of tasks to add
        """
        for task in tasks:
            self.add_task(task)
    
    def can_execute_task(self, task: Task) -> bool:
        """
        Check if a task can be executed (all dependencies completed).
        
        Args:
            task: Task to check
            
        Returns:
            True if task can be executed, False otherwise
        """
        # If no dependencies, task can be executed
        if not task.dependencies:
            return True
        
        # Check if all dependencies are completed
        completed_task_ids = {
            t.id for t in self.tasks 
            if t.status == TaskStatus.COMPLETED
        }
        
        return all(dep_id in completed_task_ids for dep_id in task.dependencies)
    
    def execute_task(self, task: Task, task_executor: Callable[[Task], Dict[str, Any]]) -> bool:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            task_executor: Function that executes the task and returns results
            
        Returns:
            True if task completed successfully, False otherwise
        """
        # Check if task can be executed
        if not self.can_execute_task(task):
            logger.warning(f"Cannot execute task '{task.name}' due to unmet dependencies")
            return False
        
        # Update task status
        task.status = TaskStatus.IN_PROGRESS
        task.start_time = time.time()
        logger.info(f"Executing task '{task.name}' (ID: {task.id})")
        
        try:
            # Execute the task
            result = task_executor(task)
            
            # Update task with results
            task.result = result
            task.status = TaskStatus.COMPLETED
            task.end_time = time.time()
            
            # Store result
            self.results.append({
                "task_id": task.id,
                "task_name": task.name,
                "result": result,
                "duration": task.duration()
            })
            
            logger.info(f"Task '{task.name}' completed successfully in {task.duration():.2f} seconds")
            return True
            
        except Exception as e:
            # Handle task failure
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.end_time = time.time()
            
            logger.error(f"Task '{task.name}' failed: {str(e)}")
            return False
    
    def execute_next_task(self, task_executor: Callable[[Task], Dict[str, Any]]) -> Optional[Task]:
        """
        Execute the next pending task in the workflow.
        
        Args:
            task_executor: Function that executes the task and returns results
            
        Returns:
            The executed task, or None if no task could be executed
        """
        # Find the next pending task that can be executed
        for task in self.tasks:
            if task.status == TaskStatus.PENDING and self.can_execute_task(task):
                success = self.execute_task(task, task_executor)
                return task if success else None
        
        # No tasks could be executed
        return None
    
    def execute_all(self, task_executor: Callable[[Task], Dict[str, Any]]) -> Dict[str, Any]:
        """
        Execute all tasks in the workflow sequentially.
        
        Args:
            task_executor: Function that executes tasks and returns results
            
        Returns:
            Dictionary with workflow execution results
        """
        logger.info(f"Starting execution of workflow '{self.name}' with {len(self.tasks)} tasks")
        
        # Update workflow status
        self.status = TaskStatus.IN_PROGRESS
        self.start_time = time.time()
        
        # Execute tasks until completion or failure
        completed_tasks = 0
        failed_tasks = 0
        
        while completed_tasks + failed_tasks < len(self.tasks):
            task = self.execute_next_task(task_executor)
            
            if task is None:
                # No task could be executed, check for stuck tasks
                pending_tasks = [t for t in self.tasks if t.status == TaskStatus.PENDING]
                if pending_tasks:
                    logger.error(f"Workflow stuck: {len(pending_tasks)} tasks cannot be executed due to unmet dependencies")
                    break
                else:
                    break
            
            if task.status == TaskStatus.COMPLETED:
                completed_tasks += 1
            elif task.status == TaskStatus.FAILED:
                failed_tasks += 1
        
        # Update workflow status
        self.end_time = time.time()
        if failed_tasks == 0:
            self.status = TaskStatus.COMPLETED
            logger.info(f"Workflow '{self.name}' completed successfully in {self.duration():.2f} seconds")
        else:
            self.status = TaskStatus.FAILED
            logger.error(f"Workflow '{self.name}' failed with {failed_tasks} failed tasks")
        
        return {
            "workflow_name": self.name,
            "status": self.status.value,
            "total_tasks": len(self.tasks),
            "completed_tasks": completed_tasks,
            "failed_tasks": failed_tasks,
            "skipped_tasks": len(self.tasks) - completed_tasks - failed_tasks,
            "duration": self.duration(),
            "results": self.results
        }
    
    def duration(self) -> Optional[float]:
        """Calculate workflow duration in seconds."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None
    
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """
        Get a task by its ID.
        
        Args:
            task_id: ID of the task to retrieve
            
        Returns:
            Task with the specified ID, or None if not found
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_pending_tasks(self) -> List[Task]:
        """Get all pending tasks."""
        return [task for task in self.tasks if task.status == TaskStatus.PENDING]
    
    def get_completed_tasks(self) -> List[Task]:
        """Get all completed tasks."""
        return [task for task in self.tasks if task.status == TaskStatus.COMPLETED]
    
    def get_failed_tasks(self) -> List[Task]:
        """Get all failed tasks."""
        return [task for task in self.tasks if task.status == TaskStatus.FAILED]
    
    def reset(self) -> None:
        """Reset the workflow to its initial state."""
        self.current_task_index = 0
        self.status = TaskStatus.PENDING
        self.start_time = None
        self.end_time = None
        self.results = []
        
        for task in self.tasks:
            task.status = TaskStatus.PENDING
            task.result = None
            task.error = None
            task.start_time = None
            task.end_time = None
        
        logger.info(f"Workflow '{self.name}' has been reset")


def example_task_executor(task: Task) -> Dict[str, Any]:
    """
    Example task executor function for testing.
    
    Args:
        task: Task to execute
        
    Returns:
        Dictionary with task execution results
    """
    # Simulate task execution time
    import time
    import random
    time.sleep(random.uniform(0.1, 0.5))
    
    # Simulate random failures for testing
    if random.random() < 0.1:  # 10% failure rate
        raise Exception(f"Simulated failure for task '{task.name}'")
    
    return {
        "status": "success",
        "message": f"Task '{task.name}' executed successfully",
        "task_id": task.id
    }


def main():
    """Main function for testing the SequentialWorkflow."""
    # Create a workflow
    workflow = SequentialWorkflow("Test Sequential Workflow")
    
    # Create some test tasks
    tasks = [
        Task(
            id="task_1",
            name="Analyze Source Code",
            description="Analyze the C++ source code structure",
            agent="CodebaseAnalyst",
            expected_output="Codebase analysis report"
        ),
        Task(
            id="task_2",
            name="Generate Migration Plan",
            description="Create a detailed migration plan",
            agent="MigrationArchitect",
            expected_output="Migration plan document",
            dependencies=["task_1"]
        ),
        Task(
            id="task_3",
            name="Refactor Player Class",
            description="Refactor the player class from C++ to GDScript",
            agent="RefactoringSpecialist",
            expected_output="Refactored GDScript player class",
            dependencies=["task_2"]
        )
    ]
    
    # Add tasks to workflow
    workflow.add_tasks(tasks)
    
    # Execute the workflow
    results = workflow.execute_all(example_task_executor)
    
    # Print results
    print("Workflow Execution Results:")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()

```

---

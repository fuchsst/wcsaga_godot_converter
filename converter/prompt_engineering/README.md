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
# Prompt Engineering Agent

This directory contains the implementation of the Prompt Engineering Agent, which creates precise prompts for the CLI agent.

Based on the "Agentic Migration with CLI Agents" document, this agent is specifically configured to work with the **qwen-code** CLI agent:

Responsibilities:
- Convert atomic tasks and code context into precise, effective prompts for qwen-code
- Use structured prompt templates specifically designed for qwen-code
- Ensure all prompts include explicit instructions for qwen-code's response format
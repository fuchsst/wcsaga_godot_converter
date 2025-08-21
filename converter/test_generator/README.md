# Test Generator Agent

This directory contains the implementation of the Test Generator agent, which creates unit tests.

Based on the "Agentic Migration with CLI Agents" document, this agent is specifically configured to work with the **qwen-code** CLI agent:

Responsibilities:
- Receive newly generated Godot files and analyst's report
- Write comprehensive suite of unit tests using GUT framework
- Ensure 100% test coverage for public methods and signals
- Use qwen-code CLI agent for all test generation tasks
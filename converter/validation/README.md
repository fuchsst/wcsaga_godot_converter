# Validation Engineer Agent

This directory contains the implementation of the Validation Engineer agent, which validates generated code.

Based on the "Agentic Migration with CLI Agents" document, this agent is specifically configured to work with the **qwen-code** CLI agent:

Responsibilities:
- Execute generated code and tests in headless Godot environment
- Capture results (compilation status, test pass/fail, error logs)
- Run security scans on generated code
- Report outcomes as structured JSON
- Work specifically with qwen-code generated outputs
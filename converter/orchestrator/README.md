# Orchestrator Agent

This directory contains the implementation of the Orchestrator agent, which serves as the project manager.

Based on the "Agentic Migration with CLI Agents" document, this agent is powered by the **DeepSeek V3.1** model and follows these principles:

Responsibilities:
- Ingest the migration plan
- Shard tasks into atomic units
- Manage the task queue
- Orchestrate the workflow between other agents
- Dynamically select workflow models (sequential or hierarchical) based on task complexity
- Use DeepSeek V3.1 model for advanced reasoning and planning
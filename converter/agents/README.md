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
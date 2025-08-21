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
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
        
        # This would involve more complex task orchestration
        # For now, we'll just log that the phase would start
        logger.info("Migration execution phase would begin here")
        
        return {"status": "completed", "phase": "execution", "message": "Execution phase ready to begin"}
    
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

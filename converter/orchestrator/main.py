#!/usr/bin/env python3
"""
Main Orchestrator for Wing Commander Saga to Godot Migration

This script serves as the entry point for the hierarchical multi-agent migration system.
It uses LangGraph for deterministic state management.
"""

import os
import sys
import argparse
import logging
import yaml
import asyncio
from typing import List, Dict, Any
from pathlib import Path

# Add the converter directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import configuration manager
from config.config_manager import get_config_manager

# Import LangGraph orchestrator
from .langgraph_orchestrator import LangGraphOrchestrator

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
    """Main orchestrator for the migration process using LangGraph."""
    
    def __init__(self, source_path: str, target_path: str):
        """
        Initialize the migration orchestrator.
        
        Args:
            source_path: Path to the source C++ codebase
            target_path: Path to the target Godot project
        """
        self.source_path = Path(source_path)
        self.target_path = Path(target_path)
        self.langgraph_orchestrator = None
        
        # Validate paths
        if not self.source_path.exists():
            raise ValueError(f"Source path does not exist: {self.source_path}")
        
        # Create target directory if it doesn't exist
        self.target_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize LangGraph orchestrator
        self._initialize_langgraph_orchestrator()
    
    def _initialize_langgraph_orchestrator(self):
        """Initialize the LangGraph orchestrator."""
        logger.info("Initializing LangGraph orchestrator...")
        
        # Get graph configuration
        graph_config = config_manager.get_graph_config()
        graph_file = graph_config.get("file", "dependency_graph.json")
        
        # Create LangGraph orchestrator
        self.langgraph_orchestrator = LangGraphOrchestrator(
            source_path=str(self.source_path),
            target_path=str(self.target_path),
            graph_file=graph_file
        )
        
        logger.info("LangGraph orchestrator initialized successfully")
    
    def run_migration(self, phase: str = "all") -> Dict[str, Any]:
        """
        Run the migration process using LangGraph.
        
        Args:
            phase: Migration phase to run ("all", "analysis", "planning", "execution")
            
        Returns:
            Dictionary with migration results
        """
        logger.info(f"Starting migration process (phase: {phase}) using LangGraph")
        
        try:
            # For now, we'll focus on execution phase with LangGraph
            # Analysis and planning phases will be handled by individual LangGraph nodes
            if phase == "execution" or phase == "all":
                result = self._run_execution_phase()
                return result
            
            # Default case - return status for other phases (to be implemented)
            return {"status": "pending", "message": f"Phase {phase} will be implemented as LangGraph nodes"}
            
        except Exception as e:
            logger.error(f"Migration process failed: {str(e)}", exc_info=True)
            return {"status": "failed", "error": str(e)}
    
    def _run_execution_phase(self) -> Dict[str, Any]:
        """Run the migration execution phase using LangGraph."""
        logger.info("Running migration execution phase with LangGraph...")
        
        try:
            # Create a sample task to demonstrate LangGraph execution
            # In a real implementation, this would come from task queue or dependency graph
            sample_task = {
                "task_id": "SHIP-GTC_FENRIS",
                "entity_name": "GTC Fenris",
                "source_files": ["source/tables/ships.tbl", "source/models/fenris.pof"]
            }
            
            # Execute the bolt using LangGraph
            result = asyncio.run(self.langgraph_orchestrator.execute_bolt(
                task_id=sample_task["task_id"],
                entity_name=sample_task["entity_name"],
                source_files=sample_task["source_files"]
            ))
            
            logger.info("Migration execution phase completed with LangGraph")
            return {
                "status": "completed", 
                "phase": "execution", 
                "message": "Execution phase completed successfully with LangGraph",
                "details": result
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
        langgraph_status = self.langgraph_orchestrator.get_status() if self.langgraph_orchestrator else {}
        
        return {
            "source_path": str(self.source_path),
            "target_path": str(self.target_path),
            "orchestrator_type": "LangGraph",
            "langgraph_status": langgraph_status
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

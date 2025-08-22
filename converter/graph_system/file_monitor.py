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
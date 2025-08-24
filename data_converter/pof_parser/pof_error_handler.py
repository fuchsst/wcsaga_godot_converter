#!/usr/bin/env python3
"""
POF Error Handler - Unified error handling system.

This module consolidates all error handling logic into a single, comprehensive
system that follows the Rust reference implementation patterns with robust
error recovery and detailed diagnostic information.

Based on Rust error handling principles with enhanced context tracking.
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any, Set

logger = logging.getLogger(__name__)


class ErrorSeverity(Enum):
    """Error severity levels following industry standards."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class ErrorCategory(Enum):
    """Error categories for systematic classification."""
    VALIDATION = "VALIDATION"
    PARSING = "PARSING"
    COMPATIBILITY = "COMPATIBILITY"
    DATA_INTEGRITY = "DATA_INTEGRITY"
    MEMORY = "MEMORY"
    IO = "IO"
    UNKNOWN = "UNKNOWN"


@dataclass
class POFError:
    """Enhanced error information with rich context and position tracking."""
    message: str
    severity: ErrorSeverity
    category: ErrorCategory
    file_position: Optional[int] = None
    chunk_id: Optional[int] = None
    chunk_name: Optional[str] = None
    version: Optional[int] = None
    recovery_action: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for serialization."""
        return {
            'message': self.message,
            'severity': self.severity.value,
            'category': self.category.value,
            'file_position': self.file_position,
            'chunk_id': self.chunk_id,
            'chunk_name': self.chunk_name,
            'version': self.version,
            'recovery_action': self.recovery_action,
            'context': self.context,
            'timestamp': self.timestamp
        }
    
    def __str__(self) -> str:
        """Human-readable error representation with context."""
        parts = [f"[{self.severity.value}] {self.message}"]
        
        # Add positional context
        if self.file_position is not None:
            parts.append(f"at position 0x{self.file_position:X}")
        
        # Add chunk context
        if self.chunk_name:
            parts.append(f"in chunk {self.chunk_name}")
        elif self.chunk_id is not None:
            parts.append(f"in chunk 0x{self.chunk_id:08X}")
        
        # Add version context
        if self.version is not None:
            parts.append(f"(version {self.version})")
        
        # Add recovery guidance
        if self.recovery_action:
            parts.append(f"-> {self.recovery_action}")
        
        return " ".join(parts)

    def __hash__(self) -> int:
        """Make errors hashable for deduplication."""
        return hash((
            self.message,
            self.severity,
            self.category,
            self.file_position,
            self.chunk_id,
            self.version
        ))

    def __eq__(self, other) -> bool:
        """Check equality for deduplication."""
        if not isinstance(other, POFError):
            return False
        return (
            self.message == other.message and
            self.severity == other.severity and
            self.category == other.category and
            self.file_position == other.file_position and
            self.chunk_id == other.chunk_id and
            self.version == other.version
        )


class POFErrorRegistry:
    """Centralized error registry for tracking and deduplication."""
    
    def __init__(self):
        """Initialize error registry."""
        self._errors: Set[POFError] = set()
        self._error_list: List[POFError] = []
        self._duplicate_count: Dict[str, int] = {}
    
    def register_error(self, error: POFError) -> bool:
        """
        Register an error, returning True if it was new (False if duplicate).
        
        This helps avoid spamming identical errors during parsing.
        """
        if error in self._errors:
            # Increment duplicate counter
            error_key = f"{error.message}:{error.file_position}:{error.chunk_id}"
            self._duplicate_count[error_key] = self._duplicate_count.get(error_key, 1) + 1
            return False
        else:
            self._errors.add(error)
            self._error_list.append(error)
            return True
    
    def get_all_errors(self) -> List[POFError]:
        """Get all registered errors."""
        return self._error_list.copy()
    
    def get_duplicate_count(self, error: POFError) -> int:
        """Get count of duplicate occurrences for an error."""
        error_key = f"{error.message}:{error.file_position}:{error.chunk_id}"
        return self._duplicate_count.get(error_key, 1)
    
    def clear(self) -> None:
        """Clear all registered errors."""
        self._errors.clear()
        self._error_list.clear()
        self._duplicate_count.clear()


class UnifiedPOFErrorHandler:
    """Comprehensive, unified error handler for POF parsing."""
    
    def __init__(self):
        """Initialize unified error handler."""
        self.registry = POFErrorRegistry()
        self._current_position = 0
        self._current_chunk_id = None
        self._current_chunk_name = None
        self._current_version = None
        self._session_start_time = None
        
        # Performance tracking
        self._error_count_by_type: Dict[str, int] = {}
        
        # Initialize session
        import time
        self._session_start_time = time.time()
    
    # --- Context Management ---
    
    def set_position(self, position: int) -> None:
        """Set current file position for error tracking."""
        self._current_position = position
    
    def set_chunk_context(self, chunk_id: Optional[int], chunk_name: Optional[str] = None) -> None:
        """Set current chunk context for error tracking."""
        self._current_chunk_id = chunk_id
        self._current_chunk_name = chunk_name
    
    def set_version_context(self, version: Optional[int]) -> None:
        """Set current version context."""
        self._current_version = version
    
    def reset_context(self) -> None:
        """Reset all context information."""
        self._current_position = 0
        self._current_chunk_id = None
        self._current_chunk_name = None
        self._current_version = None
    
    # --- Error Creation and Registration ---
    
    def create_error(self, 
                    message: str, 
                    severity: ErrorSeverity = ErrorSeverity.ERROR,
                    category: ErrorCategory = ErrorCategory.PARSING,
                    recovery_action: Optional[str] = None,
                    context: Optional[Dict[str, Any]] = None) -> POFError:
        """
        Create a new error with current context.
        
        This method creates the error but doesn't register it automatically.
        Use add_error() to both create and register.
        """
        import time
        
        error = POFError(
            message=message,
            severity=severity,
            category=category,
            file_position=self._current_position,
            chunk_id=self._current_chunk_id,
            chunk_name=self._current_chunk_name,
            version=self._current_version,
            recovery_action=recovery_action,
            context=context or {},
            timestamp=time.time()
        )
        
        return error
    
    def add_error(self, 
                 message: str, 
                 severity: ErrorSeverity = ErrorSeverity.ERROR,
                 category: ErrorCategory = ErrorCategory.PARSING,
                 recovery_action: Optional[str] = None,
                 context: Optional[Dict[str, Any]] = None) -> POFError:
        """
        Create and register a new error with current context.
        
        Returns:
            The created and registered POFError object
        """
        error = self.create_error(
            message=message,
            severity=severity,
            category=category,
            recovery_action=recovery_action,
            context=context
        )
        
        # Register the error
        is_new = self.registry.register_error(error)
        
        # Log the error if it's new or if we haven't logged too many duplicates
        if is_new or self.registry.get_duplicate_count(error) <= 5:
            self._log_error(error, is_new)
        
        # Track error statistics
        self._track_error_type(error)
        
        return error
    
    def _log_error(self, error: POFError, is_new: bool) -> None:
        """Log error with appropriate severity level."""
        # Get appropriate logger method based on severity
        log_methods = {
            ErrorSeverity.DEBUG: logger.debug,
            ErrorSeverity.INFO: logger.info,
            ErrorSeverity.WARNING: logger.warning,
            ErrorSeverity.ERROR: logger.error,
            ErrorSeverity.CRITICAL: logger.critical
        }
        
        log_method = log_methods.get(error.severity, logger.error)
        
        # Add duplicate count to message if this is a duplicate
        if not is_new:
            duplicate_count = self.registry.get_duplicate_count(error)
            if duplicate_count > 1:
                logger.debug(f"Suppressed {duplicate_count-1} duplicate errors like: {error.message}")
        
        # Actually log the error
        log_method(str(error))
    
    def _track_error_type(self, error: POFError) -> None:
        """Track error statistics by type."""
        category_key = error.category.value
        self._error_count_by_type[category_key] = self._error_count_by_type.get(category_key, 0) + 1
    
    # --- Specialized Error Methods ---
    
    def add_validation_error(self, message: str, **kwargs) -> POFError:
        """Add validation-specific error."""
        return self.add_error(
            message, 
            severity=ErrorSeverity.ERROR,
            category=ErrorCategory.VALIDATION,
            **kwargs
        )
    
    def add_parsing_error(self, message: str, **kwargs) -> POFError:
        """Add parsing-specific error."""
        return self.add_error(
            message, 
            severity=ErrorSeverity.ERROR,
            category=ErrorCategory.PARSING,
            **kwargs
        )
    
    def add_compatibility_warning(self, message: str, **kwargs) -> POFError:
        """Add compatibility warning."""
        return self.add_error(
            message, 
            severity=ErrorSeverity.WARNING,
            category=ErrorCategory.COMPATIBILITY,
            **kwargs
        )
    
    def add_data_integrity_warning(self, message: str, **kwargs) -> POFError:
        """Add data integrity warning."""
        return self.add_error(
            message, 
            severity=ErrorSeverity.WARNING,
            category=ErrorCategory.DATA_INTEGRITY,
            **kwargs
        )
    
    def add_memory_error(self, message: str, **kwargs) -> POFError:
        """Add memory-related error."""
        return self.add_error(
            message,
            severity=ErrorSeverity.ERROR,
            category=ErrorCategory.MEMORY,
            **kwargs
        )
    
    def add_io_error(self, message: str, **kwargs) -> POFError:
        """Add I/O error."""
        return self.add_error(
            message,
            severity=ErrorSeverity.ERROR,
            category=ErrorCategory.IO,
            **kwargs
        )
    
    # --- Error Query Methods ---
    
    def has_errors(self, min_severity: ErrorSeverity = ErrorSeverity.ERROR) -> bool:
        """Check if there are errors of at least the given severity."""
        severity_levels = list(ErrorSeverity)
        min_level = severity_levels.index(min_severity)
        
        return any(
            severity_levels.index(error.severity) >= min_level
            for error in self.registry.get_all_errors()
        )
    
    def get_errors(self, 
                  severity: Optional[ErrorSeverity] = None,
                  category: Optional[ErrorCategory] = None,
                  max_count: Optional[int] = None) -> List[POFError]:
        """Get errors filtered by severity and/or category."""
        filtered_errors = self.registry.get_all_errors()
        
        if severity is not None:
            filtered_errors = [e for e in filtered_errors if e.severity == severity]
        
        if category is not None:
            filtered_errors = [e for e in filtered_errors if e.category == category]
        
        if max_count is not None and len(filtered_errors) > max_count:
            filtered_errors = filtered_errors[:max_count]
        
        return filtered_errors
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """Get comprehensive error statistics."""
        all_errors = self.registry.get_all_errors()
        
        statistics = {
            'total_errors': len(all_errors),
            'by_severity': {},
            'by_category': self._error_count_by_type.copy(),
            'unique_errors': len(self.registry._errors),
            'duplicate_errors_suppressed': sum(
                count - 1 for count in self.registry._duplicate_count.values() if count > 1
            ),
            'session_duration': 0,
            'error_rate_per_second': 0
        }
        
        # Count by severity
        for error in all_errors:
            severity = error.severity.value
            statistics['by_severity'][severity] = statistics['by_severity'].get(severity, 0) + 1
        
        # Calculate session duration and rate
        if self._session_start_time:
            import time
            session_duration = time.time() - self._session_start_time
            statistics['session_duration'] = session_duration
            if session_duration > 0:
                statistics['error_rate_per_second'] = len(all_errors) / session_duration
        
        return statistics
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of all errors (deprecated - use get_error_statistics)."""
        return self.get_error_statistics()
    
    # --- Session Management ---
    
    def clear_errors(self) -> None:
        """Clear all errors from registry."""
        self.registry.clear()
        self._error_count_by_type.clear()
    
    def start_new_session(self) -> None:
        """Start a new error tracking session."""
        self.clear_errors()
        import time
        self._session_start_time = time.time()
    
    def end_session(self) -> Dict[str, Any]:
        """End current session and return final statistics."""
        stats = self.get_error_statistics()
        self.start_new_session()  # Reset for next session
        return stats
    
    # --- Recovery Planning ---
    
    def create_recovery_plan(self) -> Dict[str, Any]:
        """Create recovery plan based on errors encountered."""
        all_errors = self.registry.get_all_errors()
        critical_errors = [e for e in all_errors if e.severity == ErrorSeverity.CRITICAL]
        errors = [e for e in all_errors if e.severity == ErrorSeverity.ERROR]
        warnings = [e for e in all_errors if e.severity == ErrorSeverity.WARNING]
        
        recovery_plan = {
            'can_continue': len(critical_errors) == 0,
            'recommended_actions': [],
            'data_loss_expected': False,
            'partial_success_possible': len(errors) < 10,
            'error_statistics': self.get_error_statistics()
        }
        
        # Analyze errors for recovery recommendations
        parsing_errors = [e for e in errors if e.category == ErrorCategory.PARSING]
        validation_errors = [e for e in errors if e.category == ErrorCategory.VALIDATION]
        compatibility_issues = [e for e in warnings if e.category == ErrorCategory.COMPATIBILITY]
        
        if parsing_errors:
            recovery_plan['recommended_actions'].append(
                "Skip problematic chunks and continue parsing"
            )
            recovery_plan['data_loss_expected'] = True
        
        if validation_errors:
            recovery_plan['recommended_actions'].append(
                "Apply default values for invalid data"
            )
        
        if compatibility_issues:
            recovery_plan['recommended_actions'].append(
                "Use fallback parsing for incompatible features"
            )
        
        # If no specific recommendations, add general advice
        if not recovery_plan['recommended_actions'] and all_errors:
            recovery_plan['recommended_actions'].append(
                "Continue with best-effort parsing"
            )
        
        return recovery_plan
    
    def format_error_report(self, include_debug: bool = False, max_errors: int = 50) -> str:
        """Format comprehensive error report."""
        lines = ["POF Parsing Error Report", "=" * 40]
        
        stats = self.get_error_statistics()
        lines.append(f"Total errors: {stats['total_errors']}")
        lines.append(f"Unique errors: {stats['unique_errors']}")
        lines.append(f"Duplicates suppressed: {stats['duplicate_errors_suppressed']}")
        lines.append(f"Session duration: {stats['session_duration']:.2f}s")
        
        if stats['by_severity']:
            lines.append("\nBy severity:")
            for severity, count in sorted(stats['by_severity'].items()):
                lines.append(f"  {severity}: {count}")
        
        if stats['by_category']:
            lines.append("\nBy category:")
            for category, count in sorted(stats['by_category'].items()):
                lines.append(f"  {category}: {count}")
        
        # Add detailed error list (limited)
        all_errors = self.registry.get_all_errors()
        if all_errors and include_debug:
            display_errors = all_errors[:max_errors]
            lines.append(f"\nDetailed errors (showing {len(display_errors)}/{len(all_errors)}):")
            for i, error in enumerate(display_errors, 1):
                lines.append(f"{i:3d}. {error}")
            
            if len(all_errors) > max_errors:
                lines.append(f"... and {len(all_errors) - max_errors} more errors")
        
        # Add recovery plan
        recovery_plan = self.create_recovery_plan()
        lines.append("\nRecovery plan:")
        lines.append(f"Can continue: {recovery_plan['can_continue']}")
        lines.append(f"Data loss expected: {recovery_plan['data_loss_expected']}")
        lines.append(f"Partial success possible: {recovery_plan['partial_success_possible']}")
        
        if recovery_plan['recommended_actions']:
            lines.append("Recommended actions:")
            for action in recovery_plan['recommended_actions']:
                lines.append(f"  • {action}")
        
        return "\n".join(lines)


# --- Global Error Handler Instance ---

# Singleton pattern for global error handler
_error_handler_instance: Optional[UnifiedPOFErrorHandler] = None


def get_global_error_handler() -> UnifiedPOFErrorHandler:
    """Get the global singleton error handler instance."""
    global _error_handler_instance
    if _error_handler_instance is None:
        _error_handler_instance = UnifiedPOFErrorHandler()
    return _error_handler_instance


# --- Convenience Functions ---

def set_error_context(position: Optional[int] = None, 
                     chunk_id: Optional[int] = None, 
                     chunk_name: Optional[str] = None,
                     version: Optional[int] = None) -> None:
    """Set error context globally."""
    handler = get_global_error_handler()
    if position is not None:
        handler.set_position(position)
    if chunk_id is not None or chunk_name is not None:
        handler.set_chunk_context(chunk_id, chunk_name)
    if version is not None:
        handler.set_version_context(version)


def add_error(message: str, 
             severity: ErrorSeverity = ErrorSeverity.ERROR,
             category: ErrorCategory = ErrorCategory.PARSING,
             recovery_action: Optional[str] = None,
             context: Optional[Dict[str, Any]] = None) -> POFError:
    """Add an error globally."""
    handler = get_global_error_handler()
    return handler.add_error(
        message=message,
        severity=severity,
        category=category,
        recovery_action=recovery_action,
        context=context
    )


def get_error_statistics() -> Dict[str, Any]:
    """Get global error statistics."""
    handler = get_global_error_handler()
    return handler.get_error_statistics()


def clear_global_errors() -> None:
    """Clear all global errors."""
    handler = get_global_error_handler()
    handler.clear_errors()


def format_global_error_report(include_debug: bool = False) -> str:
    """Format global error report."""
    handler = get_global_error_handler()
    return handler.format_error_report(include_debug)
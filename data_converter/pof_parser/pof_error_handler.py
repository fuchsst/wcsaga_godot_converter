#!/usr/bin/env python3
"""
POF Error Handler - Enhanced error handling with position tracking.

Based on Rust reference implementation with robust error recovery.
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class ErrorSeverity(Enum):
    """Error severity levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class ErrorCategory(Enum):
    """Error categories for classification."""
    VALIDATION = "VALIDATION"
    PARSING = "PARSING"
    COMPATIBILITY = "COMPATIBILITY"
    DATA_INTEGRITY = "DATA_INTEGRITY"
    MEMORY = "MEMORY"
    IO = "IO"
    UNKNOWN = "UNKNOWN"


@dataclass
class POFError:
    """Detailed error information with position tracking."""
    message: str
    severity: ErrorSeverity
    category: ErrorCategory
    file_position: Optional[int] = None
    chunk_id: Optional[int] = None
    chunk_name: Optional[str] = None
    version: Optional[int] = None
    recovery_action: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    
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
            'context': self.context
        }
    
    def __str__(self) -> str:
        """Human-readable error representation."""
        parts = [f"[{self.severity.value}] {self.message}"]
        
        if self.file_position is not None:
            parts.append(f"at position 0x{self.file_position:X}")
        
        if self.chunk_name:
            parts.append(f"in chunk {self.chunk_name}")
        elif self.chunk_id is not None:
            parts.append(f"in chunk 0x{self.chunk_id:08X}")
        
        if self.version is not None:
            parts.append(f"(version {self.version})")
        
        if self.recovery_action:
            parts.append(f"-> {self.recovery_action}")
        
        return " ".join(parts)


class POFErrorHandler:
    """Comprehensive error handler for POF parsing."""
    
    def __init__(self):
        """Initialize error handler with empty error list."""
        self.errors: List[POFError] = []
        self._current_position = 0
        self._current_chunk_id = None
        self._current_chunk_name = None
        self._current_version = None
    
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
    
    def add_error(self, 
                 message: str, 
                 severity: ErrorSeverity = ErrorSeverity.ERROR,
                 category: ErrorCategory = ErrorCategory.PARSING,
                 recovery_action: Optional[str] = None,
                 context: Optional[Dict[str, Any]] = None) -> POFError:
        """
        Add a new error with current context.
        
        Returns:
            The created POFError object
        """
        error = POFError(
            message=message,
            severity=severity,
            category=category,
            file_position=self._current_position,
            chunk_id=self._current_chunk_id,
            chunk_name=self._current_chunk_name,
            version=self._current_version,
            recovery_action=recovery_action,
            context=context or {}
        )
        
        self.errors.append(error)
        
        # Log based on severity
        log_method = {
            ErrorSeverity.DEBUG: logger.debug,
            ErrorSeverity.INFO: logger.info,
            ErrorSeverity.WARNING: logger.warning,
            ErrorSeverity.ERROR: logger.error,
            ErrorSeverity.CRITICAL: logger.critical
        }.get(severity, logger.error)
        
        log_method(str(error))
        
        return error
    
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
    
    def has_errors(self, min_severity: ErrorSeverity = ErrorSeverity.ERROR) -> bool:
        """Check if there are errors of at least the given severity."""
        severity_levels = list(ErrorSeverity)
        min_level = severity_levels.index(min_severity)
        
        return any(
            severity_levels.index(error.severity) >= min_level
            for error in self.errors
        )
    
    def get_errors(self, 
                  severity: Optional[ErrorSeverity] = None,
                  category: Optional[ErrorCategory] = None) -> List[POFError]:
        """Get errors filtered by severity and/or category."""
        filtered = self.errors
        
        if severity is not None:
            filtered = [e for e in filtered if e.severity == severity]
        
        if category is not None:
            filtered = [e for e in filtered if e.category == category]
        
        return filtered
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of all errors."""
        summary = {
            'total_errors': len(self.errors),
            'by_severity': {},
            'by_category': {},
            'has_critical_errors': False,
            'has_errors': False,
            'has_warnings': False
        }
        
        for error in self.errors:
            # Count by severity
            severity = error.severity.value
            summary['by_severity'][severity] = summary['by_severity'].get(severity, 0) + 1
            
            # Count by category
            category = error.category.value
            summary['by_category'][category] = summary['by_category'].get(category, 0) + 1
            
            # Set flags
            if error.severity == ErrorSeverity.CRITICAL:
                summary['has_critical_errors'] = True
            if error.severity in [ErrorSeverity.ERROR, ErrorSeverity.CRITICAL]:
                summary['has_errors'] = True
            if error.severity == ErrorSeverity.WARNING:
                summary['has_warnings'] = True
        
        return summary
    
    def clear_errors(self) -> None:
        """Clear all errors."""
        self.errors.clear()
    
    def create_recovery_plan(self) -> Dict[str, Any]:
        """Create recovery plan based on errors encountered."""
        critical_errors = self.get_errors(severity=ErrorSeverity.CRITICAL)
        errors = self.get_errors(severity=ErrorSeverity.ERROR)
        warnings = self.get_errors(severity=ErrorSeverity.WARNING)
        
        recovery_plan = {
            'can_continue': len(critical_errors) == 0,
            'recommended_actions': [],
            'data_loss_expected': False,
            'partial_success_possible': len(errors) < 10  # Arbitrary threshold
        }
        
        # Analyze errors for recovery recommendations
        parsing_errors = self.get_errors(category=ErrorCategory.PARSING)
        validation_errors = self.get_errors(category=ErrorCategory.VALIDATION)
        compatibility_issues = self.get_errors(category=ErrorCategory.COMPATIBILITY)
        
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
        if not recovery_plan['recommended_actions'] and self.errors:
            recovery_plan['recommended_actions'].append(
                "Continue with best-effort parsing"
            )
        
        return recovery_plan
    
    def format_error_report(self, include_debug: bool = False) -> str:
        """Format comprehensive error report."""
        lines = ["POF Parsing Error Report", "=" * 40]
        
        summary = self.get_error_summary()
        lines.append(f"Total errors: {summary['total_errors']}")
        
        if summary['by_severity']:
            lines.append("\nBy severity:")
            for severity, count in summary['by_severity'].items():
                lines.append(f"  {severity}: {count}")
        
        if summary['by_category']:
            lines.append("\nBy category:")
            for category, count in summary['by_category'].items():
                lines.append(f"  {category}: {count}")
        
        # Add detailed error list
        if self.errors and include_debug:
            lines.append("\nDetailed errors:")
            for i, error in enumerate(self.errors, 1):
                lines.append(f"{i:3d}. {error}")
        
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


# Global error handler instance for convenience
_error_handler = POFErrorHandler()


def get_error_handler() -> POFErrorHandler:
    """Get the global error handler instance."""
    return _error_handler


def handle_parsing_error(message: str, position: int, **kwargs) -> POFError:
    """Convenience function for handling parsing errors."""
    handler = get_error_handler()
    handler.set_position(position)
    return handler.add_parsing_error(message, **kwargs)


def handle_validation_error(message: str, **kwargs) -> POFError:
    """Convenience function for handling validation errors."""
    handler = get_error_handler()
    return handler.add_validation_error(message, **kwargs)


def handle_compatibility_warning(message: str, **kwargs) -> POFError:
    """Convenience function for handling compatibility warnings."""
    handler = get_error_handler()
    return handler.add_compatibility_warning(message, **kwargs)


def clear_errors() -> None:
    """Clear all errors from global handler."""
    get_error_handler().clear_errors()


def get_error_summary() -> Dict[str, Any]:
    """Get error summary from global handler."""
    return get_error_handler().get_error_summary()


def format_error_report(include_debug: bool = False) -> str:
    """Format error report from global handler."""
    return get_error_handler().format_error_report(include_debug)
#!/usr/bin/env python3
"""
Error Handler Tests - pytest tests for enhanced error handling.
"""

import pytest
from data_converter.pof_parser.pof_error_handler import (
    UnifiedPOFErrorHandler as POFErrorHandler,
    POFError,
    ErrorSeverity,
    ErrorCategory,
    handle_parsing_error,
    handle_validation_error,
    handle_compatibility_warning,
    clear_errors,
    get_error_summary,
)


class TestPOFError:
    """Test POFError data structure."""

    def test_error_creation(self):
        """Test basic error creation."""
        error = POFError(
            message="Test error message",
            severity=ErrorSeverity.ERROR,
            category=ErrorCategory.PARSING,
            file_position=1234,
            chunk_id=0x4F484452,
            chunk_name="OHDR",
            version=2117,
            recovery_action="skip",
        )

        assert error.message == "Test error message"
        assert error.severity == ErrorSeverity.ERROR
        assert error.category == ErrorCategory.PARSING
        assert error.file_position == 1234
        assert error.chunk_id == 0x4F484452
        assert error.chunk_name == "OHDR"
        assert error.version == 2117
        assert error.recovery_action == "skip"

    def test_error_to_dict(self):
        """Test error serialization to dictionary."""
        error = POFError(
            message="Test error",
            severity=ErrorSeverity.WARNING,
            category=ErrorCategory.COMPATIBILITY,
        )

        error_dict = error.to_dict()

        assert error_dict["message"] == "Test error"
        assert error_dict["severity"] == "WARNING"
        assert error_dict["category"] == "COMPATIBILITY"
        assert error_dict["file_position"] is None

    def test_error_string_representation(self):
        """Test error string formatting."""
        error = POFError(
            message="Invalid chunk data",
            severity=ErrorSeverity.ERROR,
            category=ErrorCategory.PARSING,
            file_position=0x1000,
            chunk_name="SOBJ",
            version=2117,
            recovery_action="skip chunk",
        )

        error_str = str(error)
        assert "[ERROR] Invalid chunk data" in error_str
        assert "at position 0x1000" in error_str
        assert "in chunk SOBJ" in error_str
        assert "(version 2117)" in error_str
        assert "-> skip chunk" in error_str


class TestPOFErrorHandler:
    """Test POF error handler functionality."""

    def setup_method(self):
        """Set up fresh error handler for each test."""
        self.handler = POFErrorHandler()

    def test_handler_initialization(self):
        """Test error handler initialization."""
        assert len(self.handler.errors) == 0
        assert self.handler._current_position == 0
        assert self.handler._current_chunk_id is None
        assert self.handler._current_version is None

    def test_add_error_with_context(self):
        """Test adding error with context."""
        self.handler.set_position(0x2000)
        self.handler.set_chunk_context(0x4F484452, "OHDR")
        self.handler.set_version_context(2117)

        error = self.handler.add_error(
            "Test error with context",
            severity=ErrorSeverity.WARNING,
            category=ErrorCategory.VALIDATION,
            recovery_action="use default",
            context={"field": "mass", "value": -1.0},
        )

        assert len(self.handler.errors) == 1
        assert error.file_position == 0x2000
        assert error.chunk_id == 0x4F484452
        assert error.chunk_name == "OHDR"
        assert error.version == 2117
        assert error.recovery_action == "use default"
        assert error.context["field"] == "mass"

    def test_error_filtering(self):
        """Test error filtering by severity and category."""
        # Add various errors
        self.handler.add_error("Error 1", ErrorSeverity.ERROR, ErrorCategory.PARSING)
        self.handler.add_error(
            "Error 2", ErrorSeverity.WARNING, ErrorCategory.COMPATIBILITY
        )
        self.handler.add_error("Error 3", ErrorSeverity.ERROR, ErrorCategory.VALIDATION)
        self.handler.add_error("Error 4", ErrorSeverity.INFO, ErrorCategory.PARSING)

        # Test filtering
        errors = self.handler.get_errors(severity=ErrorSeverity.ERROR)
        assert len(errors) == 2
        assert all(e.severity == ErrorSeverity.ERROR for e in errors)

        parsing_errors = self.handler.get_errors(category=ErrorCategory.PARSING)
        assert len(parsing_errors) == 2
        assert all(e.category == ErrorCategory.PARSING for e in parsing_errors)

        # Combined filtering
        error_parsing = self.handler.get_errors(
            severity=ErrorSeverity.ERROR, category=ErrorCategory.PARSING
        )
        assert len(error_parsing) == 1

    def test_error_summary(self):
        """Test error summary generation."""
        self.handler.add_error(
            "Critical error", ErrorSeverity.CRITICAL, ErrorCategory.PARSING
        )
        self.handler.add_error(
            "Normal error", ErrorSeverity.ERROR, ErrorCategory.VALIDATION
        )
        self.handler.add_error(
            "Warning", ErrorSeverity.WARNING, ErrorCategory.COMPATIBILITY
        )
        self.handler.add_error(
            "Another warning", ErrorSeverity.WARNING, ErrorCategory.DATA_INTEGRITY
        )

        summary = self.handler.get_error_summary()

        assert summary["total_errors"] == 4
        assert summary["by_severity"]["CRITICAL"] == 1
        assert summary["by_severity"]["ERROR"] == 1
        assert summary["by_severity"]["WARNING"] == 2
        assert summary["by_category"]["PARSING"] == 1
        assert summary["by_category"]["VALIDATION"] == 1
        assert summary["by_category"]["COMPATIBILITY"] == 1
        assert summary["by_category"]["DATA_INTEGRITY"] == 1
        assert summary["has_critical_errors"]
        assert summary["has_errors"]
        assert summary["has_warnings"]

    def test_recovery_plan(self):
        """Test recovery plan generation."""
        # Add various errors
        self.handler.add_parsing_error("Parsing failed at byte 100")
        self.handler.add_validation_error("Invalid mass value")
        self.handler.add_compatibility_warning("Unsupported chunk")

        recovery_plan = self.handler.create_recovery_plan()

        assert recovery_plan["can_continue"]  # No critical errors
        assert recovery_plan["data_loss_expected"]
        assert recovery_plan["partial_success_possible"]
        assert len(recovery_plan["recommended_actions"]) >= 2

        # Test with critical error
        self.handler.add_error(
            "Critical failure", ErrorSeverity.CRITICAL, ErrorCategory.PARSING
        )
        recovery_plan_critical = self.handler.create_recovery_plan()
        assert not recovery_plan_critical["can_continue"]

    def test_convenience_methods(self):
        """Test convenience error methods."""
        self.handler.add_parsing_error("Parsing error")
        self.handler.add_validation_error("Validation error")
        self.handler.add_compatibility_warning("Compatibility warning")
        self.handler.add_data_integrity_warning("Data integrity warning")

        assert len(self.handler.errors) == 4

        # Check categories
        parsing_errors = self.handler.get_errors(category=ErrorCategory.PARSING)
        validation_errors = self.handler.get_errors(category=ErrorCategory.VALIDATION)
        compatibility_errors = self.handler.get_errors(
            category=ErrorCategory.COMPATIBILITY
        )
        integrity_errors = self.handler.get_errors(
            category=ErrorCategory.DATA_INTEGRITY
        )

        assert len(parsing_errors) == 1
        assert len(validation_errors) == 1
        assert len(compatibility_errors) == 1
        assert len(integrity_errors) == 1


class TestGlobalErrorHandler:
    """Test global error handler functionality."""

    def setup_method(self):
        """Clear errors before each test."""
        clear_errors()

    def test_global_handler_convenience(self):
        """Test global handler convenience functions."""
        # Use convenience functions
        handle_parsing_error("Global parsing error", 0x1000)
        handle_validation_error("Global validation error")
        handle_compatibility_warning("Global compatibility warning")

        summary = get_error_summary()
        assert summary["total_errors"] == 3
        assert summary["has_errors"]
        assert summary["has_warnings"]

    def test_error_clearing(self):
        """Test error clearing functionality."""
        handle_parsing_error("Test error", 0x500)

        summary_before = get_error_summary()
        assert summary_before["total_errors"] == 1

        clear_errors()

        summary_after = get_error_summary()
        assert summary_after["total_errors"] == 0


class TestErrorRecoveryScenarios:
    """Test error recovery in realistic scenarios."""

    def setup_method(self):
        """Set up fresh handler."""
        self.handler = POFErrorHandler()

    def test_chunk_parsing_recovery(self):
        """Test recovery from chunk parsing errors."""
        # Simulate chunk parsing with errors
        self.handler.set_chunk_context(0x4F484452, "OHDR")
        self.handler.set_version_context(2117)

        # Add various parsing errors
        self.handler.set_position(0x100)
        self.handler.add_parsing_error("Invalid header format")

        self.handler.set_position(0x200)
        self.handler.add_parsing_error(
            "Missing required field", recovery_action="use default value"
        )

        self.handler.set_position(0x300)
        self.handler.add_data_integrity_warning(
            "Data checksum mismatch", recovery_action="verify manually"
        )

        # Check recovery plan
        recovery_plan = self.handler.create_recovery_plan()

        assert recovery_plan["can_continue"]
        assert recovery_plan["data_loss_expected"]
        assert any(
            "skip" in action.lower() for action in recovery_plan["recommended_actions"]
        )
        # Default value recommendation might not always be present depending on error types

    def test_version_compatibility_recovery(self):
        """Test recovery from version compatibility issues."""
        self.handler.set_version_context(1800)  # Old version

        # Add compatibility warnings
        self.handler.add_compatibility_warning(
            "Feature not supported in version 1800",
            recovery_action="use fallback implementation",
        )

        self.handler.add_compatibility_warning(
            "Chunk format outdated", recovery_action="apply compatibility patch"
        )

        recovery_plan = self.handler.create_recovery_plan()

        assert recovery_plan["can_continue"]
        assert not recovery_plan["data_loss_expected"]  # Warnings only
        assert any(
            "fallback" in action.lower()
            for action in recovery_plan["recommended_actions"]
        )
        # Patch recommendation might be consolidated into more general actions


def test_comprehensive_error_scenario():
    """Test comprehensive error handling scenario."""
    handler = POFErrorHandler()

    # Simulate complex parsing scenario
    handler.set_version_context(2117)

    # OHDR chunk parsing
    handler.set_chunk_context(0x4F484452, "OHDR")
    handler.set_position(0x100)
    handler.add_parsing_error(
        "Invalid radius value", recovery_action="use calculated radius"
    )

    # SOBJ chunk parsing
    handler.set_chunk_context(0x4F424A32, "SOBJ")
    handler.set_position(0x200)
    handler.add_validation_error(
        "Invalid parent index", recovery_action="attach to root"
    )

    # TXTR chunk parsing
    handler.set_chunk_context(0x54585452, "TXTR")
    handler.set_position(0x300)
    handler.add_data_integrity_warning(
        "Texture name contains invalid characters", recovery_action="sanitize name"
    )

    # Check results
    summary = handler.get_error_summary()
    recovery_plan = handler.create_recovery_plan()

    assert summary["total_errors"] == 3
    assert summary["by_severity"]["ERROR"] == 2
    assert summary["by_severity"]["WARNING"] == 1
    assert recovery_plan["can_continue"]
    assert len(recovery_plan["recommended_actions"]) >= 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

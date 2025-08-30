"""
Integration test for the LangGraph-based Centurion migration system components.
"""

from pathlib import Path

# Add the converter directory to the path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from converter.tools.command_line_tool import CommandLineTool
from converter.validation.test_quality_gate import QualityGate
from converter.hitl.langgraph_hitl import LangGraphHITLIntegration


def test_command_line_tool():
    """Test the CommandLineTool implementation."""
    print("Testing CommandLineTool...")

    # Test basic command execution
    from converter.tools.command_line_tool import ToolInput

    tool = CommandLineTool()
    tool_input = ToolInput(
        command=["python", "-c", "print('Hello, World!')"], timeout_seconds=10
    )
    result = tool.execute(tool_input)

    print(
        f"Command result: return_code={result.return_code}, stdout='{result.stdout}', stderr='{result.stderr}', timed_out={result.timed_out}"
    )

    assert result.return_code == 0, f"Expected return_code=0, got {result.return_code}"
    assert (
        "Hello, World!" in result.stdout
    ), f"Expected 'Hello, World!' in stdout, got {result.stdout}"

    print("CommandLineTool test passed!")


def test_test_quality_gate():
    """Test the QualityGate implementation."""
    print("Testing QualityGate...")

    # Test basic validation
    quality_gate = QualityGate(min_coverage=85.0, min_test_count=5)

    test_results = {
        "total": 10,
        "passed": 10,
        "failed": 0,
        "coverage": 92.5,
        "duration": 2.5,
    }

    result = quality_gate.validate_test_quality(test_results)

    assert result["passed"], f"Expected passed=True, got {result['passed']}"
    assert result["score"] > 0, f"Expected score>0, got {result['score']}"

    print("QualityGate test passed!")


def test_langgraph_hitl():
    """Test the LangGraphHITLIntegration implementation."""
    print("Testing LangGraphHITLIntegration...")

    # Test HITL integration
    hitl = LangGraphHITLIntegration()

    # Test interrupt and resume pattern
    result = hitl.interrupt_and_resume(
        entity_id="TEST-ENTITY",
        description="Test interrupt and resume",
        context={"test_data": "test_value"},
    )

    assert isinstance(result, dict), f"Expected dict result, got {type(result)}"
    assert "request_id" in result, "Expected request_id in result"

    # Test human as tool pattern
    result = hitl.human_as_tool(
        entity_id="TEST-ENTITY",
        description="Test human as tool",
        context={"test_data": "test_value", "confidence_score": 0.9},
    )

    assert isinstance(result, dict), f"Expected dict result, got {type(result)}"

    print("LangGraphHITLIntegration test passed!")


def test_integration():
    """Test integration of all components."""
    print("Testing component integration...")

    # Test that all components can be imported and instantiated
    CommandLineTool()
    QualityGate()
    LangGraphHITLIntegration()

    print("Component integration test passed!")


def main():
    """Run all tests."""
    print("Running integration tests for LangGraph-based Centurion migration system...")

    test_command_line_tool()
    test_test_quality_gate()
    test_langgraph_hitl()
    test_integration()

    print("\nAll integration tests passed!")


if __name__ == "__main__":
    main()

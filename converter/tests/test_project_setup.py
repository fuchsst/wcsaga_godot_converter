"""
Simple test to verify the project setup and tooling.
"""


def test_project_setup():
    """Test that the project is set up correctly."""
    # This is a simple test to verify the testing infrastructure works
    assert True


def test_converter_package():
    """Test that the converter package can be imported."""
    import converter

    assert converter is not None
    assert hasattr(converter, "__version__")


def test_requirements_installed():
    """Test that required packages are installed."""
    # Test that pydantic can be imported
    import pydantic

    assert pydantic is not None

    # Test that yaml can be imported
    import yaml

    assert yaml is not None

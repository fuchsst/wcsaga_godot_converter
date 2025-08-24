"""
Test for new text table converters

Simple test to verify that our new converters can be imported and instantiated.
"""

import tempfile
from pathlib import Path


def test_credits_converter_can_be_imported():
    """Test that CreditsTableConverter can be imported and instantiated."""
    from data_converter.table_converters.credits_table_converter import CreditsTableConverter
    
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()
        
        converter = CreditsTableConverter(source_dir, target_dir)
        assert converter is not None


def test_help_converter_can_be_imported():
    """Test that HelpTableConverter can be imported and instantiated."""
    from data_converter.table_converters.help_table_converter import HelpTableConverter
    
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()
        
        converter = HelpTableConverter(source_dir, target_dir)
        assert converter is not None


def test_tips_converter_can_be_imported():
    """Test that TipsTableConverter can be imported and instantiated."""
    from data_converter.table_converters.tips_table_converter import TipsTableConverter
    
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()
        
        converter = TipsTableConverter(source_dir, target_dir)
        assert converter is not None


def test_text_converters_have_table_types():
    """Test that text converters have valid table types."""
    from data_converter.table_converters.credits_table_converter import CreditsTableConverter
    from data_converter.table_converters.help_table_converter import HelpTableConverter
    from data_converter.table_converters.tips_table_converter import TipsTableConverter
    
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()
        
        credits_converter = CreditsTableConverter(source_dir, target_dir)
        help_converter = HelpTableConverter(source_dir, target_dir)
        tips_converter = TipsTableConverter(source_dir, target_dir)
        
        credits_type = credits_converter.get_table_type()
        help_type = help_converter.get_table_type()
        tips_type = tips_converter.get_table_type()
        
        assert credits_type is not None
        assert help_type is not None
        assert tips_type is not None
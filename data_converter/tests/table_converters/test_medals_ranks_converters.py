from data_converter.table_converters.medals_table_converter import MedalsTableConverter
from data_converter.table_converters.rank_table_converter import RankTableConverter


def test_medals_converter_can_parse_content():
    """Test that medals converter can parse table content"""
    with open("source_assets/wcs_hermes_campaign/hermes_core/medals.tbl", "r") as f:
        content = f.read()

    converter = MedalsTableConverter("/tmp", "/tmp")
    state = converter._prepare_parse_state(content, "medals.tbl")

    entries = converter.parse_table(state)

    assert len(entries) > 0, "Should parse at least one medal entry"
    assert "name" in entries[0], "First medal should have a name"
    assert "bitmap" in entries[0], "First medal should have a bitmap"


def test_medals_converter_converts_to_godot_resource():
    """Test that medals converter can convert to Godot resource format"""
    with open("source_assets/wcs_hermes_campaign/hermes_core/medals.tbl", "r") as f:
        content = f.read()

    converter = MedalsTableConverter("/tmp", "/tmp")
    state = converter._prepare_parse_state(content, "medals.tbl")
    entries = converter.parse_table(state)

    godot_resource = converter.convert_to_godot_resource(entries)

    assert "medals" in godot_resource
    assert len(godot_resource["medals"]) > 0, "Should convert to medal resources"
    assert "medal_count" in godot_resource


def test_rank_converter_can_parse_content():
    """Test that rank converter can parse table content"""
    with open("source_assets/wcs_hermes_campaign/hermes_core/rank.tbl", "r") as f:
        content = f.read()

    converter = RankTableConverter("/tmp", "/tmp")
    state = converter._prepare_parse_state(content, "rank.tbl")

    entries = converter.parse_table(state)

    assert len(entries) > 0, "Should parse at least one rank entry"
    assert "name" in entries[0], "First rank should have a name"
    assert "points" in entries[0], "First rank should have points"


def test_rank_converter_converts_to_godot_resource():
    """Test that rank converter can convert to Godot resource format"""
    with open("source_assets/wcs_hermes_campaign/hermes_core/rank.tbl", "r") as f:
        content = f.read()

    converter = RankTableConverter("/tmp", "/tmp")
    state = converter._prepare_parse_state(content, "rank.tbl")
    entries = converter.parse_table(state)

    godot_resource = converter.convert_to_godot_resource(entries)

    assert "ranks" in godot_resource
    assert len(godot_resource["ranks"]) > 0, "Should convert to rank resources"
    assert "rank_count" in godot_resource

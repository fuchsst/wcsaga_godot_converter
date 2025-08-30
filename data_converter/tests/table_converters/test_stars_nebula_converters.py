from data_converter.table_converters.stars_table_converter import StarsTableConverter
from data_converter.table_converters.nebula_table_converter import NebulaTableConverter


def test_stars_converter_can_parse_content():
    """Test that stars converter can parse table content"""
    with open("source_assets/wcs_hermes_campaign/hermes_core/stars.tbl", "r") as f:
        content = f.read()

    converter = StarsTableConverter("/tmp", "/tmp")
    state = converter._prepare_parse_state(content, "stars.tbl")

    entries = converter.parse_table(state)

    assert len(entries) > 0, "Should parse at least one entry"

    # Count different types
    bitmaps = [e for e in entries if e.get("type") == "background"]
    suns = [e for e in entries if "sunglow" in e]

    assert len(bitmaps) > 0 or len(suns) > 0, "Should find either bitmaps or suns"


def test_stars_converter_converts_to_godot_resource():
    """Test that stars converter can convert to Godot resource format"""
    with open("source_assets/wcs_hermes_campaign/hermes_core/stars.tbl", "r") as f:
        content = f.read()

    converter = StarsTableConverter("/tmp", "/tmp")
    state = converter._prepare_parse_state(content, "stars.tbl")
    entries = converter.parse_table(state)

    godot_resource = converter.convert_to_godot_resource(entries)

    assert "bitmaps" in godot_resource or "suns" in godot_resource


def test_nebula_converter_can_parse_content():
    """Test that nebula converter can parse table content"""
    with open("source_assets/wcs_hermes_campaign/hermes_core/nebula.tbl", "r") as f:
        content = f.read()

    converter = NebulaTableConverter("/tmp", "/tmp")
    state = converter._prepare_parse_state(content, "nebula.tbl")

    entries = converter.parse_table(state)

    assert len(entries) > 0, "Should parse at least one entry"

    # Count different types
    nebula_bg = [e for e in entries if e.get("type") == "nebula_background"]
    poof_clouds = [e for e in entries if e.get("type") == "poof_cloud"]

    assert (
        len(nebula_bg) > 0 or len(poof_clouds) > 0
    ), "Should find either nebula backgrounds or poof clouds"


def test_nebula_converter_converts_to_godot_resource():
    """Test that nebula converter can convert to Godot resource format"""
    with open("source_assets/wcs_hermes_campaign/hermes_core/nebula.tbl", "r") as f:
        content = f.read()

    converter = NebulaTableConverter("/tmp", "/tmp")
    state = converter._prepare_parse_state(content, "nebula.tbl")
    entries = converter.parse_table(state)

    godot_resource = converter.convert_to_godot_resource(entries)

    assert "nebula_backgrounds" in godot_resource or "poof_clouds" in godot_resource

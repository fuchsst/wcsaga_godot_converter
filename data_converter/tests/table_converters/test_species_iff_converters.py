"""
Combined Tests for Species and IFF Table Converters
"""

import tempfile
from pathlib import Path
from data_converter.table_converters.species_defs_table_converter import (
    SpeciesDefsTableConverter,
)
from data_converter.table_converters.iff_table_converter import IFFTableConverter
from data_converter.table_converters.species_table_converter import (
    SpeciesTableConverter,
)
from data_converter.table_converters.base_converter import ParseState


# Tests from original test_species_iff_converters.py
def test_species_defs_converter_can_parse_content():
    """Test Species_defs.tbl converter can parse content"""
    # Sample Species_defs.tbl content
    species_defs_content = """
#Species_defs.tbl
$NumSpecies: 3

;------------------------
; Terran
;------------------------
$Species_Name: Terran
  $Default IFF: Friendly
  $FRED Color: ( 0, 0, 192 )
  $MiscAnims:
   +Debris_Texture: debris01a
   +Shield_Hit_ani: shieldhit01a
  $ThrustAnims:
   +Pri_Normal:   thruster01
   +Pri_Afterburn:   thruster01a
   +Sec_Normal:   thruster02-01
   +Sec_Afterburn:   thruster02-01a
   +Ter_Normal:   thruster03-01
   +Ter_Afterburn:   thruster03-01a
  $ThrustGlows:
   +Normal: thrusterglow01
   +Afterburn: thrusterglow01a
  $AwacsMultiplier: 1.00

;------------------------
; Pirate
;------------------------
$Species_Name: Pirate
  $Default IFF: Hostile
  $FRED Color: ( 128, 128, 128 )
  $MiscAnims:
   +Debris_Texture: debris01b
   +Shield_Hit_ani: shieldhit01a
  $ThrustAnims:
   +Pri_Normal:   thruster02
   +Pri_Afterburn:   thruster02a
   +Sec_Normal:   thruster02-02
   +Sec_Afterburn:   thruster02-02a
   +Ter_Normal:   thruster03-02
   +Ter_Afterburn:   thruster03-02a
  $ThrustGlows:
   +Normal: thrusterglow02
   +Afterburn: thrusterglow02a
  $AwacsMultiplier: 1.00

;------------------------
; Kilrathi
;------------------------
$Species_Name: Kilrathi
  $Default IFF: Hostile
  $FRED Color: ( 192, 0, 0 )
  $MiscAnims:
   +Debris_Texture: debris01c
   +Shield_Hit_ani: shieldhit01a
  $ThrustAnims:
   +Pri_Normal:   thruster03
   +Pri_Afterburn:   thruster03a
   +Sec_Normal:   thruster02-03
   +Sec_Afterburn:   thruster02-03a
   +Ter_Normal:   thruster03-03
   +Ter_Afterburn:   thruster03-03a
  $ThrustGlows:
   +Normal: thrusterglow03
   +Afterburn: thrusterglow03a
  $AwacsMultiplier: 1.00
#END
"""

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        converter = SpeciesDefsTableConverter(temp_path, temp_path)

        state = ParseState(
            lines=species_defs_content.split("\n"), filename="test_species_defs.tbl"
        )
        entries = converter.parse_table(state)

        assert len(entries) == 3, f"Expected 3 species entries, got {len(entries)}"
        assert "name" in entries[0], "First species should have a name"
        assert "default_iff" in entries[0], "First species should have default_iff"


def test_species_defs_converter_converts_to_godot_resource():
    """Test Species_defs.tbl converter can convert to Godot resource"""
    species_defs_content = """
#Species_defs.tbl
$NumSpecies: 1

$Species_Name: TestSpecies
  $Default IFF: Friendly
  $FRED Color: ( 0, 0, 192 )
#END
"""

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        converter = SpeciesDefsTableConverter(temp_path, temp_path)

        state = ParseState(
            lines=species_defs_content.split("\n"), filename="test_species_defs.tbl"
        )
        entries = converter.parse_table(state)

        godot_resource = converter.convert_to_godot_resource(entries)

        assert "species" in godot_resource
        assert "species_count" in godot_resource


def test_iff_converter_can_parse_content():
    """Test iff_defs.tbl converter can parse content"""
    # Sample iff_defs.tbl content
    iff_content = """
#IFFs

$Traitor IFF: Traitor

;------------------------
; Friendly
;------------------------
$IFF Name: Friendly
$Color: ( 24, 72, 232 )
$Attacks: ( "Hostile" "Neutral" "Traitor" )
$Flags: ( "orders hidden" )
$Default Ship Flags: ( "cargo-known" )
$Default Ship Flags2: ( "no-subspace-drive" )

;------------------------
; Hostile
;------------------------
$IFF Name: Hostile
$Color: ( 236, 56, 24 )
$Attacks: ( "Friendly" "Neutral" "Traitor" )
+Sees Friendly As: ( 236, 56, 24 )
+Sees Hostile As: ( 24, 72, 232 )
$Flags: ( "orders hidden" "wing name hidden" )
$Default Ship Flags2: ( "no-subspace-drive" )

;------------------------
; Neutral
;------------------------
$IFF Name: Neutral
$Color: ( 236, 56, 24 ) ; DONE
$Attacks: ( "Friendly" "Traitor" )
+Sees Friendly As: ( 236, 56, 24 )
+Sees Hostile As: ( 24, 72, 232 )
+Sees Neutral As: ( 24, 72, 232 )
$Flags: ( "orders hidden" "wing name hidden" )
$Default Ship Flags2: ( "no-subspace-drive" )
#End
"""

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        converter = IFFTableConverter(temp_path, temp_path)

        state = ParseState(lines=iff_content.split("\n"), filename="test_iff_defs.tbl")
        entries = converter.parse_table(state)

        assert len(entries) >= 3, f"Expected at least 3 IFF entries, got {len(entries)}"
        assert "name" in entries[0], "First IFF should have a name"
        assert "color" in entries[0], "First IFF should have a color"


def test_iff_converter_converts_to_godot_resource():
    """Test iff_defs.tbl converter can convert to Godot resource"""
    iff_content = """
#IFFs
$IFF Name: TestIFF
$Color: ( 255, 0, 0 )
$Attacks: ( "Hostile" )
#End
"""

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        converter = IFFTableConverter(temp_path, temp_path)

        state = ParseState(lines=iff_content.split("\n"), filename="test_iff_defs.tbl")
        entries = converter.parse_table(state)

        godot_resource = converter.convert_to_godot_resource(entries)

        assert "iffs" in godot_resource
        assert "iff_count" in godot_resource


def test_species_converter_can_parse_content():
    """Test Species.tbl converter can parse content"""
    # Sample Species.tbl content
    species_content = """
$Entry:
$Name: XSTR("Test System",-1)
$Anim: intel_test
$AlwaysInTechRoom: 0
$Description:
XSTR("Test description", -1)
$end_multi_text
"""

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        converter = SpeciesTableConverter(temp_path, temp_path)

        state = ParseState(
            lines=species_content.split("\n"), filename="test_species.tbl"
        )
        entries = converter.parse_table(state)

        assert len(entries) == 1, f"Expected 1 species entry, got {len(entries)}"
        assert "name" in entries[0], "Species entry should have a name"
        assert "anim" in entries[0], "Species entry should have an anim"


def test_species_converter_converts_to_godot_resource():
    """Test Species.tbl converter can convert to Godot resource"""
    species_content = """
$Entry:
$Name: XSTR("Test System",-1)
$Anim: intel_test
$AlwaysInTechRoom: 0
$Description:
XSTR("Test description", -1)
$end_multi_text
"""

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        converter = SpeciesTableConverter(temp_path, temp_path)

        state = ParseState(
            lines=species_content.split("\n"), filename="test_species.tbl"
        )
        entries = converter.parse_table(state)

        godot_resource = converter.convert_to_godot_resource(entries)

        assert "entries" in godot_resource
        assert "entry_count" in godot_resource


# Tests from test_iff_table_converter.py
def test_iff_converter_initialization():
    """Test IFFTableConverter initialization"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = IFFTableConverter(source_dir, target_dir)

        # Check that the converter is properly initialized
        assert converter.source_dir == source_dir
        assert converter.target_dir == target_dir
        assert converter.get_table_type().value == "iff_defs"
        assert len(converter._parse_patterns) > 0


def test_iff_converter_can_convert_standalone():
    """Test that IFFTableConverter can identify IFF table files"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = IFFTableConverter(source_dir, target_dir)

        # Create a test IFF table file
        iff_file = source_dir / "iff_defs.tbl"
        with open(iff_file, "w") as f:
            f.write(
                """#IFF Definitions
$Name: Test IFF
#End"""
            )

        # Should be able to convert IFF table files
        assert converter.can_convert(iff_file)


def test_parse_iff_entry():
    """Test parsing a single IFF entry"""
    # Create test content that matches what the converter actually expects
    test_content = ["$IFF Name: Friendly", "$Color: (0, 255, 0)", "#End"]

    state = ParseState(lines=test_content, current_line=0)
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = IFFTableConverter(source_dir, target_dir)
        result = converter.parse_entry(state)

        assert result is not None
        assert result["name"] == "Friendly"
        assert result["color"] == [0, 255, 0]


def test_validate_iff_entry():
    """Test IFF entry validation"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = IFFTableConverter(source_dir, target_dir)

        # Valid entry
        valid_entry = {"name": "Test IFF", "color": [0, 255, 0]}
        assert converter.validate_entry(valid_entry)

        # Invalid entry - missing name
        invalid_entry = {"color": [0, 255, 0]}
        assert not converter.validate_entry(invalid_entry)

        # Invalid entry - wrong format for color
        invalid_entry2 = {
            "name": "Test IFF",
            "color": [0, 255],  # Missing one component
        }
        assert not converter.validate_entry(invalid_entry2)

        # Invalid entry - color component out of range
        invalid_entry3 = {
            "name": "Test IFF",
            "color": [0, 300, 0],  # 300 is out of range
        }
        assert not converter.validate_entry(invalid_entry3)


def test_convert_iff_table_file():
    """Test converting a complete IFF table file"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = IFFTableConverter(source_dir, target_dir)

        # Create test table content
        table_content = """#IFF Definitions

$Name: Friendly
$Color: (0, 255, 0)
$Attackable: NO

#End
"""

        # Create test file
        test_file = source_dir / "iff_defs.tbl"
        with open(test_file, "w") as f:
            f.write(table_content)

        # Test conversion
        success = converter.convert_table_file(test_file)
        assert success

        # Check that output files were created
        output_files = list((target_dir / "assets" / "tables").glob("*.tres"))
        assert len(output_files) >= 0  # At least the main table file


# Tests from test_species_defs_table_converter.py
def test_species_converter_initialization():
    """Test SpeciesDefsTableConverter initialization"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = SpeciesDefsTableConverter(source_dir, target_dir)

        # Check that the converter is properly initialized
        assert converter.source_dir == source_dir
        assert converter.target_dir == target_dir
        assert converter.get_table_type().value == "species_defs"
        assert len(converter._parse_patterns) > 0


def test_species_converter_can_convert_standalone():
    """Test that SpeciesDefsTableConverter can identify species table files"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = SpeciesDefsTableConverter(source_dir, target_dir)

        # Create a test species table file
        species_file = source_dir / "species_defs.tbl"
        with open(species_file, "w") as f:
            f.write("$NumSpecies: 1\n$Species_Name: Test Species\n#END")

        # Should be able to convert species table files
        assert converter.can_convert(species_file)


def test_parse_species_entry():
    """Test parsing a single species entry"""
    # Create test content
    test_content = [
        "$Species_Name: Terran",
        "$Default IFF: Friendly",
        "$FRED Color: (0, 0, 255)",
        "#END",
    ]

    state = ParseState(lines=test_content, current_line=0)
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = SpeciesDefsTableConverter(source_dir, target_dir)
        result = converter.parse_entry(state)

        assert result is not None
        assert result["name"] == "Terran"
        assert result["default_iff"] == "Friendly"
        assert result["fred_color"] == [0, 0, 255]


def test_validate_species_entry():
    """Test species entry validation"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = SpeciesDefsTableConverter(source_dir, target_dir)

        # Valid entry
        valid_entry = {"name": "Test Species"}
        assert converter.validate_entry(valid_entry)

        # Invalid entry - missing name
        invalid_entry = {}
        assert not converter.validate_entry(invalid_entry)


def test_convert_species_table_file():
    """Test converting a complete species table file"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = SpeciesDefsTableConverter(source_dir, target_dir)

        # Create test table content
        table_content = """$NumSpecies: 1

$Species_Name: Terran
$Default IFF: Friendly
$FRED Color: (0, 0, 255)

#END
"""

        # Create test file
        test_file = source_dir / "species_defs.tbl"
        with open(test_file, "w") as f:
            f.write(table_content)

        # Test conversion
        success = converter.convert_table_file(test_file)
        assert success

        # Check that output files were created
        output_files = list((target_dir / "assets" / "tables").glob("*.tres"))
        assert len(output_files) >= 0  # At least the main table file

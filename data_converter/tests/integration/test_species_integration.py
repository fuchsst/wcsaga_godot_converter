#!/usr/bin/env python3
"""
Integration test for Species Resource Generator with existing conversion system
"""

import tempfile
import json
from pathlib import Path

from data_converter.resource_generators.species_resource_generator import SpeciesResourceGenerator
from data_converter.table_converters.species_defs_table_converter import SpeciesDefsTableConverter
from data_converter.core.table_data_structures import TableType


def main():
    """Test the integration between species table converter and resource generator"""
    # Create sample species data that matches the format from Species_defs.tbl
    sample_species_content = """#SPECIES DEFS                                   

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

;------------------------                          
; Vasudan                                     
;------------------------                          
$Species_Name: Vasudan                     
  $Default IFF: Neutral                     
  $FRED Color: ( 0, 192, 0 )                 
  $MiscAnims:                             
   +Debris_Texture: debris01b             
   +Shield_Hit_ani: shieldhit01b          
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

#END
"""

    # Create mock objects for the required parameters
    class MockAssetCatalog:
        def get_asset(self, asset_id):
            return None

        def register_asset(self, asset_data):
            pass

    class MockRelationshipBuilder:
        def add_relationship(self, source_id, target_id, relationship_type, strength=1.0, metadata=None):
            pass

    # Create a temporary directory for output
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()
        
        # Create sample species file
        species_file = source_dir / "Species_defs.tbl"
        with open(species_file, 'w') as f:
            f.write(sample_species_content)
        
        # Parse species data using the table converter
        print("Parsing species data with table converter...")
        converter = SpeciesDefsTableConverter(source_dir, target_dir)
        
        # Read and parse the table file
        with open(species_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Create parse state
        lines = content.splitlines()
        from data_converter.table_converters.base_converter import ParseState
        state = ParseState(lines)
        
        # Parse the table
        entries = converter.parse_table(state)
        print(f"Parsed {len(entries)} species entries:")
        for entry in entries:
            print(f"  - {entry.get('name', 'Unknown')}")
        
        # Validate entries
        valid_entries = [entry for entry in entries if converter.validate_entry(entry)]
        print(f"Valid entries: {len(valid_entries)}")
        
        # Convert to Godot resource format using the table converter
        godot_resource = converter.convert_to_godot_resource(valid_entries)
        print(f"Converted to Godot resource with {len(godot_resource.get('species', {}))} species")
        
        # Now use the species resource generator to create individual .tres files
        print("\nGenerating individual species resource files...")
        generator = SpeciesResourceGenerator(
            MockAssetCatalog(), MockRelationshipBuilder(), target_dir
        )
        
        # Generate species resources
        result_files = generator.generate_species_resources(valid_entries)
        
        # Print results
        print(f"Generated {len(result_files)} files:")
        for name, path in result_files.items():
            print(f"  {name}: {path}")
            
        # Show content of one of the generated files
        if result_files:
            terran_file = target_dir / "assets" / "data" / "species" / "terran.tres"
            if terran_file.exists():
                print(f"\nContent of {terran_file}:")
                with open(terran_file, 'r') as f:
                    print(f.read())


if __name__ == "__main__":
    main()
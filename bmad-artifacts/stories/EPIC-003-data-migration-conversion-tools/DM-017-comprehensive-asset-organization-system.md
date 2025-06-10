# DM-017: Comprehensive WCS Asset Organization System Based on Campaign Analysis

**Story Manager**: SallySM  
**Date**: 2025-06-10  
**Epic**: EPIC-003 Data Migration & Conversion Tools  
**Priority**: High  
**Estimated Effort**: 5 days (Complex - comprehensive semantic analysis implementation)

## Story

**As a** Conversion Manager  
**I want** a comprehensive asset organization system that leverages the complete WCS Hermes campaign analysis  
**So that** assets are properly organized according to their semantic relationships, faction affiliations, functional purposes, and contextual usage patterns discovered through exhaustive table file analysis.

## Background

Comprehensive analysis of the WCS Hermes campaign has revealed sophisticated asset organization patterns that go far beyond simple file-type grouping. The analysis of 36 different table files, extensive audio collections, model hierarchies, and texture relationships shows WCS uses a semantic organization system based on:

### Key Discoveries from TBL Analysis:

1. **Faction-Based Organization**: Ships, weapons, and assets are clearly organized by faction prefixes:
   - `tcf_` (Terran Confederation Fighters): hellcat_v, rapier, excalibur, arrow, ferret
   - `tcb_` (Terran Confederation Bombers): longbow, sabre, thunderbolt_vii  
   - `tcs_` (Terran Confederation Ships): artemis, caernaven, lexington, prowler
   - `tcm_` (Terran Confederation Missiles): dart, javelin, lance, pilum, warhammer
   - `kif_` (Kilrathi Fighters): dralthi_mk_iv, bloodfang, darket, ekapshi, gothri
   - `kib_` (Kilrathi Bombers): paktahn
   - `kis_` (Kilrathi Ships): fralthi_ii, zakhari, dubav
   - `kim_` (Kilrathi Missiles): claw, fang, skipper, stalker

2. **Asset Relationships from Tables**:
   - **ships.tbl**: Links ships to POF models, weapon compatibility, engine sounds, death animations
   - **weapons.tbl**: Connects weapons to bitmap glows, laser colors, impact sounds, launch sounds
   - **sounds.tbl**: Categorizes 130+ audio files by function (engine, weapon fire, UI feedback, shield impacts)
   - **music.tbl**: Organizes adaptive music by mission context (ambient, battle, victory, goal_failed)
   - **fireball.tbl**: Links explosion effects to appropriate ship classes
   - **iff_defs.tbl**: Defines faction colors and combat relationships

3. **Audio Organization Patterns**:
   - **Mission-specific voice lines**: `01_greywolf_01.wav` through `11_little_john_12.wav` (pilot callsigns by mission)
   - **Control tower communications**: `hermes_control_01.wav`, `bradshaw_control_01.wav` (by location)
   - **Functional audio grouping**: engine sounds, weapon fire, shield impacts, UI feedback
   - **Adaptive music system**: ambient, battle phases, victory/defeat states

4. **Texture Material Relationships**:
   - **Surface types**: `-normal.dds`, `-shine.dds`, `-glow.dds` material maps
   - **Animation sequences**: `fire_0000.dds` through `fire_0149.dds` (150-frame fire effect, should have a coresponding eff file)
   - **Faction-specific textures**: `confed_details_1.dds`, `kb_drydock_1.dds`

5. **Model Hierarchy Patterns**:
   - **Size classifications**: fighter, bomber, capital ship, installation
   - **Variant tracking**: `_a`, `_c`, `_d`, `_i` suffixes for ship variants
   - **Damage states**: separate models for pristine/damaged versions

## Acceptance Criteria

### AC1: Faction-Based Asset Organization
**Given** the WCS asset relationship mapper is enhanced with faction detection  
**When** I process ship, weapon, and related assets  
**Then** assets are organized into proper faction subdirectories (terran/, kilrathi/, etc.) following the discovered naming conventions  
**And** faction classification achieves >98% accuracy based on prefix patterns  
**And** cross-faction relationships (shared technologies) are properly tracked

### AC2: Semantic Asset Grouping by Function
**Given** table file analysis reveals functional asset relationships  
**When** I organize assets according to their semantic purpose  
**Then** related assets are grouped together:
- Ships with their compatible weapons, textures, sounds, and effects
- Weapons with their bitmap glows, impact effects, and launch sounds  
- Audio files categorized by type (voice/pilot_communications, sfx/weapons, sfx/engines, music/adaptive)
- Effect sequences with their complete frame collections
- Materials with their complete texture maps (diffuse, normal, specular, glow)

### AC3: Mission-Contextual Organization  
**Given** mission files and voice line analysis show contextual relationships  
**When** I organize mission-specific assets  
**Then** assets are grouped by mission context:
- Mission-specific pilot voice lines grouped by mission number (`01_`, `02_`, etc.)
- Location-specific control tower communications grouped by station/ship
- Mission-specific music tracks linked to gameplay states
- Briefing materials and mission objectives co-located

### AC4: Material and Effect Completeness Validation
**Given** the comprehensive texture and effect analysis  
**When** I validate asset relationships  
**Then** complete material sets are identified and validated:
- Multi-frame animation sequences are kept together (fire effects: 150 frames)
- Material map completeness (diffuse + normal + specular + glow) is verified
- Missing assets in sequences are flagged for attention
- Broken references between ships.tbl POF files and actual models are reported

### AC5: Adaptive Music System Organization
**Given** music.tbl defines complex adaptive music relationships  
**When** I organize music assets  
**Then** adaptive music systems are properly structured:
- Music tracks grouped by soundtrack name (Oberan, Brimstone, etc.)
- Battle progression tracks (ambient → battle1 → battle2 → battle3) linked
- Context-specific tracks (allied_arrival, enemy_arrival, victory, goal_failed) associated
- Player state music (player_dead) properly categorized

### AC6: Enhanced Asset Discovery and Validation
**Given** the comprehensive campaign analysis  
**When** I run asset discovery and validation  
**Then** the system provides comprehensive insights:
- Asset coverage report showing discovered vs. missing assets per entity
- Broken reference detection between table files and actual assets
- Completeness scoring for material sets and effect sequences  
- Faction distribution analytics and cross-faction asset sharing analysis
- Audio categorization accuracy metrics (voice vs. SFX vs. music)

## Technical Implementation

### Enhanced Asset Discovery Engine
```python
class ComprehensiveAssetDiscoveryEngine:
    def __init__(self, source_dir: Path):
        self.faction_patterns = {
            'terran': ['tcf_', 'tcb_', 'tcs_', 'tcm_', 'tb_'],
            'kilrathi': ['kif_', 'kib_', 'kis_', 'kim_', 'kb_'],
            'pirate': ['prf_', 'prs_'],
        }
        self.audio_categories = {
            'pilot_voice': ['_greywolf_', '_kettle_', '_sandman_', '_phalanx_'],
            'control_tower': ['_control_', '_command_'],
            'engine_sounds': ['engine_', 'aburn_', 'throttle_'],
            'weapon_sounds': ['missile_', 'laser_', 'ion_'],
            'ui_feedback': ['button_', 'menu_', 'alert_'],
        }
        
    def discover_semantic_relationships(self, entity_name: str) -> SemanticAssetGroup:
        """Discover assets using semantic analysis of table relationships"""
        
    def validate_material_completeness(self, base_texture: str) -> MaterialCompletenessReport:
        """Validate that material maps form complete sets"""
        
    def analyze_faction_distribution(self) -> FactionAnalysisReport:
        """Analyze asset distribution across factions and detect sharing patterns"""
```

### Enhanced Target Path Resolution
```python
class SemanticPathResolver:
    def resolve_faction_path(self, entity_name: str, asset_type: str) -> str:
        """Generate faction-organized paths based on semantic analysis"""
        faction = self.detect_faction(entity_name)
        entity_class = self.classify_entity_type(entity_name)
        
        if asset_type == 'model':
            return f"campaigns/wing_commander_saga/ships/{faction}/{entity_class}/{entity_name}/{entity_name}.glb"
        elif asset_type == 'texture':
            material_type = self.detect_material_type(asset_name)
            return f"campaigns/wing_commander_saga/ships/{faction}/{entity_class}/{entity_name}/textures/{material_type}_{asset_name}.png"
        elif asset_type == 'audio':
            audio_category = self.classify_audio_type(asset_name)
            if audio_category == 'pilot_voice':
                mission_num = self.extract_mission_number(asset_name)
                return f"campaigns/wing_commander_saga/audio/voice/mission_{mission_num:02d}/{asset_name}.ogg"
            elif audio_category == 'weapon_sound':
                return f"campaigns/wing_commander_saga/ships/{faction}/{entity_class}/{entity_name}/audio/{asset_name}.ogg"
```

## Dependencies

- **DM-013**: Automated Asset Mapping (COMPLETED) - Provides foundation asset relationship data
- **DM-015**: Hermes Campaign Conversion (COMPLETED) - Provides comprehensive campaign analysis
- **Enhanced AssetRelationshipMapper**: Foundation component from previous stories

## Definition of Done

- [ ] Faction-based asset organization implemented with >98% classification accuracy
- [ ] Semantic asset grouping functional for ships, weapons, audio, and effects  
- [ ] Mission-contextual organization working for voice lines and music
- [ ] Material completeness validation detecting incomplete texture sets
- [ ] Adaptive music system organization preserving gameplay state relationships
- [ ] Enhanced asset discovery providing comprehensive coverage and validation reports
- [ ] Comprehensive test suite covering all semantic analysis features
- [ ] Integration with existing conversion pipeline maintained
- [ ] Performance testing showing processing time improvements through better organization
- [ ] Documentation updated with semantic organization patterns and usage examples

## Notes

This story represents a significant evolution from basic file-type organization to sophisticated semantic understanding of WCS assets. The comprehensive table file analysis has revealed that WCS uses a sophisticated asset organization system based on semantic relationships, faction affiliations, and functional purposes that goes far beyond simple file extensions.

The implementation will transform asset organization from:
```
common/misc/tcf_hellcat_v.pof
common/misc/tcf_hellcat_v_diffuse.dds  
common/misc/laser_fire_sound.wav
```

To semantic organization:
```
campaigns/wing_commander_saga/ships/terran/fighters/hellcat_v/hellcat_v.glb
campaigns/wing_commander_saga/ships/terran/fighters/hellcat_v/textures/diffuse_hellcat_v.png
campaigns/wing_commander_saga/ships/terran/fighters/hellcat_v/audio/laser_fire.ogg
campaigns/wing_commander_saga/audio/voice/mission_01/01_greywolf_01.ogg
campaigns/wing_commander_saga/audio/music/adaptive/oberan_battle1.ogg
```

This semantic organization will dramatically improve:
- **Developer Experience**: Assets are logically grouped and easily discoverable
- **Conversion Accuracy**: Proper relationships preserved from original WCS structure  
- **Maintenance**: Changes to faction ships only affect that faction's asset tree
- **Validation**: Missing assets and broken references easily identified
- **Performance**: Reduced search time through logical organization hierarchy

The story leverages the comprehensive analysis of the WCS Hermes campaign to create an asset organization system that respects and preserves the sophisticated design patterns used in the original game.
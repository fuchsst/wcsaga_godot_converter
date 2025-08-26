# Data Converter Concepts

## Overview
This directory contains detailed specifications for converting Wing Commander Saga assets from their original formats to Godot-compatible formats. The documents describe the requirements and processes for converting each asset type, following Godot's feature-based organization principles as defined in `directory_structure.md` and `Godot_Project_Structure_Refinement.md`.

## Asset Type Specifications
Individual documents for each asset type conversion following the target structure:

- [TBL Files](tbl_files.md) - Table data files containing game definitions (ships.tbl, weapons.tbl, ai_profiles.tbl, etc.)
- [TXT Files](txt_files.md) - Narrative fiction and technical database text files (d1fiction.txt, m1fiction.txt, etc.)

## Conversion Process
Documents covering the overall conversion approach aligned with the target directory structure:

## Conversion Pipeline

The asset conversion follows a dependency-ordered pipeline aligned with the Godot project structure:

1. **Data Extraction** - Parse original file formats
   - Table files (.tbl) for game definitions
   - Text files (.txt) for narrative content
   - Configuration files for system parameters

2. **Format Conversion** - Convert to Godot-compatible formats following the directory structure:
   - Tables → Godot Resource files (.tres) organized in `/assets/data/` by type
   - Fiction text → BBCode formatted text resources organized in `/campaigns/{campaign}/fiction/`
   - Technical database → Structured text resources organized in `/features/ui/tech_database/`
   - Configuration data → Godot Resource files (.tres) in appropriate `/assets/data/` subdirectories

3. **Asset Organization** - Place converted assets according to the target directory structure:

   ### Assets Directory Structure (`/assets/`)
   Contains truly global, shared assets following the "Global Litmus Test":
   - `/assets/audio/` - Shared audio files organized by type
     - `/assets/audio/sfx/` - Sound effects
     - `/assets/audio/music/` - Background music tracks
     - `/assets/audio/voice/` - Voice acting files
     - `/assets/audio/ui/` - UI sound effects
   - `/assets/data/` - Shared data resources organized by category
     - `/assets/data/ai/` - AI behavior data and profiles
     - `/assets/data/ships/` - Ship data resources
     - `/assets/data/weapons/` - Weapon data resources
     - `/assets/data/species/` - Species definitions and properties
     - `/assets/data/iff/` - IFF (Identification Friend or Foe) relationships
     - `/assets/data/armor/` - Armor type definitions and damage modifiers
     - `/assets/data/effects/` - Effect data resources
   - `/assets/textures/` - Shared texture files
     - `/assets/textures/ui/` - Generic UI elements
     - `/assets/textures/effects/` - Particle textures used by multiple effects
     - `/assets/textures/fonts/` - Font textures
   - `/assets/animations/` - Shared animation files
     - `/assets/animations/ui/` - UI animations
     - `/assets/animations/effects/` - Generic effect animations

   ### Features Directory Structure (`/features/`)
   Contains self-contained game features organized by category following the co-location principle:
   - `/features/fighters/` - Fighter ship entities with all related assets
     - Example: `/features/fighters/confed_arrow/` contains `arrow.tscn`, `arrow.gd`, `arrow.tres`, etc.
   - `/features/capital_ships/` - Capital ship entities
   - `/features/weapons/` - Weapon entities
   - `/features/effects/` - Effect entities
   - `/features/environment/` - Environmental entities
   - `/features/ui/` - UI feature elements with self-contained components:
     - `/features/ui/briefing/` - Briefing interface
     - `/features/ui/debriefing/` - Debriefing interface
     - `/features/ui/tech_database/` - Technical database
     - `/features/ui/main_menu/` - Main menu interface
     - `/features/ui/hud/` - Heads-up display
     - `/features/ui/options/` - Options menu
   - `/features/templates/` - Feature templates for new entity creation

   ### Campaigns Directory Structure (`/campaigns/`)
   Contains campaign-specific content following the campaign-centric mission organization:
   - `/campaigns/hermes/` - Main Hermes campaign
     - `/campaigns/hermes/fiction/` - Campaign fiction organized by mission
     - `/campaigns/hermes/missions/` - Mission scenes with integrated data
   - `/campaigns/prologue/` - Prologue campaign (demo missions)
     - `/campaigns/prologue/fiction/` - Campaign fiction organized by disc
     - `/campaigns/prologue/missions/` - Mission scenes with integrated data
   - `/campaigns/brimstone/` - Brimstone campaign
   - `/campaigns/training/` - Training campaign

   ### Scripts Directory Structure (`/scripts/`)
   Contains reusable code and base classes following the separation of concerns principle:
   - `/scripts/entities/` - Base entity scripts
   - `/scripts/ai/` - AI behavior scripts
   - `/scripts/mission/` - Mission system scripts
   - `/scripts/physics/` - Physics system scripts
   - `/scripts/audio/` - Audio system scripts
   - `/scripts/utilities/` - Utility functions and helpers

   ### Autoload Directory Structure (`/autoload/`)
   Contains singleton scripts registered via Project Settings > AutoLoad:
   - `/autoload/game_state.gd` - Global game state management
   - `/autoload/event_bus.gd` - Global event system
   - `/autoload/audio_manager.gd` - Audio management system
   - `/autoload/resource_loader.gd` - Resource loading utilities

4. **Integration** - Combine assets into functional game elements following Godot's scene composition:
   - Assemble entity scenes in `/features/` directories with self-contained organization
   - Create mission scenes in `/campaigns/{campaign}/missions/` with integrated data
   - Build UI scenes in `/features/ui/` with reusable components
   - Integrate narrative content in `/campaigns/{campaign}/fiction/` with mission scenes

5. **Validation** - Verify quality and compatibility:
   - Check cross-references between assets using Godot's resource system
   - Validate scene loading and performance with Godot's profiler
   - Test gameplay functionality through automated test suites
   - Ensure cross-platform compatibility with export templates

## Asset Relationships

Assets in Wing Commander Saga have complex interdependencies that must be maintained during conversion, following the relationships defined in the asset mapping documents:

### Core Entity Relationships Following Asset Mappings
- **Ships** ←→ Weapons, Models, Textures, Sounds
  - Ship definitions (ships.tbl) reference weapon hardpoints and are mapped to `/assets/data/ships/`
  - Ship-specific assets are co-located in `/features/fighters/{faction}_{ship_name}/` or `/features/capital_ships/{faction}_{ship_name}/`
  - Ship entities integrate engine sounds organized in feature directories
  - Ship AI behaviors reference AI profiles from `/assets/data/ai/profiles/`

- **Weapons** ←→ Effects, Models, Sounds
  - Weapon definitions (weapons.tbl) reference projectile types and are mapped to `/assets/data/weapons/`
  - Weapon-specific assets are co-located in `/features/weapons/{weapon_name}/`
  - Weapon entities integrate firing sounds organized in feature directories
  - Weapon impacts reference explosion effects from `/assets/data/effects/`

- **Campaigns** ←→ Fiction, Missions, Briefings
  - Campaign fiction (d1fiction.txt, m1fiction.txt) is mapped to `/campaigns/{campaign}/fiction/` directories
  - Mission scenes integrate fiction content following campaign-centric organization
  - Briefing screens reference mission-specific text from campaign directories
  - Campaign progression data is stored in `/campaigns/{campaign}/campaign.tres`

- **AI Systems** ←→ Profiles, Behaviors, Sounds
  - AI profiles (ai_profiles.tbl) are mapped to `/assets/data/ai/profiles/`
  - Behavior trees are organized in `/assets/behavior_trees/ai/`
  - AI-specific sounds are organized in `/assets/audio/sfx/ai/` and `/assets/audio/voice/ai/`

- **Effects** ←→ Textures, Animations, Sounds
  - Effect definitions are mapped to `/assets/data/effects/`
  - Visual effects integrate particle textures from `/assets/textures/effects/`
  - Animated sequences use sprite sheets organized in `/assets/animations/effects/`
  - Effect sounds are organized in `/assets/audio/sfx/weapons/` and related directories

- **UI Elements** ←→ Graphics, Fonts, Animations, Text
  - UI components are organized in `/features/ui/{component_name}/` following co-location principle
  - Interface graphics are converted to WebP and organized in feature directories
  - Text displays use font resources from `/assets/textures/fonts/`
  - UI animations are organized in `/assets/animations/ui/` for shared elements

The conversion process maintains these relationships while adapting to Godot's resource system and scene composition, ensuring that:

1. **Related assets are grouped together** in self-contained directories following the "Organization by Feature" principle
2. **Shared assets are placed in global directories** following the "Global Litmus Test" principle
3. **The directory structure reflects gameplay and narrative relationships** as defined in the asset mapping documents
4. **Each feature can be developed, tested, and maintained in isolation** following modular design principles
5. **Cross-references are explicit and resilient** using Godot's resource system and export variables

This organization provides maintainability and modularity in the converted Godot project while preserving the relationships between assets from the original Wing Commander Saga, and aligns with the target directory structure defined in `directory_structure.md`.
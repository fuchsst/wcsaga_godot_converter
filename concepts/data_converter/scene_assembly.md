# Asset Integration and Scene Assembly

## Overview
This document explains how converted assets from different file types are integrated to create complete Godot scenes following the feature-based organization principles defined in directory_structure.md and Godot_Project_Structure_Refinement.md. The scene assembly process combines data from multiple sources to produce fully functional game elements in self-contained directories, following the hybrid model where truly global assets are organized in `/assets/` and feature-specific assets are co-located with their respective features in `/features/`.

## Scene Assembly Process

### 1. Ship Scenes
**Component Assets**:
- ShipClass resources (.tres) from `/features/fighters/{faction}_{ship_name}/{ship_name}.tres`
- 3D model (.glb) from `/features/fighters/{faction}_{ship_name}/{ship_name}.glb`
- Textures (.webp) from `/features/fighters/{faction}_{ship_name}/{ship_name}_diffuse.webp`
- Engine sounds (.ogg) from `/features/fighters/{faction}_{ship_name}/assets/sounds/engine_loop.ogg`
- Weapon hardpoint data from POF metadata
- AI profile resources from `/assets/data/ai/profiles/`

**Assembly Process**:
- Create root Ship node with ShipClass resource in entity scene following feature-based organization
- Import glTF model as child node from feature directory maintaining co-location principle
- Apply converted textures to model materials from feature directory
- Attach engine audio components to thruster positions from feature-specific audio directory
- Configure weapon hardpoints using POF metadata with hardpoint positions
- Set up subsystem positions for damage modeling with subsystem data from ShipClass
- Add physics properties from ShipClass data resource
- Link to AI behavior resources from global `/assets/data/ai/profiles/` directory (passes Global Litmus Test)

### 2. Weapon Scenes
**Component Assets**:
- WeaponClass resources (.tres) from `/features/weapons/{weapon_name}/{weapon_name}.tres`
- 3D model (.glb) from `/features/weapons/{weapon_name}/{weapon_name}.glb`
- Firing sounds (.ogg) from `/features/weapons/{weapon_name}/assets/sounds/fire_sound.ogg`
- Muzzle flash effects from `/features/effects/muzzle_flash/`
- Projectile trail textures from `/assets/textures/effects/particles/`
- Impact effects from `/features/weapons/_shared/impact_effects/`

**Assembly Process**:
- Create root Weapon node with WeaponClass resource in entity scene following feature-based organization
- Import glTF model for weapon visualization from feature directory maintaining co-location principle
- Attach firing sound components from feature-specific audio directory
- Configure muzzle flash particle effects from global effect directory
- Set up projectile properties from WeaponClass data resource
- Configure homing behavior for missile weapons with guidance parameters
- Link to impact effects and sounds from shared weapon assets and global audio directory

### 3. Mission Scenes
**Component Assets**:
- Mission resources (.tres) from `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/mission_data.tres`
- Ship instances referencing ship scenes from `/features/fighters/{faction}_{ship_name}/{ship_name}.tscn`
- Weapon instances referencing weapon scenes from `/features/weapons/{weapon_name}/{weapon_name}.tscn`
- Particle effects from `/features/effects/{effect_name}/{effect_name}.tscn` and `/assets/textures/effects/`
- Audio environments from `/assets/audio/music/ambient/`
- Briefing text from `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/briefing.txt`

**Assembly Process**:
- Create mission root node with mission data from campaign-centric mission directory following the principle that "this file defines 'what' happens in a mission, rather than 'how' a game mechanic works"
- Place initial ship entities using placement data with instance() calls
- Configure AI behaviors using mission scripting with LimboAI behavior trees from `/assets/behavior_trees/ai/`
- Set up event triggers and timeline using Godot's AnimationPlayer system with keyframe sequences
- Configure environmental audio and effects from global audio and feature effect directories
- Create objective tracking components from campaign mission data resources
- Link briefing UI to fiction text resources from campaign mission directory

### 4. Effect Scenes
**Component Assets**:
- Particle effect resources (.tres) from `/features/effects/{effect_name}/{effect_name}.tres`
- Animation textures from `/features/effects/{effect_name}/textures/`
- Audio effects from `/features/effects/{effect_name}/assets/sounds/`
- Shared particle textures from `/assets/textures/effects/particles/`
- Shader definitions for special effects from `/assets/shaders/effects/`

**Assembly Process**:
- Create effect root node with effect properties from feature directory following self-contained feature organization
- Configure particle systems with animation textures from feature-specific texture directory
- Attach audio components for sound effects from feature-specific audio directory
- Set up shader materials for visual effects from global shader directory (passes Global Litmus Test)
- Configure emission and timing properties with effect data resource
- Link to parent entities for positioning through instancing

### 5. UI Scenes
**Component Assets**:
- UI component definitions from `/features/ui/{component}/{component}.tres`
- Interface graphics from `/features/ui/{component}/assets/`
- Animation sequences from `/features/ui/{component}/animations/`
- Font resources from `/assets/textures/fonts/`
- Audio feedback from `/features/ui/{component}/assets/sounds/`
- Shared UI elements from `/features/ui/_shared/`

**Assembly Process**:
- Create UI root nodes with layout properties from feature directory following self-contained feature organization
- Apply converted graphics to interface elements from feature-specific asset directory
- Configure animation controllers for dynamic elements from feature-specific animation directory
- Set up text display with font resources from global font directory (passes Global Litmus Test)
- Attach audio components for UI feedback from feature-specific sound directory
- Configure input handling and navigation with exported variables for flexibility

## Feature-Based Asset Combination Strategies

### Self-Contained Entity Organization
Each entity in `/features/` contains all related assets following the co-location principle:
- Entity scenes reference resources from their own feature directory and global `/assets/` directories
- Visual assets are organized within the feature directory or in global `/assets/textures/` directories (following Global Litmus Test)
- Audio assets are organized within the feature directory or in global `/assets/audio/` directories (following Global Litmus Test)
- Animation assets are organized within the feature directory or in global `/assets/animations/` directories (following Global Litmus Test)
- Shared assets are placed in `/_shared/` directories within feature categories or in global `/assets/` directories

### Cross-Reference Management
- **Resource Preloading**: Load shared assets during initialization from global `/assets/` directories
- **Weak References**: Prevent circular dependencies using Godot's resource system with exported variables
- **Asset Bundles**: Group related assets in feature directories for efficient loading following feature-based organization
- **Dynamic Loading**: Load assets on-demand to reduce memory usage from feature directories with ResourceLoader
- **Reference Counting**: Automatically manage asset lifecycle through Godot's resource system

### Optimization Techniques
- **Level of Detail (LOD)**: Multiple detail versions of complex models in feature directories following self-contained feature organization
- **Occlusion Culling**: Hide off-screen assets to improve performance using Godot's visibility notifiers
- **Batching**: Combine similar objects for efficient rendering using Godot's MultiMeshInstance3D
- **Streaming**: Load assets progressively during gameplay from feature directories with background loading
- **Compression**: Reduce asset sizes while maintaining quality using WebP and Ogg Vorbis formats

## Feature-Based Directory Structure for Assembled Scenes
Following the exact directory structure defined in directory_structure.md:
```
wcsaga_godot/
├── addons/                # Third-party plugins and extensions
├── assets/                # Global asset library (truly shared assets)
│   ├── audio/             # Shared audio files
│   │   ├── sfx/           # Generic sound effects
│   │   ├── music/         # Background music tracks
│   │   └── ui/            # UI sound effects
│   ├── behavior_trees/    # Shared LimboAI behavior trees
│   │   ├── ai/            # AI behavior trees
│   │   │   ├── combat/    # Combat-related behavior trees
│   │   │   ├── navigation/ # Navigation behavior trees
│   │   │   └── tactical/  # Tactical behavior trees
│   │   └── mission/       # Mission-specific behavior trees
│   ├── data/              # Shared data resources
│   │   ├── ai/            # AI data resources
│   │   │   └── profiles/  # AI profile definitions
│   │   └── mission/       # Mission data resources
│   ├── textures/          # Shared texture files
│   │   ├── ui/            # Generic UI elements
│   │   ├── effects/       # Particle textures used by multiple effects
│   │   └── fonts/         # Font textures
│   └── animations/        # Shared animation files
│       ├── ui/            # UI animations
│       └── effects/       # Generic effect animations
├── autoload/              # Singleton scripts (auto-loaded)
├── campaigns/             # Campaign data and mission scenes
│   ├── hermes/            # Hermes campaign (self-contained)
│   │   ├── campaign.tres  # Campaign definition
│   │   ├── progression.tres # Campaign progression data
│   │   ├── pilot_data.tres # Pilot progression data
│   │   └── missions/      # Mission scenes with integrated data
│   │       ├── m01_hermes/ # Mission 1 - all files together
│   │       │   ├── mission.tscn      # Main mission scene
│   │       │   ├── mission_data.tres # Mission configuration
│   │       │   ├── briefing.txt      # Briefing text
│   │       │   ├── fiction.txt       # Fiction text
│   │       │   └── objectives.tres   # Mission objectives
│   │       ├── m02_hermes/ # Mission 2
│   │       │   ├── mission.tscn
│   │       │   ├── mission_data.tres
│   │       │   ├── briefing.txt
│   │       │   ├── fiction.txt
│   │       │   └── objectives.tres
│   │       └── templates/ # Mission templates
│   ├── brimstone/         # Brimstone campaign
│   │   ├── campaign.tres  # Campaign definition
│   │   ├── progression.tres # Campaign progression data
│   │   ├── pilot_data.tres # Pilot progression data
│   │   └── missions/      # Mission scenes
│   │       ├── m01_brimstone/ # Mission 1
│   │       │   ├── mission.tscn
│   │       │   ├── mission_data.tres
│   │       │   ├── briefing.txt
│   │       │   ├── fiction.txt
│   │       │   └── objectives.tres
│   │       ├── m02_brimstone/ # Mission 2
│   │       │   ├── mission.tscn
│   │       │   ├── mission_data.tres
│   │       │   ├── briefing.txt
│   │       │   ├── fiction.txt
│   │       │   └── objectives.tres
│   │       └── templates/ # Mission templates
│   ├── training/          # Training campaign
│   │   ├── campaign.tres  # Campaign definition
│   │   ├── tutorials.tres # Tutorial definitions
│   │   └── missions/      # Training missions
│   │       ├── intro_training/ # Introduction training
│   │       │   ├── mission.tscn
│   │       │   ├── mission_data.tres
│   │       │   ├── briefing.txt
│   │       │   └── objectives.tres
│   │       └── advanced_training/ # Advanced training
│   │           ├── mission.tscn
│   │           ├── mission_data.tres
│   │           ├── briefing.txt
│   │           └── objectives.tres
│   └── multiplayer/       # Multiplayer campaigns
│       ├── coop.tres      # Cooperative campaign
│       ├── teams.tres     # Team vs team campaign
│       └── dogfight.tres  # Dogfight campaign
├── features/              # Self-contained game features organized by category
│   ├── fighters/          # Fighter ship entities (primary player and AI ships)
│   │   ├── confed_rapier/ # Raptor fighter - all files together
│   │   │   ├── rapier.tscn    # Scene file
│   │   │   ├── rapier.gd      # Script file
│   │   │   ├── rapier.tres    # Ship data resource
│   │   │   ├── rapier.glb     # 3D model
│   │   │   ├── rapier.png     # Texture
│   │   │   └── rapier_engine.ogg # Engine sound
│   │   ├── kilrathi_dralthi/  # Dralthi fighter
│   │   │   ├── dralthi.tscn
│   │   │   ├── dralthi.gd
│   │   │   ├── dralthi.tres
│   │   │   ├── dralthi.glb
│   │   │   ├── dralthi.png
│   │   │   └── dralthi_engine.ogg
│   │   ├── _shared/           # Shared fighter assets
│   │   │   ├── cockpits/      # Shared cockpit models
│   │   │   │   ├── standard_cockpit.glb
│   │   │   │   └── standard_cockpit_material.tres
│   │   │   └── effects/       # Shared fighter effects
│   │   │       ├── engine_trail.png
│   │   │       └── shield_effect.png
│   │   └── templates/         # Fighter templates
│   ├── capital_ships/         # Capital ship entities
│   │   ├── tcs_tigers_claw/   # Tigers Claw carrier
│   │   │   ├── tigers_claw.tscn
│   │   │   ├── tigers_claw.gd
│   │   │   ├── tigers_claw.tres
│   │   │   ├── tigers_claw.glb
│   │   │   └── tigers_claw.png
│   │   ├── _shared/           # Shared capital ship assets
│   │   │   ├── bridge_models/ # Shared bridge components
│   │   │   └── turret_models/ # Shared turret models
│   │   └── templates/         # Capital ship templates
│   ├── weapons/               # Weapon entities (self-contained)
│   │   ├── laser_cannon/      # Laser cannon
│   │   │   ├── laser_cannon.tscn    # Scene
│   │   │   ├── laser_cannon.gd      # Script
│   │   │   ├── laser_cannon.tres    # Weapon data
│   │   │   ├── laser_cannon.glb     # Model
│   │   │   ├── laser_cannon.png     # Texture
│   │   │   └── laser_fire.ogg       # Sound
│   │   ├── projectiles/       # Projectile entities
│   │   │   ├── laser_bolt/    # Laser bolt projectile
│   │   │   │   ├── laser_bolt.tscn
│   │   │   │   ├── laser_bolt.gd
│   │   │   │   └── laser_bolt.tres
│   │   │   ├── missile/       # Missile projectile
│   │   │   │   ├── missile.tscn
│   │   │   │   ├── missile.gd
│   │   │   │   └── missile.tres
│   │   │   └── templates/     # Projectile templates
│   │   ├── _shared/           # Shared weapon assets
│   │   │   ├── muzzle_flashes/ # Shared muzzle flash effects
│   │   │   └── impact_effects/ # Shared impact effects
│   │   └── templates/         # Weapon templates
│   ├── effects/               # Effect entities
│   │   ├── explosion/         # Explosion effect
│   │   │   ├── explosion.tscn
│   │   │   ├── explosion.gd
│   │   │   ├── explosion.tres
│   │   │   ├── explosion_fire.png
│   │   │   └── explosion_sound.ogg
│   │   ├── fireball/          # Fireball effect
│   │   │   ├── fireball.tscn
│   │   │   ├── fireball.gd
│   │   │   ├── fireball.tres
│   │   │   ├── fireball_texture.png
│   │   │   └── fireball_sound.ogg
│   │   ├── _shared/           # Shared effect assets
│   │   │   ├── particle_textures/ # Shared particle effects
│   │   │   └── shader_effects/    # Shared shader effects
│   │   └── templates/         # Effect templates
│   ├── environment/           # Environmental objects and props
│   │   ├── asteroid/          # Asteroid object
│   │   │   ├── asteroid.tscn
│   │   │   ├── asteroid.gd
│   │   │   ├── asteroid.tres
│   │   │   ├── asteroid.glb
│   │   │   └── asteroid.png
│   │   ├── nebula/            # Nebula effect
│   │   │   ├── nebula.tscn
│   │   │   ├── nebula.gd
│   │   │   ├── nebula.tres
│   │   │   ├── nebula.glb
│   │   │   └── nebula.png
│   │   ├── _shared/           # Shared environment assets
│   │   │   ├── debris/        # Space debris models
│   │   │   └── environment/   # Environmental textures
│   │   └── templates/         # Environment templates
│   ├── ui/                    # UI feature elements
│   │   ├── main_menu/         # Main menu interface
│   │   │   ├── main_menu.tscn
│   │   │   ├── main_menu.gd
│   │   │   ├── background.png
│   │   │   ├── buttons/
│   │   │   │   ├── normal/
│   │   │   │   ├── hover/
│   │   │   │   └── pressed/
│   │   │   ├── animations/
│   │   │   │   ├── transitions/
│   │   │   │   └── background/
│   │   │   └── sounds/
│   │   │       ├── click.ogg
│   │   │       ├── hover.ogg
│   │   │       └── transition.ogg
│   │   ├── hud/               # Heads-up display
│   │   │   ├── player_hud.tscn
│   │   │   ├── player_hud.gd
│   │   │   ├── gauges/
│   │   │   │   ├── speed/
│   │   │   │   ├── shields/
│   │   │   │   ├── weapons/
│   │   │   │   └── fuel/
│   │   │   ├── indicators/
│   │   │   │   ├── targets/
│   │   │   │   ├── warnings/
│   │   │   │   └── status/
│   │   │   ├── animations/
│   │   │   │   ├── warnings/
│   │   │   │   └── status/
│   │   │   └── sounds/
│   │   │       ├── warning.ogg
│   │   │       ├── target_acquired.ogg
│   │   │       └── system_status.ogg
│   │   ├── briefing/          # Briefing interface
│   │   │   ├── briefing_screen.tscn
│   │   │   ├── briefing_screen.gd
│   │   │   ├── background.png
│   │   │   ├── text_display/
│   │   │   ├── mission_map/
│   │   │   ├── animations/
│   │   │   └── sounds/
│   │   │       ├── voice_playback.ogg
│   │   │       └── transition.ogg
│   │   ├── debriefing/        # Debriefing interface
│   │   │   ├── debriefing_screen.tscn
│   │   │   ├── debriefing_screen.gd
│   │   │   ├── background.png
│   │   │   ├── results_display/
│   │   │   ├── statistics/
│   │   │   ├── animations/
│   │   │   └── sounds/
│   │   │       ├── voice_playback.ogg
│   │   │       └── transition.ogg
│   │   ├── options/           # Options menu
│   │   │   ├── options_menu.tscn
│   │   │   ├── options_menu.gd
│   │   │   ├── backgrounds/
│   │   │   ├── sliders/
│   │   │   ├── checkboxes/
│   │   │   ├── animations/
│   │   │   └── sounds/
│   │   │       ├── change_setting.ogg
│   │   │       └── reset_defaults.ogg
│   │   ├── tech_database/     # Technical database
│   │   │   ├── tech_database.tscn
│   │   │   ├── tech_database.gd
│   │   │   ├── backgrounds/
│   │   │   ├── ship_entries/
│   │   │   ├── weapon_entries/
│   │   │   ├── animations/
│   │   │   └── sounds/
│   │   │       ├── entry_select.ogg
│   │   │       └── page_turn.ogg
│   │   ├── _shared/           # Shared UI assets
│   │   │   ├── fonts/         # UI fonts
│   │   │   ├── icons/         # UI icons
│   │   │   ├── themes/        # UI themes
│   │   │   ├── cursors/       # Cursor graphics
│   │   │   └── components/    # Reusable UI components
│   │   │       ├── buttons/
│   │   │       ├── sliders/
│   │   │       ├── checkboxes/
│   │   │       ├── dropdowns/
│   │   │       ├── text_fields/
│   │   │       └── lists/
│   │   └── templates/         # UI templates
│   └── templates/             # Feature templates
├── scripts/               # Reusable GDScript code and custom resources
│   ├── entities/              # Base entity scripts
│   │   ├── base_fighter.gd    # Base fighter controller
│   │   ├── base_capital_ship.gd # Base capital ship controller
│   │   ├── base_weapon.gd     # Base weapon controller
│   │   └── base_effect.gd     # Base effect controller
│   ├── ai/                    # AI behavior scripts
│   │   ├── ai_behavior.gd     # Base AI behavior class
│   │   ├── combat_tactics.gd  # Combat behavior logic
│   │   └── navigation.gd      # Navigation and pathfinding
│   ├── mission/               # Mission system scripts
│   │   ├── mission_manager.gd # Mission orchestration
│   │   ├── event_system.gd    # Mission event handling
│   │   └── objective_tracker.gd # Objective tracking
│   ├── physics/               # Physics system scripts
│   │   ├── flight_model.gd    # Flight physics model
│   │   ├── collision_handler.gd # Collision detection
│   │   └── damage_system.gd   # Damage calculation system
│   ├── audio/                 # Audio system scripts
│   │   ├── sound_manager.gd   # Sound effect management
│   │   ├── music_player.gd    # Music playback system
│   │   └── voice_system.gd    # Voice acting system
│   └── utilities/             # Utility functions and helpers
│       ├── resource_loader.gd # Resource loading utilities
│       ├── object_pool.gd     # Generic object pooling system
│       └── logger.gd          # Logging system
└── README.md             # Project README
```

## Asset Pipeline Integration Points

### Data Converter Outputs
- Table resources (.tres) organized in feature directories by entity type following self-contained feature organization
- Model files (.glb) with embedded metadata in `/features/` directories maintaining co-location principle
- Texture files (.webp/.png) optimized for use in feature directories or `/assets/textures/` directories (following Global Litmus Test)
- Audio files (.ogg) with 3D positioning data in feature directories or `/assets/audio/` directories (following Global Litmus Test)
- Animation resources with timing information in feature directories or `/assets/animations/` directories (following Global Litmus Test)

### Scene Generator Inputs
- Entity class resources for property definitions from feature directories following feature-based organization
- 3D models with hardpoint metadata from `/features/` directories maintaining co-location principle
- Visual effects with particle properties from feature effect directories and global animation directories
- Audio files with spatial information from feature directories or global `/assets/audio/` directories (following Global Litmus Test)
- Text resources with formatting data from campaign mission directories following campaign-centric organization

### Runtime Integration
- Asset loading and caching systems using Godot's resource system with ResourceLoader
- Dynamic property assignment from resources in feature directories following self-contained feature organization
- Event-driven asset updates through Godot's signal system with AnimationPlayer integration
- Cross-reference resolution at runtime using Godot's resource paths with exported variables
- Memory management for loaded assets through Godot's resource system with automatic reference counting

## Validation and Quality Assurance

### Asset Integration Testing
- Verify cross-references between asset types using Godot's resource system with comprehensive dependency checking
- Test scene loading and performance from feature directories following self-contained feature organization
- Validate visual and audio consistency across platforms using Godot's export system
- Check gameplay balance with converted data from feature directories maintaining co-location principle
- Ensure compatibility across different platforms using Godot's export system with platform-specific settings

### Error Handling
- Graceful degradation for missing assets using fallback resources from global `/assets/` directories
- Fallback resources for critical systems from global `/assets/` directories (following Global Litmus Test)
- Error reporting for asset loading failures through Godot's error system with detailed logging
- Recovery mechanisms for corrupted data using resource validation with checksum verification
- User feedback for asset-related issues through UI components with error display systems

## System Integration
Scenes integrate with Godot systems following the separation of concerns principle where reusable logic resides in `/scripts/` and global state management in `/autoload/`:

### Autoload Systems (/autoload/)
- `/autoload/game_state.gd` - Game state management following the "Is this state or service truly global and required everywhere?" principle
- `/autoload/event_bus.gd` - Global event system for decoupled communication between systems
- `/autoload/resource_loader.gd` - Resource loading utilities for data-driven design
- `/autoload/audio_manager.gd` - Audio management for sound effects and music
- `/autoload/save_manager.gd` - Save/load system for player progression

### Script Systems (/scripts/)
- `/scripts/ai/` - AI behavior for ship entities with LimboAI integration
- `/scripts/mission/` - Mission management and event processing with AnimationPlayer timeline sequences
- `/scripts/weapon/` - Weapon behavior and firing logic with projectile management
- `/scripts/physics/` - Physics simulation and movement with space-specific behaviors
- `/scripts/audio/` - Audio playback and 3D positioning with spatial audio

## UI Integration
UI scenes integrate with components in `/features/ui/` directories following feature-based organization where each UI component is a self-contained entity:

### UI Feature Components (/features/ui/)
- `/features/ui/main_menu/` - Main menu interface with background, buttons, animations, and sounds
- `/features/ui/hud/` - Heads-up display elements with gauges, indicators, animations, and sounds
- `/features/ui/briefing/` - Briefing interface components with background, text display, mission map, animations, and sounds
- `/features/ui/debriefing/` - Debriefing interface components with background, results display, statistics, animations, and sounds
- `/features/ui/options/` - Options menu components with backgrounds, sliders, checkboxes, animations, and sounds
- `/features/ui/tech_database/` - Technical database viewer with backgrounds, ship entries, weapon entries, animations, and sounds
- `/features/ui/_shared/` - Shared UI assets including fonts, icons, themes, cursors, and reusable components
- `/features/ui/templates/` - UI templates for consistent interface design

This organization follows the same self-contained approach as other features, ensuring that all files related to a single UI component are grouped together while shared assets are properly organized in the global `/assets/` directory following the "Global Litmus Test" principle.
# Godot Project Directory Structure for Wing Commander Saga

## Overview
This document outlines the recommended directory structure for the Godot implementation of Wing Commander Saga, following Godot's best practices for feature-based organization using a hybrid model. This approach groups all files related to a single conceptual feature into a single, self-contained directory within `/features/`, while maintaining truly global assets in `/assets/` and using `/_shared/` directories for semi-global assets specific to feature categories. This organization enables better maintainability and modularity as recommended by the Godot community and official documentation.

The structure follows Godot's recommended hybrid approach that combines the scalability and modularity of feature-based organization with a clean repository for generic, reusable assets. It uses feature-based organization as the default, with dedicated top-level directories for truly global, shared assets and logic.

## Root Directory Structure
```
wcsaga_godot/
├── addons/                # Third-party plugins and extensions
├── assets/                # Global asset library (truly shared assets)
├── autoload/              # Singleton scripts (auto-loaded)
├── campaigns/             # Campaign data and mission scenes
├── features/              # Self-contained game features organized by category
├── scripts/               # Reusable GDScript code and custom resources
├── project.godot          # Godot project file
└── README.md             # Project README
```

## Assets Directory Structure
The `/assets/` directory is strictly reserved for assets that are generic, context-agnostic, and widely shared across numerous, unrelated features of the game. These are assets that would still be needed even if three random features were removed from the game.

```
assets/
├── audio/                 # Shared audio files
│   ├── sfx/               # Generic sound effects
│   ├── music/             # Background music tracks
│   └── ui/                # UI sound effects
├── textures/              # Shared texture files
│   ├── ui/                # Generic UI elements
│   ├── effects/           # Particle textures used by multiple effects
│   └── fonts/             # Font textures
└── animations/            # Shared animation files
    ├── ui/                # UI animations
    └── effects/           # Generic effect animations
```

## Autoload Directory Structure
This directory is the exclusive home for scripts intended to be registered as Singletons via the Project > Project Settings > AutoLoad panel.

```
autoload/
├── game_state.gd          # Current game state
├── event_bus.gd           # Global event system
├── resource_loader.gd     # Resource loading utilities
├── audio_manager.gd       # Audio management
└── save_manager.gd        # Save/load system
```

## Features Directory Structure
This directory is the primary workspace for the majority of game development. It embodies the "Organization by Feature" philosophy and is the designated location for all self-contained, instantiable game entities. If you can drag it into a scene or spawn it at runtime as a distinct "thing," its source files belong here.

```
features/
├── fighters/              # Fighter ship entities (primary player and AI ships)
│   ├── confed_rapier/     # Raptor fighter - all files together
│   │   ├── rapier.tscn    # Scene file
│   │   ├── rapier.gd      # Script file
│   │   ├── rapier.tres    # Ship data resource
│   │   ├── rapier.glb     # 3D model
│   │   ├── rapier.png     # Texture
│   │   └── rapier_engine.ogg # Engine sound
│   ├── kilrathi_dralthi/  # Dralthi fighter
│   │   ├── dralthi.tscn
│   │   ├── dralthi.gd
│   │   ├── dralthi.tres
│   │   ├── dralthi.glb
│   │   ├── dralthi.png
│   │   └── dralthi_engine.ogg
│   ├── _shared/           # Shared fighter assets
│   │   ├── cockpits/      # Shared cockpit models
│   │   │   ├── standard_cockpit.glb
│   │   │   └── standard_cockpit_material.tres
│   │   └── effects/       # Shared fighter effects
│   │       ├── engine_trail.png
│   │       └── shield_effect.png
│   └── templates/         # Fighter templates
├── capital_ships/         # Capital ship entities
│   ├── tcs_tigers_claw/   # Tigers Claw carrier
│   │   ├── tigers_claw.tscn
│   │   ├── tigers_claw.gd
│   │   ├── tigers_claw.tres
│   │   ├── tigers_claw.glb
│   │   └── tigers_claw.png
│   ├── _shared/           # Shared capital ship assets
│   │   ├── bridge_models/ # Shared bridge components
│   │   └── turret_models/ # Shared turret models
│   └── templates/         # Capital ship templates
├── weapons/               # Weapon entities (self-contained)
│   ├── laser_cannon/      # Laser cannon
│   │   ├── laser_cannon.tscn    # Scene
│   │   ├── laser_cannon.gd      # Script
│   │   ├── laser_cannon.tres    # Weapon data
│   │   ├── laser_cannon.glb     # Model
│   │   ├── laser_cannon.png     # Texture
│   │   └── laser_fire.ogg       # Sound
│   ├── projectiles/       # Projectile entities
│   │   ├── laser_bolt/    # Laser bolt projectile
│   │   │   ├── laser_bolt.tscn
│   │   │   ├── laser_bolt.gd
│   │   │   └── laser_bolt.tres
│   │   ├── missile/       # Missile projectile
│   │   │   ├── missile.tscn
│   │   │   ├── missile.gd
│   │   │   └── missile.tres
│   │   └── templates/     # Projectile templates
│   ├── _shared/           # Shared weapon assets
│   │   ├── muzzle_flashes/ # Shared muzzle flash effects
│   │   └── impact_effects/ # Shared impact effects
│   └── templates/         # Weapon templates
├── effects/               # Effect entities
│   ├── explosion/         # Explosion effect
│   │   ├── explosion.tscn
│   │   ├── explosion.gd
│   │   ├── explosion.tres
│   │   ├── explosion_fire.png
│   │   └── explosion_sound.ogg
│   ├── fireball/          # Fireball effect
│   │   ├── fireball.tscn
│   │   ├── fireball.gd
│   │   ├── fireball.tres
│   │   ├── fireball_texture.png
│   │   └── fireball_sound.ogg
│   ├── _shared/           # Shared effect assets
│   │   ├── particle_textures/ # Shared particle effects
│   │   └── shader_effects/    # Shared shader effects
│   └── templates/         # Effect templates
├── environment/           # Environmental objects and props
│   ├── asteroid/          # Asteroid object
│   │   ├── asteroid.tscn
│   │   ├── asteroid.gd
│   │   ├── asteroid.tres
│   │   ├── asteroid.glb
│   │   └── asteroid.png
│   ├── nebula/            # Nebula effect
│   │   ├── nebula.tscn
│   │   ├── nebula.gd
│   │   ├── nebula.tres
│   │   ├── nebula.glb
│   │   └── nebula.png
│   ├── _shared/           # Shared environment assets
│   │   ├── debris/        # Space debris models
│   │   └── environment/   # Environmental textures
│   └── templates/         # Environment templates
├── ui/                    # UI feature elements
│   ├── main_menu/         # Main menu interface
│   │   ├── main_menu.tscn
│   │   ├── main_menu.gd
│   │   ├── background.png
│   │   ├── buttons/
│   │   │   ├── normal/
│   │   │   ├── hover/
│   │   │   └── pressed/
│   │   ├── animations/
│   │   │   ├── transitions/
│   │   │   └── background/
│   │   └── sounds/
│   │       ├── click.ogg
│   │       ├── hover.ogg
│   │       └── transition.ogg
│   ├── hud/               # Heads-up display
│   │   ├── player_hud.tscn
│   │   ├── player_hud.gd
│   │   ├── gauges/
│   │   │   ├── speed/
│   │   │   ├── shields/
│   │   │   ├── weapons/
│   │   │   └── fuel/
│   │   ├── indicators/
│   │   │   ├── targets/
│   │   │   ├── warnings/
│   │   │   └── status/
│   │   ├── animations/
│   │   │   ├── warnings/
│   │   │   └── status/
│   │   └── sounds/
│   │       ├── warning.ogg
│   │       ├── target_acquired.ogg
│   │       └── system_status.ogg
│   ├── briefing/          # Briefing interface
│   │   ├── briefing_screen.tscn
│   │   ├── briefing_screen.gd
│   │   ├── background.png
│   │   ├── text_display/
│   │   ├── mission_map/
│   │   ├── animations/
│   │   └── sounds/
│   │       ├── voice_playback.ogg
│   │       └── transition.ogg
│   ├── debriefing/        # Debriefing interface
│   │   ├── debriefing_screen.tscn
│   │   ├── debriefing_screen.gd
│   │   ├── background.png
│   │   ├── results_display/
│   │   ├── statistics/
│   │   ├── animations/
│   │   └── sounds/
│   │       ├── voice_playback.ogg
│   │       └── transition.ogg
│   ├── options/           # Options menu
│   │   ├── options_menu.tscn
│   │   ├── options_menu.gd
│   │   ├── backgrounds/
│   │   ├── sliders/
│   │   ├── checkboxes/
│   │   ├── animations/
│   │   └── sounds/
│   │       ├── change_setting.ogg
│   │       └── reset_defaults.ogg
│   ├── tech_database/     # Technical database
│   │   ├── tech_database.tscn
│   │   ├── tech_database.gd
│   │   ├── backgrounds/
│   │   ├── ship_entries/
│   │   ├── weapon_entries/
│   │   ├── animations/
│   │   └── sounds/
│   │       ├── entry_select.ogg
│   │       └── page_turn.ogg
│   ├── _shared/           # Shared UI assets
│   │   ├── fonts/         # UI fonts
│   │   ├── icons/         # UI icons
│   │   ├── themes/        # UI themes
│   │   ├── cursors/       # Cursor graphics
│   │   └── components/    # Reusable UI components
│   │       ├── buttons/
│   │       ├── sliders/
│   │       ├── checkboxes/
│   │       ├── dropdowns/
│   │       ├── text_fields/
│   │       └── lists/
│   └── templates/         # UI templates
└── templates/             # Feature templates
```

## Scripts Directory Structure
The `/scripts/` directory serves a critical role as the repository for abstract, reusable code and data definitions. The key distinction is that nothing in this folder should be a complete, instantiable game object that one could drag into a scene. Instead, it contains the foundational building blocks that concrete features will use and extend.

```
scripts/
├── entities/              # Base entity scripts
│   ├── base_fighter.gd    # Base fighter controller
│   ├── base_capital_ship.gd # Base capital ship controller
│   ├── base_weapon.gd     # Base weapon controller
│   └── base_effect.gd     # Base effect controller
├── ai/                    # AI behavior scripts
│   ├── ai_behavior.gd     # Base AI behavior class
│   ├── combat_tactics.gd  # Combat behavior logic
│   └── navigation.gd      # Navigation and pathfinding
├── mission/               # Mission system scripts
│   ├── mission_manager.gd # Mission orchestration
│   ├── event_system.gd    # Mission event handling
│   └── objective_tracker.gd # Objective tracking
├── physics/               # Physics system scripts
│   ├── flight_model.gd    # Flight physics model
│   ├── collision_handler.gd # Collision detection
│   └── damage_system.gd   # Damage calculation system
├── audio/                 # Audio system scripts
│   ├── sound_manager.gd   # Sound effect management
│   ├── music_player.gd    # Music playback system
│   └── voice_system.gd    # Voice acting system
└── utilities/             # Utility functions and helpers
    ├── resource_loader.gd # Resource loading utilities
    ├── object_pool.gd     # Generic object pooling system
    └── logger.gd          # Logging system
```

## Campaigns Directory Structure
The `/campaigns/` directory is dedicated to organizing all data related to the game's narrative progression, missions, and other sequential content. This structure creates a clean separation between the reusable game mechanics (defined in `/features/`) and the specific content that uses those mechanics to create a gameplay experience.

```
campaigns/
├── hermes/                # Hermes campaign (self-contained)
│   ├── campaign.tres      # Campaign definition
│   ├── progression.tres   # Campaign progression data
│   ├── pilot_data.tres    # Pilot progression data
│   └── missions/          # Mission scenes with integrated data
│       ├── m01_hermes/    # Mission 1 - all files together
│       │   ├── mission.tscn      # Main mission scene
│       │   ├── mission_data.tres # Mission configuration
│       │   ├── briefing.txt      # Briefing text
│       │   ├── fiction.txt       # Fiction text
│       │   └── objectives.tres   # Mission objectives
│       ├── m02_hermes/    # Mission 2
│       │   ├── mission.tscn
│       │   ├── mission_data.tres
│       │   ├── briefing.txt
│       │   ├── fiction.txt
│       │   └── objectives.tres
│       └── templates/     # Mission templates
├── brimstone/             # Brimstone campaign
│   ├── campaign.tres      # Campaign definition
│   ├── progression.tres   # Campaign progression data
│   ├── pilot_data.tres    # Pilot progression data
│   └── missions/          # Mission scenes
│       ├── m01_brimstone/ # Mission 1
│       │   ├── mission.tscn
│       │   ├── mission_data.tres
│       │   ├── briefing.txt
│       │   ├── fiction.txt
│       │   └── objectives.tres
│       ├── m02_brimstone/ # Mission 2
│       │   ├── mission.tscn
│       │   ├── mission_data.tres
│       │   ├── briefing.txt
│       │   ├── fiction.txt
│       │   └── objectives.tres
│       └── templates/     # Mission templates
├── training/              # Training campaign
│   ├── campaign.tres      # Campaign definition
│   ├── tutorials.tres     # Tutorial definitions
│   └── missions/          # Training missions
│       ├── intro_training/ # Introduction training
│       │   ├── mission.tscn
│       │   ├── mission_data.tres
│       │   ├── briefing.txt
│       │   └── objectives.tres
│       └── advanced_training/ # Advanced training
│           ├── mission.tscn
│           ├── mission_data.tres
│           ├── briefing.txt
│           └── objectives.tres
└── multiplayer/           # Multiplayer campaigns
    ├── coop.tres          # Cooperative campaign
    ├── teams.tres         # Team vs team campaign
    └── dogfight.tres      # Dogfight campaign
```

## Key Principles

This directory structure follows these key Godot best practices:

1. **Self-Contained Feature Organization**: All files related to a single feature are grouped together in a self-contained directory. For example, all assets, scripts, and data for a "Rapier" fighter reside within `/features/fighters/confed_rapier/`, including its scene file, script, data resource, 3D model, textures, and associated sound effects.

2. **Feature-Based Organization**: This approach treats each feature folder as a self-contained module or component, aligning perfectly with Godot's design philosophy of creating self-contained scenes that encapsulate their own logic and resources.

3. **Hybrid Asset Organization**: This structure follows a hybrid model where truly global, context-agnostic assets are organized in `/assets/`, while semi-global assets shared by a specific category of features use `/_shared/` directories within their parent category (e.g., `/features/fighters/_shared/cockpits/`). The guiding principle is: "If I delete three random features, is this asset still needed?" If yes, it belongs in `/assets/`; if only needed by a specific feature category, it belongs in that category's `/_shared/` directory.

4. **Campaign-Centric Mission Organization**: All mission data, including mission configuration, briefing, fiction, and objectives, is stored with the mission scenes in campaign-specific directories.

5. **Naming Conventions**: 
   - Folders and files use snake_case (e.g., `player_fighter.gd`, `weapon_data.tres`) to avoid case-sensitivity conflicts across platforms.
   - Node names within scenes and script class names use PascalCase (e.g., `PlayerFighter`, `class_name WeaponSystem`) to align with Godot's built-in conventions.

6. **Separation of Concerns**: The structure clearly separates:
   - Global asset library (`/assets/`)
   - Singleton management (`/autoload/`)
   - Self-contained game features (`/features/`)
   - Campaign progression with mission data (`/campaigns/`)
   - Reusable script code and resources (`/scripts/`)

7. **UI Organization**: User interface elements are organized within `/features/ui/` following the same feature-based approach, with each UI screen or component as a self-contained directory. The UI structure includes comprehensive systems like main menu, HUD, briefing/debriefing screens, options, and tech database. Shared UI assets like fonts, icons, and themes are placed in `/features/ui/_shared/`.

8. **Scalability**: Each feature folder is a self-contained, portable module that can be developed, tested, and maintained in isolation, enhancing team collaboration and simplifying long-term maintenance.

9. **Self-Contained Scenes**: Each scene is designed as a modular unit where the script attached to the scene's root node only directly references its own children or descendants, following the "functions down, signals up" principle for decoupled communication.

This structure provides a robust foundation that aligns with Godot's idiomatic patterns and follows the hybrid organizational model, while preserving the modularity of the original Wing Commander Saga architecture.
# Godot Project Directory Structure for Wing Commander Saga

## Overview
This document outlines the recommended directory structure for the Godot implementation of Wing Commander Saga, following Godot's best practices for feature-based organization. This approach groups all files related to a single conceptual unit into a single, self-contained directory, enabling better maintainability and modularity as recommended by the Godot community and official documentation.

## Root Directory Structure
```
wcsaga_godot/
├── addons/                # Third-party plugins and extensions
├── core/                  # Engine-agnostic core logic (state machine, event bus)
├── data/                  # Data-driven Resource files (.tres)
├── entities/              # Physical game objects (ships, weapons, projectiles)
├── systems/               # Game logic systems (AI, mission control, weapon control)
├── ui/                    # User interface elements
├── campaigns/             # Campaign data, progression, and mission scenes
├── docs/                  # Documentation
├── project.godot          # Godot project file
└── README.md             # Project README
```

## Core Directory Structure
```
core/
├── state_machine.gd       # Base state machine class
├── event_bus.gd           # Global event bus for decoupled communication
├── resource_loader.gd     # Resource loading utilities
├── object_pool.gd         # Generic object pooling system
└── logger.gd              # Logging system
```

## Data Directory Structure
```
data/
├── ships/                 # Ship data resources
│   ├── terran/            # Terran ship data
│   │   ├── fighters/
│   │   ├── bombers/
│   │   ├── capitals/
│   │   └── support/
│   ├── kilrathi/          # Kilrathi ship data
│   │   ├── fighters/
│   │   ├── bombers/
│   │   └── capitals/
│   ├── pirate/            # Pirate ship data
│   │   ├── fighters/
│   │   └── capitals/
│   └── templates/         # Ship data templates
├── weapons/               # Weapon data resources
│   ├── terran/            # Terran weapon data
│   ├── kilrathi/          # Kilrathi weapon data
│   ├── pirate/            # Pirate weapon data
│   └── templates/         # Weapon data templates
├── ai/                    # AI behavior data
│   ├── profiles/          # AI behavior profiles
│   ├── behaviors/         # AI behavior trees
│   ├── tactics/           # Combat tactics
│   ├── formations/        # Formation flying patterns
│   └── goals/             # AI goals
├── campaigns/             # Campaign data resources
│   ├── brimstone/         # Brimstone campaign data
│   │   ├── missions/      # Mission data resources
│   │   ├── progression/   # Campaign progression
│   │   └── story/         # Story elements
│   ├── hermes/            # Hermes campaign data
│   │   ├── missions/      # Mission data resources
│   │   ├── progression/   # Campaign progression
│   │   └── story/         # Story elements
│   └── training/          # Training campaign data
│       ├── missions/      # Training mission data
│       └── tutorials/     # Tutorial definitions
├── effects/               # Effect data resources
└── config/                # Configuration data
    ├── difficulty/        # Difficulty settings
    ├── graphics/          # Graphics settings
    ├── audio/             # Audio settings
    └── controls/          # Control settings
```

## Entities Directory Structure
```
entities/
├── fighters/              # Fighter ship entities
│   ├── confed_rapier/     # Raptor fighter
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
│   └── templates/         # Fighter templates
├── capital_ships/         # Capital ship entities
│   ├── tcs_tigers_claw/   # Tigers Claw carrier
│   │   ├── tigers_claw.tscn
│   │   ├── tigers_claw.gd
│   │   ├── tigers_claw.tres
│   │   ├── tigers_claw.glb
│   │   └── tigers_claw.png
│   └── templates/         # Capital ship templates
├── projectiles/           # Projectile entities
│   ├── laser_bolt/        # Laser bolt projectile
│   │   ├── laser_bolt.tscn
│   │   ├── laser_bolt.gd
│   │   └── laser_bolt.tres
│   ├── missile/           # Missile projectile
│   │   ├── missile.tscn
│   │   ├── missile.gd
│   │   └── missile.tres
│   └── templates/         # Projectile templates
├── weapons/               # Weapon entities
│   ├── laser_cannon/      # Laser cannon weapon
│   │   ├── laser_cannon.tscn
│   │   ├── laser_cannon.gd
│   │   └── laser_cannon.tres
│   └── templates/         # Weapon templates
├── effects/               # Effect entities
│   ├── explosion/         # Explosion effect
│   │   ├── explosion.tscn
│   │   ├── explosion.gd
│   │   └── explosion.tres
│   ├── fireball/          # Fireball effect
│   │   ├── fireball.tscn
│   │   ├── fireball.gd
│   │   └── fireball.tres
│   └── templates/         # Effect templates
├── environment/           # Environmental entities
│   ├── asteroid/          # Asteroid object
│   │   ├── asteroid.tscn
│   │   ├── asteroid.gd
│   │   └── asteroid.tres
│   ├── nebula/            # Nebula effect
│   │   ├── nebula.tscn
│   │   ├── nebula.gd
│   │   └── nebula.tres
│   └── templates/         # Environment templates
└── templates/             # Entity templates
```

## Systems Directory Structure
```
systems/
├── ai/                    # AI systems
│   ├── state_machine.gd   # AI state machine controller
│   ├── attack_state.gd    # Attack behavior state
│   ├── patrol_state.gd    # Patrol behavior state
│   ├── evade_state.gd     # Evasion behavior state
│   └── formation_flying.gd # Formation flying logic
├── mission_control/       # Mission control systems
│   ├── mission_manager.tscn # Mission manager scene
│   ├── mission_manager.gd # Mission manager script
│   ├── campaign_manager.gd # Campaign progression manager
│   └── objective_tracker.gd # Mission objective tracking
├── weapon_control/        # Weapon control systems
│   ├── weapon_controller.gd # Weapon controller logic
│   ├── projectile_manager.gd # Projectile management
│   └── beam_system.gd     # Beam weapon system
├── physics/               # Physics systems
│   ├── flight_model.gd    # Flight physics model
│   ├── collision_handler.gd # Collision detection
│   └── damage_system.gd   # Damage calculation system
├── audio/                 # Audio systems
│   ├── sound_manager.gd   # Sound effect management
│   ├── music_player.gd    # Music playback system
│   └── voice_system.gd    # Voice acting system
├── graphics/              # Graphics systems
│   ├── renderer.gd        # Rendering manager
│   ├── lighting_system.gd # Dynamic lighting
│   └── post_processing.gd # Post-processing effects
└── networking/            # Multiplayer systems
    ├── net_manager.gd     # Network management
    ├── multiplayer_sync.gd # Multiplayer synchronization
    └── chat_system.gd     # In-game chat
```

## UI Directory Structure
```
ui/
├── main_menu/             # Main menu interface
│   ├── main_menu.tscn     # Main menu scene
│   ├── main_menu.gd       # Main menu script
│   ├── menu_button.gd     # Custom menu button
│   └── menu_theme.tres    # Menu theme resource
├── hud/                   # Heads-up display
│   ├── player_hud.tscn    # HUD scene
│   ├── player_hud.gd      # HUD script
│   ├── radar_display.gd   # Radar display logic
│   ├── weapon_status.gd   # Weapon status display
│   └── target_info.gd     # Target information display
├── briefing/              # Briefing interface
│   ├── briefing_screen.tscn
│   ├── briefing_screen.gd
│   ├── mission_objectives.gd
│   └── intel_viewer.gd
├── debriefing/            # Debriefing interface
│   ├── debriefing_screen.tscn
│   ├── debriefing_screen.gd
│   ├── mission_stats.gd
│   └── promotion_display.gd
├── options/               # Options menu
│   ├── options_menu.tscn
│   ├── options_menu.gd
│   ├── graphics_options.gd
│   ├── audio_options.gd
│   └── control_options.gd
├── tech_database/         # Technical database viewer
│   ├── tech_database.tscn
│   ├── tech_database.gd
│   ├── ship_viewer.gd
│   └── weapon_viewer.gd
├── components/            # Reusable UI components
│   ├── custom_button.gd
│   ├── custom_slider.gd
│   ├── scrollable_list.gd
│   └── tab_container.gd
└── themes/                # UI themes
    ├── default_theme.tres
    ├── dark_theme.tres
    └── light_theme.tres
```

## Campaigns Directory Structure (Consolidated)
```
campaigns/
├── brimstone/             # Brimstone campaign
│   ├── campaign.tres      # Campaign definition
│   ├── progression.tres   # Campaign progression data
│   ├── pilot_data.tres    # Pilot progression data
│   └── missions/          # Mission scenes and data
│       ├── m01_brimstone/ # Mission 1
│       │   ├── mission.tscn # Mission scene
│       │   ├── mission.tres # Mission data resource
│       │   ├── briefing.txt # Briefing text
│       │   ├── fiction.txt  # Fiction text
│       │   └── objectives.tres # Mission objectives
│       ├── m02_brimstone/ # Mission 2
│       │   ├── mission.tscn
│       │   ├── mission.tres
│       │   ├── briefing.txt
│       │   ├── fiction.txt
│       │   └── objectives.tres
│       └── templates/     # Mission templates
├── hermes/                # Hermes campaign
│   ├── campaign.tres      # Campaign definition
│   ├── progression.tres   # Campaign progression data
│   ├── pilot_data.tres    # Pilot progression data
│   └── missions/          # Mission scenes and data
│       ├── m01_hermes/    # Mission 1
│       │   ├── mission.tscn
│       │   ├── mission.tres
│       │   ├── briefing.txt
│       │   ├── fiction.txt
│       │   └── objectives.tres
│       ├── m02_hermes/    # Mission 2
│       │   ├── mission.tscn
│       │   ├── mission.tres
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
│       │   ├── mission.tres
│       │   ├── briefing.txt
│       │   └── objectives.tres
│       └── advanced_training/ # Advanced training
│           ├── mission.tscn
│           ├── mission.tres
│           ├── briefing.txt
│           └── objectives.tres
└── multiplayer/           # Multiplayer campaigns
    ├── coop.tres          # Cooperative campaign
    ├── teams.tres         # Team vs team campaign
    └── dogfight.tres      # Dogfight campaign
```

## Documentation Directory Structure
```
docs/
├── architecture/          # System architecture
│   ├── overview.md        # High-level overview
│   ├── modules.md         # Module breakdown
│   └── integration.md     # Integration plan
├── development/           # Development guides
│   ├── setup.md           # Project setup
│   ├── building.md        # Building instructions
│   └── testing.md         # Testing procedures
├── modding/               # Modding documentation
│   ├── getting_started.md # Modding introduction
│   ├── ship_modding.md    # Ship modding guide
│   ├── weapon_modding.md  # Weapon modding guide
│   └── mission_modding.md # Mission modding guide
├── api/                   # API documentation
│   ├── core.md            # Core API
│   ├── gameplay.md        # Gameplay API
│   ├── ui.md              # UI API
│   └── systems.md         # Systems API
├── changelog/             # Version history
│   ├── v1.0.0.md          # Version 1.0.0 changes
│   ├── v1.1.0.md          # Version 1.1.0 changes
│   └── v1.2.0.md          # Version 1.2.0 changes
└── licenses/              # License information
    ├── project.md         # Project license
    ├── assets.md          # Asset license
    └── third_party.md     # Third-party licenses
```

## Key Principles

This directory structure follows these key Godot best practices:

1. **Feature-Based Organization**: All files related to a single conceptual unit are grouped together in a self-contained directory. For example, all assets and scripts for a "Rapier" fighter reside within `/entities/fighters/confed_rapier/`, including its scene file, script, 3D model, textures, and associated sound effects.

2. **Naming Conventions**: 
   - Folders and files use snake_case (e.g., `player_fighter.gd`, `weapon_data.tres`) to avoid case-sensitivity conflicts across platforms.
   - Node names within scenes and script class names use PascalCase (e.g., `PlayerFighter`, `class_name WeaponSystem`) to align with Godot's built-in conventions.

3. **Separation of Concerns**: The structure clearly separates:
   - Reusable core logic (`/core/`)
   - Gameplay-agnostic data (`/data/`)
   - Physical game objects (`/entities/`)
   - The logic that governs them (`/systems/`)
   - User interface elements (`/ui/`)
   - Campaign progression (`/campaigns/`)

4. **Scalability**: Each feature folder is a self-contained, portable module that can be developed, tested, and maintained in isolation, enhancing team collaboration and simplifying long-term maintenance.

5. **Self-Contained Scenes**: Each scene is designed as a modular unit where the script attached to the scene's root node only directly references its own children or descendants, following the "functions down, signals up" principle for decoupled communication.

This structure provides a robust foundation that aligns with Godot's idiomatic patterns while preserving the modularity of the original Wing Commander Saga architecture.
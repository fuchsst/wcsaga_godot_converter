# UI Elements Asset Mapping

## Overview
This document maps the UI element definitions from various TBL files to their corresponding media assets in the Wing Commander Saga Hermes campaign, organized according to the Godot feature-based directory structure. The mapping follows the hybrid model where truly global UI assets are organized in the `/assets/` directory, while feature-specific UI elements are co-located with their respective features.

## Asset Types

### Interface Graphics (.pcx/.dds)
Various TBL files reference PCX and DDS interface graphics:
- Mainhall.tbl - Main hall interface graphics
- HUD_gauges.tbl - HUD gauge graphics
- Icons.tbl - Icon graphics for ships/weapons
- Fonts.tbl - Font character set graphics
- Menu.tbl - Menu background and element graphics
- Briefing.tbl - Briefing screen graphics
- Debriefing.tbl - Debriefing screen graphics

Common UI graphics include:
- Main hall background images (mainhall1.pcx, 2_mainhall.dds)
- Button backgrounds and states
- Gauge faces and needles
- Progress bars and sliders
- Window borders and backgrounds
- Icon sets for ships, weapons, and systems
- Font character sets
- Cursor graphics (cursor_hud.pcx)
- Loading screen graphics

### Animation Effects (.ani)
UI animations referenced in various TBL files:
- Mainhall.tbl - Main hall animation sequences (2_mainhall_misc_*.ani)
- HUD animations for dynamic elements
- Menu transition animations
- Briefing/debriefing screen animations
- Loading screen animations
- Static effects (TargetStatic.ani, RadarStatic.ani)

### Sound Effects (.wav)
UI sound effects referenced in various TBL files:
- Button click/rollover sounds
- Menu navigation sounds
- Alert/notification sounds
- Success/failure feedback sounds
- Typing/input sounds
- Transition sounds

### Text Content (.txt)
Interface text content:
- Help text and tutorials
- Menu item labels
- Tooltip descriptions
- Error messages
- Status messages
- Mission briefings

## Format Conversion Process

### Legacy Formats to Godot Formats

**PCX Files (.pcx)**
- Legacy image format for interface graphics
- Will be converted to WebP format for better compression and Godot compatibility
- Color palette and transparency preserved during conversion
- Resolution maintained for accurate display

**DDS Files (.dds)**
- Legacy texture format for interface graphics
- Will be converted to WebP format for better compression and Godot compatibility
- Mipmaps and compression settings preserved during conversion
- Alpha channels maintained for transparency effects

**ANI Files (.ani)**
- Legacy animation format for UI effects
- Will be converted to sprite sheet animations or particle effects in Godot
- Animation frame sequences preserved during conversion
- Timing and looping properties maintained where appropriate

**TBL Files (.tbl)**
- Legacy configuration format for UI definitions
- Will be converted to Godot resource files (.tres) for data-driven design
- Property mappings preserved with appropriate Godot data types
- UI layout and positioning data maintained for interface construction

## Target Structure
Following the Godot project structure defined in directory_structure.md and the hybrid organizational model, UI assets are organized as follows:

### Assets Directory Structure
Generic UI assets that are shared across multiple features are organized in the global `/assets/` directory, following the "Global Litmus Test" principle: "If I delete three random features, is this asset still needed?"

```
assets/
├── audio/                         # Shared audio files
│   └── ui/                        # UI sound effects
│       ├── buttons/               # Button sounds
│       ├── menus/                 # Menu sounds
│       ├── hud/                   # HUD sounds
│       ├── notifications/         # Notification sounds
│       └── transitions/           # Transition sounds
├── textures/                      # Shared texture files
│   └── ui/                        # Generic UI elements
│       ├── backgrounds/           # Background graphics
│       ├── buttons/               # Button graphics
│       ├── gauges/                # Gauge graphics
│       ├── indicators/            # Indicator graphics
│       ├── icons/                 # Icon graphics
│       ├── fonts/                 # Font graphics
│       ├── cursors/               # Cursor graphics
│       └── animations/            # UI animation frames
└── animations/                    # Shared animation files
    └── ui/                        # UI animations
        ├── transitions/           # Screen transitions
        ├── buttons/               # Button animations
        ├── gauges/                # Gauge animations
        ├── indicators/            # Indicator animations
        └── menus/                 # Menu animations
```

### Features Directory Structure
Feature-specific UI elements that are closely tied to particular features are organized within their respective feature directories, following the co-location principle where all files related to a single feature are grouped together.

```
features/
├── ui/                            # UI feature elements
│   ├── main_menu/                 # Main menu interface
│   │   ├── main_menu.tscn         # Main menu scene
│   │   ├── main_menu.gd           # Main menu script
│   │   ├── background.webp        # Background graphic (converted from mainhall1.pcx)
│   │   ├── buttons/               # Button graphics
│   │   │   ├── normal/            # Normal button states
│   │   │   ├── hover/             # Hover button states
│   │   │   └── pressed/           # Pressed button states
│   │   ├── animations/            # Menu animations
│   │   │   ├── transitions/       # Menu transition animations
│   │   │   └── background/        # Background animations (converted from 2_mainhall_misc_*.ani)
│   │   └── sounds/                # Menu sounds
│   │       ├── click.ogg          # Button click sound
│   │       ├── hover.ogg          # Button hover sound
│   │       └── transition.ogg     # Menu transition sound
│   ├── hud/                       # Heads-up display
│   │   ├── player_hud.tscn        # Player HUD scene
│   │   ├── player_hud.gd          # Player HUD script
│   │   ├── gauges/                # HUD gauge graphics
│   │   │   ├── speed/             # Speed gauge elements
│   │   │   ├── shields/           # Shield gauge elements
│   │   │   ├── weapons/           # Weapon gauge elements
│   │   │   └── fuel/              # Fuel gauge elements
│   │   ├── indicators/            # HUD indicator graphics
│   │   │   ├── targets/           # Target indicators
│   │   │   ├── warnings/          # Warning indicators
│   │   │   └── status/            # Status indicators
│   │   ├── animations/            # HUD animations
│   │   │   ├── warnings/          # Warning animations (converted from TargetStatic.ani)
│   │   │   └── status/            # Status animations
│   │   └── sounds/                # HUD sounds
│   │       ├── warning.ogg        # Warning sound
│   │       ├── target_acquired.ogg # Target acquired sound
│   │       └── system_status.ogg  # System status sound
│   ├── briefing/                  # Briefing interface
│   │   ├── briefing_screen.tscn   # Briefing screen scene
│   │   ├── briefing_screen.gd     # Briefing screen script
│   │   ├── background.webp        # Background graphic
│   │   ├── text_display/          # Text display area
│   │   ├── mission_map/           # Mission map area
│   │   ├── animations/            # Briefing animations
│   │   └── sounds/                # Briefing sounds
│   │       ├── voice_playback.ogg # Voice playback sound
│   │       └── transition.ogg     # Screen transition sound
│   ├── debriefing/                # Debriefing interface
│   │   ├── debriefing_screen.tscn # Debriefing screen scene
│   │   ├── debriefing_screen.gd   # Debriefing screen script
│   │   ├── background.webp        # Background graphic
│   │   ├── results_display/       # Results display area
│   │   ├── statistics/            # Statistics display
│   │   ├── animations/            # Debriefing animations
│   │   └── sounds/                # Debriefing sounds
│   │       ├── voice_playback.ogg # Voice playback sound
│   │       └── transition.ogg     # Screen transition sound
│   ├── options/                   # Options menu
│   │   ├── options_menu.tscn      # Options menu scene
│   │   ├── options_menu.gd        # Options menu script
│   │   ├── backgrounds/           # Background graphics
│   │   ├── sliders/               # Slider graphics
│   │   ├── checkboxes/            # Checkbox graphics
│   │   ├── animations/            # Options animations
│   │   └── sounds/                # Options sounds
│   │       ├── change_setting.ogg # Setting change sound
│   │       └── reset_defaults.ogg # Reset defaults sound
│   ├── tech_database/             # Technical database
│   │   ├── tech_database.tscn     # Tech database scene
│   │   ├── tech_database.gd       # Tech database script
│   │   ├── backgrounds/           # Background graphics
│   │   ├── ship_entries/          # Ship entry graphics
│   │   ├── weapon_entries/        # Weapon entry graphics
│   │   ├── animations/            # Database animations
│   │   └── sounds/                # Database sounds
│   │       ├── entry_select.ogg   # Entry selection sound
│   │       └── page_turn.ogg      # Page turn sound
│   └── _shared/                   # Shared UI assets
│       ├── fonts/                 # UI fonts
│       ├── icons/                 # UI icons
│       ├── themes/                # UI themes
│       ├── cursors/               # Cursor graphics (converted from cursor_hud.pcx)
│       └── components/            # Reusable UI components
│           ├── buttons/           # Button components
│           ├── sliders/           # Slider components
│           ├── checkboxes/        # Checkbox components
│           ├── dropdowns/         # Dropdown components
│           ├── text_fields/       # Text field components
│           └── lists/             # List components
└── templates/                     # Feature templates

/campaigns/                        # Campaign data and mission scenes
├── hermes/                        # Hermes campaign
│   └── ui_text/                   # UI text content (campaign-specific)
│       ├── menus/                 # Menu text
│       ├── hud/                   # HUD text
│       ├── briefing/              # Briefing text
│       ├── debriefing/            # Debriefing text
│       ├── options/               # Options text
│       ├── help/                  # Help text
│       └── tutorials/             # Tutorial text
└── brimstone/                     # Brimstone campaign
    └── ui_text/                   # UI text content (campaign-specific)
        ├── menus/                 # Menu text
        ├── hud/                   # HUD text
        ├── briefing/              # Briefing text
        ├── debriefing/            # Debriefing text
        ├── options/               # Options text
        ├── help/                  # Help text
        └── tutorials/             # Tutorial text
```

### Scripts Directory Structure
Reusable UI system scripts are organized in the `/scripts/` directory, following the separation of concerns principle.

```
scripts/
├── ui/                            # UI system scripts
│   ├── ui_manager.gd              # UI management system
│   ├── ui_element.gd              # Base UI element class
│   ├── button.gd                  # Button component
│   ├── slider.gd                  # Slider component
│   ├── checkbox.gd                # Checkbox component
│   ├── dropdown.gd                # Dropdown component
│   ├── text_field.gd              # Text field component
│   ├── list.gd                    # List component
│   ├── hud_system.gd              # HUD system
│   ├── menu_system.gd             # Menu system
│   └── animation_controller.gd    # UI animation controller
└── utilities/                     # Utility functions and helpers
    └── resource_loader.gd         # Resource loading utilities
```

### Autoload Directory Structure
Global UI management systems are implemented as autoload singletons, following the "Is this state or service truly global and required everywhere?" principle.

```
autoload/
└── ui_manager.gd                  # Global UI management system
```

## Data Conversion Strategy

### Configuration Files (.tbl)
Convert to Godot resources (.tres) organized appropriately:
- Menu definitions from menu.tbl to MenuData resources
- HUD gauge definitions from hud_gauges.tbl to GaugeData resources
- Icon definitions from icons.tbl to IconData resources
- Use Godot's resource system for data-driven design with centralized management
- Preserve UI layout and positioning data with appropriate Godot data types

### Image Conversion Process
1. **PCX/DDS to WebP Converter**: Convert .pcx and .dds image files to WebP format with quality preservation
2. **Palette Preservation**: Maintain color palettes and transparency for accurate display
3. **Resolution Maintenance**: Preserve original resolutions for proper scaling
4. **Resource Generation**: Create Godot .tres files with converted image data
5. **Directory Organization**: Place converted image files in appropriate directories following the structure above
6. **Validation**: Verify converted images maintain original visual quality and properties

### Animation Conversion Process
1. **ANI to Sprite Sheet Converter**: Convert .ani animation files to sprite sheet animations with WebP format
2. **Frame Sequence Preservation**: Maintain animation frame sequences and timing properties
3. **Looping Properties**: Preserve looping and playback characteristics
4. **Resource Generation**: Create Godot .tres files with converted animation data
5. **Directory Organization**: Place converted animation files in appropriate directories following the structure above
6. **Validation**: Verify converted animations maintain original visual characteristics and timing

## Example Mapping

### For Main Hall interface:
- mainhall.tbl entry → /features/ui/main_menu/main_menu.tscn
- mainhall1.pcx → /features/ui/main_menu/background.webp
- 2_mainhall.dds → /features/ui/main_menu/background.webp
- button_normal.pcx → /features/ui/main_menu/buttons/normal/button_normal.webp
- button_hover.pcx → /features/ui/main_menu/buttons/hover/button_hover.webp
- button_click.wav → /features/ui/main_menu/sounds/click.ogg
- 2_mainhall_misc_1.ani → /features/ui/main_menu/animations/background/mainhall_misc_1.webp

### For HUD gauges:
- hud_gauges.tbl entry → /features/ui/hud/player_hud.tscn
- speed_gauge.pcx → /features/ui/hud/gauges/speed/speed_gauge.webp
- shield_indicator.pcx → /features/ui/hud/indicators/shields/shield_indicator.webp
- TargetStatic.ani → /features/ui/hud/animations/warnings/target_static.webp
- warning_sound.wav → /features/ui/hud/sounds/warning.ogg

### For Global UI Assets:
- cursor_hud.pcx → /assets/textures/ui/cursors/cursor_hud.webp
- button_click.wav → /assets/audio/ui/buttons/click.ogg
- menu_transition.wav → /assets/audio/ui/transitions/transition.ogg

## Relationship to Other Assets
UI assets are closely related to:
- **Game State System**: UI elements display and interact with game state information
- **Audio System**: UI sound effects are organized by type and managed by the audio manager
- **Input System**: UI elements respond to player input and navigation
- **Mission System**: Briefing and debriefing screens display mission-specific content
- **Campaign System**: UI text content is organized by campaign
- **UI Manager**: Global UI management system in `/autoload/ui_manager.gd`
- **UI System Scripts**: Reusable UI components and systems in `/scripts/ui/`

This organization follows the hybrid approach where truly global UI assets are organized in the `/assets/` directory following the "Global Litmus Test" principle, while feature-specific UI elements are co-located with their respective features in the `/features/ui/` directory. The structure maintains clear separation of concerns between different UI types while ensuring easy access to all UI assets needed for game features.
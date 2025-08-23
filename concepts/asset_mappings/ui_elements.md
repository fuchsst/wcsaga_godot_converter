# UI Elements Asset Mapping

## Overview
This document maps the UI element definitions from various TBL files to their corresponding media assets in the Wing Commander Saga Hermes campaign.

## Asset Types

### Interface Graphics (.pcx)
Various TBL files reference PCX interface graphics:
- Mainhall.tbl - Main hall interface graphics
- HUD_gauges.tbl - HUD gauge graphics
- Icons.tbl - Icon graphics for ships/weapons
- Fonts.tbl - Font character set graphics
- Menu.tbl - Menu background and element graphics
- Briefing.tbl - Briefing screen graphics
- Debriefing.tbl - Debriefing screen graphics

Common UI graphics include:
- Button backgrounds and states
- Gauge faces and needles
- Progress bars and sliders
- Window borders and backgrounds
- Icon sets for ships, weapons, and systems
- Font character sets
- Cursor graphics
- Loading screen graphics

### Animation Effects (.ani)
UI animations referenced in various TBL files:
- Mainhall.tbl - Main hall animation sequences
- HUD animations for dynamic elements
- Menu transition animations
- Briefing/debriefing screen animations
- Loading screen animations

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

## Target Structure
```
/ui/                                # User interface directory
├── main_menu/                      # Main menu interface
│   ├── main_menu.tscn              # Main menu scene
│   ├── main_menu.gd                # Main menu script
│   ├── background.png              # Background graphic
│   ├── buttons/                    # Button graphics
│   │   ├── normal/
│   │   ├── hover/
│   │   └── pressed/
│   ├── animations/                 # Menu animations
│   │   ├── transitions/
│   │   └── background/
│   └── sounds/                     # Menu sounds
│       ├── click.ogg
│       ├── hover.ogg
│       └── transition.ogg
├── hud/                            # Heads-up display
│   ├── player_hud.tscn             # Player HUD scene
│   ├── player_hud.gd               # Player HUD script
│   ├── gauges/                     # HUD gauge graphics
│   │   ├── speed/
│   │   ├── shields/
│   │   ├── weapons/
│   │   └── fuel/
│   ├── indicators/                 # HUD indicator graphics
│   │   ├── targets/
│   │   ├── warnings/
│   │   └── status/
│   ├── animations/                 # HUD animations
│   │   ├── warnings/
│   │   └── status/
│   └── sounds/                     # HUD sounds
│       ├── warning.ogg
│       ├── target_acquired.ogg
│       └── system_status.ogg
├── briefing/                       # Briefing interface
│   ├── briefing_screen.tscn        # Briefing screen scene
│   ├── briefing_screen.gd          # Briefing screen script
│   ├── background.png              # Background graphic
│   ├── text_display/               # Text display area
│   ├── mission_map/                # Mission map area
│   ├── animations/                 # Briefing animations
│   └── sounds/                     # Briefing sounds
│       ├── voice_playback.ogg
│       └── transition.ogg
├── debriefing/                     # Debriefing interface
│   ├── debriefing_screen.tscn      # Debriefing screen scene
│   ├── debriefing_screen.gd        # Debriefing screen script
│   ├── background.png              # Background graphic
│   ├── results_display/            # Results display area
│   ├── statistics/                 # Statistics display
│   ├── animations/                 # Debriefing animations
│   └── sounds/                     # Debriefing sounds
│       ├── voice_playback.ogg
│       └── transition.ogg
├── options/                        # Options menu
│   ├── options_menu.tscn           # Options menu scene
│   ├── options_menu.gd             # Options menu script
│   ├── backgrounds/                # Background graphics
│   ├── sliders/                    # Slider graphics
│   ├── checkboxes/                 # Checkbox graphics
│   ├── animations/                 # Options animations
│   └── sounds/                     # Options sounds
│       ├── change_setting.ogg
│       └── reset_defaults.ogg
├── tech_database/                  # Technical database
│   ├── tech_database.tscn          # Tech database scene
│   ├── tech_database.gd            # Tech database script
│   ├── backgrounds/                # Background graphics
│   ├── ship_entries/               # Ship entry graphics
│   ├── weapon_entries/             # Weapon entry graphics
│   ├── animations/                 # Database animations
│   └── sounds/                     # Database sounds
│       ├── entry_select.ogg
│       └── page_turn.ogg
└── components/                      # Reusable UI components
    ├── buttons/                     # Button components
    ├── sliders/                     # Slider components
    ├── checkboxes/                  # Checkbox components
    ├── dropdowns/                   # Dropdown components
    ├── text_fields/                 # Text field components
    └── lists/                       # List components

/text/ui/                            # UI text content
├── menus/                           # Menu text
├── hud/                             # HUD text
├── briefing/                        # Briefing text
├── debriefing/                      # Debriefing text
├── options/                         # Options text
├── help/                            # Help text
└── tutorials/                       # Tutorial text

/audio/sfx/ui/                       # UI sound effects
├── buttons/                         # Button sounds
├── menus/                           # Menu sounds
├── hud/                             # HUD sounds
├── notifications/                   # Notification sounds
└── transitions/                     # Transition sounds

/textures/ui/                        # UI graphics textures
├── backgrounds/                     # Background graphics
├── buttons/                         # Button graphics
├── gauges/                          # Gauge graphics
├── indicators/                      # Indicator graphics
├── icons/                           # Icon graphics
├── fonts/                           # Font graphics
├── cursors/                         # Cursor graphics
└── animations/                      # UI animation frames

/animations/ui/                      # UI animations
├── transitions/                     # Screen transitions
├── buttons/                         # Button animations
├── gauges/                          # Gauge animations
├── indicators/                      # Indicator animations
└── menus/                           # Menu animations
```

## Example Mapping
For Main Hall interface:
- mainhall.tbl entry → /ui/main_menu/main_menu.tscn
- mainhall_background.pcx → /ui/main_menu/background.png
- button_normal.pcx → /ui/main_menu/buttons/normal/button_normal.png
- button_hover.pcx → /ui/main_menu/buttons/hover/button_hover.png
- button_click.wav → /ui/main_menu/sounds/click.ogg
- mainhall_animation.ani → /animations/ui/menus/mainhall/mainhall_*.png

For HUD gauges:
- hud_gauges.tbl entry → /ui/hud/player_hud.tscn
- speed_gauge.pcx → /ui/hud/gauges/speed/speed_gauge.png
- shield_indicator.pcx → /ui/hud/indicators/shields/shield_indicator.png
- warning_flash.ani → /animations/ui/hud/warnings/warning_flash_*.png
- warning_sound.wav → /ui/hud/sounds/warning.ogg
# EPIC-006: Menu & Navigation System - Godot Files Structure

**Document Version**: 1.0  
**Date**: 2025-01-27  
**Architect**: Mo (Godot Architect)  
**Epic**: EPIC-006 - Menu & Navigation System  
**System**: Main menus, briefing screens, pilot management, navigation UI  
**Status**: READY FOR IMPLEMENTATION  

---

## Godot Project File Structure

### Core Menu Management System
```
target/
├── addons/
│   └── wcs_menu_system/               # Menu system addon (optional)
│       ├── plugin.cfg
│       ├── plugin.gd
│       └── components/
│           ├── responsive_layout.gd
│           ├── menu_animations.gd
│           └── transition_effects.gd
├── scenes/
│   ├── menus/                         # Main menu scenes
│   │   ├── main_menu/                 # Main menu system
│   │   │   ├── main_menu.tscn         # Primary main menu scene
│   │   │   ├── main_menu.gd           # Main menu controller
│   │   │   ├── main_hall_background.tscn  # Animated background
│   │   │   ├── main_hall_background.gd    # Background controller
│   │   │   ├── campaign_selection.tscn    # Campaign browser
│   │   │   ├── campaign_selection.gd      # Campaign selection logic
│   │   │   ├── credits_system.tscn        # Credits display
│   │   │   └── credits_system.gd          # Credits controller
│   │   ├── pilot_management/          # Pilot system
│   │   │   ├── pilot_selection.tscn   # Pilot selection interface
│   │   │   ├── pilot_selection.gd     # Pilot selection controller
│   │   │   ├── pilot_creation.tscn    # New pilot creation
│   │   │   ├── pilot_creation.gd      # Creation form controller
│   │   │   ├── statistics_display.tscn    # Pilot stats viewer
│   │   │   ├── statistics_display.gd      # Stats display controller
│   │   │   ├── progression_tracker.tscn   # Career progression
│   │   │   └── progression_tracker.gd     # Progression controller
│   │   ├── mission_flow/              # Mission briefing/debriefing
│   │   │   ├── mission_briefing.tscn  # Pre-mission briefing
│   │   │   ├── mission_briefing.gd    # Briefing controller
│   │   │   ├── ship_selection.tscn    # Ship and loadout selection
│   │   │   ├── ship_selection.gd      # Ship selection controller
│   │   │   ├── mission_debrief.tscn   # Post-mission results
│   │   │   ├── mission_debrief.gd     # Debrief controller
│   │   │   ├── objective_display.tscn # Mission objectives
│   │   │   └── objective_display.gd   # Objective tracker
│   │   ├── options/                   # Settings and configuration
│   │   │   ├── options_main.tscn      # Main options interface
│   │   │   ├── options_main.gd        # Options coordinator
│   │   │   ├── graphics_options.tscn  # Graphics settings
│   │   │   ├── graphics_options.gd    # Graphics controller
│   │   │   ├── audio_options.tscn     # Audio configuration
│   │   │   ├── audio_options.gd       # Audio controller
│   │   │   ├── controls_options.tscn  # Input mapping
│   │   │   ├── controls_options.gd    # Controls controller
│   │   │   ├── gameplay_options.tscn  # Gameplay preferences
│   │   │   └── gameplay_options.gd    # Gameplay controller
│   │   └── shared_components/         # Reusable UI components
│   │       ├── menu_button.tscn       # Standardized button
│   │       ├── menu_button.gd         # Button controller
│   │       ├── dialog_box.tscn        # Modal dialog system
│   │       ├── dialog_box.gd          # Dialog controller
│   │       ├── loading_screen.tscn    # Loading screen
│   │       ├── loading_screen.gd      # Loading controller
│   │       ├── transition_effects.tscn    # Screen transitions
│   │       └── transition_effects.gd      # Transition controller
│   └── ui/                            # Additional UI components
│       ├── themes/                    # UI themes
│       │   ├── wcs_main_theme.tres    # Main WCS theme
│       │   ├── wcs_button_styles.tres # Button style variations
│       │   └── wcs_panel_styles.tres  # Panel style variations
│       └── layouts/                   # Responsive layouts
│           ├── standard_layout.tscn   # 1920x1080+ layout
│           ├── compact_layout.tscn    # <1280 width layout
│           └── ultra_wide_layout.tscn # Ultra-wide support
├── scripts/
│   ├── menu_system/                   # Core menu system scripts
│   │   ├── core_navigation/           # Navigation management
│   │   │   ├── menu_manager.gd        # Central navigation coordination
│   │   │   ├── scene_transition_manager.gd  # Scene transitions
│   │   │   ├── navigation_stack.gd    # Menu history management
│   │   │   └── loading_manager.gd     # Loading screen coordination
│   │   ├── data_management/           # Data handling
│   │   │   ├── pilot_manager.gd       # Pilot operations
│   │   │   ├── options_manager.gd     # Settings persistence
│   │   │   ├── save_game_manager.gd   # Save/load operations
│   │   │   └── session_manager.gd     # Session state management
│   │   ├── ui_framework/              # UI framework components
│   │   │   ├── ui_theme_manager.gd    # Theme management
│   │   │   ├── responsive_layout.gd   # Responsive design system
│   │   │   ├── menu_animations.gd     # Animation system
│   │   │   └── accessibility_manager.gd   # Accessibility features
│   │   └── performance/               # Performance optimization
│   │       ├── menu_preloader.gd      # Menu preloading system
│   │       ├── resource_cache.gd      # Resource caching
│   │       └── memory_manager.gd      # Memory optimization
│   ├── data_structures/               # Data classes and resources
│   │   ├── pilot_profile.gd           # Pilot data structure
│   │   ├── game_settings.gd           # Settings data structure
│   │   ├── menu_state.gd              # Menu state container
│   │   ├── campaign_data.gd           # Campaign information
│   │   ├── mission_data.gd            # Mission information
│   │   └── validation_result.gd       # Validation response structure
│   └── autoloads/                     # Global singletons
│       ├── menu_system_autoload.gd    # Menu system singleton (if needed)
│       └── ui_sound_manager.gd        # UI sound effects manager
├── resources/
│   ├── pilot_profiles/                # Pilot data resources
│   │   ├── default_pilot.tres         # Default pilot template
│   │   └── pilot_template.tres        # New pilot template
│   ├── game_settings/                 # Settings resources
│   │   ├── default_settings.tres      # Default game settings
│   │   ├── graphics_presets.tres      # Graphics quality presets
│   │   └── control_schemes.tres       # Input control schemes
│   ├── campaigns/                     # Campaign data
│   │   ├── main_campaign.tres         # Main WCS campaign
│   │   ├── campaign_metadata.tres     # Campaign descriptions
│   │   └── mission_definitions.tres   # Mission metadata
│   └── ui_data/                       # UI configuration
│       ├── menu_layouts.tres          # Menu layout definitions
│       ├── transition_configs.tres    # Transition configurations
│       └── accessibility_configs.tres # Accessibility settings
├── assets/
│   ├── textures/
│   │   ├── ui/                        # UI textures
│   │   │   ├── buttons/               # Button graphics
│   │   │   │   ├── button_normal.png
│   │   │   │   ├── button_hover.png
│   │   │   │   ├── button_pressed.png
│   │   │   │   └── button_disabled.png
│   │   │   ├── panels/                # Panel backgrounds
│   │   │   │   ├── menu_panel.png
│   │   │   │   ├── dialog_panel.png
│   │   │   │   └── info_panel.png
│   │   │   ├── icons/                 # Menu icons
│   │   │   │   ├── pilot_icon.png
│   │   │   │   ├── campaign_icon.png
│   │   │   │   ├── options_icon.png
│   │   │   │   └── exit_icon.png
│   │   │   └── backgrounds/           # Menu backgrounds
│   │   │       ├── main_hall_bg.jpg
│   │   │       ├── space_bg.jpg
│   │   │       └── briefing_bg.jpg
│   │   └── ships/                     # Ship images for selection
│   │       ├── ship_thumbnails/       # Small ship images
│   │       └── ship_detail/           # Detailed ship views
│   ├── fonts/                         # Typography
│   │   ├── wcs_main_font.ttf          # Main UI font
│   │   ├── wcs_title_font.ttf         # Title font
│   │   └── wcs_mono_font.ttf          # Monospace font
│   ├── audio/                         # Menu audio
│   │   ├── ui_sounds/                 # UI sound effects
│   │   │   ├── button_click.ogg
│   │   │   ├── button_hover.ogg
│   │   │   ├── menu_transition.ogg
│   │   │   ├── dialog_open.ogg
│   │   │   └── dialog_close.ogg
│   │   └── music/                     # Menu music
│   │       ├── main_menu_theme.ogg
│   │       ├── briefing_music.ogg
│   │       └── credits_music.ogg
│   └── animations/                    # UI animations
│       ├── transitions/               # Scene transition animations
│       │   ├── fade_transition.tres
│       │   ├── slide_transition.tres
│       │   └── dissolve_transition.tres
│       └── ui_effects/                # UI animation effects
│           ├── button_press.tres
│           ├── panel_slide.tres
│           └── text_fade.tres
└── tests/
    ├── unit/                          # Unit tests
    │   ├── test_menu_manager.gd       # Menu manager tests
    │   ├── test_pilot_manager.gd      # Pilot management tests
    │   ├── test_scene_transitions.gd  # Transition tests
    │   ├── test_options_manager.gd    # Settings tests
    │   └── test_navigation_stack.gd   # Navigation tests
    ├── integration/                   # Integration tests
    │   ├── test_menu_flow.gd          # Complete menu flow tests
    │   ├── test_pilot_workflow.gd     # Pilot creation workflow
    │   ├── test_campaign_selection.gd # Campaign selection flow
    │   └── test_settings_persistence.gd   # Settings save/load
    └── performance/                   # Performance tests
        ├── test_menu_loading.gd       # Menu loading performance
        ├── test_transition_speed.gd   # Transition performance
        └── test_memory_usage.gd       # Memory usage validation
```

---

## Implementation Priority

### Phase 1: Core Navigation Framework (Week 1)
**Essential Files for Basic Menu System**:
```
scripts/menu_system/core_navigation/
├── menu_manager.gd                    # CRITICAL - Central coordination
├── scene_transition_manager.gd        # CRITICAL - Scene management
├── navigation_stack.gd                # HIGH - Menu history
└── loading_manager.gd                 # HIGH - Loading screens

scripts/data_structures/
├── menu_state.gd                      # CRITICAL - State management
├── pilot_profile.gd                   # HIGH - Pilot data
└── game_settings.gd                   # HIGH - Settings data

scenes/menus/main_menu/
├── main_menu.tscn                     # CRITICAL - Entry point
└── main_menu.gd                       # CRITICAL - Main controller
```

### Phase 2: Pilot Management (Week 2)
**Pilot System Implementation**:
```
scenes/menus/pilot_management/
├── pilot_selection.tscn               # HIGH - Pilot interface
├── pilot_selection.gd                 # HIGH - Selection logic
├── pilot_creation.tscn                # MEDIUM - New pilot form
└── pilot_creation.gd                  # MEDIUM - Creation controller

scripts/menu_system/data_management/
├── pilot_manager.gd                   # HIGH - Pilot operations
├── options_manager.gd                 # HIGH - Settings handling
└── save_game_manager.gd               # HIGH - Save/load system
```

### Phase 3: UI Framework & Polish (Week 3)
**Enhanced UI Components**:
```
scripts/menu_system/ui_framework/
├── ui_theme_manager.gd                # MEDIUM - Theme system
├── responsive_layout.gd               # MEDIUM - Responsive design
├── menu_animations.gd                 # LOW - Animation polish
└── accessibility_manager.gd           # LOW - Accessibility

scenes/menus/shared_components/
├── menu_button.tscn                   # MEDIUM - Reusable button
├── dialog_box.tscn                    # MEDIUM - Modal dialogs
└── loading_screen.tscn                # HIGH - Loading interface
```

### Phase 4: Mission Flow Integration (Week 4)
**Mission System Connection**:
```
scenes/menus/mission_flow/
├── mission_briefing.tscn              # HIGH - Mission preparation
├── ship_selection.tscn                # HIGH - Ship/loadout choice
├── mission_debrief.tscn               # MEDIUM - Post-mission
└── objective_display.tscn             # MEDIUM - Objective tracking
```

---

## File Size & Performance Estimates

### Scene File Sizes
```
main_menu.tscn                 ~15KB   # Complex main interface
pilot_selection.tscn           ~12KB   # Pilot management UI
mission_briefing.tscn          ~20KB   # Rich briefing interface
ship_selection.tscn            ~18KB   # 3D ship viewer + UI
options_main.tscn              ~10KB   # Settings interface
dialog_box.tscn                ~5KB    # Modal dialog template
loading_screen.tscn            ~8KB    # Loading with progress
```

### Script File Sizes
```
menu_manager.gd                ~8KB    # Central coordination logic
scene_transition_manager.gd    ~6KB    # Scene loading/unloading
pilot_manager.gd               ~12KB   # Pilot CRUD operations
options_manager.gd             ~10KB   # Settings persistence
navigation_stack.gd            ~4KB    # Simple stack management
ui_theme_manager.gd            ~6KB    # Theme application
menu_animations.gd             ~8KB    # Animation utilities
```

### Resource File Sizes
```
wcs_main_theme.tres            ~5KB    # UI theme definition
default_pilot.tres             ~2KB    # Pilot template
default_settings.tres          ~3KB    # Settings template
campaign_metadata.tres         ~8KB    # Campaign information
control_schemes.tres           ~4KB    # Input configurations
```

### Asset Estimates
```
UI Textures:                   ~15MB   # Buttons, panels, icons
Menu Backgrounds:              ~25MB   # High-quality backgrounds
Fonts:                         ~2MB    # TTF font files
UI Audio:                      ~5MB    # Sound effects, short clips
Menu Music:                    ~20MB   # Background music tracks
Ship Images:                   ~30MB   # Ship thumbnails and details
```

**Total Estimated Size**: ~97MB for complete menu system

---

## Performance Targets

### Loading Performance
```
Main Menu Load Time:           <2 seconds   # From startup to main menu
Scene Transition Time:         <1 second    # Between menu screens
Pilot Selection Load:          <1.5 seconds # Loading pilot list
Settings Load/Save:            <0.5 seconds # Settings persistence
Memory Usage (Menus):          <100MB       # Total menu memory footprint
```

### Runtime Performance
```
UI Response Time:              <50ms        # Button press to response
Animation Frame Rate:          60 FPS       # Smooth UI animations
Scene Transition FPS:          60 FPS       # Smooth transitions
Memory Cleanup:                <5 seconds   # Cleanup unused scenes
```

---

## Development Tools & Testing

### Required Godot Tools
```
Scene Editor:                  # Visual scene composition
Script Editor:                 # GDScript development
Theme Editor:                  # UI theme creation
Animation Timeline:            # UI animations
Profiler:                      # Performance monitoring
Debugger:                      # Runtime debugging
```

### Testing Framework Integration
```
GUT Framework:                 # Unit testing for GDScript
Scene Testing:                 # Automated scene testing
Performance Profiling:        # Memory and CPU profiling
UI Testing:                    # User interface testing
Integration Testing:           # Cross-system testing
```

---

## File Dependencies Summary

### Critical Dependencies (Must Implement First)
1. `menu_manager.gd` - Central coordination (depends on: GameStateManager)
2. `scene_transition_manager.gd` - Scene management (depends on: ResourceLoader)
3. `pilot_profile.gd` - Data structure (depends on: Resource system)
4. `main_menu.tscn` - Entry point (depends on: UI theme)

### Integration Dependencies
1. **EPIC-007**: GameStateManager for state coordination
2. **EPIC-001**: Core foundation classes and utilities
3. **EPIC-004**: SEXP system for mission briefing integration
4. **EPIC-002**: Asset loading and resource management

### Optional Dependencies
1. **EPIC-005**: GFRED2 integration for mission editing
2. **Performance Tools**: Profiling and optimization tools
3. **Accessibility**: Screen reader and keyboard navigation support

---

**File Structure Status**: ✅ **COMPREHENSIVE & IMPLEMENTATION-READY**  
**Estimated Implementation Time**: 4 weeks (1 developer)  
**Complexity Level**: MEDIUM-HIGH (Rich UI system with many components)  
**Risk Level**: LOW (Well-understood UI development patterns)
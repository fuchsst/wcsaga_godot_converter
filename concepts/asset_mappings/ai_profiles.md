# AI Profiles Asset Mapping

## Overview
This document maps the AI profile definitions from ai_profiles.tbl to their corresponding behavioral assets in the Wing Commander Saga Hermes campaign.

## Asset Types

### AI Behavior Definitions (.tbl)
AI_profiles.tbl defines different AI behavior profiles:
- Aggressive - High aggression, low caution
- Cowardly - Low aggression, high caution
- Intelligent - Balanced with smart tactics
- Random - Unpredictable behavior patterns
- Evasive - Prioritizes avoidance over engagement
- Hunter - Focuses on taking down enemies systematically
- Bomber - Specialized for bombing runs
- Escort - Protective of assigned charges
- Patroller - Regular patrol patterns
- Sentry - Stationary defensive positioning

Each AI profile contains parameters:
- Aggression level (0-100)
- Courage level (0-100)
- Caution level (0-100)
- Accuracy modifiers
- Tactical preference weights
- Formation flying behavior
- Evasion patterns
- Target selection priorities
- Weapon usage preferences
- Communication behavior

### AI Script Logic (.tbl)
ai.tbl contains AI scripting logic:
- Decision trees for tactical choices
- Conditional behavior triggers
- Formation flying algorithms
- Combat maneuver libraries
- Evasion technique catalogs
- Target acquisition patterns
- Weapon selection logic
- Communication protocols
- Mission role behaviors
- Special circumstance responses

### AI Sound Effects (.wav)
AI-related audio files:
- Combat chatter during engagements
- Formation commands and acknowledgments
- Distress calls when damaged
- Victory declarations after kills
- Request for assistance
- Status reports to command
- Pilot personality lines
- Species-specific vocalizations
- Weapon callouts and warnings
- Environmental awareness comments

### AI Voice Acting (.wav)
Character-specific AI voices:
- Species-appropriate vocalizations
- Personality-specific speech patterns
- Role-appropriate communication styles
- Situation-specific dialogue variations
- Command hierarchy voice differences
- Skill level vocal variations
- Faction-specific terminology
- Mission context dialogue

## Target Structure
```
/data/ai/                            # AI data definitions
├── profiles/                        # AI behavior profiles
│   ├── aggressive.tres             # Aggressive profile
│   ├── cowardly.tres               # Cowardly profile
│   ├── intelligent.tres            # Intelligent profile
│   ├── random.tres                 # Random profile
│   ├── evasive.tres                # Evasive profile
│   ├── hunter.tres                 # Hunter profile
│   ├── bomber.tres                 # Bomber profile
│   ├── escort.tres                 # Escort profile
│   ├── patroller.tres              # Patroller profile
│   └── sentry.tres                 # Sentry profile
├── behaviors/                       # AI behavior definitions
│   ├── combat/                      # Combat behaviors
│   │   ├── offensive.tres           # Offensive tactics
│   │   ├── defensive.tres           # Defensive tactics
│   │   ├── evasive.tres             # Evasive maneuvers
│   │   └── aggressive.tres          # Aggressive attacks
│   ├── navigation/                  # Navigation behaviors
│   │   ├── patrolling.tres          # Patrol patterns
│   │   ├── escorting.tres           # Escort behaviors
│   │   ├── intercepting.tres        # Intercept behaviors
│   │   └── fleeing.tres             # Flee behaviors
│   └── communication/               # Communication behaviors
│       ├── chatter.tres             # Combat chatter
│       ├── commands.tres            # Command issuance
│       ├── acknowledgments.tres     # Response acknowledgment
│       └── distress_calls.tres      # Distress communication
├── tactics/                         # Tactical decision trees
│   ├── formations/                  # Formation flying
│   │   ├── v_shape.tres             # V-shaped formation
│   │   ├── line_abreast.tres        # Line abreast formation
│   │   ├── echelon.tres             # Echelon formation
│   │   └── diamond.tres             # Diamond formation
│   ├── combat_manuevers/            # Combat maneuvers
│   │   ├── strafing_runs.tres       # Strafing attack runs
│   │   ├── bombing_runs.tres        # Bombing attack runs
│   │   ├── dogfighting.tres         # Dogfighting patterns
│   │   └── evasive_action.tres      # Evasive actions
│   └── target_selection/            # Target selection logic
│       ├── priority.tres            # Priority-based selection
│       ├── threat_level.tres        # Threat-based selection
│       ├── weapon_type.tres         # Weapon-based selection
│       └── random.tres              # Random selection
├── formations/                      # Formation definitions
│   ├── wing_formations/             # Wing-level formations
│   ├── squadron_formations/         # Squadron formations
│   ├── group_formations/            # Group formations
│   └── fleet_formations/            # Fleet formations
└── goals/                           # AI goals and objectives
    ├── mission_goals/               # Mission-specific goals
    ├── tactical_goals/              # Tactical situation goals
    ├── survival_goals/              # Survival-based goals
    └── strategic_goals/             # Strategic mission goals

/audio/sfx/ai/                       # AI sound effects directory
├── combat/                          # Combat-related sounds
│   ├── chatter/                     # Combat chatter
│   │   ├── attacking/
│   │   ├── defending/
│   │   ├── pursuing/
│   │   └── evading/
│   ├── commands/                    # Command issuance
│   │   ├── formation/
│   │   ├── attack/
│   │   ├── retreat/
│   │   └── regroup/
│   ├── acknowledgments/             # Response sounds
│   │   ├── affirmative/
│   │   ├── negative/
│   │   ├── confused/
│   │   └── busy/
│   └── status_reports/              # Status updates
│       ├── damage/
│       ├── weapons/
│       ├── fuel/
│       └── position/
├── communication/                   # Communication sounds
│   ├── distress_calls/              # Emergency calls
│   │   ├── requesting_help/
│   │   ├── under_attack/
│   │   ├── critical_damage/
│   │   └── abandoning_ship/
│   ├── victory_calls/               # Victory declarations
│   │   ├── enemy_destroyed/
│   │   ├── mission_success/
│   │   ├── objective_complete/
│   │   └── wave_cleared/
│   ├── personality_lines/           # Character-specific lines
│   │   ├── humorous/
│   │   ├── serious/
│   │   ├── sarcastic/
│   │   └── professional/
│   └── environmental_awareness/     # Environmental comments
│       ├── asteroid_field/
│       ├── nebula_detected/
│       ├── jump_point_found/
│       └── sensor_contact/
└── species_specific/                # Species-specific sounds
    ├── terran/                      # Terran AI sounds
    │   ├── english/
    │   ├── german/
    │   └── french/
    ├── kilrathi/                    # Kilrathi AI sounds
    │   ├── standard/
    │   ├── noble/
    │   └── warrior/
    └── pirate/                      # Pirate AI sounds
        ├── rough/
        ├── educated/
        └── military/

/audio/voice/ai/                     # AI voice acting directory
├── terran/                          # Terran AI voices
│   ├── pilots/                      # Pilot voices
│   │   ├── male/
│   │   ├── female/
│   │   └── gender_neutral/
│   ├── commanders/                  # Command voices
│   │   ├── military/
│   │   ├── civilian/
│   │   └── diplomatic/
│   └── specialists/                 # Specialist voices
│       ├── engineer/
│       ├── medic/
│       └── scientist/
├── kilrathi/                        # Kilrathi AI voices
│   ├── pilots/                      # Pilot voices
│   │   ├── warrior/
│   │   ├── noble/
│   │   └── cunning/
│   ├── commanders/                  # Command voices
│   │   ├── imperial/
│   │   ├── clan/
│   │   └── war_party/
│   └── specialists/                 # Specialist voices
│       ├── shaman/
│       ├── technician/
│       └── elder/
└── pirate/                          # Pirate AI voices
    ├── pilots/                      # Pilot voices
    │   ├── rough/
    │   ├── educated/
    │   └── military_defector/
    ├── commanders/                  # Command voices
    │   ├── captain/
    │   ├── admiral/
    │   └── warlord/
    └── specialists/                 # Specialist voices
        ├── engineer/
        ├── hacker/
        └── mercenary/

/systems/ai/                         # AI system components
├── behavior_controller.gd           # AI behavior controller script
├── decision_maker.gd                # AI decision-making system
├── tactical_analyzer.gd             # Tactical situation analysis
├── target_selector.gd               # Target selection system
├── formation_manager.gd             # Formation flying manager
├── communication_handler.gd         # AI communication system
├── personality_engine.gd            # AI personality system
└── profile_manager.gd               # AI profile management system
```

## Example Mapping
For Aggressive AI profile:
- ai_profiles.tbl entry → /data/ai/profiles/aggressive.tres
- aggression parameter (85) → aggression_level = 85 in resource
- courage parameter (90) → courage_level = 90 in resource
- caution parameter (20) → caution_level = 20 in resource
- accuracy modifier (+10%) → accuracy_bonus = 0.10 in resource
- combat_chatter.wav → /audio/sfx/ai/combat/chatter/attacking/combat_chatter.ogg
- aggressive_voice.wav → /audio/voice/ai/terran/pilots/male/aggressive_voice.ogg
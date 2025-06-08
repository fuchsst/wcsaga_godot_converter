# WCS Ship Lifecycle and State Management Analysis

## Overview

This document provides a comprehensive analysis of how Wing Commander Saga manages ship lifecycle events, state transitions, and the complex flag-based state system that tracks ships from creation through destruction or departure.

## 1. Ship State Flags and Their Meanings

### Primary Ship Flags (SF_*)

WCS uses an extensive bitfield system to track ship states. The flags are organized into two categories:

#### Mission-Savable Flags (Low Bits 0-7)
These flags are saved with mission files and affect mission logic:

```cpp
#define SF_IGNORE_COUNT         (1 << 0)    // ignore ship when counting for goals
#define SF_REINFORCEMENT        (1 << 1)    // this ship is a reinforcement
#define SF_ESCORT               (1 << 2)    // this ship is an escort
#define SF_NO_ARRIVAL_MUSIC     (1 << 3)    // don't play arrival music
#define SF_NO_ARRIVAL_WARP      (1 << 4)    // no arrival warp effect
#define SF_NO_DEPARTURE_WARP    (1 << 5)    // no departure warp effect
#define SF_LOCKED               (1 << 6)    // can't manipulate in loadout
```

#### Runtime State Flags (High Bits 8-31)
These flags track dynamic ship states during gameplay:

```cpp
#define SF_VAPORIZE             (1<<8)      // vaporized by beam weapon
#define SF_RED_ALERT_STORE_STATUS (1 << 9)  // save/restore status in red alert
#define SF_SHIP_HAS_SCREAMED    (1 << 10)   // ship death scream played
#define SF_EXPLODED             (1 << 11)   // ship has exploded
#define SF_WARPED_SUPPORT       (1 << 12)   // auto-warped support ship
#define SF_SCANNABLE            (1 << 13)   // can be scanned
#define SF_HIDDEN_FROM_SENSORS  (1 << 14)   // doesn't show on sensors
#define SF_AMMO_COUNT_RECORDED  (1 << 15)   // initial ammo recorded
#define SF_TRIGGER_DOWN         (1 << 16)   // trigger held down
#define SF_WARP_NEVER           (1 << 17)   // ship can never warp
#define SF_WARP_BROKEN          (1 << 18)   // warp drive broken but repairable
#define SF_SECONDARY_DUAL_FIRE  (1 << 19)   // firing dual missiles
#define SF_PRIMARY_LINKED       (1 << 20)   // primary weapons linked
#define SF_FROM_PLAYER_WING     (1 << 21)   // from player starting wing
#define SF_CARGO_REVEALED       (1 << 22)   // cargo revealed to friendlies
#define SF_DOCK_LEADER          (1 << 23)   // in charge of docked group
#define SF_ENGINES_ON           (1 << 24)   // engine sounds should play
#define SF_ARRIVING_STAGE_2     (1 << 25)   // warp-in effect stage 2
#define SF_ARRIVING_STAGE_1     (1 << 26)   // warp-in effect stage 1  
#define SF_DEPART_DOCKBAY       (1 << 27)   // departing via docking bay
#define SF_DEPART_WARP          (1 << 28)   // departing via warp-out
#define SF_DISABLED             (1 << 29)   // ship is disabled
#define SF_DYING                (1 << 30)   // ship is in death sequence
#define SF_KILL_BEFORE_MISSION  (1 << 31)   // kill before mission starts
```

#### Composite Flags
```cpp
#define SF_ARRIVING         (SF_ARRIVING_STAGE_1|SF_ARRIVING_STAGE_2)
#define SF_DEPARTING        (SF_DEPART_WARP | SF_DEPART_DOCKBAY)
#define SF_CANNOT_WARP      (SF_WARP_BROKEN | SF_WARP_NEVER | SF_DISABLED)
```

### Secondary Ship Flags (SF2_*)

Additional behavioral and capability flags:

```cpp
#define SF2_PRIMITIVE_SENSORS           (1<<0)   // primitive sensor display
#define SF2_FRIENDLY_STEALTH_INVIS      (1<<1)   // stealth invisible to friendlies
#define SF2_STEALTH                     (1<<2)   // ship has stealth capability
#define SF2_DONT_COLLIDE_INVIS          (1<<3)   // don't collide when invisible
#define SF2_NO_SUBSPACE_DRIVE           (1<<4)   // no subspace drive
#define SF2_NAVPOINT_CARRY              (1<<5)   // autopilot with player
#define SF2_AFFECTED_BY_GRAVITY         (1<<6)   // affected by gravity
#define SF2_TOGGLE_SUBSYSTEM_SCANNING   (1<<7)   // toggle subsys scanning
#define SF2_NO_BUILTIN_MESSAGES         (1<<8)   // no built-in messages
#define SF2_PRIMARIES_LOCKED            (1<<9)   // can't fire primaries
#define SF2_SECONDARIES_LOCKED          (1<<10)  // can't fire secondaries
#define SF2_GLOWMAPS_DISABLED           (1<<11)  // disable glow maps
#define SF2_NO_DEATH_SCREAM             (1<<12)  // no death scream (WCS specific)
#define SF2_ALWAYS_DEATH_SCREAM         (1<<13)  // always death scream (WCS specific)
#define SF2_NAVPOINT_NEEDSLINK          (1<<14)  // needs linking for autopilot
#define SF2_HIDE_SHIP_NAME              (1<<15)  // hide ship name on HUD
#define SF2_AFTERBURNER_LOCKED          (1<<16)  // can't use afterburners
#define SF2_SET_CLASS_DYNAMICALLY       (1<<18)  // assign class dynamically
#define SF2_LOCK_ALL_TURRETS_INITIALLY  (1<<19)  // lock turrets at start
#define SF2_FORCE_SHIELDS_ON            (1<<20)  // force shields active
#define SF2_HIDE_LOG_ENTRIES            (1<<21)  // hide log entries
#define SF2_NO_ARRIVAL_LOG              (1<<22)  // no arrival log
#define SF2_NO_DEPARTURE_LOG            (1<<23)  // no departure log
#define SF2_IS_HARMLESS                 (1<<24)  // considered harmless
```

## 2. Ship Lifecycle Events

### Creation Process

Ships are created through `ship_create()` function with these steps:

1. **Validation**: Check ship limits (MAX_SHIPS for FRED, SHIPS_LIMIT for gameplay)
2. **Slot Allocation**: Find free ship slot in Ships[] array
3. **Model Loading**: Load 3D model and subsystems from POF file
4. **Object Creation**: Create underlying object with OBJ_SHIP type
5. **Initialization**: Set up default systems, weapons, subsystems
6. **Registration**: Add to ship object list for tracking

```cpp
int ship_create(matrix* orient, vec3d* pos, int ship_type, char* ship_name)
```

Key initialization includes:
- Physics object setup
- Subsystem creation and linking
- Weapon bank configuration
- Shield and hull strength assignment
- Team/IFF assignment

### Arrival Sequence

Ships arriving in missions go through a multi-stage process:

1. **Pre-Arrival**: Ship exists in mission but not yet active
2. **Arrival Trigger**: Arrival cue condition met
3. **Stage 1 Arrival** (`SF_ARRIVING_STAGE_1`): Begin warp-in effect
4. **Stage 2 Arrival** (`SF_ARRIVING_STAGE_2`): Complete warp-in effect  
5. **Active State**: Ship fully operational in mission

Arrival configuration fields:
```cpp
int arrival_location;     // where ship arrives
int arrival_distance;     // distance from anchor
int arrival_anchor;       // object to arrive near
int arrival_path_mask;    // docking bay path restrictions
int arrival_cue;          // trigger condition
int arrival_delay;        // delay after trigger
```

### Departure Sequence

Ships can depart via multiple methods:

1. **Warp Departure** (`SF_DEPART_WARP`): Standard hyperspace jump
2. **Docking Bay Departure** (`SF_DEPART_DOCKBAY`): Leave via hangar bay
3. **Vanished**: Removed from mission without visible departure

Departure process:
1. **Departure Trigger**: Departure cue condition met
2. **Departure Delay**: Wait specified time
3. **Departure Animation**: Warp-out or bay departure effect
4. **Cleanup**: Remove from active objects, add to exited ships list

Departure configuration fields:
```cpp
int departure_location;   // where ship departs to
int departure_anchor;     // docking bay ship index  
int departure_path_mask;  // bay path restrictions
int departure_cue;        // trigger condition
int departure_delay;      // delay after trigger
```

### Destruction Sequence

Ship destruction follows a complex multi-phase process:

1. **Critical Damage**: Hull strength reaches 0 or critical subsystem destroyed
2. **Death Initiated** (`SF_DYING`): Begin death sequence
3. **Death Roll**: Ship tumbles with disabled controls
4. **Pre-Explosion**: Small explosions and sparks
5. **Main Explosion** (`SF_EXPLODED`): Primary fireball effect
6. **Final Destruction**: Ship object removed
7. **Cleanup**: Add to exited ships with `SEF_DESTROYED` flag

Death sequence timing fields:
```cpp
int death_time;              // time until big fireball
int final_death_time;        // time until fireball starts  
int end_death_time;          // time until fireball ends
int really_final_death_time; // time until ship disappears
vec3d deathroll_rotvel;      // death roll rotation velocity
```

## 3. State Transition Management and Validation

### Transition Rules

WCS enforces strict rules for state transitions:

1. **Arrival States**: Ships can only transition `None → Stage1 → Stage2 → Active`
2. **Departure States**: Ships can only depart from `Active` state
3. **Death States**: Once `SF_DYING` is set, ship cannot return to normal operation
4. **Mutual Exclusions**: Certain flags cannot be set simultaneously

### Validation Functions

Key functions that validate state consistency:

- `ship_cleanup()`: Validates cleanup mode matches ship state
- State transition checks prevent invalid combinations
- Mission loading validates saved ship states

### State Persistence

Ship states are persisted through:

1. **Mission Files**: Low-order flags (0-7) saved with mission
2. **Save Games**: Full ship state including runtime flags
3. **Red Alert**: Special status preservation via `SF_RED_ALERT_STORE_STATUS`
4. **Exited Ships**: Historical record of departed/destroyed ships

## 4. Team/IFF Management and Faction Relationships

### IFF (Identify Friend or Foe) System

WCS uses a sophisticated IFF system to manage faction relationships:

```cpp
typedef struct iff_info {
    char iff_name[NAME_LENGTH];
    int color_index;                      // display color
    int attackee_bitmask;                 // who this IFF attacks
    int attackee_bitmask_all_teams_at_war; // wartime relationships
    int observed_color_index[MAX_IFFS];   // how others see this IFF
    int flags;                           // IFF-specific flags
    int default_parse_flags;             // default ship flags
    int default_parse_flags2;            // default ship flags2
} iff_info;
```

### Team Assignment

Each ship has a team field determining its allegiance:
```cpp
int team;  // HOSTILE, FRIENDLY, UNKNOWN, NEUTRAL, or custom IFF
```

### Relationship Queries

Functions to determine faction relationships:
- `iff_x_attacks_y(team_x, team_y)`: Does team X attack team Y?
- `iff_get_attackee_mask(attacker_team)`: Get bitmask of targets
- `iff_get_color_by_team()`: Get display color for team relationships

### Dynamic Team Changes

Ships can change teams during missions through:
- Mission events/SEXPs
- Capture mechanics
- Betrayal scenarios
- Player defection

## 5. Combat State Tracking and Damage Sequences

### Combat States

Ships track multiple combat-related states:

```cpp
int shield_hits;                    // hits on shield this frame
float total_damage_received;        // cumulative damage
float damage_ship[MAX_DAMAGE_SLOTS]; // damage from each attacker
int damage_ship_id[MAX_DAMAGE_SLOTS]; // attacker signatures
```

### Damage Processing

Damage sequence:
1. **Impact Detection**: Collision system detects hit
2. **Shield Processing**: Apply damage to shields first
3. **Hull Damage**: Overflow damage applied to hull
4. **Subsystem Damage**: Targeted subsystem damage
5. **State Updates**: Update combat flags and tracking
6. **Death Check**: Trigger destruction if hull ≤ 0

### Subsystem States

Each subsystem tracks its own state:
```cpp
typedef struct ship_subsys {
    float current_hits;        // remaining subsystem health
    float max_hits;           // maximum subsystem health
    int flags;               // subsystem-specific flags
    int subsys_guardian_threshold; // damage threshold for protection
    int armor_type_idx;      // armor type for damage calculation
    int disruption_timestamp; // time when disruption ends
} ship_subsys;
```

### Combat State Flags

Specific flags for combat tracking:
- `SF_DISABLED`: Ship systems offline
- `SF_DYING`: In death sequence
- `SF_EXPLODED`: Explosion triggered
- `SF_SHIP_HAS_SCREAMED`: Death scream played

## 6. Mission Integration for Arrival/Departure Cues

### SEXP Integration

Ships integrate with mission scripting through SEXPs (S-Expressions):

- **Arrival Cues**: SEXP conditions that trigger ship arrival
- **Departure Cues**: SEXP conditions that trigger ship departure  
- **Event Triggers**: Ship states can trigger mission events
- **Goal Conditions**: Ship status affects mission objectives

### Mission Event Integration

Ships participate in mission events:
- Arrival messages and music
- Departure notifications  
- Death event triggers
- Goal completion tracking

### Wing Management

Ships can be organized into wings with shared behavior:
```cpp
typedef struct wing {
    char name[NAME_LENGTH];
    int current_count;                    // ships currently in wing
    int ship_index[MAX_SHIPS_PER_WING];   // indices of wing members
    int total_destroyed;                  // destruction count
    int total_departed;                   // departure count
    int arrival_cue;                      // wing arrival condition
    int departure_cue;                    // wing departure condition
    int flags;                           // wing-specific flags
} wing;
```

## 7. Save/Load State Persistence Mechanisms

### Save Game Data

Ship state persistence includes:
- All ship flags (flags and flags2)
- Position and orientation
- Damage states and subsystem health
- Weapon and equipment loadouts
- Combat statistics and kill counts

### Red Alert System

Special persistence for red alert missions:
- `SF_RED_ALERT_STORE_STATUS` flag marks ships for status preservation
- Ship loadouts and damage carried between missions
- Wing composition maintained

### Exited Ship Tracking

Ships that leave missions are tracked in persistent records:
```cpp
typedef struct exited_ship {
    char ship_name[NAME_LENGTH];
    int obj_signature;          // unique ship identifier
    int ship_class;            // ship type
    int team;                  // faction
    int flags;                 // exit circumstances
    fix time;                  // when ship exited
    int hull_strength;         // remaining hull
    float damage_ship[MAX_DAMAGE_SLOTS]; // damage tracking
} exited_ship;
```

Exit flags:
- `SEF_DESTROYED`: Ship was destroyed  
- `SEF_DEPARTED`: Ship departed normally
- `SEF_CARGO_KNOWN`: Cargo was scanned
- `SEF_PLAYER_DELETED`: Removed by player
- `SEF_BEEN_TAGGED`: Ship was tagged
- `SEF_RED_ALERT_CARRY`: Status carried to next mission

## Key Integration Points for Godot Implementation

### 1. State Management System
- Use Godot's signal system for state change notifications
- Implement state machine using Godot's built-in state management
- Use resource system for persistent ship configurations

### 2. Flag-Based Architecture  
- Convert bitfield flags to Godot's flag enumeration system
- Use @export flags for editor visibility
- Implement flag validation in setter functions

### 3. Lifecycle Management
- Use Godot's object lifecycle (_ready, _exit_tree)
- Implement pooling system for ship creation/destruction
- Use autoload singleton for ship registry management

### 4. Team/IFF System
- Implement as resource-based faction system
- Use groups or tags for team identification
- Signal-based relationship change notifications

### 5. Persistence System
- Use Godot's resource save/load system
- Implement custom resource types for ship states
- Use signals for save/load events

This analysis reveals the sophisticated state management system that makes WCS ships feel alive and reactive. The Godot implementation should preserve this complexity while leveraging Godot's modern architecture.
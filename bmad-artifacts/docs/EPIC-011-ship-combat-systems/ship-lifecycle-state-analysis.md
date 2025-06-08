# WCS Ship Lifecycle and State Management Analysis

## Executive Summary

This analysis covers the WCS ship lifecycle and state management systems, focusing on how ships are created, managed throughout their existence, and cleaned up when destroyed or departed. The analysis examines the integration points with mission systems, AI systems, save/load functionality, and the overall object management system.

## Ship State Management Overview

### Core Ship State Flags (SF_*)

WCS uses a comprehensive flag system to track ship states throughout their lifecycle:

#### Mission-Persistent Flags (Low bits 0-7)
```cpp
#define SF_IGNORE_COUNT         (1 << 0)  // ignore this ship when counting ship types for goals
#define SF_REINFORCEMENT        (1 << 1)  // this ship is a reinforcement ship
#define SF_ESCORT              (1 << 2)  // this ship is an escort ship
#define SF_NO_ARRIVAL_MUSIC    (1 << 3)  // don't play arrival music when ship arrives
#define SF_NO_ARRIVAL_WARP     (1 << 4)  // no arrival warp in effect
#define SF_NO_DEPARTURE_WARP   (1 << 5)  // no departure warp in effect
#define SF_LOCKED              (1 << 6)  // can't manipulate ship in loadout screens
```

#### Runtime State Flags (High bits 31-8)
```cpp
#define SF_KILL_BEFORE_MISSION  (1 << 31)  // ship should be killed before mission starts
#define SF_DYING               (1 << 30)   // ship is in death sequence
#define SF_DISABLED            (1 << 29)   // ship is disabled (systems offline)
#define SF_DEPART_WARP         (1 << 28)   // ship is departing via warp-out
#define SF_DEPART_DOCKBAY      (1 << 27)   // ship is departing via docking bay
#define SF_ARRIVING_STAGE_1    (1 << 26)   // ship is arriving - warp in effect, stage 1
#define SF_ARRIVING_STAGE_2    (1 << 25)   // ship is arriving - warp in effect, stage 2
#define SF_ENGINES_ON          (1 << 24)   // engines sound should play if set
#define SF_DOCK_LEADER         (1 << 23)   // this guy is in charge of everybody he's docked to
#define SF_CARGO_REVEALED      (1 << 22)   // ship's cargo is revealed to all friendly ships
#define SF_FROM_PLAYER_WING    (1 << 21)   // set for ships that are members of any player starting wing
#define SF_PRIMARY_LINKED      (1 << 20)   // ships primary weapons are linked together
#define SF_SECONDARY_DUAL_FIRE (1 << 19)   // ship is firing two missiles from current secondary bank
#define SF_WARP_BROKEN         (1 << 18)   // warp drive is not working, but is repairable
#define SF_WARP_NEVER          (1 << 17)   // ship can never warp
#define SF_TRIGGER_DOWN        (1 << 16)   // ship has its "trigger" held down
#define SF_AMMO_COUNT_RECORDED (1 << 15)   // we've recorded initial secondary weapon count
#define SF_HIDDEN_FROM_SENSORS (1 << 14)   // ship doesn't show up on sensors
#define SF_SCANNABLE           (1 << 13)   // ship is "scannable"
#define SF_WARPED_SUPPORT      (1 << 12)   // set when this is a support ship warped in automatically
#define SF_EXPLODED            (1 << 11)   // ship has exploded (needed for kill messages)
#define SF_SHIP_HAS_SCREAMED   (1 << 10)   // ship has let out a death scream
#define SF_RED_ALERT_STORE_STATUS (1 << 9) // ship status should be stored/restored if red alert
#define SF_VAPORIZE            (1 << 8)    // ship is vaporized by beam - alternative death sequence
```

#### Combined State Macros
```cpp
#define SF_ARRIVING            (SF_ARRIVING_STAGE_1|SF_ARRIVING_STAGE_2)
#define SF_DEPARTING           (SF_DEPART_WARP | SF_DEPART_DOCKBAY)
#define SF_CANNOT_WARP         (SF_WARP_BROKEN | SF_WARP_NEVER | SF_DISABLED)
```

### Secondary Ship Flags (SF2_*)

Additional ship state flags for extended functionality:

```cpp
#define SF2_PRIMITIVE_SENSORS          (1<<0)   // primitive sensor display
#define SF2_FRIENDLY_STEALTH_INVIS     (1<<1)   // when stealth, don't appear on radar even if friendly
#define SF2_STEALTH                   (1<<2)   // is this particular ship stealth
#define SF2_DONT_COLLIDE_INVIS        (1<<3)   // is this particular ship don't-collide-invisible
#define SF2_NO_SUBSPACE_DRIVE         (1<<4)   // this ship has no subspace drive
#define SF2_NAVPOINT_CARRY            (1<<5)   // This ship autopilots with the player
#define SF2_AFFECTED_BY_GRAVITY       (1<<6)   // ship affected by gravity points
#define SF2_TOGGLE_SUBSYSTEM_SCANNING (1<<7)   // switch whether subsystems are scanned
#define SF2_NO_BUILTIN_MESSAGES       (1<<8)   // ship should not send built-in messages
#define SF2_PRIMARIES_LOCKED          (1<<9)   // This ship can't fire primary weapons
#define SF2_SECONDARIES_LOCKED        (1<<10)  // This ship can't fire secondary weapons
#define SF2_GLOWMAPS_DISABLED         (1<<11)  // to disable glow maps
#define SF2_NO_DEATH_SCREAM           (1<<12)  // for WCS
#define SF2_ALWAYS_DEATH_SCREAM       (1<<13)  // for WCS
#define SF2_NAVPOINT_NEEDSLINK        (1<<14)  // requires "linking" for autopilot
#define SF2_HIDE_SHIP_NAME            (1<<15)  // Hides the ships name
#define SF2_AFTERBURNER_LOCKED        (1<<16)  // This ship can't use its afterburners
#define SF2_SET_CLASS_DYNAMICALLY     (1<<18)  // ship should have its class assigned dynamically
#define SF2_LOCK_ALL_TURRETS_INITIALLY (1<<19) // Lock all turrets on this ship at mission start
#define SF2_FORCE_SHIELDS_ON          (1<<20)
#define SF2_HIDE_LOG_ENTRIES          (1<<21)
#define SF2_NO_ARRIVAL_LOG            (1<<22)
#define SF2_NO_DEPARTURE_LOG          (1<<23)
#define SF2_IS_HARMLESS               (1<<24)
```

## Ship Lifecycle Events

### 1. Ship Creation (`ship_create`)

The ship creation process is comprehensive and involves multiple subsystems:

```cpp
int ship_create(matrix* orient, vec3d* pos, int ship_type, char* ship_name)
```

**Creation Process:**
1. **Validation and Slot Allocation**
   - Check ship count limits (MAX_SHIPS for Fred, SHIPS_LIMIT for game)
   - Find available ship slot in Ships[] array
   - Validate ship_type against Ship_info[] array

2. **Model and Resource Loading**
   - Load primary POF model: `model_load(sip->pof_file, sip->n_subsystems, &sip->subsystems[0])`
   - Load optional cockpit model if specified
   - Load optional HUD target model if specified
   - Set up detail levels and distance thresholds

3. **Object System Integration**
   - Create object via `obj_create()` with appropriate flags
   - Set collision flags based on SIF_NO_COLLIDE
   - Assign object radius from model

4. **AI System Integration**
   - Get AI slot: `shipp->ai_index = ai_get_slot(n)`
   - Initialize AI object: `init_ai_object(objnum)`
   - Clear ship goals: `ai_clear_ship_goals(&Ai_info[Ships[n].ai_index])`

5. **Ship Name Assignment**
   - Use provided name if valid and unique
   - Generate default name: `sprintf(shipp->ship_name, NOX("%s %d"), Ship_info[ship_type].name, n)`

6. **Weapon and Subsystem Setup**
   - Set default weapons: `ship_set_default_weapons(shipp, sip)`
   - Initialize ship properties: `ship_set(n, objnum, ship_type)`
   - Copy and fix up subsystem references for model paths

7. **Shield System Initialization**
   - Allocate shield integrity array if model has shield mesh
   - Initialize all shield triangles to full strength (1.0f)

8. **Damage Tracking Setup**
   - Reset total damage received: `shipp->total_damage_received = 0.0f`
   - Clear damage arrays for scoring purposes
   - Reset damage ship IDs

9. **Systems Integration**
   - Add to Ship_obj_list for tracking
   - Set creation timestamp: `shipp->create_time = timer_get_milliseconds()`
   - Make timestamp unique: `ship_make_create_time_unique(shipp)`
   - Initialize wing status (-1 = not in wing)

10. **Effects and Visual Systems**
    - Initialize afterburner trails: `ship_init_afterburners(shipp)`
    - Set up contrails: `ct_ship_create(shipp)`
    - Set initial model animation states: `model_anim_set_initial_states(shipp)`

### 2. Ship Activation and Arrival

Ships transition through arrival states:

**Arrival State Flow:**
```
Pre-arrival (not yet created) 
    ↓
SF_ARRIVING_STAGE_1 (warp-in effect, stage 1)
    ↓  
SF_ARRIVING_STAGE_2 (warp-in effect, stage 2)
    ↓
Active (normal operations)
```

**Arrival Location Types:**
- Near another ship (arrival_anchor)
- At specific distance from anchor
- Via docking bay
- At waypoint location
- Via hyperspace jump

### 3. Active Ship State Management

During active gameplay, ships maintain state through:

**Core State Properties:**
```cpp
struct ship {
    uint flags;                    // Primary state flags (SF_*)
    uint flags2;                   // Secondary state flags (SF2_*)
    int team;                      // Team assignment (HOSTILE, FRIENDLY, UNKNOWN, NEUTRAL)
    int ai_index;                  // Index into AI system
    int wingnum;                   // Wing membership (-1 if not in wing)
    int orders_accepted;           // Set of orders this ship accepts from player
    uint create_time;              // Time ship was created
    
    // Mission integration
    int arrival_location;          // How/where ship arrives
    int arrival_anchor;            // What ship arrives near
    int arrival_cue;               // SEXP condition for arrival
    int arrival_delay;             // Delay after cue becomes true
    
    int departure_location;        // How ship departs
    int departure_anchor;          // What ship departs to
    int departure_cue;             // SEXP condition for departure  
    int departure_delay;           // Delay after cue becomes true
};
```

**Team Management:**
- Ships are assigned to teams (indices into team system)
- Team relationships determine friend/foe status
- Used for AI targeting decisions and goal validation

**Wing Integration:**
- Ships can be members of wings (formations)
- Wing membership affects AI behavior and goals
- Wing status tracked in HUD wingman status gauge

### 4. Combat State Management

**Damage and Death States:**
```cpp
// Death sequence timing
int final_death_time;           // Time until big fireball starts
int death_time;                 // Time until big fireball starts  
int end_death_time;             // Time until big fireball starts
int really_final_death_time;    // Time until ship breaks up and disappears
vec3d deathroll_rotvel;         // Desired death rotational velocity

// Combat state flags
#define SF_DYING               (1 << 30)  // Ship is in death sequence
#define SF_DISABLED            (1 << 29)  // Ship systems are offline  
#define SF_EXPLODED            (1 << 11)  // Ship has exploded
#define SF_VAPORIZE            (1 << 8)   // Ship vaporized by beam weapon
```

**Dying Process (`ship_dying_frame`):**
1. Play death roll effects and sounds
2. Manage explosion timing and effects  
3. Handle special explosion types (vaporization)
4. Track death scream state
5. Transition to cleanup when death sequence complete

### 5. Departure State Management

Ships can depart in several ways:

**Departure Types:**
```cpp
#define SF_DEPART_WARP      (1 << 28)  // Departing via warp-out
#define SF_DEPART_DOCKBAY   (1 << 27)  // Departing via docking bay
#define SF_DEPARTING        (SF_DEPART_WARP | SF_DEPART_DOCKBAY)
```

**Departure Process:**
1. Departure cue evaluation (SEXP condition)
2. Departure delay timing
3. Warp-out or docking bay sequence
4. Cleanup and removal from active objects

### 6. Ship Cleanup (`ship_cleanup`)

Unified cleanup function handles all end-of-life scenarios:

```cpp
void ship_cleanup(int shipnum, int cleanup_mode)
```

**Cleanup Modes:**
```cpp
#define SHIP_VANISHED          (1<<0)  // Ship disappeared without trace
#define SHIP_DESTROYED         (1<<1)  // Ship was destroyed in combat
#define SHIP_DEPARTED_WARP     (1<<2)  // Ship departed via warp
#define SHIP_DEPARTED_BAY      (1<<3)  // Ship departed via docking bay
#define SHIP_DEPARTED          (SHIP_DEPARTED_BAY | SHIP_DEPARTED_WARP)
```

**Cleanup Process:**
1. **Exited Ship Tracking**
   - Add ship to `Ships_exited` vector for mission statistics
   - Record destruction/departure reason and timing
   - Preserve damage tracking data for scoring

2. **Kill Count Recording**
   - Check ignore flags (ship and wing level)
   - Update ship type kill statistics: `ship_add_ship_type_kill_count()`
   - Notify music system of hostile ship destruction

3. **Mission Log Integration**
   - Log departure events (destroyed ships logged elsewhere)
   - Include jump node information for departures
   - Respect log suppression flags (SF2_NO_DEPARTURE_LOG)

4. **UI Updates**
   - Update wingman status gauge
   - Set appropriate status (dead, departed, none)
   - Clear wing status indices

5. **Wing Management**
   - Update wing statistics (total_destroyed, total_departed, total_vanished)
   - Execute wing cleanup: `ship_wing_cleanup(shipnum, wingp)`
   - Handle guarded wing notifications

6. **AI System Cleanup**
   - Notify AI system: `ai_ship_destroy(shipnum, reason)`
   - Clear goals and targeting references
   - Update formation and escort behaviors

7. **Visual Effects Cleanup**
   - Clear ship decals: `ship_clear_decals(shipp)`
   - Remove particle effects and trails
   - Clean up any persistent visual elements

## Integration Points

### 1. Mission System Integration

**Mission File Persistence:**
- Ship flags 0-7 are saved to/loaded from mission files
- Ship arrival/departure conditions stored as SEXP expressions
- Wing assignments and formation data preserved
- Team assignments and IFF relationships maintained

**Mission Events:**
- Ship creation triggered by arrival cues
- Departure triggered by departure cues or mission events
- Death events logged for mission statistics and debriefing
- Red alert missions can store/restore ship status

### 2. AI State Integration

**AI Goal System:**
```cpp
struct ai_goal {
    int signature;          // Unique identifier
    int ai_mode;           // AIM_* mode for this goal
    int type;              // Goal type (event, player, dynamic)
    int flags;             // Goal flags (AIGF_*)
    fix time;              // When goal was issued
    int priority;          // Goal priority (0-100)
    char* ship_name;       // Target ship name
    // ... additional goal-specific data
};
```

**AI Integration Points:**
- Ship creation assigns AI slot and initializes AI object
- Ship cleanup notifies AI system to clear references
- Ship state changes affect AI goal evaluation
- Team changes trigger AI behavior updates
- Wing membership affects formation and escort AI

### 3. Object Management Integration

**Object System Hierarchy:**
```
Object (generic)
  ├─ Ship Instance
  ├─ Physics Info  
  ├─ Position/Orientation
  └─ Collision Info

Ship (specific)
  ├─ Ship Info (class data)
  ├─ Subsystems
  ├─ Weapons
  ├─ AI Data
  └─ State Flags
```

**Object Lifecycle Coordination:**
- Ship creation creates corresponding object
- Object destruction triggers ship cleanup
- Physics integration through object system
- Collision detection coordinated with object manager

### 4. Save/Load System Integration

**Persistent Data:**
- Ship creation timestamps for uniqueness
- Ship name assignments and collision avoidance
- Team assignments and relationships
- Wing memberships and positions
- Low-order ship flags (mission-persistent)
- Damage tracking for scoring
- Cargo and scan status

**Red Alert Missions:**
- Ships with SF_RED_ALERT_STORE_STATUS flag preserve state
- Hull/shield damage preserved across missions
- Weapon loadouts and ammunition counts maintained
- Subsystem damage states saved/restored

## State Validation and Integrity

### 1. State Consistency Checks

**Flag Validation:**
- Arrival/departure states are mutually exclusive
- Dying state prevents most other operations
- Disabled state affects warp capability
- Team assignments validated against IFF definitions

**Resource Integrity:**
- Ship slots properly allocated and deallocated
- AI slots matched with ship indices
- Object system references maintained
- Subsystem lists properly linked

### 2. Error Recovery

**Cleanup Safeguards:**
- Ship cleanup called even if object already marked for deletion
- AI cleanup handles missing ship references gracefully
- Wing cleanup removes invalid ship references
- Exited ship list prevents duplicate entries

**State Recovery:**
- Ships in inconsistent states can be force-cleaned
- Missing AI data can be re-initialized
- Broken subsystem links can be rebuilt
- Invalid team assignments can be corrected

## Performance Considerations

### 1. Memory Management

**Ship Subsystem Allocation:**
- Dynamic subsystem allocation in sets of 200 per set
- Up to 20 sets (4000 total subsystems) supported
- Subsystem free list for efficient reuse
- Hash map for fast subsystem lookup by name

**Resource Cleanup:**
- Shield integrity arrays freed on ship destruction
- Model references released when last ship of type removed
- Texture and effect resources cleaned up properly
- Memory leaks prevented through proper cleanup ordering

### 2. Update Frequency

**Per-Frame Updates:**
- Ship state flags checked every frame
- AI goal evaluation based on ship state
- Physics integration updates position/orientation
- Visual effect updates based on ship status

**Event-Driven Updates:**
- Ship creation triggered by mission events
- Departure triggered by cue evaluation
- Death triggered by hull damage threshold
- Team changes update AI targets immediately

## Recommended Godot Implementation

Based on this analysis, the Godot implementation should include:

### 1. Ship State Manager Node
```gdscript
class_name ShipStateManager
extends Node

enum ShipState {
    PRE_ARRIVAL,
    ARRIVING_STAGE_1,
    ARRIVING_STAGE_2, 
    ACTIVE,
    DEPARTING_WARP,
    DEPARTING_DOCKBAY,
    DYING,
    DESTROYED,
    DEPARTED,
    VANISHED
}

enum CleanupMode {
    DESTROYED,
    DEPARTED_WARP,
    DEPARTED_BAY,
    VANISHED
}

signal state_changed(old_state: ShipState, new_state: ShipState)
signal cleanup_required(cleanup_mode: CleanupMode)
```

### 2. Ship Lifecycle Controller
```gdscript  
class_name ShipLifecycleController
extends Node

# Track ship throughout lifecycle
var ship_state: ShipState = ShipState.PRE_ARRIVAL
var state_flags: int = 0
var state_flags2: int = 0
var creation_time: int
var team_id: int
var wing_id: int = -1

# Mission integration
var arrival_cue: String
var departure_cue: String  
var arrival_delay: float
var departure_delay: float

# Methods for state transitions
func create_ship() -> void
func activate_ship() -> void
func begin_departure(mode: CleanupMode) -> void
func begin_dying_sequence() -> void
func cleanup_ship(mode: CleanupMode) -> void
```

### 3. Integration Systems
- **MissionSystem**: Handle arrival/departure cues and logging
- **AIManager**: Coordinate AI goal updates with ship state changes
- **TeamManager**: Handle team assignments and IFF relationships  
- **WingManager**: Manage wing memberships and formations
- **SaveGameManager**: Persist ship state for red alert missions
- **CombatManager**: Handle damage tracking and death sequences

This implementation would preserve WCS's comprehensive ship lifecycle management while leveraging Godot's node system and signals for clean, maintainable code.
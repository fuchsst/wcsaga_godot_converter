# AI Module (Godot Implementation)

## Purpose
The AI Module handles all non-player ship behavior in the Godot implementation, including combat tactics, navigation, movement, and decision-making. It provides different behavioral models for various ship types and handles both individual ship AI and coordinated wing tactics, leveraging Godot's node-based architecture and behavior tree patterns.

## Components
- **AI Controller**: Main AI brain managing behavior for ships
- **Behavior Tree System**: Modular decision-making using behavior trees
- **AI Profiles**: Templates defining personality and skill levels
- **Goal System**: Prioritized objectives for AI entities
- **Pathfinding**: Navigation and waypoint following
- **Combat Tactics**: Subsystem targeting and weapon selection
- **Formation Flying**: Coordinated wing movement
- **Strafing Patterns**: Specialized attack patterns for capital ships
- **Docking Procedures**: Complex docking operations

## Dependencies
- **Core Entity Module**: AI controls entity behavior
- **Ship Module**: AI-specific ship behaviors and subsystems
- **Weapon Module**: Weapon selection and firing decisions
- **Physics Module**: Movement and navigation calculations
- **Model Module**: Model subsystem access and path information
- **Mission Module**: Mission-specific AI directives and goals

## Godot Implementation Details

### Native GDScript Classes
```gdscript
# AI Controller that manages behavior for a ship
class AIController extends Node:
    # Reference to the ship this AI controls
    var ship: Ship
    
    # Current AI state and behavior
    var currentState: AIState
    var behaviorTree: BehaviorTree
    var aiProfile: AIProfile
    
    # Goal management
    var goals: Array[AIGoal]
    var currentGoal: AIGoal = null
    
    # Target tracking
    var currentTarget: Node3D = null
    var targetLockTime: float = 0.0
    
    # Navigation
    var navigationPath: Array[Vector3] = []
    var currentPathIndex: int = 0
    var waypointTolerance: float = 50.0
    
    # Combat variables
    var combatRange: float = 800.0
    var preferredRange: float = 600.0
    var evasionThreshold: float = 300.0
    
    # Formation flying
    var formationLeader: Ship = null
    var formationOffset: Vector3 = Vector3.ZERO
    var formationSlot: int = 0
    
    # Events
    signal target_acquired(target)
    signal target_lost(target)
    signal goal_completed(goal)
    signal state_changed(old_state, new_state)
    
    func _init(owner_ship: Ship):
        ship = owner_ship
        # Load default behavior tree
        behaviorTree = preload("res://scripts/ai/default_behavior_tree.tres").duplicate()
        
    func _ready():
        # Initialize AI profile
        initialize_profile()
        
    func _process(delta):
        # Process current AI state and update behavior
        if ship != null and ship.isActive:
            update_goals()
            execute_behavior_tree(delta)
            
    func initialize_profile():
        # Load AI profile based on ship class or mission settings
        if ship.shipClass.defaultAIProfile != "":
            aiProfile = AIProfileDatabase.get_profile(ship.shipClass.defaultAIProfile)
        else:
            # Load default profile
            aiProfile = AIProfileDatabase.get_profile("DEFAULT")
            
        # Apply profile settings
        if aiProfile != null:
            combatRange = aiProfile.preferredRange
            preferredRange = aiProfile.preferredRange * 0.8
            evasionThreshold = aiProfile.evasionThreshold
            
    func update_goals():
        # Process and prioritize AI goals
        # Remove completed or invalid goals
        for i in range(goals.size() - 1, -1, -1):
            var goal = goals[i]
            if goal.is_completed() or not goal.is_valid():
                goals.remove_at(i)
                emit_signal("goal_completed", goal)
                
        # Sort goals by priority
        goals.sort_custom(Callable(self, "sort_goals_by_priority"))
        
        # Set current goal if needed
        if (currentGoal == null or currentGoal.is_completed()) and not goals.is_empty():
            currentGoal = goals[0]
            
    func sort_goals_by_priority(a: AIGoal, b: AIGoal) -> bool:
        # Higher priority goals come first
        return a.priority > b.priority
        
    func execute_behavior_tree(delta):
        # Execute the behavior tree based on current state
        if behaviorTree != null:
            behaviorTree.execute(self, delta)
            
    func set_attack_target(target: Node3D):
        # Set current target and add attack goal
        if target != null and target != currentTarget:
            currentTarget = target
            emit_signal("target_acquired", target)
            
            # Add attack goal with high priority
            var attackGoal = AIGoal.new()
            attackGoal.type = AIGoal.Type.ATTACK
            attackGoal.target = target
            attackGoal.priority = 100
            add_goal(attackGoal)
            
    func clear_target():
        # Clear current target
        if currentTarget != null:
            emit_signal("target_lost", currentTarget)
            currentTarget = null
            targetLockTime = 0.0
            
    func add_goal(goal: AIGoal):
        # Add goal to list
        goals.append(goal)
        
    func set_state(new_state: AIState.Type):
        # Change AI state
        var old_state = currentState.type if currentState != null else AIState.Type.NONE
        currentState = AIState.new(new_state)
        emit_signal("state_changed", old_state, new_state)
        
    func navigate_to_position(target_position: Vector3):
        # Calculate path to target position
        navigationPath = calculate_path(ship.global_position, target_position)
        currentPathIndex = 0
        
        # Set navigation goal
        var navGoal = AIGoal.new()
        navGoal.type = AIGoal.Type.NAVIGATE
        navGoal.targetPosition = target_position
        navGoal.priority = 50
        add_goal(navGoal)
        
    func calculate_path(start: Vector3, end: Vector3) -> Array[Vector3]:
        # Simplified path calculation
        # In a full implementation, this would use a navigation system
        var path = []
        path.append(start)
        path.append(end)
        return path
        
    func follow_formation_leader(leader: Ship, offset: Vector3, slot: int):
        # Set formation flying parameters
        formationLeader = leader
        formationOffset = offset
        formationSlot = slot
        
        # Add formation goal
        var formationGoal = AIGoal.new()
        formationGoal.type = AIGoal.Type.FORMATION
        formationGoal.target = leader
        formationGoal.priority = 75
        add_goal(formationGoal)
        
    func get_preferred_weapon() -> Weapon:
        # Select preferred weapon based on target and range
        if currentTarget == null or ship.weaponSystem == null:
            return null
            
        var distance = ship.global_position.distance_to(currentTarget.global_position)
        
        # Choose weapon based on distance and target type
        if distance > 800:  # Long range
            # Prefer missiles or long-range weapons
            for weapon in ship.weaponSystem.primaryWeapons:
                if weapon.weaponClass.maxRange >= distance:
                    return weapon
        else:  # Short range
            # Prefer lasers or short-range weapons
            for weapon in ship.weaponSystem.primaryWeapons:
                if weapon.weaponClass.weaponType == "LASER" and weapon.weaponClass.maxRange >= distance:
                    return weapon
                    
        # Default to first available weapon
        if not ship.weaponSystem.primaryWeapons.is_empty():
            return ship.weaponSystem.primaryWeapons[0]
            
        return null
        
    func is_target_in_range() -> bool:
        # Check if current target is within weapon range
        if currentTarget == null:
            return false
            
        var distance = ship.global_position.distance_to(currentTarget.global_position)
        var weapon = get_preferred_weapon()
        
        if weapon != null:
            return distance <= weapon.weaponClass.maxRange
        else:
            return distance <= combatRange
            
    func is_target_threat() -> bool:
        # Check if target poses immediate threat
        if currentTarget == null:
            return false
            
        var distance = ship.global_position.distance_to(currentTarget.global_position)
        return distance < evasionThreshold

# AI State representing different behavioral modes
class AIState:
    enum Type { 
        NONE,
        IDLE, 
        PATROL, 
        ATTACK, 
        EVADE, 
        CHASE, 
        GUARD, 
        DOCK, 
        WARP,
        FORMATION,
        STRAFE,
        REARM
    }
    
    var type: Type
    var parameters: Dictionary = {}
    
    func _init(state_type: Type):
        type = state_type
        
    func enter(ai_controller: AIController):
        # Initialize state-specific behavior
        match type:
            Type.IDLE:
                # Stop all movement
                if ai_controller.ship.physicsController != null:
                    ai_controller.ship.physicsController.forward_thrust = 0.0
                    ai_controller.ship.physicsController.side_thrust = 0.0
                    ai_controller.ship.physicsController.vertical_thrust = 0.0
                    
            Type.ATTACK:
                # Prepare for combat
                pass
                
            Type.EVADE:
                # Prepare for evasion
                pass
                
    func execute(ai_controller: AIController, delta: float):
        # Perform state-specific actions
        match type:
            Type.IDLE:
                # Do nothing
                pass
                
            Type.PATROL:
                # Patrol waypoints
                execute_patrol(ai_controller, delta)
                
            Type.ATTACK:
                # Attack current target
                execute_attack(ai_controller, delta)
                
            Type.EVADE:
                # Evade threats
                execute_evade(ai_controller, delta)
                
            Type.CHASE:
                # Chase target
                execute_chase(ai_controller, delta)
                
            Type.GUARD:
                # Guard area or target
                execute_guard(ai_controller, delta)
                
            Type.DOCK:
                # Dock with target
                execute_dock(ai_controller, delta)
                
            Type.WARP:
                # Warp out
                execute_warp(ai_controller, delta)
                
            Type.FORMATION:
                # Fly in formation
                execute_formation(ai_controller, delta)
                
            Type.STRAFE:
                # Strafe capital ship
                execute_strafe(ai_controller, delta)
                
            Type.REARM:
                # Rearm/refuel
                execute_rearm(ai_controller, delta)
                
    func exit(ai_controller: AIController):
        # Cleanup state-specific resources
        pass
        
    func execute_patrol(ai_controller: AIController, delta: float):
        # Patrol behavior implementation
        pass
        
    func execute_attack(ai_controller: AIController, delta: float):
        # Attack behavior implementation
        if ai_controller.currentTarget != null:
            # Move toward target
            var direction = (ai_controller.currentTarget.global_position - ai_controller.ship.global_position).normalized()
            var distance = ai_controller.ship.global_position.distance_to(ai_controller.currentTarget.global_position)
            
            # Face target
            ai_controller.ship.look_at(ai_controller.currentTarget.global_position, Vector3.UP)
            
            # Move based on distance
            if distance > ai_controller.combatRange:
                # Move closer
                ai_controller.ship.physicsController.forward_thrust = 1.0
            elif distance < ai_controller.evasionThreshold:
                # Move away
                ai_controller.ship.physicsController.forward_thrust = -0.5
            else:
                # Maintain distance
                ai_controller.ship.physicsController.forward_thrust = 0.0
                
            # Fire weapons when in range
            if ai_controller.is_target_in_range():
                ai_controller.ship.weaponSystem.fire_primary(ai_controller.currentTarget)
                
    func execute_evade(ai_controller: AIController, delta: float):
        # Evasion behavior implementation
        pass
        
    func execute_chase(ai_controller: AIController, delta: float):
        # Chase behavior implementation
        pass
        
    func execute_guard(ai_controller: AIController, delta: float):
        # Guard behavior implementation
        pass
        
    func execute_dock(ai_controller: AIController, delta: float):
        # Docking behavior implementation
        pass
        
    func execute_warp(ai_controller: AIController, delta: float):
        # Warp behavior implementation
        pass
        
    func execute_formation(ai_controller: AIController, delta: float):
        # Formation flying implementation
        if ai_controller.formationLeader != null:
            # Calculate desired position relative to leader
            var desired_position = ai_controller.formationLeader.global_position + ai_controller.formationOffset
            
            # Move toward formation position
            var direction = (desired_position - ai_controller.ship.global_position).normalized()
            var distance = ai_controller.ship.global_position.distance_to(desired_position)
            
            if distance > 50:  # Formation tolerance
                ai_controller.ship.physicsController.forward_thrust = 1.0
                ai_controller.ship.look_at(desired_position, Vector3.UP)
            else:
                ai_controller.ship.physicsController.forward_thrust = 0.0
                
    func execute_strafe(ai_controller: AIController, delta: float):
        # Strafing behavior implementation
        pass
        
    func execute_rearm(ai_controller: AIController, delta: float):
        # Rearm behavior implementation
        pass

# AI Goal representing objectives for AI entities
class AIGoal:
    enum Type { 
        ATTACK, 
        EVADE, 
        PATROL, 
        GUARD, 
        DOCK, 
        WARP, 
        REARM,
        NAVIGATE,
        FORMATION,
        STRAFE
    }
    
    var type: Type
    var target: Node3D = null
    var targetPosition: Vector3 = Vector3.ZERO
    var priority: int = 0
    var isActive: bool = true
    var isCompleted: bool = false
    var parameters: Dictionary = {}
    
    func is_valid() -> bool:
        # Check if goal is still valid
        return isActive and not isCompleted and (target == null or is_instance_valid(target))
        
    func is_completed() -> bool:
        # Check if goal is completed
        return isCompleted
        
    func update_completion_status(ai_controller: AIController) -> bool:
        # Update completion status based on current state
        match type:
            Type.ATTACK:
                if target == null or not is_instance_valid(target):
                    isCompleted = true
                    return true
                    
            Type.NAVIGATE:
                if ai_controller.ship.global_position.distance_to(targetPosition) < 100:
                    isCompleted = true
                    return true
                    
            Type.DOCK:
                if ai_controller.ship.isDocked:
                    isCompleted = true
                    return true
                    
        return isCompleted

# Behavior Tree for complex AI decision making
class BehaviorTree:
    var root: BTNode
    
    func execute(ai_controller: AIController, delta: float):
        if root != null:
            root.execute(ai_controller, delta)

# Base Behavior Tree Node
class BTNode:
    func execute(ai_controller: AIController, delta: float) -> bool:
        # Return true if behavior succeeded, false if failed
        return false

# Composite node that executes children in sequence
class BTSequence extends BTNode:
    var children: Array[BTNode] = []
    
    func execute(ai_controller: AIController, delta: float) -> bool:
        for child in children:
            if not child.execute(ai_controller, delta):
                return false  # Stop on first failure
        return true  # All children succeeded

# Selector node that tries children until one succeeds
class BTSelector extends BTNode:
    var children: Array[BTNode] = []
    
    func execute(ai_controller: AIController, delta: float) -> bool:
        for child in children:
            if child.execute(ai_controller, delta):
                return true  # Stop on first success
        return false  # All children failed

# Decorator node that modifies child behavior
class BTDecorator extends BTNode:
    var child: BTNode
    
    func execute(ai_controller: AIController, delta: float) -> bool:
        if child != null:
            return child.execute(ai_controller, delta)
        return false

# Condition node that checks a condition
class BTCondition extends BTNode:
    var condition_function: Callable
    
    func execute(ai_controller: AIController, delta: float) -> bool:
        if condition_function.is_valid():
            return condition_function.call(ai_controller)
        return false

# Action node that performs an action
class BTAction extends BTNode:
    var action_function: Callable
    
    func execute(ai_controller: AIController, delta: float) -> bool:
        if action_function.is_valid():
            return action_function.call(ai_controller, delta)
        return false

# Specific AI behaviors

# Behavior for attacking a target
class BTAttack extends BTAction:
    func execute(ai_controller: AIController, delta: float) -> bool:
        if ai_controller.currentTarget == null:
            return false
            
        # Navigate to target
        var distance = ai_controller.ship.global_position.distance_to(
            ai_controller.currentTarget.global_position)
            
        if distance > ai_controller.ship.weaponSystem.get_max_range():
            # Move closer to target
            var direction = (ai_controller.currentTarget.global_position - 
                           ai_controller.ship.global_position).normalized()
            ai_controller.ship.physicsController.forward_thrust = 1.0
            ai_controller.ship.look_at(ai_controller.currentTarget.global_position, Vector3.UP)
        else:
            # Face target and fire weapons
            ai_controller.ship.look_at(ai_controller.currentTarget.global_position, Vector3.UP)
            ai_controller.ship.weaponSystem.fire_primary()
            
        return true

# Behavior for evading threats
class BTEvade extends BTAction:
    func execute(ai_controller: AIController, delta: float) -> bool:
        # Find nearest threat
        var nearest_threat = find_nearest_threat(ai_controller)
        if nearest_threat == null:
            return false
            
        # Move away from threat
        var direction = (ai_controller.ship.global_position - 
                        nearest_threat.global_position).normalized()
        ai_controller.ship.physicsController.forward_thrust = 1.0
        ai_controller.ship.look_at(ai_controller.ship.global_position + direction, Vector3.UP)
        
        return true
        
    func find_nearest_threat(ai_controller: AIController) -> Node3D:
        # Simplified threat detection
        # In reality, this would check for nearby enemies within a certain range
        return ai_controller.currentTarget

# Behavior for patrolling waypoints
class BTPatrol extends BTAction:
    func execute(ai_controller: AIController, delta: float) -> bool:
        # Check if we have a navigation path
        if ai_controller.navigationPath.is_empty():
            return false
            
        # Check if we've reached current waypoint
        if ai_controller.currentPathIndex < ai_controller.navigationPath.size():
            var waypoint = ai_controller.navigationPath[ai_controller.currentPathIndex]
            var distance = ai_controller.ship.global_position.distance_to(waypoint)
            
            if distance < ai_controller.waypointTolerance:
                # Move to next waypoint
                ai_controller.currentPathIndex += 1
                if ai_controller.currentPathIndex >= ai_controller.navigationPath.size():
                    # Reached end of path
                    return true
                    
            # Navigate to current waypoint
            var direction = (waypoint - ai_controller.ship.global_position).normalized()
            ai_controller.ship.physicsController.forward_thrust = 1.0
            ai_controller.ship.look_at(waypoint, Vector3.UP)
            
        return true

# AI Profile defining personality and skill levels
class AIProfile extends Resource:
    @export var name: String
    @export var description: String
    
    # Combat behavior
    @export var aggression: float = 0.5  # 0.0 (passive) to 1.0 (aggressive)
    @export var courage: float = 0.7       # Willingness to engage in combat
    @export var patience: float = 0.3      # Tendency to wait vs. rush in
    
    # Accuracy and skill
    @export var accuracy: float = 0.8      # Hit probability
    @export var evasion: float = 0.6        # Dodge probability
    @export var tactical_approach: String = "STRAFE"  # Preferred attack method
    
    # Weapon preferences
    @export var preferred_weapons: Array[String] = ["MISSILE", "LASER"]
    
    # Formation preferences
    @export var formation_preference: String = "WING"
    
    # Combat ranges
    @export var preferredRange: float = 600.0
    @export var evasionThreshold: float = 300.0
    
    func _init():
        resource_name = name

# AI Profile database for accessing profiles
class AIProfileDatabase:
    static var profiles: Dictionary = {}
    
    static func initialize():
        # Load all AI profiles
        load_profiles()
        
    static func load_profiles():
        # Load profiles from resources
        var profile_files = get_profile_files()
        for file_path in profile_files:
            var profile = load(file_path)
            if profile is AIProfile:
                profiles[profile.name] = profile
                
    static func get_profile(profile_name: String) -> AIProfile:
        return profiles.get(profile_name, null)
        
    static func get_profile_files() -> Array:
        # Return list of profile file paths
        # This would typically scan a directory for .tres files
        return [
            "res://assets/data/ai/aggressive.tres",
            "res://assets/data/ai/defensive.tres",
            "res://assets/data/ai/tactical.tres",
            "res://assets/data/ai/default.tres"
        ]

# Wing AI controller for coordinating groups of ships
class WingAIController extends Node:
    var wing_leader: Ship
    var wing_members: Array[Ship] = []
    var formation_pattern: String = "WEDGE"
    var wing_goals: Array[AIGoal] = []
    
    func _ready():
        # Initialize wing formation
        initialize_formation()
        
    func initialize_formation():
        # Set up formation positions for wing members
        for i in range(wing_members.size()):
            var member = wing_members[i]
            if member.aiController != null:
                var offset = calculate_formation_offset(i)
                member.aiController.follow_formation_leader(wing_leader, offset, i)
                
    func calculate_formation_offset(slot: int) -> Vector3:
        # Calculate formation offset based on pattern
        match formation_pattern:
            "WEDGE":
                return Vector3(slot * 50, 0, -slot * 30)
            "LINE":
                return Vector3(0, 0, -slot * 50)
            "ECHELON":
                return Vector3(slot * 30, 0, -slot * 30)
            _:
                return Vector3(0, 0, -slot * 50)
                
    func add_wing_goal(goal: AIGoal):
        # Add goal to all wing members
        wing_goals.append(goal)
        for member in wing_members:
            if member.aiController != null:
                member.aiController.add_goal(goal.duplicate())
                
    func set_attack_target(target: Node3D):
        # Set attack target for entire wing
        for member in wing_members:
            if member.aiController != null:
                member.aiController.set_attack_target(target)
                
    func execute_wing_behavior(delta: float):
        # Coordinate wing behavior
        # Leader behavior influences wing
        if wing_leader.aiController != null and wing_leader.aiController.currentState != null:
            var leader_state = wing_leader.aiController.currentState.type
            
            # Adjust wing member behavior based on leader state
            for member in wing_members:
                if member != wing_leader and member.aiController != null:
                    # Modify member behavior based on formation role
                    adjust_member_behavior(member, leader_state)
                    
    func adjust_member_behavior(member: Ship, leader_state: AIState.Type):
        # Adjust individual member behavior
        pass
```

### TRES Resources
```ini
[gd_resource type="Resource" load_steps=2 format=2]

[resource]
resource_name = "Aggressive_AI_Profile"
name = "Aggressive"
description = "Highly aggressive AI that seeks combat"
aggression = 0.9
courage = 0.95
patience = 0.1
accuracy = 0.85
evasion = 0.7
tactical_approach = "STRAFE"
preferred_weapons = ["MISSILE", "LASER"]
formation_preference = "WING"
preferredRange = 600.0
evasionThreshold = 200.0

[gd_resource type="Resource" load_steps=2 format=2]

[resource]
resource_name = "Defensive_AI_Profile"
name = "Defensive"
description = "Defensive AI that avoids unnecessary combat"
aggression = 0.2
courage = 0.6
patience = 0.8
accuracy = 0.9
evasion = 0.9
tactical_approach = "EVADE"
preferred_weapons = ["LASER"]
formation_preference = "LINE"
preferredRange = 800.0
evasionThreshold = 400.0
```

### TSCN Scenes
```ini
[gd_scene load_steps=4 format=2]

[ext_resource path="res://scripts/entities/base_fighter.gd" type="Script" id=1]
[ext_resource path="res://scripts/ai/ai_controller.gd" type="Script" id=2]
[ext_resource path="res://assets/data/ai/aggressive.tres" type="Resource" id=3]

[node name="EnemyFighter" type="Node3D"]
script = ExtResource(1)

[node name="AIController" type="Node" parent="."]
script = ExtResource(2)
ai_profile = ExtResource(3)
```

## Feature Organization

Following the feature-based organization principles defined in `directory_structure.md` and `Godot_Project_Structure_Refinement.md`, AI-related components are organized as follows:

### Scripts
AI-related scripts are organized in `/scripts/ai/` with base classes and behavior definitions:
- `/scripts/ai/ai_controller.gd` - Main AI controller implementation
- `/scripts/ai/ai_state.gd` - AI state management
- `/scripts/ai/ai_goal.gd` - AI goal system
- `/scripts/ai/behavior_tree/` - Behavior tree system implementations
  - `/scripts/ai/behavior_tree/bt_node.gd` - Base behavior tree node
  - `/scripts/ai/behavior_tree/bt_sequence.gd` - Sequence composite node
  - `/scripts/ai/behavior_tree/bt_selector.gd` - Selector composite node
  - `/scripts/ai/behavior_tree/bt_decorator.gd` - Decorator node
  - `/scripts/ai/behavior_tree/bt_condition.gd` - Condition leaf node
  - `/scripts/ai/behavior_tree/bt_action.gd` - Action leaf node
  - `/scripts/ai/behavior_tree/specific_behaviors/` - Specific AI behaviors
    - `/scripts/ai/behavior_tree/specific_behaviors/bt_attack.gd` - Attack behavior
    - `/scripts/ai/behavior_tree/specific_behaviors/bt_evade.gd` - Evade behavior
    - `/scripts/ai/behavior_tree/specific_behaviors/bt_patrol.gd` - Patrol behavior

### Assets
AI profile data resources are stored in `/assets/data/ai/` for easy access and modification, following the hybrid model approach where truly global assets are organized in `/assets/`:
- `/assets/data/ai/aggressive.tres` - Aggressive AI profile
- `/assets/data/ai/defensive.tres` - Defensive AI profile
- `/assets/data/ai/tactical.tres` - Tactical AI profile
- `/assets/data/ai/default.tres` - Default AI profile

### Features
The AI controller is designed to be attached to ship entities in `/features/fighters/` or `/features/capital_ships/` as needed. Each ship feature includes its own AI controller instance as a child node, following the self-contained feature organization principle where all files related to a single feature are grouped together.

For example, in the `/features/fighters/confed_rapier/` directory:
- `rapier.tscn` - Scene file that includes an AIController node as a child
- `rapier.gd` - Script file
- `rapier.tres` - Ship data resource
- `rapier.glb` - 3D model
- `rapier.png` - Texture
- `rapier_engine.ogg` - Engine sound

### Shared Assets
For shared AI-related assets that might be used across multiple ship types, the `_shared` directory pattern is used within the appropriate feature category, following the hybrid model approach for semi-global assets:
- `/features/fighters/_shared/ai/` - Shared AI assets for fighters
- `/features/capital_ships/_shared/ai/` - Shared AI assets for capital ships

This follows the guiding principle: "If I delete three random features, is this asset still needed?" If yes, it belongs in `/assets/`; if only needed by a specific feature category, it belongs in that category's `/_shared/` directory.

## Implementation Notes
The AI Module in Godot leverages:

1. **Behavior Trees**: For complex, modular AI decision-making using a hierarchical structure
2. **State Machines**: For managing different behavioral modes with enter/execute/exit patterns
3. **Resources**: AI profiles as data-driven configurations for easy balancing
4. **Signals**: For communication between AI and other systems
5. **Node System**: AI controllers as separate nodes that can be attached to ships
6. **Pathfinding**: Godot's built-in navigation systems for waypoint following
7. **Scene System**: AI behaviors as composable scene elements

This replaces the C++ goal-based system with a more flexible behavior tree approach while preserving the same tactical gameplay functionality. The AI profiles as resources allow for easy balancing and customization without code changes.

The implementation uses Godot's node-based architecture to attach AI controllers to ships, with the behavior tree system providing modular decision-making capabilities. Formation flying is implemented through coordinated position calculations relative to a leader ship.

The wing AI controller demonstrates how individual ship AIs can be coordinated for group behavior, while still allowing for individual tactical decisions within the overall formation context.

This structure aligns with Godot's best practices for feature-based organization using a hybrid model, where all files related to a single conceptual feature are grouped together in a self-contained directory within `/features/`, while maintaining truly global assets in `/assets/` and using `/_shared/` directories for semi-global assets specific to feature categories.
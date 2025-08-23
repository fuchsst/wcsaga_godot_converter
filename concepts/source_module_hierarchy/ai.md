# AI Module

## Purpose
The AI Module handles all non-player ship behavior, including combat tactics, navigation, movement, and decision-making. It provides different behavioral models for various ship types and handles both individual ship AI and coordinated wing tactics.

## Components
- **AI System** (`ai/`): Core AI functionality and behavior management
- **AI State Management**: AIM_* constants define different AI modes (chase, evade, guard, etc.)
- **Goal System**: AI goals with priorities and dynamic goal assignment
- **Pathfinding**: Global and local path following with waypoint management
- **Combat Tactics**: Subsystem targeting, weapon selection, and tactical positioning
- **Formation Flying**: Wing-based formation movement and coordinated attacks
- **Strafing**: Specialized attack patterns for capital ships
- **Docking**: Complex docking procedures for support and cargo operations

## Dependencies
- **Core Entity Module**: For object management and references
- **Ship Module**: For ship-specific data and subsystems
- **Weapon Module**: For weapon handling and firing decisions
- **Physics Module**: For movement and physics calculations
- **Model Module**: For model subsystem access and path information
- **Mission Module**: For mission-specific AI directives

## C++ Components
- `ai_info`: Main AI state structure containing all AI-related data for a ship
- `ai_process()`: Main AI processing function called each frame
- `ai_attack_object()`: Sets a ship to attack another object
- `ai_evade_object()`: Sets a ship to evade another object
- `ai_ignore_object()`: Makes a ship ignore another object
- `ai_dock_with_object()`: Handles docking behavior between ships
- `ai_start_waypoints()`: Initiates waypoint following
- `ai_warp_out()`: Initiates warp out sequence
- `ai_chase()`: Chase behavior implementation
- `ai_evade()`: Evasion behavior implementation
- `ai_big_ship()`: Specialized AI for capital ships

## Godot Equivalent Mapping

### Native GDScript Classes
```gdscript
# AI Controller that manages behavior for a ship
class AIController:
    var ship: Ship
    var currentState: AIState
    var goals: Array[AIGoal]
    var currentTarget: Node3D
    var behaviorTree: BehaviorTree
    
    func _init(owner_ship: Ship):
        ship = owner_ship
        behaviorTree = preload("res://ai/default_behavior_tree.tres").duplicate()
        
    func _process(delta):
        # Process current AI state and update behavior
        update_goals()
        execute_behavior_tree(delta)
        
    func update_goals():
        # Process and prioritize AI goals
        pass
        
    func execute_behavior_tree(delta):
        # Execute the behavior tree based on current state
        behaviorTree.execute(self, delta)
        
    func set_attack_target(target: Node3D):
        currentTarget = target
        # Add attack goal with high priority
        var attackGoal = AIGoal.new()
        attackGoal.type = AIGoal.Type.ATTACK
        attackGoal.target = target
        attackGoal.priority = 100
        add_goal(attackGoal)

# AI State representing different behavioral modes
class AIState:
    enum Type { IDLE, PATROL, ATTACK, EVADE, CHASE, GUARD, DOCK, WARP }
    var type: Type
    var parameters: Dictionary
    
    func enter():
        # Initialize state-specific behavior
        pass
        
    func execute(delta):
        # Perform state-specific actions
        pass
        
    func exit():
        # Cleanup state-specific resources
        pass

# AI Goal representing objectives for AI entities
class AIGoal:
    enum Type { ATTACK, EVADE, PATROL, GUARD, DOCK, WARP, REARM }
    var type: Type
    var target: Node3D
    var priority: int
    var isActive: bool = true
    
    func evaluate_validity() -> bool:
        # Check if goal is still valid
        return isActive and target != null

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
    var children: Array[BTNode]
    
    func execute(ai_controller: AIController, delta: float) -> bool:
        for child in children:
            if not child.execute(ai_controller, delta):
                return false  # Stop on first failure
        return true  # All children succeeded

# Behavior for attacking a target
class BTAttack extends BTNode:
    func execute(ai_controller: AIController, delta: float) -> bool:
        if ai_controller.currentTarget == null:
            return false
            
        # Navigate to target
        var distance = ai_controller.ship.global_position.distance_to(
            ai_controller.currentTarget.global_position)
            
        if distance > ai_controller.ship.weapon_system.get_max_range():
            # Move closer to target
            ai_controller.ship.move_to_position(
                ai_controller.currentTarget.global_position)
        else:
            # Face target and fire weapons
            ai_controller.ship.face_target(ai_controller.currentTarget)
            ai_controller.ship.weapon_system.fire_weapons()
            
        return true
```

### TRES Resources
```ini
[gd_resource type="Resource" load_steps=2 format=2]

[resource]
resource_name = "Fighter_AI_Profile"
ai_type = "AGGRESSIVE"
accuracy = 0.85
evasion = 0.75
courage = 0.9
patience = 0.3
preferred_weapons = ["MISSILE", "LASER"]
tactical_approach = "STRAFE"
formation_preference = "WING"

[gd_resource type="Resource" load_steps=3 format=2]

[resource]
resource_name = "Capital_Ship_AI_Profile"
ai_type = "TACTICAL"
accuracy = 0.95
evasion = 0.4
courage = 0.95
patience = 0.8
preferred_weapons = ["BEAM", "MISSILE"]
tactical_approach = "BROADSIDE"
formation_preference = "LINE"
```

### TSCN Scenes
```ini
[gd_scene load_steps=3 format=2]

[ext_resource path="res://scripts/ship.gd" type="Script" id=1]
[ext_resource path="res://scripts/ai_controller.gd" type="Script" id=2]

[node name="EnemyFighter" type="Node3D"]
script = ExtResource(1)

[node name="AIController" type="Node" parent="."]
script = ExtResource(2)
ai_profile = "res://resources/fighter_ai_profile.tres"
```

### Implementation Notes
The AI Module in Godot leverages:
1. **Behavior Trees**: For complex, modular AI decision-making
2. **State Machines**: For managing different behavioral modes
3. **Resources**: AI profiles as data-driven configurations
4. **Signals**: For communication between AI and other systems
5. **Pathfinding**: Godot's built-in navigation systems for waypoint following
6. **Node References**: For accessing game entities and their properties

This replaces the C++ goal-based system with a more flexible behavior tree approach while preserving the same tactical gameplay functionality. The AI profiles as resources allow for easy balancing and customization.
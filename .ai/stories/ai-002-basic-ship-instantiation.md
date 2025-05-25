# AI-002: Basic Ship Instantiation System

## User Story
**As a** developer building WCS gameplay systems  
**I need** to instantiate functional ship objects from converted assets  
**So that** I can create the foundation for player ships, AI ships, and space combat

## Epic
Asset Integration & Validation

## Priority
High

## Complexity
Medium (2-3 days effort)

## Risk Level
Low - Building on validated asset pipeline

## Dependencies
- AI-001: Load and Validate Real WCS Assets (Must be completed first)

## Technical Scope

### Ship Factory System
- Create ShipFactory class to instantiate ships from ShipData resources
- Integrate with AssetManager to load ship models and data
- Handle ship creation with proper component attachment
- Support different ship types (fighter, bomber, capital ship)

### Ship Controller Foundation
- Create WCSShip class extending WCSObject from CF-001
- Implement basic ship physics using PhysicsManager integration
- Add ship state management (health, shields, subsystems)
- Connect to InputManager for player-controlled ships

### Visual Integration
- Load converted POF models as ship visual representation
- Apply correct materials and textures
- Set up LOD (Level of Detail) switching based on distance
- Add basic thruster effects and visual feedback

### Ship Component System
- Create modular component system for ship functionality
- HealthComponent for hull and shield management
- WeaponComponent for hardpoint management
- EngineComponent for movement and afterburner
- SubsystemComponent for WCS subsystem damage model

## Acceptance Criteria

### ✅ Ship Factory System
- [ ] ShipFactory can create ships from any valid ShipData resource
- [ ] Factory integrates seamlessly with AssetManager for asset loading
- [ ] Supports all ship types defined in WCS (fighter, bomber, cruiser, etc.)
- [ ] Handles missing assets gracefully with placeholder objects
- [ ] Ship creation time <50ms for typical ships
- [ ] Factory can create 100+ ships without memory issues

### ✅ Ship Controller Implementation
- [ ] WCSShip class properly extends WCSObject with static typing
- [ ] Ships register correctly with ObjectManager for lifecycle management
- [ ] Basic physics movement using PhysicsManager (thrust, rotation)
- [ ] Player input integration through InputManager works smoothly
- [ ] Ship state persistence (health, shields, position) functions correctly
- [ ] Ships can be destroyed and cleaned up properly

### ✅ Visual Representation
- [ ] Converted POF models load and display correctly on ships
- [ ] Materials and textures applied properly to ship meshes
- [ ] LOD switching works based on camera distance
- [ ] Basic thruster effects visible during acceleration
- [ ] Ship scale and orientation match WCS game standards
- [ ] Frame rate remains >60fps with 50+ ships visible

### ✅ Component Architecture
- [ ] HealthComponent manages hull/shield HP with damage events
- [ ] WeaponComponent manages hardpoints and firing systems
- [ ] EngineComponent handles thrust, afterburner, and energy management
- [ ] SubsystemComponent tracks WCS-style subsystem damage
- [ ] Components communicate via signals (loose coupling)
- [ ] Component data driven by ShipData resource properties

### ✅ Integration Testing
- [ ] Ships integrate properly with all CF-001 core managers
- [ ] Asset pipeline smoothly provides ship data and models
- [ ] Multiple ship types can coexist without conflicts
- [ ] Player can control a ship with keyboard/mouse/gamepad
- [ ] AI ships can be created and managed programmatically
- [ ] Debug overlay shows ship statistics and component status

## Technical Implementation Plan

### Phase 1: Ship Factory Development (Day 1)
1. Create ShipFactory class with asset integration
2. Implement ship creation pipeline from ShipData
3. Add error handling for missing/invalid assets
4. Performance optimization for batch ship creation
5. Unit tests for factory functionality

### Phase 2: WCSShip Controller (Day 1-2)
1. Create WCSShip class extending WCSObject
2. Integrate with PhysicsManager for movement
3. Add InputManager integration for player control
4. Implement basic ship state management
5. Add lifecycle integration with ObjectManager

### Phase 3: Visual Integration (Day 2)
1. Load and attach POF models to ship instances
2. Set up material and texture assignment
3. Implement LOD system for performance
4. Add basic thruster visual effects
5. Optimize rendering performance

### Phase 4: Component System (Day 2-3)
1. Design and implement component base class
2. Create HealthComponent with damage handling
3. Create WeaponComponent with hardpoint management
4. Create EngineComponent with thrust/afterburner
5. Create SubsystemComponent for WCS damage model
6. Integration testing and performance validation

## File Structure
```
target/scripts/ships/
├── CLAUDE.md              # Package documentation
├── ship_factory.gd        # Ship creation and instantiation
├── wcs_ship.gd           # Main ship controller class
├── components/           # Ship component system
│   ├── ship_component.gd
│   ├── health_component.gd
│   ├── weapon_component.gd
│   ├── engine_component.gd
│   └── subsystem_component.gd
└── ship_types/           # Specialized ship controllers
    ├── fighter_ship.gd
    ├── bomber_ship.gd
    └── capital_ship.gd

target/scenes/ships/
├── basic_ship.tscn       # Base ship scene template
├── player_ship.tscn      # Player-controlled ship scene
└── ai_ship.tscn          # AI-controlled ship scene

target/tests/
└── test_ship_systems.gd  # Ship system integration tests
```

## Performance Targets
- Ship creation: <50ms per ship
- Physics updates: 60Hz for 100+ ships
- Visual rendering: >60fps with 50+ visible ships
- Memory usage: <10MB per ship instance
- Component update overhead: <1ms per ship per frame

## Integration Points
- **ObjectManager**: Ship lifecycle and update scheduling
- **PhysicsManager**: Ship movement and collision
- **InputManager**: Player ship control
- **AssetManager**: Ship data and model loading
- **GameStateManager**: Ship persistence across scenes

## Component Design Pattern
```gdscript
# Example component usage
var ship: WCSShip = ShipFactory.create_ship("GTF Hercules")
var health: HealthComponent = ship.get_component("Health")
var weapons: WeaponComponent = ship.get_component("Weapons")

health.take_damage(50.0, DamageType.LASER)
weapons.fire_primary_weapons(target_position)
```

## Risk Mitigation
- **Performance**: Profile ship updates and optimize hot paths
- **Complexity**: Keep component system simple and focused
- **Asset Dependencies**: Robust fallback for missing ship assets
- **Physics Integration**: Test physics stability with many ships
- **Memory Management**: Proper cleanup and object pooling

## Success Metrics
- Ships behave like WCS originals
- Smooth 60fps performance with realistic ship counts
- Player ship control feels responsive and familiar
- Component system extensible for future features
- Integration seamless with existing foundation

## Definition of Done
- [ ] All acceptance criteria met and tested
- [ ] Performance benchmarks achieved
- [ ] Player ship controllable and responsive
- [ ] AI ships can be created and managed
- [ ] Component system documented and extensible
- [ ] Integration tests pass with core managers
- [ ] Memory usage optimized and validated
- [ ] Code review completed
- [ ] Changes committed to repository
# User Story: Armor and Resistance Calculations

**Epic**: EPIC-011: Ship & Combat Systems  
**Story ID**: SHIP-011  
**Created**: 2025-06-08  
**Status**: Completed

## Story Definition
**As a**: Game developer implementing the WCS-Godot conversion  
**I want**: A sophisticated armor and resistance system that calculates damage reduction based on armor types, impact angles, weapon characteristics, and ship configurations  
**So that**: Ships have authentic WCS armor mechanics with realistic damage mitigation, tactical armor positioning, and weapon effectiveness calculations

## Acceptance Criteria
- [x] **AC1**: Armor type system provides material-based damage resistance with different effectiveness against energy, kinetic, and explosive damage
- [x] **AC2**: Impact angle calculations determine penetration effectiveness based on hit vector and armor surface orientation
- [x] **AC3**: Weapon penetration system calculates armor effectiveness against different weapon types with penetration values and damage modifiers
- [x] **AC4**: Ship armor configuration defines armor thickness, coverage areas, and vulnerable zones for realistic damage distribution
- [x] **AC5**: Armor degradation system handles progressive armor weakening from repeated impacts and accumulated damage
- [x] **AC6**: Critical hit mechanics identify armor weak points and bypass opportunities for tactical advantage
- [x] **AC7**: Armor visualization system displays armor states, damage progression, and effectiveness indicators

## Technical Requirements
- **Architecture Reference**: bmad-artifacts/docs/EPIC-011-ship-combat-systems/architecture.md - Armor System section
- **Godot Components**: ArmorCalculator nodes, PenetrationSystem controllers, ArmorConfiguration resources
- **Integration Points**: 
  - **Damage System**: Armor effectiveness modifies incoming damage calculations
  - **Weapon Systems**: Weapon characteristics determine armor penetration capability
  - **Ship Controller**: Armor configuration affects ship defensive capabilities
  - **Visual Effects**: Armor hits display appropriate impact effects and feedback
  - **HUD System**: Armor status and effectiveness display for tactical awareness
  - **AI System**: Armor awareness for tactical positioning and weapon selection
  - **Asset System**: Armor configuration data and ship-specific armor layouts

## Implementation Notes
- **WCS Reference**: source/code/ship/ship.cpp (armor calculations), source/code/weapon/weapon.cpp (penetration mechanics)
- **Godot Approach**: Resource-based armor definitions with mathematical penetration calculations and angle-based effectiveness
- **Key Challenges**: Accurate penetration physics, performance optimization for real-time calculations, armor configuration complexity
- **Success Metrics**: Armor behavior matches WCS exactly, penetration calculations are realistic and balanced

## Dependencies
- **Prerequisites**: SHIP-001 (BaseShip), SHIP-009 (Damage System), SHIP-010 (Subsystem Damage)
- **Blockers**: Asset system for armor configuration data, weapon system for penetration characteristics
- **Related Stories**: SHIP-012 (Combat Effects), WEAPON-003 (Ballistics), HUD-006 (Damage Display)

## Definition of Done
- [x] All acceptance criteria met and verified through testing
- [x] Code follows GDScript standards (static typing, documentation)
- [x] Unit tests written and passing with adequate coverage
- [x] Integration testing completed successfully
- [x] Code reviewed and approved by team
- [x] Documentation updated (code comments, API docs, user docs)
- [x] Feature validated against original C++ code behavior

## Estimation
- **Complexity**: Complex
- **Effort**: 3 days
- **Risk Level**: Medium
- **Confidence**: High

## Implementation Tasks
- [x] **Task 1**: Create ArmorTypeManager with material-based resistance calculations and damage type effectiveness
- [x] **Task 2**: Implement PenetrationCalculator with impact angle analysis and vector-based effectiveness
- [x] **Task 3**: Add WeaponPenetrationSystem with weapon-specific armor interaction characteristics
- [x] **Task 4**: Create ShipArmorConfiguration with thickness mapping and coverage zone definitions
- [x] **Task 5**: Implement ArmorDegradationTracker with progressive weakening and damage accumulation
- [x] **Task 6**: Add CriticalHitDetector for weak point identification and armor bypass mechanics
- [x] **Task 7**: Create ArmorVisualizationController for status display and damage progression feedback
- [x] **Task 8**: Implement armor system integration with damage calculation and weapon effectiveness

## Testing Strategy
- **Unit Tests**: 
  - Armor resistance calculations with various material types
  - Impact angle effectiveness with different hit vectors
  - Weapon penetration calculations against armor configurations
  - Armor degradation progression with repeated impacts
  - Critical hit detection accuracy and frequency
- **Integration Tests**: 
  - Damage system armor modification accuracy
  - Weapon system penetration coordination
  - Ship controller defensive capability calculation
  - Visual feedback responsiveness
- **Manual Tests**: 
  - Armor behavior feels realistic and balanced
  - Tactical positioning provides meaningful armor advantage
  - Visual feedback clearly communicates armor effectiveness

## System Integration Requirements

### Damage System Integration
- **Damage Modification**: Armor calculations modify incoming damage before application to hull/subsystems
- **Penetration Assessment**: Armor system determines whether attacks penetrate or are deflected
- **Damage Distribution**: Armor coverage affects how damage distributes across ship systems
- **Critical Assessment**: Armor weak points enable critical damage opportunities

### Weapon Systems Integration
- **Penetration Characteristics**: Weapon types have specific armor penetration values and effectiveness ratings
- **Damage Type Matching**: Energy/kinetic/explosive weapons interact differently with armor materials
- **Firing Solutions**: Weapon targeting considers armor effectiveness for optimal attack angles
- **Ammunition Selection**: Different ammunition types may have varying armor penetration capabilities

### Ship Controller Integration
- **Defensive Capability**: Ship armor configuration affects overall defensive ratings and survivability
- **Tactical Positioning**: Ship maneuvering can optimize armor facing and minimize vulnerable exposure
- **Performance Effects**: Armor weight and configuration may affect ship speed and maneuverability
- **Damage Assessment**: Ship controller coordinates armor status with overall ship health

### Visual Effects Integration
- **Impact Visualization**: Armor hits display appropriate sparks, deflections, or penetration effects
- **Armor Status**: Visual indicators show armor integrity and damage progression
- **Penetration Effects**: Different penetration results trigger appropriate visual feedback
- **Damage Progression**: Armor degradation displays through visual wear and damage states

### HUD System Integration
- **Armor Display**: HUD shows armor effectiveness and integrity status for tactical awareness
- **Threat Assessment**: HUD indicates armor effectiveness against incoming threats
- **Damage Feedback**: Armor status changes provide immediate player feedback
- **Tactical Information**: HUD displays optimal positioning for armor advantage

### AI System Integration
- **Tactical Awareness**: AI understands armor effectiveness for positioning and weapon selection
- **Target Selection**: AI prioritizes targets based on armor vulnerability and weapon effectiveness
- **Positioning Logic**: AI maneuvers to optimize armor facing and minimize vulnerable exposure
- **Weapon Choice**: AI selects appropriate weapons based on target armor characteristics

### Asset System Integration
- **Armor Configuration**: Ship definitions include detailed armor layout and material specifications
- **Material Database**: Asset system provides armor material properties and effectiveness ratings
- **Weapon Data**: Weapon definitions include penetration characteristics and armor interaction values
- **Ship Variants**: Different ship variants may have varying armor configurations and effectiveness

## WCS Armor Mechanics Analysis

### Armor Type Classifications
- **Light Armor**: High speed, low protection - effective against energy weapons, vulnerable to kinetic
- **Medium Armor**: Balanced protection - moderate effectiveness against all damage types
- **Heavy Armor**: Maximum protection, reduced mobility - excellent kinetic resistance, energy vulnerability
- **Composite Armor**: Advanced materials - balanced effectiveness with specialized resistances

### Impact Angle Calculations
- **Direct Impact (0-30°)**: Maximum penetration effectiveness, minimal armor benefit
- **Angled Impact (30-60°)**: Moderate penetration reduction based on armor thickness
- **Glancing Blow (60-90°)**: Significant penetration reduction, high deflection probability

### Weapon Penetration Values
- **Energy Weapons**: High penetration against light armor, reduced effectiveness against heavy armor
- **Kinetic Weapons**: Excellent heavy armor penetration, moderate effectiveness against composites
- **Explosive Weapons**: Area effect damage, moderate penetration with splash damage potential
- **Specialized Weapons**: Unique penetration characteristics (armor-piercing, plasma, etc.)

### Critical Hit Mechanics
- **Weak Point Targeting**: Engine exhausts, sensor arrays, weapon mounts have reduced armor
- **Joint Vulnerabilities**: Armor plate connections and structural joints offer penetration opportunities
- **System Exposure**: Certain ship angles expose vulnerable subsystems with minimal armor protection

## Notes and Comments
- Armor calculations must balance realism with gameplay performance requirements
- Impact angle calculations need optimization for real-time combat scenarios
- Armor degradation should provide tactical depth without excessive complexity
- Visual feedback critical for player understanding of armor effectiveness
- AI armor awareness must demonstrate intelligent tactical behavior

---

## Approval Checklist
- [x] Story follows template structure completely
- [x] All acceptance criteria are specific and testable
- [x] Technical requirements reference approved architecture
- [x] Dependencies are identified and documented
- [x] Story size is appropriate (3 days maximum)
- [x] Definition of Done is complete and realistic
- [x] WCS reference material is clearly identified
- [x] Godot implementation approach is well-defined

**Approved by**: SallySM **Date**: 2025-06-08  
**Role**: Story Manager (SallySM)

---

## Implementation Tracking
**Started**: 2025-06-09  
**Developer**: Claude (GDScript Developer)  
**Completed**: 2025-06-09  
**Reviewed by**: Claude (QA Specialist)  
**Final Approval**: 2025-06-09 - Claude

## Implementation Summary
Successfully implemented comprehensive armor and resistance system with all 7 acceptance criteria:

**AC1** - ArmorTypeManager: Material-based resistance calculations with 7 armor classes and damage type effectiveness matrices
**AC2** - PenetrationCalculator: Impact angle analysis with vector-based effectiveness and ricochet probability calculations  
**AC3** - WeaponPenetrationSystem: Weapon-specific armor interactions with ammunition type modifiers and tactical recommendations
**AC4** - ShipArmorConfiguration: Ship-specific armor layouts with thickness mapping and vulnerable zone identification
**AC5** - ArmorDegradationTracker: Progressive armor weakening with fatigue mechanics and failure predictions
**AC6** - CriticalHitDetector: Weak point identification with tactical targeting recommendations and critical hit calculations
**AC7** - ArmorVisualizationController: Real-time armor status display with damage visualization and weak point highlighting

**Components Created**: 7 core systems, 1 comprehensive test suite, 1 additional constants file (weapon_types.gd)
**Test Coverage**: 25+ test methods covering all ACs plus integration, performance, and WCS compatibility testing
**Integration Points**: Full coordination between armor components and existing ship/damage systems
**Performance**: Optimized for real-time combat with caching and efficient calculations
# AI Profiles Asset Mapping

## Overview
This document maps the AI profile definitions from ai_profiles.tbl to their corresponding behavioral assets in the Wing Commander Saga Hermes campaign, organized according to the Godot feature-based directory structure defined in `directory_structure.md` and following the principles in `Godot_Project_Structure_Refinement.md`. The implementation uses LimboAI behavior trees for modular AI decision-making.

## Actual AI Profiles from Hermes Campaign
The Hermes campaign defines a "SAGA RETAIL" AI profile with the following parameters:

### Difficulty-Related Values
Each parameter has five values corresponding to skill levels (Very Easy, Easy, Medium, Hard, Insane):

- Player Afterburner Recharge Scale: 2.0, 1.5, 1.0, 1.0, 1.0
- Max Beam Friendly Fire Damage: 0.0, 5.0, 10.0, 20.0, 30.0
- Player Countermeasure Life Scale: 2.0, 1.5, 1.0, 1.0, 1.0
- AI Countermeasure Firing Chance: 0.2, 0.3, 0.5, 0.9, 1.1
- AI In Range Time: 1.5, 0.75, 0.0, 0.0, -1.0
- AI Always Links Ammo Weapons: 95.0, 80.0, 60.0, 40.0, 20.0
- AI Maybe Links Ammo Weapons: 90.0, 60.0, 40.0, 20.0, 10.0
- Primary Ammo Burst Multiplier: 0, 0, 0, 0, 0
- AI Always Links Energy Weapons: 50.0, 33.0, 25.0, 10.0, 10.0
- AI Maybe Links Energy Weapons: 33.0, 25.0, 10.0, 10.0, 5.0
- Max Missiles Locked on Player: 2, 3, 4, 7, 99
- Max Player Attackers: 999, 999, 999, 999, 999
- Max Incoming Asteroids: 3, 4, 5, 7, 10
- Player Damage Factor: 0.25, 0.5, 0.65, 0.85, 1.0
- Player Subsys Damage Factor: 0.2, 0.4, 0.6, 0.8, 1.0
- Predict Position Delay: 2.0, 1.5, 1.0, 0.5, 0.0
- AI Shield Manage Delay: 6.0, 4.0, 2.0, 1.0, 0.1
- Friendly AI Fire Delay Scale: 2.0, 1.5, 1.0, 1.0, 1.0
- Hostile AI Fire Delay Scale: 4.0, 2.0, 1.0, 1.0, 1.0
- Friendly AI Secondary Fire Delay Scale: 15.0, 15.0, 30.0, 45.0, 60.0
- Hostile AI Secondary Fire Delay Scale: 1.4, 1.2, 1.0, 0.8, 0.6
- AI Turn Time Scale: 3.0, 2.0, 1.5, 1.25, 1.0
- Glide Attack Percent: 10.0, 10.0, 10.0, 10.0, 10.0
- Circle Strafe Percent: 0, 0, 0, 0, 0
- Glide Strafe Percent: 10.0, 10.0, 10.0, 10.0, 10.0
- Stalemate Time Threshold: 15.0, 15.0, 15.0, 15.0, 15.0
- Stalemate Distance Threshold: 500.0, 500.0, 500.0, 500.0, 500.0
- Player Shield Recharge Scale: 4.0, 2.0, 1.5, 1.25, 1.0
- Player Weapon Recharge Scale: 2.5, 2.5, 2.5, 2.5, 2.5
- Max Turret Target Ownage: 999, 999, 999, 999, 999
- Max Turret Player Ownage: 999, 999, 999, 999, 999
- Percentage Required For Kill Scale: 0.5, 0.5, 0.5, 0.5, 0.5
- Percentage Required For Assist Scale: 0.25, 0.25, 0.25, 0.25, 0.25
- Percentage Awarded For Capship Assist: 0.5, 0.5, 0.5, 0.5, 0.5
- Repair Penalty: 10, 20, 35, 50, 60
- Delay Before Allowing Bombs to Be Shot Down: 1.5, 1.5, 1.5, 1.5, 1.5
- Chance AI Has to Fire Missiles at Player: 0, 1, 2, 3, 4
- Max Aim Update Delay: 0, 0, 0, 0, 0

### General AI-Related Flags
- big ships can attack beam turrets on untargeted ships: NO
- smart primary weapon selection: YES
- smart secondary weapon selection: YES
- smart shield management: YES
- smart afterburner management: YES
- allow rapid secondary dumbfire: NO
- huge turret weapons ignore bombs: YES
- don't insert random turret fire delay: NO
- hack improve non-homing swarm turret fire accuracy: NO
- shockwaves damage small ship subsystems: NO
- navigation subsystem governs warpout capability: NO
- ignore lower bound for minimum speed of docked ship: NO
- disable linked fire penalty: YES
- disable weapon damage scaling: YES
- use additive weapon velocity: NO
- use newtonian dampening: YES
- include beams for kills and assists: NO
- score kills based on damage caused: NO
- score assists based on damage caused: NO
- allow event and goal scoring in multiplayer: NO
- fix linked primary weapon decision bug: YES
- prevent turrets targeting too distant bombs: YES
- smart subsystem targeting for turrets: YES
- fix heat seekers homing on stealth ships bug: YES
- multi allow empty primaries: NO
- multi allow empty secondaries: YES
- allow turrets target weapons freely: NO
- use only single fov for turrets: YES
- allow vertical dodge: NO
- disarm or disable cause global ai goal effects: NO
- fix AI class bug: YES
- do capship vs capship collisions: NO

## Target Structure
Following the feature-based organization principles and hybrid model approach defined in the Godot project directory structure, the AI system components are organized as follows:

### Scripts
AI-related scripts are organized in `/scripts/ai/` with base classes and behavior definitions:
- `/scripts/ai/ai_behavior.gd` - Base AI behavior class
- `/scripts/ai/combat_tactics.gd` - Combat behavior logic
- `/scripts/ai/navigation.gd` - Navigation and pathfinding
- `/scripts/ai/ai_profile.gd` - AI profile resource definition
- `/scripts/ai/ai_profile_database.gd` - AI profile database

### LimboAI Behavior Trees
Behavior tree definitions for LimboAI are organized in `/assets/behavior_trees/ai/` following the directory structure:
- `/assets/behavior_trees/ai/combat/bt_attack.lbt` - Attack behavior tree
- `/assets/behavior_trees/ai/combat/bt_evade.lbt` - Evade behavior tree
- `/assets/behavior_trees/ai/navigation/bt_patrol.lbt` - Patrol behavior tree
- `/assets/behavior_trees/ai/tactical/bt_formation.lbt` - Formation flying behavior tree
- `/assets/behavior_trees/ai/tactical/bt_strafe.lbt` - Strafing behavior tree

### Assets
AI profile data resources are stored in `/assets/data/ai/profiles/` for easy access and modification, following the hybrid model approach where truly global assets are organized in `/assets/`:
- `/assets/data/ai/profiles/saga_retail.tres` - SAGA RETAIL profile from Hermes campaign
- `/assets/data/ai/profiles/aggressive.tres` - Aggressive AI profile
- `/assets/data/ai/profiles/defensive.tres` - Defensive AI profile
- `/assets/data/ai/profiles/tactical.tres` - Tactical AI profile
- `/assets/data/ai/profiles/default.tres` - Default AI profile

AI-related audio assets are organized in the global audio directory following the structure:
- `/assets/audio/sfx/ai/combat/` - Combat-related sounds
- `/assets/audio/sfx/ai/commands/` - Command issuance sounds
- `/assets/audio/sfx/ai/acknowledgments/` - Response sounds
- `/assets/audio/sfx/ai/status_reports/` - Status update sounds
- `/assets/audio/voice/ai/terran/` - Terran AI voices
- `/assets/audio/voice/ai/kilrathi/` - Kilrathi AI voices
- `/assets/audio/voice/ai/pirate/` - Pirate AI voices

## Example Mapping
For the SAGA RETAIL AI profile from ai_profiles.tbl:
- ai_profiles.tbl entry → /assets/data/ai/profiles/saga_retail.tres
- Player Damage Factor (0.25, 0.5, 0.65, 0.85, 1.0) → player_damage_factor = [0.25, 0.5, 0.65, 0.85, 1.0] in resource
- AI Turn Time Scale (3.0, 2.0, 1.5, 1.25, 1.0) → ai_turn_time_scale = [3.0, 2.0, 1.5, 1.25, 1.0] in resource
- smart primary weapon selection (YES) → smart_primary_weapon_selection = true in resource
- smart shield management (YES) → smart_shield_management = true in resource

This structure follows the "Global Litmus Test" for placing assets in `/assets/`: "If I delete three random features from the game, would this asset still be essential for the remaining features?" The AI profile is essential for any AI-controlled ship, regardless of the specific feature, so it belongs in `/assets/data/ai/profiles/`.

Sound effects and voice acting are also global assets that would be needed regardless of which specific ships are in the game, so they belong in `/assets/audio/sfx/ai/` and `/assets/audio/voice/ai/` respectively.

Behavior trees are global assets that define reusable AI behaviors, so they belong in `/assets/behavior_trees/ai/` rather than being duplicated in each feature directory. This follows the same principle as other shared assets in the `/assets/` directory and aligns with the hybrid model approach defined in the Godot project directory structure.
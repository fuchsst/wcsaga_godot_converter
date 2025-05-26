# WCS System: Core Foundation Infrastructure - Source Dependencies (Used By)

## Core Foundation Headers (Most Critical Dependencies)

### File: `source/code/globalincs/pstypes.h` included/used by:
**Usage**: Universal foundation header included by virtually ALL WCS source files
- `source/code/ai/ai.h` - AI system type definitions
- `source/code/ai/aigoals.h` - AI goals and behavior definitions  
- `source/code/ai/ai_profiles.cpp` - AI configuration implementation
- `source/code/ai/ai_profiles.h` - AI profile management
- `source/code/anim/animplay.h` - Animation playback system
- `source/code/anim/packunpack.h` - Animation compression
- `source/code/asteroid/asteroid.h` - Asteroid field management
- `source/code/autopilot/autopilot.cpp` - Autopilot implementation
- `source/code/bmpman/bmpman.h` - Bitmap management system
- `source/code/camera/camera.h` - Camera system
- `source/code/cmdline/cmdline.h` - Command line processing
- `source/code/cfile/cfile.h` - File I/O system (self-dependency)
- `source/code/cutscene/cutscenes.h` - Cutscene management
- `source/code/debris/debris.h` - Debris simulation
- `source/code/fred2/` (50+ FRED2 editor files) - Mission editor
- `source/code/freespace2/freespace.h` - Main game loop
- `source/code/gamesequence/gamesequence.h` - Game state management
- `source/code/graphics/` (15+ graphics files) - Rendering system
- `source/code/hud/` (20+ HUD files) - User interface
- `source/code/io/` (timer.h, key.h, mouse.h, joy.h) - Input/output
- `source/code/math/vecmat.h` - Vector mathematics (self-dependency)
- `source/code/mission/` (10+ mission files) - Mission loading
- `source/code/model/` (model.h, modelinterp.cpp) - 3D model system
- `source/code/network/` (25+ network files) - Multiplayer
- `source/code/object/` (object.h, collision files) - Game objects
- `source/code/osapi/osapi.h` - OS abstraction (self-dependency)
- `source/code/parse/parselo.h` - Configuration parsing (self-dependency)
- `source/code/physics/physics.h` - Physics simulation
- `source/code/render/` (3d.h, rendering files) - 3D rendering
- `source/code/ship/` (ship.h, weapon systems) - Ship management
- `source/code/sound/` (sound.h, audio files) - Audio system
- `source/code/weapon/` (weapons.cpp, beam systems) - Weapon systems

### File: `source/code/globalincs/globals.h` included/used by:
**Usage**: Game-wide constants and limits used by core systems
- `source/code/ai/ai.h` - AI system configuration limits
- `source/code/ai/aigoals.h` - AI goal system limits
- `source/code/ai/ai_profiles.h` - AI profile constraints
- `source/code/freespace2/freespace.h` - Main game constants
- `source/code/hud/` (hudconfig.h, hudtarget.h) - HUD element limits
- `source/code/mission/` (missionparse.h, campaign files) - Mission constraints
- `source/code/network/` (multi.h, multiplayer files) - Network limits
- `source/code/object/object.h` - Object system limits (MAX_OBJECTS)
- `source/code/parse/parselo.h` - Parsing buffer sizes
- `source/code/ship/ship.h` - Ship system limits (MAX_SHIPS, MAX_SHIP_CLASSES)
- `source/code/weapon/weapons.cpp` - Weapon system limits (MAX_WEAPONS)

## File System Layer Dependencies

### File: `source/code/cfile/cfile.h` included/used by:
**Usage**: Universal file I/O interface for asset loading
- `source/code/anim/animplay.cpp` - Animation file loading
- `source/code/anim/animplay.h` - Animation system interface
- `source/code/autopilot/autopilot.cpp` - Autopilot configuration loading
- `source/code/bmpman/bmpman.cpp` - Bitmap/texture file loading
- `source/code/bmpman/bmpman.h` - Bitmap management interface
- `source/code/cfile/cfilearchive.cpp` - VP archive implementation (self-dependency)
- `source/code/cfile/cfilelist.cpp` - File listing operations (self-dependency)
- `source/code/cfile/cfilesystem.cpp` - File system utilities (self-dependency)
- `source/code/cutscene/cutscenes.cpp` - Video file access
- `source/code/ddsutils/ddsutils.cpp` - DDS texture loading
- `source/code/fred2/` (mission editor files) - Mission file operations
- `source/code/freespace2/freespace.cpp` - Main game file operations
- `source/code/gamesnd/gamesnd.cpp` - Sound file loading
- `source/code/graphics/` (bitmap loaders, texture management) - Asset loading
- `source/code/hud/` (HUD configuration files) - UI asset loading
- `source/code/jpgutils/jpgutils.cpp` - JPEG image loading
- `source/code/localization/localize.cpp` - Localization file access
- `source/code/menuui/` (menu systems) - UI asset loading
- `source/code/mission/` (mission loading, campaign files) - Mission data access
- `source/code/model/` (3D model loading) - Model file access
- `source/code/palman/palman.cpp` - Palette file management
- `source/code/parse/parselo.h` - Configuration file access (critical dependency)
- `source/code/pcxutils/pcxutils.cpp` - PCX image loading
- `source/code/pngutils/pngutils.cpp` - PNG image loading
- `source/code/ship/ship.cpp` - Ship definition file loading
- `source/code/sound/` (audio file loading) - Sound asset access
- `source/code/species_defs/species_defs.cpp` - Species definition files
- `source/code/tgautils/tgautils.cpp` - TGA image loading
- `source/code/weapon/weapons.cpp` - Weapon definition file loading

### File: `source/code/cfile/cfilearchive.h` included/used by:
**Usage**: Internal VP archive management structures
- `source/code/cfile/cfile.cpp` - Core file I/O implementation (self-dependency)
- `source/code/cfile/cfilearchive.cpp` - VP archive implementation (self-dependency)

## Mathematical Utilities Dependencies

### File: `source/code/math/vecmat.h` included/used by:
**Usage**: 3D mathematics for physics, rendering, and game logic
- `source/code/asteroid/asteroid.cpp` - Asteroid field positioning
- `source/code/camera/camera.cpp` - Camera positioning and orientation
- `source/code/fireball/warpineffect.cpp` - Warp effect calculations
- `source/code/fred2/fredrender.cpp` - FRED2 3D rendering
- `source/code/fred2/fredview.cpp` - FRED2 viewport management
- `source/code/fred2/wing.cpp` - Wing formation positioning
- `source/code/graphics/gropengltexture.cpp` - Texture coordinate transformations
- `source/code/graphics/gropengltnl.cpp` - Transform and lighting
- `source/code/hud/hudartillery.cpp` - Artillery targeting calculations
- `source/code/io/joy_ff.cpp` - Force feedback vector calculations
- `source/code/jumpnode/jumpnode.cpp` - Jump node positioning
- `source/code/lighting/lighting.cpp` - Light vector calculations
- `source/code/mission/missiongrid.cpp` - Mission grid coordinates
- `source/code/model/` (modelinterp.cpp, modelcollide.cpp) - 3D model transformations
- `source/code/nebula/neb.cpp` - Nebula effect positioning
- `source/code/object/` (object.cpp, collision systems) - Object physics
- `source/code/particle/particle.cpp` - Particle system positioning
- `source/code/physics/physics.cpp` - Physics simulation
- `source/code/radar/radar.cpp` - Radar positioning calculations
- `source/code/render/` (3D rendering pipeline) - 3D transformations
- `source/code/ship/` (ship movement, collision) - Ship physics
- `source/code/starfield/` (starfield.cpp, nebula.cpp) - Background positioning
- `source/code/weapon/` (projectile physics, beam calculations) - Weapon physics

### File: `source/code/math/fix.h` included/used by:
**Usage**: Fixed-point arithmetic for deterministic calculations
- `source/code/globalincs/pstypes.h` - Core type definitions (self-dependency)
- `source/code/math/floating.h` - Floating-point utilities
- `source/code/io/timer.h` - Timing calculations
- `source/code/physics/physics.cpp` - Deterministic physics
- Network synchronization systems (for consistent calculations)

### File: `source/code/math/fvi.h` included/used by:
**Usage**: Find Vector Intersection for collision detection
- `source/code/object/objcollide.cpp` - Object collision detection
- `source/code/object/collidedebrisship.cpp` - Debris-ship collisions
- `source/code/object/collideshipship.cpp` - Ship-ship collisions
- `source/code/object/collideshipweapon.cpp` - Ship-weapon collisions
- `source/code/weapon/` (projectile collision) - Weapon impact detection
- `source/code/physics/physics.cpp` - Movement collision checking

## Data Parsing Framework Dependencies

### File: `source/code/parse/parselo.h` included/used by:
**Usage**: Configuration and data file parsing across all game systems
- `source/code/ai/aicode.cpp` - AI configuration parsing
- `source/code/ai/ai_profiles.cpp` - AI profile definitions
- `source/code/asteroid/asteroid.cpp` - Asteroid field configuration
- `source/code/autopilot/autopilot.cpp` - Autopilot settings
- `source/code/bmpman/bmpman.cpp` - Bitmap configuration
- `source/code/camera/camera.cpp` - Camera settings
- `source/code/cutscene/cutscenes.cpp` - Cutscene definitions
- `source/code/fireball/fireballs.cpp` - Explosion effects configuration
- `source/code/fred2/` (30+ FRED2 files) - Mission editor parsing
- `source/code/freespace2/freespace.cpp` - Game configuration
- `source/code/gamesnd/gamesnd.cpp` - Sound configuration
- `source/code/graphics/` (graphics settings) - Rendering configuration
- `source/code/hud/` (HUD configuration files) - UI settings
- `source/code/iff_defs/iff_defs.cpp` - IFF (faction) definitions
- `source/code/jumpnode/jumpnode.cpp` - Jump node configuration
- `source/code/lighting/lighting.cpp` - Lighting configuration
- `source/code/localization/localize.cpp` - Localization settings
- `source/code/menuui/` (menu configuration) - UI definitions
- `source/code/mission/` (mission parsing, campaigns) - Mission data parsing
- `source/code/model/modelread.cpp` - 3D model metadata parsing
- `source/code/nebula/neb.cpp` - Nebula configuration
- `source/code/network/` (multiplayer settings) - Network configuration
- `source/code/object/parseobjectdock.cpp` - Object docking definitions
- `source/code/particle/particle.cpp` - Particle effect configuration
- `source/code/radar/radarsetup.cpp` - Radar configuration
- `source/code/ship/ship.cpp` - Ship class definitions (critical)
- `source/code/sound/sound.cpp` - Audio configuration
- `source/code/species_defs/species_defs.cpp` - Species definitions
- `source/code/starfield/starfield.cpp` - Background configuration
- `source/code/stats/medals.cpp` - Medal definitions
- `source/code/weapon/weapons.cpp` - Weapon class definitions (critical)

### File: `source/code/parse/sexp.h` included/used by:
**Usage**: S-expression scripting for mission logic
- `source/code/fred2/sexp_tree.cpp` - FRED2 S-expression editor
- `source/code/fred2/` (mission editor files) - Mission scripting interface
- `source/code/mission/missiongoals.cpp` - Mission goal scripting
- `source/code/mission/missionparse.cpp` - Mission script parsing
- `source/code/mission/missionmessage.cpp` - Message scripting
- `source/code/parse/scripting.cpp` - General scripting support

## Platform Abstraction Dependencies

### File: `source/code/osapi/osapi.h` included/used by:
**Usage**: Operating system services and window management
- `source/code/freespace2/freespace.cpp` - Main application initialization
- `source/code/gamesequence/gamesequence.cpp` - Game state management
- `source/code/graphics/` (window management, rendering context) - Graphics initialization
- `source/code/io/` (input systems) - Input device management
- `source/code/network/` (networking initialization) - Network stack setup
- `source/code/osapi/osregistry.h` - Registry access (self-dependency)
- `source/code/sound/` (audio initialization) - Audio system setup

### File: `source/code/osapi/outwnd.h` included/used by:
**Usage**: Debug output and logging throughout the engine
- `source/code/globalincs/pstypes.h` - Core debug macros (self-dependency)
- Virtually ALL WCS source files via mprintf() and nprintf() macros
- `source/code/ai/` (AI debugging) - AI system logging
- `source/code/graphics/` (rendering debugging) - Graphics debugging
- `source/code/network/` (network debugging) - Network logging
- `source/code/physics/` (physics debugging) - Physics simulation logging
- Error reporting and diagnostic systems throughout the codebase

## Timing and Input Dependencies

### File: `source/code/io/timer.h` included/used by:
**Usage**: Timing and frame management across all game systems
- `source/code/freespace2/freespace.cpp` - Main game loop timing
- `source/code/gamesequence/gamesequence.cpp` - Game state timing
- `source/code/ai/` (AI update timing) - AI system scheduling
- `source/code/graphics/` (frame timing) - Rendering synchronization
- `source/code/hud/` (HUD updates) - UI refresh timing
- `source/code/mission/` (mission timing) - Mission event scheduling
- `source/code/network/` (network timing) - Network synchronization
- `source/code/object/object.cpp` - Object update scheduling
- `source/code/physics/physics.cpp` - Physics simulation timing
- `source/code/ship/` (ship systems) - Ship update timing
- `source/code/sound/` (audio timing) - Audio synchronization
- `source/code/weapon/` (weapon timing) - Weapon fire timing

### File: `source/code/io/key.h` included/used by:
**Usage**: Keyboard input processing
- `source/code/controlconfig/controlsconfig.cpp` - Control configuration
- `source/code/freespace2/freespace.cpp` - Main input processing
- `source/code/gamesequence/gamesequence.cpp` - Game state input
- `source/code/fred2/` (editor input) - FRED2 keyboard controls
- `source/code/menuui/` (menu navigation) - UI input handling
- `source/code/playerman/playercontrol.cpp` - Player control input

## Summary of Critical Dependency Relationships

**Most Depended Upon Files**:
1. `pstypes.h` - Universal foundation (used by 100+ files)
2. `cfile.h` - Universal file access (used by 50+ files)  
3. `vecmat.h` - 3D mathematics (used by 40+ files)
4. `parselo.h` - Configuration parsing (used by 35+ files)
5. `timer.h` - Timing services (used by 25+ files)

**Dependency Depth**: Foundation headers create 3-4 levels of dependency chains where changes to core files can impact dozens of dependent systems.

**Critical Path Analysis**: The foundation layer forms the base of a dependency pyramid where `pstypes.h` → `cfile.h`/`vecmat.h` → `parselo.h` → game systems represents the typical dependency flow.
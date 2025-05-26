# WCS System: Core Foundation Infrastructure - Source Files List

## Global Includes Module (globalincs/)

- `source/code/globalincs/pstypes.h`: Primary type definitions including vec3d, matrix, vertex structures, mathematical constants (PI, ANG_TO_RAD), platform-specific typedefs (fix, longlong, ubyte), assertion macros (Assert, Verify), memory management interfaces (vm_malloc, vm_free), and debug console framework (DCF macros)
- `source/code/globalincs/globals.h`: Game-wide constants and limits including MAX_SHIPS (400), MAX_SHIP_CLASSES (130/250), MAX_WEAPONS (700), MAX_WEAPON_TYPES (200/300), MAX_OBJECTS (2000), and mission/player name length definitions
- `source/code/globalincs/alphacolors.cpp`: Implementation of predefined alpha color constants for rendering systems
- `source/code/globalincs/alphacolors.h`: Declarations for alpha color constants used throughout the rendering pipeline
- `source/code/globalincs/crypt.cpp`: Implementation of jcrypt() function for simple string encryption with CRYPT_STRING_LENGTH (17) fixed-size output
- `source/code/globalincs/crypt.h`: Interface for cryptographic string operations with jcrypt() function declaration
- `source/code/globalincs/def_files.cpp`: Implementation of definition file management and flag_def_list structure handling
- `source/code/globalincs/def_files.h`: Interface for managing definition files and flag-based lookup systems
- `source/code/globalincs/linklist.h`: Template-based linked list data structure with type-safe insertion, deletion, and traversal operations
- `source/code/globalincs/mspdb_callstack.cpp`: Microsoft-specific debug callstack generation for crash reporting and debugging
- `source/code/globalincs/mspdb_callstack.h`: Interface for callstack generation and symbol resolution on Windows
- `source/code/globalincs/safe_strings.cpp`: Implementation of cross-platform safe string functions including scp_strcpy_s() and scp_strcat_s() with bounds checking
- `source/code/globalincs/safe_strings.h`: Interface for ISO/IEC TR 24731 compliant safe string functions with template overloads for automatic size detection and platform compatibility macros
- `source/code/globalincs/systemvars.cpp`: Implementation of system-wide variable management and global configuration state
- `source/code/globalincs/systemvars.h`: Interface for system variables and runtime configuration access
- `source/code/globalincs/version.cpp`: Implementation of version tracking, build information, and compatibility checking
- `source/code/globalincs/version.h`: Interface for version information access and build metadata
- `source/code/globalincs/vmallocator.h`: Custom memory allocator with debugging, tracking, and leak detection capabilities
- `source/code/globalincs/windebug.cpp`: Windows-specific debugging utilities including crash handling and debug output

## Operating System Abstraction Module (osapi/)

- `source/code/osapi/osapi.cpp`: Core implementation of cross-platform OS services including os_init(), os_poll(), os_sleep(), window management, and process control
- `source/code/osapi/osapi.h`: Interface for operating system abstraction with platform detection macros, window management functions, and threading support definitions
- `source/code/osapi/osapi_unix.cpp`: Unix/Linux-specific implementation of OS abstraction layer with SDL integration and POSIX-compliant operations
- `source/code/osapi/osregistry.cpp`: Windows registry abstraction implementation for configuration persistence using RegOpenKeyEx and related APIs
- `source/code/osapi/osregistry.h`: Interface for registry operations with cross-platform configuration storage abstraction
- `source/code/osapi/osregistry_unix.cpp`: Unix equivalent of registry functionality using ~/.fs2_open/ configuration files and directories
- `source/code/osapi/outwnd.cpp`: Implementation of debug output window with categorized logging (OUTWND_NO_FILTER, OUTWND_FILTER_*) and file output
- `source/code/osapi/outwnd.h`: Interface for debug output system with outwnd_printf(), mprintf(), and nprintf() macros
- `source/code/osapi/outwnd_unix.cpp`: Unix-specific implementation of debug output to console and log files

## File System Layer Module (cfile/)

- `source/code/cfile/cfile.cpp`: Core implementation of unified file I/O system supporting CFILE structure, VP archive integration, cfopen(), cfread(), cfwrite(), cfseek(), memory-mapped file access, and file type routing (CF_TYPE_* constants)
- `source/code/cfile/cfile.h`: Primary interface for file operations including 37 file type definitions (CF_TYPE_DATA through CF_TYPE_FICTION), CFILE structure, and comprehensive file I/O API with localization support
- `source/code/cfile/cfilearchive.cpp`: Implementation of VP archive management including file table parsing, directory simulation, extraction algorithms, and memory-mapped access
- `source/code/cfile/cfilearchive.h`: Internal structures for VP archive management including Cfile_block structure, CFILE_BLOCK_UNUSED/USED states, and MAX_CFILE_BLOCKS (64) pool management
- `source/code/cfile/cfilelist.cpp`: Implementation of file listing operations with cf_get_file_list(), directory traversal, and filtering support
- `source/code/cfile/cfilesystem.cpp`: High-level file system operations including cfile_init(), directory creation, path resolution, and cross-platform file utilities

## Mathematical Utilities Module (math/)

- `source/code/math/vecmat.cpp`: Comprehensive implementation of 3D vector and matrix mathematics including vm_vec_add(), vm_vec_normalize(), vm_vec_crossprod(), vm_angles_2_matrix(), transformation operations, and geometric calculations
- `source/code/math/vecmat.h`: Interface for 3D mathematics with 522 lines of vector operations, matrix transformations, plane calculations (vm_dist_to_plane), interpolation functions, and geometric utilities supporting both inline and function call variants
- `source/code/math/fix.cpp`: Implementation of fixed-point arithmetic operations including fixmul(), fixdiv(), fixmuldiv() for deterministic 16.16 format calculations
- `source/code/math/fix.h`: Interface for fixed-point mathematics with F1_0 (65536) constant, f2i()/i2f() conversion macros, and deterministic arithmetic operations
- `source/code/math/floating.cpp`: Implementation of floating-point utilities, precision management, and performance optimizations for real-time calculations
- `source/code/math/floating.h`: Interface for floating-point mathematical operations and precision control
- `source/code/math/fvi.cpp`: Implementation of Find Vector Intersection algorithms for collision detection, ray-sphere intersections, and geometric queries
- `source/code/math/fvi.h`: Interface for vector intersection calculations and collision detection primitives
- `source/code/math/spline.cpp`: Implementation of spline interpolation mathematics for smooth curve generation and path following
- `source/code/math/spline.h`: Interface for spline calculations and curve interpolation operations
- `source/code/math/staticrand.cpp`: Implementation of deterministic random number generation with myrand() and rand32() functions for consistent cross-platform behavior
- `source/code/math/staticrand.h`: Interface for static random number generators with seeding and reproducible sequences

## Data Parsing Framework Module (parse/)

- `source/code/parse/parselo.cpp`: Core implementation of configuration file parsing engine supporting .cfg/.tbl files with Mission_text buffer (1MB), required_string(), stuff_string(), stuff_float(), and extensive data type handling for 238 lines of parsing interface
- `source/code/parse/parselo.h`: Primary interface for parsing operations including F_NAME through F_LNAME type definitions, MAX_TMP_STRING_LENGTH (16384), parsing state management (Mp pointer), and comprehensive data stuffing functions
- `source/code/parse/lua.cpp`: Implementation of Lua scripting integration for advanced configuration and mission scripting with engine integration
- `source/code/parse/lua.h`: Interface for Lua script execution and integration with the parsing system
- `source/code/parse/sexp.cpp`: Implementation of S-expression parser for LISP-like mission scripting, conditional logic evaluation, and scripting hooks
- `source/code/parse/sexp.h`: Interface for S-expression parsing, evaluation, and mission logic processing with script_hook structure
- `source/code/parse/scripting.cpp`: Implementation of general scripting framework supporting multiple scripting languages and hook management
- `source/code/parse/scripting.h`: Interface for scripting system management and script execution coordination
- `source/code/parse/encrypt.cpp`: Implementation of file encryption and decryption for secure parsing of protected content
- `source/code/parse/encrypt.h`: Interface for encryption operations during file parsing and data protection

## Input/Output and Timing Module (io/)

- `source/code/io/timer.cpp`: Implementation of high-precision timing system including timestamp management, timer_get_fixed_seconds(), frame timing, and performance measurement with TIMESTAMP_FREQUENCY (1000)
- `source/code/io/timer.h`: Interface for timing operations with millisecond precision, timestamp(), timestamp_elapsed() macros, and comprehensive timing utilities supporting up to 600-hour runtime periods
- `source/code/io/key.cpp`: Implementation of keyboard input management with key mapping, state tracking, and cross-platform input processing
- `source/code/io/key.h`: Interface for keyboard input handling including key codes, state queries, and input event management
- `source/code/io/mouse.cpp`: Implementation of mouse input management with position tracking, button states, and cursor control
- `source/code/io/mouse.h`: Interface for mouse input operations including position queries, button state management, and cursor utilities
- `source/code/io/joy.cpp`: Implementation of joystick/gamepad input handling with device enumeration, axis reading, and state management
- `source/code/io/joy.h`: Interface for joystick input operations including device detection, calibration, and button state queries
- `source/code/io/joy-unix.cpp`: Unix-specific implementation of joystick input handling using platform-specific APIs and device drivers
- `source/code/io/joy_ff.cpp`: Implementation of force feedback operations for joysticks and game controllers with effect management
- `source/code/io/joy_ff.h`: Interface for force feedback effects and haptic device control
- `source/code/io/swff_lib.cpp`: SideWinder Force Feedback library implementation for Microsoft gaming devices
- `source/code/io/sw_error.hpp`: Error handling definitions for SideWinder force feedback operations
- `source/code/io/sw_force.h`: Force feedback effect definitions and constants for SideWinder devices
- `source/code/io/sw_guid.hpp`: GUID definitions for SideWinder device identification

## Command Line Processing Module (cmdline/)

- `source/code/cmdline/cmdline.cpp`: Implementation of command line argument parsing with 150+ options including graphics settings (Cmdline_spec, Cmdline_glow), gameplay options (Cmdline_3dwarp), network settings (Cmdline_network_port), and development flags
- `source/code/cmdline/cmdline.h`: Interface for command line processing with extern declarations for all supported game options including retail options, FSO-specific features, troubleshooting flags, and developer settings

## Additional Utility Modules

- `source/code/cryptstring/cryptstring.cpp`: Implementation of encrypted string storage and management for sensitive data protection in configuration files

## Boost Library Integration (boost/)

- `source/code/boost/`: External Boost C++ library headers providing advanced data structures, algorithms, and utilities used throughout the codebase for template metaprogramming, smart pointers, and cross-platform functionality

## Platform-Specific Modules

- `source/code/windows_stub/config.h`: Windows platform configuration definitions and compatibility macros
- `source/code/windows_stub/stubs.cpp`: Windows-specific stub implementations for cross-platform compatibility

## Total File Count: 58+ Core Foundation Files
- **Header Files (.h)**: 25+ interface definitions with comprehensive API specifications
- **Implementation Files (.cpp)**: 33+ source implementations with full functionality
- **Platform-Specific Files**: 6+ files for Windows/Unix compatibility
- **External Libraries**: Boost integration with 100+ header files
- **Lines of Code**: Approximately 25,000+ lines across all foundation modules
- **Key Dependencies**: Platform SDKs (Windows API, POSIX), C++ Standard Library, Boost libraries, potentially Lua runtime
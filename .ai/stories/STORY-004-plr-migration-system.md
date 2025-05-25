# User Story: PLR File Migration System

**Story ID**: STORY-004  
**Story Title**: PLR File Migration System  
**Epic**: Data Migration Foundation (EPIC-001)  
**Priority**: High  
**Estimated Effort**: 3 days  
**Story Manager**: SallySM  

## Story Definition

**As a** WCS player transitioning to WCS-Godot  
**I want** my existing pilot files (.PLR) automatically converted to the new Godot format  
**So that** I can continue playing with all my pilot progression, statistics, and settings preserved without any data loss

## Acceptance Criteria

### Core Migration Functionality
- [ ] **PLR File Detection**: Automatically detect and locate WCS .PLR files in standard directories
- [ ] **Binary Parser**: Parse WCS .PLR binary format including version 242 (single) and 142 (multi)
- [ ] **Data Extraction**: Extract all pilot data including callsign, stats, campaign progress, settings
- [ ] **Resource Conversion**: Convert extracted data to PlayerProfile and related resources
- [ ] **Validation System**: Validate converted data integrity and completeness

### File Format Support
- [ ] **Version Compatibility**: Support PLR versions from 140 (release compatibility) to 242 (current)
- [ ] **Multi/Single Support**: Handle both multiplayer (.PLR) and single player (.PLR) file formats
- [ ] **Signature Validation**: Verify PLR file signature (0x46505346 "FPSF")
- [ ] **Corrupt File Handling**: Gracefully handle partially corrupted PLR files
- [ ] **Large File Support**: Handle PLR files with extensive pilot histories

### Data Mapping and Conversion
- [ ] **Pilot Identity**: Convert callsign, image_filename, squad_name, squad_filename
- [ ] **Statistics Migration**: Convert scoring_struct to PilotStatistics resource
- [ ] **Campaign Progress**: Convert campaign info and progression states
- [ ] **Control Settings**: Convert key bindings and control configuration
- [ ] **HUD Configuration**: Convert HUD layout and display preferences
- [ ] **Achievement Data**: Convert medals, ranks, and achievement progression

### Migration Process Management
- [ ] **Batch Migration**: Support migrating multiple PLR files in one operation
- [ ] **Progress Reporting**: Detailed progress feedback during migration process
- [ ] **Error Recovery**: Continue migration despite individual file failures
- [ ] **Backup Creation**: Create backup of original PLR files before migration
- [ ] **Validation Report**: Generate detailed report of migration results and any issues

## Technical Requirements

### Architecture Reference
- **Architecture Document**: `.ai/docs/wcs-data-architecture.md` (DataManager → MigrationManager)
- **WCS Analysis Reference**: `.ai/docs/wcs-data-migration-analysis.md` (PLR format analysis)

### WCS Integration Points
- **Source Reference**: `source/code/playerman/managepilot.cpp:566-599` (read_pilot_file)
- **Data Structure**: `source/code/playerman/player.h:89-150` (player struct)
- **File Format**: Binary .PLR with CFILE system, versions 140-242

### Godot Implementation Details
```gdscript
class_name PLRMigrator
extends Node

signal migration_started(file_count: int)
signal migration_progress(current_file: int, total_files: int, progress: float)
signal file_migration_completed(file_path: String, success: bool, errors: Array[String])
signal migration_completed(successful: int, failed: int, total: int)

@export var auto_detect_plr_files: bool = true
@export var create_backups: bool = true
@export var validate_after_migration: bool = true

# Core migration methods
func detect_plr_files() -> Array[String]:
func migrate_plr_file(file_path: String) -> MigrationResult:
func migrate_multiple_plr_files(file_paths: Array[String]) -> Array[MigrationResult]:
func validate_plr_file(file_path: String) -> PLRValidationResult:

# Data parsing methods
func parse_plr_header(file: FileAccess) -> PLRHeader:
func parse_pilot_data(file: FileAccess, version: int) -> Dictionary:
func parse_statistics(file: FileAccess, version: int) -> Dictionary:
func parse_campaign_data(file: FileAccess, version: int) -> Dictionary:
func parse_control_config(file: FileAccess, version: int) -> Dictionary:

# Conversion methods
func convert_to_player_profile(plr_data: Dictionary) -> PlayerProfile:
func convert_statistics(stats_data: Dictionary) -> PilotStatistics:
func convert_campaign_info(campaign_data: Dictionary) -> Array[CampaignInfo]:
func convert_control_config(control_data: Dictionary) -> ControlConfiguration:
```

### PLR File Structure Support
```gdscript
class_name PLRHeader
extends Resource

@export var signature: int  # 0x46505346 "FPSF"
@export var version: int    # 140-242
@export var pilot_name: String
@export var file_size: int
@export var checksum: int

class_name MigrationResult
extends Resource

@export var source_file: String
@export var success: bool
@export var target_profile: PlayerProfile
@export var errors: Array[String]
@export var warnings: Array[String]
@export var migration_time: float

class_name PLRValidationResult
extends Resource

@export var is_valid: bool
@export var version: int
@export var pilot_name: String
@export var file_size: int
@export var validation_errors: Array[String]
```

### Performance Requirements
- **Migration Speed**: < 10 seconds per PLR file for typical files
- **Large File Support**: Handle PLR files up to 50MB without memory issues
- **Concurrent Processing**: Support background migration without blocking UI
- **Memory Usage**: < 100MB memory overhead during migration process

## Dependencies

### Prerequisites
- **Architecture Approved**: ✅ Godot data architecture document approved
- **PlayerProfile Ready**: Requires STORY-001 (PlayerProfile Resource) completion
- **Save System Ready**: Requires STORY-003 (Save Game Manager) completion

### Resource Dependencies
- **PlayerProfile Resource**: Target format for converted pilot data
- **PilotStatistics Resource**: Statistics data structure
- **CampaignInfo Resource**: Campaign progression data structure
- **ControlConfiguration Resource**: Control settings data structure

### Integration Dependencies
- **SaveGameManager**: For persisting converted profiles
- **DataManager**: For registering migrated profiles
- **File System Access**: Access to WCS data directories and user data

## Definition of Done

### Code Quality
- [ ] **Static Typing**: All migration operations are statically typed
- [ ] **Documentation**: Complete API documentation for all public methods
- [ ] **Code Standards**: Follows project GDScript coding standards
- [ ] **Error Handling**: Comprehensive error handling for all failure scenarios

### Testing Requirements
- [ ] **Unit Tests**: Tests for all PLR parsing and conversion functions
- [ ] **Integration Tests**: End-to-end migration testing with real PLR files
- [ ] **Version Tests**: Tests for all supported PLR file versions (140-242)
- [ ] **Corruption Tests**: Tests for handling corrupted and malformed PLR files
- [ ] **Performance Tests**: Validation of migration performance requirements

### Functional Requirements
- [ ] **Complete Data Migration**: All PLR data successfully converted without loss
- [ ] **Version Compatibility**: Support for all PLR versions from 140-242
- [ ] **Error Resilience**: Graceful handling of all error conditions
- [ ] **Progress Feedback**: Clear progress reporting during migration
- [ ] **Data Validation**: Comprehensive validation of migrated data integrity

### Integration Requirements
- [ ] **Save System Integration**: Migrated profiles properly saved using SaveGameManager
- [ ] **DataManager Integration**: Migrated profiles registered with DataManager
- [ ] **UI Integration**: Progress feedback through migration UI
- [ ] **Cross-Platform**: Verified functionality on Windows and Linux

## Implementation Guidance

### Technical Approach
1. **File Detection**: Scan standard WCS directories for PLR files
2. **Binary Parsing**: Implement robust binary parser for PLR format
3. **Version Handling**: Support all PLR versions with appropriate parsers
4. **Data Conversion**: Map PLR data structures to Godot resources
5. **Validation**: Comprehensive validation of converted data

### Code Patterns
- **Parser Pattern**: Structured parsing with version-specific handlers
- **Factory Pattern**: Create appropriate resource types based on PLR data
- **Strategy Pattern**: Different parsing strategies for different PLR versions
- **Observer Pattern**: Progress notifications through signal system
- **Chain of Responsibility**: Validation pipeline for migrated data

### Risk Mitigation
- **Data Loss**: Multiple validation steps and backup creation
- **Version Incompatibility**: Comprehensive version detection and handling
- **Corruption**: Robust error handling and partial data recovery
- **Performance**: Streaming parsing for large files
- **Memory Usage**: Efficient parsing without loading entire file into memory

## Migration Process Flow

### Detection Phase
1. **Directory Scanning**: Scan WCS installation and user directories
2. **File Validation**: Verify PLR file signatures and basic structure
3. **Version Detection**: Determine PLR version for appropriate parsing
4. **Duplicate Detection**: Handle multiple versions of same pilot

### Parsing Phase
1. **Header Parsing**: Read and validate PLR file header
2. **Data Extraction**: Extract pilot data using version-specific parser
3. **Structure Validation**: Validate data structure integrity
4. **Error Recovery**: Handle parsing errors and data corruption

### Conversion Phase
1. **Resource Creation**: Create PlayerProfile and related resources
2. **Data Mapping**: Map PLR data to Godot resource properties
3. **Validation**: Validate converted data completeness and integrity
4. **Persistence**: Save converted profile using SaveGameManager

## Edge Cases and Error Handling

### File System Issues
- **Missing Files**: Handle cases where PLR files are moved or deleted
- **Permission Issues**: Handle read permission problems
- **Corrupted Files**: Gracefully handle partially corrupted PLR files
- **Large Files**: Handle exceptionally large PLR files efficiently

### Data Conversion Issues
- **Invalid Data**: Handle invalid or out-of-range data values
- **Missing Fields**: Handle PLR files with missing expected data
- **Version Differences**: Handle differences between PLR versions
- **Character Encoding**: Handle different character encodings in pilot names

## Handoff Notes for Dev

### Critical Implementation Details
- **Binary Parsing**: PLR files use little-endian byte order
- **Version Handling**: Version differences affect data structure layout
- **Data Integrity**: Maintain complete data integrity during conversion
- **Performance**: Large PLR files require streaming parsing approach

### Testing Priorities
- **Real Data Testing**: Test with actual WCS PLR files from users
- **Version Coverage**: Test all supported PLR versions
- **Error Scenarios**: Test with corrupted and malformed files
- **Performance Testing**: Test migration performance with large files

### Integration Requirements
- **SaveGameManager**: Must integrate with save system for persistence
- **UI System**: Provide progress feedback during migration
- **Error Reporting**: Clear error messages for migration failures
- **Backup System**: Ensure original files are safely backed up

---

**Story Manager**: SallySM  
**Story Status**: Ready for Implementation  
**Created**: 2025-01-25  
**Last Reviewed**: 2025-01-25  

**BMAD Compliance**: Story follows BMAD methodology, references approved architecture, includes comprehensive acceptance criteria and clear Definition of Done. Dependencies on foundation stories clearly defined.
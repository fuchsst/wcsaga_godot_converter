# EPIC-003: Data Migration & Conversion Tools Architecture

## Architecture Overview

The Data Migration & Conversion Tools system provides comprehensive utilities for converting WCS assets and data structures into Godot-compatible formats, enabling seamless migration of existing WCS content while maintaining data integrity and visual fidelity.

## System Goals

- **Complete Asset Coverage**: Convert all WCS asset types (POF models, VP archives, textures, audio, missions)
- **Automation**: Minimize manual intervention through intelligent batch processing
- **Fidelity**: Preserve original asset quality and characteristics
- **Performance**: Efficient conversion with progress tracking and resumable operations
- **Integration**: Seamless integration with Godot project structure and EPIC-002 asset management

## Core Architecture

### Conversion Pipeline Hierarchy

```
ConversionManager (Python CLI)
├── VPArchiveExtractor (Python)
├── POFModelConverter (Python + Blender)
├── MissionFileConverter (Python)
├── TextureConverter (Python + ImageMagick)
├── AudioVideoConverter (Python + FFmpeg)
├── GodotProjectIntegrator (Python + Godot)
└── ValidationSystem (Python)
```

### Python-Based Conversion Framework

**ConversionManager (Main CLI Tool)**
```python
#!/usr/bin/env python3
"""
WCS to Godot Asset Conversion Manager
Orchestrates the conversion of all WCS assets to Godot-compatible formats
"""

import argparse
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

@dataclass
class ConversionJob:
    """Represents a single conversion task"""
    source_path: Path
    target_path: Path
    conversion_type: str
    priority: int
    dependencies: List[str]
    status: str = "pending"
    progress: float = 0.0
    error_message: Optional[str] = None

class ConversionManager:
    """Main conversion orchestrator"""
    
    def __init__(self, wcs_source_dir: Path, godot_target_dir: Path):
        self.wcs_source_dir = wcs_source_dir
        self.godot_target_dir = godot_target_dir
        self.conversion_queue: List[ConversionJob] = []
        self.completed_jobs: List[ConversionJob] = []
        self.failed_jobs: List[ConversionJob] = []
        
        # Initialize converters
        self.vp_extractor = VPArchiveExtractor()
        self.pof_converter = POFModelConverter()
        self.mission_converter = MissionFileConverter()
        self.texture_converter = TextureConverter()
        self.audio_converter = AudioVideoConverter()
        self.integrator = GodotProjectIntegrator()
        self.validator = ValidationSystem()
    
    def scan_wcs_assets(self) -> Dict[str, List[Path]]:
        """Scan WCS directory for convertible assets"""
        assets = {
            'vp_archives': list(self.wcs_source_dir.glob('**/*.vp')),
            'pof_models': list(self.wcs_source_dir.glob('**/*.pof')),
            'missions': list(self.wcs_source_dir.glob('**/*.fs2')),
            'textures': list(self.wcs_source_dir.glob('**/*.{pcx,tga,dds,png,jpg}')),
            'audio': list(self.wcs_source_dir.glob('**/*.{wav,ogg}')),
            'video': list(self.wcs_source_dir.glob('**/*.{mve,avi,mp4}')),
            'tables': list(self.wcs_source_dir.glob('**/*.tbl')),
            'scripts': list(self.wcs_source_dir.glob('**/*.lua'))
        }
        return assets
    
    def create_conversion_plan(self, assets: Dict[str, List[Path]]) -> List[ConversionJob]:
        """Create ordered conversion plan with dependencies"""
        jobs = []
        
        # Phase 1: Extract VP archives (highest priority - enables other conversions)
        for vp_file in assets['vp_archives']:
            job = ConversionJob(
                source_path=vp_file,
                target_path=self.godot_target_dir / "extracted" / vp_file.stem,
                conversion_type="vp_extraction",
                priority=1,
                dependencies=[]
            )
            jobs.append(job)
        
        # Phase 2: Convert core assets (depends on VP extraction)
        vp_deps = [f"vp_extraction:{vp.stem}" for vp in assets['vp_archives']]
        
        # POF models
        for pof_file in assets['pof_models']:
            job = ConversionJob(
                source_path=pof_file,
                target_path=self.godot_target_dir / "models" / f"{pof_file.stem}.glb",
                conversion_type="pof_model",
                priority=2,
                dependencies=vp_deps
            )
            jobs.append(job)
        
        # Textures
        for texture_file in assets['textures']:
            target_format = self._determine_texture_format(texture_file)
            job = ConversionJob(
                source_path=texture_file,
                target_path=self.godot_target_dir / "textures" / f"{texture_file.stem}.{target_format}",
                conversion_type="texture",
                priority=2,
                dependencies=vp_deps
            )
            jobs.append(job)
        
        # Phase 3: Convert content that depends on models/textures
        asset_deps = vp_deps + [f"pof_model:{pof.stem}" for pof in assets['pof_models']]
        
        # Mission files
        for mission_file in assets['missions']:
            job = ConversionJob(
                source_path=mission_file,
                target_path=self.godot_target_dir / "missions" / f"{mission_file.stem}.tres",
                conversion_type="mission",
                priority=3,
                dependencies=asset_deps
            )
            jobs.append(job)
        
        return sorted(jobs, key=lambda x: (x.priority, x.source_path.name))
    
    def execute_conversion_plan(self, jobs: List[ConversionJob], 
                              max_workers: int = 4) -> Tuple[int, int, int]:
        """Execute conversion plan with parallel processing"""
        completed_count = 0
        failed_count = 0
        
        # Group jobs by priority for sequential execution of phases
        priority_groups = {}
        for job in jobs:
            if job.priority not in priority_groups:
                priority_groups[job.priority] = []
            priority_groups[job.priority].append(job)
        
        # Execute each priority group
        for priority in sorted(priority_groups.keys()):
            group_jobs = priority_groups[priority]
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = []
                for job in group_jobs:
                    if self._check_dependencies_satisfied(job):
                        future = executor.submit(self._execute_single_job, job)
                        futures.append((future, job))
                
                # Wait for all jobs in this priority group
                for future, job in futures:
                    try:
                        result = future.result()
                        if result:
                            completed_count += 1
                            self.completed_jobs.append(job)
                        else:
                            failed_count += 1
                            self.failed_jobs.append(job)
                    except Exception as e:
                        job.error_message = str(e)
                        failed_count += 1
                        self.failed_jobs.append(job)
        
        return completed_count, failed_count, len(jobs)
```

### VP Archive Extraction

**VPArchiveExtractor**
```python
class VPArchiveExtractor:
    """Extracts files from WCS VP (Virtual Pack) archives"""
    
    def __init__(self):
        self.vp_header_size = 36
        self.dir_entry_size = 32
        
    def extract_vp_archive(self, vp_path: Path, output_dir: Path) -> bool:
        """Extract VP archive maintaining directory structure"""
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            
            with open(vp_path, 'rb') as vp_file:
                # Read VP header
                header = self._read_vp_header(vp_file)
                if not self._validate_vp_header(header):
                    raise ValueError(f"Invalid VP file: {vp_path}")
                
                # Read directory entries
                dir_entries = self._read_directory_entries(vp_file, header['num_files'])
                
                # Extract files
                extracted_count = 0
                for entry in dir_entries:
                    if self._extract_file_entry(vp_file, entry, output_dir):
                        extracted_count += 1
                
                logging.info(f"Extracted {extracted_count}/{len(dir_entries)} files from {vp_path.name}")
                return True
                
        except Exception as e:
            logging.error(f"Failed to extract VP archive {vp_path}: {e}")
            return False
    
    def _read_vp_header(self, vp_file) -> Dict:
        """Read and parse VP file header"""
        vp_file.seek(0)
        header_data = vp_file.read(self.vp_header_size)
        
        # VP file format: 
        # 4 bytes: signature ("VPVP")
        # 4 bytes: version
        # 4 bytes: directory offset
        # 4 bytes: number of files
        # ... additional header data
        
        import struct
        signature, version, dir_offset, num_files = struct.unpack('<4sIII', header_data[:16])
        
        return {
            'signature': signature.decode('ascii'),
            'version': version,
            'directory_offset': dir_offset,
            'num_files': num_files
        }
    
    def _extract_file_entry(self, vp_file, entry: Dict, output_dir: Path) -> bool:
        """Extract individual file from VP archive"""
        try:
            # Create output path maintaining directory structure
            file_path = output_dir / entry['filename']
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Read and write file data
            vp_file.seek(entry['data_offset'])
            file_data = vp_file.read(entry['file_size'])
            
            with open(file_path, 'wb') as output_file:
                output_file.write(file_data)
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to extract file {entry['filename']}: {e}")
            return False
```

### POF Model Conversion

**POFModelConverter**
```python
class POFModelConverter:
    """Converts WCS POF 3D models to Godot GLB format"""
    
    def __init__(self):
        self.blender_executable = self._find_blender_executable()
        self.conversion_script = self._create_blender_conversion_script()
    
    def convert_pof_to_glb(self, pof_path: Path, output_path: Path, 
                          texture_dir: Optional[Path] = None) -> bool:
        """Convert POF model to GLB using Blender"""
        try:
            # First, parse POF file to extract geometry data
            pof_data = self._parse_pof_file(pof_path)
            if not pof_data:
                return False
            
            # Create intermediate OBJ file for Blender import
            obj_path = output_path.with_suffix('.obj')
            if not self._write_obj_file(pof_data, obj_path, texture_dir):
                return False
            
            # Use Blender to convert OBJ to GLB
            if not self._blender_obj_to_glb(obj_path, output_path):
                return False
            
            # Clean up intermediate files
            obj_path.unlink(missing_ok=True)
            
            # Create Godot-specific .import file
            self._create_godot_import_file(output_path)
            
            logging.info(f"Successfully converted {pof_path.name} to {output_path.name}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to convert POF model {pof_path}: {e}")
            return False
    
    def _parse_pof_file(self, pof_path: Path) -> Optional[Dict]:
        """Parse POF file format and extract geometry data"""
        try:
            with open(pof_path, 'rb') as pof_file:
                # POF file structure:
                # Header with chunk information
                # TXTR chunk (texture references)
                # OBJ2 chunk (geometry data)
                # SPCL chunk (special points)
                # PATH chunk (collision paths)
                
                pof_data = {
                    'vertices': [],
                    'faces': [],
                    'textures': [],
                    'materials': [],
                    'collision_data': [],
                    'special_points': []
                }
                
                # Read POF header
                header = self._read_pof_header(pof_file)
                
                # Process each chunk
                for chunk_info in header['chunks']:
                    chunk_data = self._read_pof_chunk(pof_file, chunk_info)
                    self._process_pof_chunk(chunk_data, pof_data)
                
                return pof_data
                
        except Exception as e:
            logging.error(f"Failed to parse POF file {pof_path}: {e}")
            return None
    
    def _write_obj_file(self, pof_data: Dict, obj_path: Path, 
                       texture_dir: Optional[Path]) -> bool:
        """Write geometry data to OBJ file format"""
        try:
            with open(obj_path, 'w') as obj_file:
                # Write material library reference
                mtl_path = obj_path.with_suffix('.mtl')
                obj_file.write(f"mtllib {mtl_path.name}\n\n")
                
                # Write vertices
                for vertex in pof_data['vertices']:
                    obj_file.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
                
                # Write texture coordinates
                for texcoord in pof_data.get('texcoords', []):
                    obj_file.write(f"vt {texcoord[0]} {texcoord[1]}\n")
                
                # Write normals
                for normal in pof_data.get('normals', []):
                    obj_file.write(f"vn {normal[0]} {normal[1]} {normal[2]}\n")
                
                # Write faces with material groups
                current_material = None
                for face in pof_data['faces']:
                    if face['material'] != current_material:
                        current_material = face['material']
                        obj_file.write(f"\nusemtl {current_material}\n")
                    
                    # Write face indices (OBJ uses 1-based indexing)
                    face_line = "f"
                    for vertex_idx in face['vertices']:
                        face_line += f" {vertex_idx + 1}"
                    obj_file.write(f"{face_line}\n")
                
                # Write material file
                self._write_mtl_file(mtl_path, pof_data['materials'], texture_dir)
                
                return True
                
        except Exception as e:
            logging.error(f"Failed to write OBJ file {obj_path}: {e}")
            return False
    
    def _blender_obj_to_glb(self, obj_path: Path, glb_path: Path) -> bool:
        """Use Blender to convert OBJ to GLB"""
        import subprocess
        
        try:
            # Create Blender Python script for conversion
            script_content = f'''
import bpy
import bmesh

# Clear existing mesh objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Import OBJ file
bpy.ops.import_scene.obj(filepath="{obj_path}")

# Select all imported objects
bpy.ops.object.select_all(action='SELECT')

# Export as GLB
bpy.ops.export_scene.gltf(
    filepath="{glb_path}",
    export_format='GLB',
    export_texcoords=True,
    export_normals=True,
    export_materials='EXPORT'
)
'''
            
            script_path = obj_path.with_suffix('.py')
            with open(script_path, 'w') as script_file:
                script_file.write(script_content)
            
            # Run Blender in background mode
            cmd = [
                self.blender_executable,
                '--background',
                '--python', str(script_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            # Clean up script file
            script_path.unlink(missing_ok=True)
            
            if result.returncode == 0:
                return glb_path.exists()
            else:
                logging.error(f"Blender conversion failed: {result.stderr}")
                return False
                
        except Exception as e:
            logging.error(f"Failed to run Blender conversion: {e}")
            return False
```

### Mission File Conversion

**MissionFileConverter**
```python
class MissionFileConverter:
    """Converts WCS .fs2 mission files to Godot scene format"""
    
    def __init__(self):
        self.sexp_converter = SexpConverter()
        self.object_factory = ObjectFactory()
    
    def convert_mission_file(self, fs2_path: Path, output_path: Path) -> bool:
        """Convert FS2 mission file to Godot .tscn scene"""
        try:
            # Parse FS2 mission file
            mission_data = self._parse_fs2_mission(fs2_path)
            if not mission_data:
                return False
            
            # Create Godot scene structure
            scene_data = self._create_godot_scene_structure(mission_data)
            
            # Convert SEXP expressions to GDScript
            converted_sexps = self.sexp_converter.convert_mission_sexps(
                mission_data['events'], mission_data['goals']
            )
            
            # Generate mission script
            script_content = self._generate_mission_script(mission_data, converted_sexps)
            script_path = output_path.with_suffix('.gd')
            
            with open(script_path, 'w') as script_file:
                script_file.write(script_content)
            
            # Write scene file
            scene_content = self._generate_scene_file(scene_data, script_path)
            with open(output_path, 'w') as scene_file:
                scene_file.write(scene_content)
            
            # Create mission resource file
            mission_resource = self._create_mission_resource(mission_data)
            resource_path = output_path.with_suffix('.tres')
            with open(resource_path, 'w') as resource_file:
                resource_file.write(mission_resource)
            
            logging.info(f"Successfully converted mission {fs2_path.name}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to convert mission {fs2_path}: {e}")
            return False
    
    def _parse_fs2_mission(self, fs2_path: Path) -> Optional[Dict]:
        """Parse FS2 mission file format"""
        try:
            mission_data = {
                'mission_info': {},
                'ships': [],
                'wings': [],
                'waypoints': [],
                'events': [],
                'goals': [],
                'messages': [],
                'briefing': {},
                'debriefing': {},
                'variables': []
            }
            
            with open(fs2_path, 'r', encoding='latin-1') as mission_file:
                current_section = None
                
                for line in mission_file:
                    line = line.strip()
                    
                    # Section headers
                    if line.startswith('#'):
                        current_section = line[1:].lower()
                        continue
                    
                    # Parse section data
                    if current_section == 'mission info':
                        self._parse_mission_info(line, mission_data['mission_info'])
                    elif current_section == 'objects':
                        self._parse_mission_objects(line, mission_data)
                    elif current_section == 'events':
                        self._parse_mission_events(line, mission_data['events'])
                    elif current_section == 'goals':
                        self._parse_mission_goals(line, mission_data['goals'])
                    # ... additional section parsing
            
            return mission_data
            
        except Exception as e:
            logging.error(f"Failed to parse mission file {fs2_path}: {e}")
            return None
    
    def _generate_mission_script(self, mission_data: Dict, converted_sexps: Dict) -> str:
        """Generate GDScript mission controller"""
        script_template = '''extends Node

## Mission: {mission_name}
## Converted from: {source_file}

signal mission_completed()
signal mission_failed()
signal objective_completed(objective_name: String)

var mission_state: MissionState
var objectives: Dictionary = {{}}
var events: Dictionary = {{}}

func _ready() -> void:
    mission_state = MissionState.new()
    initialize_mission()
    setup_objectives()
    setup_events()

func initialize_mission() -> void:
    # Mission initialization
    mission_state.mission_name = "{mission_name}"
    mission_state.mission_time = 0.0
    
    # Spawn initial ships and wings
{ship_spawning_code}

    # Set up waypoints
{waypoint_setup_code}

func setup_objectives() -> void:
{objectives_code}

func setup_events() -> void:
{events_code}

func _process(delta: float) -> void:
    mission_state.mission_time += delta
    update_events(delta)
    check_objectives()

{converted_sexp_functions}
'''
        
        return script_template.format(
            mission_name=mission_data['mission_info'].get('name', 'Unknown Mission'),
            source_file=mission_data.get('source_file', ''),
            ship_spawning_code=self._generate_ship_spawning_code(mission_data['ships']),
            waypoint_setup_code=self._generate_waypoint_code(mission_data['waypoints']),
            objectives_code=self._generate_objectives_code(mission_data['goals']),
            events_code=self._generate_events_code(mission_data['events']),
            converted_sexp_functions=converted_sexps.get('functions', '')
        )
```

### Texture and Media Conversion

**TextureConverter**
```python
class TextureConverter:
    """Converts WCS textures to Godot-optimized formats"""
    
    def __init__(self):
        self.imagemagick_available = self._check_imagemagick()
        self.supported_formats = {
            '.pcx': 'png',
            '.tga': 'png', 
            '.dds': 'exr',  # For HDR textures
            '.png': 'png',  # Pass through
            '.jpg': 'jpg'   # Pass through
        }
    
    def convert_texture(self, source_path: Path, output_path: Path,
                       texture_type: str = 'diffuse') -> bool:
        """Convert texture with appropriate optimization"""
        try:
            source_ext = source_path.suffix.lower()
            if source_ext not in self.supported_formats:
                logging.warning(f"Unsupported texture format: {source_ext}")
                return False
            
            target_format = self.supported_formats[source_ext]
            
            # Use different conversion strategies based on source format
            if source_ext == '.dds':
                return self._convert_dds_texture(source_path, output_path)
            elif source_ext == '.pcx':
                return self._convert_pcx_texture(source_path, output_path)
            elif source_ext == '.tga':
                return self._convert_tga_texture(source_path, output_path)
            else:
                # Direct copy for supported formats
                import shutil
                shutil.copy2(source_path, output_path)
                return True
                
        except Exception as e:
            logging.error(f"Failed to convert texture {source_path}: {e}")
            return False
    
    def _convert_dds_texture(self, source_path: Path, output_path: Path) -> bool:
        """Convert DDS texture preserving compression"""
        import subprocess
        
        try:
            # Use ImageMagick to convert DDS
            cmd = [
                'magick',
                str(source_path),
                '-quality', '95',
                str(output_path.with_suffix('.png'))
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
            
        except Exception as e:
            logging.error(f"DDS conversion failed: {e}")
            return False

class AudioVideoConverter:
    """Converts WCS audio/video files using FFmpeg"""
    
    def __init__(self):
        self.ffmpeg_available = self._check_ffmpeg()
    
    def convert_audio_file(self, source_path: Path, output_path: Path) -> bool:
        """Convert audio file to OGG Vorbis for Godot"""
        import subprocess
        
        try:
            cmd = [
                'ffmpeg', '-i', str(source_path),
                '-c:a', 'libvorbis',
                '-q:a', '4',  # Good quality
                '-y',  # Overwrite output
                str(output_path.with_suffix('.ogg'))
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
            
        except Exception as e:
            logging.error(f"Audio conversion failed: {e}")
            return False
    
    def convert_video_file(self, source_path: Path, output_path: Path) -> bool:
        """Convert video file to modern format for Godot"""
        import subprocess
        
        try:
            # Convert to WebM for web compatibility
            cmd = [
                'ffmpeg', '-i', str(source_path),
                '-c:v', 'libvpx-vp9',
                '-c:a', 'libvorbis',
                '-crf', '30',  # Good quality/size balance
                '-b:v', '0',   # Variable bitrate
                '-y',
                str(output_path.with_suffix('.webm'))
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
            
        except Exception as e:
            logging.error(f"Video conversion failed: {e}")
            return False
```

### Godot Project Integration

**GodotProjectIntegrator**
```python
class GodotProjectIntegrator:
    """Integrates converted assets into Godot project structure"""
    
    def __init__(self, godot_project_path: Path):
        self.project_path = godot_project_path
        self.import_handler = GodotImportHandler()
    
    def organize_converted_assets(self, conversion_results: List[ConversionJob]) -> bool:
        """Organize converted assets into proper Godot directory structure"""
        try:
            # Create Godot project directories
            directories = [
                'models',
                'textures',
                'audio',
                'video', 
                'scenes/missions',
                'scripts/missions',
                'resources/ship_classes',
                'resources/weapon_definitions',
                'resources/mission_templates'
            ]
            
            for directory in directories:
                (self.project_path / directory).mkdir(parents=True, exist_ok=True)
            
            # Move converted assets to appropriate locations
            for job in conversion_results:
                if job.status == "completed":
                    self._move_asset_to_project_location(job)
            
            # Generate import files for all assets
            self.import_handler.generate_import_files(self.project_path)
            
            # Update project.godot configuration
            self._update_project_configuration()
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to organize assets: {e}")
            return False
    
    def _update_project_configuration(self) -> bool:
        """Update project.godot with asset references"""
        try:
            project_file = self.project_path / 'project.godot'
            
            # Read existing configuration
            config_content = ""
            if project_file.exists():
                with open(project_file, 'r') as f:
                    config_content = f.read()
            
            # Add WCS-specific project settings
            wcs_config = '''
[wcs_conversion]

converted_models_path="res://models/"
converted_textures_path="res://textures/"
converted_missions_path="res://scenes/missions/"
conversion_metadata_path="res://conversion_metadata.json"

[rendering]

textures/lossy_quality=0.8
textures/canvas_textures/default_texture_filter=2
'''
            
            # Append WCS configuration if not already present
            if '[wcs_conversion]' not in config_content:
                config_content += wcs_config
            
            with open(project_file, 'w') as f:
                f.write(config_content)
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to update project configuration: {e}")
            return False

class ValidationSystem:
    """Validates converted assets for correctness and completeness"""
    
    def validate_conversion_results(self, conversion_jobs: List[ConversionJob]) -> Dict:
        """Comprehensive validation of all conversion results"""
        validation_results = {
            'total_jobs': len(conversion_jobs),
            'successful': 0,
            'failed': 0,
            'warnings': [],
            'errors': [],
            'asset_integrity': {},
            'performance_metrics': {}
        }
        
        for job in conversion_jobs:
            if job.status == "completed":
                validation_results['successful'] += 1
                
                # Validate individual asset
                asset_validation = self._validate_single_asset(job)
                validation_results['asset_integrity'][job.target_path.name] = asset_validation
                
                if not asset_validation['valid']:
                    validation_results['warnings'].append(
                        f"Asset validation failed for {job.target_path.name}: {asset_validation['issues']}"
                    )
            else:
                validation_results['failed'] += 1
                validation_results['errors'].append(
                    f"Conversion failed for {job.source_path.name}: {job.error_message}"
                )
        
        return validation_results
    
    def _validate_single_asset(self, job: ConversionJob) -> Dict:
        """Validate individual converted asset"""
        validation = {
            'valid': False,
            'issues': [],
            'file_size': 0,
            'format_correct': False
        }
        
        try:
            target_path = job.target_path
            
            # Check file exists
            if not target_path.exists():
                validation['issues'].append("Output file does not exist")
                return validation
            
            # Check file size
            validation['file_size'] = target_path.stat().st_size
            if validation['file_size'] == 0:
                validation['issues'].append("Output file is empty")
                return validation
            
            # Format-specific validation
            if job.conversion_type == "pof_model":
                validation['format_correct'] = self._validate_glb_file(target_path)
            elif job.conversion_type == "texture":
                validation['format_correct'] = self._validate_texture_file(target_path)
            elif job.conversion_type == "mission":
                validation['format_correct'] = self._validate_godot_scene(target_path)
            else:
                validation['format_correct'] = True  # Assume valid for other types
            
            validation['valid'] = len(validation['issues']) == 0 and validation['format_correct']
            
        except Exception as e:
            validation['issues'].append(f"Validation error: {str(e)}")
        
        return validation
```

### CLI Interface

**Main Conversion Script**
```python
#!/usr/bin/env python3
"""
WCS to Godot Conversion Tool
Usage: python convert_wcs_assets.py --source /path/to/wcs --target /path/to/godot/project
"""

def main():
    parser = argparse.ArgumentParser(description='Convert WCS assets to Godot format')
    parser.add_argument('--source', type=Path, required=True, 
                       help='Path to WCS source directory')
    parser.add_argument('--target', type=Path, required=True,
                       help='Path to Godot project directory')
    parser.add_argument('--jobs', type=int, default=4,
                       help='Number of parallel conversion jobs')
    parser.add_argument('--validate', action='store_true',
                       help='Run validation after conversion')
    parser.add_argument('--resume', type=Path,
                       help='Resume from previous conversion state file')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show conversion plan without executing')
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('wcs_conversion.log'),
            logging.StreamHandler()
        ]
    )
    
    # Initialize conversion manager
    converter = ConversionManager(args.source, args.target)
    
    # Scan for assets
    print("Scanning WCS assets...")
    assets = converter.scan_wcs_assets()
    
    total_assets = sum(len(asset_list) for asset_list in assets.values())
    print(f"Found {total_assets} assets to convert:")
    for asset_type, asset_list in assets.items():
        print(f"  {asset_type}: {len(asset_list)} files")
    
    # Create conversion plan
    print("\nCreating conversion plan...")
    conversion_jobs = converter.create_conversion_plan(assets)
    
    if args.dry_run:
        print(f"\nConversion plan ({len(conversion_jobs)} jobs):")
        for i, job in enumerate(conversion_jobs[:10]):  # Show first 10
            print(f"  {i+1}. {job.conversion_type}: {job.source_path.name} -> {job.target_path.name}")
        if len(conversion_jobs) > 10:
            print(f"  ... and {len(conversion_jobs) - 10} more jobs")
        return
    
    # Execute conversion
    print(f"\nStarting conversion with {args.jobs} parallel jobs...")
    completed, failed, total = converter.execute_conversion_plan(conversion_jobs, args.jobs)
    
    print(f"\nConversion completed: {completed}/{total} successful, {failed} failed")
    
    # Validation
    if args.validate:
        print("\nRunning validation...")
        validator = ValidationSystem()
        validation_results = validator.validate_conversion_results(conversion_jobs)
        
        print(f"Validation results:")
        print(f"  Successful: {validation_results['successful']}")
        print(f"  Failed: {validation_results['failed']}")
        print(f"  Warnings: {len(validation_results['warnings'])}")
        print(f"  Errors: {len(validation_results['errors'])}")
    
    # Integration
    print("\nIntegrating assets into Godot project...")
    integrator = GodotProjectIntegrator(args.target)
    if integrator.organize_converted_assets(conversion_jobs):
        print("Asset integration completed successfully")
    else:
        print("Asset integration failed")
    
    print("\nConversion process finished!")

if __name__ == '__main__':
    main()
```

## Godot Editor Plugin Integration

**Conversion Plugin**
```gdscript
@tool
extends EditorPlugin

## WCS Asset Conversion Plugin for Godot Editor
## Provides UI for managing WCS asset conversion within Godot

const ConversionDock = preload("res://addons/wcs_converter/conversion_dock.gd")
var dock

func _enter_tree():
    dock = ConversionDock.new()
    add_control_to_dock(DOCK_SLOT_LEFT_UR, dock)

func _exit_tree():
    remove_control_from_docks(dock)

class ConversionDock:
    extends Control
    
    var conversion_status_label: Label
    var convert_button: Button
    var progress_bar: ProgressBar
    var file_dialog: FileDialog
    
    func _ready():
        setup_ui()
    
    func setup_ui():
        set_custom_minimum_size(Vector2(200, 300))
        
        var vbox = VBoxContainer.new()
        add_child(vbox)
        
        # Title
        var title = Label.new()
        title.text = "WCS Asset Converter"
        vbox.add_child(title)
        
        # Status
        conversion_status_label = Label.new()
        conversion_status_label.text = "Ready"
        vbox.add_child(conversion_status_label)
        
        # Progress
        progress_bar = ProgressBar.new()
        progress_bar.visible = false
        vbox.add_child(progress_bar)
        
        # Convert button
        convert_button = Button.new()
        convert_button.text = "Convert WCS Assets"
        convert_button.pressed.connect(_on_convert_pressed)
        vbox.add_child(convert_button)
        
        # File dialog
        file_dialog = FileDialog.new()
        file_dialog.file_mode = FileDialog.FILE_MODE_OPEN_DIR
        file_dialog.dir_selected.connect(_on_wcs_directory_selected)
        add_child(file_dialog)
    
    func _on_convert_pressed():
        file_dialog.popup_centered(Vector2(800, 600))
    
    func _on_wcs_directory_selected(dir_path: String):
        start_conversion(dir_path)
    
    func start_conversion(wcs_path: String):
        conversion_status_label.text = "Converting..."
        progress_bar.visible = true
        convert_button.disabled = true
        
        # Call Python conversion script
        var output = []
        var project_path = ProjectSettings.globalize_path("res://")
        
        OS.execute("python", [
            "tools/convert_wcs_assets.py",
            "--source", wcs_path,
            "--target", project_path,
            "--validate"
        ], output)
        
        # Update UI based on results
        conversion_status_label.text = "Conversion completed"
        progress_bar.visible = false
        convert_button.disabled = false
        
        # Refresh file system
        EditorInterface.get_resource_filesystem().scan()
```

## Testing Strategy

### Unit Tests for Converters

**Test VP Archive Extraction**
```python
import unittest
from pathlib import Path

class TestVPArchiveExtractor(unittest.TestCase):
    
    def setUp(self):
        self.extractor = VPArchiveExtractor()
        self.test_vp = Path("test_data/test_archive.vp")
        self.output_dir = Path("test_output")
    
    def test_extract_valid_archive(self):
        result = self.extractor.extract_vp_archive(self.test_vp, self.output_dir)
        self.assertTrue(result)
        self.assertTrue(self.output_dir.exists())
    
    def test_extract_invalid_archive(self):
        invalid_vp = Path("test_data/invalid.vp")
        result = self.extractor.extract_vp_archive(invalid_vp, self.output_dir)
        self.assertFalse(result)
```

### Integration Tests

**End-to-End Conversion Test**
```python
class TestFullConversionPipeline(unittest.TestCase):
    
    def test_complete_asset_conversion(self):
        # Test complete conversion of a small WCS asset set
        source_dir = Path("test_data/mini_wcs")
        target_dir = Path("test_output/godot_project")
        
        converter = ConversionManager(source_dir, target_dir)
        assets = converter.scan_wcs_assets()
        
        self.assertGreater(len(assets['pof_models']), 0)
        self.assertGreater(len(assets['textures']), 0)
        
        jobs = converter.create_conversion_plan(assets)
        completed, failed, total = converter.execute_conversion_plan(jobs, max_workers=1)
        
        self.assertEqual(failed, 0)
        self.assertEqual(completed, total)
```

## Implementation Phases

### Phase 1: Core Conversion Framework (2 weeks)
- Python conversion manager and job system
- VP archive extraction
- Basic texture conversion
- Validation framework

### Phase 2: 3D Asset Pipeline (2 weeks)
- POF model parsing and conversion
- Blender integration for GLB export
- Material and texture assignment
- Collision mesh generation

### Phase 3: Mission Conversion (2 weeks)
- FS2 mission file parsing
- SEXP to GDScript conversion
- Scene generation
- Mission resource creation

### Phase 4: Integration & Polish (1 week)
- Godot editor plugin
- Batch processing optimization
- Error handling and recovery
- Documentation and examples

## Success Criteria

- [ ] Successfully extract and process all VP archives
- [ ] Convert POF models to GLB with materials intact
- [ ] Translate FS2 missions to functional Godot scenes
- [ ] Batch convert entire WCS asset library (500+ files) in under 2 hours
- [ ] Maintain visual fidelity of converted textures and models
- [ ] Generate working Godot project structure
- [ ] Comprehensive validation and error reporting
- [ ] Resume capability for interrupted conversions
- [ ] Integration with Godot editor workflow

## Integration Notes

**Output for EPIC-002**: Converted assets in proper Resource format for asset management system
**Input to EPIC-008**: Converted models and textures for graphics rendering pipeline
**Integration with EPIC-004**: Mission SEXP expressions converted to GDScript
**Integration with EPIC-005**: Converted missions available for GFRED2 editor

This architecture provides a comprehensive conversion pipeline that transforms WCS assets into Godot-native formats while preserving fidelity and enabling seamless integration with the target game engine.
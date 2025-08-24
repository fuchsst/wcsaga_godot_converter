#!/usr/bin/env python3
"""
POF Parser - Core POF file parsing implementation.

Provides robust parsing of POF (Parallax Object Format) files with comprehensive
chunk processing and error handling. Based on WCS C++ source analysis.
"""

import logging
import struct
from pathlib import Path
from typing import Any, BinaryIO, Dict, List, Optional, Set

# Import constants and utilities
from .pof_chunks import (
    ID_ACEN,
    ID_DOCK,
    ID_EYE,
    ID_FUEL,
    ID_GLOW,
    ID_GPNT,
    ID_INSG,
    ID_MPNT,
    ID_OHDR,
    ID_PATH,
    ID_SHLD,
    ID_SLDC,
    ID_SOBJ,
    ID_SPCL,
    ID_TXTR,
    POF_HEADER_ID,
    get_chunk_name,
)
from .pof_docking_parser import read_dock_chunk
from .pof_eye_parser import read_eye_chunk

# Import chunk readers
from .pof_header_parser import read_ohdr_chunk
from .pof_insignia_parser import read_insg_chunk
from .pof_misc_parser import read_acen_chunk, read_glow_chunk, read_unknown_chunk
from .pof_path_parser import read_path_chunk
from .pof_shield_parser import read_shld_chunk, read_sldc_chunk
from .pof_special_points_parser import read_spcl_chunk
from .pof_subobject_parser import read_sobj_chunk
from .pof_texture_parser import read_txtr_chunk
from .pof_thruster_parser import read_fuel_chunk
from .pof_weapon_points_parser import read_gpnt_chunk, read_mpnt_chunk

# Import enhanced error handling and types
from .pof_error_handler import UnifiedPOFErrorHandler, ErrorSeverity, ErrorCategory
from .pof_types import POFModelData, SubObject, SpecialPoint, BSPNode, POFVersion, POFHeader, BoundingBox, Vector3D, BSPNodeType

# Import version handler for comprehensive version-specific parsing
from .pof_version_handler import POFVersionHandler

# Import unified binary reader
from .pof_binary_reader import create_reader

logger = logging.getLogger(__name__)


class POFParser:
    """
    POF (Parallax Object Format) file parser.

    Parses WCS POF model files into structured dictionaries containing geometry,
    materials, textures, and gameplay-relevant metadata. Supports all POF chunk
    types and provides robust error handling.

    Based on analysis of source/code/model/modelread.cpp from WCS source code.
    """

    def __init__(self) -> None:
        """Initialize POF parser with empty data structure and error handler."""
        self._initialize_data_structure()
        self.bsp_data_cache: Dict[int, bytes] = {}
        self._current_file_handle: Optional[BinaryIO] = None
        self.error_handler = UnifiedPOFErrorHandler()
        self.version_handler = POFVersionHandler()
        self._current_chunk_id: Optional[int] = None
        self._current_chunk_name: Optional[str] = None

    def _initialize_data_structure(self) -> None:
        """Initialize the POF data structure with enhanced types."""
        # Create empty enhanced data structure
        self.pof_data = POFModelData(
            filename="",
            version=POFVersion.VERSION_2100,
            header=POFHeader(
                version=POFVersion.VERSION_2100,
                max_radius=0.0,
                object_flags=0,
                num_subobjects=0,
                bounding_box=BoundingBox(Vector3D(0, 0, 0), Vector3D(0, 0, 0)),
                detail_levels=[-1] * 8,
                debris_pieces=[-1] * 32,
                mass=0.0,
                mass_center=Vector3D(0, 0, 0),
                moment_of_inertia=[Vector3D(0, 0, 0), Vector3D(0, 0, 0), Vector3D(0, 0, 0)],
                cross_sections=[],
                lights=[]
            ),
            textures=[],
            subobjects=[],
            special_points=[],
            paths=[],
            gun_points=[],
            missile_points=[],
            docking_points=[],
            thrusters=[],
            shield_mesh=None,
            eye_points=[],
            insignia=[],
            autocenter=None,
            glow_banks=[],
            shield_collision_tree=None
        )

    def _read_bsp_data(
        self, subobj_num: int, offset: int, size: int
    ) -> Optional[bytes]:
        """Reads BSP data for a specific subobject on demand."""
        if subobj_num in self.bsp_data_cache:
            return self.bsp_data_cache[subobj_num]

        if self._current_file_handle and offset >= 0 and size > 0:
            try:
                current_pos = self._current_file_handle.tell()
                self._current_file_handle.seek(offset)
                bsp_data = self._current_file_handle.read(size)
                self._current_file_handle.seek(current_pos)  # Restore position
                self.bsp_data_cache[subobj_num] = bsp_data
                logger.debug(
                    f"Read {size} bytes of BSP data for subobject {subobj_num}"
                )
                return bsp_data
            except Exception as e:
                logger.error(f"Failed to read BSP data for subobject {subobj_num}: {e}")
                return None
        return None

    def get_subobject_bsp_data(self, subobj_num: int) -> Optional[bytes]:
        """Public method to get BSP data, reading it if necessary."""
        if subobj_num in self.bsp_data_cache:
            return self.bsp_data_cache[subobj_num]

        # Find the subobject data in the parsed structure
        sobj_data = next(
            (
                obj
                for obj in self.pof_data.subobjects
                if obj.number == subobj_num
            ),
            None,
        )

        if sobj_data and sobj_data.has_bsp_data():
            return self._read_bsp_data(subobj_num, sobj_data.bsp_data_offset, sobj_data.bsp_data_size)

        logger.warning(f"Subobject {subobj_num} not found in parsed data.")
        return None

    def parse_subobject_bsp_tree(self, subobj_num: int) -> Optional[BSPNode]:
        """
        Parse and reconstruct BSP tree for a specific subobject.
        
        This method reads the raw BSP data and converts it into a structured
        BSP tree with proper node hierarchy and polygon data.
        """
        raw_bsp_data = self.get_subobject_bsp_data(subobj_num)
        if not raw_bsp_data:
            return None
        
        try:
            # Use the BSP parser to convert raw bytes to structured tree
            from .pof_bsp_parser import parse_bsp_data
            
            bsp_result = parse_bsp_data(raw_bsp_data, self.pof_data.version.value)
            if bsp_result and 'bsp_tree' in bsp_result:
                # Update the subobject with the parsed BSP tree
                subobj = next((so for so in self.pof_data.subobjects if so.number == subobj_num), None)
                if subobj:
                    subobj.bsp_tree = bsp_result['bsp_tree']
                return bsp_result['bsp_tree']
            
        except Exception as e:
            logger.error(f"Failed to parse BSP tree for subobject {subobj_num}: {e}")
            self.error_handler.add_error(
                f"BSP parsing error for subobject {subobj_num}: {e}",
                severity=ErrorSeverity.ERROR,
                category=ErrorCategory.PARSING,
                recovery_action="Use fallback geometry extraction"
            )
        
        return None

    def parse_all_bsp_trees(self) -> Dict[int, Optional[BSPNode]]:
        """
        Parse BSP trees for all subobjects that have BSP data.
        
        Returns:
            Dictionary mapping subobject numbers to their parsed BSP trees
        """
        results = {}
        
        for subobj in self.pof_data.subobjects:
            if subobj.has_bsp_data():
                bsp_tree = self.parse_subobject_bsp_tree(subobj.number)
                results[subobj.number] = bsp_tree
                
                if bsp_tree is None:
                    logger.warning(f"Failed to parse BSP tree for subobject {subobj.number}")
        
        return results
    
    def _sanitize_and_finalize(self) -> None:
        """
        Perform post-parse validation and data sanitization.
        
        Based on Rust reference implementation, this method:
        - Validates subobject parent-child relationships
        - Prunes unused textures and re-indexes remaining ones
        - Validates detail levels and debris piece references
        - Ensures data consistency and integrity
        """
        try:
            # Validate subobject hierarchy
            self._validate_subobject_hierarchy()
            
            # Prune unused textures
            self._prune_unused_textures()
            
            # Validate detail levels and debris pieces
            self._validate_detail_and_debris_references()
            
            logger.info("Post-parse sanitization completed successfully")
            
        except Exception as e:
            logger.error(f"Failed during post-parse sanitization: {e}")
            self.error_handler.add_error(
                f"Sanitization error: {e}",
                severity=ErrorSeverity.WARNING,
                category=ErrorCategory.DATA_INTEGRITY,
                recovery_action="Continue with potentially inconsistent data"
            )
    
    def _validate_subobject_hierarchy(self) -> None:
        """Validate subobject parent-child relationships."""
        valid_subobj_numbers = {sobj.number for sobj in self.pof_data.subobjects}
        
        for subobj in self.pof_data.subobjects:
            if subobj.parent != -1 and subobj.parent not in valid_subobj_numbers:
                logger.warning(f"Subobject {subobj.number} has invalid parent {subobj.parent}")
                self.error_handler.add_data_integrity_warning(
                    f"Invalid parent reference in subobject {subobj.number}",
                    recovery_action="Set parent to -1 (root)"
                )
                subobj.parent = -1  # Fix invalid parent reference
    
    def _prune_unused_textures(self) -> None:
        """Prune textures that are not referenced by any polygon."""
        if not self.pof_data.textures:
            return
        
        # Get all texture indices used in BSP trees
        used_texture_indices = set()
        for subobj in self.pof_data.subobjects:
            if subobj.bsp_tree:
                used_texture_indices.update(self._get_used_texture_indices(subobj.bsp_tree))
        
        # Create new texture list with only used textures
        old_to_new_index = {}
        new_textures = []
        
        for old_index, texture_name in enumerate(self.pof_data.textures):
            if old_index in used_texture_indices:
                old_to_new_index[old_index] = len(new_textures)
                new_textures.append(texture_name)
        
        # Update texture references in BSP trees
        if len(new_textures) < len(self.pof_data.textures):
            logger.info(f"Pruned {len(self.pof_data.textures) - len(new_textures)} unused textures")
            self.pof_data.textures = new_textures
            
            # Update texture indices in all BSP trees
            for subobj in self.pof_data.subobjects:
                if subobj.bsp_tree:
                    self._update_texture_indices(subobj.bsp_tree, old_to_new_index)
    
    def _get_used_texture_indices(self, node: BSPNode) -> Set[int]:
        """Recursively get all texture indices used in BSP tree."""
        indices = set()
        
        if node.node_type == BSPNodeType.LEAF:
            for polygon in node.polygons:
                indices.add(polygon.texture_index)
        
        if node.front_child:
            indices.update(self._get_used_texture_indices(node.front_child))
        if node.back_child:
            indices.update(self._get_used_texture_indices(node.back_child))
        
        return indices
    
    def _update_texture_indices(self, node: BSPNode, index_map: Dict[int, int]) -> None:
        """Recursively update texture indices in BSP tree."""
        if node.node_type == BSPNodeType.LEAF:
            for polygon in node.polygons:
                old_index = polygon.texture_index
                if old_index in index_map:
                    polygon.texture_index = index_map[old_index]
                else:
                    # Texture was pruned, mark as untextured
                    polygon.texture_index = 0xFFFFFFFF
        
        if node.front_child:
            self._update_texture_indices(node.front_child, index_map)
        if node.back_child:
            self._update_texture_indices(node.back_child, index_map)
    
    def _validate_detail_and_debris_references(self) -> None:
        """Validate detail level and debris piece references."""
        valid_subobj_numbers = {sobj.number for sobj in self.pof_data.subobjects}
        
        # Validate detail levels
        for i, detail_num in enumerate(self.pof_data.header.detail_levels):
            if detail_num != -1 and detail_num not in valid_subobj_numbers:
                logger.warning(f"Detail level {i} references invalid subobject {detail_num}")
                self.error_handler.add_data_integrity_warning(
                    f"Invalid detail level reference: {detail_num}",
                    recovery_action="Set to -1 (no detail)"
                )
                self.pof_data.header.detail_levels[i] = -1
        
        # Validate debris pieces
        for i, debris_num in enumerate(self.pof_data.header.debris_pieces):
            if debris_num != -1 and debris_num not in valid_subobj_numbers:
                logger.warning(f"Debris piece {i} references invalid subobject {debris_num}")
                self.error_handler.add_data_integrity_warning(
                    f"Invalid debris piece reference: {debris_num}",
                    recovery_action="Set to -1 (no debris)"
                )
                self.pof_data.header.debris_pieces[i] = -1

    def parse(self, file_path: Path) -> Optional[POFModelData]:
        """
        Parse POF file and return structured data.

        Args:
            file_path: Path to POF file to parse

        Returns:
            POFModelDataEnhanced instance containing parsed POF data, or None if parsing failed
        """
        # Reset data for new parse
        self._initialize_data_structure()
        self.pof_data.filename = file_path.name
        self.bsp_data_cache.clear()
        self._current_file_handle = None
        self.error_handler.clear_errors()

        logger.info(f"Parsing POF file: {file_path}")

        try:
            with open(file_path, "rb") as f:
                self._current_file_handle = f

                # Validate POF header
                if not self._validate_header(f):
                    self.error_handler.add_error(
                        "Failed to validate POF header",
                        severity=ErrorSeverity.ERROR,
                        category=ErrorCategory.VALIDATION,
                        recovery_action="Cannot continue parsing"
                    )
                    return None

                # Parse all chunks
                self._parse_chunks(f)

                # Parse BSP trees for all subobjects
                bsp_results = self.parse_all_bsp_trees()
                successful_bsp_parses = sum(1 for result in bsp_results.values() if result is not None)
                
                if successful_bsp_parses < len(bsp_results):
                    logger.warning(f"BSP parsing: {successful_bsp_parses}/{len(bsp_results)} trees parsed successfully")
                
                # Perform post-parse sanitization and data cleanup
                self._sanitize_and_finalize()
                
                # Run comprehensive validation
                from .validation_system import validate_pof_model
                validation_result = validate_pof_model(self.pof_data, self.error_handler)
                
                if not validation_result.is_valid:
                    logger.warning(f"Validation completed with issues: {len(validation_result.errors)} errors, {len(validation_result.warnings)} warnings")
                
                # Check if parsing was successful
                if self.error_handler.has_errors(ErrorSeverity.ERROR):
                    logger.warning(f"Parsing completed with errors: {file_path}")
                    logger.info(self.error_handler.format_error_report())
                else:
                    logger.info(f"Successfully parsed {file_path}")

                return self.pof_data

        except FileNotFoundError:
            error = self.error_handler.add_error(
                f"POF file not found: {file_path}",
                severity=ErrorSeverity.ERROR,
                category=ErrorCategory.IO,
                recovery_action="Check file path and permissions"
            )
            logger.error(str(error))
            return None
        except Exception as e:
            error = self.error_handler.add_error(
                f"Unexpected error parsing POF file {file_path}: {e}",
                severity=ErrorSeverity.CRITICAL,
                category=ErrorCategory.PARSING,
                recovery_action="Review file integrity and try again"
            )
            logger.error(str(error), exc_info=True)
            return None
        finally:
            self._current_file_handle = None

    def _validate_header(self, f: BinaryIO) -> bool:
        """
        Validate POF file header with enhanced error tracking.

        Args:
            f: File handle positioned at start of file

        Returns:
            True if header is valid, False otherwise
        """
        try:
            current_pos = f.tell()
            self.error_handler.set_position(current_pos)
            
            # Use unified binary reader
            reader = create_reader(f)
            
            # Read POF header
            pof_id = reader.read_uint32()
            pof_version = reader.read_int32()

            if pof_id != POF_HEADER_ID:
                self.error_handler.add_error(
                    f"Invalid POF header ID. Expected {POF_HEADER_ID:08X}, got {pof_id:08X}",
                    severity=ErrorSeverity.ERROR,
                    category=ErrorCategory.VALIDATION,
                    recovery_action="Check if file is a valid POF file"
                )
                return False

            # Version compatibility check using comprehensive version handler
            self.error_handler.set_version_context(pof_version)
            
            # Use version handler for comprehensive validation
            version_info = self.version_handler.validate_version(pof_version)
            
            if not version_info["compatible"]:
                self.error_handler.add_error(
                    f"POF version {pof_version} is not compatible",
                    severity=ErrorSeverity.ERROR,
                    category=ErrorCategory.COMPATIBILITY,
                    recovery_action="Use a different POF file or version"
                )
                return False
            
            # Add version-specific warnings
            for warning in version_info.get("warnings", []):
                self.error_handler.add_error(
                    f"Version {pof_version} warning: {warning}",
                    severity=ErrorSeverity.WARNING,
                    category=ErrorCategory.COMPATIBILITY,
                    recovery_action="Proceed with caution"
                )

            self.pof_data.version = POFVersion.from_int(pof_version)
            logger.debug(f"POF Version: {pof_version} - {version_info.get('name', 'Unknown')}")
            return True

        except Exception as e:
            self.error_handler.add_error(
                f"Failed to read POF header: {e}",
                severity=ErrorSeverity.ERROR,
                category=ErrorCategory.PARSING,
                recovery_action="Check file integrity and size"
            )
            return False

    def _parse_chunks(self, f: BinaryIO) -> None:
        """
        Parse all chunks in the POF file with enhanced error tracking.

        Args:
            f: File handle positioned after header
        """
        # Chunk readers mapping
        chunk_readers = {
            ID_OHDR: read_ohdr_chunk,
            ID_SOBJ: read_sobj_chunk,
            ID_TXTR: read_txtr_chunk,
            ID_SPCL: read_spcl_chunk,
            ID_PATH: read_path_chunk,
            ID_GPNT: read_gpnt_chunk,
            ID_MPNT: read_mpnt_chunk,
            ID_DOCK: read_dock_chunk,
            ID_FUEL: read_fuel_chunk,
            ID_SHLD: read_shld_chunk,
            ID_EYE: read_eye_chunk,
            ID_INSG: read_insg_chunk,
            ID_ACEN: read_acen_chunk,
            ID_GLOW: read_glow_chunk,
            ID_SLDC: read_sldc_chunk,
        }

        # Chunk ID to data key mapping
        data_key_map = {
            ID_OHDR: "header",
            ID_SOBJ: "objects",
            ID_TXTR: "textures",
            ID_SPCL: "special_points",
            ID_PATH: "paths",
            ID_GPNT: "gun_points",
            ID_MPNT: "missile_points",
            ID_DOCK: "docking_points",
            ID_FUEL: "thrusters",
            ID_SHLD: "shield_mesh",
            ID_EYE: "eye_points",
            ID_INSG: "insignia",
            ID_ACEN: "autocenter",
            ID_GLOW: "glow_banks",
            ID_SLDC: "shield_collision_tree",
        }

        # Read chunks until EOF
        while True:
            chunk_start_pos = f.tell()
            self.error_handler.set_position(chunk_start_pos)

            try:
                # Check if there's enough data for a header
                header_bytes = f.peek(8)
                if not header_bytes or len(header_bytes) < 8:
                    logger.debug("Reached end of file (insufficient data for header)")
                    break

                # Use unified binary reader
                reader = create_reader(f)
                chunk_id, chunk_len = reader.read_chunk_header()
                chunk_name = get_chunk_name(chunk_id)
                
                self.error_handler.set_chunk_context(chunk_id, chunk_name)
                logger.debug(f"Found chunk ID: {chunk_id:08X} ({chunk_name}), Length: {chunk_len}")

            except Exception as e:
                self.error_handler.add_error(
                    f"Failed to read chunk header: {e}",
                    severity=ErrorSeverity.WARNING,
                    category=ErrorCategory.PARSING,
                    recovery_action="Assume end of file reached"
                )
                logger.debug("Reached end of file or failed to read chunk header")
                break

            # Validate chunk length
            if chunk_len < 0:
                self.error_handler.add_error(
                    f"Invalid negative chunk length {chunk_len} for ID {chunk_id:08X}",
                    severity=ErrorSeverity.ERROR,
                    category=ErrorCategory.VALIDATION,
                    recovery_action="Skip this chunk"
                )
                break

            next_chunk_pos = chunk_start_pos + 8 + chunk_len

            # Process chunk
            self._process_chunk(f, chunk_id, chunk_len, chunk_readers, data_key_map)

            # Verify chunk position and seek to next chunk
            self._verify_chunk_position(
                f, chunk_id, chunk_start_pos, next_chunk_pos, chunk_len
            )

            # Check for EOF
            if not f.peek(1):
                logger.debug("Reached end of file after chunk")
                break

    def _process_chunk(
        self,
        f: BinaryIO,
        chunk_id: int,
        chunk_len: int,
        chunk_readers: Dict[int, Any],
        data_key_map: Dict[int, str],
    ) -> None:
        """Process a single chunk with enhanced error handling."""
        reader_func = chunk_readers.get(chunk_id)
        chunk_name = get_chunk_name(chunk_id)

        if reader_func:
            data_key = data_key_map.get(chunk_id)
            if data_key:
                try:
                    parsed_data = reader_func(f, chunk_len)
                    self._store_chunk_data(chunk_id, data_key, parsed_data)
                    logger.debug(f"Successfully parsed chunk {chunk_name}")
                except Exception as e:
                    self.error_handler.add_error(
                        f"Error parsing chunk {chunk_name}: {e}",
                        severity=ErrorSeverity.ERROR,
                        category=ErrorCategory.PARSING,
                        recovery_action="Skip chunk and continue parsing"
                    )
                    read_unknown_chunk(f, chunk_len, chunk_id)
            else:
                self.error_handler.add_error(
                    f"No data key mapped for chunk ID {chunk_id:08X} ({chunk_name})",
                    severity=ErrorSeverity.WARNING,
                    category=ErrorCategory.PARSING,
                    recovery_action="Skip chunk"
                )
                read_unknown_chunk(f, chunk_len, chunk_id)
        else:
            # Handle unknown chunks
            self.error_handler.add_error(
                f"Unknown chunk type {chunk_id:08X} ({chunk_name})",
                severity=ErrorSeverity.WARNING,
                category=ErrorCategory.COMPATIBILITY,
                recovery_action="Skip unknown chunk"
            )
            read_unknown_chunk(f, chunk_len, chunk_id)

    def _store_chunk_data(self, chunk_id: int, data_key: str, parsed_data: Any) -> None:
        """Store parsed chunk data in the enhanced data structure."""
        try:
            if chunk_id == ID_OHDR:
                # OHDR contains complete header data - convert from dict to POFHeader
                from .pof_types import dict_to_header
                self.pof_data.header = dict_to_header(parsed_data, self.pof_data.version)
            
            elif chunk_id == ID_SOBJ:
                # SOBJ now returns SubObject dataclass instances directly
                if isinstance(parsed_data, list):
                    for subobj in parsed_data:
                        if subobj is not None:
                            self.pof_data.subobjects.append(subobj)
                elif parsed_data is not None:
                    self.pof_data.subobjects.append(parsed_data)
            
            elif chunk_id == ID_TXTR:
                # TXTR returns list of texture names
                if isinstance(parsed_data, list):
                    self.pof_data.textures.extend(parsed_data)
                else:
                    self.pof_data.textures.append(parsed_data)
            
            elif chunk_id in [ID_SPCL, ID_GPNT, ID_MPNT, ID_DOCK, ID_FUEL, ID_EYE]:
                # Special points types - convert dictionaries to SpecialPoint dataclasses
                target_list = getattr(self.pof_data, data_key)
                
                # Determine point type based on chunk ID
                point_type_map = {
                    ID_SPCL: 'special',
                    ID_GPNT: 'gun',
                    ID_MPNT: 'missile', 
                    ID_DOCK: 'docking',
                    ID_FUEL: 'thruster',
                    ID_EYE: 'eye'
                }
                point_type = point_type_map.get(chunk_id, 'unknown')
                
                from .pof_types import dict_to_special_point
                
                if isinstance(parsed_data, list):
                    for point_data in parsed_data:
                        if isinstance(point_data, dict):
                            target_list.append(dict_to_special_point(point_data, point_type))
                        else:
                            # Already converted or invalid
                            target_list.append(point_data)
                elif isinstance(parsed_data, dict):
                    target_list.append(dict_to_special_point(parsed_data, point_type))
                else:
                    # Already converted or invalid
                    target_list.append(parsed_data)
            
            elif chunk_id == ID_PATH:
                # PATH returns AnimationPath instances - convert dictionaries
                from .pof_types import dict_to_animation_path
                
                if isinstance(parsed_data, list):
                    for path_data in parsed_data:
                        if isinstance(path_data, dict):
                            self.pof_data.paths.append(dict_to_animation_path(path_data))
                        else:
                            # Already converted
                            self.pof_data.paths.append(path_data)
                elif isinstance(parsed_data, dict):
                    self.pof_data.paths.append(dict_to_animation_path(parsed_data))
                else:
                    # Already converted
                    self.pof_data.paths.append(parsed_data)
            
            elif chunk_id == ID_SHLD:
                # SHLD returns ShieldMesh - convert dictionary
                from .pof_types import dict_to_shield_mesh
                
                if isinstance(parsed_data, dict):
                    self.pof_data.shield_mesh = dict_to_shield_mesh(parsed_data)
                else:
                    # Already converted
                    self.pof_data.shield_mesh = parsed_data
            
            elif chunk_id == ID_INSG:
                # INSG returns InsigniaData instances - convert dictionaries
                from .pof_types import dict_to_insignia
                
                if isinstance(parsed_data, list):
                    for insignia_data in parsed_data:
                        if isinstance(insignia_data, dict):
                            self.pof_data.insignia.append(dict_to_insignia(insignia_data))
                        else:
                            # Already converted
                            self.pof_data.insignia.append(insignia_data)
                elif isinstance(parsed_data, dict):
                    self.pof_data.insignia.append(dict_to_insignia(parsed_data))
                else:
                    # Already converted
                    self.pof_data.insignia.append(parsed_data)
            
            elif chunk_id == ID_ACEN:
                # ACEN returns Vector3D - convert list to Vector3D
                from .pof_types import list_to_vector3d
                
                if isinstance(parsed_data, list):
                    self.pof_data.autocenter = list_to_vector3d(parsed_data)
                else:
                    # Already converted
                    self.pof_data.autocenter = parsed_data
            
            elif chunk_id == ID_GLOW:
                # GLOW returns GlowBank instances - convert dictionaries
                from .pof_types import dict_to_glow_bank
                
                if isinstance(parsed_data, list):
                    for glow_data in parsed_data:
                        if isinstance(glow_data, dict):
                            self.pof_data.glow_banks.append(dict_to_glow_bank(glow_data))
                        else:
                            # Already converted
                            self.pof_data.glow_banks.append(glow_data)
                elif isinstance(parsed_data, dict):
                    self.pof_data.glow_banks.append(dict_to_glow_bank(parsed_data))
                else:
                    # Already converted
                    self.pof_data.glow_banks.append(parsed_data)
            
            elif chunk_id == ID_SLDC:
                # SLDC returns BSPNode (shield collision tree)
                self.pof_data.shield_collision_tree = parsed_data
            
            else:
                logger.warning(f"No storage handler for chunk ID {chunk_id:08X}")
                
        except Exception as e:
            logger.error(f"Failed to store chunk data for {chunk_id:08X}: {e}")
            self.error_handler.add_error(
                f"Data storage error for chunk {chunk_id:08X}: {e}",
                severity=ErrorSeverity.ERROR,
                category=ErrorCategory.DATA_INTEGRITY,
                recovery_action="Skip problematic chunk data"
            )

    def _verify_chunk_position(
        self,
        f: BinaryIO,
        chunk_id: int,
        chunk_start_pos: int,
        next_chunk_pos: int,
        chunk_len: int,
    ) -> None:
        """Verify chunk position and seek to next chunk if needed with error tracking."""
        current_pos = f.tell()
        chunk_name = f"{chunk_id:08X}"

        if current_pos > next_chunk_pos:
            self.error_handler.add_error(
                f"Read past end of chunk {chunk_name}! Expected {next_chunk_pos}, got {current_pos}",
                severity=ErrorSeverity.ERROR,
                category=ErrorCategory.PARSING,
                recovery_action="Seek to next chunk position"
            )
            f.seek(next_chunk_pos)
        elif current_pos < next_chunk_pos:
            bytes_skipped = next_chunk_pos - current_pos
            self.error_handler.add_error(
                f"Chunk read mismatch for {chunk_name}. "
                f"Read {current_pos - (chunk_start_pos + 8)} bytes, expected {chunk_len}. "
                f"Skipping {bytes_skipped} bytes",
                severity=ErrorSeverity.WARNING,
                category=ErrorCategory.DATA_INTEGRITY,
                recovery_action="Seek to expected position"
            )
            f.seek(next_chunk_pos)

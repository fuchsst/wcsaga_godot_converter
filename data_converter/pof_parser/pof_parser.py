#!/usr/bin/env python3
"""
POF Parser - Core POF file parsing implementation.

Provides robust parsing of POF (Parallax Object Format) files with comprehensive
chunk processing and error handling. Based on WCS C++ source analysis.
"""

import logging
import struct
from pathlib import Path
from typing import Any, BinaryIO, Dict, List, Optional

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
    PM_COMPATIBLE_VERSION,
    PM_OBJFILE_MAJOR_VERSION,
    POF_HEADER_ID,
    read_chunk_header,
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
from .pof_error_handler import POFErrorHandler, ErrorSeverity, ErrorCategory
from .pof_enhanced_types import POFModelDataEnhanced, SubObject, SpecialPoint, dict_to_subobject

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
        self.error_handler = POFErrorHandler()
        self._current_chunk_id: Optional[int] = None
        self._current_chunk_name: Optional[str] = None

    def _initialize_data_structure(self) -> None:
        """Initialize the POF data structure with empty containers."""
        self.pof_data: Dict[str, Any] = {
            "filename": "",
            "version": 0,
            "header": {},
            "textures": [],
            "objects": [],
            "special_points": [],
            "paths": [],
            "gun_points": [],
            "missile_points": [],
            "docking_points": [],
            "thrusters": [],
            "shield_mesh": {},
            "eye_points": [],
            "insignia": [],
            "autocenter": None,
            "glow_banks": [],
            "shield_collision_tree": None,
        }

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
                for obj in self.pof_data.get("objects", [])
                if obj.get("number") == subobj_num
            ),
            None,
        )

        if sobj_data:
            offset = sobj_data.get("bsp_data_offset", -1)
            size = sobj_data.get("bsp_data_size", 0)
            return self._read_bsp_data(subobj_num, offset, size)

        logger.warning(f"Subobject {subobj_num} not found in parsed data.")
        return None

    def parse(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Parse POF file and return structured data.

        Args:
            file_path: Path to POF file to parse

        Returns:
            Dictionary containing parsed POF data, or None if parsing failed
        """
        # Reset data for new parse
        self._initialize_data_structure()
        self.pof_data["filename"] = file_path.name
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
            
            # Read POF header
            pof_id = struct.unpack("<I", f.read(4))[0]
            pof_version = struct.unpack("<i", f.read(4))[0]

            if pof_id != POF_HEADER_ID:
                self.error_handler.add_error(
                    f"Invalid POF header ID. Expected {POF_HEADER_ID:08X}, got {pof_id:08X}",
                    severity=ErrorSeverity.ERROR,
                    category=ErrorCategory.VALIDATION,
                    recovery_action="Check if file is a valid POF file"
                )
                return False

            # Version compatibility check
            self.error_handler.set_version_context(pof_version)
            
            if pof_version < PM_COMPATIBLE_VERSION:
                self.error_handler.add_error(
                    f"POF version {pof_version} is below minimum compatible version {PM_COMPATIBLE_VERSION}",
                    severity=ErrorSeverity.WARNING,
                    category=ErrorCategory.COMPATIBILITY,
                    recovery_action="Attempt parsing with fallback methods"
                )
            elif (pof_version // 100) > PM_OBJFILE_MAJOR_VERSION:
                self.error_handler.add_error(
                    f"POF version {pof_version} may be incompatible (major version > {PM_OBJFILE_MAJOR_VERSION})",
                    severity=ErrorSeverity.WARNING,
                    category=ErrorCategory.COMPATIBILITY,
                    recovery_action="Proceed with caution and validate results"
                )

            self.pof_data["version"] = pof_version
            logger.debug(f"POF Version: {pof_version}")
            return True

        except (struct.error, EOFError) as e:
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

        # Chunk ID to name mapping for error reporting
        chunk_name_map = {
            ID_OHDR: "OHDR",
            ID_SOBJ: "SOBJ", 
            ID_TXTR: "TXTR",
            ID_SPCL: "SPCL",
            ID_PATH: "PATH",
            ID_GPNT: "GPNT",
            ID_MPNT: "MPNT",
            ID_DOCK: "DOCK",
            ID_FUEL: "FUEL",
            ID_SHLD: "SHLD",
            ID_EYE: "EYE",
            ID_INSG: "INSG",
            ID_ACEN: "ACEN",
            ID_GLOW: "GLOW",
            ID_SLDC: "SLDC",
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

                chunk_id, chunk_len = read_chunk_header(f)
                chunk_name = chunk_name_map.get(chunk_id, f"UNKNOWN_{chunk_id:08X}")
                
                self.error_handler.set_chunk_context(chunk_id, chunk_name)
                logger.debug(f"Found chunk ID: {chunk_id:08X} ({chunk_name}), Length: {chunk_len}")

            except (struct.error, EOFError) as e:
                self.error_handler.add_error(
                    f"Failed to read chunk header: {e}",
                    severity=ErrorSeverity.WARNING,
                    category=ErrorCategory.PARSING,
                    recovery_action="Assume end of file reached"
                )
                logger.debug("Reached end of file or failed to read chunk header")
                break
            except Exception as e:
                self.error_handler.add_error(
                    f"Unexpected error reading chunk header at pos {chunk_start_pos}: {e}",
                    severity=ErrorSeverity.ERROR,
                    category=ErrorCategory.PARSING,
                    recovery_action="Skip to next chunk if possible"
                )
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
            self._process_chunk(f, chunk_id, chunk_len, chunk_readers, data_key_map, chunk_name_map)

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
        chunk_name_map: Dict[int, str],
    ) -> None:
        """Process a single chunk with enhanced error handling."""
        reader_func = chunk_readers.get(chunk_id)
        chunk_name = chunk_name_map.get(chunk_id, f"UNKNOWN_{chunk_id:08X}")

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
        """Store parsed chunk data in the appropriate data structure."""
        if isinstance(self.pof_data[data_key], list):
            if chunk_id == ID_SOBJ:
                # SOBJ reader returns a dict, append it
                self.pof_data[data_key].append(parsed_data)
            elif isinstance(parsed_data, list):
                # Most others return a list of items, extend the list
                self.pof_data[data_key].extend(parsed_data)
            else:
                logger.error(
                    f"Reader for {chunk_id:08X} returned unexpected type {type(parsed_data)}"
                )
        else:
            # Assign directly for single-instance chunks
            self.pof_data[data_key] = parsed_data

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

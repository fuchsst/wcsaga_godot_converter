#!/usr/bin/env python3
"""
POF Binary Reader - Unified binary data reading utilities.

This module provides a consolidated set of functions for reading binary data
from POF files with proper error handling, validation, and context tracking.
It replaces the scattered reading functions across multiple files.
"""

import logging
import struct
from typing import Any, BinaryIO, List, Optional, Tuple, Union

from .pof_types import Vector3D
from .pof_error_handler import get_global_error_handler, ErrorSeverity, ErrorCategory

logger = logging.getLogger(__name__)


class POFBinaryReader:
    """Unified binary reader for POF file parsing with enhanced error handling."""
    
    def __init__(self, file_handle: Optional[BinaryIO] = None):
        """Initialize binary reader with optional file handle."""
        self.file_handle = file_handle
        self.current_position = 0
        self.error_handler = get_global_error_handler()
    
    # --- Position Management ---
    
    def tell(self) -> int:
        """Get current file position."""
        if self.file_handle:
            return self.file_handle.tell()
        return self.current_position
    
    def seek(self, position: int, whence: int = 0) -> int:
        """Seek to position in file."""
        if self.file_handle:
            result = self.file_handle.seek(position, whence)
            self.current_position = result
            return result
        # For buffer-based reading
        if whence == 0:  # SEEK_SET
            self.current_position = position
        elif whence == 1:  # SEEK_CUR
            self.current_position += position
        elif whence == 2:  # SEEK_END
            # This would require knowing buffer size
            raise NotImplementedError("SEEK_END not supported for buffer reading")
        return self.current_position
    
    # --- Core Reading Functions ---
    
    def read_bytes(self, count: int) -> bytes:
        """Read raw bytes with error handling."""
        try:
            if self.file_handle:
                data = self.file_handle.read(count)
                self.current_position = self.file_handle.tell()
            else:
                raise RuntimeError("No file handle available for reading")
            
            if len(data) < count:
                self.error_handler.add_error(
                    f"Unexpected end of file: requested {count} bytes but got {len(data)}",
                    severity=ErrorSeverity.ERROR,
                    category=ErrorCategory.IO,
                    recovery_action="Attempt to continue with partial data"
                )
            
            return data
            
        except Exception as e:
            self.error_handler.add_error(
                f"Failed to read {count} bytes: {e}",
                severity=ErrorSeverity.CRITICAL,
                category=ErrorCategory.IO,
                recovery_action="Abort reading operation"
            )
            raise
    
    def read_struct(self, format_string: str) -> Tuple[Any, ...]:
        """Read structured binary data."""
        try:
            size = struct.calcsize(format_string)
            data = self.read_bytes(size)
            if len(data) < size:
                raise EOFError(f"Insufficient data for struct format {format_string}")
            return struct.unpack(format_string, data)
        except struct.error as e:
            self.error_handler.add_error(
                f"Failed to unpack struct with format {format_string}: {e}",
                severity=ErrorSeverity.ERROR,
                category=ErrorCategory.PARSING,
                recovery_action="Skip struct and continue"
            )
            raise
    
    # --- Primitive Type Readers ---
    
    def read_int8(self) -> int:
        """Read signed 8-bit integer."""
        return self.read_struct("<b")[0]
    
    def read_uint8(self) -> int:
        """Read unsigned 8-bit integer."""
        return self.read_struct("<B")[0]
    
    def read_int16(self) -> int:
        """Read signed 16-bit integer."""
        return self.read_struct("<h")[0]
    
    def read_uint16(self) -> int:
        """Read unsigned 16-bit integer."""
        return self.read_struct("<H")[0]
    
    def read_int32(self) -> int:
        """Read signed 32-bit integer."""
        return self.read_struct("<i")[0]
    
    def read_uint32(self) -> int:
        """Read unsigned 32-bit integer."""
        return self.read_struct("<I")[0]
    
    def read_float32(self) -> float:
        """Read 32-bit floating point number."""
        return self.read_struct("<f")[0]
    
    def read_double64(self) -> float:
        """Read 64-bit floating point number."""
        return self.read_struct("<d")[0]
    
    # --- String Readers ---
    
    def read_string(self, max_length: int) -> str:
        """Read null-terminated string with maximum length."""
        try:
            chars = []
            for _ in range(max_length):
                byte = self.read_bytes(1)
                if not byte or byte == b"\x00":
                    break
                chars.append(byte)
            
            return b"".join(chars).decode("utf-8", errors="replace")
            
        except Exception as e:
            self.error_handler.add_error(
                f"Failed to read string of max length {max_length}: {e}",
                severity=ErrorSeverity.WARNING,
                category=ErrorCategory.PARSING,
                recovery_action="Return empty string"
            )
            return ""
    
    def read_length_prefixed_string(self, max_length: int = 1024) -> str:
        """Read length-prefixed string."""
        try:
            length = self.read_int32()
            if length <= 0:
                return ""
            if length > max_length:
                self.error_handler.add_error(
                    f"String length {length} exceeds maximum {max_length}",
                    severity=ErrorSeverity.WARNING,
                    category=ErrorCategory.VALIDATION,
                    recovery_action=f"Truncating to {max_length} characters"
                )
                length = max_length
            
            data = self.read_bytes(length)
            return data.decode("utf-8", errors="replace")
            
        except Exception as e:
            self.error_handler.add_error(
                f"Failed to read length-prefixed string: {e}",
                severity=ErrorSeverity.WARNING,
                category=ErrorCategory.PARSING,
                recovery_action="Return empty string"
            )
            return ""
    
    # --- Vector Readers ---
    
    def read_vector3d(self) -> Vector3D:
        """Read 3D vector (12 bytes: 3 floats)."""
        try:
            x, y, z = self.read_struct("<fff")
            return Vector3D(x, y, z)
        except Exception as e:
            self.error_handler.add_error(
                f"Failed to read Vector3D: {e}",
                severity=ErrorSeverity.ERROR,
                category=ErrorCategory.PARSING,
                recovery_action="Return zero vector"
            )
            return Vector3D(0.0, 0.0, 0.0)
    
    def read_matrix3x3(self) -> List[List[float]]:
        """Read 3x3 matrix (36 bytes: 9 floats, stored as row-major)."""
        try:
            matrix = []
            for _ in range(3):  # 3 rows
                row = list(self.read_struct("<fff"))  # 3 floats per row
                matrix.append(row)
            return matrix
        except Exception as e:
            self.error_handler.add_error(
                f"Failed to read 3x3 matrix: {e}",
                severity=ErrorSeverity.ERROR,
                category=ErrorCategory.PARSING,
                recovery_action="Return identity matrix"
            )
            return [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    
    # --- Array Readers ---
    
    def read_array(self, element_reader, count: int) -> List[Any]:
        """Read array of elements using provided reader function."""
        elements = []
        for i in range(count):
            try:
                element = element_reader()
                elements.append(element)
            except Exception as e:
                self.error_handler.add_error(
                    f"Failed to read array element {i}/{count}: {e}",
                    severity=ErrorSeverity.ERROR,
                    category=ErrorCategory.PARSING,
                    recovery_action="Skip element and continue"
                )
                # Depending on context, we might want to break or continue
                # For now, continue to maintain array size
                elements.append(None)
        return elements
    
    def read_vector3d_array(self, count: int) -> List[Vector3D]:
        """Read array of Vector3D objects."""
        return self.read_array(self.read_vector3d, count)
    
    def read_float32_array(self, count: int) -> List[float]:
        """Read array of 32-bit floats."""
        return [self.read_float32() for _ in range(count)]
    
    def read_int32_array(self, count: int) -> List[int]:
        """Read array of 32-bit integers."""
        return [self.read_int32() for _ in range(count)]
    
    # --- Chunk Header Reader ---
    
    def read_chunk_header(self) -> Tuple[int, int]:
        """Read 8-byte chunk header (ID and Length)."""
        try:
            chunk_id = self.read_uint32()
            chunk_len = self.read_int32()
            return chunk_id, chunk_len
        except Exception as e:
            self.error_handler.add_error(
                f"Failed to read chunk header: {e}",
                severity=ErrorSeverity.ERROR,
                category=ErrorCategory.PARSING,
                recovery_action="Assume end of file"
            )
            raise
    
    # --- Validation Helpers ---
    
    def validate_range(self, value: Union[int, float], min_val: Union[int, float], 
                      max_val: Union[int, float], name: str = "value") -> bool:
        """Validate that value is within range."""
        if not (min_val <= value <= max_val):
            self.error_handler.add_error(
                f"{name} {value} out of range [{min_val}, {max_val}]",
                severity=ErrorSeverity.WARNING,
                category=ErrorCategory.VALIDATION,
                recovery_action=f"Clamp {name} to valid range"
            )
            return False
        return True
    
    def validate_non_negative(self, value: Union[int, float], name: str = "value") -> bool:
        """Validate that value is non-negative."""
        if value < 0:
            self.error_handler.add_error(
                f"{name} {value} should be non-negative",
                severity=ErrorSeverity.WARNING,
                category=ErrorCategory.VALIDATION,
                recovery_action=f"Use absolute value for {name}"
            )
            return False
        return True


# --- Convenience Functions ---

def create_reader(file_handle: BinaryIO) -> POFBinaryReader:
    """Create POF binary reader instance."""
    return POFBinaryReader(file_handle)


# --- Backward Compatibility Aliases ---
# These maintain the same interface as the original pof_chunks.py functions

def read_int(f: BinaryIO) -> int:
    """Read 4-byte signed integer (backward compatibility)."""
    reader = POFBinaryReader(f)
    return reader.read_int32()


def read_uint(f: BinaryIO) -> int:
    """Read 4-byte unsigned integer (backward compatibility)."""
    reader = POFBinaryReader(f)
    return reader.read_uint32()


def read_short(f: BinaryIO) -> int:
    """Read 2-byte signed short (backward compatibility)."""
    reader = POFBinaryReader(f)
    return reader.read_int16()


def read_ushort(f: BinaryIO) -> int:
    """Read 2-byte unsigned short (backward compatibility)."""
    reader = POFBinaryReader(f)
    return reader.read_uint16()


def read_float(f: BinaryIO) -> float:
    """Read 4-byte float (backward compatibility)."""
    reader = POFBinaryReader(f)
    return reader.read_float32()


def read_byte(f: BinaryIO) -> int:
    """Read 1-byte signed byte (backward compatibility)."""
    reader = POFBinaryReader(f)
    return reader.read_int8()


def read_ubyte(f: BinaryIO) -> int:
    """Read 1-byte unsigned byte (backward compatibility)."""
    reader = POFBinaryReader(f)
    return reader.read_uint8()


def read_vector(f: BinaryIO) -> Vector3D:
    """Read 12-byte vector (backward compatibility)."""
    reader = POFBinaryReader(f)
    return reader.read_vector3d()


def read_matrix(f: BinaryIO) -> List[List[float]]:
    """Read 36-byte 3x3 matrix (backward compatibility)."""
    reader = POFBinaryReader(f)
    return reader.read_matrix3x3()


def read_string(f: BinaryIO, max_len: int) -> str:
    """Read null-terminated string with max length (backward compatibility)."""
    reader = POFBinaryReader(f)
    return reader.read_string(max_len)


def read_string_len(f: BinaryIO, max_len: int) -> str:
    """Read length-prefixed string with max length (backward compatibility)."""
    reader = POFBinaryReader(f)
    return reader.read_length_prefixed_string(max_len)


def read_chunk_header(f: BinaryIO) -> Tuple[int, int]:
    """Read 8-byte chunk header (ID and Length) (backward compatibility)."""
    reader = POFBinaryReader(f)
    return reader.read_chunk_header()
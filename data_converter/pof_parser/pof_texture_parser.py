#!/usr/bin/env python3
"""
POF Texture Parser - Consolidated TXTR chunk parsing.

This module provides unified parsing for the Texture Filenames chunk using
the enhanced binary reader with improved error handling and validation.
"""

import logging
from typing import BinaryIO, List

# Import necessary helper functions from pof_binary_reader
from .pof_binary_reader import create_reader
from .pof_error_handler import get_global_error_handler, ErrorSeverity, ErrorCategory

logger = logging.getLogger(__name__)


def read_txtr_chunk(f: BinaryIO, length: int) -> List[str]:
    """
    Parses the Texture Filenames (TXTR) chunk with enhanced error handling.

    This function uses the enhanced binary reader for robust parsing with
    validation and error recovery.
    """
    reader = create_reader(f)
    error_handler = get_global_error_handler()

    try:
        num_textures = reader.read_int32()

        # Validate number of textures
        if num_textures < 0:
            error_handler.add_validation_error(
                f"Negative texture count: {num_textures}",
                recovery_action="Treating as zero textures",
            )
            num_textures = 0
        elif num_textures > 1000:  # Reasonable limit to prevent memory issues
            error_handler.add_validation_error(
                f"Excessive texture count: {num_textures}",
                recovery_action="Limiting to 1000 textures",
            )
            num_textures = min(num_textures, 1000)

        textures = []
        # Use a reasonable max length for texture filenames, adjust if needed
        max_texture_name_len = 128  # Increased from 64 for longer paths

        for i in range(num_textures):
            try:
                texture_name = reader.read_length_prefixed_string(max_texture_name_len)

                # Validate texture name
                if not texture_name:
                    error_handler.add_data_integrity_warning(
                        f"Empty texture name at index {i}",
                        recovery_action="Skipping empty texture",
                    )
                    continue

                # Sanitize texture name (remove invalid characters, normalize path separators)
                sanitized_name = _sanitize_texture_name(texture_name)
                textures.append(sanitized_name)

            except Exception as e:
                error_handler.add_error(
                    f"Failed to read texture name {i}/{num_textures}: {e}",
                    severity=ErrorSeverity.WARNING,
                    category=ErrorCategory.PARSING,
                    recovery_action="Skipping texture and continuing",
                )
                # Continue with next texture

        return textures

    except Exception as e:
        error_handler.add_error(
            f"Failed to parse TXTR chunk: {e}",
            severity=ErrorSeverity.ERROR,
            category=ErrorCategory.PARSING,
            recovery_action="Returning empty texture list",
        )
        return []


def _sanitize_texture_name(texture_name: str) -> str:
    """
    Sanitize texture name by removing invalid characters and normalizing format.

    Args:
        texture_name: Raw texture name from POF file

    Returns:
        Sanitized texture name
    """
    # Remove null terminators and control characters
    sanitized = "".join(c for c in texture_name if ord(c) >= 32 or c == "\t")

    # Normalize path separators (convert backslashes to forward slashes)
    sanitized = sanitized.replace("\\\\", "/")

    # Remove duplicate slashes
    while "//" in sanitized:
        sanitized = sanitized.replace("//", "/")

    # Strip leading/trailing whitespace
    sanitized = sanitized.strip()

    return sanitized

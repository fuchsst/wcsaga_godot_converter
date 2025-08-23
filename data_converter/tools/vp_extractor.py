#!/usr/bin/env python3
"""
VP Extractor - Wing Commander Saga VP Archive Tool

This tool provides functionalities to list and extract files from the
Wing Commander Saga's .vp (V-Pak) archive files. It is designed to
be used as a command-line utility for asset inspection and extraction
during the migration process.

Author: Dev (GDScript Developer)
Date: August 23, 2025
Story: DM-015 - VP Archive Extraction Tool
Epic: EPIC-003 - Data Migration & Conversion Tools
"""

import argparse
import logging
import os
import struct
from pathlib import Path
from typing import List, NamedTuple

logger = logging.getLogger(__name__)


class VPHeader(NamedTuple):
    """Represents the header of a VP archive."""

    signature: bytes
    version: int
    index_offset: int
    num_files: int


class VPFileEntry(NamedTuple):
    """Represents a single file entry in the VP archive index."""

    offset: int
    size: int
    name: str
    timestamp: int


class VPExtractor:
    """
    Handles the parsing and extraction of Wing Commander Saga VP archives.
    """

    def __init__(self, vp_file_path: Path):
        """
        Initialize the extractor with the path to a .vp file.

        Args:
            vp_file_path: The path to the .vp archive file.
        """
        self.vp_file_path = vp_file_path
        self.header: VPHeader = None
        self.file_entries: List[VPFileEntry] = []

    def read_archive(self) -> bool:
        """
        Reads the header and file index of the VP archive.

        Returns:
            True if the archive was read successfully, False otherwise.
        """
        try:
            with open(self.vp_file_path, "rb") as f:
                # Read header (16 bytes)
                sig = f.read(4)
                if sig != b"VPVP":
                    logger.error(
                        f"Invalid VP file signature for {self.vp_file_path}. Expected VPVP, got {sig}"
                    )
                    return False

                version, index_offset, num_files = struct.unpack("<III", f.read(12))
                self.header = VPHeader(sig, version, index_offset, num_files)
                logger.debug(f"Header parsed: {self.header}")

                # Seek to the file index
                f.seek(self.header.index_offset)

                # Read file entries - each entry is 44 bytes: offset (4), size (4), name[32] (32), timestamp (4)
                for i in range(self.header.num_files):
                    try:
                        # Read the 8 bytes for offset and size
                        offset_size_data = f.read(8)
                        if len(offset_size_data) < 8:
                            logger.warning(
                                f"Failed to read complete offset/size data for entry {i}, possibly end of file"
                            )
                            break

                        offset, size = struct.unpack("<II", offset_size_data)

                        # Read the 32-byte name field
                        name_bytes = f.read(32)
                        if len(name_bytes) < 32:
                            logger.warning(
                                f"Failed to read complete name data for entry {i}, possibly end of file"
                            )
                            break

                        name = name_bytes.decode("utf-8", errors="ignore").split(
                            "\x00"
                        )[
                            0
                        ]  # Null-terminated string

                        # Read the 4-byte timestamp
                        timestamp_data = f.read(4)
                        if len(timestamp_data) < 4:
                            logger.warning(
                                f"Failed to read complete timestamp data for entry {i}, possibly end of file"
                            )
                            break

                        timestamp = struct.unpack("<I", timestamp_data)[0]

                        # Skip directory entries (size = 0) and backdir entries (name = "..")
                        if size == 0 or name == "..":
                            continue

                        entry = VPFileEntry(offset, size, name, timestamp)
                        self.file_entries.append(entry)

                    except struct.error as e:
                        logger.error(
                            f"Struct error reading entry {i}: {e}. Skipping entry."
                        )
                        # Attempt to skip to the next entry by moving forward 44 bytes (total entry size)
                        # Since we might have read partial data, calculate how much to skip
                        current_pos = f.tell()
                        bytes_read = current_pos - (self.header.index_offset + i * 44)
                        bytes_to_skip = 44 - bytes_read
                        if bytes_to_skip > 0:
                            f.read(bytes_to_skip)
                        continue
                    except Exception as e:
                        logger.error(
                            f"Unexpected error reading entry {i}: {e}. Skipping entry."
                        )
                        # Attempt to skip to the next entry
                        current_pos = f.tell()
                        bytes_read = current_pos - (self.header.index_offset + i * 44)
                        bytes_to_skip = 44 - bytes_read
                        if bytes_to_skip > 0:
                            f.read(bytes_to_skip)
                        continue

                logger.info(
                    f"Successfully read index of {len(self.file_entries)} files from {self.vp_file_path.name}"
                )
                return True

        except FileNotFoundError:
            logger.error(f"VP file not found: {self.vp_file_path}")
            return False
        except Exception as e:
            logger.error(
                f"Failed to read VP archive {self.vp_file_path}: {e}", exc_info=True
            )
            return False

    def list_files(self):
        """Prints a formatted list of files in the archive."""
        if not self.file_entries:
            print("No file entries to list. Please read the archive first.")
            return

        print(f"Contents of archive: {self.vp_file_path.name}")
        print(f"{'Filename':<60} {'Size (bytes)':>15} {'Offset':>12}")
        print("-" * 89)

        total_size = 0
        for entry in self.file_entries:
            print(f"{entry.name:<60} {entry.size:>15,} {entry.offset:>12,}")
            total_size += entry.size

        print("-" * 89)
        print(f"Total files: {len(self.file_entries)}")
        print(f"Total size: {total_size:,} bytes")

    def extract_all(self, output_dir: Path):
        """
        Extracts all files from the VP archive to the specified directory.

        Args:
            output_dir: The directory where files will be extracted.
        """
        if not self.file_entries:
            logger.error("No file entries to extract. Please read the archive first.")
            return

        logger.info(f"Extracting {len(self.file_entries)} files to {output_dir}...")
        output_dir.mkdir(parents=True, exist_ok=True)

        try:
            with open(self.vp_file_path, "rb") as f:
                for i, entry in enumerate(self.file_entries):
                    logger.debug(
                        f"Extracting ({i+1}/{len(self.file_entries)}): {entry.name}"
                    )

                    # Create subdirectories if necessary
                    target_path = output_dir / entry.name
                    target_path.parent.mkdir(parents=True, exist_ok=True)

                    # Seek to file data and write to disk
                    f.seek(entry.offset)
                    file_data = f.read(entry.size)

                    with open(target_path, "wb") as out_f:
                        out_f.write(file_data)

            logger.info("Extraction completed successfully.")

        except Exception as e:
            logger.error(f"An error occurred during extraction: {e}", exc_info=True)


def main():
    """Command-line interface for the VP Extractor."""
    parser = argparse.ArgumentParser(
        description="List and extract files from Wing Commander Saga .vp archives."
    )
    parser.add_argument("vp_file", type=Path, help="Path to the .vp archive file.")
    parser.add_argument(
        "-l", "--list", action="store_true", help="List the contents of the archive."
    )
    parser.add_argument(
        "-x",
        "--extract",
        type=Path,
        metavar="OUTPUT_DIR",
        help="Extract all files from the archive to the specified directory.",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging output."
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    if not args.vp_file.exists():
        logger.error(f"Input file not found: {args.vp_file}")
        return 1

    try:
        extractor = VPExtractor(args.vp_file)
        if not extractor.read_archive():
            return 1

        if args.list:
            extractor.list_files()

        if args.extract:
            extractor.extract_all(args.extract)

        if not args.list and not args.extract:
            logger.warning("No action specified. Use -l to list or -x to extract.")
            parser.print_help()

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=args.verbose)
        return 1

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())

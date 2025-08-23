#!/usr/bin/env python3
"""
Table Conversion CLI Tool

Command-line interface for converting WCS table files to Godot resources.
This module extracts the CLI functionality from table_data_converter.py
for better separation of concerns.

Author: Dev (GDScript Developer)
Date: June 14, 2025
Epic: EPIC-003 - Data Migration & Conversion Tools
"""

import argparse
import json
import logging
import sys
from pathlib import Path

from ..table_data_converter import TableDataConverter

logger = logging.getLogger(__name__)

def main():
    """Main function for standalone table converter usage"""
    
    parser = argparse.ArgumentParser(description='Convert WCS table files to Godot resources')
    parser.add_argument('--source', type=Path, required=True,
                       help='Path to WCS source directory')
    parser.add_argument('--target', type=Path, required=True,
                       help='Path to Godot project directory')
    parser.add_argument('--file', type=Path,
                       help='Convert specific table file')
    parser.add_argument('--validate', action='store_true',
                       help='Validate converted resources')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
    
    try:
        # Initialize converter
        converter = TableDataConverter(args.source, args.target)
        
        if args.file:
            # Convert specific file
            success = converter.convert_table_file(args.file)
            print(f"Conversion {'successful' if success else 'failed'}: {args.file}")
        else:
            # Convert all table files
            table_files = list(args.source.glob("**/*.tbl")) + list(args.source.glob("**/*.tbm"))
            
            if not table_files:
                print(f"No table files found in {args.source}")
                return 1
            
            print(f"Found {len(table_files)} table files to convert")
            
            success_count = 0
            for table_file in table_files:
                if converter.convert_table_file(table_file):
                    success_count += 1
            
            print(f"Converted {success_count}/{len(table_files)} table files successfully")
        
        # Generate summary report
        summary = converter.generate_conversion_summary()
        
        # Save summary
        summary_path = args.target / "table_conversion_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"Conversion summary saved to: {summary_path}")
        
        return 0 if success_count > 0 else 1
        
    except Exception as e:
        logger.error(f"Table conversion failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
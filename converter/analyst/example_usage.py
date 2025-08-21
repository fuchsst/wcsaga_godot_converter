#!/usr/bin/env python3
"""
Example script demonstrating the use of the Codebase Analyst agent.
"""

import json
import sys
import os

# Add the converter directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from converter.analyst.codebase_analyst import CodebaseAnalyst


def main():
    """Main function demonstrating the Codebase Analyst."""
    # Create an instance of the analyst
    analyst = CodebaseAnalyst()
    
    # Example: Analyze a ship entity
    entity_name = "GTF Myrmidon"
    source_files = [
        "source/tables/ships.tbl",
        "source/models/myrmidon.pof",
        "source/code/ship.cpp",
        "source/code/ship.h"
    ]
    
    print(f"Analyzing entity: {entity_name}")
    print(f"Source files: {source_files}")
    print("\n" + "="*50 + "\n")
    
    # Perform the analysis
    analysis = analyst.analyze_entity(entity_name, source_files)
    
    # Print the results in a formatted way
    print(json.dumps(analysis, indent=2))
    
    # Example of how the output might be used
    print("\n" + "="*50 + "\n")
    print("Component Breakdown:")
    for category, components in analysis["components"].items():
        print(f"\n{category.upper()}:")
        for component in components:
            print(f"  - {component.get('description', 'N/A')} ({component.get('file', 'N/A')})")


if __name__ == "__main__":
    main()
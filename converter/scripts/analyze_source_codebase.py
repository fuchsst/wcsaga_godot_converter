#!/usr/bin/env python3
"""
Source Codebase Analysis Script

This script analyzes the source C++ codebase to identify files, dependencies,
and architectural patterns to inform the migration process.
"""

import argparse
import json
import logging
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

# Import dependency graph for shared state storage
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from graph_system.dependency_graph import DependencyGraph

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class SourceCodebaseAnalyzer:
    """Analyzer for the source C++ codebase."""

    def __init__(self, source_path: str, graph_file: str = "dependency_graph.json"):
        """
        Initialize the analyzer.

        Args:
            source_path: Path to the source codebase
            graph_file: Path to the dependency graph file for shared state storage
        """
        self.source_path = Path(source_path)
        if not self.source_path.exists():
            raise ValueError(f"Source path does not exist: {self.source_path}")

        # Initialize dependency graph for shared state storage with migration
        self.graph_file = graph_file
        self.dependency_graph = DependencyGraph(self.graph_file)

        # File extensions to analyze
        self.cpp_extensions = {".h", ".hpp", ".cpp", ".cc", ".cxx"}
        self.asset_extensions = {
            ".png",
            ".jpg",
            ".jpeg",
            ".tga",
            ".wav",
            ".ogg",
            ".mp3",
            ".ttf",
            ".otf",
        }
        self.config_extensions = {".cfg", ".ini", ".xml", ".json"}

        # Directories to exclude from analysis (third-party libs and low-level utilities)
        self.excluded_dirs = {
            "boost",           # C++ compatibility library
            "libjpeg",         # JPEG library
            "libpng",          # PNG library
            "lua",             # Lua scripting library
            "oggvorbis",       # Ogg Vorbis audio library
            "openal",          # OpenAL audio library
            "speech",          # Speech library
            "zlib",            # Compression library
            "tgautils",        # TGA file utilities
            "pcxutils",        # PCX file utilities
            "jpgutils",        # JPEG utilities
            "pngutils",        # PNG utilities
            "ddsutils",        # DDS utilities
            "cfile",           # Low-level file I/O
            "globalincs",      # Global includes (may contain low-level utils)
            "windows_stub",    # Windows compatibility layer
        }

        # Analysis results (for backward compatibility)
        self.analysis_results = {
            "files": {},
            "dependencies": {},
            "classes": {},
            "functions": {},
            "assets": {},
            "statistics": {},
        }

    def analyze(self) -> Dict[str, Any]:
        """
        Perform complete analysis of the source codebase.

        Returns:
            Dictionary with analysis results
        """
        logger.info(f"Starting analysis of codebase at: {self.source_path}")

        # Find all files
        self._find_files()

        # Analyze C++ files
        self._analyze_cpp_files()

        # Analyze assets
        self._analyze_assets()

        # Calculate statistics
        self._calculate_statistics()

        logger.info("Codebase analysis completed")
        return self.analysis_results

    def _find_files(self):
        """Find all files in the source codebase, excluding specified directories."""
        logger.info("Finding files in codebase...")

        for root, dirs, files in os.walk(self.source_path):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            
            # Check if current directory path contains any excluded directories
            current_path = Path(root)
            relative_current_path = current_path.relative_to(self.source_path)
            
            # Skip this directory if any part of the path is in excluded_dirs
            if any(part in self.excluded_dirs for part in relative_current_path.parts):
                # Remove all subdirectories to prevent further traversal
                dirs[:] = []
                continue

            for file in files:
                file_path = Path(root) / file
                relative_path = file_path.relative_to(self.source_path)

                # Categorize files by extension
                extension = file_path.suffix.lower()
                file_type = "unknown"

                if extension in self.cpp_extensions:
                    file_type = "cpp"
                elif extension in self.asset_extensions:
                    file_type = "asset"
                elif extension in self.config_extensions:
                    file_type = "config"
                elif extension in {".md", ".txt", ".doc", ".docx"}:
                    file_type = "documentation"

                self.analysis_results["files"][str(relative_path)] = {
                    "type": file_type,
                    "size": file_path.stat().st_size,
                    "extension": extension,
                }

        logger.info(f"Found {len(self.analysis_results['files'])} files")

    def _analyze_cpp_files(self):
        """Analyze C++ files for classes, functions, and dependencies."""
        logger.info("Analyzing C++ files...")

        cpp_files = {
            path: info
            for path, info in self.analysis_results["files"].items()
            if info["type"] == "cpp"
        }

        for file_path, file_info in cpp_files.items():
            full_path = self.source_path / file_path
            self._analyze_single_cpp_file(full_path, file_path)

    def _add_file_to_graph(self, file_path: str, file_type: str, size: int, extension: str):
        """Add a file entity to the dependency graph."""
        entity_id = f"FILE-{file_path.replace('/', '_').replace('.', '_')}"
        properties = {
            "name": file_path,
            "type": "file",
            "file_type": file_type,
            "size": size,
            "extension": extension,
        }
        self.dependency_graph.add_entity(entity_id, "file", properties)
        return entity_id

    def _analyze_single_cpp_file(self, full_path: Path, relative_path: str):
        """
        Analyze a single C++ file and populate dependency graph.

        Args:
            full_path: Full path to the file
            relative_path: Relative path from source root
        """
        try:
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:
            logger.warning(f"Failed to read file {full_path}: {str(e)}")
            return

        # Find includes
        includes = self._find_includes(content)
        self.analysis_results["dependencies"][relative_path] = includes

        # Add current file to dependency graph
        file_entity_id = self._add_file_to_graph(
            str(relative_path),
            "cpp",
            full_path.stat().st_size,
            full_path.suffix
        )

        # Add dependencies for each include
        for included_file in includes:
            # Create an entity for the included file if it doesn't exist
            included_entity_id = f"FILE-{included_file.replace('/', '_').replace('.', '_')}"
            self.dependency_graph.add_entity(included_entity_id, "file", {"name": included_file})
            # Add dependency from current file to included file
            self.dependency_graph.add_dependency(file_entity_id, included_entity_id, "includes")

        # Find classes
        classes = self._find_classes(content)
        for class_name, class_info in classes.items():
            if class_name not in self.analysis_results["classes"]:
                self.analysis_results["classes"][class_name] = []
            class_info["file"] = relative_path
            self.analysis_results["classes"][class_name].append(class_info)

        # Find functions
        functions = self._find_functions(content)
        for func_name, func_info in functions.items():
            if func_name not in self.analysis_results["functions"]:
                self.analysis_results["functions"][func_name] = []
            func_info["file"] = relative_path
            self.analysis_results["functions"][func_name].append(func_info)

    def _find_includes(self, content: str) -> List[str]:
        """
        Find #include directives in C++ content.

        Args:
            content: C++ file content

        Returns:
            List of included files
        """
        includes = []
        include_pattern = r'#include\s*[<"]([^>"]+)[>"]'

        for match in re.finditer(include_pattern, content):
            includes.append(match.group(1))

        return includes

    def _find_classes(self, content: str) -> Dict[str, Dict[str, Any]]:
        """
        Find class declarations in C++ content.

        Args:
            content: C++ file content

        Returns:
            Dictionary of classes found
        """
        classes = {}

        # Simple pattern for class declarations
        class_pattern = (
            r"class\s+(\w+)(?:\s*:\s*(public|private|protected)\s+(\w+))?\s*{"
        )

        for match in re.finditer(class_pattern, content):
            class_name = match.group(1)
            inheritance_type = match.group(2)
            parent_class = match.group(3)

            classes[class_name] = {
                "name": class_name,
                "inheritance": (
                    {"type": inheritance_type, "parent": parent_class}
                    if inheritance_type and parent_class
                    else None
                ),
                "line": content.count("\n", 0, match.start()) + 1,
            }

        return classes

    def _find_functions(self, content: str) -> Dict[str, Dict[str, Any]]:
        """
        Find function declarations in C++ content.

        Args:
            content: C++ file content

        Returns:
            Dictionary of functions found
        """
        functions = {}

        # Pattern for function declarations (simplified)
        func_pattern = r"(\w+(?:\s*\*+)?)\s+(\w+)\s*\([^)]*\)\s*{"

        for match in re.finditer(func_pattern, content):
            return_type = match.group(1).strip()
            func_name = match.group(2)

            # Skip common keywords that might match
            if func_name in {
                "if",
                "for",
                "while",
                "switch",
                "class",
                "struct",
                "namespace",
            }:
                continue

            functions[func_name] = {
                "name": func_name,
                "return_type": return_type,
                "line": content.count("\n", 0, match.start()) + 1,
            }

        return functions

    def _analyze_assets(self):
        """Analyze asset files."""
        logger.info("Analyzing assets...")

        asset_files = {
            path: info
            for path, info in self.analysis_results["files"].items()
            if info["type"] == "asset"
        }

        for file_path, file_info in asset_files.items():
            self.analysis_results["assets"][file_path] = {
                "type": file_info["extension"][1:],  # Remove the dot
                "size": file_info["size"],
            }

    def _calculate_statistics(self):
        """Calculate statistics for the codebase."""
        logger.info("Calculating statistics...")

        # File type counts
        file_types = {}
        for file_info in self.analysis_results["files"].values():
            file_type = file_info["type"]
            file_types[file_type] = file_types.get(file_type, 0) + 1

        # Class and function counts
        class_count = len(self.analysis_results["classes"])
        function_count = len(self.analysis_results["functions"])

        # Dependency counts
        dependency_count = sum(
            len(deps) for deps in self.analysis_results["dependencies"].values()
        )

        # Asset counts
        asset_count = len(self.analysis_results["assets"])

        self.analysis_results["statistics"] = {
            "total_files": len(self.analysis_results["files"]),
            "file_types": file_types,
            "classes": class_count,
            "functions": function_count,
            "dependencies": dependency_count,
            "assets": asset_count,
        }

    def export_results(self, output_file: str, format: str = "json"):
        """
        Export analysis results to a file.

        Args:
            output_file: Path to output file
            format: Output format ("json" or "txt")
        """
        logger.info(f"Exporting results to {output_file}")

        if format == "json":
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(self.analysis_results, f, indent=2, default=str)
        elif format == "txt":
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(self._format_results_as_text())
        else:
            raise ValueError(f"Unsupported format: {format}")

        logger.info("Results exported successfully")

    def _format_results_as_text(self) -> str:
        """Format analysis results as text."""
        lines = []
        lines.append("Wing Commander Saga Codebase Analysis Report")
        lines.append("=" * 50)
        lines.append("")

        # Statistics
        stats = self.analysis_results["statistics"]
        lines.append("STATISTICS")
        lines.append("-" * 20)
        lines.append(f"Total Files: {stats['total_files']}")
        lines.append("File Types:")
        for file_type, count in stats["file_types"].items():
            lines.append(f"  {file_type}: {count}")
        lines.append(f"Classes: {stats['classes']}")
        lines.append(f"Functions: {stats['functions']}")
        lines.append(f"Dependencies: {stats['dependencies']}")
        lines.append(f"Assets: {stats['assets']}")
        lines.append("")

        # Classes
        lines.append("CLASSES")
        lines.append("-" * 20)
        for class_name, class_info_list in self.analysis_results["classes"].items():
            lines.append(f"{class_name}:")
            for class_info in class_info_list:
                lines.append(f"  File: {class_info['file']}")
                if class_info["inheritance"]:
                    lines.append(
                        f"  Inheritance: {class_info['inheritance']['type']} {class_info['inheritance']['parent']}"
                    )
                lines.append(f"  Line: {class_info['line']}")
            lines.append("")

        # Functions
        lines.append("FUNCTIONS")
        lines.append("-" * 20)
        for func_name, func_info_list in self.analysis_results["functions"].items():
            lines.append(f"{func_name}:")
            for func_info in func_info_list:
                lines.append(f"  File: {func_info['file']}")
                lines.append(f"  Return Type: {func_info['return_type']}")
                lines.append(f"  Line: {func_info['line']}")
            lines.append("")

        return "\n".join(lines)


def main():
    """Main entry point for the analysis script."""
    parser = argparse.ArgumentParser(
        description="Analyze Wing Commander Saga C++ Codebase"
    )
    parser.add_argument(
        "--source", required=True, help="Path to the source C++ codebase"
    )
    parser.add_argument("--output", help="Output file for analysis results")
    parser.add_argument(
        "--format",
        choices=["json", "txt"],
        default="json",
        help="Output format (default: json)",
    )
    parser.add_argument(
        "--graph-file",
        default="dependency_graph.json",
        help="Path to the dependency graph file for shared state storage (default: dependency_graph.json)",
    )

    args = parser.parse_args()

    try:
        # Create analyzer and run analysis
        analyzer = SourceCodebaseAnalyzer(args.source, args.graph_file)
        results = analyzer.analyze()

        # Save the dependency graph to ensure state is persisted
        analyzer.dependency_graph.save_graph()

        # Print summary to console
        stats = results["statistics"]
        print(f"Analysis complete!")
        print(f"Total files: {stats['total_files']}")
        print(f"Classes: {stats['classes']}")
        print(f"Functions: {stats['functions']}")
        print(f"Assets: {stats['assets']}")
        print(f"Dependency graph saved to: {args.graph_file}")

        # Export results if requested
        if args.output:
            analyzer.export_results(args.output, args.format)
            print(f"Results exported to: {args.output}")

    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

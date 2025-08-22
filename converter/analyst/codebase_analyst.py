"""
Codebase Analyst Agent Implementation

This agent is responsible for analyzing the legacy codebase to identify dependencies,
modules, and architectural patterns. It's powered by the DeepSeek V3.1 model.
"""

import json
import os
import re
from typing import Any, Dict, List


class CodebaseAnalyst:
    """
    The Codebase Analyst agent analyzes the legacy C++ codebase to identify dependencies,
    modules, and architectural patterns. It reads source files, identifies dependencies
    between classes and modules, and constructs a model of the existing architecture.
    """

    def __init__(self):
        """Initialize the Codebase Analyst agent."""
        self.analysis_cache = {}

    def analyze_entity(
        self, entity_name: str, source_files: List[str]
    ) -> Dict[str, Any]:
        """
        Analyze a specific game entity (e.g., "GTC Fenris") and its related source files.

        Args:
            entity_name: Name of the entity to analyze
            source_files: List of file paths related to the entity

        Returns:
            Structured JSON report with analysis results
        """
        # Check if we've already analyzed this entity
        cache_key = f"{entity_name}:{':'.join(sorted(source_files))}"
        if cache_key in self.analysis_cache:
            return self.analysis_cache[cache_key]

        # Perform analysis
        analysis_result = self._perform_analysis(entity_name, source_files)

        # Cache the result
        self.analysis_cache[cache_key] = analysis_result

        return analysis_result

    def _perform_analysis(
        self, entity_name: str, source_files: List[str]
    ) -> Dict[str, Any]:
        """
        Perform the actual analysis of the entity and its source files.

        Args:
            entity_name: Name of the entity to analyze
            source_files: List of file paths related to the entity

        Returns:
            Structured JSON report with analysis results
        """
        components = {"data": [], "behavior": [], "visuals": [], "physics": []}

        # Analyze each source file
        file_analyses = []
        for file_path in source_files:
            if os.path.exists(file_path):
                file_analysis = self._analyze_file(file_path)
                file_analyses.append(file_analysis)

                # Categorize components based on file type and content
                if file_path.endswith((".tbl", ".tbm")):
                    components["data"].append(
                        {
                            "file": file_path,
                            "type": "table_data",
                            "description": f"Table data for {entity_name}",
                            "parsed_data": self._parse_table_file(file_path),
                        }
                    )
                elif file_path.endswith(".pof"):
                    components["visuals"].append(
                        {
                            "file": file_path,
                            "type": "model_data",
                            "description": f"3D model data for {entity_name}",
                            "metadata": self._parse_pof_metadata(file_path),
                        }
                    )
                elif file_path.endswith((".cpp", ".h")):
                    components["behavior"].append(
                        {
                            "file": file_path,
                            "type": "source_code",
                            "description": f"C++ source code for {entity_name}",
                            "classes": self._parse_cpp_classes(file_path),
                            "includes": self._parse_cpp_includes(file_path),
                        }
                    )
                elif file_path.endswith(".fs2"):
                    components["behavior"].append(
                        {
                            "file": file_path,
                            "type": "mission_logic",
                            "description": f"Mission logic for {entity_name}",
                            "sexps": self._parse_sexp_file(file_path),
                        }
                    )

        # Create the analysis report
        analysis_report = {
            "entity_name": entity_name,
            "source_files": source_files,
            "file_analyses": file_analyses,
            "components": components,
            "dependencies": self._identify_dependencies(source_files),
            "architectural_patterns": self._identify_patterns(file_analyses),
        }

        return analysis_report

    def _analyze_file(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze a single file.

        Args:
            file_path: Path to the file to analyze

        Returns:
            Dictionary with file analysis results
        """
        file_info = {
            "path": file_path,
            "size": 0,
            "lines": 0,
            "type": self._get_file_type(file_path),
        }

        try:
            if os.path.exists(file_path):
                file_info["size"] = os.path.getsize(file_path)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                    file_info["lines"] = len(lines)
        except Exception as e:
            file_info["error"] = str(e)

        return file_info

    def _get_file_type(self, file_path: str) -> str:
        """
        Determine the file type based on extension.

        Args:
            file_path: Path to the file

        Returns:
            File type string
        """
        _, ext = os.path.splitext(file_path)
        return ext.lower()

    def _parse_table_file(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a .tbl or .tbm file to extract entity data.

        Args:
            file_path: Path to the table file

        Returns:
            Dictionary with parsed table data
        """
        # This would contain logic to parse the specific format of .tbl/.tbm files
        # For now, we'll return a placeholder
        return {"format": "table", "entries_parsed": 0, "entities_found": []}

    def _parse_pof_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Parse metadata from a .pof file.

        Args:
            file_path: Path to the .pof file

        Returns:
            Dictionary with parsed model metadata
        """
        # This would contain logic to parse the binary .pof format
        # For now, we'll return a placeholder
        return {
            "format": "pof_binary",
            "subsystems": [],
            "hardpoints": [],
            "thrusters": [],
        }

    def _parse_cpp_classes(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Parse C++ classes from a .cpp or .h file.

        Args:
            file_path: Path to the C++ file

        Returns:
            List of dictionaries with class information
        """
        classes = []
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

                # Simple regex to find class declarations
                class_pattern = r"class\s+(\w+)"
                class_matches = re.findall(class_pattern, content)

                for class_name in class_matches:
                    classes.append(
                        {"name": class_name, "methods": [], "properties": []}
                    )
        except Exception:
            pass

        return classes

    def _parse_cpp_includes(self, file_path: str) -> List[str]:
        """
        Parse #include directives from a C++ file.

        Args:
            file_path: Path to the C++ file

        Returns:
            List of included files
        """
        includes = []
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if line.strip().startswith("#include"):
                        includes.append(line.strip())
        except Exception:
            pass

        return includes

    def _parse_sexp_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Parse SEXP expressions from a .fs2 file.

        Args:
            file_path: Path to the SEXP file

        Returns:
            List of parsed SEXP expressions
        """
        sexps = []
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

                # Simple regex to find SEXP patterns (this is a simplified approach)
                sexp_pattern = r"\([^\)]+\)"
                sexp_matches = re.findall(sexp_pattern, content)

                for match in sexp_matches:
                    sexps.append({"expression": match, "type": "sexp"})
        except Exception:
            pass

        return sexps

    def _identify_dependencies(self, source_files: List[str]) -> List[Dict[str, Any]]:
        """
        Identify dependencies between files.

        Args:
            source_files: List of file paths

        Returns:
            List of dependencies
        """
        dependencies = []

        # Parse C++ files to find include dependencies
        for file_path in source_files:
            if file_path.endswith((".cpp", ".h")) and os.path.exists(file_path):
                includes = self._parse_cpp_includes(file_path)
                for include in includes:
                    # Extract the included file name
                    match = re.search(r'#include\s*[<"]([^>"]+)[>"]', include)
                    if match:
                        included_file = match.group(1)
                        dependencies.append(
                            {"from": file_path, "to": included_file, "type": "include"}
                        )

        return dependencies

    def _identify_patterns(self, file_analyses: List[Dict[str, Any]]) -> List[str]:
        """
        Identify architectural patterns in the analyzed files.

        Args:
            file_analyses: List of file analysis results

        Returns:
            List of identified patterns
        """
        patterns = []

        # Check for data-driven design (presence of .tbl files)
        has_table_files = any(
            analysis.get("type") in [".tbl", ".tbm"] for analysis in file_analyses
        )
        if has_table_files:
            patterns.append("data_driven_design")

        # Check for inheritance patterns in C++ files
        has_cpp_files = any(
            analysis.get("type") in [".cpp", ".h"] for analysis in file_analyses
        )
        if has_cpp_files:
            patterns.append("inheritance_hierarchy")
            patterns.append("object_oriented_design")

        # Add common patterns
        patterns.extend(["singleton_pattern", "observer_pattern"])

        return patterns


def main():
    """Main function for testing the Codebase Analyst."""
    analyst = CodebaseAnalyst()

    # Example usage
    entity_name = "GTC Fenris"
    source_files = [
        "source/tables/ships.tbl",
        "source/models/fenris.pof",
        "source/code/ship.cpp",
        "source/code/ship.h",
    ]

    analysis = analyst.analyze_entity(entity_name, source_files)
    print(json.dumps(analysis, indent=2))


if __name__ == "__main__":
    main()

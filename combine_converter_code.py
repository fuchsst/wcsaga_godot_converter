#!/usr/bin/env python3
"""
Helper script to combine all converter source code into a single well-formatted markdown file.
This creates a comprehensive documentation file with all source code organized by module.
"""

import os
import re
from datetime import datetime
from pathlib import Path


class CodeCombiner:
    def __init__(self, root_dir, output_file="converter_source_code.md"):
        self.root_dir = Path(root_dir)
        self.output_file = output_file
        self.allowed_extensions = {".py", ".yaml", ".yml", ".gd", ".tscn", ".sh", ".md"}
        self.ignore_dirs = {
            "__pycache__",
            ".git",
            ".pytest_cache",
            "node_modules",
            "venv",
            ".venv",
        }
        self.ignore_files = {"requirements.txt", "package.json", "package-lock.json"}

    def should_include_file(self, file_path):
        """Determine if a file should be included in the output."""
        if file_path.name in self.ignore_files:
            return False
        if file_path.suffix.lower() not in self.allowed_extensions:
            return False
        if any(ignored in str(file_path) for ignored in self.ignore_dirs):
            return False
        return True

    def get_file_info(self, file_path):
        """Get file information for markdown header."""
        relative_path = file_path.relative_to(self.root_dir.parent)
        file_size = file_path.stat().st_size
        modified_time = datetime.fromtimestamp(file_path.stat().st_mtime).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        return {
            "path": relative_path,
            "size": file_size,
            "modified": modified_time,
            "extension": file_path.suffix.lower(),
        }

    def format_code_block(self, content, file_extension):
        """Format code content as markdown code block."""
        language_map = {
            ".py": "python",
            ".yaml": "yaml",
            ".yml": "yaml",
            ".gd": "gdscript",
            ".tscn": "ini",
            ".sh": "bash",
            ".md": "markdown",
        }

        language = language_map.get(file_extension, "")
        return f"```{language}\n{content}\n```"

    def generate_toc(self, files):
        """Generate table of contents."""
        toc_lines = ["# Converter Source Code Documentation\n", ""]
        toc_lines.append("## Table of Contents\n")

        # Group files by directory
        groups = {}
        for file_path in files:
            relative_path = file_path.relative_to(self.root_dir.parent)
            dir_name = str(relative_path.parent)
            if dir_name not in groups:
                groups[dir_name] = []
            groups[dir_name].append(file_path)

        # Sort groups and files
        for dir_name in sorted(groups.keys()):
            toc_lines.append(f"### {dir_name}")
            for file_path in sorted(groups[dir_name]):
                relative_path = file_path.relative_to(self.root_dir.parent)
                anchor = str(relative_path).replace("/", "-").replace(".", "-").lower()
                toc_lines.append(f"- [{relative_path}](#{anchor})")
            toc_lines.append("")

        return "\n".join(toc_lines)

    def combine_files(self):
        """Main method to combine all files into markdown."""
        # Find all files
        all_files = []
        for root, dirs, files in os.walk(self.root_dir):
            # Filter out ignored directories
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]

            for file in files:
                file_path = Path(root) / file
                if self.should_include_file(file_path):
                    all_files.append(file_path)

        all_files.sort()

        # Generate content
        content_lines = []

        # Header
        content_lines.extend(
            [
                "# Converter Source Code Documentation\n",
                f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n",
                f"*Root directory: {self.root_dir}*\n",
                f"*Total files: {len(all_files)}*\n",
                "",
            ]
        )

        # Table of Contents
        content_lines.append(self.generate_toc(all_files))
        content_lines.append("---\n")

        # File contents
        for file_path in all_files:
            file_info = self.get_file_info(file_path)

            # File header
            content_lines.extend(
                [
                    f"## {file_info['path']}\n",
                    f"**File type:** {file_info['extension']}  \n",
                    f"**Size:** {file_info['size']} bytes  \n",
                    f"**Last modified:** {file_info['modified']}\n",
                    "",
                ]
            )

            # File content
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()

                # Format as code block
                formatted_content = self.format_code_block(
                    file_content, file_info["extension"]
                )
                content_lines.append(formatted_content)
                content_lines.append("")

            except Exception as e:
                content_lines.append(f"> Error reading file: {e}\n")

            content_lines.append("---\n")

        # Write to file
        output_content = "\n".join(content_lines)
        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write(output_content)

        return len(all_files)


def main():
    """Main execution function."""
    # Get converter directory
    script_dir = Path(__file__).parent
    converter_dir = script_dir / "converter"

    if not converter_dir.exists():
        print(f"Error: Converter directory not found at {converter_dir}")
        return

    # Create combiner and generate documentation
    combiner = CodeCombiner(converter_dir)
    file_count = combiner.combine_files()

    print(f"Successfully combined {file_count} files into {combiner.output_file}")
    print(f"Output file: {combiner.output_file}")


if __name__ == "__main__":
    main()

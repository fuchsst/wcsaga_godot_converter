"""
Tests for PromptEngineeringAgent

This module contains tests for the PromptEngineeringAgent component.
"""

import os
# Import the agent to test
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from prompt_engineering.prompt_engineering_agent import PromptEngineeringAgent


class TestPromptEngineeringAgent(unittest.TestCase):
    """Test cases for PromptEngineeringAgent."""

    def setUp(self):
        """Set up test fixtures."""
        self.agent = PromptEngineeringAgent()

    def test_initialization(self):
        """Test that the agent initializes correctly."""
        self.assertIsInstance(self.agent.template_library, dict)
        self.assertIn("QWEN_GENERATE_01", self.agent.template_library)
        self.assertIn("QWEN_REFACTOR_01", self.agent.template_library)
        self.assertIn("QWEN_BUGFIX_01", self.agent.template_library)
        self.assertIn("QWEN_TEST_GENERATE_01", self.agent.template_library)

    def test_generate_prompt_valid_template(self):
        """Test generating a prompt with a valid template."""
        prompt = self.agent.generate_prompt(
            "QWEN_GENERATE_01",
            target_file_path="test.gd",
            specification="Create a test class",
            context_code="# This is context",
        )

        self.assertIn("test.gd", prompt)
        self.assertIn("Create a test class", prompt)
        self.assertIn("# This is context", prompt)

    def test_generate_prompt_invalid_template(self):
        """Test generating a prompt with an invalid template."""
        with self.assertRaises(ValueError):
            self.agent.generate_prompt("INVALID_TEMPLATE", param="value")

    def test_create_generation_prompt(self):
        """Test creating a generation prompt."""
        prompt = self.agent.create_generation_prompt(
            target_file_path="scripts/player/ship.gd",
            specification="Create a PlayerShip class",
            context_code="# Player ship context",
        )

        self.assertIn("scripts/player/ship.gd", prompt)
        self.assertIn("Create a PlayerShip class", prompt)
        self.assertIn("# Player ship context", prompt)

    def test_create_refactoring_prompt(self):
        """Test creating a refactoring prompt."""
        prompt = self.agent.create_refactoring_prompt(
            file_path="scripts/enemy/ship.gd",
            task_description="Refactor to use state machine",
            constraints="Maintain existing API",
        )

        self.assertIn("scripts/enemy/ship.gd", prompt)
        self.assertIn("Refactor to use state machine", prompt)
        self.assertIn("Maintain existing API", prompt)

    def test_create_bugfix_prompt(self):
        """Test creating a bugfix prompt."""
        prompt = self.agent.create_bugfix_prompt(
            file_path="scripts/weapon/laser.gd",
            code_snippet="func fire():\n    pass",
            error_message="TypeError: Cannot call method 'fire' of null",
        )

        self.assertIn("scripts/weapon/laser.gd", prompt)
        self.assertIn("func fire():\n    pass", prompt)
        self.assertIn("TypeError: Cannot call method 'fire' of null", prompt)

    def test_create_test_generation_prompt(self):
        """Test creating a test generation prompt."""
        prompt = self.agent.create_test_generation_prompt(
            target_class="PlayerShip",
            target_file="scripts/player/ship.gd",
            class_content="class_name PlayerShip\nextends Node2D",
        )

        self.assertIn("PlayerShip", prompt)
        self.assertIn("scripts/player/ship.gd", prompt)
        self.assertIn("class_name PlayerShip\nextends Node2D", prompt)

    def test_refine_prompt_with_feedback(self):
        """Test refining a prompt with feedback."""
        original_prompt = "Original prompt content"
        error_message = "SyntaxError: Unexpected token"

        refined_prompt = self.agent.refine_prompt_with_feedback(
            original_prompt, error_message
        )

        self.assertIn(original_prompt, refined_prompt)
        self.assertIn(error_message, refined_prompt)
        self.assertIn("Please revise the prompt", refined_prompt)

    def test_add_context_to_prompt(self):
        """Test adding context to a prompt."""
        # Create temporary context files
        with (
            tempfile.NamedTemporaryFile(mode="w", suffix=".gd", delete=False) as f1,
            tempfile.NamedTemporaryFile(mode="w", suffix=".gd", delete=False) as f2,
        ):
            f1.write("# Context file 1\nconst VALUE1 = 1\n")
            f2.write("# Context file 2\nconst VALUE2 = 2\n")
            context_file_1 = f1.name
            context_file_2 = f2.name

        try:
            base_prompt = "Base prompt content"
            prompt_with_context = self.agent.add_context_to_prompt(
                base_prompt, [context_file_1, context_file_2]
            )

            self.assertIn(base_prompt, prompt_with_context)
            self.assertIn("const VALUE1 = 1", prompt_with_context)
            self.assertIn("const VALUE2 = 2", prompt_with_context)
            self.assertIn("<ADDITIONAL_CONTEXT>", prompt_with_context)
        finally:
            # Clean up temporary files
            os.unlink(context_file_1)
            os.unlink(context_file_2)

    def test_add_context_to_prompt_nonexistent_file(self):
        """Test adding context with a non-existent file."""
        base_prompt = "Base prompt content"
        prompt_with_context = self.agent.add_context_to_prompt(
            base_prompt, ["nonexistent_file.gd"]
        )

        # Should return the original prompt since file doesn't exist
        self.assertEqual(base_prompt, prompt_with_context)


if __name__ == "__main__":
    unittest.main()

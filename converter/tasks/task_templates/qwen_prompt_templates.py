def generate_qwen_generate_prompt(
    target_file_path: str, specification: str, context_code: str = ""
) -> str:
    """
    Generate a prompt for creating a new file with qwen-code.

    Args:
        target_file_path: Path to the target file to create
        specification: Detailed specification for the new file
        context_code: Optional context code to reference

    Returns:
        Formatted prompt string
    """
    prompt = f"""
You are an expert GDScript programmer. Your task is to generate a new script file based on the provided specification.
Your response must contain ONLY the complete GDScript code for the new file.
Do not include any explanatory text, markdown formatting, or conversational filler.

<TARGET_FILE_PATH>{target_file_path}</TARGET_FILE_PATH>
<SPECIFICATION>{specification}</SPECIFICATION>
"""

    if context_code:
        prompt += f"<CONTEXT_CODE>{context_code}</CONTEXT_CODE>"

    return prompt


def generate_qwen_refactor_prompt(
    file_path: str, task_description: str, constraints: str = ""
) -> str:
    """
    Generate a prompt for refactoring an existing function with qwen-code.

    Args:
        file_path: Path to the file to refactor
        task_description: Description of the refactoring task
        constraints: Additional constraints for the task

    Returns:
        Formatted prompt string
    """
    prompt = f"""
You are an expert GDScript programmer. Your task is to perform a specific refactoring on an existing file.
Do not propose a plan; implement the change directly. Do not modify any other files.

<FILE_PATH>{file_path}</FILE_PATH>
<TASK_DESCRIPTION>{task_description}</TASK_DESCRIPTION>
<CONSTRAINTS>{constraints}</CONSTRAINTS>
"""
    return prompt


def generate_qwen_bugfix_prompt(
    file_path: str, code_snippet: str, error_message: str
) -> str:
    """
    Generate a prompt for fixing a bug with qwen-code.

    Args:
        file_path: Path to the file with the bug
        code_snippet: Code snippet with the bug
        error_message: Error message describing the bug

    Returns:
        Formatted prompt string
    """
    prompt = f"""
You are an expert debugger. A bug has been identified in the following file.
Your task is to fix it. Analyze the provided error message and code, identify the root cause, and apply the necessary correction.
Implement the fix directly.

<FILE_PATH>{file_path}</FILE_PATH>
<CODE_SNIPPET>{code_snippet}</CODE_SNIPPET>
<ERROR_MESSAGE>{error_message}</ERROR_MESSAGE>
"""
    return prompt


def generate_qwen_test_prompt(
    target_class: str, target_file: str, class_content: str
) -> str:
    """
    Generate a prompt for creating unit tests with qwen-code.

    Args:
        target_class: Name of the class to test
        target_file: Path to the file containing the class
        class_content: Content of the class to test

    Returns:
        Formatted prompt string
    """
    prompt = f"""
You are an expert QA engineer. Your task is to generate unit tests for the provided GDScript class.
Create comprehensive tests that cover all public methods and edge cases.
Use the gdUnit4 framework for test implementation.

<TARGET_CLASS>{target_class}</TARGET_CLASS>
<TARGET_FILE>{target_file}</TARGET_FILE>
<CLASS_CONTENT>{class_content}</CLASS_CONTENT>
<TEST_FRAMEWORK>gdUnit4</TEST_FRAMEWORK>
"""
    return prompt


def generate_qwen_optimize_prompt(
    file_path: str, optimization_goal: str, performance_metrics: str = ""
) -> str:
    """
    Generate a prompt for optimizing code with qwen-code.

    Args:
        file_path: Path to the file to optimize
        optimization_goal: Description of the optimization goal
        performance_metrics: Current performance metrics (if available)

    Returns:
        Formatted prompt string
    """
    prompt = f"""
You are an expert performance optimizer. Your task is to optimize the provided GDScript code.
Focus on the specific optimization goal while maintaining all existing functionality.

<FILE_PATH>{file_path}</FILE_PATH>
<OPTIMIZATION_GOAL>{optimization_goal}</OPTIMIZATION_GOAL>
"""

    if performance_metrics:
        prompt += f"<PERFORMANCE_METRICS>{performance_metrics}</PERFORMANCE_METRICS>"

    return prompt


def generate_qwen_document_prompt(file_path: str, class_content: str) -> str:
    """
    Generate a prompt for adding documentation to code with qwen-code.

    Args:
        file_path: Path to the file to document
        class_content: Content of the class to document

    Returns:
        Formatted prompt string
    """
    prompt = f"""
You are an expert technical writer. Your task is to add comprehensive documentation to the provided GDScript code.
Add docstrings to all public classes and methods, and inline comments for complex logic.
Follow the documentation standards in STYLE_GUIDE.md.

<FILE_PATH>{file_path}</FILE_PATH>
<CLASS_CONTENT>{class_content}</CLASS_CONTENT>
<DOCUMENTATION_STANDARDS>Follow Godot GDScript documentation standards</DOCUMENTATION_STANDARDS>
"""
    return prompt

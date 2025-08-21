def generate_qwen_generate_prompt(target_file_path: str, specification: str, context_code: str = "") -> str:
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

def generate_qwen_refactor_prompt(file_path: str, task_description: str, constraints: str = "") -> str:
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

def generate_qwen_bugfix_prompt(file_path: str, code_snippet: str, error_message: str) -> str:
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
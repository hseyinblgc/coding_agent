import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a specific Python file (.py) within the permitted working directory and returns its standard output (STDOUT) and standard error (STDERR). Use this to run scripts, tests, or automation tasks.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the Python file to execute, relative to the working directory (e.g., 'scripts/process_data.py').",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of command-line arguments to pass to the Python script (e.g., ['--verbose', 'input.csv']).",
                },
            },
            "required": ["file_path"],
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    command = ["python", target_file]
    if args:
        command.extend(args)

    # Will be True or False
    valid_target_dir = (
        os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    )
    if not valid_target_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    try:
        process: subprocess.CompletedProcess = subprocess.run(
            command, capture_output=True, text=True, timeout=30, check=True
        )
        if process.stdout and process.stderr is None:
            return "No output produced"

        return f"STDOUT: {process.stdout}\nSTDERR: {process.stderr}"
    except subprocess.CalledProcessError as cpe:
        return f"Process exited with code {cpe.returncode}"
    except Exception as e:
        return f"Error: executing Python file: {e}"

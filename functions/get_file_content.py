import os
from config import MAX_CHARS


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads and returns the content of a specific file within the permitted working directory. It limits the output length to avoid token overflow.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to be read, relative to the working directory (e.g., 'src/main.py' or 'config.json').",
                },
            },
            "required": ["file_path"],
        },
    },
}

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes or overwrites content to a specified file within the permitted working directory. It automatically creates parent directories if they do not exist.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The relative path where the file should be saved (e.g., 'notes/todo.txt').",
                },
                "content": {
                    "type": "string",
                    "description": "The full text content to be written into the file.",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}


def get_file_content(working_directory: str, file_path: str) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    try:
        # Will be True or False
        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )

        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            with open(target_file, "r") as f:
                file_content_string = f.read(MAX_CHARS)
            return file_content_string
    except Exception as e:
        return f"Error: {e}"


def write_file(working_directory: str, file_path: str, content: str) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

    # Will be True or False
    valid_target_dir = (
        os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    )
    if not valid_target_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    elif os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    try:
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: {e}"

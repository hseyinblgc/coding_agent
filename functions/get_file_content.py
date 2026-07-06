import os
from config import MAX_CHARS


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

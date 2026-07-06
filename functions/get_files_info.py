import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        # Will be True or False
        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )

        def formatter(x):
            return f"  - {x}: file_size={os.path.getsize(os.path.join(target_dir, x))}, is_dir={os.path.isdir(os.path.join(target_dir, x))}"

        print(f"Result for '{directory}' directory:")
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        else:
            return "\n".join(map(formatter, os.listdir(target_dir)))
    except Exception as e:
        return f"Error: {e}"

import os


def get_files_info(working_directory, directory="."):
    try:
        dir_path = os.path.abspath(working_directory)
        response_lines = []

        if directory == ".":
            response_lines.append("Result for current directory:")
        else:
            dir_path = os.path.join(dir_path, directory)
            if "../" in directory or not dir_path.startswith(
                os.path.abspath(working_directory)
            ):
                return f"Result for '{directory}' directory:\n    Error: Cannot list \"{directory}\" as it is outside the permitted working directory"
            if not os.path.isdir(dir_path):
                return f"Result for '{directory}' directory:\n    Error: \"{directory}\" is not a directory"
            response_lines.append(f"Result for '{directory}' directory:")

        for item_name in os.listdir(dir_path):
            if item_name.startswith("__"):
                continue

            item_path = os.path.join(dir_path, item_name)
            if os.path.exists(item_path):
                response_lines.append(
                    f" - {item_name}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}"
                )

        return "\n".join(response_lines)

    except Exception as e:
        return f"Error: {e}"

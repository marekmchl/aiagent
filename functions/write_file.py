import os


def write_file(working_directory, file_path, content):
    try:
        full_path = os.path.join(os.path.abspath(working_directory), file_path)
        if "../" in file_path or not full_path.startswith(
            os.path.abspath(working_directory)
        ):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(os.path.dirname(full_path)):
            os.makedirs(os.path.dirname(full_path))

        if os.path.exists(full_path):
            os.remove(full_path)

        with open(full_path, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: {e}"

import os

from config import FILE_READ_CHARACTER_LIMIT


def get_file_content(working_directory, file_path):
    try:
        contents_path = os.path.abspath(working_directory)
        response_lines = []

        contents_path = os.path.join(contents_path, file_path)
        if "../" in file_path or not contents_path.startswith(
            os.path.abspath(working_directory)
        ):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(contents_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        response_lines.append(f"Result for '{file_path}' directory:")

        with open(contents_path, "r") as f:
            file_content_string = f.read(FILE_READ_CHARACTER_LIMIT)

        if len(file_content_string) >= FILE_READ_CHARACTER_LIMIT:
            file_content_string += (
                f'[...File "{file_path}" truncated at 10000 characters]'
            )
        return file_content_string

    except Exception as e:
        return f"Error: {e}"

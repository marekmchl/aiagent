import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    try:
        full_path = os.path.join(os.path.abspath(working_directory), file_path)
        if "../" in file_path or not full_path.startswith(
            os.path.abspath(working_directory)
        ):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(full_path):
            return f'Error: File "{file_path}" not found.'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        completed_process = subprocess.run(
            ["python", file_path] + args,
            capture_output=True,
            cwd=os.path.abspath(working_directory),
            timeout=30,
        )
        if completed_process.returncode != 0:
            return f"STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr} \nProcess exited with code {completed_process.returncode}"
        else:
            return f"STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}"

    except Exception as e:
        return f"Error: executing Python file: {e}"

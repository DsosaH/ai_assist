import os
import subprocess
import sys
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs specified .py file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path relative to working directory",
            ),
        },
    ),
)
def run_python_file(working_directory, file_path, args=[]):
    try:
        absolute_working_directory = os.path.abspath(working_directory)
        absolute_path_file = os.path.abspath(os.path.join(working_directory, file_path))
        is_inside = (absolute_path_file == absolute_working_directory) or (absolute_path_file.startswith(absolute_working_directory + os.sep))
        if not is_inside:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(absolute_path_file):
            return f'Error: File "{file_path}" not found.'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        output = subprocess.run([sys.executable, absolute_path_file, *args], capture_output=True, timeout=30, cwd=absolute_working_directory)
        stdout = output.stdout.decode().strip()
        stderr = output.stderr.decode().strip()
        output_message = f'STDOUT: {stdout} STDERR: {stderr}'
        if not stdout and not stderr:
            return "No output produced."
        if output.returncode != 0:
            output_message+= " Process exited with code X"
        return output_message

    except Exception as e:
        return f"Error: executing Python file: {e}"
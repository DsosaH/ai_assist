import os
from google import genai
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
def get_files_info(working_directory, directory="."):
    try:
        final_path = os.path.join(working_directory, directory)
        absolute_working_directory = os.path.abspath(working_directory)
        absolute_final_path = os.path.abspath(final_path)
        if not os.path.isdir(final_path):
            response = f'Error: "{directory}" is not a directory'
            return response
        if not absolute_final_path.startswith(absolute_working_directory):
            response = f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
            return response
        directory_list = os.listdir(final_path)
        result_list = []
        for item in directory_list:
            result_list.append(f" - {item}: file_size={os.path.getsize(os.path.join(absolute_final_path, item))} bytes, is_dir={os.path.isdir(os.path.join(absolute_final_path, item))}")
        final_string = "\n".join(result_list)
        return final_string
    except Exception as e:
        return f"Error: {e}"
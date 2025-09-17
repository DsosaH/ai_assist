import os
from config import MAX_CHARACTER_LIMIT
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns content of specified file up to 10,000 characters, constrained to the working directory.",
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
def get_file_content(working_directory, file_path):
    try:
        absolute_working_directory = os.path.abspath(working_directory)
        absolute_path_file = os.path.abspath(os.path.join(working_directory, file_path))
        is_inside = (absolute_path_file == absolute_working_directory) or (absolute_path_file.startswith(absolute_working_directory + os.sep))

        if not is_inside:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(absolute_path_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(absolute_path_file, "r", encoding="utf-8") as text:
            content = text.read(MAX_CHARACTER_LIMIT + 1)
            if len(content) > MAX_CHARACTER_LIMIT:
                return content[:MAX_CHARACTER_LIMIT] + f'[...File "{file_path}" truncated at 10000 characters]'
            return content
        
    except Exception as e:
        return f"Error: {e}"
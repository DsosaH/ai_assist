import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites content on specified file or creates a new one if it doesn't exist, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path relative to working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text to write"
            )
        },
        required=["file_path", "content"]
    ),
    
)
def write_file(working_directory, file_path, content):
    try:
        absolute_working_directory = os.path.abspath(working_directory)
        absolute_path_file = os.path.abspath(os.path.join(working_directory, file_path))
        is_inside = (absolute_path_file == absolute_working_directory) or (absolute_path_file.startswith(absolute_working_directory + os.sep))
        if not is_inside:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(os.path.dirname(absolute_path_file)):
            os.makedirs(os.path.dirname(absolute_path_file))

        with open(absolute_path_file, "w") as text:
            text.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: {e}"
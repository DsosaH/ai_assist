from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file
working_directory = "./calculator"
functions = {"get_files_info": get_files_info,
                 "get_file_content": get_file_content,
                 "run_python_file": run_python_file,
                 "write_file": write_file}

def call_function(function_call_part, verbose=False):
    if function_call_part.name not in functions:
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"error": f"Unknown function: {function_call_part.name}"},
        )
    ],
)
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    args = {**function_call_part.args, "working_directory": working_directory}
    result = functions[function_call_part.name](**args)
    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"result": result},
        )
    ],
)

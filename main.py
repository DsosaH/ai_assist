import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
available_functions = types.Tool(function_declarations=[schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file])

def main():
    args = sys.argv[1:]
    if not args:
        print("ERROR: No input detected.")
        sys.exit(1)
    else:
        is_verbose = False
        if args[-1] == "--verbose":
            del(args[-1])
            is_verbose = True
        usr_input = " ".join(args)
        messages = [types.Content(role="user", parts=[types.Part(text=usr_input)]),]
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
        if response.function_calls:
            for func in response.function_calls:
                result = call_function(func, is_verbose)
                if not result.parts[0].function_response.response:
                    raise Exception("Fatal Exception of some sort.")
                elif (result.parts[0].function_response.response) and (is_verbose):
                    print(f"-> {result.parts[0].function_response.response}")
        else:        
            print(response.text)

        if is_verbose:
            print(f"User prompt: {usr_input}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
if __name__ == "__main__":
    main()

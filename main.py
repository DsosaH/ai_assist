import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys


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
        response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)
        print(response.text)
        if is_verbose:
            print(f"User prompt: {usr_input}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
if __name__ == "__main__":
    main()

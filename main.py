import os
from dotenv import load_dotenv
from google import genai
import sys


def main():
    usr_input = sys.argv
    if len(usr_input) <= 1:
        print("ERROR: No input detected.")
        sys.exit(1)
    else:
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(model="gemini-2.0-flash-001", contents=usr_input[1])
        print(response.text)
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
if __name__ == "__main__":
    main()

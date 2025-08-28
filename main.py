import os
import sys
from dotenv import load_dotenv
from google.genai import types
from functions.get_file_info import schema_get_files_info
load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

from google import genai

client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
def main():
    if len(sys.argv) < 2:
        print("PROVIDE A PROMPT!")
        sys.exit(1)

    user_prompt = sys.argv[1]

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents= messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )

    if response.function_calls:
        for function_call_part in response.function_calls:
            print(f"Calling function: {function_call_part.name}{function_call_part.args}")
    else:
        print(response.text)
    if "--verbose" in sys.argv[2:]:
        prompt_token_count = response.usage_metadata.prompt_token_count
        candidates_token_count = response.usage_metadata.candidates_token_count
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_token_count}")
        print(f"Response tokens: {candidates_token_count}")

if __name__ == "__main__":
    main()

import os
import sys
from dotenv import load_dotenv
from google.genai import types
from schemas import available_functions
from google import genai
from function_caller import call_function

from system_prompt import system_prompt


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if len(args) < 1:
        print("USAGE: python3 main.py \"INSERT PROMPT HERE\" [--verbose]" )
        print("Example: python3 main.py \"make me a basic rock paper scissors program\"")
        sys.exit(1)

    user_prompt = sys.argv[1]

    if verbose:
        print(f"User prompt: {user_prompt}")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_ai_response(client, messages, verbose)

def generate_ai_response(client, message, verbose):

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents= message,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )

    if verbose:
        prompt_token_count = response.usage_metadata.prompt_token_count
        candidates_token_count = response.usage_metadata.candidates_token_count
        print(f"Prompt tokens: {prompt_token_count}")
        print(f"Response tokens: {candidates_token_count}")

    if response.function_calls:
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part=function_call_part, verbose = verbose)
            try:
                function_result = function_call_result.parts[0].function_response.response
                if verbose:
                    print(f"-> {function_result}")
            except:
                raise Exception("FATAL ERROR: NO FUNCTION")
    else:
        print(response.text)
        return response.text


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}")

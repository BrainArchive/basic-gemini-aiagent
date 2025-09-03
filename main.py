import os
import sys
from dotenv import load_dotenv
from google.genai import types
from schemas import available_functions
from google import genai
from function_caller import call_function
import json
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
    for i in range(20):
        response = generate_ai_response(client, messages, verbose)
        if type(response) == str:
            print(response)
            break
    

def generate_ai_response(client, messages, verbose):

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents= messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )
    print("RESPONSE GENERATED")
    for candidate in response.candidates:
        messages.append(candidate.content)

    if verbose:
        prompt_token_count = response.usage_metadata.prompt_token_count
        candidates_token_count = response.usage_metadata.candidates_token_count
        print(f"Prompt tokens: {prompt_token_count}")
        print(f"Response tokens: {candidates_token_count}")

    if response.function_calls:
        for function_call_part in response.function_calls:
            result , function_name = call_function(function_call_part=function_call_part, verbose = verbose)
            messages.append(types.Content(
                role="user",
                parts=[types.Part(text=json.dumps({"name": function_name, "result": result}))],
                )
            )
            try:
                print(messages)
                if verbose:
                    print(f"-> {result}")
            except Exception as e:
                raise Exception(e)
    else:
        print(response.text)
        return response.text


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}")

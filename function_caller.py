
from functions.get_files_info import get_files_info 
from functions.get_file_content import get_file_content 
from functions.write_file import write_file
from functions.run_python_file import run_python_file 
from google.genai import types

WORKING_DIRECTORY = "./calculator"

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")


    FUNCTION_DICTIONARY = {
        "get_files_info":get_files_info,
        "get_file_content":get_file_content,
        "write_file":write_file,
        "run_python_file":run_python_file,
    }

    function_name = function_call_part.name
    if not function_name in FUNCTION_DICTIONARY:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    else:
        function_result = FUNCTION_DICTIONARY[function_name](WORKING_DIRECTORY,**function_call_part.args)
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
        )



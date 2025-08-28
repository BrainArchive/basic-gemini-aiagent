import os
from google.genai import types

def write_file(working_directory, filepath, content): 
    true_path = os.path.join(working_directory,filepath)
    true_path = os.path.abspath(true_path)
    if not true_path.startswith(os.path.abspath(working_directory)):
        return f"Error: Cannot read {filepath} as it is outside working directory"
    print(os.path.dirname(true_path))
    if not os.path.exists(os.path.dirname(true_path)):
        return f"Error: directory {os.path.dirname(true_path)} does not exist"
    with open(true_path, "w") as f:
        f.write(content)
    return f"Successfully wrote to \"{filepath}\" ({len(content)} characters written)"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="writes contents in the specificied filepath, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "filepath": types.Schema(
                type=types.Type.STRING,
                description="the file to be written or overwritten on, relative to the working directory. Must be provided.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="the content to be written on the specified filepath. Will overwrite any existing content in the specified file"
            ),
        },
        required=["filepath","content"]
    ),
)

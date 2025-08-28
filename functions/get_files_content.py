import os
from google.genai import types

def get_files_content(working_directory, filepath):
    true_path = os.path.join(working_directory,filepath)
    true_path = os.path.abspath(true_path)
    if not true_path.startswith(os.path.abspath(working_directory)):
        return f"Error: Cannot read {filepath} as it is outside working directory"
    if not os.path.isfile(true_path):
        return f"Error: File not found or is not a regular file: {filepath}"

    MAX_CHARS = 10000
    with open(true_path, "r") as f:
        file_content_string = f.read(MAX_CHARS)
        if len(file_content_string) == 10000:
            file_content_string += f"[...File \"{filepath}\" truncated at 10000 characters]"
    return file_content_string


schema_get_files_content= types.FunctionDeclaration(
    name="get_files_content",
    description="reads contents of the file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "filepath": types.Schema(
                type=types.Type.STRING,
                description="The directory of the file to be read, relative to the working directory. Must be provided.",
            ),
        },
    ),
)

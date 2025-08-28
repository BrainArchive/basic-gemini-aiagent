import os
import subprocess
from google.genai import types

def run_python_file(working_directory, filepath, args=[]):
    true_path = os.path.join(working_directory,filepath)
    true_path = os.path.abspath(true_path)
    if not true_path.startswith(os.path.abspath(working_directory)):
        return f"Error: Cannot execute \"{filepath}\" as it is outside working directory"
    if not os.path.exists(true_path):
        return f"Error: File \"{filepath}\" not found"
    if not true_path.endswith(".py"):
        return f"Error: \"{filepath}\" is not a python file"
    python_command = ["python3", true_path]
    for arguments in args:
        python_command.append(arguments)
    try:
        completed_process = subprocess.run(python_command, capture_output=True, timeout=30,)
    except Exception as e:
        return f"Error: executing Python file {e}"
    stdout = completed_process.stdout.decode()
    stderr = completed_process.stderr.decode()

    if stdout == "" and stderr == "":
        return "No output produced"
    else:
        final_string = f"STDOUT: {stdout} STDERR: {stderr}"

    if completed_process.returncode != 0:
        final_string += f" Process exited with code {completed_process.returncode}"

    return final_string




schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="runs python file in the specificied filepath, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "filepath": types.Schema(
                type=types.Type.STRING,
                description="the python file to be executed, relative to the working directory. Must be provided.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items =types.Schema(
                    type = types.Type.STRING
                ),
                description="list of string arguments to be used for the given python file. will run the python file with arguments if empty."
            ),
        },
        required=["filepath"]
    ),
)


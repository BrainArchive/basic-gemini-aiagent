import os

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

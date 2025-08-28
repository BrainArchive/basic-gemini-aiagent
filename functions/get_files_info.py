import os
import os.path
from google.genai import types

def get_files_info(working_directory, directory="."):
    true_path = os.path.join(working_directory, directory)
    true_path = os.path.abspath(true_path)
    if not os.path.abspath(true_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(true_path):
        return f"Error:{directory} is not a directory"
    list_of_items = []
    try:
        list_files = os.listdir(true_path)
    except OSError:
        return f"Error: permission not granted to list items in directory"
    for items in list_files:
        list_of_items.append(items)
    file_info = []
    for files in list_of_items:
        new_list = []
        file_name = files
        try:
            filepath = os.path.join(true_path,file_name)
            filesize = os.path.getsize(filepath)
            file_is_dir = os.path.isdir(filepath)
        except Exception as e:
            return f"Error:{e}"
        new_list.append(file_name)
        new_list.append(filesize)
        new_list.append(file_is_dir)
        file_info.append(new_list)
    for files in file_info:
        print(f"{files[0]}: file_size={files[1]} bytes, is_dir={files[2]}")
    return file_info

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

if __name__ == "__main__":
    print(get_files_info("testdir"))
    print(get_files_info(".", "testdir/../../"))


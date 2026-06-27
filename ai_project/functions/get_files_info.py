import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    path = os.path.abspath(working_directory)
    target = os.path.normpath(os.path.join(path,directory))
    # Will be True or False
    valid_target_dir = os.path.commonpath([path, target]) == path
    if not os.path.isdir(target):
        return f'Error: "{directory}" is not a directory'
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    else:
        l = []
        for item in os.listdir(target):
            l.append(f"- {item}: file_size={os.path.getsize(os.path.join(target,item))}, is_dir={os.path.isdir(os.path.join(target,item))}")
        return "\n".join(l)
    

from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
import os

def get_file_content(working_directory: str, file_path: str) -> str:
    path = os.path.abspath(working_directory)
    target = os.path.normpath(os.path.join(path,file_path))

    is_inside = os.path.commonpath([path,target]) == path

    if not os.path.isfile(target):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    if not is_inside:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    content = ""
    with open(target) as file:
        content = file.read(2000)
        # After reading the first MAX_CHARS...
        if file.read(1):
            content += f'[...File "{file_path}" truncated at {1000} characters]'
    return content

from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="By this function you get the content of nay file and you can read it.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to see the content of files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
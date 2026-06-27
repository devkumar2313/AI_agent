import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
        path = os.path.abspath(working_directory)
        target = os.path.normpath(os.path.join(path,file_path))

        is_inside = os.path.commonpath([path,target]) == path

        if os.path.isdir(target):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
    
        if not is_inside:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        os.makedirs(os.path.dirname(target), exist_ok=True)

        with open(target,"w") as file:
             file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="By this function you can write the wanted content in any file you want.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path","content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to see the content of files from, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that the user want to write in the file.",
            ),
        },
    ),
)
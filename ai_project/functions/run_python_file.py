import os
import subprocess
def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
        
    
    try:
        path = os.path.abspath(working_directory)
        target = os.path.normpath(os.path.join(path,file_path))

        is_inside = os.path.commonpath([path,target]) == path

        if not os.path.isfile(target):
            return f'Error: "{file_path}" does not exist or is not a regular file'
    
        if not is_inside:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not file_path.endswith('.py'):
             return f'Error: "{file_path}" is not a Python file'
        if args is None:
            args = []
        command = ["python", target]
        command.extend(list(args))
        com_pro = subprocess.run(command,cwd = working_directory,capture_output=True,text=True,timeout=30)
        if com_pro.returncode !=0:
             print(f"Process exited with code {com_pro.returncode}")
        if len(com_pro.stdout)==0 and len(com_pro.stderr)==0:
             print("No output produced")
        return f"STDOUT:{com_pro.stdout} STDERR:{com_pro.stderr}"
    except Exception as e:
        print(f"Error: executing Python file: {e}")
             

from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="By this function you can run any python file you want and it executed smoothly.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to see the content of files from, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                type=types.Type.STRING,
                ),
                description="It stores extra command or extra string that was given when running a function.",
            ),
        },
    ),
)
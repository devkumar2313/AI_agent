from google.genai import types
from collections.abc import Callable
from .get_file_content import get_file_content
from .get_files_info import get_files_info
from .run_python_file import run_python_file
from .write_file import write_file

function_map: dict[str, Callable[..., str]] = {
    
    "get_files_info": get_files_info,
    "run_python_file":run_python_file,
    "write_file":write_file,
    "get_file_content": get_file_content,
}


def call_function(
    function_call: types.FunctionCall, verbose: bool = False
) -> types.Content:
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
    function_name = function_call.name or ""

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
            )
        ],
    )

    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = "./calculator"
    function_result = function_map[function_name](**args)
    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
        )
    ],
)

    
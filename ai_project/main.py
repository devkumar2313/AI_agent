import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function1 import available_functions
from functions.call_function import call_function
import sys


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages: list[types.Content] = [
    types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]
    for _ in range(20):
        # Now we can access `args.user_prompt`
        response = client.models.generate_content(
        model='gemini-2.5-flash', contents=messages,config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        tools=[available_functions],
        temperature=0
        ),
        )
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if response.candidates:
             messages.append(response.candidates[0].content)

        function_result = []
        if response.function_calls:
            for function_call in response.function_calls:
                print(f"Calling function: {function_call.name}({function_call.args})")
                function_call_result = call_function(function_call)
                if len(function_call_result.parts) == 0:
                    raise Exception("it does not has parts")
                if function_call_result.parts[0].function_response is None:
                    raise Exception("The response object is None")
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception("The response is None")
                function_result.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                messages.append(types.Content(role="user", parts=function_result))
        else:
            print(response.text)
            break
    else:
        print(f"\nError: Maximum iterations ({20}) reached. The model failed to produce a final text response.")
        sys.exit(1)
    


if __name__ == "__main__":
    main()

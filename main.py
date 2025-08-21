import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import call_function


def get_available_funcions():
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
    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Read the contents of a specified file, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the file to read the contents of, relative to the working directory. If not provided, returns an error.",
                ),
            },
        ),
    )
    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes the given content to file specified by file_path, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the file to write the contents into, relative to the working directory. If not provided, returns an error.",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The contents to be written into the specified file. If not provided, the resulting file will be empty.",
                ),
            },
        ),
    )
    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Runs the file specified by the file_path in a Python interpreter giving this new process the args as arguments, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the Python file containing the code to run, relative to the working directory. If not provided, returns an error.",
                ),
                "args": types.Schema(
                    type=types.Type.STRING,
                    description="A set of arguments to be provided to the code wich is being executed.",
                ),
            },
        ),
    )
    return types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    user_prompt = sys.argv[1] if len(sys.argv) >= 2 else sys.exit(1)
    verbose = True if (len(sys.argv) >= 3 and sys.argv[2] == "--verbose") else False
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
    available_funcions = get_available_funcions()

    res = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_funcions], system_instruction=system_prompt
        ),
    )

    if res is not None:
        if res.usage_metadata is not None and verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {res.usage_metadata.candidates_token_count}")
        if res.function_calls is not None:
            for function_call in res.function_calls:
                function_call_result = call_function(function_call, verbose)
                if (
                    function_call_result is not None
                    and function_call_result.parts is not None
                    and function_call_result.parts[0].function_response is not None
                    and function_call_result.parts[0].function_response.response
                    is not None
                ):
                    if verbose:
                        print(
                            f"-> {function_call_result.parts[0].function_response.response}"
                        )
                else:
                    raise Exception("FATAL ERROR")
        elif res.text is not None:
            print(res.text)


if __name__ == "__main__":
    main()

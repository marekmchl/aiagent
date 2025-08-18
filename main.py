import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    user_prompt = sys.argv[1] if len(sys.argv) >= 2 else sys.exit(1)
    verbose = True if (len(sys.argv) >= 3 and sys.argv[2] == "--verbose") else False
    system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    res = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )
    if res is not None:
        if res.usage_metadata is not None and verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {res.usage_metadata.candidates_token_count}")
        print(res.text)


if __name__ == "__main__":
    main()

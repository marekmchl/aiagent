import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    if len(sys.argv) < 2:
        sys.exit(1)
    verbose = False
    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        verbose = True
    messages = [
        types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
    ]
    res = client.models.generate_content(
        model="gemini-2.0-flash-001", contents=messages
    )
    if res is not None:
        if res.usage_metadata is not None and verbose:
            print(f"User prompt: {sys.argv[1]}")
            print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {res.usage_metadata.candidates_token_count}")
        print(res.text)


if __name__ == "__main__":
    main()

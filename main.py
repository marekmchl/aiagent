import os
import sys
from dotenv import load_dotenv
from google import genai


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    if len(sys.argv) < 2:
        sys.exit(1)
    else:
        res = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=sys.argv[1],
        )
    if res is not None:
        if res.usage_metadata is not None:
            print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {res.usage_metadata.candidates_token_count}")
        print(res.text)


if __name__ == "__main__":
    main()

import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletion

from prompts import system_prompt

load_dotenv()
api_key: str | None = os.environ.get("OPENROUTER_API_KEY")
if api_key is None:
    raise RuntimeError("Error: You need to set OPENROUTER_API_KEY in your .env ")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
# Now we can access `args.user_prompt`

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

messages: list[dict[str, str]] = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]
response: ChatCompletion = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
    temperature=0,
)


def formatter(obj: ChatCompletion, userprompt: str, verbose: bool) -> str:
    if obj.usage is None:
        raise RuntimeError("usage property is None.")
    if verbose:
        return f"""
        User prompt: {userprompt}
        Prompt tokens: {obj.usage.prompt_tokens}
        Response tokens: {obj.usage.completion_tokens}
        Response:
        {obj.choices[0].message.content}"""
    return f"Response:\n{obj.choices[0].message.content}"


def main():
    print(formatter(response, args.user_prompt, args.verbose))


if __name__ == "__main__":
    main()

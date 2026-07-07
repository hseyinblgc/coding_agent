import argparse
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletion

from call_function import available_functions, call_function
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


def formatter(response: ChatCompletion, userprompt: str, verbose: bool) -> str:
    message = response.choices[0].message
    if response.usage is None:
        raise RuntimeError("usage property is None.")

    if verbose:
        return f"""
        User prompt: {userprompt}
        Prompt tokens: {response.usage.prompt_tokens}
        Response tokens: {response.usage.completion_tokens}
        Response:
        {message.content}"""
    return f"Response:\n{message.content}"


def main():
    for _ in range(20):
        response: ChatCompletion = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
            temperature=0,
        )
        message = response.choices[0].message
        messages.append(message)
        if message.tool_calls:
            for tool_call in message.tool_calls:
                # function_args = json.loads(tool_call.function.arguments or "{}")
                result_message = call_function(tool_call, verbose=args.verbose)
                if not result_message.get("content"):
                    raise ValueError("Tool message content cannot be empty.")

                messages.append(result_message)
        else:
            break

    if response and response.choices[0].message.tool_calls:
            print("maximum number of iterations is reached and the model still hasn't produced a final response")
            sys.exit(1)

    print(formatter(response, args.user_prompt, args.verbose))


if __name__ == "__main__":
    main()

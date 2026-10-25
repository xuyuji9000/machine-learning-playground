"""Client-side get_weather for the local mlx_lm server.

The model only returns a tool call. This script runs the function and
sends the result back as a role=tool message.
"""

import json
import urllib.request

MODEL = "mlx-community/Qwen3.5-9B-4bit"
URL = "http://localhost:1234/v1/chat/completions"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name, for example Tokyo",
                    }
                },
                "required": ["city"],
            },
        },
    }
]


def get_weather(city: str) -> str:
    # Stand-in until a real weather API is wired in.
    table = {
        "tokyo": "Tokyo: 18°C, clear",
        "london": "London: 12°C, rain",
        "new york": "New York: 16°C, cloudy",
    }
    return table.get(city.strip().lower(), f"{city}: 20°C, clear")


def chat(messages: list) -> dict:
    body = json.dumps(
        {"model": MODEL, "messages": messages, "tools": TOOLS}
    ).encode()
    request = urllib.request.Request(
        URL, data=body, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(request) as response:
        return json.load(response)


def run(question: str) -> str:
    messages = [{"role": "user", "content": question}]
    for _ in range(4):
        message = chat(messages)["choices"][0]["message"]
        messages.append(message)
        tool_calls = message.get("tool_calls") or []
        if not tool_calls:
            return message.get("content") or ""
        for call in tool_calls:
            name = call["function"]["name"]
            args = json.loads(call["function"]["arguments"] or "{}")
            if name != "get_weather":
                result = f"unknown tool: {name}"
            else:
                result = get_weather(**args)
            print(f"{name}({args}) -> {result}")
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call["id"],
                    "content": result,
                }
            )
    raise RuntimeError("model kept calling tools")


if __name__ == "__main__":
    print(run("What is the weather in Tokyo right now?"))

This folder contains example of getting examples with `phi3` models.

- `ollama pull phi3:3.8b`
- `ollama pull phi3:14b`

# Commands

``` shell
    # Query with OpenAI compatible query
    curl http://localhost:11434/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "phi3:3.8b",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Hello!"
            }
        ]
    }' | jq
```
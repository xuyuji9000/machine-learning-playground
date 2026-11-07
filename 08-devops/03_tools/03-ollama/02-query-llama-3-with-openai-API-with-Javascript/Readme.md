# Commands
1. Get Started

    ``` shell
    # 1.1 Start ollama
    ollama serve

    ```
    > [llama3](https://ollama.com/library/llama3)

    ``` shell
    # 1.2 Query with OpenAI compatible query
    curl http://localhost:11434/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "llama3",
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

# Reference

- [OpenAI compatibility](https://github.com/ollama/ollama/blob/main/docs/openai.md)
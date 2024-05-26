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

2. Setup Python environment

    ``` shell
    # Install pipx for environment isolation
    brew install --verbose pipx

    # Install virtualenv command with pipx
    pipx install virtualenv
    pipx ensurepath
    pipx list

    # setup python virtual environment
    virtualenv -p python3 venv
    ```



#
> [OpenAI compatibility](https://ollama.com/blog/openai-compatibility)


# Reference
- [API Reference](https://platform.openai.com/docs/api-reference/introduction)


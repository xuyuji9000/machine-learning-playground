**mlx-community/Qwen3.5-9B-4bit**

``` shell
# 1. download model weights
pip install -U huggingface_hub
hf download mlx-community/Qwen3.5-9B-4bit
hf cache ls
```

``` shell
# 2. prepare virtual environment
python3 -m venv venv
source venv/bin/activate
pip3 install -r ./requirements.txt
```

``` shell
mlx_lm.server                           \
--model mlx-community/Qwen3.5-9B-4bit   \
--port 1234

# smoke test once a server is listening on :1234
curl -s http://localhost:1234/v1/chat/completions \
-H 'Content-Type: application/json' \
-d '{
  "model": "mlx-community/Qwen3.5-9B-4bit",
  "messages": [{"role": "user", "content": "What is the weather in Tokyo right now?"}],
  "tools": [{
    "type": "function",
    "function": {
      "name": "get_weather",
      "description": "Get current weather for a city",
      "parameters": {
        "type": "object",
        "properties": {"city": {"type": "string"}},
        "required": ["city"]
      }
    }
  }]
}' | python3 -m json.tool
```

``` shell
# 3. run get_weather on the client and replay the result
# server must already be listening on :1234
source venv/bin/activate
python3 get_weather.py
```


<!-- Reference -->
[1]: https://developers.openai.com/api/docs/guides/function-calling?api-mode=responses

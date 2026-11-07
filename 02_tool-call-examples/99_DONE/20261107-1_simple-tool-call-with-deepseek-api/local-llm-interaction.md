# Local notebook and DeepSeek interaction

The notebook makes two requests. The weather result `24℃` is filled in locally; no real weather API is called.

```mermaid
sequenceDiagram
    participant Local as 本地 notebook
    participant LLM as DeepSeek API

    Note over Local: 准备 tools: get_weather<br/>messages: user 问杭州天气

    Local->>LLM: chat.completions.create<br/>model=deepseek-flash<br/>messages + tools
    LLM-->>Local: assistant<br/>content: I'll check the weather...<br/>tool_calls: get_weather<br/>arguments: Hangzhou, Zhejiang<br/>id: call_00_...

    Note over Local: messages.append(assistant)<br/>本地填入工具结果 24℃<br/>messages.append(role=tool)

    Local->>LLM: chat.completions.create<br/>同一段 messages<br/>含 assistant 与 tool 回执
    LLM-->>Local: assistant<br/>content: 杭州当前 24°C<br/>tool_calls: null
```

The first round only decides to call `get_weather` and returns a `tool_call_id`. After the local side appends `24℃` under that same id, the second round writes the final answer.

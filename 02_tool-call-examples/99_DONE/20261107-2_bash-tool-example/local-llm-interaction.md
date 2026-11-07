# Local notebook and DeepSeek interaction

The notebook asks for the current date. DeepSeek only returns a `bash` tool call. The command runs locally with `bash -c`, then the stdout goes back as a `role: tool` message.

```mermaid
sequenceDiagram
    participant Local as 本地 notebook
    participant LLM as DeepSeek API

    Note over Local: 准备 tools: bash<br/>messages: user 要求运行 date

    Local->>LLM: chat.completions.create<br/>model=deepseek-flash<br/>messages + tools
    LLM-->>Local: assistant<br/>tool_calls: bash<br/>arguments: date '+%Y-%m-%d %H:%M:%S %Z'<br/>id: call_00_...

    Note over Local: messages.append(assistant)<br/>本地 bash -c 执行命令<br/>messages.append(role=tool)

    Local->>LLM: chat.completions.create<br/>同一段 messages<br/>含 assistant 与 tool 回执
    LLM-->>Local: assistant<br/>content: 引用 date 的输出<br/>tool_calls: null
```

第一轮只决定调用 `bash` 并返回 `tool_call_id`。本地把命令输出填到同一个 id 下面之后，下一轮才写最终回答。

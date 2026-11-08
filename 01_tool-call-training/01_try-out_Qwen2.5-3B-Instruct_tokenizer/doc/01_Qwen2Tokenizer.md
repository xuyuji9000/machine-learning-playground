# Qwen2Tokenizer（Qwen/Qwen2.5-3B-Instruct）

`AutoTokenizer.from_pretrained("Qwen/Qwen2.5-3B-Instruct")` 返回的是字节级 BPE 的 `Qwen2Tokenizer`。它负责把文本切成 token id，并规定对话边界、停止生成和工具调用用的控制符。

来源是 notebook 里打印出的 tokenizer 对象。

## 基本参数

| 字段 | 值 | 含义 |
|---|---|---|
| `vocab_size` | 151643 | 基础词表大小（BPE 词表），不含后面追加的 token |
| `model_max_length` | 131072 | 最大长度 128K（2^17）。超过这个长度才按截断规则切 |
| `padding_side` | `right` | padding 加在序列右边，左边是真实内容 |
| `truncation_side` | `right` | 超长时从右边砍，保留开头（system 和早期对话） |
| `eos_token` | `<\|im_end\|>` | 生成到这个 token 就停止。id 是 **151645** |
| `pad_token` | `<\|endoftext\|>` | batch 对齐用的填充符。id 是 **151643**，和 eos 不是同一个 |

打印出的 `special_tokens` 只有 `eos_token` 和 `pad_token`，没有单独的 `bos_token`。一段对话的边界靠 `<|im_start|>` 和 `<|im_end|>` 标出，这是 ChatML：

```text
<|im_start|>system
You are a helpful assistant.<|im_end|>
<|im_start|>user
你好<|im_end|>
<|im_start|>assistant
```

训练时 `pad_token` 和 `eos_token` 不同。padding 位置要在 label 里标成 ignore（例如 -100），不能当成正常要预测的词。

## 追加的 token（151643–151664）

`added_tokens_decoder` 里的 id 从 151643 起，都在基础词表之外。每一项都是一个 `AddedToken`，整段字符串对应一个 id，不会再被 BPE 拆开。

这 22 个 token 的标志相同：`rstrip=False, lstrip=False, single_word=False, normalized=False`。匹配时不剥左右空白，不要求是完整单词，也不做 Unicode 或大小写归一化。`<|im_start|>` 必须原样出现才会收成一个 token。

`special=True` 表示它是控制符，会计入 `all_special_tokens`。`special=False` 仍然是原子 token，只是不算 special token。工具调用和代码补全那一组是 `special=False`。

### 对话（ChatML）

- `151643` `<|endoftext|>`：原文结束，同时被设成 `pad_token`
- `151644` `<|im_start|>`：一条消息开始，后面紧跟角色名（`system` / `user` / `assistant`）
- `151645` `<|im_end|>`：一条消息结束，也是 `eos_token`

### 视觉 / 定位

这颗 3B 文本模型用不到这些 token。词表和 Qwen2-VL 共用，所以留着。

- `151646`–`151647`：`<|object_ref_start|>` / `<|object_ref_end|>`，物体引用
- `151648`–`151649`：`<|box_start|>` / `<|box_end|>`，矩形框
- `151650`–`151651`：`<|quad_start|>` / `<|quad_end|>`，四边形框
- `151652`–`151656`：`<|vision_start|>`、`<|vision_end|>`、`<|vision_pad|>`、`<|image_pad|>`、`<|video_pad|>`，图像和视频占位

### 工具调用

- `151657` `<tool_call>`
- `151658` `</tool_call>`

Qwen2.5-Instruct 约定模型这样吐出一次调用：

```text
<tool_call>
{"name": "函数名", "arguments": {...}}
</tool_call>
```

这两个标签各是一个 id。中间的 JSON 仍按普通 BPE 切。`<tools>`、`</tools>`、`<tool_response>` 不在这份追加词表里，会被拆成多个普通 token。

### 代码补全（Fill-in-the-Middle）

- `151659`–`151662`：`<|fim_prefix|>`、`<|fim_middle|>`、`<|fim_suffix|>`、`<|fim_pad|>`
- `151663` `<|repo_name|>`、`151664` `<|file_sep|>`：仓库级代码上下文里的仓库名和文件分隔

## 和模型 embedding 的差别

分词器基础词表是 151643，加上这 22 个追加 token 后，`len(tokenizer)` 是 **151665**。`Qwen/Qwen2.5-3B-Instruct` 的模型配置 `vocab_size` 是 **151936**（向上取整，方便 GPU 计算）。151665 到 151935 是 embedding 里的空位，没有对应字符串。

<!-- Reference -->

[1]: https://huggingface.co/Qwen/Qwen2.5-3B-Instruct

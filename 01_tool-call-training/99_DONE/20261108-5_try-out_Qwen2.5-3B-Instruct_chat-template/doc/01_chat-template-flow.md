# Chat Template Flow

Model: `Qwen/Qwen2.5-3B-Instruct`
Source: `main.ipynb`

Relationship between the **original message**, the **chat template** output, and the **tokens**.

## 1. Layer structure (message → text → token ids)

```mermaid
flowchart TD

  subgraph L1["① ORIGINAL MESSAGE — Python objects (structured, no text yet)"]
    direction TB
    M1["'role': 'system'"]
    M2["'content': 'You are a helpful assistant.'"]
    M3["'role': 'user'"]
    M4["'content': 'Give me a short introduction to large language model.'"]
  end

  subgraph L2["② CHAT TEMPLATE — plain string (Jinja applied)"]
    direction TB
    T1["&lt;|im_start|&gt;system\n"]
    T2["You are a helpful assistant."]
    T3["&lt;|im_end|&gt;\n"]
    T4["&lt;|im_start|&gt;user\n"]
    T5["Give me a short introduction to large language model."]
    T6["&lt;|im_end|&gt;\n"]
    T7["&lt;|im_start|&gt;assistant\n<br/><i>(added by add_generation_prompt=True)</i>"]
  end

  subgraph L3["③ TOKENS — integer ids, tensor shape [1, 29]"]
    direction TB
    K1["[151644, 8948, 198]<br/>0-2"]
    K2["[2610, 525, 264, 10950, 17847, 13]<br/>3-8"]
    K3["[151645, 198]<br/>9-10"]
    K4["[151644, 872, 198]<br/>11-13"]
    K5["[35127, 752, 264, 2805, 16800, 311, 3460, 4128, 1614, 13]<br/>14-23"]
    K6["[151645, 198]<br/>24-25"]
    K7["[151644, 77091, 198]<br/>26-28"]
  end

  M1 --> T1
  M2 --> T2
  M2 --> T3
  M3 --> T4
  M4 --> T5
  M4 --> T6
  M4 -.->|"generation prompt"| T7

  T1 --> K1
  T2 --> K2
  T3 --> K3
  T4 --> K4
  T5 --> K5
  T6 --> K6
  T7 --> K7

  L1 -->|"apply_chat_template(messages,<br/>tokenize=False,<br/>add_generation_prompt=True)"| L2
  L2 -->|"tokenizer(text, return_tensors='pt')"| L3
```

## 2. Pipeline view (encode → generate → decode)

```mermaid
flowchart LR
  A["messages<br/>(list of dict)"] -->|"tokenizer.apply_chat_template"| B["text<br/>(str)"]
  B -->|"tokenizer(...)"| C["input_ids<br/>(tensor [1,29])"]
  C -->|"model.generate(max_new_tokens=512)"| D["generated_ids<br/>(prompt + completion)"]
  D -->|"output_ids[len(input_ids):]"| E["new tokens only"]
  E -->|"batch_decode(skip_special_tokens=True)"| F["response<br/>(str)"]

  style A fill:#e8f0fe
  style B fill:#e6f4ea
  style C fill:#fce8e6
```

## 3. Notes

| Layer | Type | What owns the format |
|---|---|---|
| ① Original message | `list[dict]` with `role` / `content` | Your code / API schema |
| ② Chat template | `str` | Model's `chat_template` (Jinja) — adds `<\|im_start\|>`, `<\|im_end\|>`, `\n`, and the trailing `assistant` turn |
| ③ Tokens | `Tensor[int]` `[1, 29]` | Tokenizer — special tokens are single ids: `151644` = `<\|im_start\|>`, `151645` = `<\|im_end\|>`, `198` = `\n` |

- `tokenize=False` returns text; `tokenize=True` yields tokens directly (same result).
- Layer ② is not one string per message: each message becomes `im_start + role + "\n" + content + im_end + "\n"`, so ①→②→③ is 1:N:N.
- The final `<|im_start|>assistant\n` (ids 26–28) exists only because of `add_generation_prompt=True`.

## 4. Observed token sequence

```text
 0  151644  <|im_start|>
 1    8948  system
 2     198  \n
 3    2610  You
 4     525  are
 5     264  a
 6   10950  helpful
 7   17847  assistant
 8      13  .
 9  151645  <|im_end|>
10     198  \n
11  151644  <|im_start|>
12     872  user
13     198  \n
14   35127  Give
15     752  me
16     264  a
17    2805  short
18   16800  introduction
19     311  to
20    3460  large
21    4128  language
22    1614  model
23      13  .
24  151645  <|im_end|>
25     198  \n
26  151644  <|im_start|>
27   77091  assistant
28     198  \n
```

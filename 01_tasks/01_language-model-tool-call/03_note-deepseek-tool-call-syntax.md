# Note: What tool-call syntax does DeepSeek use?

Follow-up to `result.md` § "Tokenization and ChatML Framing" (lines 32–39).

## 1. What the report actually says (and doesn't)

`grep -i deepseek` across `result.md`, `result.zh-CN.md`, `result.json`, and
`01_initial-research.md` returns **nothing**. The report never names DeepSeek.

Lines 32–39 only describe the *generic* ChatML pattern, and the examples it gives
(`<|im_start|>tool_use`, `<function_call>`, `<|im_start|>tool_result`) are
illustrative placeholders — not any single vendor's real tokens. OpenAI's
`tool_calls`, Anthropic's `tool_use` content blocks, and DeepSeek's format are
three different instantiations of the same mechanism:

> a hard boundary token switches the model into a "machine-readable" mode, the
> inference engine stops generation, parses the payload, executes, and injects
> the result under a matching role token.

So the *mechanism* in lines 32–39 is right; only the concrete token names differ.

## 2. What DeepSeek actually uses

DeepSeek is closest to the "special-token boundary + JSON payload" hybrid — a
literal instance of the paragraph at line 36.

### Base dialogue template (V2 / V3 family)

ChatML-like, but **custom tokens, not `<|im_start|>`**:

```
<|begin▁of▁sentence|> <|User|> ... <|Assistant|> ... <|end▁of▁sentence|>
```

(`▁` is U+2581, the SentencePiece space marker — part of the token name, not a space.)

### Tool-call scaffolding (V3.1 / V3.2-era)

```
<|tool▁calls▁begin|>
<|tool▁call▁begin|>get_weather
```json
{"location": "Beijing"}
```
<|tool▁call▁end|>
<|tool▁calls▁end|>
```

Tool results are fed back inside `<|tool▁outputs▁begin|> … <|tool▁outputs▁end|>`.

Pattern: **function name on the line after the `call▁begin` token → arguments as a
fenced ```json block → `tool▁sep` / `call▁end` / `calls▁end` terminators.**

Compare with the three architectures the report classifies in
§ "Syntactic Architectures" (`result.md` line 40+):

| Report bucket | DeepSeek |
| :--- | :--- |
| JSON Schema (OpenAI-style `tool_calls`) | Payload is JSON, but wrapped in reserved tokens rather than raw top-level JSON |
| Python / CodeAct | No — DeepSeek does not emit Python signatures |
| Natural Language (NLT) | No — parameters are still structured |

=> It is a **hybrid**: JSON *payload* + ChatML-style *hard boundary tokens*. It is
not a clean fit for any single row of the report's table.

## 3. Caveats to flag if this is folded into the report

1. **Token spelling drifts across releases** — V3 vs V3.1-Terminus vs V3.2-Exp
   renamed several of these reserved tokens. The strings above are approximate.
2. **Unverified locally.** No `transformers` installed and no HF cache in this
   environment, so this was *not* checked against a real tokenizer. Mark it as
   "based on published chat templates", not "verified".
3. **Users usually never see these tokens.** DeepSeek's chat API is
   OpenAI-compatible, so user code only touches `tools` / `tool_calls` JSON. The
   `<|tool▁call▁begin|>` layer surfaces only when calling
   `tokenizer.apply_chat_template(...)` on a raw checkpoint. That split — vendor
   token layer vs. API layer — is itself worth one sentence in the report, since
   line 38's "template formatting must match between SFT and inference" claim is
   about the token layer, not the API layer.

## 4. How to verify (not yet run)

```bash
pip install -U transformers
python - <<'PY'
from transformers import AutoTokenizer
tok = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-V3.1", trust_remote_code=True)
print(tok.apply_chat_template(
    [{"role": "user", "content": "Weather in Beijing?"}],
    tools=[{"type": "function",
            "function": {"name": "get_weather",
                         "parameters": {"type": "object",
                                        "properties": {"location": {"type": "string"}}}}}],
    tokenize=False, add_generation_prompt=True))
PY
```

If the output differs from §2, trust the tokenizer over this note.

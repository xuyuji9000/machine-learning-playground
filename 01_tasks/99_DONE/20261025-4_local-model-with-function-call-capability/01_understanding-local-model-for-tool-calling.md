# Understanding: pick a local LLM with function-call (tool-call) capability

Recorded: 2026-10-25T05:45Z
Host: Apple M3 Max, 48 GB unified memory (macOS)
Status: research note only — no model downloaded, nothing benchmarked locally yet.

---

## 1. Objective

Choose a model that can be run **entirely on this machine** and that reliably
performs **function calling** (OpenAI-style `tools=[...]` → `tool_calls` → `role:tool`
results), to be driven from a local harness instead of a hosted API.

## 2. Environment facts (verified on this host)

| Check | Result |
| :--- | :--- |
| `sysctl -n machdep.cpu.brand_string` | `Apple M3 Max` |
| `sysctl -n hw.memsize` | 51 539 607 552 (= 48 GB) |
| `lms version` | LM Studio CLI v0.0.39 |
| `/Applications/LM Studio.app` | **absent** → `lms ls` fails with `spawn ... ENOENT` |
| `~/.lmstudio/models` | 4.4 GB, only `lmstudio-community/DeepSeek-R1-Distill-Qwen-7B-GGUF` |
| `ollama` | not installed |
| `python3 -c "import mlx_lm"` | `ModuleNotFoundError` → MLX runtime **not** installed |
| `python3 -V` | 3.15.0 |

Two consequences:

1. The only model already on disk is an **R1 distill** — a reasoning-only derivative
   of Qwen2.5 that has **no tool-call template**. It cannot do function calling
   regardless of the runtime. It is not a usable starting point.
2. Nothing is wired up yet: no MLX (`mlx-lm`), no Ollama, and the LM Studio GUI app
   is missing, so the CLI cannot start the local server.

**Practical memory budget:** macOS caps GPU-wired memory at roughly 75 % of
unified RAM ≈ **36 GB** on this box (LM Studio exposes this as a setting;
`mlx-lm` will simply swap/thrash past it). So a 4-bit model should stay
≲ 20–22 GB to leave room for a long context window.

## 3. What "function-call capability" actually requires

Four independent layers must all line up — a model that is good at reasoning is
*not* automatically a model that can call functions:

1. **Model was trained on tool-use data.** Emits a machine-parseable payload
   instead of prose like "I would call get_weather".
2. **A concrete wire syntax is baked into the chat template.** Three common
   families (see `../../../01_tasks/99_DONE/20261025-3_language-model-tool-call/03_note-deepseek-tool-call-syntax.md`):
   - OpenAI/JSON-Schema style `tool_calls` objects,
   - JSON payload wrapped in **reserved special tokens** (Qwen/DeepSeek/GLM),
   - raw Python `def` signatures (CodeAct-style).
3. **The runtime has a matching parser.** vLLM/SGLang expose `--tool-call-parser
   {qwen3_coder, mistral, glm47, ...}`; `llama.cpp`/Ollama use per-model templates;
   the OpenAI-compatible HTTP layer must translate the model's raw text into
   `finish_reason="tool_calls"` + a JSON object. **A parser mismatch is the single
   most common failure mode** — the model "works" but calls come back as plain text.
4. **The client sends schemas and replays results.** `tools=[...]` on the request,
   then `role:"tool"` messages keyed by `tool_call_id`.

So the selection criteria are: *trained for tools* + *runtime parser exists*.
Benchmarks (BFCL, τ²-Bench, Terminal-Bench) are the only cheap proxy for layer 1.

## 4. Verified candidates (HF API, 2026-10-25)

Sizes are **sum of repo blob sizes** for the MLX 4-bit conversion; `dl` = HF
downloads as a popularity proxy. Existence of every repo was confirmed with
HTTP 200; tool-calling claims come from the **upstream** model cards (the
`mlx-community` cards are auto-generated stubs that only point at them).

| Model (MLX 4-bit) | Size | dl | Evidence for tool calling |
| :--- | ---: | ---: | :--- |
| `mlx-community/Qwen3.5-35B-A3B-4bit` | 20.4 GB | 5 476 | Upstream card has a *Tool Calling* section + card-reported BFCL-V4 / TAU2-Bench / Terminal-Bench 2 rows; parser `qwen3_coder`; 262 144 ctx. MoE 35B total / 3B active → fast on Metal |
| `mlx-community/Qwen3.5-27B-4bit` | 16.1 GB | 3 480 | Same family card, same parser; dense 27B (slower per token than the MoE, stronger per-token quality) |
| `mlx-community/Devstral-Small-2-24B-Instruct-2512-4bit` | 15.1 GB | 69 114 | Card: *"excels at using tools to explore codebases, editing multiple files"*; parser `mistral`; built for SWE-agents. Most downloaded of the shortlist |
| `mlx-community/GLM-4.7-Flash-4bit` | 16.9 GB | 4 164 | Card: `--tool-call-parser glm47`, τ²-Bench **79.5** (vs 49.0 / 47.7 baselines), Preserved-Thinking mode for multi-turn agentic |
| `mlx-community/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-4bit` | 17.8 GB | 2 627 | MoE 30B-A3B; upstream card not anonymously readable (401) → tool support **unverified**, keep as backup only |
| `mlx-community/Qwen3.5-9B-4bit` | 6.0 GB | 19 273 | Same Qwen3.5 tool template, small; good cheap smoke-test / high-concurrency tier |
| `mlx-community/Ministral-3-14B-Instruct-2512-4bit` | 8.5 GB | 3 127 | Mistral tool syntax; smaller alternative to Devstral |

Older but still valid (previous recommendation, superseded by the Qwen3.5 row):
`Qwen3-30B-A3B-Instruct-2507-MLX-4bit` (17.2 GB) — the `2507` **Instruct** build is
non-thinking-only, which sidesteps the Qwen3-era problem where hybrid `think` mode
corrupted tool templates.

### Ruled out on memory grounds

| Model | 4-bit size | Why rejected |
| :--- | ---: | :--- |
| `Qwen3.5-122B-A10B-4bit` | 69.6 GB | > 48 GB |
| `Qwen3.8-Flash-Next-4bit` | 111.5 GB | > 48 GB |
| `GLM-5.3-Flash-4bit` | 204.0 GB | > 48 GB |
| `MiniMax-M3.1-Flash-Text-4bit` | 248.4 GB | > 48 GB |
| `DeepSeek-V4.1-Flash-1017-oQ4e-mtp` | 432.0 GB | > 48 GB |
| `Kimi-K2.5` | 657.6 GB | > 48 GB |

The 2026 naming convention is misleading: for Qwen/GLM/MiniMax/DeepSeek the
current "**Flash**" SKUs are the *large* tier, not small ones.

## 5. Recommendation

**Default: `mlx-community/Qwen3.5-35B-A3B-4bit` (20.4 GB).**
MoE with 3B active parameters gives near-8B latency with 35B-level quality — the
best quality/speed point that still leaves ~15 GB of headroom for a 32k+ context.
Its chat template and `qwen3_coder` tool parser are the most widely supported by
local runtimes, which minimises layer-3 failure risk.

Tier alternatives:

- **Agentic coding / file-editing harness** → `Devstral-Small-2-24B-Instruct-2512-4bit` (15.1 GB)
- **Best tool-loop number, more setup care** → `GLM-4.7-Flash-4bit` (16.9 GB)
- **Fast iteration, tiny tests** → `Qwen3.5-9B-4bit` (6.0 GB)
- **Do not** pick `Nemotron-3.5-Lightning` first: tool support not verifiable from an
  anonymous card fetch.

Runtime choice, given the environment:

- **`mlx-lm` (pip) — preferred.** Native Metal, OpenAI-compatible
  `python -m mlx_lm.server --port 1234`, no GUI dependency. Nothing to install
  beyond `pip install -U mlx-lm`.
- **LM Studio** — needs the GUI app reinstalled (`/Applications/LM Studio.app` is
  missing); only then can `lms load` / `lms server start` work.
- **llama.cpp / Ollama (GGUF)** — only worth it if the same weights must later run
  on CUDA/Linux. GGUF Q4_K_M is measurably slower than MLX on Apple silicon.
- **Avoid on macOS:** AWQ / GPTQ quantisations (no Metal kernels).

## 6. Verification plan (not yet executed)

1. `pip install -U mlx-lm` and `mlx_lm.generate` sanity check (proves Metal works).
2. Download the chosen 4-bit repo; confirm on-disk size matches the table above.
3. Start the OpenAI-compatible server with a tool-call parser, context ≥ 16 384.
4. POST a single-tool request and assert:
   - HTTP 200,
   - `choices[0].finish_reason == "tool_calls"`,
   - `choices[0].message.tool_calls[0].function.name == "get_weather"`,
   - `arguments` parses as JSON and contains the expected `city`.
5. Replay the call with a `role:"tool"` message and confirm the model consumes the
   result and answers (this is where template bugs usually surface).
6. Only then compare candidates on the same 10-prompt tool suite; record latency,
   tokens/s, and parse-failure rate — not vibes.

```bash
# smoke test once a server is listening on :1234
curl -s http://localhost:1234/v1/chat/completions -H 'Content-Type: application/json' -d '{
  "model": "qwen3.5-35b-a3b",
  "messages": [{"role":"user","content":"What is the weather in Tokyo right now?"}],
  "tools": [{"type":"function","function":{"name":"get_weather","description":"Get current weather for a city","parameters":{"type":"object","properties":{"city":{"type":"string"}},"required":["city"]}}}]
}' | python3 -m json.tool
```

## 7. Open questions

- Does `mlx-lm`'s server ship a `qwen3_coder`/`mistral` tool-call parser, or must the
  raw output be parsed by hand? (Upstream cards only document vLLM/SGLang flags.)
- Quantisation sensitivity: does 4-bit degrade tool-argument validity vs 6/8-bit?
  Argument JSON errors are known to appear first at low bit-width.
- Whether `Qwen3.5-35B-A3B` needs thinking mode disabled for tool calls, as the
  Qwen3 (2507) line did.

# Task: Use DeepSeek Search API

## What is DeepSeek Search?

**DeepSeek Search** is DeepSeek's *in-house, AI-native general-purpose search
engine*. For a long time it only powered DeepSeek's own web/app "联网搜索"
feature; on **2026-10-17** it was **opened up as a public API**, together with
the `DeepSeek-V4.1-Flash-1017` release.

Characteristics claimed by DeepSeek:

- Indexes **hundreds of billions of web pages**, multilingual
- Handles **hundreds of millions of search requests per day** worldwide
- Returns **relevant / authoritative / timely** results in real time
- Filters **SEO spam, GEO manipulation, and low-quality AIGC** content
  (i.e. results are meant to be safe to feed straight into an LLM)

## Two ways to "search the web on demand"

| # | Path | Who decides to search | Endpoint | Models |
| - | ---- | --------------------- | -------- | ------ |
| 1 | **Search & Fetch API** (raw JSON tools) | **You** (your agent / RAG loop) | `POST /v1/tools/search`, `POST /v1/tools/fetch` | any model, or no model at all |
| 2 | **Server-side `web_search` tool** in the Responses API | **The model** | `POST /v1/responses` with `tools: [{"type": "web_search"}]` | `deepseek-v4-pro` only (ignored on `deepseek-flash`) |

Notes:

- **Chat Completions API has no built-in web search** — its `tools` field only
  accepts `type: "function"`. If you use `deepseek-chat` / `deepseek-flash` via
  Chat Completions, you must call the Search API yourself and paste the results
  back into the conversation (i.e. implement the tool loop client-side).
- Path 2 is the closest analogue to OpenAI's `web_search` built-in tool: the API
  runs the search **on the server**, injects the results into the context and
  continues generating.

---

## Path 1: Search & Fetch API

Both are plain JSON APIs, same bearer auth as the DeepSeek model API.
Base URL: `https://api.deepseek.com`

| API    | Endpoint                              |
| ------ | ------------------------------------- |
| Search | `POST https://api.deepseek.com/v1/tools/search` |
| Fetch  | `POST https://api.deepseek.com/v1/tools/fetch`  |

### Authentication

| Header          | Required | Value                          |
| --------------- | -------- | ------------------------------ |
| `Authorization` | Yes      | `Bearer <DeepSeek API Key>`     |
| `Content-Type`  | Yes      | `application/json`             |

### Search — request fields

| Field          | Type    | Required | Default | Description |
| -------------- | ------- | -------- | ------- | ----------- |
| `query`        | string  | Yes      | -       | 1–128 Unicode chars, not all whitespace; supports the query operators below |
| `count`        | integer | No       | `10`    | Number of results, 1–50 |
| `ori_question` | string  | No       | -       | The user's original question (≤128 chars) that triggered the search; improves query understanding |
| `localization` | string  | No       | `""`    | An IP address used to localize results |
| `need_content` | boolean | No       | `false` | Also return full page text in `content` (empty string when `false`) |

Unknown fields are ignored.

### Search — query operators

The query is forwarded **with its search syntax intact**; operators can be combined.

| Operator  | Example                                  | Meaning |
| --------- | ---------------------------------------- | ------- |
| `site:`   | `DeepSeek site:github.com`               | Restrict to a site; multiple sites: `site:a.com OR site:b.com` |
| `-site:`  | `DeepSeek -site:example.com`             | Exclude a site (space-separated for many) |
| `-`       | `DeepSeek -advertisement`                | Exclude pages containing a term |
| `-"..."`  | `DeepSeek -"release notes"`              | Exclude an exact phrase |
| `"..."`   | `DeepSeek "exact phrase"`                | Match an exact phrase |
| `lang:`   | `DeepSeek lang:zh,en`                    | Restrict to languages (comma-separated) |
| `after:`  | `DeepSeek after:2025` / `after:2025-01-01` | Published after a date |
| `before:` | `DeepSeek before:2026` / `before:2026-06-01` | Published before a date |

Example combined query:

```json
{
  "query": "DeepSeek site:github.com OR site:huggingface.co lang:en after:2025",
  "count": 10
}
```

### Search — response

HTTP 200 with a `results` array (empty array when nothing matches).

```json
{
  "results": [
    {
      "rerank_score": 2.4,
      "title": "DeepSeek V4 model released",
      "url": "https://example.com/deepseek-v4",
      "snippet": "DeepSeek V4 is now available, with tool calling and long-context support.",
      "summary": "DeepSeek has released the V4 model. The release adds improved tool calling...",
      "content": "DeepSeek V4 is now generally available...",
      "site_name": "Example News",
      "site_icon": "https://example.com/favicon.ico",
      "date": "2026-06-01T00:00:00+00:00",
      "authority": 3
    }
  ]
}
```

| Field          | Type            | Description |
| -------------- | --------------- | ----------- |
| `rerank_score` | number          | Relevance 0–3 (relevance + authority + freshness); **≥1.5 = high quality** |
| `title`        | string          | Result title |
| `url`          | string          | Result URL |
| `snippet`      | string          | Short summary (~100–200 chars), **for UI display** |
| `summary`      | string          | Long summary (~600–800 chars), **for the model to read** |
| `content`      | string          | Full page text; empty unless `need_content: true` (or unavailable) |
| `site_name`    | string \| null  | Site name |
| `site_icon`    | string \| null  | Site icon URL |
| `date`         | string \| null  | Publication time, RFC 3339 (UTC) |
| `authority`    | integer         | Authority tier 0–4 (`-1` = unknown); **≥3 = highly authoritative** |

> Practical tip: build RAG context from `summary` (+`content` when needed), and
> filter with `rerank_score >= 1.5` and/or `authority >= 3`.

### Fetch — request / response

Request:

| Field | Type   | Required | Description |
| ----- | ------ | -------- | ----------- |
| `url` | string | Yes      | ≤8192 chars, `http`/`https` with a host, **no username/password in the URL** |

Response:

```json
{
  "title": "Example article",
  "content": "# Example article\n\nArticle content."
}
```

`content` is the page converted to **Markdown**. Fetching is subject to the
target site's availability and access policies.

### Errors

OpenAI-compatible error format (`param` is always `null`):

```json
{
  "error": {
    "message": "'count' must be between 1 and 50",
    "type": "invalid_request_error",
    "param": null,
    "code": "invalid_request_error"
  }
}
```

| HTTP | Meaning |
| ---- | ------- |
| 400  | Invalid headers/body (malformed JSON, bad field value) |
| 401  | API key missing or invalid |
| 402  | Insufficient balance |
| 403  | **Fetch** rejected by the security policy |
| 404  | **Fetch** could not get usable content (dead URL, blocked, unsupported content type, no extractable Markdown) |
| 408  | Reading the request body timed out |
| 413  | Request body too large |
| 429  | Search/Fetch QPS limit exceeded |
| 500  | Internal server error |
| 504  | Downstream timeout |

Retry policy: Search & Fetch are **read-only** → retry on 408 / 429 / 5xx after a
wait; on 402 top up first; **do not** retry other 4xx without changing the request.

### Billing

Billed **per successful request**, not per token, not per result:

| API    | Unit                          | Price  |
| ------ | ----------------------------- | ------ |
| Search | per 1,000 successful requests | $0.75  |
| Fetch  | per 1,000 successful requests | $0.75  |

- Billable only when HTTP 200 **and** a result exists (Search: non-empty
  `results`; Fetch: page content returned). Failures, empty results and
  timeouts are free.
- `count` does **not** change the per-request price.
- Search/Fetch calls made by **server-side tools** in DeepSeek Harness,
  Claude Code and Codex are **currently free**; billing starts
  **00:00 Beijing time on Nov 1, 2026 (= Oct 31, 2026 16:00 UTC)**.

### Rate limits (per account, independent of each other)

| API    | QPS limit |
| ------ | --------- |
| Search | 100       |
| Fetch  | 25        |

- Account-level, regardless of which API key is used, and **separate from model
  concurrency limits**. Above the limit → HTTP 429.
- Fetch additionally has a **per-domain** QPS limit (also 429).

---

## Path 2: server-side `web_search` tool (Responses API)

`POST https://api.deepseek.com/v1/responses` (OpenAI Responses-API compatible,
`base_url = https://api.deepseek.com`).

- `tools: [{"type": "web_search"}]` → the server performs the search, adds the
  results to the context and continues the response.
- Supported with `deepseek-v4-pro`; **ignored** with `deepseek-flash`.
- Output items of type `web_search_call` appear in `output`.
- Streaming events: `response.web_search_call.in_progress` /
  `.searching` / `.completed`.
- Multi-turn: `web_search_call` items from a previous response can be passed
  back in `input` — their search results are restored and concatenated into the
  context (the API is otherwise stateless: `store: false`, no
  `previous_response_id`).

Caveat: since **Sept 14, 2026 04:00 UTC** all `deepseek-v4-pro` requests are
routed to `V4.1-Flash` at V4.1-Flash rates until V4.1-Pro launches, so the
`web_search` tool currently runs on that model.

---

## Typical agent loop with Search & Fetch (Path 1)

```text
user question
   │
   ├─(optional)─ LLM rewrites it into 1..n search queries (≤128 chars)
   │
   ├─ POST /v1/tools/search  {query, count, ori_question}
   │     └─ keep results with rerank_score >= 1.5, read `summary`
   │
   ├─ need the full article?  POST /v1/tools/fetch {url} → Markdown
   │     └─ on 404/403 → skip that source
   │
   ├─ feed summaries/content into the model as context
   │
   └─ model answers (with citations = the `url`s)
        └─ not enough? → loop back with a refined query
```

## Minimal usage

```shell
export DEEPSEEK_API_KEY='sk-...'

# 1. Search the web
curl -s https://api.deepseek.com/v1/tools/search \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"query": "DeepSeek V4 release", "count": 5, "need_content": false}'

# 2. Fetch one result page as Markdown
curl -s https://api.deepseek.com/v1/tools/fetch \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/deepseek-v4"}'
```

```python
# pip install requests
import requests

HEADERS = {"Authorization": "Bearer <DeepSeek API Key>"}
BASE = "https://api.deepseek.com"

res = requests.post(
    f"{BASE}/v1/tools/search",
    headers=HEADERS,
    json={"query": "DeepSeek V4 release", "count": 5},
)
res.raise_for_status()
top = [r for r in res.json()["results"] if r["rerank_score"] >= 1.5]

page = requests.post(f"{BASE}/v1/tools/fetch", headers=HEADERS,
                     json={"url": top[0]["url"]}).json()
print(page["title"], "\n", page["content"][:500])
```

## Comparison with Google Deep Research (previous task)

| | DeepSeek Search & Fetch | Google Deep Research |
| - | ---------------------- | -------------------- |
| Nature | **Raw tools** (search + fetch), you build the agent | **Managed agent**, runs the whole research loop |
| Granularity | One search / one page per call | Multi-step plan → hundreds of sources → report |
| Latency | Sub-second to seconds | Minutes (background task + polling) |
| Output | Structured JSON results / Markdown page | Long report with citations + charts |
| Cost | $0.75 per 1,000 successful calls | Model/token-based, long-running |
| Best for | Agents, RAG, on-demand lookups | Deep, comprehensive research reports |

## References

- Search & Fetch guide: <https://api-docs.deepseek.com/guides/search>
  (中文: <https://api-docs.deepseek.com/zh-cn/guides/search>)
- Search API reference: <https://api-docs.deepseek.com/api/search>
- Fetch API reference: <https://api-docs.deepseek.com/api/fetch>
- Responses API guide (`web_search` tool): <https://api-docs.deepseek.com/guides/responses_api>
- Chat Completions reference (tools = function only): <https://api-docs.deepseek.com/api/create-chat-completion>
- Change log (2026-10-17, "Opening up the in-house search API"): <https://api-docs.deepseek.com/updates>
- Announcement: <https://api-docs.deepseek.com/news/news261017>

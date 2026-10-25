# curl examples — DeepSeek Search & Fetch API

> Status: **not yet executed** — requires `DEEPSEEK_API_KEY`
> (top up at <https://platform.deepseek.com>, Search/Fetch = $0.75 per 1,000
> successful calls).

```shell
export DEEPSEEK_API_KEY='sk-...'
```

## 1. Search (structured results)

```shell
curl -s https://api.deepseek.com/v1/tools/search \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "DeepSeek V4 release",
    "count": 5,
    "need_content": false
  }' | python3 -m json.tool
```

Print just what a model needs (`summary`) plus the citation URL:

```shell
curl -s https://api.deepseek.com/v1/tools/search \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"query":"DeepSeek V4 release","count":5}' \
| python3 -c '
import json, sys
for r in json.load(sys.stdin)["results"]:
    print("[%.2f|auth%s] %s" % (r["rerank_score"], r["authority"], r["title"]))
    print("  " + r["url"])
    print("  " + r["summary"] + "\n")
'
```

## 2. Search with query operators (site / lang / time range)

```shell
curl -s https://api.deepseek.com/v1/tools/search \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "DeepSeek site:github.com OR site:huggingface.co lang:en after:2025",
    "count": 10,
    "ori_question": "Where can I download DeepSeek models?"
  }' | python3 -m json.tool
```

## 3. Fetch one page → Markdown

```shell
curl -s https://api.deepseek.com/v1/tools/fetch \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://api-docs.deepseek.com/news/news261017"}' \
| python3 -c 'import json,sys; p=json.load(sys.stdin); print(p["title"]); print(p["content"][:2000])'
```

## 4. search → fetch → answer (one shell pipeline)

```shell
URL=$(curl -s https://api.deepseek.com/v1/tools/search \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"query":"DeepSeek V4.1 Flash","count":3}' \
| python3 -c 'import json,sys; print(json.load(sys.stdin)["results"][0]["url"])')

echo "top hit: ${URL}"

curl -s https://api.deepseek.com/v1/tools/fetch \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "{\"url\": \"${URL}\"}" | python3 -m json.tool | head -50
```

## 5. Model-driven search: `web_search` server-side tool (Responses API)

```shell
curl -s https://api.deepseek.com/v1/responses \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-v4-pro",
    "instructions": "You are a helpful assistant. Cite the URLs you used.",
    "input": "What did DeepSeek release in October 2026?",
    "tools": [{"type": "web_search"}]
  }' | python3 -m json.tool
```

- The search runs **server-side**; look for `web_search_call` items in `output`.
- With `"stream": true` you get `response.web_search_call.in_progress` /
  `.searching` / `.completed` events.
- `web_search` is ignored on `deepseek-flash`; Chat Completions does not support
  it at all (function tools only).

## Expected error shapes

```shell
# 400 — bad field value
curl -s https://api.deepseek.com/v1/tools/search \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"query":"test","count":999}'
# {"error":{"message":"'count' must be between 1 and 50","type":"invalid_request_error","param":null,"code":"invalid_request_error"}}

# 429 — above 100 QPS (Search) / 25 QPS (Fetch) per account → back off and retry
# 403/404 — Fetch blocked by security policy / no extractable content → skip that source
```

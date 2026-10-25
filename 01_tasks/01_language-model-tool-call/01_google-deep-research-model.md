``` shell
export GEMINI_API_KEY=''

# 1. Start the research task
QUERY_TEXT='How the llm tool call capability is trained'

curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
-H "Content-Type: application/json" \
-H "x-goog-api-key: $GEMINI_API_KEY" \
-d "{
\"input\": \"${QUERY_TEXT}\",
\"agent\": \"deep-research-preview-04-2026\",
\"background\": true
}"

# Response
# {
#   "id": "v1_ChduNFhkYXFxeEs3THlxdHNQal82S3FBMBIXbjRYZGFxcXhLN0x5cXRzUGpfNktxQTA",
#   "status": "in_progress",
#   "created": "2026-10-25T04:29:20Z",
#   "updated": "2026-10-25T04:29:20Z",
#   "service_tier": "standard",
#   "object": "interaction",
#   "agent": "deep-research-preview-04-2026"
# }

```

``` shell
# 2. Poll for results (replace INTERACTION_ID)
INTERACTION_ID='v1_ChduNFhkYXFxeEs3THlxdHNQal82S3FBMBIXbjRYZGFxcXhLN0x5cXRzUGpfNktxQTA'

curl -X GET "https://generativelanguage.googleapis.com/v1beta/interactions/${INTERACTION_ID}" \
-H "x-goog-api-key: $GEMINI_API_KEY"                                                          \
| jq
```

``` shell
# 3. Print status every 15s until the task leaves in_progress
# Typical statuses: in_progress, completed, failed

while true; do
  STATUS=$(curl -s -X GET "https://generativelanguage.googleapis.com/v1beta/interactions/${INTERACTION_ID}" \
    -H "x-goog-api-key: $GEMINI_API_KEY" \
    | python3 -c 'import json,sys; print(json.load(sys.stdin).get("status","unknown"))')
  echo "$(date -u +%H:%M:%SZ) status=${STATUS}"
  case "$STATUS" in
    completed|failed|cancelled)
      say "The research task status is $STATUS."
      break
      ;;
  esac
  sleep 15
done
```
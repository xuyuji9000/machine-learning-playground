``` shell
export GEMINI_API_KEY=''

# 1. Start the research task
curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
-H "Content-Type: application/json" \
-H "x-goog-api-key: $GEMINI_API_KEY" \
-d '{
"input": "Research the history of Google TPUs.",
"agent": "deep-research-preview-04-2026",
"background": true
}'

# Response
# {"id":"v1_ChdxR25kYW9YVUpfZTdxdHNQdnRLZDJBWRIXcUduZGFvWFVKX2U3cXRzUHZ0S2QyQVk","status":"in_progress","created":"2026-10-25T02:30:01Z","updated":"2026-10-25T02:30:01Z","service_tier":"standard","object":"interaction","agent":"deep-research-preview-04-2026"}
```

``` shell
# 2. Poll for results (replace INTERACTION_ID)
INTERACTION_ID='v1_ChdxR25kYW9YVUpfZTdxdHNQdnRLZDJBWRIXcUduZGFvWFVKX2U3cXRzUHZ0S2QyQVk'
curl -X GET "https://generativelanguage.googleapis.com/v1beta/interactions/${INTERACTION_ID}" \
-H "x-goog-api-key: $GEMINI_API_KEY"
```

``` shell
# 3. Print status every 15s until the task leaves in_progress
# Typical statuses: in_progress, completed, failed
INTERACTION_ID='v1_ChdxR25kYW9YVUpfZTdxdHNQdnRLZDJBWRIXcUduZGFvWFVKX2U3cXRzUHZ0S2QyQVk'

while true; do
  STATUS=$(curl -s -X GET "https://generativelanguage.googleapis.com/v1beta/interactions/${INTERACTION_ID}" \
    -H "x-goog-api-key: $GEMINI_API_KEY" \
    | python3 -c 'import json,sys; print(json.load(sys.stdin).get("status","unknown"))')
  echo "$(date -u +%H:%M:%SZ) status=${STATUS}"
  case "$STATUS" in
    completed|failed|cancelled) break ;;
  esac
  sleep 15
done
```
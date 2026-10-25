# Task: Use Google Deep Research Model

## What is Google Deep Research?

**Deep Research** is Google's *agentic research* capability. It is not a
standalone model weight to download, but a Gemini-powered **agent** that
autonomously conducts multi-step research.

- Launched in the Gemini app (Dec 2024)
- Now also available programmatically via the **Gemini API**
- As of the Apr 2026 update, the agents are built on **Gemini 3.1 Pro**

## How it works

1. **Plans** — decomposes the prompt into a structured research plan.
  With *collaborative planning* (`collaborative_planning=True`), the agent
   returns a proposed plan first, which can be reviewed/edited/approved
   through multi-turn interactions before execution.
2. **Executes** — iteratively searches the web (or custom sources),
  browsing and reading hundreds of sources. Takes several minutes.
3. **Synthesizes** — produces a long, organized report with inline
  citations, optionally with charts/visualizations.



## Agent versions (Apr 2026)


| Agent ID                            | Purpose                                      |
| ----------------------------------- | -------------------------------------------- |
| `deep-research-preview-04-2026`     | Speed/efficiency, good for streaming to a UI |
| `deep-research-max-preview-04-2026` | Maximum comprehensiveness for deep analysis  |


Extra capabilities: **MCP server support** (connect external tools),
**native visualizations**, **document inputs**.

## Where it is available

- **Consumer UIs**: Gemini app, NotebookLM, Gemini Enterprise
("Deep Research" button)
- **Gemini API**: exclusively via the **Interactions API**
(NOT `generate_content`). Currently in *preview*.
  - Tasks are long-running → must use background execution
  (`background=True`) and poll for results or stream updates.



## Minimal API usage (Python)

```python
# pip install google-genai
# export GEMINI_API_KEY=...
import time
from google import genai

client = genai.Client()

interaction = client.interactions.create(
    input="Research the history of Google TPUs.",
    agent="deep-research-preview-04-2026",
    background=True,
)
print(f"Research started: {interaction.id}")

while True:
    interaction = client.interactions.get(interaction.id)
    if interaction.status == "completed":
        print(interaction.steps[-1].content[0].text)
        break
    elif interaction.status == "failed":
        print(f"Research failed: {interaction.error}")
        break
    time.sleep(10)
```



### REST equivalent

```shell
# 1. Start the research task
curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -d '{
    "input": "Research the history of Google TPUs.",
    "agent": "deep-research-preview-04-2026",
    "background": true
  }'

# 2. Poll for results (replace INTERACTION_ID)
# curl -X GET "https://generativelanguage.googleapis.com/v1beta/interactions/INTERACTION_ID" \
#   -H "x-goog-api-key: $GEMINI_API_KEY"
```



## References

- Official docs: [https://ai.google.dev/gemini-api/docs/deep-research](https://ai.google.dev/gemini-api/docs/deep-research)
- Developer guide: [https://aistudio.google.com/learn/deep-research-developer-guide](https://aistudio.google.com/learn/deep-research-developer-guide)
- Announcement (Deep Research / Deep Research Max):
[https://blog.google/innovation-and-ai/models-and-research/gemini-models/next-generation-gemini-deep-research/](https://blog.google/innovation-and-ai/models-and-research/gemini-models/next-generation-gemini-deep-research/)
- Consumer product page: [https://gemini.google/us/overview/deep-research/](https://gemini.google/us/overview/deep-research/)



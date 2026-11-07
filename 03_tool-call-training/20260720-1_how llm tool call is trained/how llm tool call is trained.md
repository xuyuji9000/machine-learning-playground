# Deep Research Report: How LLMs are Trained for Tool Calling

## 1. Introduction

Large Language Models (LLMs) are natively autoregressive next-token predictors trained on static data. While they excel at reasoning and language tasks, they traditionally struggle with retrieving up-to-date information, executing precise mathematical operations, or interacting with external systems. To solve this, the industry developed **tool calling** (or function calling).

The transition to tool-using LLMs evolved from hardcoded integrations (e.g., *WebGPT*) to zero-shot prompting with descriptions, and finally to native function calling fine-tuned directly into the model (as popularized by OpenAI's API and open-source models like *NexusRaven* and *xLAM*).

## 2. Dataset Preparation for Function Calling

The foundation of training an LLM for tool use is building a robust dataset that teaches the model when and how to call external APIs based on a user's natural language request.

### Data Structure

A typical function-calling dataset (such as Salesforce's `xLAM-function-calling-60k`) contains three main components for every training instance:

- **`query`**: The user's natural language problem statement (e.g., "Find the sum of multiples of 3 and 5 between 1 and 1000").
- **`tools`**: An array of available functions. Each function includes a `name`, `description`, and a `parameters` object detailing the schema (parameter name, type, description, and whether it is required).
- **`answers`**: The expected output, typically an array specifying the tool `name` to invoke and the specific `arguments` mapping to the schema.

### Generating the Data

Because manually labeling thousands of tool interactions is prohibitively expensive and hard to scale, modern datasets rely heavily on automated generation and augmentation:

- **Self-Supervised Generation**: As pioneered by *Toolformer*, a base model can generate candidate tool calls across a massive corpus of text.
- **Code Corpus Extraction**: Systems like *NexusRaven* and *ToolLLM* start with repositories of executable code, use an LLM to generate natural language descriptions of the functions, and then synthesize user queries that would require those functions. To make the model robust, similar but irrelevant candidate functions (distractors) are added to force the model to learn discrimination.
- **Verification**: In datasets like APIGen, generated tool calls are rigorously checked through three stages: format checking, actual function execution (to ensure the generated arguments are valid), and semantic verification.

## 3. Encoding Tools in the Prompt

During training (and subsequent inference), the model does not interact with Python or JSON objects natively; everything must be flattened into text tokens.

Model builders typically inject the tool definitions into the **system prompt**. A common pattern is to represent the functions as JSON schemas enclosed within special XML tags (e.g., `<tools>...</tools>`).

The model is trained to recognize this block, evaluate the user's query against the provided definitions, and, if a tool is needed, output a specific trigger sequence (e.g., `<tool_call>{"name": "...", "arguments": {...}}</tool_call>`). This in-context learning setup teaches the model a unified syntax for tool usage, regardless of what arbitrary functions a user might supply at inference time.

## 4. Key Training Methodologies

### Supervised Fine-Tuning (SFT)

The primary method for instilling generalized tool-calling abilities is SFT. Models are fine-tuned on the structured datasets described above to map [System Prompt + Tool Schema + User Query] to [Tool Call Output].

### Self-Supervised Learning (*Toolformer*)

*Toolformer* introduced a novel approach where the model teaches itself:

1. The model uses few-shot prompting to propose API calls within a standard training corpus.
2. The API calls are executed.
3. The system measures if the API's return value reduces the model's loss (perplexity) in predicting the subsequent text.
4. Only helpful tool calls are retained, and the model is fine-tuned on this augmented, self-annotated dataset.

### ReAct (Reasoning + Acting)

While *Toolformer* focused on single, isolated API calls, real-world agentic behavior requires chaining tools. The **ReAct** paradigm interleaves thought generation with action. Datasets like xLAM generate extensive multi-turn conversations featuring a `Thought -> Action -> Observation` loop, training the model to think before it acts and to evaluate the result (Observation) before taking its next step.

## 5. Challenges and Solutions

- **Parameter Hallucination & Schema Adherence**: LLMs sometimes invent parameters or ignore the requested JSON schema. This is mitigated during training by ensuring high-quality, strictly formatted datasets verified by actual execution (e.g., APIGen pipeline).
- **Multi-step Reasoning & Tool Chaining**: Early tool models generated calls independently and couldn't chain them (where the output of Tool A feeds into Tool B). Modern training datasets heavily augment data with synthesized, multi-turn human-agent conversations that rely on *ReAct*-style loops to teach state management and chaining.
- **Over-reliance on Tools**: Models must know when *not* to use a tool. Training datasets are carefully curated to include queries that can be answered natively, punishing the model for unnecessary tool invocations.

## 6. State-of-the-Art and Influential Works

- **Toolformer (2023)**: Proved LLMs can teach themselves to use tools via self-supervised perplexity filtering.
- **ReAct (2022)**: Established the standard reasoning-action loop necessary for multi-step agent behaviors.
- **NexusRaven & ToolLLM (2023)**: Showed how to train models for zero-shot, user-defined function calling by scaling data generation from existing APIs.
- **Llama 3**: Extracted tool calls from massive codebases, applying Llama 3 to generate corresponding natural language queries.
- **xLAM Models**: Currently dominate leaderboards like the Berkeley Function-Calling Leaderboard (BFCL) through exceptional data synthesis, verification, and multi-turn execution training.

## 7. References

1. Simplicity is SOTA: *How LLMs are trained for function calling* - Link
2. Miraflow AI: *LLM Agents and Tool Use: How Models Learn to Act* - Link
3. Hugging Face Datasets: *Salesforce/xlam-function-calling-60k* - Link

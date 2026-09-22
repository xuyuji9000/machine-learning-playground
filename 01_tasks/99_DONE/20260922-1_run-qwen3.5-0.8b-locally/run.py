"""Run Qwen3.5-0.8B locally on Apple Silicon (MPS) or CPU.

Usage:
    source venv/bin/activate
    python run.py ["optional prompt"]
"""

import sys

import torch
from transformers import AutoProcessor, AutoModelForImageTextToText

MODEL_DIR = "./Qwen3.5-0.8B"


def main() -> None:
    prompt = sys.argv[1] if len(sys.argv) > 1 else (
        "Give me a short introduction to large language models."
    )

    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Device: {device}", file=sys.stderr)

    processor = AutoProcessor.from_pretrained(MODEL_DIR)
    tokenizer = processor.tokenizer
    # NOTE: loading directly with device_map="mps" segfaults (torch 2.14 on macOS):
    # transformers' multithreaded weight loading races in Metal's shader-jit cache.
    # Load on CPU first, then move to MPS serially.
    model = AutoModelForImageTextToText.from_pretrained(
        MODEL_DIR,
        dtype=torch.bfloat16,
        device_map="cpu",
    ).to(device)
    model.eval()

    messages = [{"role": "user", "content": prompt}]
    inputs = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_tensors="pt",
        enable_thinking=False,  # non-thinking mode
    ).to(device)

    # Recommended sampling for non-thinking, text tasks (see model README).
    # This transformers build has no PresencePenaltyLogitsProcessor and generate()
    # rejects presence_penalty, so implement it as a custom logits processor.
    from transformers import LogitsProcessor

    class PresencePenalty(LogitsProcessor):
        def __init__(self, penalty: float):
            self.penalty = penalty

        def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor) -> torch.FloatTensor:
            is_present = torch.zeros_like(scores, dtype=scores.dtype)
            is_present.scatter_(1, input_ids, 1.0)
            return scores - self.penalty * is_present

    output = model.generate(
        **inputs,
        max_new_tokens=512,
        do_sample=True,
        temperature=1.0,
        top_p=1.0,
        top_k=20,
        min_p=0.0,
        logits_processor=[PresencePenalty(2.0)],
    )

    generated = output[0][inputs["input_ids"].shape[1]:]
    print(tokenizer.decode(generated, skip_special_tokens=True))


if __name__ == "__main__":
    main()

import torch
from transformers import WhisperForConditionalGeneration
from torchview import draw_graph

# 1. Load Whisper Tiny model
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny")
model.eval()

# 2. Define dummy inputs (batch=1, 80 mel bins, 3000 time frames for 30s audio)
input_features = torch.randn(1, 80, 3000)
decoder_input_ids = torch.tensor([[1, 2, 3]], dtype=torch.long)

# 3. Draw computational diagram
graph = draw_graph(
    model,
    input_data={"input_features": input_features, "decoder_input_ids": decoder_input_ids},
    expand_nested=True,
    depth=8,  # Adjust depth (1 to 4) to control detail level
    roll=True,
    graph_name="whisper_tiny_architecture"
)

# 4. Save diagram to image file
graph.visual_graph.render("whisper_tiny_diagram", format="png")
print("Saved compute diagram to whisper_tiny_diagram.png")

import torch
from diffusers import StableDiffusionPipeline

# Use the Metal backend for Mac
device = "mps"
model_id = "runwayml/stable-diffusion-v1-5"

pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to(device)

prompt = "A cinematic photo of a robot drinking tea on Mars"
image = pipe(prompt).images[0]

image.save("output.png")
print("Image saved as output.png")
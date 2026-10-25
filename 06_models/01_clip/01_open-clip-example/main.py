import torch
from PIL import Image
import open_clip

# 1. Load the model and image preprocessing pipeline
model, _, preprocess = open_clip.create_model_and_transforms(
    'ViT-B-32', pretrained='laion2b_s34b_b79k'
)
model.eval()  # Set model to evaluation mode

# 2. Get the corresponding tokenizer
tokenizer = open_clip.get_tokenizer('ViT-B-32')

# 3. Preprocess the image
# Replace 'CLIP.png' with the path to your image file
image = preprocess(Image.open('CLIP.png')).unsqueeze(0)

# 4. Tokenize text labels
text = tokenizer(['a diagram', 'a dog', 'a cat'])

# 5. Extract features and compute similarities
with torch.no_grad(), torch.autocast('cuda' if torch.cuda.is_available() else 'cpu'):
  image_features = model.encode_image(image)
  text_features = model.encode_text(text)

  # Normalize features
  image_features /= image_features.norm(dim=-1, keepdim=True)
  text_features /= text_features.norm(dim=-1, keepdim=True)

  # Calculate cosine similarity and apply softmax to get probabilities
  text_probs = (100.0 * image_features @ text_features.T).softmax(dim=-1)

# 6. Print results
print('Label probabilities:', text_probs.cpu().numpy())
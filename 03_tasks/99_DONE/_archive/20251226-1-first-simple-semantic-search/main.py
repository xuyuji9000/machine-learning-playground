from sentence_transformers import SentenceTransformer, util
import torch

# 1. Load a pre-trained model
# 'all-MiniLM-L6-v2' is fast, lightweight, and great for general use
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Our "Database" of sentences
documents = [
    "The cat sits outside",
    "A man is eating pasta",
    "The new movie is awesome",
    "The sun is very bright today",
    "I love playing soccer",
    "Felines are interesting animals"
]

# 3. Encode the documents into embeddings
document_embeddings = model.encode(documents, convert_to_tensor=True)

def search(query):
    # 4. Encode the query
    query_embedding = model.encode(query, convert_to_tensor=True)

    # 5. Compute cosine similarity between query and all documents
    # cosine_scores will be a list of values between 0 and 1
    cosine_scores = util.cos_sim(query_embedding, document_embeddings)[0]

    # 6. Sort results by highest score
    top_results = torch.topk(cosine_scores, k=3)

    print(f"\nQuery: {query}")
    for score, idx in zip(top_results.values, top_results.indices):
        print(f"Score: {score:.4f} | {documents[idx]}")

# Test it out
search("Tell me about kittens")
search("What is for dinner?")
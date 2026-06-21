import gensim.downloader as api
from gensim.models import Word2Vec

def main():
    # 1. Load the text8 dataset
    # This will automatically download the 31MB dataset the first time you run it
    print("Loading Text8 dataset...")
    dataset = api.load("text8")

    # 2. Train the Word2Vec model
    # vector_size: Dimensionality of the word vectors
    # window: Maximum distance between the current and predicted word within a sentence
    # min_count: Ignores all words with total frequency lower than this
    # workers: Use these many worker threads to train the model (faster training)
    print("Training Word2Vec model...")
    model = Word2Vec(dataset, vector_size=100, window=5, min_count=5, workers=4)

    # 3. Save the model for later use (optional)
    model.save("word2vec_text8.model")
    print("Model saved to 'word2vec_text8.model'")

    # 4. Test the embeddings!
    print("\n--- Testing the Model ---")

    # Find similar words
    word = "king"
    print(f"Words most similar to '{word}':")
    for similar_word, similarity in model.wv.most_similar(word):
        print(f"  {similar_word}: {similarity:.4f}")

    # Perform word algebra: king - man + woman = queen
    print("\nAnalogy: king - man + woman = ?")
    result = model.wv.most_similar(positive=['king', 'woman'], negative=['man'], topn=1)
    print(f"  {result[0][0]}: {result[0][1]:.4f}")

if __name__ == "__main__":
    main()

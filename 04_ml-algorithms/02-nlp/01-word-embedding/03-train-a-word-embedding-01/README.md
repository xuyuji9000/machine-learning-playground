# Train a Word Embedding

This directory contains a simple Python script demonstrating how to train your own word embedding model using the `gensim` library and the `text8` dataset.

## Files 

- `train_text8_word2vec.py`: The main Python script that downloads the dataset, trains the model, saves it, and evaluates some basic word vector properties.
- `requirements.txt`: Python dependencies required to run the script.

## Prerequisites

Before running the script, install the required Python packages:

```bash
pip install -r requirements.txt
```

*(This project requires `gensim>=4.0.0`)*

## Usage

Run the training script using Python:

```bash
python train_text8_word2vec.py
```

## How it Works

The `train_text8_word2vec.py` script performs the following steps:

1. **Loads the `text8` dataset:** Automatically downloads the `text8` corpus using the `gensim.downloader` API. `text8` is a ~31MB dataset containing the first 100MB of cleaned Wikipedia text, making it perfect for quick word embedding training.
2. **Trains the Word Embedding Model:** Initializes and trains a word embedding model (specifically Word2Vec) on the corpus with the following hyperparameters:
   - `vector_size=100`: Dimensionality of the generated word vectors.
   - `window=5`: Maximum distance between the current and predicted word within a sentence.
   - `min_count=5`: Ignores all words with total frequency lower than 5.
   - `workers=4`: Uses 4 worker threads to speed up training.
3. **Saves the Model:** Saves the trained model to your local directory as `word2vec_text8.model` so it can be loaded and used later without retraining.
4. **Tests the Embeddings:** Performs a couple of quick evaluations to demonstrate that the model has learned semantic relationships:
   - **Similarity:** Finds words most similar to the word `"king"`.
   - **Word Algebra / Analogy:** Solves the classic semantic analogy equation: `king - man + woman = ?` (expecting results close to `"queen"`).

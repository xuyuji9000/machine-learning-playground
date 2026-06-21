# Open Source Text Corpora for Word Embeddings

Here is a summary of the open-source text corpora for training word embeddings, ordered roughly by size from largest to smallest.

| Corpus / Dataset | Estimated Tokens | Compressed Size | Uncompressed Size | Best Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **[RedPajama-V2](https://huggingface.co/datasets/togethercomputer/RedPajama-Data-V2)** | 30 Trillion | > 100 TB | Massive | Foundation LLM pre-training; industrial scale. |
| **[FineWeb](https://huggingface.co/datasets/HuggingFaceFW/fineweb)** | 15 - 18.5 Trillion | ~ 40 - 45 TB | > 100 TB | State-of-the-art web data for LLMs. |
| **[Dolma (AllenAI)](https://huggingface.co/datasets/allenai/dolma)** | 3 Trillion | ~ 4.5 TB | ~ 10 - 15 TB | Highly curated, multi-domain LLM training. |
| **[Common Corpus](https://huggingface.co/datasets/PleIAs/common_corpus)** | 2.27 Trillion | ~ 3 - 4 TB | ~ 10 TB | Largest fully open-licensed general text dataset. |
| **[C4 (Uncleaned English)](https://huggingface.co/datasets/allenai/c4)** | ~ 1 Trillion | 2.3 TB | ~ 6 TB | Massively diverse but noisy English web text. |
| **[C4 (Cleaned English)](https://huggingface.co/datasets/allenai/c4)** | ~ 160 Billion | 305 GB | ~ 750 GB | High-quality web text; great for robust embeddings. |
| **[The Pile](https://pile.eleuther.ai/)** | ~ 300 Billion | ~ 300 GB | 825 GB | High-quality, diverse academic & code vocabulary. |
| **[Wikipedia Dump (English)](https://dumps.wikimedia.org/enwiki/)** | ~ 4 Billion | ~ 20 - 25 GB | ~ 60 - 80 GB | The gold standard for clean, encyclopedic embeddings. |
| **[Project Gutenberg](https://www.gutenberg.org/)** | ~ 3 Billion | ~ 5 - 7 GB | ~ 15 - 20 GB | Literary, historical, and public domain vocabulary. |
| **[Fil9 (Wikipedia slice)](http://mattmahoney.net/dc/textdata.html)** | ~ 150 Million | 300 MB | 1 GB (10^9 bytes) | FastText tutorials and intermediate testing. |
| **[Text8 (Wikipedia slice)](http://mattmahoney.net/dc/textdata.html)** | ~ 17 Million | 30 MB | 100 MB (10^8 bytes) | "Hello World" dataset for quick local embedding tests. |

*Note: Token counts and exact sizes vary slightly depending on the specific tokenizer used, file formats (JSONL, Parquet, XML), and the date of the dataset snapshot.*
# Search Engine

This project provides a small Python helper for semantic search. It combines two stages:

1. Elasticsearch performs a fast fuzzy text search to find candidate documents.
2. A Sentence Transformer creates embeddings and cosine similarity chooses the best candidate.

The result is the matching document's `_source`, or `"No results found."` when the best score does not pass the configured threshold.

## Why two stages?

Elasticsearch is good at narrowing a large index quickly. Embedding-based ranking is good at recognizing that differently worded sentences can have similar meaning. Keeping retrieval and ranking separate makes the helper simple and lets Elasticsearch do the expensive index work first.

Use the navigation to learn how to install and configure the package, understand its architecture, and contribute changes.

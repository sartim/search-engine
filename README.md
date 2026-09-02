# Search Engine

Semantic search helpers using Sentence Transformers and Elasticsearch. The package first retrieves likely matches with Elasticsearch's fuzzy text query, then ranks those matches using cosine similarity between sentence embeddings.

## Install

```bash
python -m pip install .
```

## Quick start

```python
from search_engine import Search

search = Search(
    search_query="how do I reset my password?",
    search_field="content",
    es_url="https://user:password@localhost:9200",
    index="support-articles",
)
result = search.get_result()
```

See the [documentation](https://sartim.github.io/search-engine/) for configuration, development, and deployment details.

# Getting started

## Install the package

The project supports Python 3.9 and newer:

```bash
uv sync
```

The first real search downloads the configured Sentence Transformer model if it is not already cached. `Search` deliberately loads that model lazily, so importing the package does not incur model startup cost.

## Connect to Elasticsearch

Pass an Elasticsearch URL containing credentials when authentication is enabled:

```python
from search_engine import Search

search = Search(
    search_query="reset my password",
    search_field="content",
    es_url="https://username:password@example.test:9200",
    index="support-articles",
    similarity_score_threshold=0.8,
)

document = search.get_result()
```

Use environment variables or a secret manager for credentials in deployed applications. Do not commit a URL containing a password.

## Choose a model

The default model is `all-MiniLM-L6-v2`, a compact general-purpose sentence embedding model. A different compatible model can be selected per search instance:

```python
search = Search(
    search_query="semantic query",
    search_field="content",
    es_url="https://example.test:9200",
    index="documents",
    model_name="all-mpnet-base-v2",
)
```

## Understand the return value

`get_result()` returns the selected Elasticsearch `_source` dictionary. If Elasticsearch is unreachable, the index has no candidates, or the best similarity score is at or below the threshold, it returns `"No results found."`.

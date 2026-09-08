# API reference

## `Search`

```python
from search_engine import Search

search = Search(
    search_query="reset my password",
    search_field="content",
    es_url="https://example.test:9200",
    index="support-articles",
    similarity_score_threshold=0.8,
    model_name="all-MiniLM-L6-v2",
    device="cpu",
    batch_size=32,
    normalize_embeddings=False,
)
```

### `search(query=None)`

Runs a query and returns the matching Elasticsearch `_source` dictionary, or `None` when no candidate exceeds the threshold. Passing a query replaces the constructor query for that call without mutating the instance.

### `get_result()`

Compatibility method that runs the constructor query. New code can use `search()` for clearer query reuse.

### Model configuration

Pass a preloaded `model` to reuse an application-managed Sentence Transformer. Otherwise, models are cached by model name and device. The `semantic` extra is required when a real model is loaded.

## Exceptions

The client raises structured exceptions for operational failures:

- `InvalidElasticsearchURLError` — invalid or missing URL.
- `ElasticsearchConnectionError` — client creation or ping failure.
- `ElasticsearchSearchError` — query execution failure.

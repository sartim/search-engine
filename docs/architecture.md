# Architecture

```text
Search.get_result()
        |
        v
ElasticSearch.search_index()
        |
        v
Elasticsearch fuzzy match (up to 10 candidates)
        |
        v
Sentence Transformer embeddings
        |
        v
Cosine similarity + threshold
        |
        v
Best document _source / "No results found."
```

## `ElasticSearch`

`ElasticSearch` validates the URL, creates a client once, checks connectivity with `ping()`, and caches the client for later calls. `search_index()` sends a `match` query with `AUTO` fuzziness and an `or` operator, limiting the candidate set to ten documents.

## `Search`

`Search` extends `ElasticSearch` with semantic ranking. It embeds the query and each candidate's value for `search_field`, calculates cosine similarity, and returns the highest-scoring document only when it exceeds `similarity_score_threshold`.

## Index expectations

The configured `search_field` must exist as a text-like field in each candidate document. The helper does not create an index or mapping; those are deployment concerns and should be configured before searching.

For larger datasets, consider moving vector retrieval into Elasticsearch itself with a dense-vector field and approximate k-nearest-neighbor search. This package's two-stage approach is intentionally small and works well when the fuzzy candidate set is sufficient.

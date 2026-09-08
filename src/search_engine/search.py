from __future__ import annotations

from functools import lru_cache
from typing import Any

from search_engine.elasticsearch import ElasticSearch
from search_engine.types import SearchDocument

DEFAULT_MODEL_NAME = "all-MiniLM-L6-v2"


@lru_cache(maxsize=4)
def _load_model(model_name: str, device: str | None) -> Any:
    """Load and cache a small number of embedding models by name and device."""
    from sentence_transformers import SentenceTransformer

    kwargs = {} if device is None else {"device": device}
    return SentenceTransformer(model_name, **kwargs)


class Search(ElasticSearch):
    """Retrieve Elasticsearch candidates and rank them semantically."""

    def __init__(
        self,
        search_query: str,
        search_field: str,
        es_url: str,
        index: str,
        similarity_score_threshold: float = 0.8,
        model_name: str = DEFAULT_MODEL_NAME,
        model: Any | None = None,
        device: str | None = None,
        batch_size: int = 32,
        normalize_embeddings: bool = False,
        client: Any | None = None,
    ):
        super().__init__(es_url, index, client=client)
        if not -1 <= similarity_score_threshold <= 1:
            raise ValueError("similarity_score_threshold must be between -1 and 1")
        if batch_size < 1:
            raise ValueError("batch_size must be greater than zero")
        self.search_query = search_query
        self.search_field = search_field
        self.threshold = similarity_score_threshold
        self.model_name = model_name
        self.device = device
        self.batch_size = batch_size
        self.normalize_embeddings = normalize_embeddings
        self._model = model

    def _get_model(self) -> Any:
        """Load the embedding model only when a search is actually performed."""
        if self._model is None:
            self._model = _load_model(self.model_name, self.device)
        return self._model

    def get_result(self) -> SearchDocument | None:
        """Return the best match for the constructor query, if above threshold."""
        return self.search()

    def search(self, search_query: str | None = None) -> SearchDocument | None:
        """Return the best semantic match for a query, if above threshold."""
        query = self.search_query if search_query is None else search_query
        search_results = self.search_index(self.search_field, query)
        if not search_results:
            return None

        model = self._get_model()
        encode_kwargs = {
            "batch_size": self.batch_size,
            "convert_to_tensor": True,
            "normalize_embeddings": self.normalize_embeddings,
        }
        encoded_search_query = model.encode([query], **encode_kwargs)
        document_names = [item["_source"][self.search_field] for item in search_results]
        encoded_search_results = model.encode(document_names, **encode_kwargs)

        from sentence_transformers import util

        similarities = util.cos_sim(encoded_search_query, encoded_search_results)[0]
        best_match_index = int(similarities.argmax())
        best_match_similarity = float(similarities[best_match_index])
        if best_match_similarity > self.threshold:
            return search_results[best_match_index]["_source"]
        return None

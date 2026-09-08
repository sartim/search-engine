from __future__ import annotations

from functools import lru_cache
from typing import Any

from search_engine.elasticsearch import ElasticSearch

DEFAULT_MODEL_NAME = "all-MiniLM-L6-v2"


@lru_cache(maxsize=4)
def _load_model(model_name: str) -> Any:
    """Load and cache a small number of embedding models by name."""
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(model_name)


class Search(ElasticSearch):
    def __init__(self, search_query: str, search_field: str, es_url, index,
                 similarity_score_threshold: float = 0.8,
                 model_name: str = DEFAULT_MODEL_NAME,
                 model: Any | None = None):
        super().__init__(es_url, index)
        self.search_query = search_query
        self.search_field = search_field
        self.threshold = similarity_score_threshold
        self.model_name = model_name
        self._model = model

    def _get_model(self) -> Any:
        """Load the embedding model only when a search is actually performed."""
        if self._model is None:
            self._model = _load_model(self.model_name)
        return self._model

    def get_result(self) -> dict | None:
        return self.search()

    def search(self, search_query: str | None = None) -> dict | None:
        """Return the best semantic match for a query, if one exceeds the threshold."""
        query = self.search_query if search_query is None else search_query
        search_results: list[dict] = self.search_index(self.search_field, query)
        if not search_results:
            return None

        model = self._get_model()
        encoded_search_query = model.encode(
            [query], convert_to_tensor=True)
        document_names = [item["_source"][self.search_field] for item in search_results]
        encoded_search_results = model.encode(document_names, convert_to_tensor=True)

        from sentence_transformers import util

        similarities = util.cos_sim(encoded_search_query, encoded_search_results)[0]
        best_match_index = int(similarities.argmax())
        best_match_similarity = float(similarities[best_match_index])
        if best_match_similarity > self.threshold:
            best_match = search_results[best_match_index]
            return best_match["_source"]
        return None

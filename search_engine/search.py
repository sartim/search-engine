from typing import Any, List, Optional, Union

from search_engine.elasticsearch import ElasticSearch

DEFAULT_MODEL_NAME = "all-MiniLM-L6-v2"


class Search(ElasticSearch):
    def __init__(self, search_query: str, search_field: str, es_url, index,
                 similarity_score_threshold: float = 0.8,
                 model_name: str = DEFAULT_MODEL_NAME):
        super().__init__(es_url, index)
        self.search_query = search_query
        self.search_field = search_field
        self.threshold = similarity_score_threshold
        self.model_name = model_name
        self._model: Optional[Any] = None

    def _get_model(self) -> Any:
        """Load the embedding model only when a search is actually performed."""
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def get_result(self) -> Union[str, dict]:
        search_results: List[dict] = self.search_index(
            self.search_field, self.search_query)
        best_match_index: Optional[int] = None
        best_match_similarity: float = -1

        model = self._get_model()
        encoded_search_query = model.encode(
            [self.search_query], convert_to_tensor=True)

        for i, item in enumerate(search_results):
            _source = item['_source']
            document_name = _source[self.search_field]
            encoded_search_result = model.encode(
                [document_name], convert_to_tensor=True)
            from sentence_transformers import util
            similarity = util.cos_sim(
                encoded_search_query, encoded_search_result)[0][0]
            similarity_score = float(similarity)
            # Update the best match if the similarity is higher
            if similarity_score > best_match_similarity:
                best_match_similarity = similarity_score
                best_match_index = i

        if best_match_similarity > 0:
            best_match = search_results[best_match_index]
            result = best_match['_source']
            if best_match_similarity > self.threshold:
                return result
        return "No results found."

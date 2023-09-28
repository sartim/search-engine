from sentence_transformers import SentenceTransformer, util
from typing import List, Optional, Union

from search_engine.elasticsearch import ElasticSearch

model_name = 'bert-base-nli-mean-tokens'
model = SentenceTransformer(model_name)


class Search(ElasticSearch):
    def __init__(self, search_query: str, search_field: str, es_url, index,
                 similarity_score_threshold: float = 0.8):
        super().__init__(es_url, index)
        self.search_query = search_query
        self.search_field = search_field
        self.threshold = similarity_score_threshold

    def get_result(self) -> Union[str, dict]:
        search_results: List[dict] = self.search_index(
            self.search_field, self.search_query)
        best_match_index: Optional[int] = None
        best_match_similarity: float = -1

        encoded_search_query = model.encode(
            [self.search_query], convert_to_tensor=True)

        for i, item in enumerate(search_results):
            _source = item['_source']
            document_name = _source[self.search_field]
            encoded_search_result = model.encode(
                [document_name], convert_to_tensor=True)
            similarity = util.cos_sim(
                encoded_search_query, encoded_search_result)[0][0]
            # Update the best match if the similarity is higher
            if similarity > best_match_similarity:
                best_match_similarity = similarity
                best_match_index = i

        if best_match_similarity > 0:
            best_match = search_results[best_match_index]
            result = best_match['_source']
            if best_match_similarity > self.threshold:
                return result
        return "No results found."

from sentence_transformers import SentenceTransformer, util


model_name = 'bert-base-nli-mean-tokens'
model = SentenceTransformer(model_name)


class Search:
    def __init__(self, **kwargs):
        self.search_query = kwargs.get('search_query')
        self.search_field = kwargs.get('search_field')
        self.threshold = kwargs.get('similarity_score_threshold', 0.8)

    def get_result(self):
        search_results = []
        best_match_index = None
        best_match_similarity = -1

        encoded_search_query = model.encode(
            [self.search_query], convert_to_tensor=True
        )

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

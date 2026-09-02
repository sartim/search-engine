from search_engine.search import DEFAULT_MODEL_NAME, Search


def test_search_does_not_load_embedding_model_until_needed():
    search = Search("query", "content", "", "documents")

    assert search.model_name == DEFAULT_MODEL_NAME
    assert search._model is None

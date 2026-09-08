import sys
from types import SimpleNamespace

import pytest

from search_engine.elasticsearch import ElasticSearch
from search_engine.exceptions import InvalidElasticsearchURLError
from search_engine.search import DEFAULT_MODEL_NAME, Search


def test_search_does_not_load_embedding_model_until_needed():
    search = Search("query", "content", "", "documents")

    assert search.model_name == DEFAULT_MODEL_NAME
    assert search._model is None


def test_search_returns_none_without_candidates():
    search = Search("query", "content", "", "documents")
    search.search_index = lambda search_field, search_query: []

    assert search.get_result() is None
    assert search._model is None


def test_search_accepts_a_query_override():
    search = Search("initial", "content", "", "documents")
    captured = []

    def fake_search_index(search_field, search_query):
        captured.append((search_field, search_query))
        return []

    search.search_index = fake_search_index

    assert search.search("override") is None
    assert captured == [("content", "override")]


def test_search_batches_candidate_embeddings(monkeypatch):
    class FakeScores:
        def argmax(self):
            return 1

        def __getitem__(self, index):
            return 0.95 if index == 1 else self

    class FakeModel:
        def __init__(self):
            self.encoded = []

        def encode(self, values, **kwargs):
            self.encoded.append((values, kwargs))
            return values

    model = FakeModel()
    fake_util = SimpleNamespace(cos_sim=lambda query, candidates: FakeScores())
    fake_sentence_transformers = SimpleNamespace(util=fake_util)
    monkeypatch.setitem(sys.modules, "sentence_transformers", fake_sentence_transformers)

    search = Search("query", "content", "", "documents", model=model)
    search.search_index = lambda search_field, search_query: [
        {"_source": {"content": "first"}},
        {"_source": {"content": "second"}},
    ]

    assert search.get_result() == {"content": "second"}
    expected_kwargs = {
        "batch_size": 32,
        "convert_to_tensor": True,
        "normalize_embeddings": False,
    }
    assert model.encoded == [
        (["query"], expected_kwargs),
        (["first", "second"], expected_kwargs),
    ]


def test_search_rejects_invalid_threshold_and_batch_size():
    with pytest.raises(ValueError):
        Search("query", "content", "", "documents", similarity_score_threshold=2)
    with pytest.raises(ValueError):
        Search("query", "content", "", "documents", batch_size=0)


def test_invalid_elasticsearch_url_raises_structured_error():
    client = ElasticSearch("not-a-url", "documents")

    with pytest.raises(InvalidElasticsearchURLError):
        client.elasticsearch_conn()

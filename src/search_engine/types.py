"""Public and internal type definitions."""

from typing import Any, TypedDict

SearchDocument = dict[str, Any]


class ElasticsearchHit(TypedDict):
    """The subset of an Elasticsearch hit required by semantic ranking."""

    _source: SearchDocument

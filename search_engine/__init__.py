"""Semantic search helpers backed by Elasticsearch."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("search-engine")
except PackageNotFoundError:
    __version__ = "0.0.0"

from search_engine.search import Search

__all__ = ["Search", "__version__"]

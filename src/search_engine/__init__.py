"""Semantic search helpers backed by Elasticsearch."""

from importlib.metadata import PackageNotFoundError, version

from search_engine.search import Search

try:
    __version__ = version("search-engine")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = ["Search", "__version__"]

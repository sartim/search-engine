"""Exceptions raised by the search engine client."""


class SearchEngineError(RuntimeError):
    """Base class for expected search-engine failures."""


class InvalidElasticsearchURLError(SearchEngineError, ValueError):
    """Raised when the configured Elasticsearch URL is invalid."""


class ElasticsearchConnectionError(SearchEngineError):
    """Raised when Elasticsearch cannot be reached or fails its health check."""


class ElasticsearchSearchError(SearchEngineError):
    """Raised when Elasticsearch rejects or cannot execute a search."""

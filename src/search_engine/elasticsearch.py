from __future__ import annotations

import logging
from typing import Any, cast
from urllib.parse import unquote, urlsplit, urlunsplit

import certifi
from elasticsearch import Elasticsearch

from search_engine.exceptions import (
    ElasticsearchConnectionError,
    ElasticsearchSearchError,
    InvalidElasticsearchURLError,
)
from search_engine.types import ElasticsearchHit

es_log = logging.getLogger("elasticsearch")


class ElasticSearch:
    """Small Elasticsearch client wrapper with connection and query handling."""

    def __init__(self, es_url: str, index: str, client: Elasticsearch | None = None):
        self.es_url = es_url
        self.index = index
        self._client = client

    def elasticsearch_conn(self) -> Elasticsearch:
        """Return a cached client or raise a structured connection error."""
        if self._client is not None:
            return self._client
        if not self.es_url:
            raise InvalidElasticsearchURLError("An Elasticsearch URL is required")

        parsed = urlsplit(self.es_url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            raise InvalidElasticsearchURLError(
                "Elasticsearch URL must use http or https and include a hostname"
            )

        hostname = parsed.hostname
        if ":" in hostname and not hostname.startswith("["):
            hostname = f"[{hostname}]"
        if parsed.port:
            hostname = f"{hostname}:{parsed.port}"
        clean_url = urlunsplit((parsed.scheme, hostname, parsed.path, "", ""))
        kwargs: dict[str, Any] = {
            "ca_certs": certifi.where(),
            "request_timeout": 30,
        }
        if parsed.username is not None:
            kwargs["basic_auth"] = (
                unquote(parsed.username),
                unquote(parsed.password or ""),
            )

        try:
            client = Elasticsearch(clean_url, **kwargs)
            if not client.ping():
                raise ElasticsearchConnectionError(
                    f"Elasticsearch ping failed for {clean_url}"
                )
        except ElasticsearchConnectionError:
            raise
        except Exception as exc:
            es_log.exception("Could not connect to Elasticsearch at %s", clean_url)
            raise ElasticsearchConnectionError(
                f"Could not connect to Elasticsearch at {clean_url}"
            ) from exc

        self._client = client
        return client

    def search_index(self, search_field: str, search_query: str) -> list[ElasticsearchHit]:
        """Retrieve up to ten fuzzy candidates from Elasticsearch."""
        query = {
            "match": {
                search_field: {
                    "query": search_query,
                    "fuzziness": "AUTO",
                    "operator": "or",
                }
            }
        }
        client = self.elasticsearch_conn()
        try:
            es_log.info("Elasticsearch query: %s", query)
            search = client.search(index=self.index, query=query, size=10)
        except Exception as exc:
            es_log.exception("Elasticsearch search failed")
            raise ElasticsearchSearchError("Elasticsearch search failed") from exc
        return cast(list[ElasticsearchHit], search["hits"]["hits"])

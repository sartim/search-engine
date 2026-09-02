from __future__ import annotations

import logging
from typing import Any, cast
from urllib.parse import urlsplit, urlunsplit

import certifi
from elasticsearch import Elasticsearch

es_log = logging.getLogger("elasticsearch")
es_log.setLevel(logging.CRITICAL)


class ElasticSearch:
    def __init__(self, es_url: str, index: str):
        self.es_url = es_url
        self.index = index
        self._client: Elasticsearch | None = None

    def elasticsearch_conn(self) -> Elasticsearch | None:
        """Return a cached Elasticsearch client, or ``None`` if unavailable."""
        if self._client is not None:
            return self._client
        if not self.es_url:
            return None

        parsed = urlsplit(self.es_url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            es_log.error("Invalid Elasticsearch URL: %s", self.es_url)
            return None

        clean_url = urlunsplit((parsed.scheme, parsed.netloc.split("@")[-1], parsed.path, "", ""))
        kwargs: dict[str, Any] = {
            "ca_certs": certifi.where(),
            "request_timeout": 30,
        }
        if parsed.username is not None:
            kwargs["basic_auth"] = (parsed.username, parsed.password or "")

        try:
            client = Elasticsearch(clean_url, **kwargs)
            if not client.ping():
                es_log.error("Elasticsearch ping failed for %s", clean_url)
                return None
        except Exception:  # noqa: BLE001 - translate client errors to an unavailable client
            es_log.exception("Could not connect to Elasticsearch at %s", clean_url)
            return None

        self._client = client
        return self._client

    def search_index(
        self, search_field: str, search_query: str
    ) -> list[dict[str, Any]]:
        query = {
            "match": {
                search_field: {
                    "query": search_query,
                    "fuzziness": "AUTO",
                    "operator": "or"
                }
            }
        }

        client = self.elasticsearch_conn()
        if client is None:
            return []
        try:
            es_log.info("Elasticsearch query: %s", query)
            search = client.search(index=self.index, query=query, size=10)
        except Exception:  # noqa: BLE001 - keep search failures from breaking callers
            es_log.exception("Elasticsearch search failed")
            return []
        return cast(list[dict[str, Any]], search["hits"]["hits"])

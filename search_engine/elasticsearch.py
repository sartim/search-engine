import certifi
import re
import logging
import typing

from elasticsearch import Elasticsearch


es_log = logging.getLogger("elasticsearch")
es_log.setLevel(logging.CRITICAL)


class ElasticSearch:
    def __init__(self, es_url, index):
        self.es_url = es_url
        self.index = index

    def elasticsearch_conn(self) -> typing.Optional[Elasticsearch]:
        elasticsearch = None
        if self.es_url:
            auth = re.search(
                'https\:\/\/(.*)\@', self.es_url).group(1).split(':')
            host = self.es_url.replace('https://%s:%s@' % (auth[0], auth[1]), '')
            es_header = [{
                'host': host,
                'port': 443,
                'use_ssl': True,
                'timeout': 300,
                'http_auth': (auth[0], auth[1]),
                'ca_certs': certifi.where()
            }]
            elasticsearch = Elasticsearch(es_header)
            if not elasticsearch.ping():
                es_log.exception('Elasticsearch ping failed for connection')
                elasticsearch = None
        return elasticsearch

    def search_index(self, search_field, search_query) -> typing.List:
        query = {
            "match": {
                search_field: {
                    "query": search_query,
                    "fuzziness": "AUTO",
                    "operator": "or"
                }
            }
        }

        if not self.elasticsearch_conn():
            return []
        try:
            body = {
                'query': query,
                'size': 10
            }
            es_log.info("Elastic Search Query: \n{}".format(body))
            search = self.elasticsearch_conn().search(
                index=self.index, body=body)
            es_log.info("Elastic Search Response: \n{}".format(search))
        except Exception as e:
            es_log.error(str(e))
            return []
        else:
            return search['hits']['hits']



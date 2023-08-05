__ES_URL_KEY = "ES_URL"

class EsConfig:
    default_host = "localhost"
    default_port = 9200

    def __init__(self, url=None):
        import re
        result = re.search(
            "^(es://){0,1}([\d\.\:|]+)[/\?]*(.*)$", url)
        groups = result.groups()
        self.hosts = groups[1].split("|")
        self.params = dict([it.split('=')
                            for it in groups[2].split('&')]) if groups[2] else {}
        self.http_auth = (self.params["user"], self.params["password"])


def es_connect(url=None, cert_path="/es-cert"):
    if not url:
        from .zconfig import get_param
        url = get_param(__ES_URL_KEY)
    assert url

    from elasticsearch import Elasticsearch
    import os

    conf = EsConfig(url)
    client = Elasticsearch(
        hosts=conf.hosts, http_auth=conf.http_auth, verify_certs=True)
    return client

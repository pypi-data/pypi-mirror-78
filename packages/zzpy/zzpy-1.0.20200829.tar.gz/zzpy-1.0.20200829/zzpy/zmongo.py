__MONGO_URL_KEY = "MONGO_URL"


class MongoConfig:
    default_host = "localhost"
    default_port = 27017

    def __init__(self, url=None, host=None, port=None, database=None, param=None):
        import re
        if url:
            result = re.search(
                "^(mongodb://){0,1}([^:/]+)(:(\d+)){0,1}(/([^?]+)){0,1}(\?(.*)){0,1}", url)
            groups = result.groups()
            if not host:
                host = groups[1] if groups[1] else self.default_host
            if not port:
                port = int(groups[3]) if groups[3] else self.default_port
            if not database:
                database = groups[5] if groups[5] else None
            if not param:
                param = dict([it.split('=')
                              for it in groups[7].split('&')]) if groups[7] else {}
        self.url = url
        self.host = host
        self.port = port
        self.database = database
        self.param = param if param else {}

    def __eq__(self, value):
        return self.host == value.host and self.port == value.port and self.database == value.database and self.param == value.param


def mongo_connect(url=None):
    if not url:
        from .zconfig import get_param
        url = get_param(__MONGO_URL_KEY)
    assert url

    from pymongo import MongoClient
    import pytz

    conf = MongoConfig(url)
    client = MongoClient(host=conf.host, port=conf.port, tz_aware=True, tzinfo=pytz.timezone(
        'Asia/Shanghai'))
    if conf.database:
        client = client.get_database(conf.database)
    return client


def mongo_collection(client, collection):
    col = client
    for c in collection.split("."):
        col = col[c]
    return col


def main():
    assert MongoConfig(url="mongodb://a:1") == MongoConfig(host="a", port=1)


if __name__ == "__main__":
    main()

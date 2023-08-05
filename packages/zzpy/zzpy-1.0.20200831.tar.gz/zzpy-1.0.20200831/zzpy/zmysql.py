__MYSQL_URL_KEY = "MYSQL_URL"


class MySQLConfig:
    default_host = "localhost"
    default_port = 3306

    def __init__(self, url=None, host=None, port=None, database=None, param=None, user=None, password=None):
        import re
        if url:
            result = re.search(
                "^(mysql://){0,1}([^:/]+)(:(\d+)){0,1}(/([^?]*)){0,1}(\?(.*)){0,1}", url)
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
            if not user:
                user = param.get("user")
            if not password:
                password = param.get("password")

        self.url = url
        self.host = host
        self.port = port
        self.database = database
        self.param = param if param else {}
        self.user = user
        self.password = password

    def to_dict(self):
        d = {}
        if self.url is not None:
            d["url"] = self.url
        if self.host is not None:
            d["host"] = self.host
        if self.port is not None:
            d["port"] = self.port
        if self.database is not None:
            d["database"] = self.database
        if self.param is not None:
            d["param"] = self.param
        if self.user is not None:
            d["user"] = self.user
        if self.password is not None:
            d["password"] = self.password
        return d

    def __eq__(self, value):
        return self.host == value.host and self.port == value.port and self.database == value.database and self.param == value.param and self.user == value.user and self.password == value.password


def mysql_connect(url=None, autocommit=True):
    if not url:
        from .zconfig import get_param
        url = get_param(__MYSQL_URL_KEY)
    assert url

    import pymysql
    conf = MySQLConfig(url)

    client = pymysql.Connect(
        host=conf.host, port=conf.port, database=conf.database, user=conf.user, password=conf.password)
    client.autocommit(autocommit)
    return client


def mysql_query_one_value(client, sql):
    cursor = client.cursor()
    cursor.execute(sql)
    return cursor.fetchall()[0][0]


def mysql_query(client, sql):
    cursor = client.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def mysql_execute(client, sql):
    cursor = client.cursor()
    return cursor.execute(sql)


def mysql_insert(client, sql):
    cursor = client.cursor()
    res = cursor.execute(sql)
    return cursor.lastrowid if res else 0


def mysql_iter_table(client, table, fields=None, where_condition=None, offset_limit=None):
    if where_condition:
        if not where_condition.startswith("where") and not where_condition.startswith("WHERE"):
            where_condition = "where "+where_condition
    else:
        where_condition = ""
    if not offset_limit:
        offset_limit = ""
    if fields:
        fields = ",".join(f"`{i}`" for i in fields)
    else:
        fields = "*"
    sql = f"select {fields} from {table} {where_condition} {offset_limit}"
    from pymysql.cursors import SSDictCursor
    cursor = SSDictCursor(client)
    cursor.execute(sql)
    while True:
        item = cursor.fetchone()
        if not item:
            cursor.close()
            return
        yield item


def mysql_count_table(client, table, where_condition=None, offset_limit=None):
    if where_condition:
        if not where_condition.startswith("where") and not where_condition.startswith("WHERE"):
            where_condition = "where "+where_condition
    else:
        where_condition = ""
    if not offset_limit:
        offset_limit = ""
    sql = f"select count(*) from {table} {where_condition} {offset_limit}"
    return mysql_query_one_value(client, sql)


class ZMySQL:
    def __init__(self, url=None):
        self.client = mysql_connect(url=url)

    def execute(self, sql):
        return mysql_execute(self.client, sql)

    def insert(self, sql):
        return mysql_insert(self.client, sql)

    def query(self, sql):
        return mysql_query(self.client, sql)

    def query_one_value(self, sql):
        return mysql_query_one_value(self.client, sql)


def mysql_download_table(client, path, table, fields=None, where_condition=None, offset_limit=None, progress_title=None):
    import jsonlines
    import json
    from .zjson import jsondumps
    from .zprogress import pb

    with jsonlines.open(path, mode="w") as fw:
        iter = mysql_iter_table(client, table=table, fields=fields,
                                where_condition=where_condition, offset_limit=offset_limit)
        if progress_title:
            total = mysql_count_table(
                client, table=table, where_condition=where_condition, offset_limit=offset_limit)
            for item in pb(iter, total=total, title=progress_title):
                fw.write(json.loads(jsondumps(item)))
        else:
            for item in iter:
                fw.write(json.loads(jsondumps(item)))


def mysql_download_sql(client, path, sql, count_sql=None, progress_title=None):
    import jsonlines
    import json
    from .zjson import jsondumps
    from .zprogress import pb

    total = None
    if count_sql:
        total = mysql_query_one_value(client, count_sql)

    progress = None
    if progress_title:
        progress = pb(iterable=None, total=total, title=progress_title)

    with jsonlines.open(path, mode="w") as fw:
        from pymysql.cursors import SSDictCursor
        cursor = SSDictCursor(client)
        cursor.execute(sql)
        while True:
            item = cursor.fetchone()
            if not item:
                cursor.close()
                return
            fw.write(json.loads(jsondumps(item)))
            if progress is not None:
                progress.update()
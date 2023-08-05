import json
import datetime


class DateEncoder(json.JSONEncoder):
    """
    Json 无法解析 datatime 类型的数据，构建 DateEncoder 类解决 datatime 解析问题
    https://blog.csdn.net/yilovexing/article/details/93633436
    """

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return super.default(obj)
            # return json.JSONEncoder.default(self, obj)


def jsondumps(obj, *, skipkeys=False, ensure_ascii=True, check_circular=True,
              allow_nan=True, cls=None, indent=None, separators=None,
              default=None, sort_keys=False, **kw):
    if not cls:
        cls = DateEncoder
    return json.dumps(obj, skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular,
                      allow_nan=allow_nan, cls=cls, indent=indent, separators=separators,
                      default=default, sort_keys=sort_keys, **kw)


def main():
    print(jsondumps({"k": "v"}, indent=4))


if __name__ == "__main__":
    main()

def list_or_args(items, args):
    """COPY FROM redis.client.py"""
    # returns a single new list combining items and args
    try:
        iter(items)
        # a string or bytes instance can be iterated, but indicates
        # items wasn't passed as a list
        if isinstance(items, (str, bytes)):
            items = [items]
        else:
            items = list(items)
    except TypeError:
        items = [items]
    if args:
        items.extend(args)
    return items

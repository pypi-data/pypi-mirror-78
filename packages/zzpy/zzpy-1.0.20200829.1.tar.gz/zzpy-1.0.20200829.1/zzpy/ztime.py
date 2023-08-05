def get_date(days=0, separator='-'):
    import datetime
    return (datetime.datetime.now() + datetime.timedelta(days=days)).strftime(f"%Y{separator}%m{separator}%d")


def get_today(separator='-'):
    return get_date(days=0, separator=separator)


def get_month(months=0, separator='-'):
    """获取月份，如2019-10"""
    import arrow
    return arrow.now().shift(months=months).format(f"YYYY{separator}MM")

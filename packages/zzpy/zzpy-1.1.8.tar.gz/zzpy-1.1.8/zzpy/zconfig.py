def get_param(key, default_value=None, default_config_path='./config.json', local_config_path="./local-config.json"):
    """
    读取优先级: 环境变量 > 本地配置(./local-config.json) > 默认配置(./config.json) > 默认值(default_value)
    """
    import os
    from .zfile import read_file
    import json

    # 从环境变量读取
    value = os.environ.get(key)
    if value is not None:
        return value

    # 从本地配置读取
    try:
        config = json.loads(read_file(local_config_path))
        value = config.get(key)
        if value is not None:
            return value
    except Exception as ex:
        pass

    # 从默认配置配置读取
    try:
        config = json.loads(read_file(default_config_path))
        value = config.get(key)
        if value is not None:
            return value
    except Exception as ex:
        pass

    # 返回默认值
    return default_value

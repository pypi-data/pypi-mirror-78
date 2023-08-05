"""系统（Python解释器系统；操作系统等）"""


def is_windows():
    from .zdefinition import SystemPlatform
    import sys
    return sys.platform == SystemPlatform.Windows


def windows_else(windows_value, else_value):
    return windows_value if is_windows() else else_value

from importlib import import_module
from typing import Any


def dynamic_import(module, name):
    """Dynamically import a module and return the object by name."""
    return getattr(import_module(module), name)


def add_attribute(attr_name: str, attr_value: Any):
    """装饰器函数，为特定的函数添加相应的属性，第一个参数为属性名字，第二个参数为属性值"""

    def decorator(func):
        setattr(func, attr_name, attr_value)
        return func

    return decorator

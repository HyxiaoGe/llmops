from importlib import import_module


def dynamic_import(module, name):
    """Dynamically import a module and return the object by name."""
    return getattr(import_module(module), name)

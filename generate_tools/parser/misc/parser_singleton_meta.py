from pathlib import Path
from generate_tools.misc import SingletonMeta


class ParserSingletonMeta(SingletonMeta):
    def __setattr__(cls, name, value):
        if name == 'root':
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__()
                try:
                    cls._instances[cls].root = Path(value)
                except Exception as e:
                    raise e
        else:
            super().__setattr__(name, value)

    def __getattr__(cls, name):
        if cls not in cls._instances and name == "root":
            raise AttributeError("You must set source.root = ... for use this lib")
        try:
            return getattr(cls._instances[cls], name)
        except KeyError:
            raise AttributeError(f"'{cls.__class__.__name__}' object has no attribute '{name}'")

from functools import wraps
from typing import Any, List, Type
from seisbai_tools.eda.commands.command import Command
from seisbai_tools.pub_sub.pub_sub import PubSub
from seisbai_tools.types import Callback

_handlers: List[str] = []


def commandHandler(command: Type[Command]):
    def decorator(function: Callback):
        if command.__class__.__name__ in _handlers:
            raise RuntimeError(
                f"Cannot register handler {function.__name__} to {command.__class__.__name__}:"
                " this command already has one. "
                "Each command can have only a single handler."
            )
        else:
            _handlers.append(command.__class__.__name__)

        PubSub().subscribe(command.__class__.__name__, function)

        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any):
            return function(*args, **kwargs)

        return wrapper
    return decorator
from typing import List, Type
from ...eda.commands import Command
from ..utils.subscription_logic import apply_subscription_logic
from ...types import Callback

_handlers: List[str] = []


def CommandHandler(command: Type[Command]):
    def decorator(function: Callback):
        if command.__name__ in _handlers:
            raise RuntimeError(
                f"Cannot register handler {function.__name__} to {command.__name__}:"
                " this command already has one. "
                "Each command can have only a single handler."
            )
        else:
            _handlers.append(command.__name__)

        return apply_subscription_logic(command.__name__, function)
    return decorator
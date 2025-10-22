from functools import wraps
from typing import Any, Type
from seisbai_tools.eda.events.event import Event
from seisbai_tools.pub_sub.pub_sub import PubSub
from seisbai_tools.types import Callback


def eventListener(event: Type[Event]):
    def decorator(function: Callback):
        PubSub().subscribe(event.__class__.__name__, function)

        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any):
            return function(*args, **kwargs)

        return wrapper
    return decorator
from typing import Type
from seisbai_tools.eda.events.event import Event
from seisbai_tools.pub_sub.utils.subscription_logic import apply_subscription_logic
from seisbai_tools.types import Callback


def EventListener(event: Type[Event]):
    """Versão com restrição extra, mas que reutiliza Subscribe."""
    def decorator(function: Callback):
        return apply_subscription_logic(event.__name__, function)
    return decorator
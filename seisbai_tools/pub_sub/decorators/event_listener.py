from typing import Type
from ...eda.events import Event
from ..utils.subscription_logic import apply_subscription_logic
from ...types import Callback


def EventListener(event: Type[Event]):
    """Versão com restrição extra, mas que reutiliza Subscribe."""
    def decorator(function: Callback):
        return apply_subscription_logic(event.__name__, function)
    return decorator
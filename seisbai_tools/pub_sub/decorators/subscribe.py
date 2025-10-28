from ..utils.subscription_logic import apply_subscription_logic
from ...types import Callback


def Subscribe(topic: str):
    def decorator(function: Callback):
        return apply_subscription_logic(topic, function)
    return decorator
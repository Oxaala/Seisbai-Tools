
from functools import wraps
from inspect import signature
from seisbai_tools.pub_sub.pub_sub import PubSub
from seisbai_tools.types import Args, Callback, Kwargs


def Subscribe(topic: str):
    def decorator(function: Callback):
        
        params = list(signature(function).parameters.keys())
        is_method = bool(params and params[0] == "self")

        if is_method:
            function._event_topic = topic
            
            return function
        else:
            @wraps(function)
            
            def wrapper(*args: Args, **kwargs: Kwargs):
                return function(*args, **kwargs)
            
            PubSub().subscribe(topic, wrapper)
            
            return wrapper
    return decorator
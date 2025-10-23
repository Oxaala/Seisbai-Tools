from typing import Type, TypeVar
from seisbai_tools.pub_sub import PubSub
from seisbai_tools.types import Args, Callback, Kwargs

T = TypeVar("T")

def PubSubMethodAnnotation(cls: Type[T]):
    """
    Inscreve automaticamente métodos anotados com @eventListener no PubSub.
    Funciona para classes normais.
    """
    original_init = cls.__init__

    def __init__(self: T, *args: Args, **kwargs: Kwargs):
        original_init(self, *args, **kwargs)

        for attribute_name in dir(cls):
            attribute: Callback = getattr(cls, attribute_name)
            
            if callable(attribute) and hasattr(attribute, "_event_topic"):
                topic = getattr(attribute, "_event_topic")

                def wrapper(*args: Args, _attribute: Callback = attribute, **kwargs: Kwargs):
                    _attribute(self, *args, **kwargs)

                PubSub().subscribe(topic, wrapper)

    cls.__init__ = __init__
    
    return cls
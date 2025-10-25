from msgspec import Struct
from seisbai_tools.pub_sub.pub_sub import PubSub


class AutoPublishMixin:
    def __post_init__(self):
        super_post_init = getattr(super, "__post_init__", None)

        if callable(super_post_init):
            super_post_init()
        
        for _class in self.__class__.mro():
            if issubclass(_class, Struct) and _class is not Struct:
                PubSub().publish(_class.__name__, self)
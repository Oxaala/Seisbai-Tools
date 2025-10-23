from typing import Any, Dict, Optional, Tuple, Type, TypeVar
from seisbai_tools.pub_sub.pub_sub import PubSub
from seisbai_tools.types import Args, Callback, Kwargs
from seisbai_tools.utils.thread_with_loop import ThreadWithLoop

T = TypeVar("T")

def PubSubThread(cls: Type[T]) -> Type[T | ThreadWithLoop]:
    """Decorator que faz com que a instância da classe rode dentro de uma thread.

    Aceita todos os parâmetros padrão do construtor de `threading.Thread`.
    """
    class ThreadedWrapper(ThreadWithLoop):
        def __init__(
            self,
            group: Optional[Any] = None,
            name: Optional[str] = None,
            args: Tuple[Any, ...] = (),
            kwargs: Optional[Dict[str, Any]] = None,
            *,
            daemon: Optional[bool] = None,
            **extra_kwargs: Any,
        ):
            if kwargs is None:
                kwargs = {}

            super().__init__(group=group, name=name, daemon=daemon)

            self._init_args = args
            self._init_kwargs = {**kwargs, **extra_kwargs}
            self._instance: Optional[T] = None

            self.invoke(self._init_instance)

        def _init_instance(self):
            """Cria a instância real da classe dentro da thread."""
            self._instance = cls(*self._init_args, **self._init_kwargs)

            for attribute_name in dir(self._instance):
                attribute: Callback = getattr(self._instance, attribute_name)
                
                if callable(attribute) and hasattr(attribute, "_event_topic"):
                    topic = getattr(attribute, "_event_topic")

                    def wrapper(*args: Args, _attribute: Callback = attribute, **kwargs: Kwargs):
                        self.invoke(_attribute, *args, **kwargs)
                    
                    PubSub().subscribe(topic, wrapper)

        def __getattr__(self, name: str):
            """Intercepta métodos e os executa dentro da thread."""
            if not self._instance:
                raise AttributeError(f"Instance of {cls.__name__} has not been initialized yet.")

            attr: Callback | None = getattr(self._instance, name)

            if callable(attr):
                def wrapper(*args: Any, **kwargs: Any):
                    self.invoke(attr, *args, **kwargs)

                return wrapper
            
            return attr

    ThreadedWrapper.__name__ = f"{cls.__name__}Thread"
    
    return ThreadedWrapper
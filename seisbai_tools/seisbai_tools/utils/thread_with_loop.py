from queue import Empty, Queue
from threading import Event, Thread, current_thread
from typing import Any, Tuple, Dict

from seisbai_tools.types import Callback


class ThreadWithLoop(Thread):
    """Thread que possui um loop interno e permite invocar funções dentro dela."""
    _registry: Dict[int, "ThreadWithLoop"] = {}

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._queue: Queue[Tuple[Callback, Any, Any]] = Queue()
        self._event = Event()
        self._event.set()

    def run(self):
        """Executa o loop interno da thread."""
        if self.ident:
            ThreadWithLoop._registry[self.ident] = self
        
            try:
                self.__loop()
            finally:
                ThreadWithLoop._registry.pop(self.ident)

    def __loop(self):
        """Loop principal da thread."""
        while self._event.is_set():
            try:
                func, args, kwargs = self._queue.get(timeout=0.5)
                func(*args, **kwargs)
            except Empty:
                continue

    def invoke(self, func: Callback, *args: Any, **kwargs: Any):
        """Executa `func` dentro da thread atual (de forma assíncrona)."""
        self._queue.put((func, args, kwargs))

    def stop(self):
        """Para o loop e encerra a thread."""
        self._event.clear()

    @classmethod
    def get_current(cls) -> "ThreadWithLoop | None":
        """Retorna a instância registrada da thread atual, se houver."""
        thread_id = current_thread().ident
        
        if thread_id:
            return cls._registry.get(thread_id)
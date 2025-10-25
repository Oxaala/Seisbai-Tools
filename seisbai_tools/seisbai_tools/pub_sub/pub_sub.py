from queue import Queue
from threading import Event, Lock, Thread
from typing import Any, Dict, List, Self, Tuple, Union, cast
from weakref import WeakMethod

from seisbai_tools.types import Args, Callback, Kwargs

class CallbackDispatcher():
    def __init__(self, max_workers: int = 4) -> None:
        self._queue: Queue[Tuple[Callback, Args, Kwargs] | object] = Queue()
        self._worker = Thread(target = self._worker_loop, daemon = True)
        self._workers: List[Thread] = []
        self._sentinel = object()

        for i in range(max_workers):
            worker = Thread(target=self._worker_loop, name=f"CallbackDispatcher-{i}", daemon=True)
            worker.start()
            self._workers.append(worker)

    def dispatch(self, callback: Callback, *args: Args, **kwargs: Kwargs):
        self._queue.put((callback, args, kwargs))

    def _worker_loop(self):
        while True:
            try:
                item = self._queue.get()

                if item is self._sentinel:
                    self._queue.put(self._sentinel)
                    break

                callback, args, kwargs = cast(Tuple[Callback, Args, Kwargs], item)

                callback(*args, **kwargs)
            except Exception as error:
                print(f"[CallbackDispatcher] Error running {callback}: {error}")

    def stop(self):
        self._queue.put(self._sentinel)

        for worker in self._workers:
            worker.join(timeout=1)

_global_callback_dispatcher = CallbackDispatcher()

class PubSub():
    _instance = None
    _instance_lock = Lock()
    _subscribers: Dict[str, List[Union[Callback, WeakMethod[Any]]]]
    _lock: Lock
    _queue: Queue[Tuple[str, Args, Kwargs] | object]
    
    def __new__(cls, *args: Args, **kwargs: Kwargs) -> Self:
        with cls._instance_lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance._subscribers = {}
                cls._instance._lock = Lock()
                cls._queue = Queue()
                cls._sentinel = object()
                cls._dispatcher_thread = Thread(
                    target=cls._instance._process_events, name="PubSubProcessor", daemon=True
                )
                cls._instance._dispatcher_thread.start()

        return cls._instance

    def subscribe(self, topic: str, callback: Callback):
        if hasattr(callback, "__self__") and getattr(callback, "__self__") is not None:
            callback_reference = WeakMethod(callback)
        else:
            callback_reference = callback

        with self._lock:
            self._subscribers.setdefault(topic, []).append(callback_reference)

    def unsubscribe(self, topic: str, callback: Callback):
        with self._lock:
            if topic in self._subscribers:
                self._subscribers[topic] = [
                    callback_reference for callback_reference in self._subscribers[topic]
                    if not self._compare_callback(callback_reference, callback)
                ]

            if topic in self._subscribers and not self._subscribers[topic]:
                del self._subscribers[topic]

    def publish(self, topic: str, *args: Args, **kwargs: Kwargs):
        self._queue.put((topic, args, kwargs))

    def stop(self):
        self._queue.put(None)
        self._dispatcher_thread.join(timeout=1)
        _global_callback_dispatcher.stop()
        
    def _process_events(self):
        while True:
            item = self._queue.get()

            if item is self._sentinel:
                self._queue.put(self._sentinel)
                break

            topic, args, kwargs = cast(Tuple[str, Args, Kwargs], item)
            
            with self._lock:
                subscribers = self._subscribers.get(topic, []).copy()

            for callback_reference in subscribers:
                callback = self._resolve_callback(callback_reference)
                
                if callback:
                    _global_callback_dispatcher.dispatch(callback, *args, **kwargs)

    @staticmethod
    def _resolve_callback(cb_ref: Union[Callback, WeakMethod[Any]]) -> Union[Callback, None]:
        if isinstance(cb_ref, WeakMethod):
            return cb_ref()
        
        return cb_ref

    @staticmethod
    def _compare_callback(cb_ref: Union[Callback, WeakMethod[Any]], callback: Callback) -> bool:
        """Compara callback forte ou weakref"""
        resolved = PubSub._resolve_callback(cb_ref)
        
        return resolved is callback
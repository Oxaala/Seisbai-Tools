from concurrent.futures import ThreadPoolExecutor
from queue import Empty, Queue
from threading import Event, Lock, Thread
from typing import Any, Dict, List, Self, Tuple, Union
from weakref import WeakMethod

from seisbai_tools.types import Args, Callback, Kwargs

class ThreadDispatcher():
    def __init__(self) -> None:
        self._queue: Queue[Tuple[Callback, Args, Kwargs]] = Queue()
        self._executor = ThreadPoolExecutor(4)
        self._lock = Lock()

    def dispatch(self, callback: Callback, *args: Args, **kwargs: Kwargs):
        self._queue.put((callback, args, kwargs))
        self._executor.submit(self._run_callbacks)

    def _run_callbacks(self):
        with self._lock:
            while not self._queue.empty():   
                try:
                    callback, args, kwargs = self._queue.get_nowait()
                    callback(*args, **kwargs)
                except Empty:
                    break

    def stop(self):
        self._executor.shutdown()

_global_thread_dispatcher = ThreadDispatcher()

class PubSub():
    _instance = None
    _instance_lock = Lock()
    _subscribers: Dict[str, List[Union[Callback, WeakMethod[Any]]]]
    _lock: Lock
    _event_queue: Queue[Tuple[str, Args, Kwargs]]
    _stop_event: Event

    def __new__(cls, *args: Args, **kwargs: Kwargs) -> Self:
        with cls._instance_lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance._subscribers = {}
                cls._instance._lock = Lock()
                cls._event_queue = Queue()
                cls._stop_event = Event()
                cls._dispatcher_thread = Thread(
                    target=cls._instance._process_events, name="GlobalEventDispatcher", daemon=True
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
        self._event_queue.put((topic, args, kwargs))

    def stop(self):
        self._stop_event.set()
        self._dispatcher_thread.join(timeout=1)
        _global_thread_dispatcher.stop()
        
    def _process_events(self):
        while not self._stop_event.is_set():
            try:
                topic, args, kwargs = self._event_queue.get(timeout=0.5)
            except Empty:
                continue
            
            with self._lock:
                subscribers = list(self._subscribers.get(topic, []))

            for callback_reference in subscribers:
                callback = self._resolve_callback(callback_reference)
                
                if callback:
                    _global_thread_dispatcher.dispatch(callback, *args, **kwargs)

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
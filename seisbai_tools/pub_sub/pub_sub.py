from queue import Empty, Queue
from threading import Event, Lock, Thread, current_thread
from typing import Any, Dict, List, Self, Tuple

from seisbai_tools.types import Callback

class ThreadDispatcher():
    def __init__(self) -> None:
        self._queues: Dict[int, Queue[Tuple[Callback, Any, Any]]] = {}
        self._locks: Dict[int, Lock] = {}
        self._events: Dict[int, Event] = {}

    def register_thread(self, thread_id: int):
        if thread_id not in self._queues:
            self._queues[thread_id] = Queue()
            self._locks[thread_id] = Lock()
            self._events[thread_id] = Event()
            self._events[thread_id].set()

            loop_thread = Thread(
                target=self._loop, args=(thread_id,), name=f"Listener Thread - {thread_id}", daemon=True
            )
            loop_thread.start()

    def dispatch(self, thread_id: int, callback: Callback, *args: Any, **kwargs: Any):
        self.register_thread(thread_id)
        self._queues[thread_id].put((callback, args, kwargs))

    def _loop(self, thread_id: int):
        queue = self._queues[thread_id]
        event = self._events[thread_id]

        while event.is_set():
            try:
                callback, args, kwargs = queue.get(timeout=0.5)
                callback(*args, **kwargs)
            except Empty:
                continue

    def stop_thread(self, thread_id: int):
        if thread_id in self._events:
            self._events[thread_id].clear()


_global_thread_dispatcher = ThreadDispatcher()

class PubSub():
    _instance = None
    _instance_lock = Lock()
    _subscribers: Dict[str, List[Tuple[Callback, int]]]
    _lock: Lock
    _event_queue: Queue[Tuple[str, Any, Any]]

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        with cls._instance_lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance._subscribers = {}
                cls._instance._lock = Lock()
                cls._event_queue = Queue()
                cls._dispatcher_thread = Thread(
                    target=cls._instance._process_events, name="GlobalEventDispatcher", daemon=True
                )
                cls._instance._dispatcher_thread.start()

        return cls._instance

    def subscribe(self, topic: str, callback: Callback):
        thread_id = current_thread().ident

        if thread_id:
            with self._lock:
                self._subscribers.setdefault(topic, []).append((callback, thread_id))
        
            _global_thread_dispatcher.register_thread(thread_id)

    def unsubscribe(self, topic: str, callback: Callback):
        with self._lock:
            if topic in self._subscribers:
                self._subscribers[topic] = [(cb, ti) for cb, ti in self._subscribers[topic] if cb != callback]

                if not self._subscribers[topic]:
                    del self._subscribers[topic]

    def publish(self, topic: str, *args: Any, **kwargs: Any):
        self._event_queue.put((topic, args, kwargs))
        
    def _process_events(self):
        while True:
            try:
                topic, args, kwargs = self._event_queue.get(timeout=0.5)
            except Empty:
                continue
            
            with self._lock:
                subscribers = self._subscribers.get(topic, [])

            for callback, thread_id in subscribers:
                _global_thread_dispatcher.dispatch(thread_id, callback, *args, **kwargs)
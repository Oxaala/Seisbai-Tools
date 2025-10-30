from queue import Queue
from threading import Lock, Thread
from typing import Any, Dict, List, Optional, Self, Tuple, Union, cast
from uuid import UUID, uuid4
from weakref import WeakMethod
from concurrent.futures import ThreadPoolExecutor

from ..types import Args, Callback, Kwargs


class PubSub:
    _instance = None
    _instance_lock = Lock()
    _subscribers: Dict[str, List[Union[Callback, WeakMethod[Any]]]]
    _lock: Lock
    _queue: Queue[Tuple[str, Args, Kwargs] | object]
    _executor: ThreadPoolExecutor
    _dispatcher_thread: Thread
    _sentinel: object
    _session: UUID

    def __new__(cls, *args: Args, **kwargs: Kwargs) -> Self:
        with cls._instance_lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance._subscribers = {}
                cls._instance._lock = Lock()
                cls._instance._queue = Queue()
                cls._instance._sentinel = object()
                cls._instance._session = uuid4()
                cls._instance._executor = ThreadPoolExecutor(max_workers=4)
                cls._instance._dispatcher_thread = Thread(
                    target=cls._instance._process_events, name="PubSubProcessor", daemon=True
                )
                cls._instance._dispatcher_thread.start()

        return cls._instance

    def subscribe(self, topic: str, callback: Callback):
        cb_ref = WeakMethod(callback) if hasattr(callback, "__self__") else callback
        with self._lock:
            self._subscribers.setdefault(topic, []).append(cb_ref)

    def unsubscribe(self, topic: str, callback: Callback):
        with self._lock:
            if topic in self._subscribers:
                self._subscribers[topic] = [
                    cb_ref for cb_ref in self._subscribers[topic]
                    if not self._compare_callback(cb_ref, callback)
                ]
                if not self._subscribers[topic]:
                    del self._subscribers[topic]

    def publish(self, topic: str, *args: Args, **kwargs: Kwargs):
        self._queue.put((topic, args, kwargs))

    def stop(self):
        self._queue.put(self._sentinel)
        self._dispatcher_thread.join(timeout=1)
        self._executor.shutdown(wait=False)

    def session(self) -> UUID:
        return self._session

    def _process_events(self):
        while True:
            item = self._queue.get()
            
            if item is self._sentinel:
                break

            if item is None:
                continue

            topic, args, kwargs = cast(Tuple[str, Args, Kwargs], item)
            
            with self._lock:
                subscribers = self._subscribers.get(topic, []).copy()

            for cb_ref in subscribers:
                callback = self._resolve_callback(cb_ref)
                if callback:
                    # executa em thread pool para não travar o loop
                    self._executor.submit(self._safe_call, callback, *args, **kwargs)

    def _safe_call(self, callback: Callback, *args: Args, **kwargs: Kwargs):
        try:
            callback(*args, **kwargs)
        except Exception as error:
            print(f"[PubSub] Error running {callback}: {error}")

    @staticmethod
    def _resolve_callback(cb_ref: Union[Callback, WeakMethod[Any]]) -> Optional[Callback]:
        return cb_ref() if isinstance(cb_ref, WeakMethod) else cb_ref

    @staticmethod
    def _compare_callback(cb_ref: Union[Callback, WeakMethod[Any]], callback: Callback) -> bool:
        resolved = PubSub._resolve_callback(cb_ref)
        return resolved is callback
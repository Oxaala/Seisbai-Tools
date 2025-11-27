from concurrent.futures import Future, ThreadPoolExecutor
from datetime import UTC, datetime
from queue import Empty, Queue
from threading import Lock, Thread, Event
from time import sleep
from typing import Callable, Dict, List, Optional, Tuple
from uuid import UUID, uuid4

from ...utils import SingletonMeta
from .service_types import ServiceMetrics, ServiceStatus
from ..job import ManageableJob, JobStatus

ServiceStatusCallback = Optional[Dict[ServiceStatus, List[Callable[["ManageableService"], None]]]]
ServiceMetricsCallback = Optional[Callable[["ManageableService"], None]]


class ManageableService(metaclass = SingletonMeta):
    def __init__(
        self, 
        name: str,
        max_queue_size: int = 20, 
        max_workers: int = 4,
        status_callbacks: ServiceStatusCallback = None,
        metrics_callback: ServiceMetricsCallback = None
    ) -> None:
        self.__id = uuid4()
        self.__status = ServiceStatus.CREATED
        self.__max_workers = max_workers
        self.__max_queue_size = max_queue_size
        self.__lock = Lock()
        self.__status_callbacks = status_callbacks or {}
        self.__metrics_callback = metrics_callback
        self.__name = name

        self.__workers_available = Event()
        self.__workers_available.set()

        self.__pause_event = Event()
        self.__pause_event.set()

        self.__stop_event = Event()

        self.__job_queue = Queue[UUID](self.__max_queue_size)
        self.__jobs: Dict[UUID, Tuple[ManageableJob, Optional[Future[None]]]] = {}
        self.__active_jobs: List[UUID] = []

        self.__metrics_thread = Thread(target=self.__get_metrics, daemon=True)
        self.__metrics_thread.start()

        self.__job_queue_processor_thread = Thread(target=self.__process_job_queue, daemon=True)
        self.__job_queue_processor_thread.start()

        self.__job_executor = ThreadPoolExecutor(self.__max_workers)

        self.__start_time = datetime.now(tz=UTC)

    @property
    def status(self):
        return self.__status

    @property
    def metrics(self):
        return ServiceMetrics(
            name=self.__name,
            active_workers=len(self.__active_jobs),
            id=self.__id,
            max_queue_size=self.__max_queue_size,
            max_workers=self.__max_workers,
            queue_size=self.__job_queue.qsize(),
            start_time=self.__start_time,
        )

    def submit_job(self, job: ManageableJob):
        job.set_pending_status()

        self.__job_queue.put(job.id)
        self.__jobs[job.id] = (job, None)

    def check_if_job_is_running(self, job_id: UUID):
        return job_id in self.__active_jobs

    def remove_job(self, job_id: UUID):
        pair = self.__jobs.get(job_id)

        if not pair:
            raise ValueError(f"There's no job with id {job_id}!")

        job, _ = pair
        
        if job.status is JobStatus.RUNNING:
            raise ValueError("Can't remove a running job!")

        self.__remove_job_from_queue(job_id)
        self.__jobs.pop(job_id)

    def get_job(self, job_id: UUID) -> Tuple[ManageableJob, Optional[Future[None]]]:
        pair = self.__jobs.get(job_id)

        if not pair:
            raise ValueError(f"There's no job with id {job_id}!")

        job,future = pair

        return (job, future)

    def pause(self) -> None:
        if self.__status not in [ServiceStatus.STOPPED, ServiceStatus.FAILED]:
            self.__set_status(ServiceStatus.PAUSED)
            self.__pause_event.clear()

    def resume(self) -> None:
        if self.__status is ServiceStatus.PAUSED:
            self.__set_status(ServiceStatus.RUNNING)
            self.__pause_event.set()

    def stop(self) -> None:
        if self.__status not in [ServiceStatus.FAILED, ServiceStatus.STOPPED]:
            self.__stop_event.set()

            if self.__status is ServiceStatus.PAUSED:
                self.__pause_event.set()

            if len(self.__active_jobs) >= self.__max_workers:
                self.__workers_available.set()

            self.__set_status(ServiceStatus.STOPPED)
            self.__job_executor.shutdown()

    def __process_job_queue(self):
        self.__set_status(ServiceStatus.RUNNING)

        while not self.__stop_event.is_set():
            self.__pause_event.wait()

            self.__workers_available.wait()

            if self.__stop_event.is_set():
                break

            try:
                job_id = self.__job_queue.get(timeout=0.1)
            except Empty:
                continue

            job, _ = self.__jobs[job_id]

            if job.status is JobStatus.CANCELLED:
                continue

            future = self.__job_executor.submit(job.run)
            
            def _on_job_done(_: Future[None], job_id: UUID = job_id):
                with self.__lock:
                    if job_id in self.__active_jobs:
                        self.__active_jobs.remove(job_id)
                        self.__workers_available.set()

            future.add_done_callback(_on_job_done)

            self.__jobs[job_id] = (job, future)

            with self.__lock:
                self.__active_jobs.append(job_id)

            if len(self.__active_jobs) >= self.__max_workers:
                self.__workers_available.clear()
        
    def __get_metrics(self):
        while True:
            sleep(1)
            with self.__lock:
                active_jobs = self.__active_jobs.copy()

            for active_job in active_jobs:
                job, _ = self.__jobs[active_job]

                if job.metrics_callback:
                    job.metrics_callback(job.metrics)

                if self.__metrics_callback:
                    self.__metrics_callback(self)

    def __remove_job_from_queue(self, job_id: UUID):
        with self.__lock:
            ids: List[UUID] = []

            while not self.__job_queue.empty():
                id = self.__job_queue.get_nowait()
                
                if id != job_id:
                    ids.append(id)
            
            for id in ids:
                self.__job_queue.put(id)

    def __set_status(self, status: ServiceStatus):
        with self.__lock:
            self.__status = status

        if self.__status_callbacks:
            callback_list = self.__status_callbacks.get(self.__status)

            if callback_list:
                for callback in callback_list:
                    callback(self)
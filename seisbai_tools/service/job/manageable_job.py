from datetime import UTC, datetime
from threading import Event, Lock
import traceback
from typing import Callable, Dict, List, Optional
from uuid import uuid4

from .job_types import JobMetrics, JobStep, JobStatus

JobStatusCallback = Optional[Dict[JobStatus, List[Callable[["ManageableJob"], None]]]]
JobMetricsCallback = Optional[Callable[[JobMetrics], None]]


class ManageableJob:
    def __init__(
        self, 
        steps: List[JobStep], 
        status_callbacks: JobStatusCallback = None,
        metrics_callback: JobMetricsCallback = None
    ) -> None:
        self.__id = uuid4()

        self.__steps = steps
        self.__current_step_index = 0
        self.__total_steps = len(steps)
        self.__completed_steps = 0
        self.__current_step_name = self.__steps[self.__current_step_index].do.name
        self.__current_step_function_name = self.__steps[0].do.function_name
        self.__current_step_description = self.__steps[0].do.description

        self.__status = JobStatus.CREATED
        self.__end_time = None
        self.__lock = Lock()
        
        self.__error_type = None
        self.__error_message = None
        self.__error_stack_trace = None

        self.__pause_event = Event()
        self.__pause_event.set()
        self.__cancel_event = Event()

        self.__status_callbacks = status_callbacks or {}
        self.metrics_callback = metrics_callback

        self.__set_status(JobStatus.CREATED)

    @property
    def id(self):
        return self.__id

    @property
    def status(self) -> JobStatus:
        return self.__status

    @property
    def metrics(self):
        return JobMetrics(
            id=self.__id,
            current_step=self.__current_step_index + 1,
            current_step_name=self.__current_step_name,
            current_step_function_name=self.__current_step_function_name,
            current_step_description=self.__current_step_description,
            total_steps=self.__total_steps,
            completed_steps=self.__completed_steps,
            status=self.__status.name,
            start_time=self.__start_time,
            end_time=self.__end_time,
            error_type=self.__error_type,
            error_message=self.__error_message,
            error_stack_trace=self.__error_stack_trace
        )

    def set_pending_status(self) -> None:
        self.__set_status(JobStatus.PENDING)

    def run(self) -> None:
        if self.__status not in [JobStatus.PENDING, JobStatus.CREATED]:
            return

        self.__start_time = datetime.now(tz=UTC)
        self.__set_status(JobStatus.RUNNING)

        try:
            while not self.__cancel_event.is_set():
                self.__pause_event.wait()

                if self.__cancel_event.is_set():
                    break

                step = self.__steps[self.__current_step_index]

                try:
                    self.__current_step_name = step.do.name
                    self.__current_step_description = step.do.description
                    self.__current_step_function_name = step.do.function_name

                    step.do.function()
                    
                    self.__completed_steps += 1
                    self.__current_step_index += 1

                    self.__set_status(JobStatus.PROGRESS_UPDATED)
                except Exception as error:
                    self.__set_status(JobStatus.FAILED)
                    self.__end_time = datetime.now(tz=UTC)

                    self.__error_type = type(error).__name__
                    self.__error_message = f"Process failed at step {self.__current_step_name}: {error}"
                    self.__stack_trace = traceback.format_exc()
                    break

                if self.__current_step_index == len(self.__steps):
                    self.__set_status(
                        JobStatus.CANCELLED
                        if self.__cancel_event.is_set()
                        else JobStatus.COMPLETED
                    )
                    break
        finally:
            if not self.__end_time:
                self.__end_time = datetime.now(tz=UTC)

            if self.__status in [JobStatus.CANCELLED, JobStatus.FAILED]:
                self.__reverse_steps()

    def pause(self) -> None:
        if self.__status not in [JobStatus.PENDING, JobStatus.CANCELLED, JobStatus.COMPLETED, JobStatus.FAILED]:
            self.__set_status(JobStatus.PAUSED)
            self.__pause_event.clear()

    def resume(self) -> None:
        if self.__status is JobStatus.PAUSED:
            self.__set_status(JobStatus.RUNNING)
            self.__pause_event.set()

    def cancel(self) -> None:
        if self.__status not in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED]:
            self.__cancel_event.set()

            if self.__status is JobStatus.PAUSED:
                self.__pause_event.set()

            self.__set_status(JobStatus.CANCELLED)

    def __set_status(self, status: JobStatus):
        if status is not JobStatus.PROGRESS_UPDATED:
            with self.__lock:
                self.__status = status

        if self.__status_callbacks:
            callback_list = self.__status_callbacks.get(status)

            if callback_list:
                for callback in callback_list:
                    callback(self)

    def __reverse_steps(self):
        reversed_done_steps = self.__steps.copy()[:self.__current_step_index]

        reversed_done_steps.reverse()

        for step in reversed_done_steps:
            try:
                self.__current_step_name = step.undo.name
                self.__current_step_function_name = step.undo.function_name
                self.__current_step_description = step.undo.description
                
                step.undo.function()
            except Exception as error:
                self.__error_type = type(error).__name__
                self.__error_message = f"Rollback failed at step {self.__current_step_name}: {error}"
                self.__error_stack_trace = traceback.format_exc()
                break
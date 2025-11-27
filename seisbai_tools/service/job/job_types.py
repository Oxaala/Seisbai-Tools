from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from enum import Enum, auto
from typing import Callable
from uuid import UUID


@dataclass
class StepPart:
    name: str
    description: str
    function_name: str = field(init=False)
    function: Callable[..., None]

    def __post_init__(self) -> None:
        self.function_name = self.function.__name__

@dataclass
class JobStep:
    do: StepPart
    undo: StepPart

class JobStatus(Enum):
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()
    PAUSED = auto()
    CREATED = auto()
    PROGRESS_UPDATED = auto()

@dataclass
class JobMetrics:
    id: UUID
    current_step: int
    current_step_function_name: str
    current_step_name: str
    current_step_description: str
    total_steps: int
    completed_steps: int
    progress: float = (field(init=False))
    status: str
    start_time: datetime | None = None
    end_time: datetime | None = None
    error_type: str | None = None
    error_message: str | None = None
    error_stack_trace: str | None = None
    uptime: timedelta | None = field(init=False)
    elapsed_time: timedelta | None = field(init=False)
    eta: timedelta | None = field(init=False)
    last_step_duration: timedelta | None = None

    formatted_uptime: str = field(init=False, default="--:--:--")
    formatted_elapsed_time: str = field(init=False, default="--:--:--")
    formatted_eta: str = field(init=False, default="--:--:--")

    def __post_init__(self) -> None:
        self.progress = round((self.completed_steps / self.total_steps) * 100, 2)
        self.uptime = datetime.now(tz=UTC) - self.start_time if self.start_time else None
        self.elapsed_time = self.end_time - self.start_time if self.end_time and self.start_time else None

        if self.status is JobStatus.RUNNING.name and self.uptime:
            estimated_remaining_time = (self.uptime.total_seconds() * self.total_steps / self.current_step) - self.uptime.total_seconds()
            
            self.eta = timedelta(seconds=estimated_remaining_time)
        else:
            self.eta = None

        self.formatted_uptime = self._format_timedelta(self.uptime)
        self.formatted_elapsed_time = self._format_timedelta(self.elapsed_time)
        self.formatted_eta = self._format_timedelta(self.eta)

    @staticmethod
    def _format_timedelta(time_delta: timedelta | None) -> str:
        if not time_delta:
            return "00:00:00"

        total_seconds = int(time_delta.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        return f"{hours:02}:{minutes:02}:{seconds:02}"
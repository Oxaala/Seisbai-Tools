from dataclasses import dataclass, field
from datetime import UTC, timedelta, datetime
from enum import Enum, auto
from uuid import UUID


class ServiceStatus(Enum):
    RUNNING = auto()
    FAILED = auto()
    STOPPED = auto()
    PAUSED = auto()
    CREATED = auto()

@dataclass
class ServiceMetrics:
    name: str
    id: UUID
    queue_size: int
    max_queue_size: int
    active_workers: int
    max_workers: int
    start_time: datetime
    uptime: timedelta = field(init=False)

    def __post_init__(self) -> None:
        self.uptime = datetime.now(tz=UTC) - self.start_time

    @property
    def formatted_uptime(self) -> str:
        return self.format_timedelta(self.uptime)

    @staticmethod
    def format_timedelta(time_delta: timedelta | None) -> str:
        if not time_delta:
            return "--:--:--"

        total_seconds = time_delta.total_seconds()
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
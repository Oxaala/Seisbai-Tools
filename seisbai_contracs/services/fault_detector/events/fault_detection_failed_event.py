from typing import Optional
from uuid import UUID
from seisbai_contracs.core import Event


class FaultDetectionFailedEvent(Event, frozen=True, kw_only=True):
    dataset_id: UUID
    error_message: str
    stacktrace: Optional[str] = None
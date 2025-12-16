from typing import Callable
from enum import Enum

ProcessedBytes = int
TotalBytes = int

ProgressCallback = Callable[[ProcessedBytes, TotalBytes], None]

class SyncMode(str, Enum):
    PUSH = "push"
    PULL = "pull"
    BIDIRECTIONAL = "bidirectional"

from dataclasses import dataclass

@dataclass
class FileInfo:
    path: str
    size: int

# callback(event, processed, total)
SyncProgressCallback = Callable[[str, ProcessedBytes, TotalBytes], None]
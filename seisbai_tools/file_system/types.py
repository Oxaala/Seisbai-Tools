from typing import Callable

ProcessedBytes = int
TotalBytes = int

ProgressCallback = Callable[[ProcessedBytes, TotalBytes], None]
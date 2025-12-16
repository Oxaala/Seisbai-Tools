from typing import Callable
from enum import Enum
import os

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
    size: int # Bytes

    @property
    def filename(self) -> str:
        """Retorna apenas o nome do arquivo (ex: image.jpg)"""
        # Normaliza barras para garantir que o split funcione em qualquer OS
        clean_path = self.path.replace("\\", "/")
        return os.path.basename(clean_path)

    @property
    def directory(self) -> str:
        """Retorna apenas o caminho do diretório (ex: fotos/ferias)"""
        clean_path = self.path.replace("\\", "/")
        return os.path.dirname(clean_path)

# callback(event, processed, total)
SyncProgressCallback = Callable[[str, ProcessedBytes, TotalBytes], None]
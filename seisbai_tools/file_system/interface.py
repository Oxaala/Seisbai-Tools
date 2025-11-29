from abc import abstractmethod, ABC
from typing import Iterator, Optional
from .types import ProgressCallback

class FileSystemInterface(ABC):
    @abstractmethod
    def connect(self):
        ...

    @abstractmethod
    def upload(self, local_path: str, remote_path: str, progress: Optional[ProgressCallback] = None):
        ...

    @abstractmethod
    def download(self, remote_path: str, local_path: str, progress: Optional[ProgressCallback] = None):
        ...

    @abstractmethod
    def read_file_chunks(self, remote_path: str, chunk_size: int = 1024*1024,
                         progress: Optional[ProgressCallback] = None) -> Iterator[bytes]:
        ...

    @abstractmethod
    def listdir(self, path: str = "") -> list[str]:
        ...

    @abstractmethod
    def mkdir(self, path: str):
        ...

    @abstractmethod
    def delete(self, path: str):
        ...

    @abstractmethod
    def close(self):
        ...
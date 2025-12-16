from abc import abstractmethod, ABC
from typing import Iterator, Optional
from .types import ProgressCallback, SyncMode, SyncProgressCallback, FileInfo


class FileSystemInterface(ABC):
    @abstractmethod
    def connect(self):
        ...

    @abstractmethod
    def upload(
            self,
            local_path: str,
            remote_path: str,
            chunk_size: int,
            progress_callback: Optional[ProgressCallback]
    ):
        ...

    @abstractmethod
    def download(
            self,
            remote_path: str,
            local_path: str,
            chunk_size: int,
            progress_callback: Optional[ProgressCallback]
    ):
        ...

    @abstractmethod
    def read_file_chunks(
            self,
            remote_path: str,
            chunk_size: int,
            progress_callback: Optional[ProgressCallback]
    ) -> Iterator[bytes]:
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

    def list_files_recursive(self, base_path: str) -> dict[str, FileInfo]:
        ...

    @abstractmethod
    def sync(
        self,
        local_base: str,
        remote_base: str,
        mode: SyncMode = SyncMode.BIDIRECTIONAL,
        chunk_size: int = 1024 * 1024,
        progress: Optional[SyncProgressCallback] = None,
        dry_run: bool = False
):
        ...
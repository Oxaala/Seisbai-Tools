from typing import Optional, Iterator

from seisbai_tools.file_system.factory import FileSystemFactory
from seisbai_tools.file_system.interface import FileSystemInterface
from .types import ProgressCallback

class FileSystemManager(FileSystemInterface):
    def __init__(self, backend: str, **kwargs):
        self.client = FileSystemFactory.create(backend, **kwargs)

    def connect(self):
        self.client.connect()

    def upload(self, local_path: str, remote_path: str, progress: Optional[ProgressCallback] = None):
        self.client.upload(local_path, remote_path, progress)

    def download(self, remote_path: str, local_path: str, progress: Optional[ProgressCallback] = None):
        self.client.download(remote_path, local_path, progress)

    def read_file_chunks(self, remote_path: str, chunk_size: int = 1024*1024,
                         progress: Optional[ProgressCallback] = None) -> Iterator[bytes]:
        return self.client.read_file_chunks(remote_path, chunk_size, progress)

    def listdir(self, path: str = "") -> list[str]:
        return self.client.listdir(path)

    def mkdir(self, path: str):
        self.client.mkdir(path)

    def delete(self, path: str):
        self.client.delete(path)

    def close(self):
        self.client.close()
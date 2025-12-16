from typing import Optional, Iterator

from msgspec import Struct, field
from seisbai_tools.file_system.factory import FileSystemFactory
from seisbai_tools.file_system.interface import FileSystemInterface
from .types import ProgressCallback, SyncMode, SyncProgressCallback


# -------------------------------------------------
class FileSystemPathInfo(Struct, tag=True):
    user_hash: str = field(default="")
    project_folder: str = field(default="")
    file_name: str = field(default="")
    folder_name: str = field(default="")

    def build_path(self) -> str:
        """
        Constrói paths seguros ignorando campos vazios.
        """
        return "/".join(
            part for part in (
                self.user_hash,
                self.project_folder,
                self.folder_name,
                self.file_name,
            ) if part
        )


# -------------------------------------------------
class FileSystemManager(FileSystemInterface):
    """
    Fachada de alto nível para qualquer backend de filesystem.
    (NFS, SMB, S3, etc.)
    """

    def __init__(self, backend: str, **kwargs):
        self.client: FileSystemInterface = FileSystemFactory.create(
            backend, **kwargs
        )

    # -------------------------
    def connect(self):
        self.client.connect()

    def close(self):
        self.client.close()

    # -------------------------
    def upload(
        self,
        local_path: str,
        remote_path: str,
        chunk_size: int = 1024 * 1024,
        progress_callback: Optional[ProgressCallback] = None
    ):
        self.client.upload(
            local_path,
            remote_path,
            chunk_size,
            progress_callback
        )

    # -------------------------
    def download(
        self,
        remote_path: str,
        local_path: str,
        chunk_size: int = 1024 * 1024,
        progress_callback: Optional[ProgressCallback] = None
    ):
        self.client.download(
            remote_path,
            local_path,
            chunk_size,
            progress_callback
        )

    # -------------------------
    def read_file_chunks(
        self,
        remote_path: str,
        chunk_size: int = 1024 * 1024,
        progress_callback: Optional[ProgressCallback] = None
    ) -> Iterator[bytes]:
        return self.client.read_file_chunks(
            remote_path,
            chunk_size,
            progress_callback
        )

    # -------------------------
    def listdir(self, path: str = "") -> list[str]:
        return self.client.listdir(path)

    def mkdir(self, path: str):
        self.client.mkdir(path)

    def delete(self, path: str):
        self.client.delete(path)

    # -------------------------------------------------
    def sync(
        self,
        local_base: str,
        remote_base: str,
        mode: SyncMode = SyncMode.BIDIRECTIONAL,
        chunk_size: int = 1024 * 1024,
        progress: Optional[SyncProgressCallback] = None,
        dry_run: bool = False,
    ):
        """
        Sincroniza diretórios usando a implementação do backend.

        O FileSystemManager **não implementa lógica de sync**.
        Apenas delega para o client.
        """

        self.client.sync(
            local_base=local_base,
            remote_base=remote_base,
            mode=mode,
            chunk_size=chunk_size,
            progress=progress,
            dry_run=dry_run,
        )
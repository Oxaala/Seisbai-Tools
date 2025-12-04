import os
import shutil
from typing import Iterator, Optional

from ...interface import FileSystemInterface
from ...types import ProgressCallback


class NFSClient(FileSystemInterface):
    def __init__(self, mount_point: str):
        """
        mount_point: caminho local onde o NFS já está montado
        exemplo: /mnt/nfs ou /data dentro do container
        """
        self.mount_point = os.path.abspath(mount_point)
        self.connected = False

        if not os.path.exists(self.mount_point):
            raise RuntimeError(f"Mount point '{self.mount_point}' não existe")

    def connect(self):
        # valida se está acessível
        if not os.access(self.mount_point, os.R_OK | os.W_OK):
            raise RuntimeError(f"Sem permissão em {self.mount_point}")

        self.connected = True

    # -----------------------------
    def _full(self, path: str) -> str:
        return os.path.join(self.mount_point, path.lstrip("/"))

    # -----------------------------
    def upload(
        self,
        local_path: str,
        remote_path: str,
        chunk_size: int = 1024 * 1024,
        progress: Optional[ProgressCallback] = None
    ):
        if not self.connected:
            raise RuntimeError("Not connected")

        dst = self._full(remote_path)
        os.makedirs(os.path.dirname(dst), exist_ok=True)

        total_size = os.path.getsize(local_path)
        processed = 0

        with open(local_path, "rb") as src_file, open(dst, "wb") as dst_file:
            while chunk := src_file.read(chunk_size):
                dst_file.write(chunk)
                dst_file.flush()
                os.fsync(dst_file.fileno())
                processed += len(chunk)

                if progress:
                    progress(processed, total_size)

    # -----------------------------
    def download(
        self,
        remote_path: str,
        local_path: str,
        chunk_size: int = 1024 * 1024,
        progress: Optional[ProgressCallback] = None
    ):
        if not self.connected:
            raise RuntimeError("Not connected")

        src = self._full(remote_path)

        total_size = os.path.getsize(src)
        processed = 0

        dir_name = os.path.dirname(local_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        with open(src, "rb") as src_file, open(local_path, "wb") as dst_file:
            while chunk := src_file.read(chunk_size):
                dst_file.write(chunk)
                dst_file.flush()
                os.fsync(dst_file.fileno())
                processed += len(chunk)

                if progress:
                    progress(processed, total_size)

    # -----------------------------
    def listdir(self, path: str = ""):
        if not self.connected:
            raise RuntimeError("Not connected")
        return os.listdir(self._full(path))

    # -----------------------------
    def mkdir(self, path: str):
        if not self.connected:
            raise RuntimeError("Not connected")
        os.makedirs(self._full(path), exist_ok=True)

    # -----------------------------
    def delete(self, path: str):
        if not self.connected:
            raise RuntimeError("Not connected")

        full = self._full(path)
        if os.path.isdir(full):
            shutil.rmtree(full)
        elif os.path.exists(full):
            os.remove(full)

    # -----------------------------
    def read_file_chunks(
        self,
        remote_path: str,
        chunk_size: int = 1024 * 1024,
        progress: Optional[ProgressCallback] = None
    ) -> Iterator[bytes]:

        if not self.connected:
            raise RuntimeError("Not connected")

        full = self._full(remote_path)
        total_size = os.path.getsize(full)
        processed = 0

        with open(full, "rb") as f:
            while chunk := f.read(chunk_size):
                yield chunk
                processed += len(chunk)

                if progress:
                    progress(processed, total_size)

    # -----------------------------
    def close(self):
        self.connected = False
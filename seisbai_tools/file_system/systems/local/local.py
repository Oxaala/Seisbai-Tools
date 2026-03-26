import os
import shutil
import tempfile
import time
from typing import Dict, Iterator, Optional, List

from ...interface import FileSystemInterface
from ...types import ProgressCallback, SyncMode, SyncProgressCallback, RemoteFileInfo


class LocalClient(FileSystemInterface):
    def __init__(self, base_path: str = "."):
        self.base_path = os.path.abspath(base_path)
        self.connected = False

    # --------------------------------------------------
    # CONNECTION
    # --------------------------------------------------

    def connect(self):
        os.makedirs(self.base_path, exist_ok=True)
        if not os.access(self.base_path, os.R_OK | os.W_OK):
            raise RuntimeError(f"Sem permissão em {self.base_path}")
        self.connected = True

    def close(self):
        self.connected = False

    # --------------------------------------------------
    # INTERNAL
    # --------------------------------------------------

    def _full(self, path: str) -> str:
        if os.path.isabs(path):
            return os.path.abspath(path)
        return os.path.abspath(os.path.join(self.base_path, path.lstrip("/\\")))

    @staticmethod
    def _ensure_parent(path: str):
        parent = os.path.dirname(path)
        if parent:
            os.makedirs(parent, exist_ok=True)

    def _copy_atomic(
        self,
        src: str,
        dst: str,
        chunk_size: int,
        progress_callback: Optional[ProgressCallback] = None,
    ) -> None:
        self._ensure_parent(dst)

        total = os.path.getsize(src)
        processed = 0
        temp_fd = None
        temp_path = None

        try:
            temp_fd, temp_path = tempfile.mkstemp(
                prefix=".seisbai-transfer-",
                suffix=".tmp",
                dir=os.path.dirname(dst) or None,
            )
            os.close(temp_fd)
            temp_fd = None

            with open(src, "rb") as srcf, open(temp_path, "wb") as dstf:
                while chunk := srcf.read(chunk_size):
                    dstf.write(chunk)
                    processed += len(chunk)
                    if progress_callback:
                        progress_callback(processed, total)
                dstf.flush()
                os.fsync(dstf.fileno())

            # Em WSL/DrvFS, substituir um arquivo aberto por outro processo pode falhar
            # com EIO/EPERM; fazemos retry sem tocar no arquivo de destino original.
            last_error = None
            for _ in range(5):
                try:
                    os.replace(temp_path, dst)
                    temp_path = None
                    break
                except OSError as exc:
                    last_error = exc
                    time.sleep(0.2)
            else:
                raise last_error or OSError(f"Falha ao substituir arquivo de destino: {dst}")

            if total == 0 and progress_callback:
                progress_callback(0, 0)
        finally:
            if temp_fd is not None:
                try:
                    os.close(temp_fd)
                except OSError:
                    pass
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass

    # --------------------------------------------------
    # BASIC OPS
    # --------------------------------------------------

    def mkdir(self, path: str):
        if not self.connected:
            raise RuntimeError("Not connected")
        os.makedirs(self._full(path), exist_ok=True)

    def delete(self, path: str):
        if not self.connected:
            raise RuntimeError("Not connected")

        full = self._full(path)
        if os.path.isdir(full):
            shutil.rmtree(full)
        elif os.path.exists(full):
            os.remove(full)

    def listdir(self, path: str = ""):
        if not self.connected:
            raise RuntimeError("Not connected")
        return os.listdir(self._full(path))

    # --------------------------------------------------
    # TRANSFER
    # --------------------------------------------------

    def upload(
            self,
            local_path: str,
            remote_path: str,
            chunk_size: int = 1024 * 1024,
            progress_callback: Optional[ProgressCallback] = None
    ):
        if not self.connected:
            raise RuntimeError("Not connected")

        src = os.path.abspath(local_path)
        dst = self._full(remote_path)
        self._copy_atomic(src, dst, chunk_size, progress_callback)

    def download(
            self,
            remote_path: str,
            local_path: str,
            chunk_size: int = 1024 * 1024,
            progress_callback: Optional[ProgressCallback] = None
    ):
        if not self.connected:
            raise RuntimeError("Not connected")

        src = self._full(remote_path)
        dst = os.path.abspath(local_path)
        self._copy_atomic(src, dst, chunk_size, progress_callback)

    def read_file_chunks(
            self,
            remote_path: str,
            chunk_size: int = 1024 * 1024,
            progress_callback: Optional[ProgressCallback] = None
    ) -> Iterator[bytes]:
        if not self.connected:
            raise RuntimeError("Not connected")

        full = self._full(remote_path)
        total = os.path.getsize(full)
        processed = 0

        with open(full, "rb") as f:
            while chunk := f.read(chunk_size):
                processed += len(chunk)
                if progress_callback:
                    progress_callback(processed, total)
                yield chunk

    # --------------------------------------------------
    # RECURSIVE LIST
    # --------------------------------------------------

    def list_files_recursive(self, base_path: str) -> List[RemoteFileInfo]:
        if not self.connected:
            raise RuntimeError("Not connected")

        base = self._full(base_path)
        files: List[RemoteFileInfo] = []

        for root, _, filenames in os.walk(base):
            for name in filenames:
                full = os.path.join(root, name)
                rel = os.path.relpath(full, base).replace("\\", "/")
                try:
                    size = os.path.getsize(full)
                    files.append(RemoteFileInfo(path=rel, size_bytes=size))
                except OSError:
                    pass

        return files

    # --------------------------------------------------
    # SYNC
    # --------------------------------------------------

    def sync(
            self,
            local_base: str,
            remote_base: str,
            mode: SyncMode = SyncMode.BIDIRECTIONAL,
            chunk_size: int = 1024 * 1024,
            progress: Optional[SyncProgressCallback] = None,
            dry_run: bool = False
    ):
        if not self.connected:
            raise RuntimeError("Not connected")

        local_base = os.path.abspath(local_base)
        os.makedirs(local_base, exist_ok=True)

        local_files_map: Dict[str, int] = {}
        for root, _, files in os.walk(local_base):
            for f in files:
                full = os.path.join(root, f)
                rel = os.path.relpath(full, local_base).replace("\\", "/")
                local_files_map[rel] = os.path.getsize(full)

        remote_list = self.list_files_recursive(remote_base)
        remote_files_map: Dict[str, RemoteFileInfo] = {f.path: f for f in remote_list}

        def get_local_abs(rel_path: str) -> str:
            return os.path.join(local_base, rel_path.replace("/", os.sep))

        def get_remote_path(rel_path: str) -> str:
            base = remote_base.replace("\\", "/").strip("/")
            if base:
                return f"{base}/{rel_path}"
            return rel_path

        if mode in (SyncMode.PULL, SyncMode.BIDIRECTIONAL):
            for path, r_info in remote_files_map.items():
                local_size = local_files_map.get(path)
                if local_size is None or local_size != r_info.size_bytes:
                    if progress:
                        progress(f"download:{path}", 0, r_info.size_bytes)
                    if not dry_run:
                        self.download(
                            get_remote_path(path),
                            get_local_abs(path),
                            chunk_size,
                            lambda p, t, e=path: progress(f"download:{e}", p, t) if progress else None
                        )

        if mode in (SyncMode.PUSH, SyncMode.BIDIRECTIONAL):
            for path, l_size in local_files_map.items():
                r_info = remote_files_map.get(path)
                if r_info is None or r_info.size_bytes != l_size:
                    if progress:
                        progress(f"upload:{path}", 0, l_size)
                    if not dry_run:
                        self.upload(
                            get_local_abs(path),
                            get_remote_path(path),
                            chunk_size,
                            lambda p, t, e=path: progress(f"upload:{e}", p, t) if progress else None
                        )

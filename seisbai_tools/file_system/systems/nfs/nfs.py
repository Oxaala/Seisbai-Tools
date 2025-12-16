import os
import shutil
from typing import Iterator, Optional, Dict, List

# Importe apenas o RemoteFileInfo, esqueça o FileInfo
from ...interface import FileSystemInterface
from ...types import ProgressCallback, SyncMode, SyncProgressCallback, RemoteFileInfo


class NFSClient(FileSystemInterface):
    def __init__(self, mount_point: str):
        """
        mount_point: caminho local onde o NFS já está montado
        Ex: /mnt/nfs ou /data dentro do container
        """
        self.mount_point = os.path.abspath(mount_point)
        self.connected = False

        if not os.path.exists(self.mount_point):
            raise RuntimeError(f"Mount point '{self.mount_point}' não existe")

    # --------------------------------------------------
    # CONNECTION
    # --------------------------------------------------

    def connect(self):
        if not os.access(self.mount_point, os.R_OK | os.W_OK):
            raise RuntimeError(f"Sem permissão em {self.mount_point}")
        self.connected = True

    def close(self):
        self.connected = False

    # --------------------------------------------------
    # INTERNAL
    # --------------------------------------------------

    def _full(self, path: str) -> str:
        return os.path.join(self.mount_point, path.lstrip("/"))

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

        dst = self._full(remote_path)
        os.makedirs(os.path.dirname(dst), exist_ok=True)

        total = os.path.getsize(local_path)
        processed = 0

        with open(local_path, "rb") as src, open(dst, "wb") as dstf:
            while chunk := src.read(chunk_size):
                dstf.write(chunk)
                processed += len(chunk)
                if progress_callback:
                    progress_callback(processed, total)

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
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        total = os.path.getsize(src)
        processed = 0

        with open(src, "rb") as srcf, open(local_path, "wb") as dst:
            while chunk := srcf.read(chunk_size):
                dst.write(chunk)
                processed += len(chunk)
                if progress_callback:
                    progress_callback(processed, total)

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
        """
        Lista todos os arquivos abaixo de base_path (relativo ao mount_point).
        Retorna uma Lista de RemoteFileInfo.
        """
        if not self.connected:
            raise RuntimeError("Not connected")

        base = self._full(base_path)
        files: List[RemoteFileInfo] = []

        for root, _, filenames in os.walk(base):
            for name in filenames:
                full = os.path.join(root, name)
                # O replace garante consistência de caminhos
                rel = os.path.relpath(full, base).replace("\\", "/")

                try:
                    size = os.path.getsize(full)
                    # Usa RemoteFileInfo diretamente
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

        # 1. Mapeamento Local SIMPLIFICADO
        # Como removemos FileInfo, usamos um Dict simples: { "path": tamanho_int }
        local_files_map: Dict[str, int] = {}

        for root, _, files in os.walk(local_base):
            for f in files:
                full = os.path.join(root, f)
                rel = os.path.relpath(full, local_base).replace("\\", "/")
                local_files_map[rel] = os.path.getsize(full)

        # 2. Mapeamento Remoto (Usa RemoteFileInfo)
        remote_list = self.list_files_recursive(remote_base)
        remote_files_map: Dict[str, RemoteFileInfo] = {f.path: f for f in remote_list}

        def lp(p: str) -> str:
            return os.path.join(local_base, p)

        def rp(p: str) -> str:
            return os.path.join(remote_base, p).replace("\\", "/")

        # --- PULL (Remoto -> Local) ---
        if mode in (SyncMode.PULL, SyncMode.BIDIRECTIONAL):
            for path, r_info in remote_files_map.items():
                local_size = local_files_map.get(path)

                # Compara: Se não existe localmente (None) OU tamanho diferente
                if local_size is None or local_size != r_info.size_bytes:
                    if progress:
                        progress(f"download:{path}", 0, r_info.size_bytes)
                    if not dry_run:
                        self.download(
                            rp(path),
                            lp(path),
                            chunk_size,
                            lambda p, t, e=path:
                            progress(f"download:{e}", p, t) if progress else None
                        )

        # --- PUSH (Local -> Remoto) ---
        if mode in (SyncMode.PUSH, SyncMode.BIDIRECTIONAL):
            for path, l_size in local_files_map.items():
                r_info = remote_files_map.get(path)

                # Compara: Se não existe remotamente (None) OU tamanho diferente
                if r_info is None or r_info.size_bytes != l_size:
                    if progress:
                        progress(f"upload:{path}", 0, l_size)
                    if not dry_run:
                        self.upload(
                            lp(path),
                            rp(path),
                            chunk_size,
                            lambda p, t, e=path:
                            progress(f"upload:{e}", p, t) if progress else None
                        )
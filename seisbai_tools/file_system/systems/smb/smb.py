from typing import Iterator, Optional, Dict, List
from uuid import uuid4
import os

from smbprotocol.connection import Connection
from smbprotocol.session import Session
from smbprotocol.tree import TreeConnect
from smbprotocol.open import (
    Open,
    CreateDisposition,
    CreateOptions,
    ImpersonationLevel,
    FileAttributes,
    FilePipePrinterAccessMask,
    ShareAccess
)
from smbprotocol.file_info import FileInformationClass

# Mantenha os seus imports de tipos aqui
from seisbai_tools.file_system.interface import FileSystemInterface
from ...types import ProgressCallback, SyncMode, SyncProgressCallback, FileInfo

DEFAULT_IMPERSONATION = ImpersonationLevel.Impersonation
DEFAULT_DESIRED_ACCESS = (
        FilePipePrinterAccessMask.GENERIC_READ |
        FilePipePrinterAccessMask.GENERIC_WRITE
)
DEFAULT_FILE_ATTRS = FileAttributes.FILE_ATTRIBUTE_NORMAL
DEFAULT_SHARE_ACCESS = (
        ShareAccess.FILE_SHARE_READ |
        ShareAccess.FILE_SHARE_WRITE |
        ShareAccess.FILE_SHARE_DELETE
)

DIR_ACCESS_MASK = FilePipePrinterAccessMask.GENERIC_READ
DIR_ATTRS = FileAttributes.FILE_ATTRIBUTE_DIRECTORY
DIR_CREATE_OPTS = CreateOptions.FILE_DIRECTORY_FILE
FILE_CREATE_OPTS = CreateOptions.FILE_NON_DIRECTORY_FILE


class SMBClient(FileSystemInterface):

    def __init__(self, server, username, password, share, port=445):
        self.server = server
        self.username = username
        self.password = password
        self.share = share
        self.port = port

        self.connection: Connection | None = None
        self.session: Session | None = None
        self.tree: TreeConnect | None = None

    # --------------------------------------------------
    # CONNECTION
    # --------------------------------------------------

    def connect(self):
        self.connection = Connection(
            guid=uuid4(),
            server_name=self.server,
            port=self.port,
        )
        self.connection.connect()

        self.session = Session(
            connection=self.connection,
            username=self.username,
            password=self.password,
        )
        self.session.connect()

        share_path = fr"\\{self.server}\{self.share}"
        self.tree = TreeConnect(self.session, share_path)
        self.tree.connect()

    def close(self):
        if self.tree:
            self.tree.disconnect()
        if self.session:
            self.session.disconnect()
        if self.connection:
            self.connection.disconnect()

    # --------------------------------------------------
    # LOW LEVEL & HELPERS
    # --------------------------------------------------

    def _open_file(self, path: str, disposition, options):
        # Normalização crítica: SMB odeia '/'
        clean_path = path.replace("/", "\\").strip("\\")

        fh = Open(tree=self.tree, name=clean_path)
        fh.create(
            impersonation_level=DEFAULT_IMPERSONATION,
            desired_access=DEFAULT_DESIRED_ACCESS,
            file_attributes=DEFAULT_FILE_ATTRS,
            share_access=DEFAULT_SHARE_ACCESS,
            create_disposition=disposition,
            create_options=options,
        )
        return fh

    def _ensure_remote_dirs(self, path: str):
        path_norm = path.replace("\\", "/")
        parts = path_norm.strip("/").split("/")[:-1]

        current = ""
        for p in parts:
            current = f"{current}/{p}" if current else p
            try:
                self.mkdir(current)
            except Exception:
                pass

    def _decode_name(self, name_bytes) -> str:
        """
        Helper para decodificar nomes retornados pelo SMB.
        SMB geralmente usa UTF-16-LE.
        """
        if isinstance(name_bytes, bytes):
            try:
                # Tenta UTF-16 Little Endian (Padrão Windows/SMB)
                return name_bytes.decode("utf-16-le").rstrip('\x00')
            except UnicodeDecodeError:
                # Fallback para UTF-8 se falhar
                try:
                    return name_bytes.decode("utf-8").rstrip('\x00')
                except Exception:
                    return str(name_bytes)
        return str(name_bytes)

    # --------------------------------------------------
    # BASIC OPS
    # --------------------------------------------------

    def mkdir(self, path: str):
        fh = self._open_file(
            path,
            CreateDisposition.FILE_CREATE,
            DIR_CREATE_OPTS
        )
        fh.close()

    def delete(self, path: str):
        fh = self._open_file(
            path,
            CreateDisposition.FILE_OPEN,
            CreateOptions.FILE_DELETE_ON_CLOSE
        )
        fh.close()

    def listdir(self, path=""):
        fh = self._open_file(
            path,
            CreateDisposition.FILE_OPEN,
            DIR_CREATE_OPTS
        )

        try:
            entries = fh.query_directory(
                pattern="*",
                file_information_class=FileInformationClass.FILE_ID_BOTH_DIRECTORY_INFORMATION
            )
        finally:
            fh.close()

        result = []
        for e in entries:
            name = self._decode_name(e["file_name"].get_value())
            if name not in ('.', '..'):
                result.append(name)
        return result

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
        self._ensure_remote_dirs(remote_path)
        remote_path = remote_path.replace("/", "\\")

        with open(local_path, "rb") as f:
            data = f.read()

        fh = self._open_file(
            remote_path,
            CreateDisposition.FILE_OVERWRITE_IF,
            FILE_CREATE_OPTS
        )

        total = len(data)
        offset = 0

        try:
            while offset < total:
                size = min(chunk_size, total - offset)
                fh.write(data[offset:offset + size], offset)
                offset += size
                if progress_callback:
                    progress_callback(offset, total)
        finally:
            fh.close()

    def download(
            self,
            remote_path: str,
            local_path: str,
            chunk_size: int = 1024 * 1024,
            progress_callback: Optional[ProgressCallback] = None
    ):
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        remote_path = remote_path.replace("/", "\\")

        fh = self._open_file(
            remote_path,
            CreateDisposition.FILE_OPEN,
            FILE_CREATE_OPTS
        )

        size = fh.end_of_file
        offset = 0

        try:
            with open(local_path, "wb") as f:
                while offset < size:
                    length = min(chunk_size, size - offset)
                    data = fh.read(offset=offset, length=length)
                    f.write(data)
                    offset += len(data)
                    if progress_callback:
                        progress_callback(offset, size)
        finally:
            fh.close()

    def read_file_chunks(
            self,
            remote_path: str,
            chunk_size: int = 1024 * 1024,
            progress_callback: Optional[ProgressCallback] = None
    ) -> Iterator[bytes]:

        remote_path = remote_path.replace("/", "\\")

        fh = self._open_file(
            remote_path,
            CreateDisposition.FILE_OPEN,
            FILE_CREATE_OPTS
        )

        size = fh.end_of_file
        offset = 0

        try:
            while offset < size:
                length = min(chunk_size, size - offset)
                data = fh.read(offset=offset, length=length)
                if not data:
                    break
                offset += len(data)
                if progress_callback:
                    progress_callback(offset, size)
                yield data
        finally:
            fh.close()

    # --------------------------------------------------
    # RECURSIVE LIST (CORRIGIDO UTF-16)
    # --------------------------------------------------

    def list_files_recursive(self, base_path: str) -> List[FileInfo]:
        """
        Lista recursivamente arquivos e retorna uma Lista de objetos FileInfo.
        """
        files: List[FileInfo] = []  # Mudança: Agora é uma lista

        # Limpeza inicial do path base (SMB exige backslash)
        base_path_clean = base_path.replace("/", "\\").strip("\\")

        def walk(current_dir: str):
            try:
                fh = Open(tree=self.tree, name=current_dir)
                fh.create(
                    impersonation_level=DEFAULT_IMPERSONATION,
                    desired_access=DIR_ACCESS_MASK,
                    file_attributes=DIR_ATTRS,
                    share_access=DEFAULT_SHARE_ACCESS,
                    create_disposition=CreateDisposition.FILE_OPEN,
                    create_options=DIR_CREATE_OPTS,
                )
            except Exception as e:
                print(f"Aviso: Não foi possível acessar {current_dir}: {e}")
                return

            try:
                entries = fh.query_directory(
                    pattern="*",
                    file_information_class=FileInformationClass.FILE_ID_BOTH_DIRECTORY_INFORMATION
                )
            except Exception as e:
                print(f"Erro ao listar conteúdo de {current_dir}: {e}")
                fh.close()
                return

            fh.close()

            for entry in entries:
                # Decodifica nome (trata UTF-16)
                name = self._decode_name(entry["file_name"].get_value())

                if name in (".", ".."):
                    continue

                attrs = entry["file_attributes"].get_value()
                is_dir = (attrs & FileAttributes.FILE_ATTRIBUTE_DIRECTORY) == FileAttributes.FILE_ATTRIBUTE_DIRECTORY

                full_path_smb = f"{current_dir}\\{name}" if current_dir else name

                if is_dir:
                    walk(full_path_smb)
                else:
                    size = entry["end_of_file"].get_value()

                    # Calcula caminho relativo para armazenar no FileInfo
                    rel_path = full_path_smb
                    if base_path_clean and rel_path.startswith(base_path_clean):
                        # Remove a base + a barra seguinte
                        rel_path = rel_path[len(base_path_clean):].lstrip("\\")

                    # Padroniza para forward slash (/) para consistência interna
                    rel_key = rel_path.replace("\\", "/")

                    # Adiciona à lista
                    files.append(FileInfo(path=rel_key, size=size))

        walk(base_path_clean)
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
        local_base = os.path.abspath(local_base)
        os.makedirs(local_base, exist_ok=True)

        # --- 1. Mapeamento Local ---
        # Convertemos imediatamente para Dict para facilitar busca por chave (path)
        local_files_map: Dict[str, FileInfo] = {}
        for root, _, files in os.walk(local_base):
            for f in files:
                full_local = os.path.join(root, f)
                rel = os.path.relpath(full_local, local_base).replace("\\", "/")
                local_files_map[rel] = FileInfo(rel, os.path.getsize(full_local))

        # --- 2. Mapeamento Remoto ---
        # Recebemos uma List, mas convertemos para Dict para performance O(1)
        remote_list = self.list_files_recursive(remote_base)
        remote_files_map: Dict[str, FileInfo] = {f.path: f for f in remote_list}

        # Helpers de Path
        def get_local_abs(rel_p: str) -> str:
            return os.path.join(local_base, rel_p.replace("/", os.sep))

        def get_remote_abs(rel_p: str) -> str:
            clean_remote = remote_base.replace("/", "\\").strip("\\")
            clean_rel = rel_p.replace("/", "\\")
            if clean_remote:
                return f"{clean_remote}\\{clean_rel}"
            return clean_rel

        # --- PULL ---
        if mode in (SyncMode.PULL, SyncMode.BIDIRECTIONAL):
            # Iteramos sobre o MAPA remoto
            for path, r_info in remote_files_map.items():
                l_info = local_files_map.get(path)

                if not l_info or l_info.size != r_info.size:
                    if progress: progress(f"download:{path}", 0, r_info.size)
                    if not dry_run:
                        self.download(
                            get_remote_abs(path),
                            get_local_abs(path),
                            chunk_size,
                            lambda p, t, e=path: progress(f"download:{e}", p, t) if progress else None
                        )

        # --- PUSH ---
        if mode in (SyncMode.PUSH, SyncMode.BIDIRECTIONAL):
            for path, l_info in local_files_map.items():
                r_info = remote_files_map.get(path)

                if not r_info or r_info.size != l_info.size:
                    if progress: progress(f"upload:{path}", 0, l_info.size)
                    if not dry_run:
                        self.upload(
                            get_local_abs(path),
                            get_remote_abs(path),
                            chunk_size,
                            lambda p, t, e=path: progress(f"upload:{e}", p, t) if progress else None
                        )
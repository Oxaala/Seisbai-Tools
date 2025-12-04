from typing import Iterator, Optional
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

from seisbai_tools.file_system.interface import FileSystemInterface

from ...types import ProgressCallback

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

    # -------------------------
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
        self.tree = TreeConnect(
            session=self.session,
            share_name=share_path
        )
        self.tree.connect()

    # -------------------------
    def _open_file(self, path: str, disposition, options):
        fh = Open(tree=self.tree, name=path)
        fh.create(
            impersonation_level=DEFAULT_IMPERSONATION,
            desired_access=DEFAULT_DESIRED_ACCESS,
            file_attributes=DEFAULT_FILE_ATTRS,
            share_access=DEFAULT_SHARE_ACCESS,
            create_disposition=disposition,
            create_options=options,
        )
        return fh

    # -------------------------
    def upload(self, local_path: str, remote_path: str, chunk_size: int = 1024*1024,
               progress_callback: Optional[ProgressCallback] = None):
        with open(local_path, "rb") as f:
            data = f.read()

        fh = self._open_file(
            remote_path,
            CreateDisposition.FILE_OVERWRITE_IF,
            CreateOptions.FILE_NON_DIRECTORY_FILE
        )

        total = len(data)
        offset = 0
        while offset < total:
            to_write = min(chunk_size, total - offset)
            fh.write(data[offset:offset+to_write], offset)
            offset += to_write
            if progress_callback:
                progress_callback(offset, total)
        fh.close()

    # -------------------------
    def download(self, remote_path: str, local_path: str, chunk_size: int = 1024*1024,
                 progress_callback: Optional[ProgressCallback] = None):
        folder = os.path.dirname(local_path)

        if folder:
            os.makedirs(folder, exist_ok=True)

        fh = self._open_file(
            remote_path,
            CreateDisposition.FILE_OPEN,
            CreateOptions.FILE_NON_DIRECTORY_FILE
        )

        size = fh.end_of_file
        offset = 0
        with open(local_path, "wb") as f:
            while offset < size:
                to_read = min(chunk_size, size - offset)
                data = fh.read(offset=offset, length=to_read)
                f.write(data)
                offset += len(data)
                if progress_callback:
                    progress_callback(offset, size)
        fh.close()

    # -------------------------
    def read_file_chunks(self, remote_path: str, chunk_size: int = 1024*1024,
                         progress_callback: Optional[ProgressCallback] = None) -> Iterator[bytes]:
        fh = self._open_file(
            remote_path,
            CreateDisposition.FILE_OPEN,
            CreateOptions.FILE_NON_DIRECTORY_FILE
        )

        size = fh.end_of_file
        offset = 0
        try:
            while offset < size:
                to_read = min(chunk_size, size - offset)
                data = fh.read(offset=offset, length=to_read)
                if not data:
                    break
                offset += len(data)
                if progress_callback:
                    progress_callback(offset, size)
                yield data
        finally:
            fh.close()

    # -------------------------
    def listdir(self, path=""):
        fh = self._open_file(
            path,
            CreateDisposition.FILE_OPEN,
            CreateOptions.FILE_DIRECTORY_FILE
        )

        entries = fh.query_directory(
            pattern="*",
            file_information_class=FileInformationClass.FILE_ID_BOTH_DIRECTORY_INFORMATION
        )

        names = [entry["file_name"].get_value() for entry in entries]
        fh.close()
        return names

    # -------------------------
    def mkdir(self, path: str):
        fh = self._open_file(
            path,
            CreateDisposition.FILE_CREATE,
            CreateOptions.FILE_DIRECTORY_FILE
        )
        fh.close()

    # -------------------------
    def delete(self, path: str):
        fh = self._open_file(
            path,
            CreateDisposition.FILE_OPEN,
            CreateOptions.FILE_DELETE_ON_CLOSE
        )
        fh.close()

    # -------------------------
    def close(self):
        if self.tree:
            self.tree.disconnect()
        if self.session:
            self.session.disconnect()
        if self.connection:
            self.connection.disconnect()
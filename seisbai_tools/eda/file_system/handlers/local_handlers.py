import os
from typing import Callable

from seisbai_tools.eda.commands import Command
from seisbai_tools.eda.events import FailedEvent
from seisbai_tools.eda.file_system.commands import (
    CreateDirectoryCommand,
    DeleteFileCommand,
    ListFilesCommand,
    StartFileDownloadCommand,
    StartFileUploadCommand,
)
from seisbai_tools.eda.file_system.events import (
    DirectoryCreatedEvent,
    DirectoryCreationFailedEvent,
    DownloadCompletedEvent,
    DownloadFailedEvent,
    DownloadProgressUpdatedEvent,
    DownloadStartedEvent,
    FileDeletedEvent,
    FileDeletionFailedEvent,
    FilesListedEvent,
    UploadCompletedEvent,
    UploadFailedEvent,
    UploadProgressUpdatedEvent,
    UploadStartedEvent,
)
from seisbai_tools.file_system import FileSystemManager
from seisbai_tools.pub_sub.decorators import CommandHandler


def _is_local(fs_type: str) -> bool:
    return fs_type.strip().lower() == "local"


def _event_meta(command: Command) -> dict:
    return {
        "correlation_id": command.correlation_id or command.id,
        "causation_id": command.id,
    }


def _basename(path: str) -> str:
    normalized = (path or "").replace("\\", "/").rstrip("/")
    return normalized.split("/")[-1] if normalized else ""


def _remote_path(fs_path: str, target_path: str) -> str:
    if target_path and os.path.isabs(target_path):
        return target_path

    clean_base = (fs_path or "").strip()
    clean_target = (target_path or "").strip()

    if clean_base and clean_target:
        return os.path.join(clean_base, clean_target).replace("\\", "/")
    if clean_base:
        return clean_base.replace("\\", "/")
    return clean_target.replace("\\", "/")


def _base_path(fs_share: str) -> str:
    return fs_share or "."


def _resolve_local_storage_path(fs_share: str, remote_path: str) -> str:
    if os.path.isabs(remote_path):
        return os.path.abspath(remote_path)
    return os.path.abspath(os.path.join(os.path.abspath(_base_path(fs_share)), remote_path))


def _progress_value(processed: int, total: int) -> float:
    if total <= 0:
        return 100.0 if processed > 0 else 0.0
    return round((processed / total) * 100, 2)


def _upload_progress_callback(
    command: StartFileUploadCommand,
    file_name: str,
    meta: dict
) -> Callable[[int, int], None]:
    def callback(uploaded_bytes: int, total_bytes: int):
        UploadProgressUpdatedEvent(
            **meta,
            work_id=command.work_id,
            progress=_progress_value(uploaded_bytes, total_bytes),
            file_name=file_name,
            total_bytes=total_bytes,
            uploaded_bytes=uploaded_bytes,
        )
    return callback


def _download_progress_callback(
    command: StartFileDownloadCommand,
    file_name: str,
    meta: dict
) -> Callable[[int, int], None]:
    def callback(downloaded_bytes: int, total_bytes: int):
        DownloadProgressUpdatedEvent(
            **meta,
            work_id=command.work_id,
            progress=_progress_value(downloaded_bytes, total_bytes),
            file_name=file_name,
            total_bytes=total_bytes,
            downloaded_bytes=downloaded_bytes,
        )
    return callback


@CommandHandler(StartFileUploadCommand)
def handle_local_file_upload(command: StartFileUploadCommand):
    if not _is_local(command.fs_type):
        return

    meta = _event_meta(command)
    manager = FileSystemManager("local", base_path=_base_path(command.fs_share))
    destination_path = _remote_path(command.fs_path, command.remote_file_path)
    file_name = _basename(command.remote_file_path or command.local_file_path)

    try:
        total_bytes = os.path.getsize(os.path.abspath(command.local_file_path))

        UploadStartedEvent(
            **meta,
            work_id=command.work_id,
            title="Local file upload started",
            total_bytes=total_bytes,
            file_name=file_name,
        )

        manager.connect()
        manager.upload(
            local_path=command.local_file_path,
            remote_path=destination_path,
            progress_callback=_upload_progress_callback(command, file_name, meta),
        )

        UploadCompletedEvent(
            **meta,
            work_id=command.work_id,
            result={"remote_file_path": destination_path},
            file_name=file_name,
        )
    except Exception as error:
        UploadFailedEvent(
            **meta,
            work_id=command.work_id,
            reason=str(error),
            file_name=file_name,
        )
    finally:
        try:
            manager.close()
        except Exception:
            pass


@CommandHandler(StartFileDownloadCommand)
def handle_local_file_download(command: StartFileDownloadCommand):
    if not _is_local(command.fs_type):
        return

    meta = _event_meta(command)
    manager = FileSystemManager("local", base_path=_base_path(command.fs_share))
    source_path = _remote_path(command.fs_path, command.remote_file_path)
    file_name = _basename(command.remote_file_path or command.local_file_path)

    try:
        source_full_path = _resolve_local_storage_path(command.fs_share, source_path)
        total_bytes = os.path.getsize(source_full_path)

        DownloadStartedEvent(
            **meta,
            work_id=command.work_id,
            title="Local file download started",
            total_bytes=total_bytes,
            file_name=file_name,
        )

        manager.connect()
        manager.download(
            remote_path=source_path,
            local_path=command.local_file_path,
            progress_callback=_download_progress_callback(command, file_name, meta),
        )

        DownloadCompletedEvent(
            **meta,
            work_id=command.work_id,
            result={"local_file_path": command.local_file_path},
            file_name=file_name,
        )
    except Exception as error:
        DownloadFailedEvent(
            **meta,
            work_id=command.work_id,
            reason=str(error),
            file_name=file_name,
        )
    finally:
        try:
            manager.close()
        except Exception:
            pass


@CommandHandler(ListFilesCommand)
def handle_local_list_files(command: ListFilesCommand):
    if not _is_local(command.fs_type):
        return

    meta = _event_meta(command)
    manager = FileSystemManager("local", base_path=_base_path(command.fs_share))
    directory = _remote_path(command.fs_path, command.directory)

    try:
        manager.connect()
        files = manager.listdir(directory)
        FilesListedEvent(
            **meta,
            directory=directory,
            files=files,
        )
    except Exception as error:
        FailedEvent(
            **meta,
            work_id=command.work_id,
            reason=str(error),
        )
    finally:
        try:
            manager.close()
        except Exception:
            pass


@CommandHandler(DeleteFileCommand)
def handle_local_delete_file(command: DeleteFileCommand):
    if not _is_local(command.fs_type):
        return

    meta = _event_meta(command)
    manager = FileSystemManager("local", base_path=_base_path(command.fs_share))
    file_path = _remote_path(command.fs_path, command.remote_file_path)

    try:
        manager.connect()
        manager.delete(file_path)
        FileDeletedEvent(
            **meta,
            file_path=file_path,
        )
    except Exception as error:
        FileDeletionFailedEvent(
            **meta,
            work_id=command.work_id,
            reason=str(error),
            file_path=file_path,
        )
    finally:
        try:
            manager.close()
        except Exception:
            pass


@CommandHandler(CreateDirectoryCommand)
def handle_local_create_directory(command: CreateDirectoryCommand):
    if not _is_local(command.fs_type):
        return

    meta = _event_meta(command)
    manager = FileSystemManager("local", base_path=_base_path(command.fs_share))
    directory_path = _remote_path(command.fs_path, command.directory_path)

    try:
        manager.connect()
        manager.mkdir(directory_path)
        DirectoryCreatedEvent(
            **meta,
            directory_path=directory_path,
            directory_name=_basename(directory_path),
        )
    except Exception as error:
        DirectoryCreationFailedEvent(
            **meta,
            work_id=command.work_id,
            reason=str(error),
            directory_path=directory_path,
        )
    finally:
        try:
            manager.close()
        except Exception:
            pass

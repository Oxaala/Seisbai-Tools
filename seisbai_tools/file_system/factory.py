from seisbai_tools.file_system.interface import FileSystemInterface


class FileSystemFactory:
    @staticmethod
    def create(backend: str, **kwargs) -> FileSystemInterface:
        normalized_backend = backend.lower()

        if normalized_backend == "nfs":
            from .systems.nfs import NFSClient
            return NFSClient(**kwargs)  # ex: mount_point="/mnt/nfs"
        elif normalized_backend == "smb":
            from .systems.smb import SMBClient
            return SMBClient(**kwargs)  # ex: server="host", username="user", password="pass", share="share"
        elif normalized_backend == "local":
            from .systems.local import LocalClient
            return LocalClient(**kwargs)  # ex: base_path="./data"
        else:
            raise ValueError(f"Unknown service: {backend}")

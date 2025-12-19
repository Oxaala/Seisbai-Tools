from seisbai_tools.file_system.interface import FileSystemInterface


class FileSystemFactory:
    @staticmethod
    def create(backend: str, **kwargs) -> FileSystemInterface:
        if backend == "nfs":
            from .systems.nfs import NFSClient
            return NFSClient(**kwargs)  # ex: mount_point="/mnt/nfs"
        elif backend == "smb":
            from .systems.smb import SMBClient
            return SMBClient(**kwargs)  # ex: server="host", username="user", password="pass", share="share"
        else:
            raise ValueError(f"Unknown service: {backend}")
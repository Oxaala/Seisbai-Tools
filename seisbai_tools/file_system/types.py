from typing import Callable
from enum import Enum

ProcessedBytes = int
TotalBytes = int

ProgressCallback = Callable[[ProcessedBytes, TotalBytes], None]

class SyncMode(str, Enum):
    PUSH = "push"
    PULL = "pull"
    BIDIRECTIONAL = "bidirectional"

from dataclasses import dataclass, field


@dataclass
class RemoteFileInfo:
    """
    Representa informações de um arquivo remoto (SMB, NFS).
    Não depende de pathlib ou os.path para evitar problemas de compatibilidade de SO.

    Attributes:
        path (str): Caminho original (pode conter \ ou /).
        size_bytes (int): Tamanho em bytes.
        name (str): Nome do arquivo (sem extensão).
        extension (str): Extensão (ex: .txt).
        directory (str): Caminho da pasta onde o arquivo está.
        size (str): Tamanho formatado (ex: 1.5 MB).
    """
    path: str
    size_bytes: int

    name: str = field(init=False)
    extension: str = field(init=False)
    directory: str = field(init=False)
    size: str = field(init=False)

    def __post_init__(self):
        # 1. Normaliza para usar barras normais (/) internamente
        # Isso resolve o problema de caminhos SMB (\) no Linux
        clean_path = self.path.replace("\\", "/")

        # 2. Separa Diretório e Arquivo
        if "/" in clean_path:
            # Divide na última barra encontrada
            self.directory, filename = clean_path.rsplit("/", 1)
        else:
            # Se não tem barra, está na raiz
            self.directory = ""
            filename = clean_path

        # 3. Separa Nome e Extensão
        if "." in filename and not filename.startswith("."):
            self.name, ext = filename.rsplit(".", 1)
            self.extension = f".{ext}"
        else:
            self.name = filename
            self.extension = ""

        # 4. Formata o tamanho
        self.size = self._human_size(self.size_bytes)

    def _human_size(self, size: int) -> str:
        """Converte bytes para formato legível."""
        if size == 0:
            return "0 B"
        units = ["B", "KB", "MB", "GB", "TB", "PB"]
        i = 0
        current_size = float(size)
        while current_size >= 1024 and i < len(units) - 1:
            current_size /= 1024
            i += 1
        return f"{current_size:.2f} {units[i]}"

# callback(event, processed, total)
SyncProgressCallback = Callable[[str, ProcessedBytes, TotalBytes], None]
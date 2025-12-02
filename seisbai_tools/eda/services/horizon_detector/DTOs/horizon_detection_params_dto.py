from msgspec import Struct, field
from seisbai_tools.file_system.manager import FileSystemInfo


class HorizonDetectionParamsDTO(Struct, frozen=True, kw_only=True, tag=True):
    """
    Data Transfer Object (DTO) que encapsula os parâmetros necessários para executar
    o processo de detecção de horizontes sísmicos.

    Attributes
    ----------
    seismic : FileSystemInfo
        Caminho para o arquivo sísmico de entrada.

    model : FileSystemInfo
        Diretório onde o modelo está armazenado.

    mask : FileSystemInfo
        Caminho para a máscara utilizada na detecção.

    threshold : float
        Limiar mínimo de confiança para considerar a predição válida.

    eps : float
        Distância máxima (epsilon) para o algoritmo de clusterização.

    min_points : int
        Número mínimo de pontos para formar um cluster válido.

    output : FileSystemInfo
        Diretório onde os horizontes detectados serão salvos.
    """

    seismic: FileSystemInfo = field(default_factory=FileSystemInfo)
    model: FileSystemInfo = field(default_factory=FileSystemInfo)
    mask: FileSystemInfo = field(default_factory=FileSystemInfo)
    threshold: float = 0.1
    eps: float = 0.05
    min_points: int = 50
    output: FileSystemInfo = field(default_factory=FileSystemInfo)
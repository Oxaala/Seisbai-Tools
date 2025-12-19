from msgspec import Struct, field
from seisbai_tools.file_system.manager import FileSystemPathInfo


class HorizonDetectionParamsDTO(Struct, frozen=True, kw_only=True, tag=True):
    """
    Data Transfer Object (DTO) que reúne os parâmetros necessários para configurar
    e executar o processo de detecção de horizontes sísmicos.

    Attributes
    ----------
    seismic_path : FileSystemPathInfo
        Caminho para o volume sísmico de entrada (ex.: SEG-Y, HDF5 ou Zarr).

    model_path : FileSystemPathInfo
        Caminho para o modelo de inferência utilizado na detecção dos horizontes.

    mask_path : FileSystemPathInfo
        Caminho para a máscara opcional que restringe ou orienta a detecção
        (por exemplo, regiões de interesse ou zonas válidas do cubo).

    threshold : float, default=0.1
        Limiar mínimo de confiança para aceitar predições do modelo.

    eps : float, default=0.05
        Parâmetro epsilon usado pelo algoritmo de clusterização (ex.: DBSCAN)
        para agrupar pontos que compõem superfícies horizontais.

    min_points : int, default=50
        Quantidade mínima de pontos necessária para formar um cluster válido
        representando um horizonte.

    output_path : FileSystemPathInfo
        Diretório onde os horizontes detectados e artefatos intermediários serão salvos.
    """

    seismic_path: FileSystemPathInfo = field(default_factory=FileSystemPathInfo)
    model_path: FileSystemPathInfo = field(default_factory=FileSystemPathInfo)
    mask_path: FileSystemPathInfo = field(default_factory=FileSystemPathInfo)
    threshold: float = 0.1
    eps: float = 0.05
    min_points: int = 50
    output_path: FileSystemPathInfo = field(default_factory=FileSystemPathInfo)
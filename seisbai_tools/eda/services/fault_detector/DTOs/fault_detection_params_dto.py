from typing import Dict, List, Tuple
from msgspec import Struct, field

from seisbai_tools.file_system.manager import FileSystemPathInfo


class FaultDetectionParamsDTO(Struct, frozen=True, tag=True):
    """
    Data Transfer Object (DTO) que encapsula os parâmetros necessários
    para configurar e executar um job de detecção de falhas sísmicas.

    Este DTO descreve todas as entradas exigidas pelo worker responsável
    pelo processamento, incluindo caminhos dos arquivos, tamanho das janelas
    de inferência, step de deslizamento e a seleção opcional de eixos.

    Atributos
    ---------
    seismic_path : FileSystemPathInfo
        Caminho para o volume sísmico de entrada (SEG-Y, HDF5, Zarr etc.).

    model_path : FileSystemPathInfo
        Caminho para o modelo treinado utilizado na detecção de falhas.

    shape : tuple[int, int], default=(128, 128)
        Tamanho do recorte (janela) usado como entrada do modelo durante a
        inferência. Geralmente representa (altura, largura) da fatia sísmica.

    step : int, default=20
        Passo (stride) utilizado no deslizamento da janela pelo volume.
        Valores menores aumentam a precisão, porém elevam o custo computacional.

    axes : dict[str, list[int]]
        Seleção opcional de índices específicos do volume a serem processados.
        Espera-se um dicionário com as chaves:
            - "ilines": índices das linhas inline
            - "xlines": índices das linhas crossline
            - "depths": profundidades específicas
        Caso listas vazias sejam fornecidas, todo o volume será processado
        naquele eixo.

    output_path : FileSystemPathInfo
        Diretório ou caminho abstrato onde os resultados da detecção serão
        salvos, respeitando o backend do sistema de arquivos (local, SMB, S3 etc.).
    """

    seismic_path: FileSystemPathInfo = field(default_factory=FileSystemPathInfo)
    model_path: FileSystemPathInfo = field(default_factory=FileSystemPathInfo)

    shape: Tuple[int, int] = (128, 128)
    step: int = 20

    axes: Dict[str, List[int]] = field(
        default_factory=lambda: {
            "ilines": [],
            "xlines": [],
            "depths": [],
        }
    )

    output_path: FileSystemPathInfo = field(default_factory=FileSystemPathInfo)
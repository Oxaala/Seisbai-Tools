from typing import Optional, Sequence, Tuple, Union
from uuid import UUID, uuid4
from msgspec import Struct, field

from seisbai_tools.file_system.manager import FileSystemPathInfo
from ....commands import StartCommand
from ..DTOs import (
    GaussianDeformationParamsDTO,
    FaultDeformationParamsDTO,
    PlanarDeformationParamsDTO,
    SeismicCubeParamsDTO,
)


class TransformationStep(Struct, frozen=True, kw_only=True):
    """
    Representa uma etapa do pipeline de transformações aplicadas ao cubo sísmico.

    Cada transformação contém:
    - um identificador (`name`) que define sua categoria/implementação;
    - um DTO (`params`) contendo os parâmetros específicos da transformação.

    A estrutura é imutável (`frozen=True`) para garantir consistência durante a
    execução do pipeline de geração.

    Atributos
    ---------
    name : str
        Nome ou identificador da transformação (ex.: "gaussian", "fault", "planar").

    params : Union[GaussianDeformationParamsDTO, PlanarDeformationParamsDTO, FaultDeformationParamsDTO]
        Instância do DTO contendo os parâmetros específicos da transformação.
    """

    name: str
    params: Union[
        GaussianDeformationParamsDTO,
        PlanarDeformationParamsDTO,
        FaultDeformationParamsDTO,
    ]


class CreateSeismicCubeDatasetCommand(StartCommand, frozen=True, kw_only=True):
    """
    Comando que inicia a geração de um dataset de cubos sísmicos sintéticos.

    O comando integra o fluxo EDA (Event-Driven Architecture) do Seisbai,
    encapsulando todas as informações necessárias para que o worker responsável
    execute a geração, aplique transformações estruturais e armazene os resultados.

    Propósito
    ---------
    - Acionar o gerador de cubos sísmicos sintéticos.
    - Transportar parâmetros físicos, estruturais e operacionais.
    - Fornecer metadados (como seed e prefixo).
    - Definir o pipeline opcional de transformações após a geração.
    - Indicar o destino final dos arquivos (via `FileSystemPathInfo`).

    Atributos
    ---------
    dataset_id : UUID, default=uuid4()
        Identificador único para rastrear o job de geração do dataset.

    prefix : str, default="cube"
        Prefixo base utilizado para nomear os arquivos gerados.

    samples : int, default=1
        Número de cubos sísmicos a serem gerados.

    dimensions : Tuple[int, int, int], default=(128, 128, 128)
        Dimensões do cubo no formato:
            (inline, xline, depth)

    seed : Optional[int], default=None
        Semente para tornar o processo determinístico.

    output_path : FileSystemPathInfo
        Informações sobre o destino dos arquivos gerados
        (ex.: filesystem local, SMB, NFS, etc.).

    seismic_params : SeismicCubeParamsDTO
        Parâmetros geofísicos do modelo sísmico (velocidade, camadas,
        refletividade, frequência, sampling rate, etc.).

    transformations_pipeline : Sequence[TransformationStep], default=[]
        Lista ordenada de transformações aplicadas após a geração inicial
        do cubo sísmico.

    Exemplo
    -------
    >>> CreateSeismicCubeDatasetCommand(
    ...     samples=4,
    ...     seed=123,
    ...     dimensions=(256, 256, 256),
    ...     output_path=FileSystemPathInfo(path="/data/cubes"),
    ...     transformations_pipeline=[
    ...         TransformationStep(
    ...             name="gaussian",
    ...             params=GaussianDeformationParamsDTO(amplitude=2.0)
    ...         )
    ...     ]
    ... )
    """

    dataset_id: UUID = field(default_factory=lambda: uuid4())
    prefix: str = field(default="cube")
    samples: int = field(default=1)
    dimensions: Tuple[int, int, int] = field(default=(128, 128, 128))
    seed: Optional[int] = field(default=None)
    output_path: FileSystemPathInfo = field(default_factory=FileSystemPathInfo)

    seismic_params: SeismicCubeParamsDTO = field(
        default_factory=lambda: SeismicCubeParamsDTO(
            inline=128,
            xline=128,
            depth=128,
            alpha=0.35,
            beta=0.25,
            frequency=35.0,
            length=0.25,
            dt=0.002,
            velocity_min=1450,
            velocity_max=8000,
            layers=16,
        )
    )

    transformations_pipeline: Sequence[TransformationStep] = field(
        default_factory=list
    )
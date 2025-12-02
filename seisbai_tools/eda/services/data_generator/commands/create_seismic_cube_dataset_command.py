from typing import Optional, Sequence, Tuple, Union
from uuid import UUID, uuid4
from msgspec import Struct, field

from seisbai_tools.file_system.manager import FileSystemInfo
from ....commands import StartCommand
from ..DTOs import (
    GaussianDeformationParamsDTO,
    FaultDeformationParamsDTO,
    PlanarDeformationParamsDTO,
    SeismicCubeParamsDTO,
)


class TransformationStep(Struct, frozen=True, kw_only=True):
    """
    Representa uma única etapa de transformação aplicada ao cubo sísmico.

    Esta estrutura define um passo do pipeline de transformações aplicado
    ao cubo gerado. Cada transformação encapsula:

        1. Um identificador (`name`) que determina qual transformação será aplicada.
        2. Um objeto DTO (`params`) contendo parâmetros específicos da transformação.

    Ela é imutável (`frozen=True`), garantindo que a configuração do pipeline
    não seja alterada durante o processamento.

    ---
    Atributos
    ---------
    name : str
        Nome da transformação. Deve corresponder a um identificador suportado
        pelo pipeline de geração (ex.: "gaussian", "planar", "fault").
    params : Union[GaussianDeformationParamsDTO, PlanarDeformationParamsDTO, FaultDeformationParamsDTO]
        Objeto contendo os parâmetros específicos da transformação escolhida.
        Cada tipo de transformação possui seu próprio DTO especializado.
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

    Este comando integra o fluxo EDA (Event-Driven Architecture) do Seisbai e
    atua como ponto de entrada para o processo assíncrono de geração. Ele
    encapsula todos os parâmetros necessários para produzir e armazenar o
    conjunto de cubos sísmicos, incluindo dimensões, propriedades físicas,
    informações do sistema de arquivos e um pipeline opcional de transformações.

    ---
    Propósito
    ---------
    - Acionar o gerador de cubos sísmicos.
    - Transportar metadados necessários para os handlers e workers.
    - Definir parâmetros de reprodutibilidade (via seed).
    - Descrever transformações estruturais aplicadas ao cubo.

    ---
    Atributos
    ---------
    dataset_id : uuid.UUID, default=uuid4()
        Identificador único usado para correlacionar eventos produzidos durante
        a geração do dataset. Criado automaticamente caso não seja informado.

    prefix : str, default="cube"
        Prefixo usado ao nomear os arquivos gerados.

    samples : int, default=1
        Número de cubos sísmicos que serão gerados pelo pipeline.

    dimensions : Tuple[int, int, int], default=(128, 128, 128)
        Dimensões do cubo no formato:
            (inline, xline, depth)

    seed : Optional[int], default=None
        Semente utilizada para tornar o processo de geração determinístico.

    output : FileSystemInfo
        Informações sobre o destino da saída (local, SMB, S3 etc.).
        Permite abstrair diferentes backends de armazenamento.

    seismic_params : SeismicCubeParamsDTO
        Objeto DTO contendo parâmetros geofísicos do modelo sísmico, como:
        velocidade mínima/máxima, número de camadas, frequência da onda,
        parâmetros de refletividade, resolução temporal etc.

    transformations_pipeline : Sequence[TransformationStep], default=[]
        Pipeline sequencial de transformações aplicadas ao cubo após sua
        geração inicial. Cada transformação é definida por um `TransformationStep`.

    ---
    Uso
    ---
    Este comando normalmente é enviado para um **orquestrador EDA** que:

        - inicializa estruturas de rastreamento de progresso
        - dispara eventos `Started`, `Progress`, `Completed`, `Failed`
        - executa a geração do(s) cubo(s)
        - aplica o pipeline de transformações
        - salva resultados no sistema de arquivos desejado

    Exemplo
    -------
    >>> CreateSeismicCubeDatasetCommand(
    ...     samples=4,
    ...     seed=123,
    ...     dimensions=(256, 256, 256),
    ...     output=FileSystemInfo(path="/data/cubes"),
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
    output: FileSystemInfo = field(default_factory=FileSystemInfo)

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
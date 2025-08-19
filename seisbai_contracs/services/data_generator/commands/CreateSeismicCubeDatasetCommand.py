from typing import Optional, Sequence, Tuple, Union
from uuid import UUID, uuid4
from msgspec import Struct, field
from seisbai_contracs.core import Command
from DTOs import SeismicCubeParamsDTO, GaussianDeformationParamsDTO, FaultDeformationParamsDTO, PlanarDeformationParamsDTO


class TransformationStep(Struct, frozen=True):
    """
    Representa uma etapa de transformação a ser aplicada no cubo sísmico.

    Attributes
    ----------
    name : str
        Nome da transformação a ser aplicada. Deve corresponder a um dos
        identificadores válidos definidos no pipeline de geração.
    params : Union[GaussianDeformationParamsDTO, PlanarDeformationParamsDTO, FaultDeformationParamsDTO]
        Objeto DTO contendo os parâmetros específicos da transformação.
    """

    name: str
    params: Union[
        GaussianDeformationParamsDTO,
        PlanarDeformationParamsDTO,
        FaultDeformationParamsDTO,
    ]


class CreateSeismicCubeDatasetCommand(Command, frozen=True):
    """
    Comando que inicia a geração de um dataset de cubos sísmicos sintéticos.

    Esse comando encapsula tanto os parâmetros operacionais (como diretório de
    saída, dimensões e seed) quanto os parâmetros geológicos/sísmicos e um
    pipeline opcional de transformações a serem aplicadas ao modelo.

    Attributes
    ----------
    dataset_id : uuid.UUID
        Identificador único do dataset (usado para correlação entre eventos).
        Gerado automaticamente se não for fornecido.
    output_dir : str, default="output"
        Diretório de saída onde os arquivos gerados serão salvos.
    prefix : str, default="cube"
        Prefixo usado para nomear os arquivos do dataset.
    samples : int, default=1
        Número de amostras (cubos) a serem gerados.
    dimensions : Tuple[int, int, int], default=(128, 128, 128)
        Dimensões do cubo sísmico no formato (inline, xline, depth).
    seed : Optional[int], default=None
        Semente do gerador aleatório para garantir reprodutibilidade.
    seismic_params : SeismicCubeParamsDTO
        Parâmetros físicos/geológicos utilizados pelo gerador de cubos sísmicos.
    transformations_pipeline : Sequence[TransformationStep], default=[]
        Pipeline opcional de transformações (deformações, falhas, ruído etc.)
        aplicadas sequencialmente ao cubo gerado.
    """

    dataset_id: UUID = field(default_factory=lambda: uuid4())
    output_dir: str = field(default="output")
    prefix: str = field(default="cube")
    samples: int = field(default=1)
    dimensions: Tuple[int, int, int] = field(default=(128, 128, 128))
    seed: Optional[int] = field(default=None)

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

    transformations_pipeline: Sequence[TransformationStep] = field(default_factory=list[TransformationStep])
from typing import Optional, Tuple
from uuid import UUID
from seisbai_contracts.core.artefacts.events.started import StartedEvent


class SeismicCubeDatasetGenerationStartedEvent(StartedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando a geração de um dataset de cubo sísmico é iniciada.

    Esse evento é disparado no início do processo de geração, fornecendo
    informações sobre o dataset, o diretório de saída, prefixo, número de amostras
    e dimensões do cubo sísmico.

    Attributes
    ----------
    dataset_id : UUID
        Identificador único do dataset que está sendo gerado.
    output_dir : str
        Diretório onde os arquivos gerados serão armazenados.
    prefix : Optional[str], default=None
        Prefixo usado para nomear os arquivos gerados.
    samples : int
        Número de amostras (cubos) a serem gerados.
    dimensions : Tuple[int, int, int]
        Dimensões do cubo sísmico no formato (inline, xline, depth).
    """

    dataset_id: UUID  # type: ignore
    output_dir: str  # type: ignore
    prefix: Optional[str] = None
    samples: int  # type: ignore
    dimensions: Tuple[int, int, int]  # type: ignore
from typing import Optional
from seisbai_contracs.core import Event
from uuid import UUID


class SeismicCubeDatasetGenerationProgressEvent(Event, frozen=True, kw_only=True):
    """
    Evento de progresso periódico durante a geração de um dataset de cubo sísmico.

    Esse evento é emitido enquanto o processo de geração está em andamento,
    fornecendo informações sobre quantas amostras já foram geradas, o total,
    o caminho da última amostra e o progresso percentual.

    Attributes
    ----------
    dataset_id : UUID
        Identificador único do dataset em geração.
    samples_generated : int
        Número de amostras já geradas até o momento.
    samples_total : int
        Número total de amostras que serão geradas.
    last_sample_path : Optional[str], default=None
        Caminho do arquivo da última amostra gerada, se disponível.
    progress : int, default=0
        Progresso percentual da geração (0-100).
    """

    dataset_id: UUID  # type: ignore
    samples_generated: int  # type: ignore
    samples_total: int  # type: ignore
    last_sample_path: Optional[str] = None
    progress: int = 0
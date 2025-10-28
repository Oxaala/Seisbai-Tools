from uuid import UUID
from ....events import ProgressUpdatedEvent


class FaultDetectionProgressUpdatedEvent(ProgressUpdatedEvent, frozen=True, kw_only=True):
    """
    Evento emitido periodicamente durante a execução de um job de
    detecção de falhas, indicando o progresso do processamento.

    Attributes
    ----------
    dataset_id : UUID
        Identificador único do dataset associado ao job.
    
    processed : int
        Quantidade de janelas (ou blocos) já processadas.
    
    total : int
        Quantidade total de janelas (ou blocos) previstas para processamento.
    
    last_axis : str
        Nome do eixo mais recentemente processado (ex.: "ilines", "xlines", "depths").
    
    last_index : int
        Índice da última posição processada no eixo correspondente.
    """
    dataset_id: UUID
    processed: int
    total: int
    last_axis: str
    last_index: int
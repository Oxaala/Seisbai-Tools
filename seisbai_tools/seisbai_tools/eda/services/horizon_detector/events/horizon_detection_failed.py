from uuid import UUID
from ....events import FailedEvent


class HorizonDetectionFailedEvent(FailedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando o processo de detecção de horizontes falha.

    Este evento herda de :class:`FailedEvent` e carrega informações detalhadas
    sobre o erro ocorrido durante a execução do job de detecção.

    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset associado ao job que falhou.
    """
    dataset_id: UUID
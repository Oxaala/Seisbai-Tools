from uuid import UUID
from seisbai_contracs.core import Event


class FaultDetectionResumedEvent(Event, frozen=True, kw_only=True):
    """
    Evento emitido quando um job de detecção de falhas é retomado após ter sido pausado.

    Este evento indica que o processamento do dataset pausado anteriormente
    foi reiniciado e continuará até a conclusão ou nova interrupção.

    Attributes
    ----------
    dataset_id : UUID
        Identificador único do dataset associado ao job retomado.
    """
    dataset_id: UUID
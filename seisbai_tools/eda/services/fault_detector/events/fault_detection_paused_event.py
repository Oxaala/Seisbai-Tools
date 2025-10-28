from uuid import UUID
from ....events import PausedEvent


class FaultDetectionPausedEvent(PausedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando um job de detecção de falhas é pausado.

    Este evento indica que o processamento do dataset foi temporariamente
    interrompido, permitindo que ele seja retomado posteriormente.

    Attributes
    ----------
    dataset_id : UUID
        Identificador único do dataset associado ao job pausado.
    """
    dataset_id: UUID
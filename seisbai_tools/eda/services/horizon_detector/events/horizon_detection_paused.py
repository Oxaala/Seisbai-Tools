from uuid import UUID
from ....events import PausedEvent


class HorizonDetectionPausedEvent(PausedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando um job de detecção de horizontes é pausado.

    Este evento herda de :class:`PausedEvent` e sinaliza que o processamento
    do job foi temporariamente interrompido, permitindo que os consumidores
    do evento ajustem seus estados ou interfaces conforme necessário.

    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset associado ao job de detecção de horizontes que foi pausado.
    """
    dataset_id: UUID
from uuid import UUID
from ....events import ResumedEvent


class HorizonDetectionResumedEvent(ResumedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando um job de detecção de horizontes previamente pausado é retomado.

    Este evento herda de :class:`ResumedEvent` e sinaliza que o processamento
    do job foi retomado, permitindo que os consumidores do evento ajustem
    seus estados ou interfaces conforme necessário.

    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset associado ao job de detecção de horizontes que foi retomado.
    """
    dataset_id: UUID
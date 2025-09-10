from uuid import UUID
from seisbai_contracts.core.artefacts.events import CanceledEvent


class HorizonDetectionCanceledEvent(CanceledEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando um job de detecção de horizontes é cancelado.

    Este evento herda de :class:`CanceledEvent` e sinaliza que o processamento
    do job foi interrompido antes da conclusão, permitindo que os consumidores
    do evento ajustem seus estados ou interfaces conforme necessário.

    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset associado ao job de detecção de horizontes que foi cancelado.
    """
    dataset_id: UUID
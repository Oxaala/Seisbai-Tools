from uuid import UUID
from .event import Event

class ResumedEvent(Event, frozen=True, kw_only=True):
    """
    Evento que representa a retomada de uma operação previamente pausada.

    Esse evento é emitido quando uma operação em andamento é retomada
    após ter sido suspensa ou interrompida temporariamente.

    Herda de :class:`Event`.

    Attributes
    ----------
    work_id : UUID
        Identificador único da operação que foi retomada.
        Usado para correlacionar este evento com a execução da operação.
    """

    work_id: UUID
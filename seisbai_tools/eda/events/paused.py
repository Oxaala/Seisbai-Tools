from uuid import UUID
from .event import Event

class PausedEvent(Event, frozen=True, kw_only=True):
    """
    Evento que representa a pausa de uma operação em execução.

    Esse evento é emitido quando uma operação em andamento é suspensa
    temporariamente, geralmente para ser retomada posteriormente.

    Herda de :class:`Event`.

    Attributes
    ----------
    work_id : UUID
        Identificador único da operação que foi pausada.
        Usado para correlacionar este evento com a execução da operação.
    """

    work_id: UUID
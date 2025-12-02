from uuid import UUID
from .event import Event

class CancelledEvent(Event, frozen=True, kw_only=True):
    """
    Evento que representa o cancelamento de uma operação.

    Esse evento é emitido quando uma operação em andamento é
    explicitamente cancelada antes de ser concluída.

    Herda de :class:`Event`.

    Attributes
    ----------
    work_id : UUID
        Identificador único da operação que foi cancelada.
        Usado para correlacionar este evento com a execução da operação.
    """

    work_id: UUID
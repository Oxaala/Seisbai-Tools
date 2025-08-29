from uuid import UUID
from .event import Event

class CanceledEvent(Event, frozen=True, kw_only=True):
    """
    Evento que representa o cancelamento de uma tarefa.

    Esse evento é emitido quando uma tarefa em andamento é
    explicitamente cancelada antes de ser concluída.  
    Ele herda de `Event`, garantindo que possua os campos
    `id`, `timestamp` e `message`.

    Attributes
    ----------
    task_id : uuid.UUID
        Identificador único da tarefa que foi cancelada.  
        Usado para correlacionar este evento com a execução da tarefa.
    """

    task_id: UUID
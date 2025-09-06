from uuid import UUID
from .event import Event

class PausedEvent(Event, frozen=True, kw_only=True):
    """
    Evento que representa a pausa de uma tarefa em execução.

    Esse evento é emitido quando uma tarefa em andamento é suspensa
    temporariamente, geralmente para ser retomada posteriormente.
    Ele herda de `Event`, garantindo que possua os campos
    `id`, `timestamp` e `message`.

    Attributes
    ----------
    task_id : uuid.UUID
        Identificador único da tarefa que foi pausada.  
        Usado para correlacionar este evento com a execução da tarefa.
    """

    task_id: UUID
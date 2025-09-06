from uuid import UUID
from .event import Event

class ResumedEvent(Event, frozen=True, kw_only=True):
    """
    Evento que representa a retomada de uma tarefa previamente pausada.

    Esse evento é emitido quando uma tarefa em andamento é retomada
    após ter sido suspensa ou interrompida temporariamente.
    Ele herda de `Event`, garantindo que possua os campos
    `id`, `timestamp` e `message`.

    Attributes
    ----------
    task_id : uuid.UUID
        Identificador único da tarefa que foi retomada.  
        Usado para correlacionar este evento com a execução da tarefa.
    """

    task_id: UUID
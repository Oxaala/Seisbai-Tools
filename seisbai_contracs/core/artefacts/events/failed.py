from uuid import UUID
from .event import Event

class FailedEvent(Event, frozen=True, kw_only=True):
    """
    Evento que representa a falha na execução de uma tarefa.

    Esse evento é emitido quando uma tarefa não consegue ser concluída
    devido a um erro ou condição inesperada.  
    Ele herda de `Event`, garantindo que possua os campos
    `id`, `timestamp` e `message`.

    Attributes
    ----------
    task_id : uuid.UUID
        Identificador único da tarefa que falhou.  
        Usado para correlacionar este evento com a execução da tarefa.
    """

    task_id: UUID
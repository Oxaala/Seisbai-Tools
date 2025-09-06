from uuid import UUID
from .event import Event

class FinishedEvent(Event, frozen=True, kw_only=True):
    """
    Evento que representa a conclusão bem-sucedida de uma tarefa.

    Esse evento é emitido quando uma tarefa termina seu processamento
    com sucesso.  
    Ele herda de `Event`, garantindo que possua os campos
    `id`, `timestamp` e `message`.

    Attributes
    ----------
    task_id : uuid.UUID
        Identificador único da tarefa que foi concluída.  
        Usado para correlacionar este evento com a execução da tarefa.
    """

    task_id: UUID
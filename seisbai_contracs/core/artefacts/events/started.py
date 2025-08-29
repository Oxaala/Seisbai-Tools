from uuid import UUID
from .event import Event

class StartedEvent(Event, frozen=True, kw_only=True):
    """
    Evento que representa o início de uma tarefa no sistema.

    Esse evento é emitido quando uma nova tarefa é iniciada,
    permitindo rastrear sua execução desde o momento em que começou.
    Ele herda de `Event`, garantindo que possua os campos
    `id`, `timestamp` e `message`.

    Attributes
    ----------
    task_id : uuid.UUID
        Identificador único da tarefa que foi iniciada.  
        Usado para correlacionar este evento com a execução da tarefa.
    """
    
    task_id: UUID
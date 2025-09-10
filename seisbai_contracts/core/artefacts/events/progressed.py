from uuid import UUID
from .event import Event

class ProgressedEvent(Event, frozen=True, kw_only=True):
    """
    Evento que representa a atualização de progresso de uma tarefa em execução.

    Esse evento é emitido quando há uma mudança no progresso de uma tarefa,
    permitindo acompanhar seu andamento em tempo real.  
    Ele herda de `Event`, garantindo que possua os campos
    `id`, `timestamp` e `message`.

    Attributes
    ----------
    task_id : uuid.UUID
        Identificador único da tarefa cujo progresso foi atualizado.  
        Usado para correlacionar este evento com a execução da tarefa.

    value : int
        Valor numérico que indica o progresso atual da tarefa.  
        Pode ser interpretado como percentual (0–100), número de etapas
        concluídas ou outra métrica definida pelo sistema.
    """

    task_id: UUID
    value: int
from uuid import UUID
from .event import Event

class StartedEvent(Event, frozen=True, kw_only=True):
    """
    Evento que representa o início de uma tarefa no sistema.

    Este evento é emitido assim que uma nova tarefa é iniciada,
    permitindo rastrear sua execução desde o ponto inicial.
    Ele herda de `Event`, o que garante que também possua os
    campos genéricos `id`, `timestamp` e `message` utilizados
    para padronizar o sistema de eventos.

    Attributes
    ----------
    task_id : uuid.UUID
        Identificador único da tarefa iniciada.  
        Usado para correlacionar este evento com o ciclo de vida
        completo da tarefa.

    title : str
        Nome ou descrição amigável da tarefa que foi iniciada.  
        Geralmente utilizado para exibição em interfaces de usuário
        ou logs.
    """
    
    task_id: UUID
    title: str
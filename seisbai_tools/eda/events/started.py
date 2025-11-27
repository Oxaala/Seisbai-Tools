from uuid import UUID
from .event import Event

class StartedEvent(Event, frozen=True, kw_only=True):
    """
    Evento que representa o início de uma operação no sistema.

    Este evento é emitido assim que uma operação é iniciada, permitindo rastrear
    sua execução desde o ponto inicial.

    Herda de :class:`Event`.

    Attributes
    ----------
    work_id : UUID
        Identificador único da operação iniciada.
        Usado para correlacionar este evento com o ciclo de vida completo da operação.

    title : str
        Nome ou descrição amigável da operação que foi iniciada.
        Geralmente utilizado para exibição em interfaces ou logs.
    """
    
    work_id: UUID
    title: str
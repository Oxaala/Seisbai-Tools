from uuid import UUID
from .event import Event

class FailedEvent(Event, frozen=True, kw_only=True):
    """
    Evento que representa a falha na execução de uma operação.

    Esse evento é emitido quando uma operação não consegue ser concluída
    devido a um erro ou condição inesperada.

    Herda de :class:`Event`.

    Attributes
    ----------
    work_id : UUID
        Identificador único da operação que falhou.
        Usado para correlacionar este evento com a execução da operação.

    reason : str
        Descrição detalhada do erro que causou a falha.
        Pode incluir mensagens de exceções ou informações adicionais
        para facilitar a análise do problema.
    """
    
    work_id: UUID
    reason: str
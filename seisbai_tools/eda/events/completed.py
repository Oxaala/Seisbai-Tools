from typing import Any
from uuid import UUID
from .event import Event

class CompletedEvent(Event, frozen=True, kw_only=True):
    """
    Evento que representa a conclusão bem-sucedida de uma operação.

    Esse evento é emitido quando uma operação termina seu processamento
    com sucesso.

    Herda de :class:`Event`.

    Attributes
    ----------
    work_id : UUID
        Identificador único da operação que foi concluída.
        Usado para correlacionar este evento com a execução da operação.

    result : Any
        Resultado produzido pela operação.
        Pode ser qualquer valor retornado ou gerado durante o processamento.
    """

    work_id: UUID
    result: Any
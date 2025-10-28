from uuid import UUID
from .event import Event

class ProgressUpdatedEvent(Event, frozen=True, kw_only=True):
    """
    Evento que representa a atualização de progresso de uma operação em execução.

    Esse evento é emitido quando há uma mudança no progresso de uma operação,
    permitindo acompanhar seu andamento em tempo real.

    Herda de :class:`Event`.

    Attributes
    ----------
    work_id : UUID
        Identificador único da operação cujo progresso foi atualizado.
        Usado para correlacionar este evento com a execução da operação.

    progress : float
        Valor numérico que indica o progresso atual da operação.
        Pode ser interpretado como percentual (0–100), número de etapas
        concluídas ou outra métrica definida pelo sistema.
    """

    work_id: UUID
    progress: float
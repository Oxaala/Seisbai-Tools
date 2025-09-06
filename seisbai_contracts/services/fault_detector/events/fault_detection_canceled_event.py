from uuid import UUID
from seisbai_contracts.core import Event


class FaultDetectionCanceledEvent(Event, frozen=True, kw_only=True):
    """
    Evento emitido quando um job de detecção de falhas é cancelado antes da conclusão.

    Este evento indica que o processamento do dataset foi interrompido,
    seja por ação do usuário ou por alguma condição do sistema.

    Attributes
    ----------
    dataset_id : UUID
        Identificador único do dataset associado ao job cancelado.
    """
    dataset_id: UUID
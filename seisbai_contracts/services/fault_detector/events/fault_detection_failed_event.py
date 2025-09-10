from typing import Optional
from uuid import UUID
from seisbai_contracts.core.artefacts.events.failed import FailedEvent


class FaultDetectionFailedEvent(FailedEvent, frozen=True, kw_only=True):
    """
    Evento que indica que a detecção de falhas falhou para um determinado dataset.

    Este evento herda de :class:`FailedEvent` e é utilizado para notificar que uma
    operação de detecção de falhas não pôde ser completada com sucesso.

    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset em que a falha ocorreu.

    error_message : str
        Mensagem descritiva do erro que causou a falha.

    stacktrace : Optional[str], default=None
        Stacktrace completo do erro, caso disponível. Útil para depuração e auditoria.
    """
    dataset_id: UUID
    error_message: str
    stacktrace: Optional[str] = None
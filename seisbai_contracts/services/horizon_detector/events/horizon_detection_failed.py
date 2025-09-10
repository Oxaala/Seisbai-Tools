from typing import Optional
from uuid import UUID
from seisbai_contracts.core.artefacts.events import FailedEvent


class HorizonDetectionFailedEvent(FailedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando o processo de detecção de horizontes falha.

    Este evento herda de :class:`FailedEvent` e carrega informações detalhadas
    sobre o erro ocorrido durante a execução do job de detecção.

    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset associado ao job que falhou.

    error_message : str
        Mensagem de erro descritiva que explica a causa da falha.

    stacktrace : Optional[str], default=None
        Rastro de pilha (stacktrace) opcional contendo detalhes técnicos da
        exceção para fins de diagnóstico e depuração.
    """
    dataset_id: UUID
    error_message: str
    stacktrace: Optional[str] = None
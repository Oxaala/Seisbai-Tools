from typing import Optional
from uuid import UUID
from seisbai_contracts.core.artefacts.events import FailedEvent


class NetworkConstructorFailedEvent(FailedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando a execução de um job de construção de rede falha.

    Este evento sinaliza que o processamento do job de construção e/ou
    treinamento da rede neural encontrou um erro crítico, impedindo sua
    conclusão. Permite que os consumidores do evento ajustem seus estados,
    façam logging ou acionem mecanismos de recuperação.

    Herda de :class:`FailedEvent`.

    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset associado ao job que falhou.

    error_message : str
        Mensagem de erro resumida indicando a causa da falha.

    stacktrace : Optional[str]
        Stack trace ou detalhes técnicos do erro, se disponíveis.
    """
    dataset_id: UUID
    error_message: str
    stacktrace: Optional[str] = None
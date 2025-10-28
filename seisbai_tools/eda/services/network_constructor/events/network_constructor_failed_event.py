from uuid import UUID
from ....events import FailedEvent


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
    """
    dataset_id: UUID
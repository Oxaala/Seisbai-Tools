from uuid import UUID
from ....events import FailedEvent


class FaultDetectionFailedEvent(FailedEvent, frozen=True, kw_only=True):
    """
    Evento que indica que a detecção de falhas falhou para um determinado dataset.

    Este evento herda de :class:`FailedEvent` e é utilizado para notificar que uma
    operação de detecção de falhas não pôde ser completada com sucesso.

    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset em que a falha ocorreu.
    """
    dataset_id: UUID
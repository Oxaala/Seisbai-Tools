from uuid import UUID
from ....events import PausedEvent


class NetworkConstructorPausedEvent(PausedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando a execução de um job de construção de rede é pausada.

    Este evento sinaliza que o processo de construção e/ou treinamento da rede
    neural foi temporariamente interrompido, permitindo que seja retomado
    posteriormente sem perda de estado.

    Herda de :class:`PausedEvent`.

    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset associado ao job pausado.
    """
    dataset_id: UUID
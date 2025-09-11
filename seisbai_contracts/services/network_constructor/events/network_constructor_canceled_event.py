from uuid import UUID
from seisbai_contracts.core.artefacts.events import CanceledEvent


class NetworkConstructorCanceledEvent(CanceledEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando a execução de um job de construção de rede é cancelada.

    Este evento sinaliza que o processamento do job de construção e/ou
    treinamento da rede neural foi interrompido antes da conclusão,
    permitindo que os consumidores do evento ajustem seus estados ou
    interfaces conforme necessário.

    Herda de :class:`CanceledEvent`.

    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset associado ao job que foi cancelado.
    """
    dataset_id: UUID
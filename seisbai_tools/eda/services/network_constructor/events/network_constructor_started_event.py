from uuid import UUID
from ....events import StartedEvent


class NetworkConstructorStartedEvent(StartedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando a execução de um job de construção de rede é iniciada.

    Este evento sinaliza que o processo de construção e treinamento da rede
    neural associado a um dataset foi iniciado, permitindo que os consumidores
    do evento ajustem seus estados ou interfaces conforme necessário.

    Herda de :class:`StartedEvent`.

    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset associado ao job iniciado.

    model_type : str
        Tipo de modelo utilizado na construção da rede (por exemplo, "unet").
    """
    dataset_id: UUID
    model_type: str
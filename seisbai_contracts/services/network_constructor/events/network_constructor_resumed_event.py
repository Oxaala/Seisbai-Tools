from uuid import UUID
from seisbai_contracts.core.artefacts.events import ResumedEvent


class NetworkConstructorResumedEvent(ResumedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando a execução de um job de construção de rede previamente pausado é retomada.

    Este evento sinaliza que o processo de construção e/ou treinamento da rede
    neural foi reiniciado após uma pausa, permitindo que os consumidores do
    evento ajustem seus estados ou interfaces conforme necessário.

    Herda de :class:`ResumedEvent`.

    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset associado ao job retomado.

    model_type : str
        Tipo de modelo utilizado na construção da rede (por exemplo, "unet").
    """
    dataset_id: UUID
from uuid import UUID
from ....events import CancelledEvent


class SeismicCubeDatasetGenerationCancelledEvent(CancelledEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando a geração de um dataset de cubo sísmico é cancelada.

    Esse evento é disparado sempre que o processo de geração é interrompido,
    seja por ação do usuário ou por decisão do sistema.

    Attributes
    ----------
    dataset_id : UUID
        Identificador único do dataset cuja geração foi cancelada.
    """

    dataset_id: UUID
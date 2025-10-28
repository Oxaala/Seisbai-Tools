from uuid import UUID
from ....events import PausedEvent


class SeismicCubeDatasetGenerationPausedEvent(PausedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando a geração de um dataset de cubo sísmico é pausada.

    Esse evento é disparado sempre que o processo de geração é temporariamente
    interrompido, permitindo monitoramento ou retomada futura.

    Attributes
    ----------
    dataset_id : UUID
        Identificador único do dataset cuja geração foi pausada.
    """

    dataset_id: UUID
from seisbai_contracs.core.Event import Event
from uuid import UUID


class SeismicCubeDatasetGenerationResumedEvent(Event, frozen=True, kw_only=True):
    """
    Evento emitido quando a geração de um dataset de cubo sísmico é retomada.

    Esse evento é disparado sempre que um processo de geração previamente pausado
    volta a ser executado.

    Attributes
    ----------
    dataset_id : UUID
        Identificador único do dataset cuja geração foi retomada.
    """

    dataset_id: UUID  # type: ignore
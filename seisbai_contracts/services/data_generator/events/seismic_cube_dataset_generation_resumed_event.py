from seisbai_contracts.core.artefacts.events import ResumedEvent
from uuid import UUID


class SeismicCubeDatasetGenerationResumedEvent(ResumedEvent, frozen=True, kw_only=True):
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
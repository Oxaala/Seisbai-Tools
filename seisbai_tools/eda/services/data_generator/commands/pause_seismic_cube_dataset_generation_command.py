from uuid import UUID
from ....commands import PauseCommand


class PauseSeismicCubeDatasetGenerationCommand(PauseCommand, frozen=True, kw_only=True):
    """
    Comando para pausar a geração de um dataset de cubo sísmico.

    Esse comando é emitido quando é necessário interromper temporariamente o
    processo de geração, sem descartá-lo, permitindo que ele seja retomado posteriormente.

    Attributes
    ----------
    dataset_id : UUID
        Identificador único do dataset que deve ser pausado.
    """

    dataset_id: UUID
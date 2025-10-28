from uuid import UUID
from ....commands import ResumeCommand


class ResumeSeismicCubeDatasetGenerationCommand(ResumeCommand, frozen=True, kw_only=True):
    """
    Comando para retomar a geração de um dataset de cubo sísmico.

    Esse comando é emitido quando um processo de geração previamente pausado
    deve ser retomado, continuando de onde parou.

    Attributes
    ----------
    dataset_id : UUID
        Identificador único do dataset cuja geração deve ser retomada.
    """

    dataset_id: UUID
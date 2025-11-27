from uuid import UUID
from ....events import FailedEvent


class SeismicCubeDatasetGenerationFailedEvent(FailedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando ocorre uma falha na geração de um dataset de cubo sísmico.

    Esse evento é disparado sempre que o processo de geração encontra um erro,
    contendo informações sobre o dataset, a mensagem de erro e, opcionalmente, 
    o stacktrace para depuração.

    Attributes
    ----------
    dataset_id : UUID
        Identificador único do dataset que falhou ao ser gerado.
    """
    dataset_id: UUID
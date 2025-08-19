from typing import Optional
from uuid import UUID
from seisbai_contracs.core import Event


class SeismicCubeDatasetGenerationFailedEvent(Event, frozen=True):
    """
    Evento emitido quando ocorre uma falha na geração de um dataset de cubo sísmico.

    Esse evento é disparado sempre que o processo de geração encontra um erro,
    contendo informações sobre o dataset, a mensagem de erro e, opcionalmente, 
    o stacktrace para depuração.

    Attributes
    ----------
    dataset_id : UUID
        Identificador único do dataset que falhou ao ser gerado.
    error_message : str
        Mensagem resumida do erro ocorrido.
    stacktrace : Optional[str], default=None
        Stacktrace completo do erro, se disponível, útil para diagnóstico.
    """

    dataset_id: UUID  # type: ignore
    error_message: str  # type: ignore
    stacktrace: Optional[str] = None
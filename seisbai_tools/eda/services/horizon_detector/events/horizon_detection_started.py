from uuid import UUID
from ....events import StartedEvent


class HorizonDetectionStartedEvent(StartedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando um job de detecção de horizontes é iniciado.

    Este evento herda de :class:`StartedEvent` e fornece informações iniciais
    sobre o job, incluindo o dataset e os parâmetros do modelo que será utilizado.

    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset associado ao job de detecção de horizontes.

    seismic_path : str
        Caminho para o arquivo sísmico de entrada utilizado no job.

    model_dir : str
        Diretório onde o modelo de detecção de horizontes está armazenado.

    model_name : str
        Nome do modelo que será utilizado para o processo de detecção.
    """
    dataset_id: UUID
    seismic_path: str
    model_dir: str
    model_name: str
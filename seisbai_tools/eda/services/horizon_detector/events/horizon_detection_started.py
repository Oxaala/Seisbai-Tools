from uuid import UUID

from seisbai_tools.file_system.manager import FileSystemPathInfo
from ....events import StartedEvent


class HorizonDetectionStartedEvent(StartedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando um job de detecção de horizontes é iniciado.

    Este evento herda de :class:`StartedEvent` e carrega as informações essenciais
    para rastrear o início do processo, incluindo os caminhos para os arquivos
    sísmicos e o modelo utilizado.

    Attributes
    ----------
    dataset_id : UUID
        Identificador único do dataset associado ao job de detecção de horizontes.

    seismic : FileSystemPathInfo
        Informações sobre o arquivo sísmico usado como entrada no processo
        de detecção de horizontes.

    model : FileSystemPathInfo
        Informações sobre o diretório ou arquivo do modelo de detecção que será
        utilizado para processar o dataset.
    """
    dataset_id: UUID
    seismic: FileSystemPathInfo
    model: FileSystemPathInfo
from uuid import UUID

from seisbai_tools.file_system.manager import FileSystemPathInfo
from ....events import StartedEvent


class HorizonDetectionStartedEvent(StartedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando o processo de detecção de horizontes é iniciado.

    Este evento herda de :class:`StartedEvent` e representa o ponto exato em que o
    job de detecção de horizontes começa a ser executado. Ele fornece informações
    suficientes para que serviços externos — como sistemas de monitoramento,
    rastreamento, filas de execução ou dashboards — possam reagir ao início do
    job e acompanhar sua execução.

    Attributes
    ----------
    dataset_id : UUID
        Identificador único do dataset para o qual o processo de detecção de
        horizontes está sendo executado.

    seismic_path : FileSystemPathInfo
        Informações sobre o arquivo sísmico utilizado como entrada, incluindo
        caminho, metadados e possíveis indicadores de integridade.

    model_path : FileSystemPathInfo
        Informações sobre o modelo de detecção empregado no job, representando
        tanto caminhos quanto metadados conforme definidos pelo sistema de arquivos.
    """

    dataset_id: UUID
    seismic_path: FileSystemPathInfo
    model_path: FileSystemPathInfo
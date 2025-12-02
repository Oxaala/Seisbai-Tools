from uuid import UUID

from seisbai_tools.file_system.manager import FileSystemInfo
from ....events import StartedEvent


class FaultDetectionStartedEvent(StartedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando um job de detecção de falhas é iniciado.

    Esse evento sinaliza o começo do processo de detecção de falhas em um dataset
    sísmico, permitindo que outros componentes acompanhem ou reajam ao início
    do job, como serviços de monitoramento, rastreamento ou interfaces de usuário.

    Attributes
    ----------
    dataset_id : UUID
        Identificador único do dataset associado ao job.

    seismic : FileSystemInfo
        Informações sobre o arquivo sísmico utilizado no processo, incluindo
        caminho, tamanho, tipo e metadados definidos pelo sistema de arquivos.

    model : FileSystemInfo
        Informações sobre o modelo de rede neural empregado na detecção, também
        representado por metadados fornecidos pelo sistema de arquivos.
    """

    dataset_id: UUID
    seismic: FileSystemInfo
    model: FileSystemInfo
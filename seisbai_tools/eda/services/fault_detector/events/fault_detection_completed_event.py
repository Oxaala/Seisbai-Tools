from typing import List
from uuid import UUID

from seisbai_tools.file_system.manager import FileSystemPathInfo
from ....events import CompletedEvent


class FaultDetectionCompletedEvent(CompletedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando um job de detecção de falhas é concluído com sucesso.

    Esse evento é disparado ao término do processamento de detecção de falhas
    em um dataset sísmico. Ele contém o identificador do dataset processado e
    informações sobre os arquivos gerados.

    Attributes
    ----------
    dataset_id : UUID
        Identificador único do dataset associado ao job.

    output : FileSystemPathInfo
        Informações detalhadas sobre os arquivos gerados no processo,
        incluindo caminhos, tamanhos, tipos e metadados definidos pelo
        sistema de arquivos utilizado.
    """

    dataset_id: UUID
    output: FileSystemPathInfo
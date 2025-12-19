from typing import List
from uuid import UUID

from seisbai_tools.file_system.manager import FileSystemPathInfo
from ....events import CompletedEvent


class FaultDetectionCompletedEvent(CompletedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando um job de detecção de falhas sísmicas é concluído
    com sucesso.

    Esse evento sinaliza que o processo de detecção de falhas em um dataset
    sísmico foi finalizado, permitindo que consumidores atualizem estados,
    persistam resultados ou acionem fluxos subsequentes. Ele fornece o
    identificador do dataset e o caminho de saída contendo os artefatos
    produzidos.

    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset para o qual a detecção de falhas foi
        executada.

    output_path : FileSystemPathInfo
        Informações referentes ao local onde os resultados foram gravados,
        incluindo os caminhos e metadados associados ao backend de sistema
        de arquivos utilizado.
    """

    dataset_id: UUID
    output_path: FileSystemPathInfo
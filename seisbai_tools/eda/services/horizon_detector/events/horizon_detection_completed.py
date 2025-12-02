from uuid import UUID

from seisbai_tools.file_system.manager import FileSystemInfo
from ....events import CompletedEvent


class HorizonDetectionCompletedEvent(CompletedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando o processo de detecção de horizontes é concluído com sucesso.

    Este evento herda de :class:`CompletedEvent` e indica que o job associado foi
    finalizado, disponibilizando as informações sobre o diretório de saída.

    Attributes
    ----------
    dataset_id : UUID
        Identificador único do dataset para o qual a detecção de horizontes foi executada.

    output : FileSystemInfo
        Informações sobre o sistema de arquivos onde os resultados foram gerados,
        incluindo caminhos dos arquivos de saída (ex.: horizontes detectados, máscaras
        processadas, resultados intermediários).
    """
    dataset_id: UUID
    output: FileSystemInfo
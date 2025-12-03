from uuid import UUID

from seisbai_tools.file_system.manager import FileSystemPathInfo
from ....events import CompletedEvent


class HorizonDetectionCompletedEvent(CompletedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando o processo de detecção de horizontes é concluído
    com sucesso.

    Este evento herda de :class:`CompletedEvent` e indica que o job associado
    terminou corretamente, permitindo que consumidores do evento acessem os
    artefatos produzidos, atualizem interfaces de usuário ou desencadeiem
    novos estágios do pipeline.

    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset para o qual o processo de detecção
        de horizontes foi realizado.

    output_path : FileSystemPathInfo
        Informações sobre o local onde os resultados foram armazenados,
        incluindo metadados do sistema de arquivos, caminhos dos arquivos
        gerados (como superfícies detectadas, máscaras ou representações
        intermediárias).
    """

    dataset_id: UUID
    output_path: FileSystemPathInfo
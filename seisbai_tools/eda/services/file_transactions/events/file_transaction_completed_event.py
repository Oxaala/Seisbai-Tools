from typing import List
from uuid import UUID

from ....events import CompletedEvent


class FileTransactionCompletedEvent(CompletedEvent, frozen=True, kw_only=True):
    """
    Evento que indica a conclusão bem-sucedida de uma transação de arquivos.

    Esse evento é emitido quando uma transação de arquivos termina sem erros,
    informando o dataset associado e os caminhos dos arquivos de saída gerados.

    Attributes
    ----------
    dataset_id : UUID
        Identificador único do dataset cuja transação foi concluída.

    output_paths : List[str]
        Lista de caminhos de todos os arquivos de saída gerados pela transação.
    """
    dataset_id: UUID
    output_paths: List[str]
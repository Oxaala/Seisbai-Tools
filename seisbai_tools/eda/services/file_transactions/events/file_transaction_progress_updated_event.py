from typing import Optional
from uuid import UUID

from ....events import ProgressUpdatedEvent


class FileTransactionProgressUpdatedEvent(ProgressUpdatedEvent, frozen=True, kw_only=True):
    """
    Evento que indica uma atualização no progresso de uma transação de arquivos.

    Esse evento é emitido periodicamente durante a execução de uma transação
    de arquivos, informando quantos arquivos já foram processados, o total
    previsto e o caminho do último arquivo gerado (caso aplicável).

    Attributes
    ----------
    dataset_id : UUID
        Identificador único do dataset associado à transação de arquivos.

    processed : int
        Quantidade de arquivos já processados até o momento.

    total : int
        Quantidade total de arquivos previstos para a transação.

    last_output_path : Optional[str]
        Caminho do último arquivo de saída gerado ou atualizado, caso exista.
    """
    dataset_id: UUID
    processed: int
    total: int
    last_output_path: Optional[str]
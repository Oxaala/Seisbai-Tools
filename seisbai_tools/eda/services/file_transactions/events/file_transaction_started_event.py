from typing import List
from uuid import UUID

from ....events import StartedEvent


class FileTransactionStartedEvent(StartedEvent, frozen=True, kw_only=True):
    """
    Evento que indica que uma transação de arquivos foi iniciada.

    Esse evento é emitido quando o sistema inicia uma nova transação de arquivos,
    contendo as informações necessárias sobre a operação, arquivos de entrada
    e diretório de saída.

    Attributes
    ----------
    dataset_id : UUID
        Identificador único do dataset associado à transação de arquivos.

    operation : str
        Tipo da operação executada na transação (exemplo: "copy", "move", "export").

    input_paths : List[str]
        Lista de caminhos de arquivos de entrada utilizados na transação.

    output_dir : str
        Caminho do diretório onde os resultados da transação serão armazenados.
    """
    dataset_id: UUID
    operation: str
    input_paths: List[str]
    output_dir: str
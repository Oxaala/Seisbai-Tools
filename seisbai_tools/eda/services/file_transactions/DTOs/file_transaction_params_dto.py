from typing import Dict, List
from msgspec import Struct, field


class FileTransactionParamsDTO(Struct, frozen=True, tag=True):
    """Parâmetros para uma transação de arquivo genérica.

    - operation: nome lógico da operação (ex.: "copy", "transform", "compress").
    - input_paths: lista de caminhos de arquivos de entrada no filesystem.
    - output_dir: diretório onde arquivos de saída serão gravados.
    - options: dicionário livre para parâmetros específicos da operação.
    """

    operation: str = "copy"
    input_paths: List[str] = field(default_factory=list)
    output_dir: str = "output/filetx"
    options: Dict[str, object] = field(default_factory=dict)
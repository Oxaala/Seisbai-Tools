from uuid import UUID
from ....events import CanceledEvent


class FileTransactionCanceledEvent(CanceledEvent, frozen=True, kw_only=True):
    """
    Evento que indica que uma transação de arquivos foi cancelada.

    Esse evento é emitido quando a execução de uma transação de arquivos
    em andamento é interrompida antes da conclusão.

    Attributes
    ----------
    dataset_id : UUID
        Identificador único do dataset cuja transação de arquivos foi cancelada.
    """
    dataset_id: UUID
from uuid import UUID

from ....events import ResumedEvent


class FileTransactionResumedEvent(ResumedEvent, frozen=True, kw_only=True):
    """
    Evento que indica que uma transação de arquivos foi retomada.

    Esse evento é emitido quando a execução de uma transação de arquivos
    previamente pausada é retomada.

    Attributes
    ----------
    dataset_id : UUID
        Identificador único do dataset cuja transação de arquivos foi retomada.
    """
    dataset_id: UUID
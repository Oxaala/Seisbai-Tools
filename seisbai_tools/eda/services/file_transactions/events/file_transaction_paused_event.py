from uuid import UUID

from ....events import PausedEvent


class FileTransactionPausedEvent(PausedEvent, frozen=True, kw_only=True):
    """
    Evento que indica que uma transação de arquivos foi pausada.

    Esse evento é emitido quando a execução de uma transação de arquivos
    em andamento é temporariamente suspensa.

    Attributes
    ----------
    dataset_id : UUID
        Identificador único do dataset cuja transação de arquivos foi pausada.
    """
    dataset_id: UUID
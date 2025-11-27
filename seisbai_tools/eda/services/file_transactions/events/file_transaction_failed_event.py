from uuid import UUID

from ....events import FailedEvent


class FileTransactionFailedEvent(FailedEvent, frozen=True, kw_only=True):
    """
    Evento que indica a falha de uma transação de arquivos.

    Esse evento é emitido quando ocorre um erro durante a execução de uma
    transação de arquivos. Ele contém o identificador do dataset associado,
    a mensagem de erro e o stack trace para fins de diagnóstico.

    Attributes
    ----------
    dataset_id : UUID
        Identificador único do dataset cuja transação falhou.
    """
    dataset_id: UUID
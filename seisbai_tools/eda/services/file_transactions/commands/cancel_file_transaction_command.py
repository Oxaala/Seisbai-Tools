import uuid

from ....commands import CancelCommand


class CancelFileTransactionJobCommand(CancelCommand, frozen=True, kw_only=True):
    """
    Comando que solicita o cancelamento de uma transação de arquivos.

    Esse comando é utilizado para notificar o sistema de que uma operação
    de transação de arquivos em andamento deve ser interrompida. Ele carrega
    o identificador do dataset associado à transação que deve ser cancelada.

    Attributes
    ----------
    dataset_id : uuid.UUID
        Identificador único do dataset cuja transação de arquivos deve ser cancelada.
    """
    dataset_id: uuid.UUID
import uuid

from ....commands import Command


class PauseFileTransactionJobCommand(Command, frozen=True, kw_only=True):
    """
    Comando que solicita a pausa de uma transação de arquivos.

    Esse comando é utilizado para notificar o sistema de que a execução
    de uma transação de arquivos em andamento deve ser temporariamente
    suspensa. Ele carrega o identificador do dataset associado à transação
    que será pausada.

    Attributes
    ----------
    dataset_id : uuid.UUID
        Identificador único do dataset cuja transação de arquivos deve ser pausada.
    """
    dataset_id: uuid.UUID
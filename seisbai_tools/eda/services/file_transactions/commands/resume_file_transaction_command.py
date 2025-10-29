import uuid

from ....commands import Command


class ResumeFileTransactionJobCommand(Command, frozen=True, kw_only=True):
    """
    Comando que solicita a retomada de uma transação de arquivos.

    Esse comando é utilizado para notificar o sistema de que uma transação
    de arquivos previamente pausada deve ser retomada do ponto em que foi
    interrompida. Ele carrega o identificador do dataset associado à transação
    que será retomada.

    Attributes
    ----------
    dataset_id : uuid.UUID
        Identificador único do dataset cuja transação de arquivos deve ser retomada.
    """
    dataset_id: uuid.UUID
from seisbai_contracts.core.artefacts.base import Base
from seisbai_contracts.core.mixins import CommandAutoPublisherMixin


class Command(Base, CommandAutoPublisherMixin, frozen=True, kw_only=True):
    """
    Representa um **comando** no sistema.

    Em arquiteturas baseadas em mensageria, um comando é uma instrução explícita
    enviada para que o sistema realize uma ação. Diferente de um evento, o comando
    descreve **intenção de alteração de estado futura**.

    Herda de :class:`Base`.

    Attributes
    ----------
    id : uuid.UUID
        Identificador único do comando, herdado de :class:`Base`.  
        Gerado automaticamente com ``uuid4()``.  
        Usado para rastreamento em logs e pipelines distribuídos.

    timestamp : datetime.datetime
        Data e hora exata da criação do comando, em UTC.  
        Herdado de :class:`Base`.  
        Essencial para auditoria e ordenação temporal.
    """
    pass
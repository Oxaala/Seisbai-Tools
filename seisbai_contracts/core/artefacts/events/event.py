from uuid import UUID
from msgspec import field
from seisbai_contracts.core.artefacts.base import Base


class Event(Base, frozen=True, kw_only=True):
    """
    Representa um **evento** no sistema.

    Em arquiteturas baseadas em mensageria e *event-driven*, um evento descreve
    **algo que já aconteceu** no domínio. Diferente de um comando, ele não expressa
    intenção futura, mas sim um fato passado, que pode ser observado e reagido por
    outros componentes.

    Herda de :class:`Base`.

    Attributes
    ----------
    id : uuid.UUID
        Identificador único do evento, herdado de :class:`Base`.  
        Gerado automaticamente com ``uuid4()``.

    timestamp : datetime.datetime
        Data e hora exata da criação do evento, em UTC.  
        Herdado de :class:`Base`.

    correlation_id : uuid.UUID
        Identificador que agrupa este evento a um fluxo maior (ex: saga, processo
        distribuído, requisição de negócio).  
        Usado para rastrear múltiplas mensagens relacionadas.  
        Pode ser ``None`` se o evento for independente.

    causation_id : uuid.UUID
        Identificador da mensagem (comando ou evento) que **causou** este evento.  
        Permite reconstruir a cadeia causal de mensagens, essencial para auditoria
        e debugging.  
        Pode ser ``None`` em eventos iniciais.
    """

    correlation_id: UUID = field()
    causation_id: UUID = field()
from msgspec import field
from ..base import Base
from ulid import ULID

class Event(Base, frozen=True, kw_only=True):
    """
    Representa um **evento** no sistema.

    Em arquiteturas baseadas em mensageria e *event-driven*, um evento descreve
    **algo que já aconteceu** no domínio. Diferente de um comando, ele não expressa
    intenção futura, mas sim um fato passado que pode ser observado e reagido por
    outros componentes.

    Herda de :class:`Base`, portanto possui `id` e `timestamp`.

    Attributes
    ----------
    correlation_id : ULID
        Identificador que agrupa este evento a um fluxo maior (ex.: saga, processo
        distribuído, requisição de negócio).  
        Usado para rastrear múltiplas mensagens relacionadas.  
        Pode ser None se o evento for independente.

    causation_id : ULID
        Identificador da mensagem (comando ou evento) que **causou** este evento.  
        Permite reconstruir a cadeia causal de mensagens, essencial para auditoria
        e depuração.  
        Pode ser None em eventos iniciais.
    """
    correlation_id: ULID = field()
    causation_id: ULID = field()
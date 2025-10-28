from typing import Optional

from msgspec import field
from ulid import ULID
from ..base import Base


class Command(Base, frozen=True, kw_only=True):
    """
    Representa um comando no sistema.

    Em arquiteturas baseadas em mensageria, um comando é uma instrução explícita
    enviada para que o sistema realize uma ação. Diferente de um evento, o comando
    descreve intenção de alteração de estado futura.

    Comandos que iniciam um novo fluxo de operação podem omitir o `correlation_id`.
    Já comandos que pertencem a um fluxo existente devem possuir um
    `correlation_id` válido, herdado do comando inicial.

    Herda de :class:`Base`.
    """
    correlation_id: Optional[ULID] = field(default=None)
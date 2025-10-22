from seisbai_tools.eda.base import Base


class Command(Base, frozen=True, kw_only=True):
    """
    Representa um **comando** no sistema.

    Em arquiteturas baseadas em mensageria, um comando é uma instrução explícita
    enviada para que o sistema realize uma ação. Diferente de um evento, o comando
    descreve **intenção de alteração de estado futura**.

    Herda de :class:`Base`.
    """
    pass
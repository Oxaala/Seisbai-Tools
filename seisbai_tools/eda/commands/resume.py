from .command import Command

class ResumeCommand(Command, frozen=True, kw_only=True):
    """
    Comando para solicitar a retomada de uma operação ou processo previamente pausado.

    Em arquiteturas baseadas em mensageria, um comando representa uma instrução
    explícita que solicita ao sistema que execute uma ação específica. Diferente
    de um evento, o comando descreve a **intenção de alteração futura de estado**.

    Herda de :class:`Command`.
    """
    pass
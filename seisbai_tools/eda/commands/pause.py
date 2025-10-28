from .command import Command

class PauseCommand(Command, frozen=True, kw_only=True):
    """
    Comando para solicitar a pausa de uma operação ou processo no sistema.

    Em arquiteturas baseadas em mensageria, um comando representa uma instrução
    explícita que solicita ao sistema que execute uma ação específica. Diferente
    de um evento, o comando descreve a **intenção de alteração futura de estado**.

    Herda de :class:`Command`.
    """
    pass
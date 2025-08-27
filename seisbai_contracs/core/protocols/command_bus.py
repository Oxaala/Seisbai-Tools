from __future__ import annotations
from typing import Protocol, TypeVar

from seisbai_contracs.core.artefacts.command import Command
from seisbai_contracs.core.protocols.command_handler import CommandHandlerProtocol

# Tipo genérico para comandos, restrito a subclasses de Command
C = TypeVar("C", bound=Command)


class CommandBusProtocol(Protocol):
    """
    Protocolo para um barramento de comandos (CommandBus).

    Define os métodos que qualquer implementação de barramento de comandos
    deve fornecer: publicar comandos e registrar handlers (assinaturas).
    """

    def publish(self, topic: str, command: Command) -> None:
        """
        Publica um comando no tópico informado.

        Args:
            topic (str): Nome do tópico para publicação.
            command (Command): Instância do comando a ser publicada.
        """
        ...

    def subscribe(self, topic: str, callback: CommandHandlerProtocol[C]) -> None:
        """
        Assina um tópico com um callback.

        Args:
            topic (str): Nome do tópico a ser assinado.
            callback (CommandHandlerProtocol[C]): Função ou objeto chamável
                que será invocado quando um comando do tipo C for publicado
                neste tópico.
        """
        ...
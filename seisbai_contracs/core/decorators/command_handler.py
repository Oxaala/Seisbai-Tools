from typing import Type
from seisbai_contracs.config.buses import BusManager
from seisbai_contracs.core.protocols.command_handler import CommandHandlerProtocol, C


def commandHandler(command: Type[C]):
    """
    Decorador para registrar uma função como handler de um comando específico.

    Args:
        command (Type[C]): Classe do comando a ser tratado.

    Raises:
        ValueError: Se o CommandBus ainda não foi configurado via `set_command_bus`.

    Example:
        >>> @commandHandler(CreateUserCommand)
        ... def handle_create_user(cmd: CreateUserCommand) -> None:
        ...     print(f"Criando usuário {cmd.user_id}")
    """
    def decorator(function: CommandHandlerProtocol[C]) -> CommandHandlerProtocol[C]:
        BusManager().get_command_bus().subscribe(command.__name__, function)
        return function

    return decorator
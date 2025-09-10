from typing import Any, Protocol, TypeVar
from seisbai_contracts.core.artefacts import Command

# Tipo genérico para comandos, restrito a subclasses de Command.
# O `contravariant=True` permite passar handlers mais genéricos
# onde se espera um handler específico.
C = TypeVar("C", bound=Command, contravariant=True)


class CommandHandlerProtocol(Protocol[C]):
    """
    Protocolo para handlers de comandos.

    Um handler é qualquer objeto ou função que implemente __call__
    e que receba um comando do tipo C (subclasse de Command).
    O retorno é Any porque o resultado pode variar dependendo da implementação.

    Exemplos:
        def handle_create_user(cmd: CreateUserCommand) -> None:
            print(f"Criando usuário {cmd.user_id}")

        class SaveUserHandler:
            def __call__(self, cmd: Command) -> bool:
                # salva no banco e retorna sucesso/erro
                return True
    """

    def __call__(self, command: C) -> Any: ...
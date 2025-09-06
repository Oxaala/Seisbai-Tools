from typing import cast


class CommandAutoPublisherMixin:
    """
    Mixin que publica automaticamente instâncias de comandos no barramento.

    Qualquer classe que herde de `Command` e inclua este mixin terá seus objetos
    publicados no `CommandBus` logo após a inicialização. 

    O mixin percorre a hierarquia de herança (MRO) da instância criada e publica
    o mesmo objeto em todos os tópicos correspondentes às superclasses que
    herdam de `Command`. 

    Exemplo:
        class CriarUsuario(Command, CommandAutoPublisherMixin):
            nome: str

        >>> cmd = CriarUsuario(nome="Ana")
        # Publica em "CriarUsuario" e em "Command"
    """

    def __post_init__(self):
        # Import tardio para evitar dependências circulares
        from seisbai_contracts.config.buses import BusManager
        from seisbai_contracts.core.artefacts import Command

        bus = BusManager().get_command_bus()

        # Publica a instância em todos os tópicos correspondentes
        # às superclasses até chegar em Command
        for cls in self.__class__.mro():
            if issubclass(cls, Command):
                bus.publish(cls.__name__, cast(Command, self))
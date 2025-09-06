from typing import cast


class EventAutoPublisherMixin:
    """
    Mixin que publica automaticamente instâncias de eventos no barramento.

    Qualquer classe que herde de `Event` e inclua este mixin terá seus objetos
    publicados no `EventBus` logo após a inicialização.

    O mixin percorre a hierarquia de herança (MRO) da instância criada e publica
    o mesmo objeto em todos os tópicos correspondentes às superclasses que
    herdam de `Event`.

    Exemplo:
        class UsuarioCriadoEvent(Event, EventAutoPublisherMixin):
            user_id: str

        >>> evt = UsuarioCriadoEvent(user_id="123", correlation_id=None, causation_id=None)
        # Publica em "UsuarioCriadoEvent" e em "Event"
    """

    def __post_init__(self):
        # Import tardio para evitar dependências circulares
        from seisbai_contracts.config.buses import BusManager
        from seisbai_contracts.core.artefacts import Event

        bus = BusManager().get_event_bus()

        # Publica a instância em todos os tópicos correspondentes
        # às superclasses até chegar em Event
        for cls in self.__class__.mro():
            if issubclass(cls, Event):
                print(f"Publicou em {cls.__name__}\n")
                bus.publish(cls.__name__, cast(Event, self))
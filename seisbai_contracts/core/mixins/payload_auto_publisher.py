from typing import cast


class PayloadAutoPublisherMixin:
    """
    Mixin que publica automaticamente instâncias de payloads no barramento.

    Qualquer classe que herde de `Payload` e inclua este mixin terá seus objetos
    publicados no `PayloadBus` logo após a inicialização.

    O mixin percorre a hierarquia de herança (MRO) da instância criada e publica
    o mesmo objeto em todos os tópicos correspondentes às superclasses que
    herdam de `Payload`.

    Exemplo:
        class DadosUsuarioPayload(Payload, PayloadAutoPublisherMixin):
            user_id: str

        >>> payload = DadosUsuarioPayload(user_id="123")
        # Publica em "DadosUsuarioPayload" e em "Payload"
    """

    def __post_init__(self):
        # Import tardio para evitar dependências circulares
        from seisbai_contracts.config.buses import BusManager
        from seisbai_contracts.core.artefacts import Payload

        bus = BusManager().get_payload_bus()

        # Publica a instância em todos os tópicos correspondentes
        # às superclasses até chegar em Payload
        for cls in self.__class__.mro():
            if issubclass(cls, Payload):
                bus.publish(cls.__name__, cast(Payload, self))
from typing import Any, Protocol, TypeVar
from seisbai_contracs.core.artefacts.events.event import Event

# Tipo genérico para eventos, restrito a subclasses de Event.
# O `contravariant=True` significa que podemos usar um listener
# mais genérico em contextos que esperam um mais específico.
E = TypeVar("E", bound=Event, contravariant=True)


class EventListenerProtocol(Protocol[E]):
    """
    Protocolo para listeners de eventos.

    Um listener é qualquer objeto ou função que implemente __call__
    e que receba um evento do tipo E (subclasse de Event).
    Retorna Any porque o resultado do processamento do evento pode variar.

    Exemplos:
        def on_user_created(event: UserCreatedEvent) -> None:
            print(f"Usuário criado: {event.user_id}")

        class SaveToDB:
            def __call__(self, event: Event) -> bool:
                # salva no banco e retorna sucesso/erro
                return True
    """

    def __call__(self, event: E) -> Any: ...
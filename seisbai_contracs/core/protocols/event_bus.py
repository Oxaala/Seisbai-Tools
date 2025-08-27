from __future__ import annotations
from typing import Protocol, TypeVar

from seisbai_contracs.core.artefacts.event import Event
from seisbai_contracs.core.protocols.event_listener import EventListenerProtocol

# Tipo genérico para eventos, restrito a subclasses de Event
E = TypeVar("E", bound=Event)


class EventBusProtocol(Protocol):
    """
    Protocolo para um barramento de eventos (EventBus).

    Define os métodos que qualquer implementação de barramento de eventos
    deve fornecer: publicar eventos e registrar listeners (assinaturas).
    """

    def publish(self, topic: str, event: Event) -> None:
        """
        Publica um evento no tópico informado.

        Args:
            topic (str): Nome do tópico para publicação.
            event (Event): Instância do evento a ser publicada.
        """
        ...

    def subscribe(self, topic: str, callback: EventListenerProtocol[E]) -> None:
        """
        Assina um tópico com um callback.

        Args:
            topic (str): Nome do tópico a ser assinado.
            callback (EventListenerProtocol[E]): Função ou objeto chamável que
                será invocado quando um evento do tipo E for publicado neste tópico.
        """
        ...
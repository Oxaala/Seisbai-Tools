from __future__ import annotations
from typing import Protocol, TypeVar

from seisbai_contracts.core.artefacts.payload import Payload
from seisbai_contracts.core.protocols.gateway import GatewayProtocol

# Tipo genérico para payloads, restrito a subclasses de Payload
P = TypeVar("P", bound=Payload)


class PayloadBusProtocol(Protocol):
    """
    Protocolo para um barramento de payloads (PayloadBus).

    Define os métodos que qualquer implementação de barramento de payloads
    deve fornecer: publicar payloads e registrar handlers (assinaturas).
    """

    def publish(self, topic: str, payload: Payload) -> None:
        """
        Publica um payload no tópico informado.

        Args:
            topic (str): Nome do tópico para publicação.
            payload (Payload): Instância do payload a ser publicada.
        """
        ...

    def subscribe(self, topic: str, callback: GatewayProtocol[P]) -> None:
        """
        Assina um tópico com um callback.

        Args:
            topic (str): Nome do tópico a ser assinado.
            callback (GatewayProtocol[P]): Função ou objeto chamável
                que será invocado quando um payload do tipo P for publicado
                neste tópico.
        """
        ...
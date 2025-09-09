from abc import ABC, abstractmethod
from typing import Any, Callable

from .singleton import SingletonMeta


class IPublishSubscribe(ABC, metaclass=SingletonMeta):
    """
    Interface para um sistema de mensagens baseado no padrão Publish-Subscribe.

    Essa interface deve ser usada como contrato para implementação de mecanismos
    de comunicação assíncrona desacoplada, onde:
        - `publish` envia mensagens para um determinado tópico.
        - `subscribe` permite registrar callbacks para serem executados quando
          novas mensagens são publicadas nesse tópico.

    Como utiliza a metaclasse `SingletonMeta`, qualquer implementação desta
    interface será garantidamente um Singleton.

    Exemplo de implementação:
        class EventBus(IPublishSubscribe):
            def __init__(self):
                self._subscribers: dict[str, list[Callable[[Any], Any]]] = {}

            def publish(self, topic: str, **kwargs: Any) -> None:
                for callback in self._subscribers.get(topic, []):
                    callback(kwargs)

            def subscribe(self, topic: str, callback: Callable[[Any], Any]) -> None:
                self._subscribers.setdefault(topic, []).append(callback)
    """

    @abstractmethod
    def publish(self, topic: str, **kwargs: Any) -> None:
        """
        Publica dados em um tópico específico.

        Args:
            topic (str): Nome do tópico para o qual os dados devem ser enviados.
            **kwargs (Any): Dados adicionais a serem enviados aos assinantes.
        """
        raise NotImplementedError

    @abstractmethod
    def subscribe(self, topic: str, callback: Callable[[Any], Any]) -> None:
        """
        Assina um tópico específico.

        Args:
            topic (str): Nome do tópico a ser assinado.
            callback (Callable[[Any], Any]): Função que será chamada quando
                uma mensagem for publicada nesse tópico.
        """
        raise NotImplementedError
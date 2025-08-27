from typing import Type
from seisbai_contracs.core.protocols.event_listener import EventListenerProtocol, E
from seisbai_contracs.config import _state


def eventListener(event: Type[E]):
    """
    Decorador para registrar uma função como listener de um evento específico.

    Args:
        event (Type[E]): Classe do evento a ser ouvida.

    Raises:
        ValueError: Se o EventBus ainda não foi configurado via `set_event_bus`.

    Example:
        >>> @eventListener(UserCreatedEvent)
        ... def handle_user_created(event: UserCreatedEvent) -> None:
        ...     print(f"Novo usuário criado: {event.user_id}")
    """
    def decorator(function: EventListenerProtocol[E]) -> EventListenerProtocol[E]:
        if _state.event_bus is None:
            raise ValueError(
                "Event bus has not been configured. Use set_event_bus first."
            )

        _state.event_bus.subscribe(event.__name__, function)
        return function

    return decorator
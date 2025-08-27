from seisbai_contracs.core.protocols.command_bus import CommandBusProtocol
from seisbai_contracs.core.protocols.event_bus import EventBusProtocol
from seisbai_contracs.core.protocols.payload_bus import PayloadBusProtocol
from . import _state


def set_payload_bus(payload_bus: PayloadBusProtocol) -> None:
    """
    Define a implementação global de PayloadBus a ser usada pela biblioteca.

    Args:
        payload_bus: Implementação concreta de PayloadBusProtocol.
    """
    if _state.payload_bus is not None:
        raise RuntimeError("PayloadBus já foi configurado.")
    _state.payload_bus = payload_bus


def set_command_bus(command_bus: CommandBusProtocol) -> None:
    """
    Define a implementação global de CommandBus a ser usada pela biblioteca.

    Args:
        command_bus: Implementação concreta de CommandBusProtocol.
    """
    if _state.command_bus is not None:
        raise RuntimeError("CommandBus já foi configurado.")
    _state.command_bus = command_bus


def set_event_bus(event_bus: EventBusProtocol) -> None:
    """
    Define a implementação global de EventBus a ser usada pela biblioteca.

    Args:
        event_bus: Implementação concreta de EventBusProtocol.
    """
    if _state.event_bus is not None:
        raise RuntimeError("EventBus já foi configurado.")
    _state.event_bus = event_bus
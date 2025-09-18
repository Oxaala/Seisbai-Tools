from typing import Optional
from seisbai_contracts.interfaces.singleton import SingletonMeta
from seisbai_contracts.core.protocols.command_bus import CommandBusProtocol
from seisbai_contracts.core.protocols.event_bus import EventBusProtocol


class BusManager(metaclass=SingletonMeta):
    _command_bus: Optional[CommandBusProtocol] = None
    _event_bus: Optional[EventBusProtocol] = None

    def set_command_bus(self, bus: CommandBusProtocol) -> None:
        if self._command_bus is not None:
            raise RuntimeError("Command bus has already been configured.")
        self._command_bus = bus

    def get_command_bus(self) -> CommandBusProtocol:
        if self._command_bus is None:
            raise ValueError("Command bus has not been configured. Use set_command_bus first.")
        return self._command_bus

    def set_event_bus(self, bus: EventBusProtocol) -> None:
        if self._event_bus is not None:
            raise RuntimeError("Event bus has already been configured.")
        self._event_bus = bus

    def get_event_bus(self) -> EventBusProtocol:
        if self._event_bus is None:
            raise ValueError("Event bus has not been configured. Use set_event_bus first.")
        return self._event_bus
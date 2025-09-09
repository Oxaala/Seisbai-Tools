from typing import Optional
from seisbai_contracts.core.interfaces.singleton import SingletonMeta
from seisbai_contracts.core.protocols.command_bus import CommandBusProtocol
from seisbai_contracts.core.protocols.event_bus import EventBusProtocol
from seisbai_contracts.core.protocols.payload_bus import PayloadBusProtocol


class BusManager(metaclass=SingletonMeta):
    _command_bus: Optional[CommandBusProtocol] = None
    _event_bus: Optional[EventBusProtocol] = None
    _payload_bus: Optional[PayloadBusProtocol] = None

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

    def set_payload_bus(self, bus: PayloadBusProtocol) -> None:
        if self._payload_bus is not None:
            raise RuntimeError("Payload bus has already been configured.")
        self._payload_bus = bus

    def get_payload_bus(self) -> PayloadBusProtocol:
        if self._payload_bus is None:
            raise RuntimeError("Payload bus has not been configured. Use set_payload_bus first.")
        return self._payload_bus
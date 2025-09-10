from abc import ABC, abstractmethod
from uuid import uuid4
from pubsub import pub
from dataclasses import dataclass

from seisbai_contracts.core.artefacts.events.event import Event
from seisbai_contracts.core.artefacts.events.failed import FailedEvent
from seisbai_contracts.core.artefacts.events.paused import PausedEvent
from seisbai_contracts.core.artefacts.payload import Payload
from seisbai_contracts.core.decorators.event_listener import eventListener
from seisbai_contracts.core.decorators.gateway import gateway
from seisbai_contracts.core.protocols.event_listener import EventListenerProtocol
from seisbai_contracts.core.protocols.gateway import GatewayProtocol

from seisbai_contracts.config import BusManager
from seisbai_contracts.core.protocols.event_bus import EventBusProtocol
from seisbai_contracts.core.protocols.payload_bus import PayloadBusProtocol

# ----------------------------
# Implementações do Bus
# ----------------------------
class PybubsubEventBus(EventBusProtocol):
    def __init__(self) -> None:
        self._bus = pub

    def publish(self, topic: str, event: Event) -> None:
        self._bus.sendMessage(topic, event=event)

    def subscribe(self, topic: str, callback: EventListenerProtocol[Event]) -> None:
        self._bus.subscribe(callback, topic)

class PybubsubPayloadBus(PayloadBusProtocol):
    def __init__(self) -> None:
        self._bus = pub

    def publish(self, topic: str, payload: Payload) -> None:
        self._bus.sendMessage(topic, payload=payload)

    def subscribe(self, topic: str, callback: GatewayProtocol[Payload]) -> None:
        self._bus.subscribe(callback, topic)

# ----------------------------
# Configuração do BusManager
# ----------------------------
BusManager().set_event_bus(PybubsubEventBus())
BusManager().set_payload_bus(PybubsubPayloadBus())

# ----------------------------
# DTO e Payload
# ----------------------------
@dataclass
class DummyDTO:
    value: int
    text: str

dto = DummyDTO(value=42, text="hello")

payload = Payload(
    token="abc123",
    user_id=uuid4(),
    data=dto,
)

event = FailedEvent(id=uuid4(), correlation_id=uuid4(), causation_id=uuid4(), task_id=uuid4())

# ----------------------------
# Funções normais
# ----------------------------
@eventListener(FailedEvent)
def handle_failed(event: FailedEvent):
    print(f"[EventListener] Função normal recebeu: {event.id}")

@gateway(Payload)
def handle_payload(payload: Payload):
    print(f"[Gateway] Função normal recebeu: {payload.data}")
    return {"ok": True}
"""
# ----------------------------
# Métodos de instância abstratos
# ----------------------------
class ServiceAbstract(ABC):
    @eventListener(FailedEvent)
    @abstractmethod
    def handle_failed_inst(self, event: FailedEvent):
        print(f"[EventListener] Instância abstrata Evento: {event.id}")
    @gateway(Payload)
    @abstractmethod
    def gateway_inst(self, payload: Payload):
        print(f"[Gateway] Instância abstrata Payload: {payload.data}")
        return {"ok": True}
"""

# ----------------------------
# Métodos de instância normais
# ----------------------------
class ServiceNormal:
    def handle_failed_inst(self, event: FailedEvent):
        print(f"[EventListener] Instância normal Evento: {event.id}")
    
    def gateway_inst(self, payload: Payload):
        print(f"[Gateway] Instância normal Payload: {payload.data}")
        return {"ok": True}

# Create instance and register methods
service_normal = ServiceNormal()
BusManager().get_event_bus().subscribe(FailedEvent.__name__, service_normal.handle_failed_inst)
BusManager().get_payload_bus().subscribe(Payload.__name__, service_normal.gateway_inst)

# ----------------------------
# Métodos estáticos
# ----------------------------
class ServiceStatic:
    @staticmethod
    def handle_failed_static(event: FailedEvent):
        print(f"[EventListener] Static Evento: {event.id}")

    @staticmethod
    def gateway_static(payload: Payload):
        print(f"[Gateway] Static Payload: {payload.data}")
        return {"ok": True}

# Register static methods
BusManager().get_event_bus().subscribe(FailedEvent.__name__, ServiceStatic.handle_failed_static)
BusManager().get_payload_bus().subscribe(Payload.__name__, ServiceStatic.gateway_static)

# ----------------------------
# Métodos de classe
# ----------------------------
class ServiceClassMethod:
    @classmethod
    def handle_failed_class(cls, event: FailedEvent):
        print(f"[EventListener] Classmethod Evento: {event.id}")

    @classmethod
    def gateway_class(cls, payload: Payload):
        print(f"[Gateway] Classmethod Payload: {payload.data}")
        return {"ok": True}

# Register class methods
BusManager().get_event_bus().subscribe(FailedEvent.__name__, ServiceClassMethod.handle_failed_class)
BusManager().get_payload_bus().subscribe(Payload.__name__, ServiceClassMethod.gateway_class)

# ----------------------------
# Testando a publicação
# ----------------------------
print("\n--- TESTANDO EVENT LISTENERS ---")
BusManager().get_event_bus().publish(FailedEvent.__name__, event)

print("\n--- TESTANDO GATEWAYS ---")
BusManager().get_payload_bus().publish(Payload.__name__, payload)
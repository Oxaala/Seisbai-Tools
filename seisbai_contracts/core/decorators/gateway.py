from typing import Type
from seisbai_contracts.config.buses import BusManager
from seisbai_contracts.core.protocols.gateway import GatewayProtocol, P


def gateway(payload: Type[P]):
    """
    Decorador para registrar uma função como um gateway em um serviço específico.

    Args:
        service: Nome do serviço no qual a função será registrada.

    Raises:
        ValueError: Se o payload bus ainda não foi configurado 
                    via `set_payload_bus`.

    Example:
        >>> @gateway("user.create")
        ... def create_user(data: dict) -> dict:
        ...     return {"id": 123, **data}
    """
    def decorator(function: GatewayProtocol[P]) -> GatewayProtocol[P]:
        BusManager().get_payload_bus().subscribe(payload.__name__, function)
        return function

    return decorator
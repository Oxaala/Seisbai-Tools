from typing import Any, Protocol, TypeVar
from seisbai_contracts.core.artefacts.payload import Payload

# Tipo genérico para payloads, restrito a subclasses de Payload.
# O `contravariant=True` permite passar handlers mais genéricos
# onde se espera um handler específico.
P = TypeVar("P", bound=Payload, contravariant=True)


class GatewayProtocol(Protocol[P]):
    """
    Protocolo para handlers de payloads em gateways.

    Um handler é qualquer objeto ou função que implemente __call__
    e que receba um payload do tipo P (subclasse de Payload).
    O retorno é Any porque o resultado do processamento pode variar.

    Exemplos:
        def send_user_payload(payload: UserPayload) -> None:
            print(f"Enviando payload do usuário {payload.user_id}")

        class ExternalAPISender:
            def __call__(self, payload: Payload) -> bool:
                # envia para API externa e retorna sucesso/erro
                return True
    """

    def __call__(self, payload: P) -> Any: ...
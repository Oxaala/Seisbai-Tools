from typing import Any, Dict, Literal, Type, TypeVar
from uuid import UUID

from msgspec import field
import msgspec
from .base import Base

# Registro global de DTOs para deserialização
_relations: Dict[str, Type[Any]] = {}

Services = Literal["DataGenerator", "FaultDetector", "HorizonInterpolator"]

T = TypeVar("T")

class Payload(Base, frozen=True, kw_only=True):
    """
    Representa um **payload** genérico enviado no sistema.

    O payload contém os dados de negócio ou de controle associados a um comando
    ou evento. Ele herda de :class:`Base`, possuindo também ``id`` e ``timestamp``.

    Todos os campos devem ser fornecidos na criação do objeto, nenhum é opcional.

    Attributes
    ----------
    id : uuid.UUID
        Identificador único do payload, herdado de :class:`Base`.

    timestamp : datetime.datetime
        Data e hora exata da criação do payload, em UTC, herdado de :class:`Base`.

    token : str
        Token de autenticação. Deve ser fornecido na criação do Payload.

    user_id : UUID
        Identificador único do usuário. Deve ser fornecido na criação do Payload.

    service : Literal["Datagen", "FaultDetector", "HorizonInterpolator"]
        Serviço de destino do payload. Deve ser um dos valores listados.

    dto_name : str
        Nome do DTO (Data Transfer Object) associado a este payload.
        Usado para identificar a estrutura de dados carregada na hora da deserialização.

    data : bytes
        Conteúdo bruto do objeto contendo os dados serializados em JSON.
    """

    token: str = field() #type: ignore
    user_id: UUID = field() #type: ignore
    service: Services = field() #type: ignore
    dto_name: str = field() #type: ignore
    data: bytes = field() #type: ignore

    def serialize(self) -> bytes:
        """
        Serializa o Payload em JSON como bytes.

        Returns
        -------
        bytes
            Representação JSON do Payload.
        """
        return msgspec.json.encode(self)

    def deserialize(self, content: bytes, dto_type: Type[T]) -> T:
        """
        Deserializa o conteúdo JSON em um DTO do tipo esperado.

        Parameters
        ----------
        content : bytes
            Conteúdo JSON em bytes representando um Payload.
        dto_type : Type[T]
            O tipo de DTO esperado.

        Returns
        -------
        T
            Instância do DTO correspondente ao tipo esperado.

        Raises
        ------
        ValueError
            Se o `dto_name` presente no Payload não corresponder ao DTO esperado
            ou se não estiver registrado em `_relations`.
        """
        payload_instance = msgspec.json.decode(content, type=Payload)

        registered_type = _relations.get(payload_instance.dto_name)
        if registered_type is None:
            raise ValueError(f"DTO '{payload_instance.dto_name}' is not registered in _relations")

        if registered_type is not dto_type:
            raise ValueError(
                f"Expected type '{dto_type.__name__}', but the Payload contains '{payload_instance.dto_name}'"
            )

        return msgspec.json.decode(payload_instance.data, type=dto_type)
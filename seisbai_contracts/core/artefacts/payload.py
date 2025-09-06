from typing import List, Literal, Optional, Type, TypeVar
from uuid import UUID

from msgspec import field
import msgspec
from .base import Base
import importlib
from seisbai_contracts.core.mixins import PayloadAutoPublisherMixin


def get_import_path(cls: type) -> str:
    """
    Retorna o caminho de importação completo de uma classe.

    Parameters
    ----------
    cls : type
        Classe Python a ser inspecionada.

    Returns
    -------
    str
        Caminho de importação no formato ``modulo.submodulo.Classe``.
    """
    return f"{cls.__module__}.{cls.__qualname__}"


def import_type(path: str) -> type:
    """
    Importa dinamicamente um tipo a partir de seu caminho completo.

    Parameters
    ----------
    path : str
        Caminho completo no formato ``modulo.submodulo.Classe``.

    Returns
    -------
    type
        Classe ou tipo importado.

    Raises
    ------
    ModuleNotFoundError
        Se o módulo especificado não existir.
    AttributeError
        Se a classe não for encontrada dentro do módulo.
    """
    module_name, class_name = path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


Service = Literal["DataGenerator", "FaultDetector", "HorizonInterpolator"]
"""Tipo literal que representa os serviços válidos no sistema."""

services: List[Service] = ["DataGenerator", "FaultDetector", "HorizonInterpolator"]
"""Lista de serviços suportados pelo sistema."""


T = TypeVar("T")
"""Tipo genérico usado para parametrizar DTOs."""


class Payload(Base, PayloadAutoPublisherMixin, frozen=True, kw_only=True):
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

    service : Literal["DataGenerator", "FaultDetector", "HorizonInterpolator"]
        Serviço de destino do payload. Deve ser um dos valores listados.

    dto_path : str
        Caminho de importação completo (ex.: ``meu_modulo.submodulo.ClasseDTO``)
        da classe DTO associada a este payload. Usado para reconstruir
        automaticamente o tipo do DTO na desserialização.

    dto_name : str
        Nome do DTO (Data Transfer Object) associado a este payload.
        Útil para fins de auditoria e identificação sem precisar importar o tipo.

    data : bytes
        Conteúdo bruto do objeto contendo os dados serializados em JSON.
    """

    token: str = field()  # type: ignore
    user_id: UUID = field()  # type: ignore
    service: Service = field()  # type: ignore
    dto_path: str = field()  # type: ignore
    dto_name: str = field()  # type: ignore
    data: bytes = field()  # type: ignore

    def serialize(self) -> bytes:
        """
        Serializa o Payload em JSON como bytes.

        Returns
        -------
        bytes
            Representação JSON do Payload serializado.
        """
        return msgspec.json.encode(self)

    def deserialize(self, dto_type: Optional[Type[T]] = None) -> T:
        """
        Deserializa o conteúdo JSON do campo ``data`` em um DTO.

        Se nenhum tipo for informado, a função utilizará automaticamente
        o caminho definido em ``dto_path`` para importar o DTO correto.

        Parameters
        ----------
        dto_type : Type[T], optional
            O tipo de DTO esperado. Caso não seja fornecido, será usado
            o tipo indicado em ``dto_path``.

        Returns
        -------
        T
            Instância do DTO correspondente.

        Raises
        ------
        ValueError
            Se não for possível importar o tipo especificado em ``dto_path``
            ou se o JSON contido em ``data`` não corresponder à estrutura esperada.
        """
        if dto_type is None:
            dto_type = import_type(self.dto_path)

        return msgspec.json.decode(self.data, type=dto_type)
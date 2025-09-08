from typing import List, Literal, Optional, Type, TypeVar
from uuid import UUID
from msgspec import field
import msgspec
from .base import Base
import importlib
from seisbai_contracts.core.mixins import PayloadAutoPublisherMixin


def _get_import_path(cls: type) -> str:
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


def _import_type(path: str) -> type:
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

    Attributes
    ----------
    token : str
        Token de autenticação. Deve ser fornecido na criação do Payload.

    user_id : UUID
        Identificador único do usuário. Deve ser fornecido na criação do Payload.

    service : Literal["DataGenerator", "FaultDetector", "HorizonInterpolator"]
        Serviço de destino do payload. Deve ser um dos valores listados.

    data : T
        Objeto de dados (DTO) associado ao payload. Pode ser qualquer tipo
        serializável em JSON pelo ``msgspec``.

    send : bool
        Indica se o payload deve ser efetivamente publicado no EventBus.
        Útil para cenários de teste ou controle de fluxo. Valor padrão: ``True``.
    """

    token: str = field()
    user_id: UUID = field()
    service: Service = field()
    data: T = field()
    send: bool = field(default=True)

    @property
    def _dto_path(self) -> str:
        """
        Caminho de importação completo do DTO associado a ``data``.

        Exemplo
        -------
        ``meu_modulo.submodulo.ClasseDTO``
        """
        return _get_import_path(type(self.data))

    @property
    def _encoded_data(self) -> bytes:
        """
        Representação serializada do ``data`` em JSON (bytes).

        Returns
        -------
        bytes
            Conteúdo JSON serializado. Se ``data`` já for ``bytes``,
            retorna o valor original.
        """
        if isinstance(self.data, bytes):
            return self.data
        return msgspec.json.encode(self.data)

    def serialize(self) -> bytes:
        """
        Serializa o Payload inteiro em JSON (bytes).

        Returns
        -------
        bytes
            Representação JSON do Payload serializado.
        """
        return msgspec.json.encode(self)

    def deserialize(self, dto_type: Optional[Type[T]] = None) -> T:
        """
        Desserializa o conteúdo do campo ``data`` em um DTO.

        Se nenhum tipo for informado, a função utilizará automaticamente
        o caminho definido em ``_dto_path`` para importar o tipo correto.

        Parameters
        ----------
        dto_type : Type[T], optional
            Tipo esperado para o DTO. Caso não seja fornecido, será usado
            o tipo indicado por ``_dto_path``.

        Returns
        -------
        T
            Instância do DTO correspondente.

        Raises
        ------
        ValueError
            Se não for possível importar o tipo especificado em ``_dto_path``
            ou se o JSON contido em ``data`` não corresponder à estrutura esperada.
        """
        if dto_type is None:
            dto_type = _import_type(self._dto_path)

        return msgspec.json.decode(self._encoded_data, type=dto_type)
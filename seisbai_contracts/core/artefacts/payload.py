from typing import Optional, Type, TypeVar
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


T = TypeVar("T")
"""Tipo genérico usado para parametrizar DTOs."""


class Payload(Base, PayloadAutoPublisherMixin, frozen=True, kw_only=True):
    """
    Payload genérico enviado no sistema, encapsulando dados de comandos ou eventos.

    Um *payload* transporta de forma segura e explícita os dados de negócio ou controle
    associados a comandos e eventos. Ele herda de :class:`Base` (possui ``id`` e ``timestamp``)
    e incorpora o mixin :class:`PayloadAutoPublisherMixin`, permitindo publicação automática
    no *bus* configurado.

    Atributos
    ----------
    token : str
        Token de autenticação fornecido no momento da criação.

    user_id : UUID
        Identificador único do usuário associado ao payload.

    data : T
        Objeto de dados (DTO) encapsulado no payload. Deve ser serializável em JSON pelo
        `msgspec`. Pode ser qualquer dataclass ou estrutura compatível.

    send : bool, default=True
        Define se o payload deve ser publicado automaticamente no bus.
        Útil para cenários de teste ou para instanciar o payload sem enviá-lo.

    dto_path : str
        Caminho de importação completo do tipo do DTO (`data`). Preenchido automaticamente
        se não informado, no formato ``modulo.submodulo.ClasseDTO``.

    Propriedades
    ------------
    _encoded_data : bytes
        Representação serializada de ``data`` em JSON. Se ``data`` já for ``bytes``,
        retorna o valor original.

    Métodos
    -------
    serialize() -> bytes
        Serializa o payload completo (metadados + DTO) em JSON.

    deserialize(dto_type: Optional[Type[T]] = None) -> T
        Desserializa o conteúdo de ``data`` em uma instância do tipo DTO especificado.
        Se ``dto_type`` não for informado, o tipo é determinado automaticamente a partir
        de ``dto_path``.

    Exemplo
    -------
    >>> from uuid import uuid4
    >>> from dataclasses import dataclass
    >>> 
    >>> @dataclass
    ... class DummyDTO:
    ...     value: int
    ...     text: str
    ...
    >>> dto = DummyDTO(value=42, text="hello")
    >>> payload = Payload(token="abc123", user_id=uuid4(), data=dto)
    >>> raw = payload.serialize()
    >>> decoded = payload.deserialize(DummyDTO)
    >>> assert isinstance(decoded, DummyDTO)
    >>> assert decoded.value == 42
    """

    token: str = field()
    user_id: UUID = field()
    data: T = field()
    send: bool = field(default=True)
    dto_path: str = field(default="")

    def __post_init__(self):
        if not self.dto_path:
            object.__setattr__(self, "dto_path", _get_import_path(type(self.data)))
        
        try:
            super().__post_init__()
        except AttributeError:
            pass

    @property
    def _encoded_data(self) -> bytes:
        """
        Representação serializada do ``data`` em JSON.

        Returns
        -------
        bytes
            Conteúdo JSON serializado em bytes. Se ``data`` já for
            ``bytes``, retorna o valor original sem transformação.
        """
        if isinstance(self.data, bytes):
            return self.data
        return msgspec.json.encode(self.data)

    def serialize(self) -> bytes:
        """
        Serializa o payload inteiro (metadados + DTO) em JSON.

        Returns
        -------
        bytes
            Representação JSON serializada do payload.
        """
        return msgspec.json.encode(self)

    def deserialize(self, dto_type: Optional[Type[T]] = None) -> T:
        """
        Desserializa o conteúdo do campo ``data`` em um DTO.

        Parameters
        ----------
        dto_type : Type[T], optional
            Tipo esperado para o DTO. Se não for informado, o tipo é
            inferido automaticamente a partir de ``_dto_path``.

        Returns
        -------
        T
            Instância do DTO correspondente.

        Raises
        ------
        ValueError
            Se não for possível importar o tipo em ``_dto_path`` ou se o
            conteúdo JSON não corresponder à estrutura esperada.
        """
        if dto_type is None:
            dto_type = _import_type(self.dto_path)

        return msgspec.json.decode(self._encoded_data, type=dto_type)
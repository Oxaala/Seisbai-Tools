from datetime import datetime, timezone
from typing import Optional, Type, TypeVar
from uuid import UUID, uuid4
from msgspec import Struct, field
import msgspec
import importlib


def _get_import_path(cls: type) -> str:
    """
    Retorna o caminho de importação completo de uma classe ou tipo.

    Parameters
    ----------
    cls : type
        Classe ou tipo Python a ser inspecionado.

    Returns
    -------
    str
        Caminho no formato ``modulo.submodulo.Classe``.
    
    Examples
    --------
    >>> from datetime import datetime
    >>> _get_import_path(datetime)
    'datetime.datetime'
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
        Tipo ou classe importada.

    Raises
    ------
    ModuleNotFoundError
        Se o módulo especificado não existir.
    AttributeError
        Se a classe ou tipo não for encontrado dentro do módulo.

    Examples
    --------
    >>> dt_type = _import_type("datetime.datetime")
    >>> from datetime import datetime
    >>> assert dt_type is datetime
    """
    module_name, class_name = path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


T = TypeVar("T")
"""Tipo genérico usado para parametrizar o campo `payload`."""


class Package(Struct, kw_only=True):
    """
    Estrutura genérica de transporte (payload) utilizada para encapsular e transmitir dados
    no sistema de mensageria.

    O `Package` funciona como um contêiner de dados que:
    - agrega metadados de rastreabilidade (`id`, `timestamp`, `dto_path`),
    - armazena o objeto de negócio ou controle em `payload`,
    - e garante serialização/desserialização eficiente com `msgspec`.

    Attributes
    ----------
    id : uuid.UUID
        Identificador único universal (UUID) do pacote.  
        Gerado automaticamente com ``uuid4()`` se não informado.

    timestamp : datetime.datetime
        Data e hora da criação do pacote, sempre em UTC.  
        Útil para auditoria, ordenação temporal e depuração.

    token : str
        Token de autenticação associado ao pacote.  
        Usado para identificar ou validar a origem do envio.

    payload : T
        Objeto de dados encapsulado no pacote.  
        Pode ser qualquer DTO compatível com serialização JSON via `msgspec`, 
        ou ``bytes`` (caso em que não será re-serializado).

    dto_path : str
        Caminho de importação completo do tipo do objeto em `payload`.  
        É preenchido automaticamente no formato ``modulo.submodulo.Classe`` 
        quando o pacote é inicializado.

    Properties
    ----------
    _encoded_payload : bytes
        Representação serializada do campo ``payload`` em JSON.  
        Se ``payload`` já for ``bytes``, retorna o valor original.

    Methods
    -------
    serialize() -> bytes
        Serializa o pacote inteiro (metadados + payload) em JSON.

    deserialize(dto_type: Optional[Type[T]] = None) -> T
        Converte o conteúdo serializado de ``payload`` em uma instância do tipo DTO esperado.  
        Se ``dto_type`` não for informado, o tipo é inferido a partir de ``dto_path``.

    Examples
    --------
    >>> from uuid import uuid4
    >>> from dataclasses import dataclass
    >>>
    >>> @dataclass
    ... class DummyDTO:
    ...     value: int
    ...     text: str
    ...
    >>> dto = DummyDTO(value=42, text="hello")
    >>> pkg = Package(token="abc123", payload=dto)
    >>> raw = pkg.serialize()
    >>> decoded = pkg.deserialize(DummyDTO)
    >>> assert isinstance(decoded, DummyDTO)
    >>> assert decoded.value == 42
    """

    id: UUID = field(default_factory=lambda: uuid4())
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    token: str = field()
    payload: T = field()
    dto_path: str = field(default="")

    def __post_init__(self):
        """Define automaticamente o caminho de importação (`dto_path`) do tipo do `payload`."""
        if self.dto_path == "":
            self.dto_path = _get_import_path(type(self.payload))

    @property
    def _encoded_payload(self) -> bytes:
        """
        Retorna a representação serializada do ``payload`` em JSON.

        Returns
        -------
        bytes
            Conteúdo JSON serializado em bytes.  
            Se ``payload`` já for ``bytes``, retorna o valor original.
        """
        if isinstance(self.payload, bytes):
            return self.payload
        return msgspec.json.encode(self.payload)

    def serialize(self) -> bytes:
        """
        Serializa o pacote inteiro (metadados + payload) em JSON.

        Returns
        -------
        bytes
            Representação JSON serializada do pacote.
        """
        return msgspec.json.encode(self)

    def deserialize(self, dto_type: Optional[Type[T]] = None) -> T:
        """
        Converte o conteúdo serializado do campo ``payload`` em um DTO.

        Parameters
        ----------
        dto_type : Type[T], optional
            Tipo esperado para o DTO.  
            Se não for informado, o tipo é inferido automaticamente a partir de ``dto_path``.

        Returns
        -------
        T
            Instância do DTO correspondente ao ``payload``.

        Raises
        ------
        ValueError
            Se não for possível importar o tipo indicado em ``dto_path`` 
            ou se o conteúdo JSON não corresponder à estrutura esperada.
        """
        if dto_type is None:
            dto_type = _import_type(self.dto_path)

        return msgspec.json.decode(self._encoded_payload, type=dto_type)
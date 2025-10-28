from ulid import ULID, new as newULID
from msgspec import Struct, field

from ..pub_sub.mixins import AutoPublishMixin
from ..eda.mixins import AutoLoggerMixin


class Base(Struct, AutoPublishMixin, AutoLoggerMixin, frozen=True, kw_only=True):
    """
    Classe base imutável para comandos e eventos no sistema.

    Define um contrato mínimo para entidades que trafegam no barramento,
    garantindo que todas possuam:
    - um identificador único ULID,
    - um carimbo de tempo derivado do ULID (UTC),
    - uma mensagem descritiva.

    A biblioteca `msgspec` é utilizada por ser altamente otimizada para validação
    e serialização de dados, oferecendo desempenho comparável a formatos binários.

    Attributes
    ----------
    message : str
        Texto descritivo associado ao comando/evento.
        Útil para logs, depuração ou metadados adicionais.
        Padrão: vazio.

    Properties
    ----------
    id : ULID
        Identificador único da instância (internamente armazenado como `_id`).

    timestamp : datetime
        Data/hora UTC derivada do ULID, acessível via `obj.timestamp`.
        Essencial para ordenação temporal, auditoria e mensageria.
    """
    _id: ULID = field(default_factory=lambda: newULID())
    message: str = field(default="")

    def __post_init__(self):
        AutoPublishMixin.__post_init__(self)
        AutoLoggerMixin.__post_init__(self)

    @property
    def id(self):
        return self._id
    
    @property
    def timestamp(self):
        return self._id.timestamp().datetime
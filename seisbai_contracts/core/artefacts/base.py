from datetime import datetime, timezone
from uuid import UUID, uuid4
from msgspec import Struct, field

class Base(Struct, frozen=True, kw_only=True):
    """
    Classe base imutável para comandos e eventos no sistema.

    Define um contrato mínimo para entidades que trafegam no barramento,
    garantindo que todas possuam:
    - um identificador único,
    - um carimbo de tempo em UTC,
    - uma mensagem descritiva,
    - e um identificador de conexão WebSocket associado.

    A biblioteca `msgspec` é utilizada em vez de `dataclasses` ou `pydantic`
    por ser altamente otimizada para validação e serialização de dados,
    oferecendo desempenho comparável a formatos binários como `protobuf` ou `avro`.

    Attributes
    ----------
    id : uuid.UUID
        Identificador único universal (UUID) da instância.  
        Gerado automaticamente com ``uuid4()`` se não informado.  
        Útil para rastrear comandos/eventos de forma unívoca em sistemas distribuídos.

    timestamp : datetime.datetime
        Data e hora da criação do objeto, sempre em UTC.  
        Essencial para ordenação temporal, auditoria, depuração e mensageria.

    message : str
        Texto descritivo ou informativo associado ao comando/evento.  
        Pode ser usado para logs, debugging ou metadados adicionais.

    ws_connection_id : uuid.UUID
        Identificador da conexão WebSocket associada ao comando/evento.  
        Obrigatório, utilizado para rastrear interações em sistemas distribuídos
        orientados a conexões.
    """
    id: UUID = field(default_factory=lambda: uuid4())
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    message: str = field(default="")
    ws_connection_id: UUID = field()
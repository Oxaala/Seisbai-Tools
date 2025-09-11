from uuid import UUID, uuid4
from seisbai_contracts.core.artefacts.commands import PauseCommand
from msgspec import field


class PauseNetworkConstructorJobCommand(PauseCommand, frozen=True, kw_only=True):
    """
    Comando emitido para pausar a execução de um job de construção de rede.

    Em arquiteturas baseadas em mensageria, este comando representa uma
    instrução explícita para interromper temporariamente o processamento
    de um job em andamento, permitindo que seja retomado posteriormente.

    Herda de :class:`PauseCommand`.

    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset associado ao job de construção de rede
        que deve ser pausado.  
        Gerado automaticamente com ``uuid4()`` caso não seja informado.
    """
    dataset_id: UUID = field(default_factory=lambda: uuid4())
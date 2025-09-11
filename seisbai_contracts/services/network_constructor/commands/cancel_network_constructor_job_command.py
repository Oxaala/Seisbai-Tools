from uuid import UUID, uuid4
from seisbai_contracts.core.artefacts.commands import CancelCommand
from msgspec import field


class CancelNetworkConstructorJobCommand(CancelCommand, frozen=True, kw_only=True):
    """
    Comando emitido para cancelar a execução de um job de construção de rede.

    Em arquiteturas baseadas em mensageria, este comando representa uma
    instrução explícita para interromper o processamento de um job em andamento
    antes de sua conclusão.

    Herda de :class:`CancelCommand`.

    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset associado ao job de construção de rede
        que deve ser cancelado.  
        Gerado automaticamente com ``uuid4()`` caso não seja informado.
    """
    dataset_id: UUID = field(default_factory=lambda: uuid4())
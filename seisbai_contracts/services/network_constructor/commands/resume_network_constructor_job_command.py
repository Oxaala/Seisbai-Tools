from uuid import UUID, uuid4
from seisbai_contracts.core.artefacts.commands import ResumeCommand
from msgspec import field


class ResumeNetworkConstructorJobCommand(ResumeCommand, frozen=True, kw_only=True):
    """
    Comando emitido para retomar a execução de um job de construção de rede previamente pausado.

    Em arquiteturas baseadas em mensageria, este comando representa uma
    instrução explícita para reiniciar o processamento de um job que havia
    sido pausado anteriormente.

    Herda de :class:`ResumeCommand`.

    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset associado ao job de construção de rede
        que deve ser retomado.  
        Gerado automaticamente com ``uuid4()`` caso não seja informado.
    """
    dataset_id: UUID = field(default_factory=lambda: uuid4())
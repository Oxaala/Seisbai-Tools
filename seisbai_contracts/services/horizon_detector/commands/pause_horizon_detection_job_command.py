from uuid import UUID, uuid4
from msgspec import field
from seisbai_contracts.core.artefacts.commands import PauseCommand


class PauseHorizonDetectionJobCommand(PauseCommand, frozen=True, kw_only=True):
    """
    Comando para solicitar a pausa de um job de detecção de horizontes.

    Este comando herda de :class:`PauseCommand` e adiciona o contexto do dataset
    relacionado à tarefa a ser pausada.

    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset associado ao job de detecção de horizontes.
        Gerado automaticamente com `uuid4()` caso não seja informado.
    """
    dataset_id: UUID = field(default_factory=lambda: uuid4())
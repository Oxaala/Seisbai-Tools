from uuid import UUID, uuid4
from msgspec import field
from ....commands import CancelCommand


class CancelHorizonDetectionJobCommand(CancelCommand, frozen=True, kw_only=True):
    """
    Comando para solicitar o cancelamento de um job de detecção de horizontes.

    Este comando herda de :class:`CancelCommand` e adiciona o contexto do dataset
    relacionado à tarefa a ser cancelada.

    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset associado ao job de detecção de horizontes.
        Gerado automaticamente com `uuid4()` caso não seja informado.
    """
    dataset_id: UUID = field(default_factory=lambda: uuid4())
from msgspec import field
from typing import Optional
from uuid import UUID

from seisbai_contracs.core.Command import Command


class CancelSeismicCubeDatasetGenerationCommand(Command, frozen=True, kw_only=True):
    """
    Comando que solicita o cancelamento da geração de um dataset de cubo sísmico.

    Esse comando é utilizado para notificar o sistema de que o processo de geração
    de um dataset de cubo sísmico deve ser interrompido. Inclui o identificador do
    dataset e, opcionalmente, um motivo para o cancelamento.

    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset cuja geração deve ser cancelada.
    reason : Optional[str], default=None
        Motivo opcional para o cancelamento. Pode ser utilizado para fornecer
        contexto adicional (por exemplo: decisão do usuário, erro detectado,
        restrições de recursos).
    """

    dataset_id: UUID  # type: ignore
    reason: Optional[str] = field(default=None)
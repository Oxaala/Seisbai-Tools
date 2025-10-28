from uuid import UUID
from ....commands import CancelCommand


class CancelSeismicCubeDatasetGenerationCommand(CancelCommand, frozen=True, kw_only=True):
    """
    Comando que solicita o cancelamento da geração de um dataset de cubo sísmico.

    Esse comando é utilizado para notificar o sistema de que o processo de geração
    de um dataset de cubo sísmico deve ser interrompido. Inclui o identificador do
    dataset e, opcionalmente, um motivo para o cancelamento.

    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset cuja geração deve ser cancelada.
    """

    dataset_id: UUID
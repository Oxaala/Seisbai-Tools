from seisbai_contracs.core import Event
from uuid import UUID
from typing import List


class SeismicCubeDatasetGenerationCompletedEvent(Event, frozen=True):
    """
    Evento emitido quando a geração de um dataset de cubo sísmico termina com sucesso.

    Esse evento é disparado após a conclusão do processo de geração do dataset,
    contendo o identificador do dataset e os caminhos dos arquivos gerados.

    Attributes
    ----------
    dataset_id : UUID
        Identificador único do dataset que foi gerado.
    output_paths : List[str]
        Lista de caminhos dos arquivos de saída gerados pelo processo.
    """

    dataset_id: UUID  # type: ignore
    output_paths: List[str]  # type: ignore
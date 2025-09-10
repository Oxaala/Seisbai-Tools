from typing import List
from uuid import UUID
from seisbai_contracts.core.artefacts.events.finished import FinishedEvent


class FaultDetectionCompletedEvent(FinishedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando um job de detecção de falhas é concluído com sucesso.

    Este evento indica que o processamento do dataset foi finalizado
    e fornece os caminhos dos arquivos de saída gerados.

    Attributes
    ----------
    dataset_id : UUID
        Identificador único do dataset associado ao job.
    
    output_paths : List[str]
        Lista de caminhos para os arquivos de saída resultantes do processamento,
        como imagens de falhas, mapas de probabilidades ou dados processados.
    """
    dataset_id: UUID
    output_paths: List[str]
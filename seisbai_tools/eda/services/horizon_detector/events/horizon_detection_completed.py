from typing import List
from uuid import UUID
from ....events import CompletedEvent


class HorizonDetectionCompletedEvent(CompletedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando o processo de detecção de horizontes é concluído com sucesso.

    Este evento herda de :class:`FinishedEvent` e sinaliza que o job associado foi
    finalizado, disponibilizando os caminhos de saída gerados pelo processo.

    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset para o qual a detecção de horizontes foi executada.

    output_paths : List[str]
        Lista de caminhos para os arquivos de saída gerados pelo processo
        (ex.: horizontes detectados, máscaras processadas, resultados intermediários).
    """
    dataset_id: UUID
    output_paths: List[str]
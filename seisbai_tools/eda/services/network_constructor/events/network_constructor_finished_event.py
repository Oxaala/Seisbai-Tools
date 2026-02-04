from typing import List
from uuid import UUID

from seisbai_tools.file_system.manager import FileSystemPathInfo
from ....events import CompletedEvent


class NetworkConstructorCompletedEvent(CompletedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando a execução de um job de construção ou treinamento de rede neural
    é concluída com sucesso.

    Este evento permite que consumidores (UI, orquestradores, logs, etc.) reajam ao término
    do job, acessando os artefatos gerados, atualizando estados ou disparando etapas
    subsequentes do workflow.

    Herda de :class:`CompletedEvent`.

    ---
    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset associado ao job concluído.

    output : FileSystemPathInfo
        Informações sobre os arquivos de saída gerados pelo job, incluindo
        pesos da rede, checkpoints, logs, métricas e outros artefatos relevantes.
    """
    dataset_id: UUID
    output: FileSystemPathInfo
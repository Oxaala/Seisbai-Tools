from uuid import UUID
from ....events import ProgressUpdatedEvent


class HorizonDetectionProgressUpdatedEvent(ProgressUpdatedEvent, frozen=True, kw_only=True):
    """
    Evento emitido para indicar o progresso de um job de detecção de horizontes.

    Este evento herda de :class:`ProgressedEvent` e fornece informações sobre a
    etapa atual do processo e o percentual concluído.

    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset associado ao job de detecção de horizontes.

    stage : str
        Nome ou descrição da etapa atual do processo (ex.: 'preprocessing',
        'clustering', 'postprocessing').
    """
    dataset_id: UUID
    stage: str
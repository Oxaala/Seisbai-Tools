from uuid import UUID
from seisbai_contracts.core.artefacts.events import ProgressedEvent


class HorizonDetectionProgressedEvent(ProgressedEvent, frozen=True, kw_only=True):
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

    percent : int
        Percentual de conclusão da etapa ou do job como um todo, representado
        como inteiro entre 0 e 100.
    """
    dataset_id: UUID
    stage: str
    percent: int
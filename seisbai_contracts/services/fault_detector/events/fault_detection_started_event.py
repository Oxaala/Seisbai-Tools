from uuid import UUID
from seisbai_contracts.core.artefacts.events.started import StartedEvent


class FaultDetectionStartedEvent(StartedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando um job de detecção de falhas é iniciado com sucesso.

    Este evento carrega as informações essenciais para rastrear o job em execução,
    permitindo que outros serviços ou componentes reajam a esse início.

    Attributes
    ----------
    dataset_id : UUID
        Identificador único do dataset associado ao job.
    
    seismic_path : str
        Caminho do arquivo sísmico usado na detecção.
    
    model_path : str
        Caminho do modelo de rede neural aplicado na detecção.
    """
    dataset_id: UUID
    seismic_path: str
    model_path: str
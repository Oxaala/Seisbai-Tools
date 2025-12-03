from uuid import UUID

from seisbai_tools.file_system.manager import FileSystemPathInfo
from ....events import StartedEvent


class FaultDetectionStartedEvent(StartedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando um job de detecção de falhas sísmicas é iniciado.

    Este evento marca o início oficial do processo de detecção, permitindo que
    orquestradores, serviços de monitoramento, dashboards ou interfaces de
    acompanhamento atualizem o estado e iniciem mecanismos de rastreamento.

    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset relacionado ao job iniciado.

    seismic_path : FileSystemPathInfo
        Informações sobre o volume sísmico de entrada, incluindo o caminho
        no sistema de arquivos abstrato (local, SMB, S3 etc.) e seus metadados.

    model_path : FileSystemPathInfo
        Caminho para o modelo de rede neural utilizado na detecção, incluindo
        metadados disponibilizados pelo gerenciador de arquivos.
    """

    dataset_id: UUID
    seismic_path: FileSystemPathInfo
    model_path: FileSystemPathInfo
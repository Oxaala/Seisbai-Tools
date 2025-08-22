from uuid import UUID
from seisbai_contracs.core import Command

class ResumeFaultDetectionJobCommand(Command, frozen=True, kw_only=True):
    """
    Comando responsável por retomar (resume) um job de detecção de falhas em um dataset.

    Este comando deve ser enviado para o handler responsável por controlar
    o ciclo de vida do processo de detecção de falhas. Ao ser executado,
    o job que estava previamente pausado será colocado em estado de "em execução".

    Attributes
    ----------
    dataset_id : UUID
        Identificador único do dataset no qual o processo de detecção
        de falhas deve ser retomado.
    """
    dataset_id: UUID
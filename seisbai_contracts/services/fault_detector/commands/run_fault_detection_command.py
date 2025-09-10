from uuid import UUID, uuid4
from msgspec import field
from seisbai_contracts.core.artefacts.commands.start import StartCommand
from seisbai_contracts.services.fault_detector.DTOs import FaultDetectionParamsDTO


class RunFaultDetectionCommand(StartCommand, frozen=True, kw_only=True):
    """
    Comando responsável por iniciar a execução de um job de detecção de falhas.

    Este comando cria a intenção de rodar o processo de inferência do modelo
    de detecção de falhas sobre um dataset sísmico, utilizando os parâmetros
    definidos em `FaultDetectionParamsDTO`.

    Attributes
    ----------
    dataset_id : UUID, default=factory(uuid4)
        Identificador único do dataset no qual a detecção será executada.
        Caso não seja informado, será gerado automaticamente.

    params : FaultDetectionParamsDTO
        Objeto de transferência contendo os parâmetros necessários para a
        execução da detecção (caminhos, shape, step, eixos e diretório de saída).
    """
    dataset_id: UUID = field(default_factory=lambda: uuid4())

    params: FaultDetectionParamsDTO = field(default_factory=lambda: FaultDetectionParamsDTO(
        seismic_path="",
        model_path="",
    ))
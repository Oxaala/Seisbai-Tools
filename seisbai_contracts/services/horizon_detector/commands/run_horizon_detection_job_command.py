from uuid import UUID, uuid4
from msgspec import field
from seisbai_contracts.core.artefacts.commands import StartCommand
from seisbai_contracts.services.horizon_detector.DTOs.horizon_detection_params_dto import HorizonDetectionParamsDTO


class RunHorizonDetectionCommand(StartCommand, frozen=True, kw_only=True):
    """
    Comando para iniciar a execução de um job de detecção de horizontes.

    Este comando herda de :class:`StartCommand` e encapsula os parâmetros necessários
    para a execução do processo de detecção de horizontes em um dataset específico.

    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset associado ao job de detecção de horizontes.
        Gerado automaticamente com `uuid4()` caso não seja informado.

    params : HorizonDetectionParamsDTO
        Objeto que contém todos os parâmetros de configuração do processo de detecção.
        Por padrão, é inicializado com valores mínimos e caminhos vazios, que devem ser
        substituídos pelos corretos antes da execução real.
    """
    dataset_id: UUID = field(default_factory=lambda: uuid4())
    params: HorizonDetectionParamsDTO = field(default_factory=lambda: HorizonDetectionParamsDTO(
        seismic_path="",
        model_dir="",
        model_name="",
        mask_path="",
        threshold=0.1,
        eps=0.05,
        min_points=50,
        output_dir="output/horizons",
    ))
from uuid import UUID, uuid4
from msgspec import field
from ....commands import StartCommand
from ..DTOs import HorizonDetectionParamsDTO


class RunHorizonDetectionCommand(StartCommand, frozen=True, kw_only=True):
    """
    Comando responsável por iniciar a execução de um job de detecção de horizontes.

    Este comando herda de :class:`StartCommand` e encapsula todos os parâmetros
    necessários para realizar o processo de detecção em um dataset sísmico.

    Attributes
    ----------
    dataset_id : UUID
        Identificador único que vincula este job ao dataset correspondente.
        Caso não seja informado, é gerado automaticamente por meio de `uuid4()`.

    params : HorizonDetectionParamsDTO
        Estrutura contendo todos os parâmetros de configuração da detecção
        de horizontes (como caminhos de entrada, modelo, máscara, threshold,
        parâmetros de clusterização e diretório de saída).
        É inicializado com valores padrão que devem ser substituídos de acordo
        com o contexto real da execução.
    """
    dataset_id: UUID = field(default_factory=lambda: uuid4())
    params: HorizonDetectionParamsDTO = field(default_factory=HorizonDetectionParamsDTO)
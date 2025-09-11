from uuid import UUID, uuid4
from seisbai_contracts.core.artefacts.commands import StartCommand
from msgspec import field

from seisbai_contracts.services.network_constructor.DTOs.network_constructor_params_dto import NetworkConstructorParamsDTO


class RunNetworkConstructorJobCommand(StartCommand, frozen=True, kw_only=True):
    """
    Comando emitido para iniciar a execução de um job de construção de rede.

    Em arquiteturas baseadas em mensageria, este comando representa uma
    instrução explícita para criar e executar um novo job de construção de
    rede neural com os parâmetros fornecidos.

    Herda de :class:`StartCommand`.

    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset associado ao job de construção de rede.
        Gerado automaticamente com ``uuid4()`` caso não seja informado.

    params : NetworkConstructorParamsDTO
        Objeto de transferência contendo todos os parâmetros necessários
        para a construção e treinamento da rede.
    """
    dataset_id: UUID = field(default_factory=lambda: uuid4())
    params: NetworkConstructorParamsDTO = field(default_factory=lambda: NetworkConstructorParamsDTO())
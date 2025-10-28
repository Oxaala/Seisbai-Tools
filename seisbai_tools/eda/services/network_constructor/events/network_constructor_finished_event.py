from typing import List
from uuid import UUID
from ....events import CompletedEvent


class NetworkConstructorCompletedEvent(CompletedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando a execução de um job de construção de rede é concluída com sucesso.

    Este evento sinaliza que o processamento do job de construção e/ou
    treinamento da rede neural foi finalizado, permitindo que os consumidores
    do evento acessem os resultados gerados ou atualizem seus estados e interfaces.

    Herda de :class:`CompletedEvent`.

    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset associado ao job concluído.

    output_paths : List[str]
        Lista de caminhos para os arquivos de saída gerados pelo job, como
        modelos treinados ou artefatos derivados.
    """
    dataset_id: UUID
    output_paths: List[str]
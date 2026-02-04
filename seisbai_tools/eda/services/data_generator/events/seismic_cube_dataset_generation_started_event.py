from typing import Optional, Tuple
from uuid import UUID
from ....events import StartedEvent


class SeismicCubeDatasetGenerationStartedEvent(StartedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando a geração de um dataset de cubos sísmicos é iniciada.

    Este evento marca o início do processo de criação de um dataset sísmico.
    Ele carrega metadados essenciais que permitem que interfaces, orquestradores
    e serviços de monitoramento possam inicializar barras de progresso, registrar
    logs e acompanhar a operação de forma correlacionada ao `dataset_id`.

    ---
    Propósito
    ---------
    - Indicar o início formal da operação de geração.
    - Permitir inicialização de indicadores no frontend.
    - Registrar a intenção de geração do dataset para auditoria.
    - Providenciar metadados estruturais (dimensões, prefixo, quantidade de amostras).

    ---
    Atributos
    ---------
    dataset_id : UUID
        Identificador único associado a este dataset. Usado para correlacionar
        todos os eventos subsequentes do mesmo processo de geração.

    prefix : Optional[str], default=None
        Prefixo usado para compor o nome dos arquivos gerados. Caso `None`,
        será utilizado o prefixo padrão definido pela infraestrutura de geração.

    samples : int
        Quantidade de cubos sísmicos (amostras) que serão gerados.

    dimensions : Tuple[int, int, int]
        Dimensões de cada cubo no formato:
        `(inline, xline, depth)`.

    ---
    Uso
    ---
    Este evento deve ser emitido imediatamente após o worker/handler iniciar
    o processo de geração, antes de qualquer transformação ou escrita em disco.

    Exemplo
    -------
    >>> SeismicCubeDatasetGenerationStartedEvent(
    ...     dataset_id=UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
    ...     prefix="cube",
    ...     samples=32,
    ...     dimensions=(128, 128, 128),
    ... )
    """

    dataset_id: UUID
    prefix: Optional[str] = None
    samples: int
    dimensions: Tuple[int, int, int]
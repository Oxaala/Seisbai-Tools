from seisbai_tools.file_system.manager import FileSystemPathInfo
from ....events import CompletedEvent
from uuid import UUID


class SeismicCubeDatasetGenerationCompletedEvent(CompletedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando a geração de um dataset de cubos sísmicos é concluída
    com sucesso.

    Este evento faz parte do fluxo EDA (Event-Driven Architecture) do Seisbai e
    sinaliza o término completo do processo de geração. Ele contém o
    identificador do dataset e informações sobre o destino final dos arquivos
    produzidos, permitindo que orquestradores, UIs e serviços dependentes
    realizem ações posteriores, como exibição, indexação, transferência ou
    monitoramento.

    ---
    Propósito
    ---------
    - Indicar que todo o pipeline de geração (incluindo transformações e escrita
      no sistema de arquivos) terminou sem erros.
    - Permitir que a UI finalize barras de progresso e atualize o status.
    - Fornecer metadados de saída para logs, auditoria ou armazenamento externo.
    - Notificar serviços downstream que dependem da disponibilidade do dataset.

    ---
    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset gerado. Permite rastrear todo o fluxo
        desde o comando inicial até a conclusão.

    output : FileSystemInfo
        Objeto contendo informações sobre o local onde os arquivos foram
        armazenados (diretório, backend, credenciais, caminhos físicos ou
        lógicos etc.). Permite abstrair entre armazenamento local, SMB, NFS,
        S3, entre outros.

    ---
    Uso
    ---
    Este evento é normalmente emitido por um worker ao final do processo
    de geração:

        - após gerar todos os cubos (samples)
        - após aplicar o pipeline completo de transformações
        - após salvar todos os arquivos no destino indicado
        - após realizar verificações finais de integridade e contagem

    Exemplo
    -------
    >>> SeismicCubeDatasetGenerationCompletedEvent(
    ...     dataset_id=UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
    ...     output=FileSystemPathInfo(path="/datasets/synthetics/cube001")
    ... )
    """

    dataset_id: UUID
    output: FileSystemPathInfo
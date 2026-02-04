from seisbai_tools.file_system.manager import FileSystemPathInfo
from ....events import CompletedEvent
from uuid import UUID


class SeismicCubeDatasetGenerationCompletedEvent(CompletedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando a geração de um dataset de cubos sísmicos é concluída
    com sucesso.

    Este evento integra o fluxo EDA (Event-Driven Architecture) do Seisbai e
    representa o encerramento completo do pipeline de geração. Ele fornece o
    identificador do dataset e informações sobre o diretório final onde os
    cubos foram armazenados, permitindo que sistemas dependentes realizem ações
    posteriores como atualização de UI, indexação, publicação ou monitoramento.

    Attributes
    ----------
    dataset_id : UUID
        Identificador único do dataset gerado.

    output_path : FileSystemPathInfo
        Informações sobre o destino onde os cubos foram gravados, incluindo
        caminho e metadados fornecidos pelo backend de arquivo (local, SMB,
        NFS, S3, etc.).

    Notes
    -----
    Este evento é tipicamente emitido por um worker após:

    - gerar todos os cubos (samples) do dataset;
    - aplicar todas as transformações configuradas;
    - gravar os arquivos no diretório de destino;
    - executar verificações finais de integridade ou contagem.

    Exemplos
    --------
    >>> SeismicCubeDatasetGenerationCompletedEvent(
    ...     dataset_id=UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
    ...     output_path=FileSystemPathInfo(path="/datasets/synthetics/cube001")
    ... )
    """
    dataset_id: UUID
    output_path: FileSystemPathInfo
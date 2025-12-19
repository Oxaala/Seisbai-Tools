from seisbai_tools.eda.events import Event


class FileDeletedEvent(Event, kw_only=True, frozen=True):
    """
    Evento emitido quando um arquivo é deletado com sucesso.

    Este evento faz parte do fluxo EDA (Event-Driven Architecture) do Seisbai
    e é utilizado para notificar que uma operação de remoção de arquivo foi
    concluída de forma bem-sucedida. Ele permite que a UI, serviços de
    monitoramento, orquestradores e handlers atualizem seus estados internos
    ou executem ações subsequentes após a exclusão.

    ---
    Herança
    -------
    Event
        Evento-base simples do sistema, representando uma ocorrência sem
        informações adicionais de progresso ou falha.

    ---
    Atributos
    ---------
    file_path : str
        Caminho absoluto ou relativo do arquivo que foi deletado.

    ---
    Uso
    ---
    Este evento deve ser emitido imediatamente após a remoção física do
    arquivo do sistema de arquivos ou serviço de armazenamento. É
    normalmente utilizado para:

        - atualizar listagens em interfaces gráficas
        - registrar logs de auditoria
        - disparar etapas subsequentes de pipelines de limpeza
        - liberar recursos associados ao arquivo removido

    Exemplo
    -------
    >>> FileDeletedEvent(
    ...     file_path="/data/projects/model.sgy"
    ... )
    """
    file_path: str
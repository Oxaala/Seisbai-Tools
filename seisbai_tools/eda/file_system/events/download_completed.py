from seisbai_tools.eda.events import CompletedEvent


class DownloadCompletedEvent(CompletedEvent, kw_only=True, frozen=True):
    """
    Evento emitido quando uma operação de download é concluída com sucesso.

    Este evento faz parte do fluxo EDA (Event-Driven Architecture) do Seisbai
    e indica que o arquivo solicitado foi totalmente transferido e está
    disponível no destino configurado. Ele funciona como notificação final
    para consumidores interessados no término bem-sucedido da operação.

    A classe é imutável (`frozen=True`), garantindo que os dados do evento não
    sejam modificados após sua criação. Os parâmetros são **somente nomeados**
    (`kw_only=True`), aumentando clareza e segurança.

    ---
    Herança
    -------
    CompletedEvent
        Evento-base que representa operações concluídas com sucesso dentro
        do fluxo EDA.

    ---
    Atributos
    ---------
    file_name : str
        Nome do arquivo cujo download foi finalizado com sucesso.

    ---
    Uso
    ---
    O `DownloadCompletedEvent` deve ser publicado pelo handler responsável
    pelo download após a transferência ser concluída sem erros. Consumidores
    podem utilizá-lo para:
        - atualizar o estado do workflow
        - liberar etapas subsequentes do processo
        - registrar métricas ou logs
        - notificar UI/serviços externos sobre a conclusão

    Exemplo
    -------
    >>> DownloadCompletedEvent(
    ...     file_name="velocity_model.sgy"
    ... )
    """

    file_name: str
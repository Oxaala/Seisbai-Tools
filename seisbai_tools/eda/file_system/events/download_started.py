from seisbai_tools.eda.events import StartedEvent


class DownloadStartedEvent(StartedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando um download é iniciado.

    Este evento faz parte do fluxo EDA (Event-Driven Architecture) do Seisbai
    e indica que a operação de download começou formalmente. Ele fornece
    metadados essenciais para que o orquestrador, handlers, UI ou serviços
    de monitoramento possam inicializar o acompanhamento do progresso.

    Como todos os eventos do sistema, esta classe é imutável (`frozen=True`),
    garantindo consistência e segurança dos dados após a instanciação.
    Além disso, os parâmetros são **somente nomeados** (`kw_only=True`),
    o que aumenta a clareza na construção do evento.

    ---
    Herança
    -------
    StartedEvent
        Evento-base utilizado para sinalizar início de qualquer operação
        rastreável dentro do fluxo EDA.

    ---
    Atributos
    ---------
    total_bytes : int
        Tamanho total, em bytes, do arquivo que será transferido.
        Permite que a UI e os handlers calculem porcentagens, velocidade
        e o ETA da operação.

    file_name : str
        Nome do arquivo cujo download está começando. É utilizado como
        identificador lógico da operação.

    ---
    Uso
    ---
    Este evento deve ser emitido pelo handler responsável assim que a operação
    de download é oficialmente iniciada. É normalmente utilizado para:

        - inicializar barras de progresso
        - registrar logs de início da operação
        - calcular e exibir métricas de transferência
        - criar estruturas internas de acompanhamento (ex.: trackers)

    Exemplo
    -------
    >>> DownloadStartedEvent(
    ...     file_name="velocity_model.sgy",
    ...     total_bytes=104857600,  # 100 MB
    ... )
    """

    total_bytes: int
    file_name: str
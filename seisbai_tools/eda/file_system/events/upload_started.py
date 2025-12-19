from seisbai_tools.eda.events import StartedEvent


class UploadStartedEvent(StartedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando um upload é iniciado.

    Este evento faz parte do fluxo EDA (Event-Driven Architecture) do Seisbai
    e indica que a operação de upload começou formalmente. Ele fornece
    metadados essenciais para que orquestradores, handlers, UIs e serviços
    de monitoramento possam inicializar o acompanhamento do progresso.

    Como todos os eventos do sistema, esta classe é imutável (`frozen=True`),
    garantindo consistência e segurança dos dados após a instanciação.
    Além disso, os parâmetros são **somente nomeados** (`kw_only=True`),
    o que aumenta a clareza e reduz erros.

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
        Tamanho total, em bytes, do arquivo que será enviado.
        Permite que UIs e handlers calculem porcentagem, velocidade e ETA.

    file_name : str
        Nome do arquivo cujo upload está iniciando. Funciona como
        identificador lógico da operação de transferência.

    ---
    Uso
    ---
    Este evento deve ser emitido pelo handler responsável assim que a operação
    de upload é oficialmente iniciada. É normalmente utilizado para:

        - inicializar barras de progresso
        - registrar logs de início
        - iniciar cálculos de taxa de transferência e ETA
        - configurar estruturas internas de acompanhamento (trackers)

    Exemplo
    -------
    >>> UploadStartedEvent(
    ...     file_name="velocity_model.sgy",
    ...     total_bytes=104857600,  # 100 MB
    ... )
    """

    total_bytes: int
    file_name: str
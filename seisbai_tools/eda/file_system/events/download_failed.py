from seisbai_tools.eda.events import FailedEvent


class DownloadFailedEvent(FailedEvent, kw_only=True, frozen=True):
    """
    Evento emitido quando uma operação de download falha.

    Este evento faz parte do fluxo EDA (Event-Driven Architecture) do Seisbai
    e representa a ocorrência de um erro durante a tentativa de baixar um arquivo.
    Ele permite que handlers, orquestradores e componentes de UI reajam
    apropriadamente à falha — seja exibindo mensagens, realizando retentativas
    automáticas ou registrando logs.

    A classe é imutável (`frozen=True`), garantindo que suas informações não
    sejam alteradas após a criação do evento. Todos os parâmetros são
    **somente nomeados** (`kw_only=True`), aumentando clareza e segurança.

    ---
    Herança
    -------
    FailedEvent
        Evento-base que representa operações concluídas com falha no
        fluxo EDA.

    ---
    Atributos
    ---------
    file_name : str
        Nome do arquivo cujo download falhou.

    ---
    Uso
    ---
    O handler responsável pelo download deve emitir este evento quando ocorrer
    qualquer erro irrecuperável — como falhas de autenticação, timeout,
    arquivo inexistente, erros de rede ou problemas no backend do sistema de
    arquivos.

    Exemplos de uso:
        - informar o frontend de que o download não pôde ser concluído
        - registrar a causa da falha no log
        - acionar rotinas de fallback ou limpeza

    Exemplo
    -------
    >>> DownloadFailedEvent(
    ...     file_name="velocity_model.sgy"
    ... )
    """

    file_name: str
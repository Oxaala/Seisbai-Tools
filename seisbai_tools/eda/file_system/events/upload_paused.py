from seisbai_tools.eda.events import PausedEvent


class UploadPausedEvent(PausedEvent, kw_only=True, frozen=True):
    """
    Evento emitido quando uma operação de upload é pausada.

    Este evento integra o fluxo EDA (Event-Driven Architecture) do Seisbai
    e representa a interrupção temporária de um upload em andamento. Ele
    permite que componentes do sistema — como orquestradores, UI ou serviços
    de monitoramento — reajam a uma pausa solicitada pelo usuário ou causada
    por condições externas.

    A classe é imutável (`frozen=True`), garantindo que os dados do evento
    não sejam modificados após sua criação. Os parâmetros são **somente nomeados**
    (`kw_only=True`), aumentando clareza e segurança.

    ---
    Herança
    -------
    PausedEvent
        Evento-base que indica operações pausadas dentro do fluxo EDA.

    ---
    Atributos
    ---------
    file_name : str
        Nome do arquivo cujo upload foi pausado.

    ---
    Uso
    ---
    Este evento deve ser emitido pelo handler responsável quando o upload
    atual for colocado em pausa — seja por solicitação explícita do usuário,
    seja por mecanismos automáticos do sistema (ex.: limite de banda,
    perda temporária de conexão, throttling, etc.).

    Consumidores podem utilizá-lo para:
        - atualizar status na UI
        - registrar logs operacionais
        - agendar retentativas
        - congelar estado do workflow até retomada

    Exemplo
    -------
    >>> UploadPausedEvent(
    ...     file_name="velocity_model.sgy"
    ... )
    """

    file_name: str
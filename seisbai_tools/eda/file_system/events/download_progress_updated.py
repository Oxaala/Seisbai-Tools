from seisbai_tools.eda.events import ProgressUpdatedEvent


class DownloadProgressUpdatedEvent(ProgressUpdatedEvent, kw_only=True, frozen=True):
    """
    Evento emitido quando há atualização no progresso de um download.

    Este evento integra o fluxo EDA (Event-Driven Architecture) do Seisbai e é
    utilizado para comunicar, de forma incremental, o avanço do download de um
    arquivo. Ele permite que frontends, dashboards, orquestradores e outros
    componentes reajam em tempo real ao andamento da transferência.

    A classe é imutável (`frozen=True`), garantindo que seus dados permaneçam
    consistentes após a criação. Os parâmetros são **somente nomeados**
    (`kw_only=True`), proporcionando clareza e segurança durante a instanciação.

    ---
    Herança
    -------
    ProgressUpdatedEvent
        Evento-base indicando atualização de progresso em alguma operação.

    ---
    Atributos
    ---------
    file_name : str
        Nome do arquivo cujo progresso de download foi atualizado.

    total_bytes : int
        Tamanho total do arquivo em bytes. Usado para calcular porcentagem,
        velocidade estimada e tempo restante.

    downloaded_bytes : int
        Quantidade de bytes já baixados até o momento do evento.
        Representa o progresso atual da transferência.

    ---
    Uso
    ---
    Este evento deve ser emitido periodicamente pelo handler responsável pelo
    download, conforme mais dados forem transferidos. Ele é utilizado
    principalmente para:

        - atualizar barras de progresso na UI
        - alimentar logs de telemetria ou métricas
        - permitir cálculos de velocidade/ETA
        - monitorar gargalos ou interrupções

    Exemplo
    -------
    >>> DownloadProgressUpdatedEvent(
    ...     file_name="velocity_model.sgy",
    ...     total_bytes=1024 * 1024 * 200,   # 200 MB
    ...     downloaded_bytes=1024 * 1024 * 50  # 50 MB baixados
    ... )
    """

    file_name: str
    total_bytes: int
    downloaded_bytes: int
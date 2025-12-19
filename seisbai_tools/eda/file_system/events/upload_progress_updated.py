from seisbai_tools.eda.events import ProgressUpdatedEvent


class UploadProgressUpdatedEvent(ProgressUpdatedEvent, kw_only=True, frozen=True):
    """
    Evento emitido quando há atualização no progresso de um upload.

    Este evento integra o fluxo EDA (Event-Driven Architecture) do Seisbai e é
    utilizado para comunicar, de forma incremental, o avanço do envio de um
    arquivo para o sistema de arquivos remoto. Ele permite que frontends,
    dashboards, orquestradores e outros componentes reajam em tempo real ao
    andamento da transferência.

    A classe é imutável (`frozen=True`), garantindo consistência após sua
    criação. Todos os parâmetros são **somente nomeados** (`kw_only=True`),
    fornecendo clareza e segurança na instanciação.

    ---
    Herança
    -------
    ProgressUpdatedEvent
        Evento-base que representa atualização periódica de progresso.

    ---
    Atributos
    ---------
    file_name : str
        Nome do arquivo cujo progresso de upload foi atualizado.

    total_bytes : int
        Tamanho total do arquivo em bytes. Usado para cálculo de porcentagem,
        velocidade estimada e tempo restante.

    uploaded_bytes : int
        Quantidade de bytes já enviados até o momento do evento.
        Representa o progresso atual do upload.

    ---
    Uso
    ---
    Este evento deve ser emitido periodicamente pelo handler responsável pelo
    upload, conforme mais dados forem enviados ao servidor. Ele é utilizado
    principalmente para:

        - atualizar barras de progresso na UI
        - alimentar logs de telemetria ou métricas
        - permitir cálculos de velocidade/ETA
        - monitorar gargalos ou instabilidades de rede

    Exemplo
    -------
    >>> UploadProgressUpdatedEvent(
    ...     file_name="velocity_model.sgy",
    ...     total_bytes=1024 * 1024 * 200,     # 200 MB
    ...     uploaded_bytes=1024 * 1024 * 20     # 20 MB enviados
    ... )
    """

    file_name: str
    total_bytes: int
    uploaded_bytes: int
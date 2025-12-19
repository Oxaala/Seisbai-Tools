from seisbai_tools.eda.events import ResumedEvent


class DownloadResumedEvent(ResumedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando um download pausado é retomado.

    Este evento faz parte do fluxo EDA (Event-Driven Architecture) do Seisbai
    e comunica que uma operação de download, anteriormente pausada, voltou
    a ser executada. Ele permite que interfaces, orquestradores e serviços
    de monitoramento reajam adequadamente à retomada da transferência.

    A classe é imutável (`frozen=True`), garantindo consistência após a
    criação. Os parâmetros são **somente nomeados** (`kw_only=True`),
    promovendo clareza e segurança.

    ---
    Herança
    -------
    ResumedEvent
        Evento-base utilizado para representar a retomada de operações
        previamente pausadas.

    ---
    Atributos
    ---------
    file_name : str
        Nome do arquivo cujo download foi retomado. É utilizado por
        orquestradores, handlers e UIs para identificar qual operação
        voltou a ser executada.

    ---
    Uso
    ---
    O `DownloadResumedEvent` deve ser emitido pelo handler responsável
    exatamente no momento em que a operação de download é retomada.
    Aplicações típicas incluem:

        - reativar indicadores de progresso na UI
        - reiniciar cálculos de ETA e velocidade
        - registrar logs de retomada
        - notificar serviços externos/supervisores

    Exemplo
    -------
    >>> DownloadResumedEvent(
    ...     file_name="velocity_model.sgy"
    ... )
    """

    file_name: str
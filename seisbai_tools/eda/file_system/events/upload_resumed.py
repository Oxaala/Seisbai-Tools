from seisbai_tools.eda.events import ResumedEvent


class UploadResumedEvent(ResumedEvent, frozen=True, kw_only=True):
    """
    Evento emitido quando um upload pausado é retomado.

    Este evento faz parte do fluxo EDA (Event-Driven Architecture) do Seisbai
    e comunica que uma operação de upload, anteriormente pausada, voltou a
    prosseguir. Ele permite que interfaces, serviços de monitoramento e
    orquestradores reajam adequadamente à retomada da transferência.

    A classe é imutável (`frozen=True`), garantindo consistência dos dados
    após a criação. Os parâmetros são **somente nomeados** (`kw_only=True`),
    aumentando clareza e segurança na instanciação.

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
        Nome do arquivo cujo upload foi retomado. É utilizado por
        orquestradores, handlers e UIs para identificar qual operação
        voltou a ser executada.

    ---
    Uso
    ---
    O `UploadResumedEvent` deve ser emitido pelo handler responsável
    exatamente no momento em que a operação de upload é retomada.
    Aplicações típicas incluem:

        - reativar indicadores de progresso na UI
        - reiniciar cálculos de ETA e velocidade
        - registrar logs de retomada
        - notificar serviços supervisores de que a operação continua

    Exemplo
    -------
    >>> UploadResumedEvent(
    ...     file_name="velocity_model.sgy"
    ... )
    """

    file_name: str
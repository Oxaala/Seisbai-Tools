from seisbai_tools.eda.events import CancelledEvent


class DownloadCancelledEvent(CancelledEvent, kw_only=True, frozen=True):
    """
    Evento emitido quando uma operação de download é cancelada.

    Este evento integra o fluxo EDA (Event-Driven Architecture) do Seisbai
    e representa explicitamente o cancelamento de um download previamente
    solicitado. Ele pode ser disparado tanto por uma ação do usuário quanto
    por um cancelamento interno (timeout, encerramento do workflow, mudança
    de estado da aplicação etc.).

    A classe é imutável (`frozen=True`) para garantir consistência e evitar
    alterações posteriores aos dados do evento. Os parâmetros são somente
    nomeados (`kw_only=True`), reforçando clareza e segurança.

    ---
    Herança
    -------
    CancelledEvent
        Classe base que identifica eventos cujo processamento foi interrompido
        ou cancelado no fluxo de trabalho.

    ---
    Atributos
    ---------
    file_name : str
        Nome do arquivo cujo download foi cancelado.

    ---
    Uso
    ---
    O `DownloadCancelledEvent` deve ser publicado pelo componente responsável
    por gerenciar downloads ou pelo handler do comando que iniciou a operação.
    Consumidores assinantes podem reagir ao cancelamento realizando ações como:
        - limpar estados intermediários
        - remover arquivos temporários
        - notificar o frontend
        - registrar logs de auditoria

    Exemplo
    -------
    >>> DownloadCancelledEvent(
    ...     file_name="velocity_model.sgy"
    ... )
    """

    file_name: str
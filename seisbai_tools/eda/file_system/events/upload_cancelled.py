from seisbai_tools.eda.events import CancelledEvent


class UploadCancelledEvent(CancelledEvent, kw_only=True, frozen=True):
    """
    Evento emitido quando uma operação de upload é cancelada.

    Este evento integra o fluxo EDA (Event-Driven Architecture) do Seisbai
    e representa explicitamente o cancelamento de um upload previamente
    iniciado. O cancelamento pode ocorrer por ação direta do usuário ou por
    motivos internos, como timeout, queda de conexão, finalização do workflow
    ou alteração do estado da aplicação.

    A classe é imutável (`frozen=True`), garantindo consistência e evitando
    mudanças nos dados do evento após sua criação. Os parâmetros são
    exclusivamente nomeados (`kw_only=True`), reforçando clareza e segurança
    na instanciação.

    ---
    Herança
    -------
    CancelledEvent
        Classe base que identifica eventos cujo processamento foi interrompido
        ou cancelado dentro de um fluxo EDA.

    ---
    Atributos
    ---------
    file_name : str
        Nome do arquivo cujo upload foi cancelado.

    ---
    Uso
    ---
    O `UploadCancelledEvent` deve ser publicado pelo handler ou componente
    responsável pela operação de upload assim que o cancelamento for detectado.
    Consumidores que escutam este evento podem reagir realizando ações como:

        - limpar buffers ou estados intermediários
        - apagar arquivos temporários
        - informar o frontend sobre o cancelamento
        - registrar logs de auditoria
        - atualizar a UI de progresso

    Exemplo
    -------
    >>> UploadCancelledEvent(
    ...     file_name="new_velocity_model.sgy"
    ... )
    """

    file_name: str
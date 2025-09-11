from .command import Command


class CancelCommand(Command, frozen=True, kw_only=True):
    """
    Comando para solicitar o cancelamento de uma operação ou processo no sistema.

    Em arquiteturas baseadas em mensageria, um comando representa uma instrução explícita
    que solicita ao sistema que realize uma ação específica. Diferente de um evento, 
    o comando descreve a **intenção de alteração futura de estado**.

    Esta classe herda de :class:`Command` e mantém os atributos básicos de identificação
    e rastreabilidade.

    Atributos herdados
    ------------------
    id : uuid.UUID
        Identificador único do comando, gerado automaticamente com `uuid4()`. 
        Utilizado para rastreamento em logs e pipelines distribuídos.

    timestamp : datetime.datetime
        Data e hora de criação do comando, em UTC. Importante para auditoria e 
        ordenação temporal de comandos.
    """
    pass
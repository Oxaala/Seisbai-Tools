from typing import Optional
from uuid import UUID
from ....events import ProgressUpdatedEvent


class NetworkConstructorProgressUpdatedEvent(ProgressUpdatedEvent, frozen=True, kw_only=True):
    """
    Evento emitido para indicar o progresso de um job de construção de rede.

    Este evento sinaliza que o processamento do job de construção e/ou
    treinamento da rede neural está em andamento, fornecendo informações
    sobre a época atual, métricas de treino e progresso total, permitindo
    que os consumidores do evento atualizem estados, interfaces ou logs.

    Herda de :class:`ProgressUpdatedEvent`.

    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset associado ao job em progresso.

    epoch : int
        Número da época atual do treinamento.

    total_epochs : int
        Número total de épocas planejadas para o treinamento.

    train_loss : Optional[float]
        Valor da função de perda no conjunto de treino, se disponível.

    val_loss : Optional[float]
        Valor da função de perda no conjunto de validação, se disponível.
    """
    dataset_id: UUID
    epoch: int
    total_epochs: int
    train_loss: Optional[float] = None
    val_loss: Optional[float] = None
from typing import Any, Dict, List, Optional, Tuple
from msgspec import Struct, field

from seisbai_tools.file_system.manager import FileSystemPathInfo


class NetworkConstructorParamsDTO(Struct, frozen=True, tag=True):
    """
    Data Transfer Object (DTO) que encapsula os parâmetros necessários para
    a construção e treinamento de redes neurais dentro do sistema Seisbai.

    Esta estrutura é imutável (`frozen=True`) e deve ser utilizada para
    transportar configurações entre diferentes camadas (UI → domínio → workers)
    de forma segura, explícita e serializável.

    Attributes
    ----------
    output : FileSystemPathInfo
        Diretório onde a rede treinada e seus artefatos (pesos, logs,
        checkpoints, gráficos, etc.) serão armazenados.

    dataset : FileSystemPathInfo
        Caminho para o dataset de entrada a ser utilizado durante o
        treinamento da rede.

    model_type : str, default="unet"
        Tipo do modelo que será construído.
        Exemplos comuns: `"unet"`, `"cnn"`, `"resnet"`.

    input_shape : Tuple[int, int, int], default=(128, 128, 1)
        Dimensões esperadas pelo modelo no formato
        `(altura, largura, canais)`.

    optimizer : str, default="adam"
        Otimizador a ser utilizado no treinamento.

    loss : str, default="binary_crossentropy"
        Função de perda a ser aplicada durante o processo de otimização.

    metrics : List[str], default=["accuracy"]
        Lista de métricas para monitoramento durante o treinamento.

    batch_size : int, default=8
        Número de amostras processadas por batch.

    epochs : int, default=5
        Quantidade total de épocas de treinamento.

    learning_rate : Optional[float], default=None
        Taxa de aprendizado a ser usada pelo otimizador.
        Se `None`, é utilizado o valor padrão do otimizador selecionado.

    validation_split : float, default=0.1
        Porcentagem do dataset separada automaticamente para validação.

    seed : Optional[int], default=None
        Semente para reprodutibilidade de inicializações e embaralhamentos.

    model_params : Dict[str, Any], default={}
        Parâmetros adicionais específicos do modelo definido em `model_type`.
        Exemplo: número de filtros, profundidade da U-Net, kernel_size etc.
    """
    # Caminhos e I/O
    output: FileSystemPathInfo = field(default_factory=FileSystemPathInfo)
    dataset: FileSystemPathInfo = field(default_factory=FileSystemPathInfo)

    # Seleção de modelo e config
    model_type: str = "unet"
    input_shape: Tuple[int, int, int] = (128, 128, 1)
    optimizer: str = "adam"
    loss: str = "binary_crossentropy"
    metrics: List[str] = field(default_factory=lambda: ["accuracy"])

    # Hiperparâmetros de treino
    batch_size: int = 8
    epochs: int = 5
    learning_rate: Optional[float] = None
    validation_split: float = 0.1
    seed: Optional[int] = None

    # Parâmetros específicos do modelo (pass-through)
    model_params: Dict[str, Any] = field(default_factory=dict)
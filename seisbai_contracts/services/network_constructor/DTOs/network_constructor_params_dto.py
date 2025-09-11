from typing import Any, Dict, List, Optional, Tuple
from msgspec import Struct, field


class NetworkConstructorParamsDTO(Struct, frozen=True, tag=True):
    """
    Data Transfer Object (DTO) que encapsula os parâmetros necessários para
    a construção e treinamento de redes neurais no contexto do sistema.

    Esta estrutura é imutável (`frozen=True`) e deve ser utilizada para
    transportar os parâmetros de configuração entre diferentes camadas do
    sistema de forma segura e explícita.

    Atributos
    ---------
    output_dir : str, default="output/networks"
        Diretório de saída onde os artefatos da rede treinada serão salvos.

    dataset_path : str
        Caminho para o dataset de entrada utilizado no treinamento da rede.

    model_type : str, default="unet"
        Tipo de modelo de rede a ser construído (ex.: "unet", "cnn", "resnet").

    input_shape : Tuple[int, int, int], default=(128, 128, 1)
        Dimensão de entrada esperada pelo modelo, incluindo canais.

    optimizer : str, default="adam"
        Otimizador a ser utilizado durante o treinamento.

    loss : str, default="binary_crossentropy"
        Função de perda a ser utilizada durante o treinamento.

    metrics : List[str], default=["accuracy"]
        Lista de métricas adicionais para avaliação do modelo.

    batch_size : int, default=8
        Número de amostras processadas por iteração de treino.

    epochs : int, default=5
        Número total de épocas de treinamento.

    learning_rate : Optional[float], default=None
        Taxa de aprendizado do otimizador. Se `None`, usa o valor padrão
        do otimizador selecionado.

    validation_split : float, default=0.1
        Proporção do dataset a ser utilizada para validação.

    seed : Optional[int], default=None
        Semente aleatória para reprodutibilidade do treinamento.

    model_params : Dict[str, Any], default={}
        Parâmetros adicionais e específicos do modelo (pass-through).
    """
    # Caminhos e I/O
    output_dir: str = "output/networks"
    dataset_path: str = ""

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
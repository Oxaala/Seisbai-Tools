from msgspec import Struct


class HorizonDetectionParamsDTO(Struct, frozen=True, tag=True):
    """
    Data Transfer Object (DTO) que encapsula os parâmetros necessários para executar
    o processo de detecção de horizontes.

    Esta estrutura é imutável (`frozen=True`) e deve ser utilizada para transportar
    os parâmetros entre diferentes camadas do sistema de forma segura e explícita.

    Atributos
    ---------
    seismic_path : str
        Caminho para o arquivo sísmico de entrada.

    model_dir : str
        Diretório onde o modelo de detecção está armazenado.

    model_name : str
        Nome do modelo a ser utilizado no processo de detecção.

    mask_path : str
        Caminho para a máscara utilizada na detecção de horizontes.

    threshold : float, default=0.1
        Valor de limiar para definição de confiança mínima nas previsões.

    eps : float, default=0.05
        Parâmetro de distância máxima (epsilon) para o algoritmo de clusterização.

    min_points : int, default=50
        Número mínimo de pontos necessários para formar um cluster válido.

    output_dir : str, default="output/horizons"
        Diretório de saída onde os horizontes detectados serão salvos.
    """
    seismic_path: str
    model_dir: str
    model_name: str
    mask_path: str
    threshold: float = 0.1
    eps: float = 0.05
    min_points: int = 50
    output_dir: str = "output/horizons"
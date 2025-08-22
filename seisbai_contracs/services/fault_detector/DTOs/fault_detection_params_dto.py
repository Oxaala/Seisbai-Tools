from dataclasses import dataclass, field
from typing import Dict, List, Tuple

@dataclass(frozen=True)
class FaultDetectionParamsDTO:
    """
    Data Transfer Object (DTO) que agrupa os parâmetros necessários
    para configurar e executar a tarefa de detecção de falhas sísmicas.

    Attributes
    ----------
    seismic_path : str
        Caminho para o arquivo sísmico de entrada (por exemplo, em formato SEG-Y ou HDF5).
    
    model_path : str
        Caminho para o modelo de rede neural treinado que será usado para a detecção.
    
    shape : Tuple[int, int], default=(128, 128)
        Tamanho do recorte (janela) que será usado como input para o modelo.
    
    step : int, default=20
        Passo (stride) do deslizamento da janela ao percorrer o volume sísmico.
    
    axes : Dict[str, List[int]], default={"ilines": [], "xlines": [], "depths": []}
        Seleção opcional de fatias do volume sísmico a serem processadas.
        As chaves esperadas são:
            - "ilines": índices das linhas inline
            - "xlines": índices das linhas crossline
            - "depths": profundidades específicas
    
    output_dir : str, default="output/faults"
        Diretório onde os resultados da detecção de falhas serão salvos.
    """
    seismic_path: str
    model_path: str
    shape: Tuple[int, int] = (128, 128)
    step: int = 20
    axes: Dict[str, List[int]] = field(default_factory=lambda: {"ilines": [], "xlines": [], "depths": []})
    output_dir: str = "output/faults"
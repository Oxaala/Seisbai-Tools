from msgspec import Struct
from typing import Optional


class SeismicCubeParamsDTO(Struct, frozen=True, tag=True):
    """
    Data Transfer Object (DTO) para parametrização de um cubo sísmico sintético.

    Este objeto define as dimensões do cubo, parâmetros físicos do modelo
    geológico e configurações de aquisição sísmica, que serão utilizados
    pelo gerador na construção do dataset.

    Suporta valores fixos ou ranges (intervalos) para geração aleatória.
    Quando campos _min e _max estão presentes, o parâmetro é tratado como range.
    Caso contrário, usa o valor fixo.

    Attributes
    ----------
    inline : int
        Número de amostras no eixo inline (direção de disparo sísmico).
        Se inline_min e inline_max estiverem presentes, este valor é ignorado.
    xline : int
        Número de amostras no eixo crossline (perpendicular ao inline).
        Se xline_min e xline_max estiverem presentes, este valor é ignorado.
    depth : int
        Número de amostras no eixo de profundidade (Z).
        Se depth_min e depth_max estiverem presentes, este valor é ignorado.
    alpha : float
        Coeficiente de rugosidade lateral (heterogeneidade no eixo inline).
        Se alpha_min e alpha_max estiverem presentes, este valor é ignorado.
    beta : float
        Coeficiente de rugosidade lateral (heterogeneidade no eixo xline).
        Se beta_min e beta_max estiverem presentes, este valor é ignorado.
    frequency : float
        Frequência dominante da onda sísmica (em Hz).
        Se frequency_min e frequency_max estiverem presentes, este valor é ignorado.
    length : float
        Comprimento de onda (em segundos).
        Se length_min e length_max estiverem presentes, este valor é ignorado.
    dt : float
        Intervalo de amostragem temporal (em segundos).
        Se dt_min e dt_max estiverem presentes, este valor é ignorado.
    velocity_min : int
        Velocidade mínima das camadas (em m/s).
    velocity_max : int
        Velocidade máxima das camadas (em m/s).
    layers : int
        Número de camadas geológicas a serem simuladas no cubo.
        Se layers_min e layers_max estiverem presentes, este valor é ignorado.
    
    Campos opcionais para ranges (geração aleatória):
    -------------------------------------------------
    inline_min, inline_max : Optional[int]
        Range para inline (substitui inline quando presente).
    xline_min, xline_max : Optional[int]
        Range para xline (substitui xline quando presente).
    depth_min, depth_max : Optional[int]
        Range para depth (substitui depth quando presente).
    alpha_min, alpha_max : Optional[float]
        Range para alpha (substitui alpha quando presente).
    beta_min, beta_max : Optional[float]
        Range para beta (substitui beta quando presente).
    frequency_min, frequency_max : Optional[float]
        Range para frequency (substitui frequency quando presente).
    length_min, length_max : Optional[float]
        Range para length (substitui length quando presente).
    dt_min, dt_max : Optional[float]
        Range para dt (substitui dt quando presente).
    layers_min, layers_max : Optional[int]
        Range para layers (substitui layers quando presente).
    """

    inline: int
    xline: int
    depth: int
    alpha: float
    beta: float
    frequency: float
    length: float
    dt: float
    velocity_min: int
    velocity_max: int
    layers: int
    
    # Campos opcionais para ranges
    inline_min: Optional[int] = None
    inline_max: Optional[int] = None
    xline_min: Optional[int] = None
    xline_max: Optional[int] = None
    depth_min: Optional[int] = None
    depth_max: Optional[int] = None
    alpha_min: Optional[float] = None
    alpha_max: Optional[float] = None
    beta_min: Optional[float] = None
    beta_max: Optional[float] = None
    frequency_min: Optional[float] = None
    frequency_max: Optional[float] = None
    length_min: Optional[float] = None
    length_max: Optional[float] = None
    dt_min: Optional[float] = None
    dt_max: Optional[float] = None
    layers_min: Optional[int] = None
    layers_max: Optional[int] = None
from msgspec import Struct


class SeismicCubeParamsDTO(Struct, frozen=True):
    """
    Data Transfer Object (DTO) para parametrização de um cubo sísmico sintético.

    Este objeto define as dimensões do cubo, parâmetros físicos do modelo
    geológico e configurações de aquisição sísmica, que serão utilizados
    pelo gerador na construção do dataset.

    Attributes
    ----------
    inline : int
        Número de amostras no eixo inline (direção de disparo sísmico).
    xline : int
        Número de amostras no eixo crossline (perpendicular ao inline).
    depth : int
        Número de amostras no eixo de profundidade (Z).
    alpha : float
        Coeficiente de rugosidade lateral (heterogeneidade no eixo inline).
    beta : float
        Coeficiente de rugosidade lateral (heterogeneidade no eixo xline).
    frequency : float
        Frequência dominante da onda sísmica (em Hz).
    length : float
        Comprimento de onda (em segundos).
    dt : float
        Intervalo de amostragem temporal (em segundos).
    velocity_min : int
        Velocidade mínima das camadas (em m/s).
    velocity_max : int
        Velocidade máxima das camadas (em m/s).
    layers : int
        Número de camadas geológicas a serem simuladas no cubo.
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
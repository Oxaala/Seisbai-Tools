from msgspec import Struct


class PlanarDeformationParamsDTO(Struct, frozen=True, tag=True):
    """
    Data Transfer Object (DTO) para parametrização de uma deformação planar
    aplicada a um cubo sísmico sintético.

    Essa transformação gera uma deformação representada por um plano definido
    por uma inclinação nos eixos X e Y. É útil para simular inclinações ou
    mergulhos constantes nas camadas sísmicas.

    Attributes
    ----------
    intercept : int
        Intercepto do plano no eixo vertical (valor inicial da deformação).
    slope_x : float
        Inclinação do plano no eixo X (crossline).
    slope_y : float
        Inclinação do plano no eixo Y (inline).
    """

    intercept: int
    slope_x: float
    slope_y: float
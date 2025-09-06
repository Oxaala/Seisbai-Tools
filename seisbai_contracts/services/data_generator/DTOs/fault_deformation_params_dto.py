from typing import Literal
from msgspec import Struct


class FaultDeformationParamsDTO(Struct, frozen=True, tag=True):
    """
    Data Transfer Object (DTO) para parametrização de uma deformação por falha
    geológica aplicada a um cubo sísmico sintético.

    Este objeto contém as propriedades necessárias para descrever uma falha
    (normal ou reversa) e como ela deve ser aplicada ao modelo gerado.

    Attributes
    ----------
    fault_type : Literal["Normal", "Reverse"]
        Tipo da falha geológica a ser aplicada:
        - "Normal": falha normal (bloco superior desce em relação ao inferior).
        - "Reverse": falha reversa (bloco superior sobe em relação ao inferior).
    crop : bool
        Indica se a área fora da falha deve ser recortada.
    standard_amplitude : bool
        Define se a amplitude do deslocamento deve ser normalizada.
    x_origin : int
        Coordenada de origem da falha no eixo X.
    y_origin : int
        Coordenada de origem da falha no eixo Y.
    z_origin : int
        Coordenada de origem da falha no eixo Z.
    throw : int
        Deslocamento vertical máximo associado à falha (em amostras).
    dip : float
        Ângulo de mergulho da falha em graus.
    strike : float
        Ângulo de direção (strike) da falha em graus.
    """
    
    fault_type: Literal["Normal", "Reverse"]
    crop: bool
    standard_amplitude: bool
    x_origin: int
    y_origin: int
    z_origin: int
    throw: int
    dip: float
    strike: float
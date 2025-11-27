from msgspec import Struct


class GaussianDeformationParamsDTO(Struct, frozen=True, tag=True):
    """
    Data Transfer Object (DTO) para parametrização de uma deformação gaussiana
    aplicada a um cubo sísmico sintético.

    Essa transformação gera uma deformação com formato de sino (função gaussiana),
    controlada pela posição do centro, amplitude e largura (sigma). É útil para
    simular variações suaves e localizadas no modelo sísmico.

    Attributes
    ----------
    offset : int
        Deslocamento vertical de referência aplicado à deformação.
    amplitude : int
        Amplitude máxima da deformação gaussiana.
    inline_center : int
        Posição central da deformação no eixo inline.
    xline_center : int
        Posição central da deformação no eixo crossline (xline).
    sigma : int
        Largura da curva gaussiana, controlando a dispersão da deformação.
        Valores maiores resultam em uma deformação mais espalhada.
    """
    
    offset: int
    amplitude: int
    inline_center: int
    xline_center: int
    sigma: int
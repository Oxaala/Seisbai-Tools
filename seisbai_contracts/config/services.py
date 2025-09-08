from enum import Enum


class Services(Enum):
    """
    Enum que define os serviços disponíveis no sistema.

    Cada membro representa um tipo de serviço que pode ser utilizado 
    em fluxos de processamento de dados sísmicos ou aprendizado de máquina.

    Attributes
    ----------
    data_generation : str
        Serviço de geração de dados sintéticos para experimentação 
        e treinamento de modelos.
    horizon_interpolation : str
        Serviço de interpolação de horizontes sísmicos, preenchendo 
        lacunas ou suavizando superfícies geológicas.
    fault_detection : str
        Serviço de detecção automática de falhas em modelos sísmicos 
        ou dados de subsuperfície.
    network_training : str
        Serviço de treinamento de redes neurais voltado para tarefas 
        de interpretação sísmica ou predição de atributos.
    """
    data_generation = "DataGeneration"
    horizon_interpolation = "HorizonInterpolation"
    fault_detection = "FaultDetection"
    network_training = "NetworkTraining"
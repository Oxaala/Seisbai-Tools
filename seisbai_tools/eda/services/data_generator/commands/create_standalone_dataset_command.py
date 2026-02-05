"""
Comando para geração de dataset usando a configuração do standalone.
"""

from typing import Dict, Any, Optional
from uuid import UUID, uuid4
from msgspec import Struct, field

from seisbai_tools.file_system.manager import FileSystemPathInfo
from ....commands import StartCommand


class CreateStandaloneDatasetCommand(StartCommand, frozen=True, kw_only=True):
    """
    Comando que inicia a geração de um dataset usando a configuração completa
    do standalone DataGenerator.
    
    Este comando aceita a configuração e dados gerados pelos steps do standalone,
    permitindo que o server processe a geração usando os models do standalone.
    
    Atributos
    ---------
    dataset_id : UUID, default=uuid4()
        Identificador único para rastrear o job de geração do dataset.
    
    prefix : str, default="dataset"
        Prefixo base utilizado para nomear os arquivos gerados.
    
    num_samples : int, default=1
        Número de amostras a serem geradas.
    
    output_path : FileSystemPathInfo
        Informações sobre o destino dos arquivos gerados.
    
    standalone_config : Dict[str, Any]
        Configuração completa coletada dos steps do standalone.
        Contém todos os parâmetros de cada step (velocity, density, reflectivity,
        deformations, faults, salt, synthetic_traces, etc.).
    
    standalone_data : Dict[str, Any], default={}
        Dados gerados durante os steps do standalone (para referência).
        Pode conter previews ou dados intermediários.
    """
    
    dataset_id: UUID = field(default_factory=lambda: uuid4())
    prefix: str = field(default="dataset")
    num_samples: int = field(default=1)
    output_path: FileSystemPathInfo = field(default_factory=FileSystemPathInfo)
    standalone_config: Dict[str, Any] = field(default_factory=dict)
    standalone_data: Dict[str, Any] = field(default_factory=dict)





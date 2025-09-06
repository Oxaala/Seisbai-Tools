from abc import ABCMeta
from typing import Any, Dict, Type, TypeVar

# Define um tipo genérico que representa a instância da classe que usa SingletonMeta
T = TypeVar("T")

class SingletonMeta(ABCMeta):
    """
    Metaclasse para criação de classes Singleton.

    Um Singleton é um padrão de projeto que garante que uma classe possua
    apenas uma instância durante toda a execução do programa e fornece
    um ponto global de acesso a essa instância.

    Esta metaclasse pode ser usada em qualquer classe que precise do
    comportamento Singleton. Basta definir a classe alvo utilizando
    `metaclass=SingletonMeta`.

    Exemplo:
        class Config(metaclass=SingletonMeta):
            def __init__(self):
                self.value = 42

        a = Config()
        b = Config()

        assert a is b  # True, ambos são a mesma instância
    """

    # Dicionário para armazenar as instâncias únicas das classes Singleton
    _instances: Dict[Type[Any], Any] = {}

    def __call__(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        """
        Sobrescreve o método de chamada da metaclasse.

        Args:
            *args: Argumentos posicionais passados ao construtor da classe.
            **kwargs: Argumentos nomeados passados ao construtor da classe.

        Returns:
            T: A instância única da classe especificada.

        Funcionamento:
            - Verifica se já existe uma instância da classe `cls` no dicionário `_instances`.
            - Caso não exista, cria uma nova instância chamando o construtor original (`super().__call__`).
            - Armazena essa instância no dicionário `_instances`.
            - Retorna sempre a mesma instância em chamadas subsequentes.
        """
        if cls not in SingletonMeta._instances:
            # Cria a instância única caso ainda não exista
            instance = super().__call__(*args, **kwargs)  # type: ignore
            SingletonMeta._instances[cls] = instance

        # Retorna a instância já existente
        return SingletonMeta._instances[cls]
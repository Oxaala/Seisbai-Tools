import importlib


def get_type(path: str) -> type:
    """
    Importa dinamicamente um tipo a partir de seu caminho completo.

    Parameters
    ----------
    path : str
        Caminho completo no formato ``modulo.submodulo.Classe``.

    Returns
    -------
    type
        Tipo ou classe importada.

    Raises
    ------
    ModuleNotFoundError
        Se o módulo especificado não existir.
    AttributeError
        Se a classe ou tipo não for encontrado dentro do módulo.

    Examples
    --------
    >>> dt_type = _import_type("datetime.datetime")
    >>> from datetime import datetime
    >>> assert dt_type is datetime
    """
    module_name, class_name = path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)
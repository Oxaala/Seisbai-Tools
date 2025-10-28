def get_import_path(cls: type) -> str:
    """
    Retorna o caminho de importação completo de uma classe ou tipo.

    Parameters
    ----------
    cls : type
        Classe ou tipo Python a ser inspecionado.

    Returns
    -------
    str
        Caminho no formato ``modulo.submodulo.Classe``.
    
    Examples
    --------
    >>> from datetime import datetime
    >>> _get_import_path(datetime)
    'datetime.datetime'
    """
    return f"{cls.__module__}.{cls.__qualname__}"
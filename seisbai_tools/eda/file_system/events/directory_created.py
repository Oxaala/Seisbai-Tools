from seisbai_tools.eda.events import Event

class DirectoryCreatedEvent(Event, kw_only=True, frozen=True):
    """
    Evento disparado quando um diretório é criado com sucesso.

    Attributes
    ----------
    directory_path : str
        Caminho completo do diretório recém-criado.
    directory_name : str
        Nome do diretório criado, extraído de `directory_path`.
    """
    directory_path: str
    directory_name: str
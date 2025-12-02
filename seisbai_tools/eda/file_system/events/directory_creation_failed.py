from seisbai_tools.eda.events import FailedEvent


class DirectoryCreationFailedEvent(FailedEvent, kw_only=True, frozen=True):
    """
    Evento disparado quando a criação de um diretório falha.

    Este evento especializa `FailedEvent` para representar falhas
    especificamente relacionadas à criação de diretórios. Além dos campos
    herdados de `FailedEvent` (como `reason` e `exception`), ele adiciona
    o caminho do diretório que não pôde ser criado.

    Attributes
    ----------
    directory_path : str
        Caminho onde o diretório deveria ser criado e cuja criação falhou.
    """

    directory_path: str
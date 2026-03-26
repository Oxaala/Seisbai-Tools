_local_handlers_registered = False


def register_local_file_system_handlers():
    """
    Registra handlers EDA para operações de file system com `fs_type="local"`.

    O registro é idempotente e acontece sob demanda, evitando efeitos
    colaterais ao importar o pacote.
    """
    global _local_handlers_registered

    if _local_handlers_registered:
        return

    from .handlers import local_handlers  # noqa: F401
    _local_handlers_registered = True

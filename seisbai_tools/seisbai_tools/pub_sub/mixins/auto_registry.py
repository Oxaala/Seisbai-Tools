from threading import Lock


_log_file_lock = Lock()

class AutoLoggerMixin:
    def __post_init__(self):
        super_post_init = getattr(super, "__post_init__", None)

        if callable(super_post_init):
            super_post_init()
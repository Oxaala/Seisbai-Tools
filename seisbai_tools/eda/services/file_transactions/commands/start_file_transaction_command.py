import uuid

from msgspec import field

from ....commands import StartCommand
from ..DTOs import FileTransactionParamsDTO


class StartFileTransactionCommand(StartCommand, frozen=True, kw_only=True):
    dataset_id: uuid.UUID = field(default_factory=uuid.uuid4)

    params: FileTransactionParamsDTO = field(default_factory=lambda: FileTransactionParamsDTO())
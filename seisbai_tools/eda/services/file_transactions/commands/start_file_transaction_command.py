import uuid

from msgspec import field

from ....commands import Command
from ..DTOs import FileTransactionParamsDTO


class StartFileTransactionCommand(Command, frozen=True, kw_only=True):
    dataset_id: uuid.UUID = field(default_factory=uuid.uuid4)

    params: FileTransactionParamsDTO = field(default_factory=lambda: FileTransactionParamsDTO())
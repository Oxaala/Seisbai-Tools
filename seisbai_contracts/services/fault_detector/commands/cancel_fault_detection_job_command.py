from uuid import UUID
from seisbai_contracts.core import Command

class CancelFaultDetectionJobCommand(Command, frozen=True, kw_only=True):
    """
    Comando utilizado para solicitar o cancelamento de um job de
    detecção de falhas em execução no sistema Seisbai.

    Este comando segue o padrão de projeto *Command*, encapsulando
    os dados necessários para identificar qual job deve ser cancelado.

    Atributos
    ---------
    dataset_id : UUID
        Identificador único do dataset cujo job de detecção de falhas
        deve ser cancelado.

    Observações
    -----------
    - As instâncias desta classe são **imutáveis** (`frozen=True`).
    - A inicialização é feita apenas com argumentos nomeados
      (`kw_only=True`), garantindo maior clareza na criação de comandos.

    Exemplos
    --------
    >>> from uuid import UUID
    >>> cmd = CancelFaultDetectionJobCommand(
    ...     dataset_id=UUID("12345678-1234-5678-1234-567812345678")
    ... )
    >>> cmd.dataset_id
    UUID('12345678-1234-5678-1234-567812345678')
    """
    dataset_id: UUID
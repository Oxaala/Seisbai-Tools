import uuid
from seisbai_tools.eda.commands import Command


class CreateDirectoryCommand(Command, kw_only=True, frozen=True):
    """
    Representa um comando para criação de diretórios em sistemas de arquivos
    remotos (ex.: SMB, NFS, S3) ou locais.

    Este comando integra o fluxo EDA (Event-Driven Architecture) do Seisbai,
    encapsulando todas as informações necessárias para que um handler execute
    a operação de criação de diretórios no backend de armazenamento definido.

    A classe é imutável (`frozen=True`), garantindo que os dados não sejam
    alterados após sua criação. Os parâmetros são somente nomeados
    (`kw_only=True`), aumentando clareza e segurança ao instanciar.

    ---
    Atributos
    ---------
    work_id : uuid.UUID
        Identificador único associado ao workflow, processo ou sessão que
        originou a operação.

    fs_type : str
        Tipo do sistema de arquivos alvo.
        Exemplos: "SMB", "NFS", "LOCAL", "S3".

    fs_user : str
        Usuário para autenticação no backend remoto, quando aplicável.

    fs_password : str
        Senha utilizada para autenticação no backend remoto, quando aplicável.

    fs_host : str
        Endereço (hostname ou IP) do servidor que hospeda o compartilhamento
        ou bucket.

    fs_port : int, padrão = 445
        Porta utilizada para acesso ao sistema remoto.
        445 é o padrão SMB.

    fs_share : str
        Nome do compartilhamento, bucket ou raiz no backend remoto.

    fs_path : str, padrão = ""
        Caminho base dentro do compartilhamento onde o diretório será criado.

    directory_path : str
        Caminho completo (ou relativo ao fs_path) do diretório que deve ser
        criado.

    ---
    Uso
    ---
    Este comando é emitido quando o orquestrador ou o frontend precisa
    solicitar a criação de um diretório no backend configurado. O handler
    correspondente interpreta os campos e executa a operação real, respeitando
    as regras específicas de cada tipo de sistema de arquivos.

    Exemplo
    -------
    >>> CreateDirectoryCommand(
    ...     work_id=uuid.uuid4(),
    ...     fs_type="SMB",
    ...     fs_user="admin",
    ...     fs_password="1234",
    ...     fs_host="192.168.0.10",
    ...     fs_port=445,
    ...     fs_share="datasets",
    ...     fs_path="/projects",
    ...     directory_path="new_model",
    ... )
    """

    work_id: uuid.UUID
    fs_type: str
    fs_user: str
    fs_password: str
    fs_host: str
    fs_share: str
    directory_path: str
    fs_port: int = 445
    fs_path: str = ""
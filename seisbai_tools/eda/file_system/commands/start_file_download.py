import uuid

from seisbai_tools.eda.commands import StartCommand


class StartFileDownloadCommand(StartCommand, kw_only=True, frozen=True):
    """
    Representa um comando de inicialização para download de arquivos a partir
    de diferentes tipos de sistemas de arquivos remotos (ex.: SMB, NFS, S3).

    Esta classe estende `StartCommand` e reúne todas as informações necessárias
    para iniciar um processo de download dentro do fluxo EDA
    (Event-Driven Architecture) do Seisbai.

    A classe é imutável (`frozen=True`), garantindo que os dados do comando não
    sejam modificados após sua criação. Os parâmetros são **somente nomeados**
    (`kw_only=True`) para melhorar a legibilidade e evitar ambiguidades ao
    instanciar o comando.

    ---
    Atributos
    ---------
    work_id : uuid.UUID
        Identificador único do workflow ou processo ao qual o download pertence.

    fs_type : str
        Tipo do sistema de arquivos remoto de onde o arquivo será baixado.
        Exemplos comuns: `"SMB"`, `"NFS"`, `"LOCAL"`, `"S3"`.

    fs_user : str
        Nome de usuário utilizado para autenticação no sistema de arquivos remoto.

    fs_password : str
        Senha utilizada para autenticação.

    fs_host : str
        Endereço (hostname ou IP) do servidor remoto.

    fs_port : int, padrão = 445
        Porta utilizada para acessar o sistema de arquivos remoto.
        O valor padrão segue a porta usual do SMB.

    fs_share : str
        Nome do compartilhamento (SMB), bucket (S3) ou volume raiz (NFS)
        onde o arquivo está localizado.

    fs_path : str, padrão = ""
        Caminho interno dentro do compartilhamento onde o arquivo se encontra.

    remote_file_path : str
        Caminho completo do arquivo no servidor remoto (incluindo nome do arquivo).
        O handler utilizará esse caminho para localizar e baixar o arquivo.

    local_file_path : str
        Caminho absoluto local onde o arquivo deve ser salvo após o download.

    ---
    Uso
    ---
    Este comando é enviado pelo frontend ou por um orquestrador de workflows
    para solicitar o início de um processo de download. O handler responsável
    deve interpretar os parâmetros e executar a operação utilizando o protocolo
    correspondente ao tipo de sistema de arquivos.

    Exemplo
    -------
    >>> StartFileDownloadCommand(
    ...     work_id=uuid.uuid4(),
    ...     fs_type="SMB",
    ...     fs_user="admin",
    ...     fs_password="1234",
    ...     fs_host="192.168.0.10",
    ...     fs_port=445,
    ...     fs_share="datasets",
    ...     fs_path="/models",
    ...     remote_file_path="/datasets/models/vel_model.sgy",
    ...     local_file_path="/local/downloads/vel_model.sgy",
    ... )
    """

    work_id: uuid.UUID
    fs_type: str
    fs_user: str
    fs_password: str
    fs_host: str
    fs_port: int = 445
    fs_path: str = ""
    fs_share: str
    remote_file_path: str
    local_file_path: str
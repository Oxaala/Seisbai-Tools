import uuid

from seisbai_tools.eda.commands import Command


class ListFilesCommand(Command, kw_only=True, frozen=True):
    """
    Representa um comando para listagem de arquivos em sistemas de arquivos
    remotos (ex.: SMB, NFS, S3) ou locais.

    Este comando faz parte do fluxo EDA (Event-Driven Architecture) do Seisbai
    e contém todos os parâmetros necessários para que um handler consulte e
    retorne os arquivos presentes em um diretório remoto ou local.

    A classe é imutável (`frozen=True`), garantindo que os dados não sejam
    modificados após sua criação. Os parâmetros são **somente nomeados**
    (`kw_only=True`), aumentando a clareza e reduzindo ambiguidades ao
    instanciar o comando.

    ---
    Atributos
    ---------
    work_id : uuid.UUID
        Identificador do workflow, processo ou sessão associados à operação.

    fs_type : str
        Tipo do sistema de arquivos que será consultado.
        Exemplos comuns: `"SMB"`, `"NFS"`, `"LOCAL"`, `"S3"`.

    fs_user : str
        Usuário utilizado para autenticação no sistema remoto, quando aplicável.

    fs_password : str
        Senha utilizada para autenticação no sistema remoto, quando aplicável.

    fs_host : str
        Endereço (hostname ou IP) do servidor que contém o sistema de arquivos.

    fs_port : int, padrão = 445
        Porta de acesso ao sistema remoto.
        O valor padrão (445) corresponde ao protocolo SMB.

    fs_share : str
        Nome do compartilhamento, bucket ou volume raiz onde a listagem ocorrerá.

    directory : str
        Caminho interno dentro do compartilhamento/bucket onde os arquivos devem
        ser listados. Representa o diretório alvo da operação.

    fs_path : str, padrão = ""
        Compatível com comandos anteriores; pode ser usado quando o backend
        espera um caminho geral. Para novos handlers, prefira utilizar
        explicitamente `directory`.

    ---
    Uso
    ---
    O frontend ou o orquestrador emite este comando quando precisa consultar
    os arquivos disponíveis em determinado diretório remoto. O handler deve
    interpretar os parâmetros e executar a listagem utilizando o protocolo
    apropriado conforme o tipo de sistema de arquivos.

    Exemplo
    -------
    >>> ListFilesCommand(
    ...     work_id=uuid.uuid4(),
    ...     fs_type="SMB",
    ...     fs_user="admin",
    ...     fs_password="1234",
    ...     fs_host="192.168.0.10",
    ...     fs_port=445,
    ...     fs_share="datasets",
    ...     directory="/models",
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
    directory: str
import uuid

from seisbai_tools.eda.commands import StartCommand


class StartFileUploadCommand(StartCommand, kw_only=True, frozen=True):
    """
    Representa um comando de inicialização para upload de arquivos utilizando
    diferentes tipos de sistemas de arquivos remotos (ex.: SMB, NFS, S3).

    Esta classe estende `StartCommand` e agrega todas as informações necessárias
    para iniciar um processo de upload dentro do fluxo EDA (Event-Driven Architecture)
    do Seisbai.

    A classe é imutável (`frozen=True`), garantindo que os dados do comando não
    sejam alterados após sua criação. Os parâmetros são **somente nomeados**
    (`kw_only=True`) para evitar erros de ordem e aumentar a clareza ao instanciar
    o comando.

    ---
    Atributos
    ---------
    work_id : uuid.UUID
        Identificador único do trabalho (workflow) ao qual o upload pertence.

    fs_type : str
        Tipo do sistema de arquivos onde o arquivo será armazenado.
        Exemplos comuns: `"SMB"`, `"NFS"`, `"LOCAL"`, `"S3"`.

    fs_user : str
        Nome de usuário utilizado para autenticação no sistema de arquivos remoto,
        quando necessário.

    fs_password : str
        Senha utilizada para autenticação no sistema remoto.

    fs_host : str
        Endereço (hostname ou IP) do servidor que contém o sistema de arquivos.

    fs_port : int, padrão = 445
        Porta utilizada para o acesso ao sistema de arquivos.
        O valor padrão corresponde à porta usual do protocolo SMB.

    fs_share : str
        Nome do compartilhamento (SMB), bucket (S3) ou volume raiz (NFS)
        onde o arquivo será armazenado.

    fs_path : str, padrão = ""
        Caminho interno dentro do compartilhamento onde o arquivo será enviado.
        Representa pastas adicionais após o `fs_share`.
        Pode estar vazio quando o arquivo deve ser colocado na raiz do share.

    remote_file_path : str
        Caminho remoto completo de destino, resultante de:
        `fs_share + fs_path + nome_do_arquivo_remoto`.
        O handler pode usá-lo diretamente para construir a URL/caminho final.

    local_file_path : str
        Caminho absoluto no sistema local apontando para o arquivo que será enviado.

    ---
    Uso
    ---
    Este comando é emitido pelo frontend ou pelo gerenciador de workflows para
    iniciar o processo de upload. O manipulador (handler) correspondente deve
    interpretar este comando e realizar a operação apropriada conforme o tipo
    de sistema de arquivos selecionado.

    Exemplo
    -------
    >>> StartFileUploadCommand(
    ...     work_id=uuid.uuid4(),
    ...     fs_type="SMB",
    ...     fs_user="admin",
    ...     fs_password="1234",
    ...     fs_host="192.168.0.10",
    ...     fs_port=445,
    ...     fs_share="datasets",
    ...     fs_path="/models",
    ...     remote_file_path="/datasets/models/dados.sgy",
    ...     local_file_path="/local/files/dados.sgy",
    ... )
    """

    work_id: uuid.UUID
    fs_type: str
    fs_user: str
    fs_password: str
    fs_host: str
    fs_port: int = 445
    fs_share: str
    fs_path: str = ""
    remote_file_path: str
    local_file_path: str
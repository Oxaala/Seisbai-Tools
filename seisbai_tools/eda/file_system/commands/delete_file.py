import uuid

from seisbai_tools.eda.commands import Command


class DeleteFileCommand(Command, kw_only=True, frozen=True):
    """
    Representa um comando para remoção de arquivos em sistemas de arquivos
    remotos (ex.: SMB, NFS, S3) ou no sistema de arquivos local.

    Este comando faz parte do fluxo EDA (Event-Driven Architecture) do Seisbai
    e encapsula todas as informações necessárias para que um handler execute a
    operação de exclusão de um arquivo específico no backend configurado.

    A classe é imutável (`frozen=True`), garantindo que seu conteúdo não seja
    alterado após a criação. Todos os parâmetros são **somente nomeados**
    (`kw_only=True`), assegurando clareza e evitando ambiguidades na passagem
    dos argumentos.

    ---
    Atributos
    ---------
    work_id : uuid.UUID
        Identificador único do workflow, processo ou sessão que originou
        a requisição.

    fs_type : str
        Tipo do sistema de arquivos onde o arquivo será removido.
        Exemplos: `"SMB"`, `"NFS"`, `"LOCAL"`, `"S3"`.

    fs_user : str
        Usuário utilizado para autenticação no sistema remoto,
        quando aplicável.

    fs_password : str
        Senha utilizada para autenticação no sistema remoto,
        quando aplicável.

    fs_host : str
        Endereço (hostname ou IP) do servidor que hospeda o sistema de
        arquivos remoto.

    fs_port : int, padrão = 445
        Porta utilizada para conexão com o sistema remoto.
        Valor padrão (445) corresponde ao protocolo SMB.

    fs_share : str
        Nome do compartilhamento, volume, bucket ou raiz lógica onde
        o arquivo está armazenado. Exemplo (SMB): `"datasets"`.

    fs_path : str, padrão = ""
        Caminho opcional dentro do compartilhamento. Pode ser utilizado
        para compatibilidade com handlers existentes, porém o caminho final
        do arquivo deve ser fornecido através de `remote_file_path`.

    remote_file_path : str
        Caminho completo ou relativo, dentro do compartilhamento, volume ou
        bucket, apontando para o arquivo que deve ser removido. Este é o
        identificador principal do alvo da operação.

    ---
    Uso
    ---
    Este comando é emitido pelo frontend ou por um orquestrador para solicitar
    a remoção de um arquivo específico. O handler responsável deve interpretar
    os campos, estabelecer a conexão necessária (quando remota) e executar a
    exclusão conforme os protocolos e permissões do sistema de arquivos.

    Exemplo
    -------
    >>> DeleteFileCommand(
    ...     work_id=uuid.uuid4(),
    ...     fs_type="SMB",
    ...     fs_user="admin",
    ...     fs_password="1234",
    ...     fs_host="192.168.0.10",
    ...     fs_port=445,
    ...     fs_share="datasets",
    ...     fs_path="/models",
    ...     remote_file_path="old_model.sgy",
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
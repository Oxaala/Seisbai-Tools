from seisbai_tools.eda.events import FailedEvent


class FileDeletionFailedEvent(FailedEvent, kw_only=True, frozen=True):
    """
    Evento emitido quando a tentativa de deletar um arquivo falha.

    Este evento faz parte do fluxo EDA (Event-Driven Architecture) do Seisbai
    e é utilizado para comunicar que uma operação de remoção de arquivo não
    pôde ser concluída. Ele fornece informações essenciais para que handlers,
    orquestradores, serviços de logging e interfaces de usuário reajam de
    forma adequada ao erro.

    A classe é imutável (`frozen=True`) e utiliza parâmetros **somente nomeados**
    (`kw_only=True`), promovendo consistência e segurança na construção.

    ---
    Herança
    -------
    FailedEvent
        Evento-base para operações que falharam, contendo metadados opcionais
        como mensagem de erro (`reason`) e exceção capturada (`exception`).

    ---
    Atributos
    ---------
    file_path : str
        Caminho completo do arquivo cuja remoção falhou.

    ---
    Uso
    ---
    Este evento deve ser disparado pelo handler responsável sempre que a
    remoção do arquivo não puder ser concluída, seja por:

        - falta de permissões
        - arquivo inexistente
        - erro de I/O
        - falhas em serviços de armazenamento remoto
        - bloqueios externos ou corrupção de path

    Normalmente utilizado para:

        - registrar logs de erro detalhados
        - exibir notificações de falha na UI
        - disparar fluxos de fallback ou retentativas
        - auxiliar diagnósticos em serviços supervisores

    Exemplo
    -------
    >>> FileDeletionFailedEvent(
    ...     file_path="/data/projects/model.sgy",
    ...     reason="Permission denied",
    ...     exception=PermissionError("EACCES: cannot remove file")
    ... )
    """
    file_path: str
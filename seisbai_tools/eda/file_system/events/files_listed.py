from typing import List

from seisbai_tools.eda.events import Event


class FilesListedEvent(Event, kw_only=True, frozen=True):
    """
    Evento emitido quando a listagem de arquivos de um diretório é concluída
    com sucesso.

    Este evento integra o fluxo EDA (Event-Driven Architecture) do Seisbai e é
    utilizado para comunicar que os arquivos de um diretório foram obtidos
    corretamente. Ele permite que orquestradores, handlers, dashboards e a UI
    utilizem as informações para exibir conteúdo, validar estados, preencher
    listas ou realizar outras operações dependentes da listagem.

    A classe é imutável (`frozen=True`) e utiliza parâmetros **somente
    nomeados** (`kw_only=True`), garantindo clareza e consistência na criação.

    ---
    Herança
    -------
    Event
        Evento-base simples do sistema EDA, representando uma ocorrência
        concluída sem dados de progresso, falha ou métrica adicional.

    ---
    Atributos
    ---------
    directory : str
        Caminho absoluto ou relativo do diretório cuja listagem foi realizada.

    files : List[str]
        Lista dos nomes dos arquivos encontrados dentro do diretório.
        A lista pode estar vazia caso o diretório exista mas não contenha
        arquivos.

    ---
    Uso
    ---
    Este evento deve ser publicado pelo componente responsável pela leitura do
    diretório assim que a operação for concluída. Ele é comumente utilizado
    para:

        - atualizar a UI com arquivos disponíveis
        - validar workflows dependentes de determinados arquivos
        - alimentar geradores de relatórios ou dashboards
        - registrar logs de operação bem-sucedida
        - sincronizar estados entre diferentes serviços

    Exemplo
    -------
    >>> FilesListedEvent(
    ...     directory="/data/models/",
    ...     files=["layer1.npy", "layer2.npy", "velocity.sgy"]
    ... )
    """
    directory: str
    files: List[str]
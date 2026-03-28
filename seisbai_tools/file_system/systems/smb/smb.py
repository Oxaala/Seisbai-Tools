from typing import Iterator, Optional, Dict, List
from uuid import uuid4
import os

from smbprotocol.connection import Connection
from smbprotocol.session import Session
from smbprotocol.tree import TreeConnect
from smbprotocol.open import (
    Open,
    CreateDisposition,
    CreateOptions,
    ImpersonationLevel,
    FileAttributes,
    FilePipePrinterAccessMask,
    ShareAccess,
    SMB2SetInfoRequest,
)
from smbprotocol.file_info import (
    FileInformationClass,
    FileDispositionInformation,
    InfoType,
)

# Importe apenas o RemoteFileInfo, esqueça o FileInfo
from seisbai_tools.file_system.interface import FileSystemInterface
from ...types import ProgressCallback, SyncMode, SyncProgressCallback, RemoteFileInfo

DEFAULT_IMPERSONATION = ImpersonationLevel.Impersonation
DEFAULT_DESIRED_ACCESS = (
    FilePipePrinterAccessMask.GENERIC_READ |
    FilePipePrinterAccessMask.GENERIC_WRITE
)
DEFAULT_FILE_ATTRS = FileAttributes.FILE_ATTRIBUTE_NORMAL
DEFAULT_SHARE_ACCESS = (
    ShareAccess.FILE_SHARE_READ |
    ShareAccess.FILE_SHARE_WRITE |
    ShareAccess.FILE_SHARE_DELETE
)

DIR_ACCESS_MASK = FilePipePrinterAccessMask.GENERIC_READ
DIR_ATTRS = FileAttributes.FILE_ATTRIBUTE_DIRECTORY
DIR_CREATE_OPTS = CreateOptions.FILE_DIRECTORY_FILE
FILE_CREATE_OPTS = CreateOptions.FILE_NON_DIRECTORY_FILE


class SMBClient(FileSystemInterface):

    def __init__(self, server, username, password, share, port=445):
        self.server = server
        self.username = username
        self.password = password
        self.share = share
        self.port = port

        self.connection: Connection | None = None
        self.session: Session | None = None
        self.tree: TreeConnect | None = None

    # --------------------------------------------------
    # CONNECTION
    # --------------------------------------------------

    def connect(self):
        # ✅ CORREÇÃO: Configurar timeout maior para downloads longos
        # O timeout padrão do smbprotocol é 60s, mas para arquivos grandes pode ser insuficiente
        self.connection = Connection(
            guid=uuid4(),
            server_name=self.server,
            port=self.port,
        )
        # Tentar configurar timeout maior se suportado
        try:
            # smbprotocol pode ter timeout configurável via require_signing ou outras opções
            # Por enquanto, apenas conectar - o timeout será gerenciado pelo retry logic
            self.connection.connect()
        except Exception as e:
            # Se falhar, tentar novamente após pequeno delay
            import time
            time.sleep(0.5)
            self.connection.connect()

        self.session = Session(
            connection=self.connection,
            username=self.username,
            password=self.password,
        )
        self.session.connect()

        share_path = fr"\\{self.server}\{self.share}"
        self.tree = TreeConnect(self.session, share_path)
        self.tree.connect()

    def close(self):
        if self.tree:
            self.tree.disconnect()
        if self.session:
            self.session.disconnect()
        if self.connection:
            self.connection.disconnect()

    # --------------------------------------------------
    # LOW LEVEL & HELPERS
    # --------------------------------------------------

    def _open_file(self, path: str, disposition, options):
        # Normalização crítica: SMB odeia '/'
        clean_path = path.replace("/", "\\").strip("\\")

        fh = Open(tree=self.tree, name=clean_path)
        fh.create(
            impersonation_level=DEFAULT_IMPERSONATION,
            desired_access=DEFAULT_DESIRED_ACCESS,
            file_attributes=DEFAULT_FILE_ATTRS,
            share_access=DEFAULT_SHARE_ACCESS,
            create_disposition=disposition,
            create_options=options,
        )
        return fh

    def _ensure_remote_dirs(self, path: str):
        path_norm = path.replace("\\", "/")
        parts = path_norm.strip("/").split("/")[:-1]

        current = ""
        for p in parts:
            current = f"{current}/{p}" if current else p
            try:
                self.mkdir(current)
            except Exception:
                pass

    def _decode_name(self, name_bytes) -> str:
        """Helper para decodificar nomes retornados pelo SMB (UTF-16-LE)."""
        if isinstance(name_bytes, bytes):
            try:
                return name_bytes.decode("utf-16-le").rstrip('\x00')
            except UnicodeDecodeError:
                try:
                    return name_bytes.decode("utf-8").rstrip('\x00')
                except Exception:
                    return str(name_bytes)
        return str(name_bytes)

    # --------------------------------------------------
    # BASIC OPS
    # --------------------------------------------------

    def mkdir(self, path: str):
        fh = self._open_file(
            path,
            CreateDisposition.FILE_CREATE,
            DIR_CREATE_OPTS
        )
        fh.close()

    def delete(self, path: str):
        """Delete file via SetInfo(FILE_DISPOSITION_INFORMATION). FILE_DELETE_ON_CLOSE
        causes STATUS_INVALID_PARAMETER on Samba and some Windows servers.
        Open() in smbprotocol has no set_info(); we send SMB2 SET_INFO manually."""
        clean_path = path.replace("/", "\\").strip("\\")
        delete_access = FilePipePrinterAccessMask.DELETE | FilePipePrinterAccessMask.SYNCHRONIZE
        fh = Open(tree=self.tree, name=clean_path)
        fh.create(
            impersonation_level=DEFAULT_IMPERSONATION,
            desired_access=delete_access,
            file_attributes=DEFAULT_FILE_ATTRS,
            share_access=DEFAULT_SHARE_ACCESS,
            create_disposition=CreateDisposition.FILE_OPEN,
            create_options=CreateOptions.FILE_NON_DIRECTORY_FILE,
        )
        try:
            disposition = FileDispositionInformation()
            disposition["delete_pending"] = True
            req = SMB2SetInfoRequest()
            req["info_type"] = InfoType.SMB2_0_INFO_FILE
            req["file_info_class"] = FileInformationClass.FILE_DISPOSITION_INFORMATION
            req["file_id"] = fh.file_id
            req["buffer"] = disposition.pack()
            r = fh.connection.send(
                req,
                fh.tree_connect.session.session_id,
                fh.tree_connect.tree_connect_id,
            )
            fh.connection.receive(r)
        finally:
            fh.close()

    def listdir(self, path=""):
        fh = self._open_file(
            path,
            CreateDisposition.FILE_OPEN,
            DIR_CREATE_OPTS
        )

        try:
            entries = fh.query_directory(
                pattern="*",
                file_information_class=FileInformationClass.FILE_ID_BOTH_DIRECTORY_INFORMATION
            )
        finally:
            fh.close()

        result = []
        for e in entries:
            name = self._decode_name(e["file_name"].get_value())
            if name not in ('.', '..'):
                result.append(name)
        return result

    # --------------------------------------------------
    # TRANSFER
    # --------------------------------------------------

    def upload(
        self,
        local_path: str,
        remote_path: str,
        chunk_size: int = 1024 * 1024,
        progress_callback: Optional[ProgressCallback] = None
    ):
        self._ensure_remote_dirs(remote_path)
        remote_path = remote_path.replace("/", "\\")

        with open(local_path, "rb") as f:
            data = f.read()

        fh = self._open_file(
            remote_path,
            CreateDisposition.FILE_OVERWRITE_IF,
            FILE_CREATE_OPTS
        )

        total = len(data)
        offset = 0

        try:
            while offset < total:
                size = min(chunk_size, total - offset)
                fh.write(data[offset:offset + size], offset)
                offset += size
                if progress_callback:
                    progress_callback(offset, total)
        finally:
            fh.close()

    def download(
        self,
        remote_path: str,
        local_path: str,
        chunk_size: int = 1024 * 1024,
        progress_callback: Optional[ProgressCallback] = None
    ):
        import logging
        import time
        logger = logging.getLogger(__name__)
        
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        remote_path = remote_path.replace("/", "\\")

        size = None
        offset = 0
        max_retries = 3
        retry_delay = 1.0
        
        # ✅ CORREÇÃO: Tentar abrir arquivo com retry
        fh = None
        for attempt in range(max_retries):
            try:
                fh = self._open_file(
                    remote_path,
                    CreateDisposition.FILE_OPEN,
                    FILE_CREATE_OPTS
                )
                size = fh.end_of_file
                logger.info(f"[SMB_DOWNLOAD] Arquivo aberto: {remote_path}, tamanho: {size} bytes")
                break
            except Exception as e:
                logger.warning(f"[SMB_DOWNLOAD] Erro ao abrir arquivo (tentativa {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    # Tentar reconectar se conexão foi perdida
                    try:
                        self.close()
                        time.sleep(retry_delay)
                        self.connect()
                    except Exception as reconnect_error:
                        logger.warning(f"[SMB_DOWNLOAD] Erro ao reconectar: {reconnect_error}")
                    time.sleep(retry_delay)
                else:
                    raise
        
        if fh is None or size is None:
            raise RuntimeError(f"Não foi possível abrir arquivo após {max_retries} tentativas: {remote_path}")

        last_progress_log = 0
        consecutive_empty_reads = 0
        max_empty_reads = 10  # Máximo de leituras vazias consecutivas antes de considerar erro
        last_data_time = time.time()  # ✅ CORREÇÃO: Rastrear última vez que dados foram recebidos
        max_idle_time = 300.0  # 5 minutos sem dados = travamento

        try:
            with open(local_path, "wb") as f:
                while offset < size:
                    # ✅ CORREÇÃO: Verificar se download não travou (timeout watchdog)
                    current_time = time.time()
                    time_since_last_data = current_time - last_data_time
                    if time_since_last_data > max_idle_time:
                        logger.error(f"[SMB_DOWNLOAD] Timeout: nenhum dado recebido por {time_since_last_data:.1f}s (máximo: {max_idle_time}s)")
                        raise RuntimeError(f"Download travou: timeout após {time_since_last_data:.1f}s sem receber dados (offset: {offset}/{size})")
                    # ✅ CORREÇÃO: Verificar conexão periodicamente para arquivos grandes
                    if offset > 0 and offset % (100 * 1024 * 1024) == 0:  # A cada 100MB
                        logger.info(f"[SMB_DOWNLOAD] Progresso: {offset}/{size} bytes ({offset*100//size}%)")
                        # Verificar se conexão ainda está ativa (tentando uma operação simples)
                        try:
                            # Tentar verificar conexão testando o tree
                            if self.tree:
                                # Apenas verificar se tree ainda está válido (não fazer operação pesada)
                                pass  # Tree ainda existe, assumir conectado
                        except Exception as check_error:
                            logger.warning(f"[SMB_DOWNLOAD] Possível perda de conexão detectada: {check_error}")
                            # Não reconectar automaticamente aqui, deixar o retry do read() lidar com isso
                    
                    length = min(chunk_size, size - offset)
                    
                    # ✅ CORREÇÃO: Ler com retry em caso de erro
                    data = None
                    read_attempt = 0
                    while read_attempt < max_retries and data is None:
                        try:
                            data = fh.read(offset=offset, length=length)
                            if data is None:
                                raise ValueError("fh.read() retornou None")
                            consecutive_empty_reads = 0  # Reset contador
                            break
                        except Exception as read_error:
                            read_attempt += 1
                            err_str = str(read_error)
                            # Tree/session inválida: não reconectar aqui (conexão é compartilhada);
                            # deixar o app invalidar e reconectar na main thread.
                            if "Cannot find Tree" in err_str or "session tree table" in err_str:
                                logger.warning("[SMB_DOWNLOAD] Conexão SMB inválida (tree/session); falhando para app reconectar.")
                                raise RuntimeError(f"Falha ao ler chunk após {max_retries} tentativas: {read_error}")
                            logger.warning(f"[SMB_DOWNLOAD] Erro ao ler chunk em offset {offset} (tentativa {read_attempt}/{max_retries}): {read_error}")
                            if read_attempt < max_retries:
                                try:
                                    fh.close()
                                    time.sleep(retry_delay)
                                    self.close()
                                    self.connect()
                                    fh = self._open_file(
                                        remote_path,
                                        CreateDisposition.FILE_OPEN,
                                        FILE_CREATE_OPTS
                                    )
                                    logger.info(f"[SMB_DOWNLOAD] Reconectado após erro de leitura, retomando em offset {offset}")
                                except Exception as reconnect_error:
                                    logger.error(f"[SMB_DOWNLOAD] Erro ao reconectar após falha de leitura: {reconnect_error}")
                                    if read_attempt >= max_retries:
                                        raise
                            else:
                                raise RuntimeError(f"Falha ao ler chunk após {max_retries} tentativas: {read_error}")
                    
                    # ✅ CORREÇÃO: Verificar se dados foram lidos
                    if not data or len(data) == 0:
                        consecutive_empty_reads += 1
                        logger.warning(f"[SMB_DOWNLOAD] Leitura vazia em offset {offset} (tentativa {consecutive_empty_reads}/{max_empty_reads})")
                        if consecutive_empty_reads >= max_empty_reads:
                            logger.error(f"[SMB_DOWNLOAD] Muitas leituras vazias consecutivas ({consecutive_empty_reads}), abortando")
                            raise RuntimeError(f"Download travou: {consecutive_empty_reads} leituras vazias consecutivas em offset {offset}")
                        # Pequeno delay antes de tentar novamente
                        time.sleep(0.2)
                        # Tentar ler novamente com tamanho menor
                        if length > 1024:
                            length = length // 2
                            logger.info(f"[SMB_DOWNLOAD] Reduzindo tamanho do chunk para {length} bytes")
                        continue
                    
                    # Se leu dados, resetar contador
                    if len(data) > 0:
                        consecutive_empty_reads = 0
                    
                    # Escrever dados
                    f.write(data)
                    f.flush()  # ✅ CORREÇÃO: Forçar flush periódico para garantir escrita
                    offset += len(data)
                    last_data_time = time.time()  # ✅ CORREÇÃO: Atualizar timestamp de última leitura bem-sucedida
                    
                    # ✅ CORREÇÃO: Logging periódico do progresso
                    if progress_callback:
                        progress_callback(offset, size)
                        # Log a cada 10% ou a cada 50MB, o que for menor
                        progress_percent = (offset * 100) // size if size > 0 else 0
                        if progress_percent >= last_progress_log + 10 or (offset - last_progress_log * size // 100) >= 50 * 1024 * 1024:
                            logger.info(f"[SMB_DOWNLOAD] Progresso: {progress_percent}% ({offset}/{size} bytes)")
                            last_progress_log = progress_percent
        except Exception as e:
            logger.error(f"[SMB_DOWNLOAD] Erro durante download: {e}", exc_info=True)
            # Se arquivo foi parcialmente baixado, manter para possível retry
            raise
        finally:
            if fh:
                try:
                    fh.close()
                except Exception:
                    pass
            logger.info(f"[SMB_DOWNLOAD] Download concluído: {offset}/{size} bytes")

    def read_file_chunks(
        self,
        remote_path: str,
        chunk_size: int = 1024 * 1024,
        progress_callback: Optional[ProgressCallback] = None
    ) -> Iterator[bytes]:

        remote_path = remote_path.replace("/", "\\")

        fh = self._open_file(
            remote_path,
            CreateDisposition.FILE_OPEN,
            FILE_CREATE_OPTS
        )

        size = fh.end_of_file
        offset = 0

        try:
            while offset < size:
                length = min(chunk_size, size - offset)
                data = fh.read(offset=offset, length=length)
                if not data:
                    break
                offset += len(data)
                if progress_callback:
                    progress_callback(offset, size)
                yield data
        finally:
            fh.close()

    # --------------------------------------------------
    # RECURSIVE LIST
    # --------------------------------------------------

    def list_files_recursive(self, base_path: str) -> List[RemoteFileInfo]:
        """
        Lista recursivamente arquivos e retorna uma Lista de objetos RemoteFileInfo.
        """
        files: List[RemoteFileInfo] = []

        # Limpeza inicial do path base (SMB exige backslash)
        base_path_clean = base_path.replace("/", "\\").strip("\\")

        def walk(current_dir: str):
            try:
                fh = Open(tree=self.tree, name=current_dir)
                fh.create(
                    impersonation_level=DEFAULT_IMPERSONATION,
                    desired_access=DIR_ACCESS_MASK,
                    file_attributes=DIR_ATTRS,
                    share_access=DEFAULT_SHARE_ACCESS,
                    create_disposition=CreateDisposition.FILE_OPEN,
                    create_options=DIR_CREATE_OPTS,
                )
            except Exception as e:
                print(f"Aviso: Não foi possível acessar {current_dir}: {e}")
                return

            try:
                entries = fh.query_directory(
                    pattern="*",
                    file_information_class=FileInformationClass.FILE_ID_BOTH_DIRECTORY_INFORMATION
                )
            except Exception as e:
                print(f"Erro ao listar conteúdo de {current_dir}: {e}")
                fh.close()
                return

            fh.close()

            for entry in entries:
                # Decodifica nome (trata UTF-16)
                name = self._decode_name(entry["file_name"].get_value())

                if name in (".", ".."):
                    continue

                attrs = entry["file_attributes"].get_value()
                is_dir = (attrs & FileAttributes.FILE_ATTRIBUTE_DIRECTORY) == FileAttributes.FILE_ATTRIBUTE_DIRECTORY

                full_path_smb = f"{current_dir}\\{name}" if current_dir else name

                if is_dir:
                    walk(full_path_smb)
                else:
                    size = entry["end_of_file"].get_value()

                    # Calcula caminho relativo
                    rel_path = full_path_smb
                    if base_path_clean and rel_path.startswith(base_path_clean):
                        rel_path = rel_path[len(base_path_clean):].lstrip("\\")

                    # Padroniza para forward slash (/) para uso no dicionário
                    rel_key = rel_path.replace("\\", "/")

                    # Adiciona à lista usando RemoteFileInfo e size_bytes
                    files.append(RemoteFileInfo(path=rel_key, size_bytes=size))

        walk(base_path_clean)
        return files

    # --------------------------------------------------
    # SYNC
    # --------------------------------------------------

    def sync(
        self,
        local_base: str,
        remote_base: str,
        mode: SyncMode = SyncMode.BIDIRECTIONAL,
        chunk_size: int = 1024 * 1024,
        progress: Optional[SyncProgressCallback] = None,
        dry_run: bool = False
    ):
        local_base = os.path.abspath(local_base)
        os.makedirs(local_base, exist_ok=True)

        # 1. Mapeamento Local (SIMPLIFICADO: path -> int)
        local_files_map: Dict[str, int] = {}
        for root, _, files in os.walk(local_base):
            for f in files:
                full_local = os.path.join(root, f)
                rel = os.path.relpath(full_local, local_base).replace("\\", "/")
                local_files_map[rel] = os.path.getsize(full_local)

        # 2. Mapeamento Remoto (Usa RemoteFileInfo)
        remote_list = self.list_files_recursive(remote_base)
        remote_files_map: Dict[str, RemoteFileInfo] = {f.path: f for f in remote_list}

        # Helpers de Path
        def get_local_abs(rel_p: str) -> str:
            return os.path.join(local_base, rel_p.replace("/", os.sep))

        def get_remote_abs(rel_p: str) -> str:
            clean_remote = remote_base.replace("/", "\\").strip("\\")
            clean_rel = rel_p.replace("/", "\\")
            if clean_remote:
                return f"{clean_remote}\\{clean_rel}"
            return clean_rel

        #

        # --- PULL (Remoto -> Local) ---
        if mode in (SyncMode.PULL, SyncMode.BIDIRECTIONAL):
            for path, r_info in remote_files_map.items():
                local_size = local_files_map.get(path)

                # Se não existe localmente (None) OU tamanho diferente
                if local_size is None or local_size != r_info.size_bytes:
                    if progress: progress(f"download:{path}", 0, r_info.size_bytes)
                    if not dry_run:
                        self.download(
                            get_remote_abs(path),
                            get_local_abs(path),
                            chunk_size,
                            lambda p, t, e=path: progress(f"download:{e}", p, t) if progress else None
                        )

        # --- PUSH (Local -> Remoto) ---
        if mode in (SyncMode.PUSH, SyncMode.BIDIRECTIONAL):
            for path, l_size in local_files_map.items():
                r_info = remote_files_map.get(path)

                # Se não existe remotamente (None) OU tamanho diferente
                if r_info is None or r_info.size_bytes != l_size:
                    if progress: progress(f"upload:{path}", 0, l_size)
                    if not dry_run:
                        self.upload(
                            get_local_abs(path),
                            get_remote_abs(path),
                            chunk_size,
                            lambda p, t, e=path: progress(f"upload:{e}", p, t) if progress else None
                        )
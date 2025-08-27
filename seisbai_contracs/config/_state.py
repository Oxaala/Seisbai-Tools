from typing import Optional

from seisbai_contracs.core.protocols.command_bus import CommandBusProtocol
from seisbai_contracs.core.protocols.event_bus import EventBusProtocol
from seisbai_contracs.core.protocols.payload_bus import PayloadBusProtocol

#: Referência global para o PayloadBus configurado.
#:
#: Esta variável inicia como ``None`` e deve ser configurada explicitamente
#: usando ``set_payload_bus(bus: PayloadBusProtocol)`` antes de ser utilizada.
#:
#: O código da aplicação (normalmente no bootstrap) deve fornecer uma
#: implementação de :class:`PayloadBusProtocol` e registrá-la aqui.
payload_bus: Optional[PayloadBusProtocol] = None


#: Referência global para o CommandBus configurado.
#:
#: Ponto de entrada para o disparo de *commands* no sistema.
#: Assim como ``payload_bus``, começa como ``None`` e deve ser configurado
#: pelo código da aplicação através de uma função de setup como
#: ``set_command_bus(bus: CommandBusProtocol)``.
command_bus: Optional[CommandBusProtocol] = None


#: Referência global para o EventBus configurado.
#:
#: Responsável por publicar eventos de domínio e distribuí-los para os
#: *subscribers* registrados. Deve ser configurado no bootstrap da aplicação,
#: normalmente via ``set_event_bus(bus: EventBusProtocol)``.
event_bus: Optional[EventBusProtocol] = None
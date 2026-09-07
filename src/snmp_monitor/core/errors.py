"""Exceções de domínio — mensagens em PT-BR, sem community/segredo."""


class SnmpMonitorError(Exception):
    """Erro operacional do monitor SNMP."""


class SnmpConfigError(SnmpMonitorError):
    """Configuração ausente ou inválida (ex.: community no ambiente)."""


class UnknownOidError(SnmpMonitorError):
    """Apelido de OID não mapeado."""


class SnmpTimeoutError(SnmpMonitorError):
    """Agente não respondeu no timeout."""


class SnmpTransportError(SnmpMonitorError):
    """Falha de transporte (rede, recusa, dispatcher)."""


class SnmpPduError(SnmpMonitorError):
    """Agente SNMP devolveu errorStatus na PDU."""

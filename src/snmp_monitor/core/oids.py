"""Apelidos de OID do ciclo 1 (IF-MIB / SNMPv2-MIB / HOST-RESOURCES)."""

from snmp_monitor.core.errors import UnknownOidError

# Chaves em minúsculas. OID numérico passa direto em resolve_oid.
ALIASES: dict[str, str] = {
    "sysdescr": "1.3.6.1.2.1.1.1.0",
    "sysobjectid": "1.3.6.1.2.1.1.2.0",
    "sysuptime": "1.3.6.1.2.1.1.3.0",
    "sysname": "1.3.6.1.2.1.1.5.0",
    "ifdescr": "1.3.6.1.2.1.2.2.1.2",
    "ifoperstatus": "1.3.6.1.2.1.2.2.1.8",
    "ifinoctets": "1.3.6.1.2.1.2.2.1.10",
    "ifoutoctets": "1.3.6.1.2.1.2.2.1.16",
    "hrprocessorload": "1.3.6.1.2.1.25.3.3.1.2",
    "hrstoragedescr": "1.3.6.1.2.1.25.2.3.1.3",
}


def resolve_oid(raw: str) -> str:
    """Converte apelido (ifDescr) ou devolve OID numérico já válido."""
    text = raw.strip()
    if not text:
        raise UnknownOidError("OID vazio.")
    if text[0].isdigit():
        return text
    oid = ALIASES.get(text.lower())
    if oid is None:
        raise UnknownOidError(f"Apelido de OID desconhecido: {text}")
    return oid

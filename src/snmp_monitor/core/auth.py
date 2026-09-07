"""Community SNMP só vem do ambiente do SO."""

from __future__ import annotations

import os

from snmp_monitor.core.errors import SnmpConfigError


def community_from_env(var_name: str = "SNMP_COMMUNITY") -> str:
    """Lê a community; nunca loga o valor."""
    value = os.environ.get(var_name, "").strip()
    if not value:
        raise SnmpConfigError(
            f"Defina {var_name} no ambiente. "
            "Nunca grave community no git ou na linha de comando."
        )
    return value

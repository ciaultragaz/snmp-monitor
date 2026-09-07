"""Apelidos de OID viram notação numérica; OID numérico passa direto."""

import pytest

from snmp_monitor.core.errors import UnknownOidError
from snmp_monitor.core.oids import resolve_oid


def test_resolve_alias_ifdescr() -> None:
    assert resolve_oid("ifDescr") == "1.3.6.1.2.1.2.2.1.2"


def test_resolve_alias_is_case_insensitive() -> None:
    assert resolve_oid("IFDESCR") == "1.3.6.1.2.1.2.2.1.2"


def test_resolve_numeric_passthrough() -> None:
    assert resolve_oid("1.3.6.1.2.1.1.1.0") == "1.3.6.1.2.1.1.1.0"


def test_resolve_strips_whitespace() -> None:
    assert resolve_oid("  sysDescr  ") == "1.3.6.1.2.1.1.1.0"


def test_resolve_unknown_alias_raises() -> None:
    with pytest.raises(UnknownOidError, match="naoExiste"):
        resolve_oid("naoExiste")

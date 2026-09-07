"""Mapeia indicação de erro do pysnmp para exceções do domínio."""

import pytest

from snmp_monitor.core.errors import SnmpPduError, SnmpTimeoutError, SnmpTransportError
from snmp_monitor.core.session import raise_if_snmp_error


def test_timeout_indication_raises_timeout() -> None:
    with pytest.raises(SnmpTimeoutError, match="timeout"):
        raise_if_snmp_error("No SNMP response received before timeout", 0, 0)


def test_generic_indication_raises_transport() -> None:
    with pytest.raises(SnmpTransportError, match="connection refused"):
        raise_if_snmp_error("connection refused", 0, 0)


def test_pdu_error_raises() -> None:
    with pytest.raises(SnmpPduError, match="noSuchName"):
        raise_if_snmp_error(None, "noSuchName", 1)


def test_success_is_noop() -> None:
    raise_if_snmp_error(None, 0, 0)

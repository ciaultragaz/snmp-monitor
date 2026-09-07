"""Community vem só do ambiente — nunca de default no código."""

import pytest

from snmp_monitor.core.auth import community_from_env
from snmp_monitor.core.errors import SnmpConfigError


def test_community_from_env_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SNMP_COMMUNITY", raising=False)
    with pytest.raises(SnmpConfigError, match="SNMP_COMMUNITY"):
        community_from_env()


def test_community_from_env_reads_and_strips(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SNMP_COMMUNITY", "  lab-community  ")
    assert community_from_env() == "lab-community"


def test_community_from_env_custom_var(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SNMP_LAB", "outra")
    assert community_from_env("SNMP_LAB") == "outra"


def test_community_from_env_rejects_blank(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SNMP_COMMUNITY", "   ")
    with pytest.raises(SnmpConfigError, match="SNMP_COMMUNITY"):
        community_from_env()

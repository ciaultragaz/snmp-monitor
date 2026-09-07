"""CLI walk/get: tabela, JSON e community obrigatória no ambiente."""

from typing import Any

import pytest
from typer.testing import CliRunner

from snmp_monitor.cli.app import app
from snmp_monitor.core.models import SnmpVarBind

runner = CliRunner()

BINDS = [
    SnmpVarBind(oid="1.3.6.1.2.1.2.2.1.2.1", value="Gi1/0/1"),
    SnmpVarBind(oid="1.3.6.1.2.1.2.2.1.2.2", value="Gi1/0/2"),
]


@pytest.fixture
def community_ok(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SNMP_COMMUNITY", "lab")


@pytest.fixture
def fake_client(monkeypatch: pytest.MonkeyPatch, community_ok: None) -> None:
    class _Fake:
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            pass

        async def walk(self, oid: str) -> list[SnmpVarBind]:
            return BINDS

        async def get(self, oid: str) -> list[SnmpVarBind]:
            return [BINDS[0]]

    monkeypatch.setattr("snmp_monitor.cli.app.SnmpClient.from_env", classmethod(lambda cls, *a, **k: _Fake()))


def test_walk_without_community_exits_nonzero(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SNMP_COMMUNITY", raising=False)
    result = runner.invoke(app, ["walk", "192.0.2.1", "--oid", "ifDescr"])
    assert result.exit_code != 0
    assert "SNMP_COMMUNITY" in result.output


def test_walk_prints_table(fake_client: None) -> None:
    result = runner.invoke(app, ["walk", "192.0.2.1", "--oid", "ifDescr"])
    assert result.exit_code == 0
    assert "Gi1/0/1" in result.output
    assert "1.3.6.1.2.1.2.2.1.2.1" in result.output


def test_walk_json(fake_client: None) -> None:
    result = runner.invoke(app, ["walk", "192.0.2.1", "--oid", "ifDescr", "--json"])
    assert result.exit_code == 0
    assert '"value": "Gi1/0/1"' in result.output


def test_get_prints_value(fake_client: None) -> None:
    result = runner.invoke(app, ["get", "192.0.2.1", "--oid", "sysDescr"])
    assert result.exit_code == 0
    assert "Gi1/0/1" in result.output

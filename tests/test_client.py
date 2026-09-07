"""Cliente resolve OID e delega GET/WALK ao transporte (sem rede)."""

import pytest

from snmp_monitor.core.client import SnmpClient
from snmp_monitor.core.errors import UnknownOidError
from snmp_monitor.core.models import SnmpCommunityAuth, SnmpTarget, SnmpVarBind


class FakeTransport:
    def __init__(self, rows: list[SnmpVarBind]) -> None:
        self.rows = rows
        self.calls: list[tuple[str, str]] = []

    async def get(self, oid: str) -> list[SnmpVarBind]:
        self.calls.append(("get", oid))
        return [row for row in self.rows if row.oid == oid]

    async def walk(self, oid: str) -> list[SnmpVarBind]:
        self.calls.append(("walk", oid))
        prefix = oid if oid.endswith(".") else f"{oid}."
        return [
            row
            for row in self.rows
            if row.oid == oid or row.oid.startswith(prefix)
        ]


def _client(transport: FakeTransport) -> SnmpClient:
    return SnmpClient(
        target=SnmpTarget(host="192.0.2.1"),
        auth=SnmpCommunityAuth(community="lab"),
        transport=transport,
    )


@pytest.mark.asyncio
async def test_walk_resolves_alias_and_returns_binds() -> None:
    transport = FakeTransport(
        [
            SnmpVarBind(oid="1.3.6.1.2.1.2.2.1.2.1", value="eth0"),
            SnmpVarBind(oid="1.3.6.1.2.1.2.2.1.2.2", value="eth1"),
        ]
    )
    result = await _client(transport).walk("ifDescr")
    assert [bind.value for bind in result] == ["eth0", "eth1"]
    assert transport.calls == [("walk", "1.3.6.1.2.1.2.2.1.2")]


@pytest.mark.asyncio
async def test_get_resolves_sysdescr() -> None:
    transport = FakeTransport(
        [SnmpVarBind(oid="1.3.6.1.2.1.1.1.0", value="switch-lab")]
    )
    result = await _client(transport).get("sysDescr")
    assert result == [SnmpVarBind(oid="1.3.6.1.2.1.1.1.0", value="switch-lab")]
    assert transport.calls == [("get", "1.3.6.1.2.1.1.1.0")]


@pytest.mark.asyncio
async def test_walk_rejects_unknown_alias() -> None:
    with pytest.raises(UnknownOidError):
        await _client(FakeTransport([])).walk("naoExiste")

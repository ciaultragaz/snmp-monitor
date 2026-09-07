"""Cliente SNMP: resolve OID e delega GET/WALK ao transporte."""

from __future__ import annotations

from typing import Literal

from snmp_monitor.core.auth import community_from_env
from snmp_monitor.core.errors import SnmpConfigError
from snmp_monitor.core.models import SnmpCommunityAuth, SnmpTarget, SnmpTransport, SnmpVarBind
from snmp_monitor.core.oids import resolve_oid


class SnmpClient:
    def __init__(
        self,
        target: SnmpTarget,
        auth: SnmpCommunityAuth,
        transport: SnmpTransport,
    ) -> None:
        self.target = target
        self.auth = auth
        self.transport = transport

    @classmethod
    def from_env(
        cls,
        host: str,
        *,
        port: int = 161,
        timeout: float = 2.0,
        retries: int = 1,
        version: Literal["1", "2c"] | str = "2c",
        community_env: str = "SNMP_COMMUNITY",
    ) -> SnmpClient:
        if version not in ("1", "2c"):
            raise SnmpConfigError(f"Versão SNMP não suportada no ciclo 1: {version}")
        from snmp_monitor.core.session import PysnmpSession

        target = SnmpTarget(host=host, port=port, timeout=timeout, retries=retries)
        auth = SnmpCommunityAuth(
            community=community_from_env(community_env),
            version=version,  # type: ignore[arg-type]
        )
        return cls(target=target, auth=auth, transport=PysnmpSession(target, auth))

    async def get(self, oid: str) -> list[SnmpVarBind]:
        return await self.transport.get(resolve_oid(oid))

    async def walk(self, oid: str) -> list[SnmpVarBind]:
        return await self.transport.walk(resolve_oid(oid))

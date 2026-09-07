"""Sessão pysnmp 7 (v3arch asyncio) e mapeamento de erro."""

from __future__ import annotations

from snmp_monitor.core.errors import SnmpPduError, SnmpTimeoutError, SnmpTransportError
from snmp_monitor.core.models import SnmpCommunityAuth, SnmpTarget, SnmpVarBind


def raise_if_snmp_error(
    error_indication: object,
    error_status: object,
    error_index: object,
) -> None:
    """Converte indicação/PDU do pysnmp em exceção de domínio."""
    if error_indication:
        text = str(error_indication)
        if "timeout" in text.lower():
            raise SnmpTimeoutError(f"Timeout SNMP: {text}")
        raise SnmpTransportError(text)
    if error_status:
        raise SnmpPduError(f"{error_status} (index={error_index})")


def _varbinds_to_models(var_binds: object) -> list[SnmpVarBind]:
    rows: list[SnmpVarBind] = []
    if not var_binds:
        return rows
    for item in var_binds:  # type: ignore[union-attr]
        name, value = item
        pretty = value.prettyPrint() if hasattr(value, "prettyPrint") else str(value)
        rows.append(SnmpVarBind(oid=str(name), value=pretty))
    return rows


class PysnmpSession:
    """GET e WALK via pysnmp; community nunca vai para log."""

    def __init__(self, target: SnmpTarget, auth: SnmpCommunityAuth) -> None:
        self._target = target
        self._auth = auth

    def _mp_model(self) -> int:
        return 0 if self._auth.version == "1" else 1

    async def get(self, oid: str) -> list[SnmpVarBind]:
        from pysnmp.hlapi.v3arch.asyncio import (
            CommunityData,
            ContextData,
            ObjectIdentity,
            ObjectType,
            SnmpEngine,
            UdpTransportTarget,
            get_cmd,
        )

        engine = SnmpEngine()
        try:
            error_indication, error_status, error_index, var_binds = await get_cmd(
                engine,
                CommunityData(self._auth.community, mpModel=self._mp_model()),
                await UdpTransportTarget.create(
                    (self._target.host, self._target.port),
                    timeout=self._target.timeout,
                    retries=self._target.retries,
                ),
                ContextData(),
                ObjectType(ObjectIdentity(oid)),
            )
            raise_if_snmp_error(error_indication, error_status, error_index)
            return _varbinds_to_models(var_binds)
        finally:
            engine.close_dispatcher()

    async def walk(self, oid: str) -> list[SnmpVarBind]:
        from pysnmp.hlapi.v3arch.asyncio import (
            CommunityData,
            ContextData,
            ObjectIdentity,
            ObjectType,
            SnmpEngine,
            UdpTransportTarget,
            walk_cmd,
        )

        engine = SnmpEngine()
        rows: list[SnmpVarBind] = []
        try:
            async for error_indication, error_status, error_index, var_binds in walk_cmd(
                engine,
                CommunityData(self._auth.community, mpModel=self._mp_model()),
                await UdpTransportTarget.create(
                    (self._target.host, self._target.port),
                    timeout=self._target.timeout,
                    retries=self._target.retries,
                ),
                ContextData(),
                ObjectType(ObjectIdentity(oid)),
                lexicographicMode=False,
            ):
                raise_if_snmp_error(error_indication, error_status, error_index)
                rows.extend(_varbinds_to_models(var_binds))
            return rows
        finally:
            engine.close_dispatcher()

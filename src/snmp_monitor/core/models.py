"""Modelos imutáveis do ciclo 1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol


@dataclass(frozen=True)
class SnmpVarBind:
    oid: str
    value: str


@dataclass(frozen=True)
class SnmpTarget:
    host: str
    port: int = 161
    timeout: float = 2.0
    retries: int = 1


@dataclass(frozen=True)
class SnmpCommunityAuth:
    community: str
    version: Literal["1", "2c"] = "2c"


class SnmpTransport(Protocol):
    async def get(self, oid: str) -> list[SnmpVarBind]: ...

    async def walk(self, oid: str) -> list[SnmpVarBind]: ...

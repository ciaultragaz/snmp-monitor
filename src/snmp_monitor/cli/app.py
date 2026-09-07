"""CLI Typer: snmp-monitor walk|get HOST --oid ..."""

from __future__ import annotations

import asyncio
import json
from collections.abc import Awaitable, Callable

import typer

from snmp_monitor.core.client import SnmpClient
from snmp_monitor.core.errors import SnmpMonitorError
from snmp_monitor.core.models import SnmpVarBind

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    help="Monitor SNMP — GET e WALK (v1/v2c). Community só via SNMP_COMMUNITY.",
)


def _print_binds(binds: list[SnmpVarBind], as_json: bool) -> None:
    if as_json:
        payload = [{"oid": bind.oid, "value": bind.value} for bind in binds]
        typer.echo(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    if not binds:
        typer.echo("Nenhum objeto retornado.")
        return
    width = max(len("OID"), max(len(bind.oid) for bind in binds))
    typer.echo(f"{'OID'.ljust(width)}  VALUE")
    for bind in binds:
        typer.echo(f"{bind.oid.ljust(width)}  {bind.value}")


def _execute(factory: Callable[[], Awaitable[list[SnmpVarBind]]], as_json: bool) -> None:
    try:
        binds = asyncio.run(factory())
    except SnmpMonitorError as exc:
        typer.echo(f"❌ {exc}", err=True)
        raise typer.Exit(code=1) from exc
    _print_binds(binds, as_json)


@app.command("walk")
def walk_cmd(
    host: str = typer.Argument(..., help="IP ou hostname do agente SNMP"),
    oid: str = typer.Option(..., "--oid", help="OID numérico ou apelido (ex.: ifDescr)"),
    port: int = typer.Option(161, "--port", help="UDP 161 por padrão"),
    timeout: float = typer.Option(2.0, "--timeout", help="Timeout em segundos"),
    retries: int = typer.Option(1, "--retries"),
    version: str = typer.Option("2c", "--version", help="1 ou 2c"),
    as_json: bool = typer.Option(False, "--json", help="Saída JSON"),
) -> None:
    """Percorre a subárvore do OID (GETNEXT)."""

    async def _run() -> list[SnmpVarBind]:
        client = SnmpClient.from_env(
            host, port=port, timeout=timeout, retries=retries, version=version
        )
        return await client.walk(oid)

    _execute(_run, as_json)


@app.command("get")
def get_cmd(
    host: str = typer.Argument(..., help="IP ou hostname do agente SNMP"),
    oid: str = typer.Option(..., "--oid", help="OID numérico ou apelido (ex.: sysDescr)"),
    port: int = typer.Option(161, "--port", help="UDP 161 por padrão"),
    timeout: float = typer.Option(2.0, "--timeout", help="Timeout em segundos"),
    retries: int = typer.Option(1, "--retries"),
    version: str = typer.Option("2c", "--version", help="1 ou 2c"),
    as_json: bool = typer.Option(False, "--json", help="Saída JSON"),
) -> None:
    """Lê um OID (GET). Use walk para colunas de tabela (ifDescr)."""

    async def _run() -> list[SnmpVarBind]:
        client = SnmpClient.from_env(
            host, port=port, timeout=timeout, retries=retries, version=version
        )
        return await client.get(oid)

    _execute(_run, as_json)

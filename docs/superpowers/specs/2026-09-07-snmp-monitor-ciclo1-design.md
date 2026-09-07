# snmp-monitor — ciclo 1 (GET/WALK)

**Status:** aprovado pelo operador (implementar ciclo 1).  
**Fora de escopo:** SET, v3, discovery, SQLite, FastAPI, traps, Docker.

## Objetivo

CLI `snmp-monitor walk|get HOST --oid ifDescr` contra agente v1/v2c. Community só em `SNMP_COMMUNITY`.

## Stack

- Python 3.11+, `pysnmp` 7.x (LeXtudio, `hlapi.v3arch.asyncio`)
- Typer, pytest (transporte injetado — sem LAN nos testes)

## Componentes

| Módulo | Responsabilidade |
|---|---|
| `core/oids.py` | Apelido → OID numérico |
| `core/auth.py` | Community do ambiente |
| `core/client.py` | `get` / `walk` |
| `core/session.py` | pysnmp + mapeamento de erro |
| `cli/app.py` | Typer |

## Segurança

- Sem SET, sem default `public`, sem community em log/git.
- Timeout/retries configuráveis.

## Sucesso

`pytest -q` verde; smoke manual: `snmp-monitor walk <host> --oid ifDescr`.

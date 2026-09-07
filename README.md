# snmp-monitor

Monitor SNMP da Ultragaz 24H. **Ciclo 1:** GET e WALK (v1/v2c) com CLI.

Community **nunca** vai para o git, YAML ou flag `-c`. Só variável de ambiente.

## Requisitos

- Python 3.11+
- Agente SNMP acessível na UDP/161 (switch, servidor, UPS ou simulador)

## Instalação

```powershell
cd C:\Users\ultra\Github\snmp-monitor
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

## Uso

```powershell
$env:SNMP_COMMUNITY = "<community-do-ambiente>"

snmp-monitor walk 192.0.2.1 --oid ifDescr
snmp-monitor get 192.0.2.1 --oid sysDescr
snmp-monitor walk 192.0.2.1 --oid ifDescr --json
snmp-monitor walk 192.0.2.1 --oid 1.3.6.1.2.1.2.2.1.8 --version 2c --timeout 3
```

### Apelidos de OID

| Apelido | OID |
|---|---|
| `sysDescr` | `1.3.6.1.2.1.1.1.0` |
| `sysName` | `1.3.6.1.2.1.1.5.0` |
| `ifDescr` | `1.3.6.1.2.1.2.2.1.2` |
| `ifOperStatus` | `1.3.6.1.2.1.2.2.1.8` |
| `ifInOctets` | `1.3.6.1.2.1.2.2.1.10` |
| `ifOutOctets` | `1.3.6.1.2.1.2.2.1.16` |
| `hrProcessorLoad` | `1.3.6.1.2.1.25.3.3.1.2` |
| `hrStorageDescr` | `1.3.6.1.2.1.25.2.3.1.3` |

OID numérico também é aceito. `ifDescr` é coluna de tabela — use **walk**, não get.

## Testes

```powershell
pytest -q
```

Os testes **não** falam com a LAN: o transporte SNMP é injetado. O walk real é smoke manual no IP do equipamento.

## Fora deste ciclo

SET, SNMPv3, descoberta, SQLite, FastAPI, traps, Docker.

## Segurança

- Sem `SET` (escrita em equipamento).
- Sem default `public` no código.
- Timeout e retries explícitos.
- Erros de rede/PDU em PT-BR, sem ecoar community.

<!-- Template GitLab: código gerado ou assistido por IA. Humano marca o checklist. -->

## Resumo

<!-- 2–5 linhas. Efeito para o operador/usuário. -->

## Tipo

- [ ] `feat`  - [ ] `fix`  - [ ] `refactor`  - [ ] `docs`  - [ ] `chore`  - [ ] `test`  - [ ] `perf`  - [ ] `ci`

## Branch e origem

- Source: `ai/…`
- Target: `main` / `master` / `release`
- Diff aproximado: ____ linhas (se > 250, fatiar)

## Como verificar

```text
# comandos que o revisor consegue colar
```

## Checklist — revisão de código de IA

Marque **somente após ler o diff**. A IA não marca estes itens.

- [ ] Li o diff completo
- [ ] Escopo = um pedido; sem refatoração de carona
- [ ] Casos de borda cobertos ou documentados
- [ ] Sem segredo novo (`.env`, chave, token, `*.key` / `*.pem`)
- [ ] Sem PII de cliente em log/fixture
- [ ] SQL com prepared statements
- [ ] Erros de API externa tratados de forma acionável
- [ ] Pipeline desta Draft MR verde
- [ ] Linter estrito passou (pre-commit + CI)
- [ ] Sem `console.log` de debug / `var` / `chmod 777`
- [ ] Conventional Commits
- [ ] Rollback óbvio

## Segurança e dados

- Superfície nova de rede/auth/upload? `Não` / `Sim:` ____
- Mudança de preço/tabela? `Não` / `Sim — MR separado`

## Integração

- Abrir como **Draft** (`/draft`)
- Merge: **squash** na protegida
- A IA **não** aperta Merge
- Após o merge: apagar a `ai/…` remota

/draft

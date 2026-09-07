<!-- Template: código gerado ou assistido por IA. Humano marca o checklist. -->

## Resumo

<!-- 2–5 linhas. O que muda para o operador/usuário, não a lista de arquivos. -->

## Tipo

- [ ] `feat`  - [ ] `fix`  - [ ] `refactor`  - [ ] `docs`  - [ ] `chore`  - [ ] `test`  - [ ] `perf`  - [ ] `ci`

## Branch e origem

- Branch: `ai/…`
- Base: `main` / `master` / outra: ____
- Diff aproximado: ____ linhas (se > 250, este PR deve ser fatiado)

## Como verificar

```text
# comandos que o revisor consegue colar
```

## Checklist — revisão de código de IA

Marque **somente após ler o diff**. A IA não marca estes itens.

- [ ] Li o diff completo (não só a descrição)
- [ ] Escopo = um pedido; sem refatoração de carona
- [ ] Casos de borda cobertos ou documentados (vazio, erro, timeout, retry)
- [ ] Sem segredo novo (`.env`, chave, token, cookie, `*.key` / `*.pem`)
- [ ] Sem PII de cliente (CPF, telefone, endereço, e-mail em log/fixture)
- [ ] SQL com prepared statements; sem concatenar input em query
- [ ] Chamadas externas com tratamento de erro acionável
- [ ] Testes automatizados passam na CI desta Draft PR
- [ ] Linter estrito passou (hook pre-commit + CI)
- [ ] Não há `console.log` de debug / `var` / `chmod 777`
- [ ] Mensagens de commit no padrão Conventional Commits
- [ ] Rollback óbvio (revert deste squash ou feature flag)

## Segurança e dados

- Superfície nova de rede/auth/upload? `Não` / `Sim:` ____
- Precisa de `/preco-seguro` ou mudança de tabela? `Não` / `Sim — PR separado`

## CI

- [ ] Checks verdes nesta Draft PR **antes** de pedir review final
- [ ] Sem skip de hook (`--no-verify`) nos commits

## Integração

- Merge: **squash** na protegida
- A IA **não** aperta Merge
- Após o merge: apagar a `ai/…` remota

# Como contribuir

Correções e melhorias são bem-vindas, por issue ou pull request. Antes de abrir um, siga as regras abaixo.

## Onde editar

1. Edite só em `base/` e nos `SKILL.md`. Nunca edite `skills/*/references/` nem `skills/*/LICENSE`: são cópias geradas e o script sobrescreve.
2. Depois de mexer em `base/` ou no `LICENSE`, rode:

   ```bash
   python3 scripts/sincronizar.py
   python3 scripts/sincronizar.py --check
   ```

   O segundo comando precisa terminar com "tudo sincronizado".
3. Mexeu em `.claude-plugin/marketplace.json`? Rode `claude plugin validate .` antes de enviar.

## Skill nova

Crie `skills/<nome>/SKILL.md` no mesmo formato das existentes: cabeçalho YAML com `name`, `description` (entre aspas duplas, até 1024 caracteres), `license` e `metadata`. Depois registre a skill em:

- `base/mapa.json` (quais arquivos de base ela leva);
- `.claude-plugin/marketplace.json`;
- a tabela do `README.md`;
- o `CHANGELOG.md`.

Toda skill nova entra com exemplo de prompt e de retorno, sem dado real de conta (nomes anonimizados ou fictícios), e só depois de executada ao vivo.

## Conteúdo

- **Nada de dado real de conta:** nomes de projetos e de contas, emails, IDs, links de relatórios, nomes de clientes ou de pessoas e métricas de cliente. Exemplos usam "Cliente A", "Cliente B", IDs inventados e o domínio reservado `.example`.
- **Comportamento do conector entra descrito (como e quando ocorre), sem dado de conta.** Se o conector mudou, atualize a base, não só a skill.
- **Acesso à conta só pelo conector MCP oficial do Reportei.** Não acrescente outro meio.
- **Skill que escreve na conta** mostra a prévia e pede confirmação explícita antes de cada escrita, e nunca liga envio automático sem um sim para isso.
- Português do Brasil, direto, sem travessão.

## Versão

Mudança publicada ganha entrada no `CHANGELOG.md` e atualização da versão em `.claude-plugin/marketplace.json` e no `metadata` dos `SKILL.md` alterados, seguindo o [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## Licença das contribuições

Ao contribuir, você autoriza a Astronauta Digital LTDA a usar, modificar e distribuir sua contribuição sob a licença deste repositório ([LICENSE](LICENSE)).

# Skills do Reportei para contas

Skills para **Claude Code** e **Codex** entenderem uma conta no **Reportei** em linguagem de gente: como foi o marketing, redes sociais, site, anúncios, conteúdo, público e metas, além de criar relatórios, dashboards e envios automáticos, a partir de pedidos em português. Feitas por [Eduardo Campos](https://github.com/eueduardocampos), conselheiro da Astronauta Martech, e validadas ao vivo na Astronauta Martech.

Cada skill foi testada ao vivo com o conector oficial do Reportei antes de entrar aqui.


## Instalação

### Claude Code e Codex, com um comando

```bash
npx skills add eueduardocampos/reportei-contas-skills -g
```

O instalador pergunta quais skills você quer e em qual ferramenta instalar. O `-g` instala na sua pasta de usuário, e as skills valem em qualquer projeto.

### Claude Code, como plugin

```
/plugin marketplace add eueduardocampos/reportei-contas-skills
/plugin install reportei-contas@reportei-contas-skills
```

### Manual

```bash
git clone https://github.com/eueduardocampos/reportei-contas-skills.git
mkdir -p ~/.claude/skills
cp -R reportei-contas-skills/skills/* ~/.claude/skills/
```

No Codex, o destino é `~/.agents/skills/`.

Se você é agência e quer a visão da carteira inteira, veja também o pacote [reportei-agencia-skills](https://github.com/eueduardocampos/reportei-agencia-skills).

## As skills

| Skill | O que faz | Na conta |
|---|---|---|
| `reportei-conta-analista-de-audiencia` | Quem é o seu público de verdade: idade, gênero, país e cidade | só lê |
| `reportei-conta-analista-de-performance` | Como foi o marketing no período, sem jargão | só lê |
| `reportei-conta-analista-de-redes-sociais` | Desempenho orgânico das redes sociais em profundidade | só lê |
| `reportei-conta-analista-de-site` | Tráfego, comportamento e conversão do site | só lê |
| `reportei-conta-assistente-de-automacao` | O envio automático do relatório | cria, altera, liga ou pausa, com confirmação |
| `reportei-conta-coach-de-metas` | Metas realistas e o progresso de cada uma | cria ou altera, com confirmação |
| `reportei-conta-comparador-de-periodos` | Melhor ou pior do que antes, em todas as plataformas | só lê |
| `reportei-conta-especialista-em-conteudo` | O que funcionou no conteúdo e o que repetir | só lê |
| `reportei-conta-gerador-de-relatorios` | O relatório pronto, com o link para compartilhar | cria, com confirmação |
| `reportei-conta-gestor-de-dashboard` | Dashboards ao vivo, com o link permanente | cria, com confirmação |
| `reportei-conta-historiador-da-conta` | Os marcos e a memória da conta na linha do tempo | cria, altera ou apaga, com confirmação |
| `reportei-conta-monitor-de-anuncios` | Investimento, ROAS e conversões dos anúncios | só lê |

## Requisitos

- O Claude Code ou o Codex.
- Uma conta no Reportei nos planos Starter, PRO ou Premium, com acesso ao projeto e pelo menos uma integração conectada.
- O conector MCP oficial do Reportei ligado no seu agente: adicione um conector personalizado com a URL `https://app.reportei.com/mcp` e entre com a sua conta do Reportei ([passo a passo do Reportei](https://reportei.com/claude-mcp/)).

## Instalou os dois pacotes?

O pacote de agências olha a carteira inteira; o de contas aprofunda um cliente de cada vez. Alguns pedidos servem para os dois (relatório, automação, meta, linha do tempo). Se o agente escolher a skill de um pacote e você queria a do outro, diga qual usar: "use a visão de agência" ou "use a visão de contas". As duas pedem confirmação antes de qualquer escrita.

## Segurança

- As skills que criam, alteram ou apagam algo na conta (relatório, dashboard, meta, automação, registro da linha do tempo) mostram antes exatamente o que vão fazer e esperam um "sim".
- Automação de envio é criada e conferida desligada. Ligar o envio sempre pede um "sim" próprio, depois de você ver o que foi gravado.
- Relatório, dashboard, meta e automação não podem ser apagados pelo conector; apagar registro da linha do tempo é definitivo. As skills avisam isso antes.
- Relatório e dashboard consomem a cota do seu plano do Reportei e geram um link que abre sem login.
- Essas regras valem para as skills deste pacote. Outras ferramentas instaladas no seu agente seguem as regras delas.

## Limites conhecidos do conector

Os detalhes ficam em `base/conector-reportei.md`. Os mais importantes:

- Ferramentas de resumo e de comparação podem voltar parciais ou mostrar só uma conta quando o projeto tem várias da mesma plataforma. As skills conferem e completam conta por conta.
- O investimento de Meta Ads e Google Ads não vem na comparação de períodos; as skills buscam à parte.
- As skills fazem uma chamada por vez ao conector.

## Estrutura

```
base/                  fonte única do conhecimento compartilhado
  mapa.json            quais arquivos de base cada skill leva
skills/<nome>/         uma pasta por skill, autossuficiente
  SKILL.md
  references/          cópia gerada de base/
  LICENSE              cópia gerada
scripts/sincronizar.py copia base/ e LICENSE para dentro das skills
.claude-plugin/        manifesto do marketplace do Claude Code
```

Edite sempre em `base/` e rode `python3 scripts/sincronizar.py`. Para contribuir, veja [CONTRIBUTING.md](CONTRIBUTING.md); o histórico está em [CHANGELOG.md](CHANGELOG.md).

## Licença

[MIT](LICENSE) © 2026 Eduardo Campos. Uso livre e gratuito, inclusive comercial, com o aviso de licença mantido.

Reportei, Claude e Codex são marcas de seus respectivos titulares. Este projeto não é afiliado nem endossado por eles.

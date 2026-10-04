---
name: "reportei-conta-comparador-de-periodos"
description: "Responde \"estou melhor ou pior do que antes?\" para uma conta no Reportei: compara dois períodos em todas as plataformas conectadas, mostra o que cresceu, o que caiu e o que ficou parado, com variação em número e em percentual, e fecha com uma conclusão de uma linha. Use quando alguém perguntar \"estou melhor ou pior que o mês passado?\", \"compara setembro com agosto\", \"evoluí no trimestre?\", \"como foi esse ano contra o ano passado?\" ou \"o que puxou o crescimento esse mês?\". Só lê. Para um resumo do período sem foco em comparação, prefira reportei-conta-analista-de-performance; para detalhar uma plataforma, reportei-conta-analista-de-redes-sociais, reportei-conta-monitor-de-anuncios ou reportei-conta-analista-de-site; para gerar um relatório comparativo para enviar, reportei-conta-gerador-de-relatorios. Requer o conector MCP do Reportei."
license: "MIT"
metadata:
  version: "0.1.1"
  author: "Eduardo Campos"
  produto: "Reportei"
  requer: "conector MCP do Reportei"
---

# Comparador de períodos

Você responde "evoluí?" para quem não é analista. Não basta pôr números lado a lado: a entrega diz o que a variação significa, se é boa ou má notícia e o que pede atenção. Leitura pura: **nenhuma chamada que escreva na conta**.

## Referências

- `references/conector-reportei.md`: ferramentas, parâmetros e o que o conector não mostra. **Leia primeiro.**
- `references/metricas-e-integracoes.md`: o que cada métrica quer dizer e quais são "menor é melhor" (seção "Métricas em que menor é melhor").
- `references/disciplina-de-evidencia.md`: como escrever números, comparações, hipóteses e o que não foi visto. **Aplique antes de entregar.**
- `references/formato-de-resposta.md`: tom, estrutura e tamanho da resposta.

## Como ler a variação

| Variação | Como dizer |
|---|---|
| acima de +20% | cresceu bastante |
| de +5% a +20% | cresceu |
| de -5% a +5% | ficou estável |
| de -5% a -20% | caiu; vale olhar |
| abaixo de -20% | caiu bastante; pede ação |

Em métricas de custo (CPC, CPM, custo por resultado), taxa de rejeição e posição média no Google, **inverta**: subir é piorar. Use a lista da seção "Métricas em que menor é melhor" de `references/metricas-e-integracoes.md`. Base pequena (ex.: de 4 para 9 leads) gera percentual grande: nesses casos, destaque o número absoluto.

## Passo a passo

```
- [ ] 1. Resolver o projeto
- [ ] 2. Fixar os dois períodos
- [ ] 3. Ver o que está conectado
- [ ] 4. Comparar
- [ ] 5. Separar o que melhorou, piorou e ficou estável
- [ ] 6. Escrever a conclusão
```

Uma chamada ao Reportei por vez, conferindo projeto e formato em cada resposta (`references/conector-reportei.md`).

1. **Projeto:** `list_projects` (com `search` se a pessoa citou um nome; se `meta.last_page` for maior que 1, peça as outras páginas antes de decidir). A busca é literal: se vier vazio, tente um trecho menor do nome, sem acento ou sem espaço. Um projeto só: use e diga o nome na resposta. Mais de um possível, ou nenhum nome citado: mostre a lista curta e pergunte qual. Nunca misture números de projetos diferentes.
2. **Períodos:** converta tudo em datas absolutas (`AAAA-MM-DD`) antes de chamar qualquer ferramenta e escreva as datas na resposta.
   - "esse mês contra o passado": do dia 1 até hoje (avise que hoje ainda está incompleto) contra o **mesmo número de dias** do mês anterior (1 a 15 de abril contra 1 a 15 de março), não contra o mês inteiro;
   - "abril contra março": os dois meses fechados;
   - "trimestre" e "ano": os períodos fechados correspondentes; se a pessoa disser "esse ano", compare até a mesma data do ano anterior;
   - "contra o ano passado": o mesmo mês (ou trimestre) do ano anterior. Útil quando o negócio é sazonal.
   Se os dois períodos têm tamanhos diferentes e a pessoa insistir, avise que totais (visitas, alcance) ficam desiguais e compare médias por dia. Em dúvida sobre fuso, `get_project` traz o `timezone`.
3. **Integrações:** `list_integrations` com o `projectId`, com `created_at` de cada uma. Plataforma conectada no meio do período ou inativa em um dos dois explica salto ou queda: zero ali não é zero, é sem base. Mais de uma conta da mesma plataforma: anote cada uma; elas são lidas conta por conta e nunca somadas nem comparadas entre si.
4. **Comparar:**
   - visão geral: `compare_periods` com `projectId`, `startDate`, `endDate` (período atual), `comparisonStartDate`, `comparisonEndDate` (período de base). Depois, confira se cada integração de `list_integrations` aparece: o retorno pode vir parcial (`partial_results`, `sources_with_errors`; repita uma vez) e, com duas contas do mesmo tipo, mostrar uma só sem avisar. Conta faltando: busque com `get_metrics_data`;
   - investimento de Meta Ads e Google Ads não vem em `compare_periods`: busque à parte com `get_metrics_data`, conta a conta, nos dois períodos;
   - "o que puxou?" ou "social ou anúncios?": `get_channel_breakdown` duas vezes, uma para cada período, e compare as categorias (redes sociais, anúncios, site, CRM, loja, email);
   - pergunta sobre uma métrica de uma plataforma só: `list_metrics` com o slug e `get_metrics_data` com `integrationId`, `start`, `end`, `comparisonStart`, `comparisonEnd` e os objetos exatamente como `list_metrics` devolveu (com `id`: o que `list_metrics` trouxer ou, se não vier, o `reference_key`). Catálogo grande: `list_metrics` com `perPage` entre 15 e 25, paginando até achar.
5. **Separar:** se houver anúncios, ponha primeiro o investimento dos dois períodos: volume sem investimento não diz se melhorou. Classifique cada métrica pela tabela acima (já invertendo as de custo). Valor em um período e zero ou vazio no outro vai em "Novo ou sem base". Escolha no máximo 4 melhoras e 4 pioras, as maiores e as que importam para o negócio; o resto vai em "estável" ou fica de fora.
6. **Concluir:** uma frase no topo responde a pergunta ("abril foi melhor que março em alcance e pior em custo de anúncio"). Se houver explicação conhecida para uma variação (sazonalidade, integração nova, mês mais curto), escreva como contexto ou hipótese, nunca como fato sem dado.

## Regras

- Sempre a variação absoluta **e** a percentual, com os dois valores: "de 2.000 para 2.400 (+400, +20%)".
- Queda relevante entra, mesmo que o resto esteja bom. Não suavize.
- Não some métricas de plataformas diferentes que medem coisas diferentes.
- Integração inativa ou sem dado em um dos períodos: diga isso; não trate como queda para zero.
- Causa só como hipótese, com o dado que a sustenta. Sem dado, "não dá para saber pelo Reportei".

## Formato de entrega

```markdown
**<Projeto> · <período atual> contra <período de base>**

<Uma frase que responde: melhor, pior ou misto, e em quê.>

**Melhorou**
- <plataforma · métrica>: de <antes> para <agora> (<+abs>, <+%>). <o que significa>.

**Piorou**
- <plataforma · métrica>: de <antes> para <agora> (<abs>, <%>). <o que significa ou hipótese>.

**Estável:** <métricas, em uma linha>.

**Novo ou sem base:** <métricas ou contas sem valor em um dos períodos>.

**O que assumi:** <datas exatas dos dois períodos; de onde veio o investimento>
**Limites:** <integrações inativas, novas ou que não vieram na comparação; período incompleto>
```

## Não faz

- Não gera relatório comparativo para enviar (use `reportei-conta-gerador-de-relatorios`).
- Não detalha uma plataforma a fundo (use as skills de redes sociais, anúncios ou site).
- Não acompanha metas (use `reportei-conta-coach-de-metas`).
- Não traz dado que não está no Reportei.

## Exemplo de prompt

> Estou melhor ou pior que o mês passado?

## Exemplo de retorno

Exemplo ilustrativo (nomes e números fictícios):

> **Cliente B · abril de 2026 contra março de 2026**
>
> Abril foi melhor em alcance e conversões e pior em custo dos anúncios: no geral, evoluiu, com atenção à mídia paga.
>
> Investimento no Google Ads: de R$ 6.000,00 para R$ 10.000,00 (+R$ 4.000,00, +67%).
> Investimento no Meta Ads: de R$ 3.000,00 para R$ 3.000,00 (+R$ 0,00, 0%).
>
> **Melhorou**
> - Instagram · alcance somado: de 200 mil para 240 mil (+40 mil, +20%). A marca apareceu mais vezes (alcance somado por dia, com repetição).
> - Google Ads · conversões: de 300 para 400 (+100, +33%).
> - Instagram · seguidores ganhos: de 2.000 para 2.500 (+500, +25%).
> - LinkedIn · seguidores ganhos: de 40 para 45 (+5, +12,5%). Base pequena: vale pelo número, não pelo percentual.
>
> **Piorou**
> - Google Ads · custo por conversão: de R$ 20,00 para R$ 25,00 (+R$ 5,00, +25%). Cada conversão ficou mais cara. Hipótese: a campanha sazonal começou em 20/04.
> - Meta Ads · CTR: de 2,0% para 1,5% (-0,5 p.p., -25%).
>
> **Estável:** visitas ao site (+2,5%).
>
> **Novo ou sem base:** TikTok (integração conectada no meio do mês, sem base de comparação).
>
> **O que assumi:** 01/04/2026 a 30/04/2026 contra 01/03/2026 a 31/03/2026; investimento lido conta a conta.
> **Limites:** nenhuma integração inativa no período.

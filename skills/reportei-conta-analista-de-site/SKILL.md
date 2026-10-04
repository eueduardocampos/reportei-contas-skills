---
name: "reportei-conta-analista-de-site"
description: "Explica em linguagem simples o que acontece no site de uma conta no Reportei: quantas pessoas chegam, de onde vêm, o que fazem, quantas viram contato ou venda e como o site aparece no Google, usando Google Analytics 4, Search Console e loja virtual conectada (Shopify, WooCommerce). Use quando alguém perguntar \"como está meu site?\", \"quantas visitas tive em setembro?\", \"de onde vêm meus visitantes?\", \"meu SEO está funcionando?\", \"como estou no Google?\" ou \"como estão as vendas da loja?\". Só lê. Para o resumo de todos os canais, prefira reportei-conta-analista-de-performance; para redes sociais, reportei-conta-analista-de-redes-sociais; para anúncios, reportei-conta-monitor-de-anuncios. Requer o conector MCP do Reportei."
license: "MIT"
metadata:
  version: "0.1.1"
  author: "Eduardo Campos"
  produto: "Reportei"
  requer: "conector MCP do Reportei"
---

# Analista de site

Você responde "meu site está trazendo resultado?" para quem não é analista. Tráfego sozinho é só um número: a entrega liga visitas a resultado (contato, cadastro, venda) e diz de onde vem o que funciona. Leitura pura: **nenhuma chamada que escreva na conta**.

## Referências

- `references/conector-reportei.md`: ferramentas, parâmetros e o que o conector não mostra. **Leia primeiro.**
- `references/metricas-e-integracoes.md`: slugs, o que cada métrica quer dizer e quais são "menor é melhor" (seção "Métricas em que menor é melhor": taxa de rejeição, posição média no Google).
- `references/disciplina-de-evidencia.md`: como escrever números, comparações, hipóteses e o que não foi visto. **Aplique antes de entregar.**
- `references/formato-de-resposta.md`: tom, estrutura e tamanho da resposta.

## Fontes cobertas

| Fonte | Slug | Responde |
|---|---|---|
| Google Analytics 4 | `google_analytics_4` | visitas (sessões), pessoas (usuários), origem do tráfego, páginas, conversões |
| Google Search Console | `search_console` | quantas vezes o site apareceu no Google, cliques, taxa de clique, posição média |
| Shopify | `shopify` | pedidos, receita, ticket médio, taxa de conversão da loja |
| WooCommerce | `woocommerce` (a confirmar) | pedidos, receita, ticket médio |

Confirme o slug em `list_integrations` antes de usar: o que vale é o que a conta tem conectado. O marcado "a confirmar" ainda não foi confirmado.

## Passo a passo

```
- [ ] 1. Resolver o projeto
- [ ] 2. Fixar o período
- [ ] 3. Ver quais fontes de site estão conectadas
- [ ] 4. Escolher o caminho pela pergunta
- [ ] 5. Buscar e comparar
- [ ] 6. Escrever a leitura
```

Uma chamada ao Reportei por vez, conferindo projeto e formato em cada resposta (`references/conector-reportei.md`).

1. **Projeto:** `list_projects` (com `search` se a pessoa citou um nome; se `meta.last_page` for maior que 1, peça as outras páginas antes de decidir). A busca é literal: se vier vazio, tente um trecho menor do nome, sem acento ou sem espaço. Um projeto só: use e diga o nome na resposta. Mais de um possível, ou nenhum nome citado: mostre a lista curta e pergunte qual. Nunca misture números de projetos diferentes.
2. **Período:** converta datas relativas em datas absolutas (`AAAA-MM-DD`). Sem período, use o último mês fechado e diga isso. Se o período inclui hoje, avise que o dia ainda está incompleto; no Search Console, avise também que os últimos 2 ou 3 dias costumam chegar atrasados. Em dúvida sobre fuso, `get_project` traz o `timezone`.
3. **Fontes:** `list_integrations` com o `projectId`. Anote GA4, Search Console e loja, com `id`, `slug`, `status` e `created_at`. Se a fonte que a pergunta pede não está conectada ou está inativa (ex.: "como estou no Google?" sem Search Console), diga isso logo e responda só com o que existe. Mais de uma conta da mesma fonte: leia uma por uma, sem somar. Fonte conectada no meio do período: zero antes da conexão não é zero, é sem dado.
4. **Caminho pela pergunta:**
   - "como está meu site?": GA4 direto com `get_metrics_data`; `get_performance_summary` só como atalho, e ele pode vir parcial ou pular a fonte (confira `partial_results` e `sources_with_errors`);
   - "de onde vêm os visitantes?": GA4, tabela de canais ou de origem/mídia;
   - "quais páginas mais vistas?": GA4, tabela de páginas por caminho e de páginas de entrada;
   - "virou contato?": GA4, conversões (key events) e eventos. Conversão zero nos dois períodos com a tabela de conversões "sem dado" indica conversão não configurada: veja na tabela de eventos se há candidatos (envio de formulário, lead). Se o projeto tiver RD Station ou CRM conectado, o contato pode estar lá: cite como fonte diferente, sem somar;
   - "como estou no Google?" ou "meu SEO funciona?": Search Console;
   - "como estão as vendas da loja?": Shopify ou WooCommerce.
5. **Buscar e comparar:** `list_metrics` com o slug da fonte (o catálogo do GA4 é grande: use `perPage` menor e pagine), escolha as métricas do caminho e chame `get_metrics_data` com `integrationId`, `start`, `end`, `comparisonStart`, `comparisonEnd` e os objetos exatamente como `list_metrics` devolveu, cada um com `id` (o que `list_metrics` trouxer ou, se não vier, o `reference_key`). Nunca invente `reference_key`. Tabelas não devolvem o período anterior: para variar canal ou página, use widgets de número por grupo de canal se o catálogo tiver; se não, faça uma segunda chamada com o período anterior. Tabelas podem vir fora de ordem: ordene você.
6. **Escrever:** comece pela frase que responde a pergunta. Depois os blocos que se aplicam (tráfego, origem, páginas, resultado, Google, loja), cada um com número, variação e o que significa. Feche com o próximo passo prático.

## Regras

- Ligue tráfego a resultado sempre que houver dado: visitas, quantas viraram conversão e, na loja, quanto isso deu em receita. Se a conversão não está configurada no GA4, diga que não dá para ligar e por quê.
- Origem em percentual do total ("42% das visitas vêm da busca no Google") é mais útil que número solto.
- GA4 e Search Console medem coisas diferentes: cliques do Search Console não são sessões do GA4 e os números não batem. Não some nem compare um com o outro como se fossem a mesma coisa.
- Em posição média no Google e em taxa de rejeição, cair é melhorar. Use a lista de `references/metricas-e-integracoes.md` (seção "Métricas em que menor é melhor").
- Pico ou queda brusca merece hipótese, marcada como hipótese e com o dado que a sustenta. Sem dado, "não dá para saber pelo Reportei".
- Fonte sem dado no período: liste em "Limites", não invente zero.
- Soma das linhas de uma tabela (canais, eventos) não bate com o total de sessões: use o total do widget de número, não a soma.
- Páginas administrativas ou com tempo de engajamento zero no topo da lista: sinalize como provável uso interno ou robô (hipótese).

## Formato de entrega

```markdown
**Site · <Projeto> · <período> (comparado a <período anterior>)**

<Uma frase que responde a pergunta.>

**Tráfego:** <visitas> (<variação>), <pessoas> (<variação>).
**De onde vêm:** <canal> <x%>, <canal> <y%>, <canal> <z%>.
**Resultado:** <conversões ou pedidos> (<variação>); <taxa de conversão>; <receita, se houver loja>.
**Páginas:** <top 3 a 5 por visualização>.
**No Google:** <cliques> (<variação>), <aparições> (<variação>), posição média <n>.

**Próximo passo:** <uma ação prática>.

**O que assumi:** <período, base de comparação, o que contei como conversão>
**Limites:** <fontes não conectadas ou inativas; conversão não configurada; tabelas sem comparação; atraso do Search Console; período incompleto>
```

Use só os blocos que a pergunta pede e que têm dado.

## Não faz

- Não analisa redes sociais (use `reportei-conta-analista-de-redes-sociais`).
- Não analisa campanhas de anúncio (use `reportei-conta-monitor-de-anuncios`).
- Não faz SEO técnico nem auditoria do site: só lê o que o Reportei traz.
- Não traz dado que não está no Reportei (vendas fora da loja conectada, por exemplo).
- Não cria relatório, dashboard, meta ou automação.

## Exemplo de prompt

> Meu SEO está funcionando?

## Exemplo de retorno

Exemplo ilustrativo (nomes e números fictícios):

> **Site · Cliente D · abril de 2026 (comparado a março)**
>
> Sim: o Cliente D apareceu mais no Google e houve mais cliques.
>
> **No Google:** 4.500 cliques (+12,5%), 105 mil aparições nos resultados (+5%). A taxa de clique (de cada 100 aparições, quantas viram clique) subiu de 4,0% para 4,3%. Posição média 14,0, praticamente igual a março (14,2).
> **Resultado:** no GA4, as visitas de busca orgânica (canal Organic Search, que inclui outros buscadores além do Google) tiveram 200 vendas atribuídas na loja virtual (+10%), 40% de todas as vendas do site.
>
> **Próximo passo:** posição média perto de 14 quer dizer que boa parte das aparições está na segunda página do Google. Os termos que já estão entre a 8ª e a 15ª posição são os mais perto de subir para a primeira.
>
> **O que assumi:** abril contra março; conversão = compra concluída marcada no GA4.
> **Limites:** os dados dos últimos dois dias do período no Search Console ainda podem mudar.

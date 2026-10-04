---
name: "reportei-conta-analista-de-audiencia"
description: "Mostra quem é o público real das redes sociais de uma conta no Reportei (idade, gênero, país e cidade no Instagram, Facebook, YouTube, LinkedIn, TikTok e Threads, quando a rede fornecer), compara as redes entre si e liga cada dado a uma decisão de conteúdo. Use quando alguém perguntar \"quem é meu público?\", \"qual a idade de quem me segue?\", \"de onde vêm meus seguidores?\", \"meu público no LinkedIn é diferente do Instagram?\" ou \"meu público é mais jovem do que eu imagino?\". Só lê. Não cobre público de anúncios nem visitantes do site; para desempenho de posts, prefira reportei-conta-especialista-em-conteudo; para seguidores e engajamento, reportei-conta-analista-de-redes-sociais. Requer o conector MCP do Reportei."
license: "MIT"
metadata:
  version: "0.1.1"
  author: "Eduardo Campos"
  produto: "Reportei"
  requer: "conector MCP do Reportei"
---

# Analista de audiência

Você mostra quem está do outro lado das publicações, com os dados demográficos que as redes entregam ao Reportei, e diz o que isso muda no conteúdo. Leitura pura: **nenhuma chamada que escreva na conta**.

## Referências

- `references/conector-reportei.md`: ferramentas e parâmetros. **Leia primeiro.**
- `references/metricas-e-integracoes.md`: widgets de público do Instagram e como achar os das outras redes em `list_metrics`.
- `references/disciplina-de-evidencia.md`: percentuais, base e o que não foi visto. **Aplique antes de entregar.**
- `references/formato-de-resposta.md`: tom, estrutura e tamanho.

## Passo a passo

```
- [ ] 1. Resolver o projeto
- [ ] 2. Fixar o período
- [ ] 3. Ver as redes e buscar o perfil do público
- [ ] 4. Detalhar uma rede (pedida, pulada ou sumida)
- [ ] 5. Escrever
```

Uma chamada ao Reportei por vez, conferindo projeto e formato em cada resposta (`references/conector-reportei.md`).

1. **Projeto:** `list_projects` (com `search` se a pessoa citou um nome; confira `meta.last_page`). A busca é literal: se vier vazio, tente um trecho menor do nome, sem acento ou sem espaço. Um projeto: use e diga o nome. Mais de um possível, ou nenhum nome citado: mostre a lista curta e pergunte qual.
2. **Período:** datas absolutas (`AAAA-MM-DD`). Padrão: último mês fechado. Perfil de público muda devagar e costuma ser um retrato do momento: `get_audience_insights` sempre traz o retrato de hoje, seja qual for o período pedido. Para "evolução", use `get_metrics_data` dos widgets de público em dois períodos distantes (pelo menos 3 meses); se vierem iguais, diga que a rede só entrega o retrato atual e ponha isso em Limites.
3. **Redes e perfil:** comece por `list_integrations` com `projectId`. Rede pedida que não aparece: diga que não está conectada ao projeto. Mais de uma conta da mesma rede: leia conta por conta, sem somar. Se a pessoa citou uma rede só ("meu público no Instagram"), vá direto ao passo 4 para ela. Para comparar redes, `get_audience_insights` com `projectId`, `startDate`, `endDate`.
   - A resposta pode vir parcial. Leia `partial_results` e `sources_with_errors`: rede com `skipped_time_budget` não é "sem dado", foi pulada; busque essa rede pelo passo 4.
   - Compare as redes pedidas com as lidas mais as com erro. Rede que sumiu sem explicação: busque pelo passo 4 ou liste como "não lida, sem motivo informado".
4. **Uma rede a fundo:** `list_metrics` com o slug da rede para achar as métricas demográficas, e `get_metrics_data` com os objetos exatamente como `list_metrics` devolveu, cada um com `id` (o que `list_metrics` trouxer ou, se não vier, o `reference_key`), mais `start`, `end` e `integrationId`.
   - No Instagram, busque também alcance de seguidores e de não seguidores, se existir no catálogo: o perfil demográfico descreve quem segue, não quem viu.
   - Se as séries de idade por gênero vierem sem rótulo, não atribua gênero por suposição: diga que a série veio sem rótulo e mostre só a idade. Cidades e países podem vir fora de ordem: ordene você.
5. **Escrever:** para cada rede, o perfil dominante em uma linha. Depois, as diferenças entre redes e a surpresa (o que provavelmente difere do que a pessoa imagina). Feche com 1 ou 2 implicações práticas.

## Regras

- Diga a base de cada número: seguidores, público alcançado ou inscritos não são a mesma coisa. Use o que o dado informar.
- Percentual sobre a soma das faixas de idade e gênero, que pode ser menor que o total de seguidores: diga quantos ficaram fora. A lista de cidades costuma ser parcial: diga isso.
- Percentual sempre com a faixa ("38% têm de 25 a 34 anos"), nunca só "a maioria".
- Rede que devolve um rótulo só (ex.: 100% de um gênero, idade vazia) tem dado pobre: trate com cautela e diga.
- Não compare com média de mercado inventada; compare as redes da própria conta.
- Cada dado demográfico vira uma implicação (tom, horário, cidade para evento, formato), marcada como sugestão.
- Gênero e idade vêm como as plataformas classificam; não interprete além disso.

## Formato de entrega

```markdown
**Público · <Projeto> · <período>**

**<Rede>** (<base: seguidores | público alcançado>)
Idade: <faixa principal> (<%>), <segunda faixa> (<%>) · Gênero: <...> · Cidades: <top 3 com %; se houver, o agrupamento regional que muda a leitura (calculado)>

**O que muda entre as redes:** <2 ou 3 frases>
**O que isso sugere:** <1 ou 2 implicações práticas>

**O que assumi:** <período, base usada, redes buscadas uma a uma>
**Limites:** <redes não conectadas, puladas ou sem dado demográfico; seguidores fora da base; lista de cidades parcial>
```

## Não faz

- Não mostra público de anúncios (segmentação de campanha não é perfil de seguidor).
- Não mostra perfil de visitante do site (use `reportei-conta-analista-de-site` para tráfego).
- Não avalia posts (use `reportei-conta-especialista-em-conteudo`).
- Não cria estratégia completa: entrega o dado e as implicações diretas.

## Exemplo de prompt

> Quem é meu público? Acho que falo com gente de 25 a 35 anos.

## Exemplo de retorno

Exemplo ilustrativo (nomes e números fictícios):

> **Público · Cliente A · abril de 2026**
>
> **Instagram** (seguidores)
> Idade: 25 a 34 anos (35%), 35 a 44 anos (30%) · Gênero: 65% mulheres · Cidades: Cidade 1 (40%), Cidade 2 (8%), Cidade 3 (5%)
>
> **Facebook** (seguidores)
> Idade: 35 a 44 anos (35%), 45 a 54 anos (25%) · Gênero: 60% mulheres · Cidades: Cidade 1 (35%)
>
> **O que muda entre as redes:** no Instagram você acertou, 25 a 34 é a faixa maior. No Facebook, mais da metade tem 35 anos ou mais: provavelmente um cliente mais maduro, que já conhece a marca.
>
> **O que isso sugere:** no Facebook, falar com esse público mais maduro (segurança, rotina, resultado); concentrar evento presencial na Cidade 1, onde estão quatro em cada dez seguidores.
>
> **O que assumi:** abril de 2026; base = seguidores com idade e gênero informados.
> **Limites:** cerca de 1 em cada 5 seguidores do Instagram não entra na base de idade e gênero; a lista de cidades cobre só as maiores.

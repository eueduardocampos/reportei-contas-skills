# Métricas e integrações: como achar, descobrir e buscar

Como sair de "o cliente quer saber como foi o mês" até um número com fonte, usando o conector do Reportei. Catálogo completo das ferramentas em `conector-reportei.md`.

## 1. Achar as integrações de um projeto

1. `list_projects` com `search` no nome do cliente. A busca é literal: se vier vazio, tente um trecho mais curto. Se vier mais de um projeto parecido (ex.: "Cliente A" e "Cliente A Filial"), mostre os dois com id e pergunte.
2. `list_integrations` com `projectId` e `perPage` 100. **Este é sempre o primeiro passo de qualquer análise**, antes das ferramentas de resumo. Confira `meta.last_page`: se for maior que 1, busque as outras páginas.
3. Para cada integração, guarde cinco campos: `id` (número, vai para `get_metrics_data`, `create_report`, `sourceIds`), `source_id` (texto, vai para `create_goal` e para o `sourceId` de `get_report_data`), `slug` (tipo, vai para `list_metrics`), `status` e `created_at`.
4. Conte as contas por `slug`. Se houver mais de uma da mesma plataforma, a análise dessa plataforma é feita **conta por conta** com `get_metrics_data` (ver abaixo).

Cuidados:
- **Mais de uma conta da mesma plataforma no projeto** (duas contas de Meta Ads, duas de Google Ads, dois Instagrams): `compare_periods`, `get_performance_summary` e `get_campaign_summary` mostram uma conta só, sem dizer qual, e cada ferramenta pode escolher uma diferente. Podem até dizer que leram todas. Leia conta por conta com `get_metrics_data`, mostre cada uma com nome e id, e nunca some ou compare números de contas diferentes como se fossem uma. Se a pessoa pedir o total, some você as leituras por conta e diga que somou.
- **Contas com o mesmo nome são contas diferentes.** Um projeto pode ter duas contas de anúncios chamadas "Cliente A". Liste as duas, com id, e pergunte qual (ou some as duas, dizendo que somou).
- **`status: active` quer dizer que a conexão existe**, não que a coleta esteja em dia. Uma conta conectada há anos pode estar com o token vencido na plataforma de origem. O sinal de problema é dado zerado ou ausente em métrica que nunca é zero (ver `disciplina-de-evidencia.md`).
- **`created_at` da integração é quando ela foi conectada ao Reportei.** Se for depois do início do período pedido (ou do período de comparação), aquele período tem buraco: o zero ou o vazio de antes da conexão não é zero, é **sem dado**. Confira antes de comparar e escreva "sem dado antes de DD/MM/AAAA", nunca "caiu" ou "cresceu". Em métrica "não retroativa", nada existe antes dessa data.
- **Rede pedida e ausente em `list_integrations`:** diga que ela não está conectada ao projeto. Não procure em outro projeto.

### Slugs vistos

Tipos comuns, conforme o uso do conector e as descrições das ferramentas: `instagram_business`, `facebook`, `facebook_ads`, `google_adwords` (Google Ads), `google_analytics_4`, `search_console`, `google_my_business`, `linkedin`, `linkedin_ads`, `tiktok_ads`, `youtube`, `twitter`, `pinterest`, `mailchimp`, `hubspot_crm`, `shopify`, `rdstation` (RD Station Marketing), `rd_crm` (RD Station CRM), `chatgpt_ads`.

O Reportei diz conectar mais de 47 plataformas. Para um tipo que não está acima, leia o `slug` que `list_integrations` devolveu; nunca adivinhe.

## 2. Descobrir métricas com `list_metrics`

`list_metrics(integrationSlug)` devolve o **catálogo do tipo**, não dados. Cada item é um widget:

| Campo | O que é |
|---|---|
| `reference_key` | Chave única do widget, com prefixo do tipo (`ig:`, `fb_ads:`). É ela que identifica a métrica em `get_metrics_data`, `create_goal` e `run_company_analysis`. |
| `component` | `number_v1` (um número), `chart_v1` (série ou gráfico), `datatable_v1` (tabela), `container_v1` (agrupador, ex.: lista de campanhas), `datagrid_v1` (grade, ex.: stories). Meta (`create_goal`) só aceita `number_v1`. |
| `metrics` | As chaves de dado dentro do widget (ex.: `["reach"]`, `["spend"]`). |
| `dimensions` | Quebra ou filtro. Pode ser texto (`["date"]`, `["media"]`) ou filtro (`{"field": "publisher_platform", "operator": "IN", "value": ["instagram"]}`). |
| `sort`, `type`, `custom`, `chart_type` | Vêm só em alguns widgets. Se vieram, vão junto, iguais. |
| `references` | Título, descrição e **etiquetas** do dado (abaixo). Não precisa ir para `get_metrics_data`. |

### As etiquetas de `references.tags` valem ouro

| Etiqueta | Valores vistos | Como usar |
|---|---|---|
| `cost` | `organic`, `paid`, `organic + paid` | Separa orgânico de pago. Quando a pessoa pedir "sem anúncio" ou "só orgânico", use só widgets `organic` e mostre a fatia paga ao lado do total se a conta tiver anúncios; se a métrica só existe como `organic + paid` (seguidores, por exemplo), diga que a plataforma não separa. Não some orgânico com "orgânico + pago" achando que são coisas separadas. |
| `calculation` | `Passed through the network` (repassado pela plataforma), `calculated` (calculado pelo Reportei), `Estimated by the network` (estimado pela plataforma) | Diz o nível de certeza do número (ver `disciplina-de-evidencia.md`). |
| `history` | `retroactive`, `not retroactive` | "Não retroativa" só tem dado desde que a integração foi conectada; comparação com período anterior pode vir nula. |
| `value` | `total value`, `partial value` | "Parcial" pode não bater com o total da plataforma. |

Leia também a `description`: ela diz como o número é feito. Exemplos vistos no Instagram Business:
- `ig:reach` é a **soma do alcance diário**: quem viu em dois dias conta duas vezes. Não é "pessoas únicas no mês".
- `ig:new_followers_count` é a variação **líquida** (seguidores no último dia menos no dia anterior ao início). Pode ser negativa.
- `ig:media_datatable` mostra o desempenho **acumulado desde a publicação** de cada post publicado no período, não só o que aconteceu dentro do período.
- Outros widgets "total ... nos posts" (`ig:media_reach`, alcance de posts da página do Facebook) também acumulam desde a publicação: numa comparação mês contra mês, favorecem o mês anterior, cujos posts tiveram mais dias para somar.
- Várias métricas de alcance dizem "nos últimos 30 dias" no título: confira se o período pedido conversa com isso.

### Paginação e tamanho

O catálogo é grande: 129 widgets no Instagram Business, 345 no Facebook Ads, mais de 400 no TikTok Ads; GA4 e Google Ads têm cerca de 95 numa página só, com mais de 100 mil caracteres. Os widgets básicos ficam no começo; use `perPage` entre 15 e 40 e pagine até achar o que precisa (no Instagram, os de seguidores ficam na segunda metade). Guarde só os widgets que vai usar e não cole o catálogo na resposta. Algumas chaves fogem do padrão de prefixo (ex.: `rdstation_experiment_*`, sem `rdstation:`).

## 3. Métricas mais usadas por plataforma

Só estão aqui as chaves vistas no catálogo ou nas descrições das ferramentas. Para as outras plataformas, a tabela descreve o que procurar no catálogo, sem chave: rode `list_metrics` e use a `reference_key` que vier.

### Instagram Business (`instagram_business`, prefixo `ig:`)

| Pergunta | Widget |
|---|---|
| Quantos seguidores tem | `ig:followers_count` (total; não retroativa) |
| Quantos seguidores ganhou ou perdeu | `ig:new_followers_count` (líquido; não retroativa); série em `ig:new_followers_count_chart` |
| Evolução de seguidores | `ig:followers_count_chart` |
| Visualizações | `ig:views` (orgânico + pago, estimada pela rede) |
| Alcance | `ig:reach` (soma diária), `ig:reach_over_time` (série), `ig:total_reach`, `ig:organic_reach`, `ig:paid_reach`, `ig:follower_reach`, `ig:non_follower_reach` (últimos 30 dias) |
| Posts do período | `ig:media_count`, `ig:media_datatable` (tabela de posts orgânicos), `ig:reels_datatable`. É o caminho quando `get_top_content` não traz posts. A tabela não vem ordenada: ordene você. |
| Interação em posts | `ig:media_engagement`, `ig:like_count`, `ig:comments_count`, `ig:media_saved`, `ig:post_shares_count`, `ig:post_interaction_rate` (interações ÷ alcance dos posts) |
| Reels | `ig:reels_count`, `ig:reels_views`, `ig:reels_reach`, `ig:reels_engagement_rate`, `ig:reels_datatable` |
| Stories | `ig:stories_count`, `ig:stories_reach_total`, `ig:stories_views`, `ig:retention`, `ig:stories_datagrid` (não retroativas) |
| Cliques no perfil | `ig:total_clicks`, `ig:clicks_breakdown` |
| Público | `ig:followers_gender_age`, `ig:followers_city`, `ig:followers_country` (retrato, não retroativas) |

### Facebook Ads / Meta Ads (`facebook_ads`, prefixo `fb_ads:`)

| Pergunta | Widget |
|---|---|
| Quanto investiu | `fb_ads:spend`; por posicionamento: `fb_ads:spend_instagram`, `fb_ads:spend_facebook` |
| Entrega | `fb_ads:impressions`, `fb_ads:reach`, `fb_ads:frequency`, `fb_ads:cpm` |
| Cliques | `fb_ads:clicks`, `fb_ads:ctr` (todos os cliques), `fb_ads:inline_link_clicks` (cliques no link), `fb_ads:inline_link_click_ctr`, `fb_ads:cost_per_inline_link_click`, `fb_ads:cpc` |
| Leads | `fb_ads:actions_lead`, `fb_ads:actions_cost_per_lead`, `fb_ads:actions_offsite_conversion.fb_pixel_lead` (leads no site) |
| Conversas | `fb_ads:actions_onsite_conversion.messaging_conversation_started_7d` |
| Vendas | `fb_ads:actions_omni_purchase`, `fb_ads:actions_cost_per_purchase`, `fb_ads:actions_omni_initiated_checkout`, `fb_ads:actions_omni_add_to_cart` |
| Página de destino | `fb_ads:actions_landing_page_view`, `fb_ads:actions_cost_per_landing_page_view` |
| Por campanha e anúncio | `fb_ads:insights_by_campaign`, `fb_ads:ads`, `fb_ads:campaigns` (container), `fb_ads:count_campaigns`, `fb_ads:count_ads` |
| Por público e posição | `fb_ads:impressions_reach_by_age`, `fb_ads:impressions_reach_by_gender`, `fb_ads:reach_by_region`, `fb_ads:performance_by_position` |
| Todas as ações (conversões) | `fb_ads:actions_by_type`: todos os eventos com custo por ação, separando formulário, pixel e eventos personalizados. É o caminho padrão para conversões da Meta; o custo por ação fica na última coluna (a tabela vem com 3 ou 5 colunas conforme a conta). |

Atenção a duas armadilhas de nome: **`fb_ads:ctr` é CTR de todos os cliques** (inclui curtir, abrir perfil), e **`fb_ads:cost_per_inline_link_click` aparece com o título "Average CPC"**, enquanto `fb_ads:cpc` é o CPC de todos os cliques. Diga qual dos dois está usando.

Antes de usar `fb_ads:actions_lead` como manchete, veja o que cada campanha otimiza: a coluna de resultados de `fb_ads:insights_by_campaign` traz o evento de cada uma. Se as campanhas otimizam para evento personalizado ou conversa, o custo por lead da conta engana.

### Facebook (página, `facebook`, prefixo `fb:`)

Catálogo pequeno (cerca de 40 widgets, uma página). Úteis: `fb:page_follows`, `fb:net_page_follows`, `fb:page_posts_count`, `fb:page_media_views_organic`, `fb:page_media_view_paid`, `fb:page_post_organic_reach`, `fb:organic_video_views`, `fb:page_posts_comments`, `fb:page_posts_shares`. Visualizações e alcance da página podem ser majoritariamente pagos: em pergunta orgânica, use as versões `organic`.

### Google Analytics 4 (`google_analytics_4`)

| Pergunta | Widget |
|---|---|
| Visitas e pessoas | `google_analytics_4:all_sessions`, `google_analytics_4:total_users` |
| Origem do tráfego | `google_analytics_4:session_default_channel_group_datatable`, `google_analytics_4:content_sources` |
| Páginas | `google_analytics_4:top_content` (por caminho), `google_analytics_4:screen_page_views` (por título), `google_analytics_4:landing_page` |
| Conversão | `google_analytics_4:conversions_count` (eventos-chave), `google_analytics_4:session_key_event_rate`, `google_analytics_4:top_conversions`, `google_analytics_4:top_events` |

Conversão zerada nos dois períodos, com `top_conversions` sem dado, indica evento-chave não configurado, não "zero contatos"; `top_events` mostra se há eventos candidatos. `new_users` pode passar de `total_users` no resumo: prefira sessões e usuários totais. Soma das linhas de canal não bate exatamente com o total de sessões: não some linhas como se fossem o total.

### Google Ads (`google_adwords`, prefixo `gads:`)

| Pergunta | Widget |
|---|---|
| Quanto investiu | `gads:cost_micros`: **já vem na moeda da conta** (em reais numa conta em real), apesar do nome. Não divida. |
| Conversões | `gads:conversions`, `gads:conversions_value`; para saber o que está sendo contado, `gads:custom_conversion_actions` |
| Por campanha | `gads:top_campaigns` |

### Outras plataformas

| Plataforma | O que procurar no catálogo |
|---|---|
| Search Console (`search_console`) | Cliques, impressões, CTR, posição média, consultas e páginas. |
| LinkedIn (página, `linkedin`, prefixo `li:`) e LinkedIn Ads (`linkedin_ads`) | Seguidores, impressões, engajamento, posts (`li:all_posts`, que é `organic + paid`; `li:posts` é só orgânico). **A taxa de engajamento do LinkedIn inclui cliques** e não se compara com a do Instagram. Nos anúncios, investimento, cliques, leads. |
| RD Station Marketing (`rdstation`) e CRMs (`rd_crm`, `hubspot_crm`) | Leads convertidos (`rdstation:leads_converted`); negócios ganhos e valor (`rd_crm:won_deals`, `rd_crm:won_deals_value`; confira a chave exata no catálogo). Catálogo do RD Station: 42 widgets, todos parciais e não retroativos. |
| TikTok Ads, YouTube, Pinterest | Investimento e resultados nos anúncios; visualizações, inscritos e tempo de exibição no YouTube. |
| E-commerce (`shopify` e outros) | Vendas, pedidos, receita. |

### Métricas em que menor é melhor

Nelas, subir é piorar; numa meta, use `positiveBad: true`. Ao comparar períodos, classifique a queda como melhora.

- Custos de mídia: CPC (`fb_ads:cpc`, `fb_ads:cost_per_inline_link_click`), CPM (`fb_ads:cpm`), custo por lead (`fb_ads:actions_cost_per_lead`), custo por compra, custo por visualização da página de destino e custo por conversão ou por resultado (no Google Ads, calculado: custo ÷ conversões).
- Frequência alta em anúncio (`fb_ads:frequency`), quando o CTR cai junto.
- Taxa de rejeição do GA4.
- Posição média do Search Console: número menor é posição melhor (1 é o topo).

Na dúvida, leia a `description` do widget em `list_metrics`.

## 4. Qual ferramenta usar

| A pessoa quer | Use | Por quê |
|---|---|---|
| Uma ou poucas métricas específicas de **uma** conta | `get_metrics_data` | Mais preciso. Exige `list_metrics` antes. Faz comparação com `comparisonStart` + `comparisonEnd`. |
| Qualquer número de plataforma com **mais de uma conta** no projeto | `get_metrics_data`, conta por conta | As ferramentas de resumo mostram uma conta só. |
| Investimento de Meta Ads ou Google Ads | `get_metrics_data` (`fb_ads:spend`, `gads:cost_micros`) | As ferramentas de resumo não trazem. |
| "Como foi o mês" do cliente, tudo de uma vez | `get_performance_summary` | Atalho: KPIs e série diária, sem comparação, uma conta por plataforma, pode pular integrações. |
| Social contra anúncio contra site | `get_channel_breakdown` | Agrupa por categoria; poucas métricas e sem comparação. |
| Prévia da mídia paga | `get_campaign_summary` | Atalho sem investimento de Meta e Google e com uma conta por plataforma. |
| Melhores posts | `get_top_content`; se não vier post, widgets de posts com `get_metrics_data` | Pode devolver só tabelas de público. |
| Perfil do público | `get_audience_insights`; para uma rede só, `get_metrics_data` dela | Retrato atual; pode voltar parcial. |
| Mês contra mês, todas as contas | `compare_periods`, completado com `get_metrics_data` | Só as primeiras métricas de cada catálogo, uma conta por plataforma, pode voltar parcial. |
| Projeto com muitas integrações e pergunta sobre poucas redes | `get_metrics_data` direto nas redes pedidas | As ferramentas de resumo gastam o tempo nas outras integrações e pulam justamente as pedidas. |
| "O que diz este relatório" ou "analise este dashboard" | `get_report_data` | Números exatamente como estão no relatório; `sortByColumn` para o maior e o menor de verdade. |
| Tabela com colunas que nenhum widget tem | `list_table_fields` + `get_custom_table_data` | Último recurso (ver `conector-reportei.md`). |
| Ranking ou total entre **vários clientes** | `run_company_analysis` | Assíncrono; avise antes. Preset `ads_spend` para investimento. |

## 5. Usando `get_metrics_data` sem erro

1. Copie de cada widget de `list_metrics` os campos `reference_key`, `component`, `metrics` e, se existirem, `dimensions`, `sort`, `type`, `custom`, `chart_type`, com os valores como vieram. Não mande `references` nem chaves que o schema não conhece (ex.: `container_type`); `added_date` foi aceito quando enviado. Não acrescente campo vazio.
2. Inclua `id`: o schema exige. Use o `id` que `list_metrics` trouxer; quando não vier, use o `reference_key` (é aceito).
3. Datas em `AAAA-MM-DD`, no fuso do projeto (`get_project`).
4. Comparação: período de mesmo tamanho, imediatamente anterior, salvo pedido (ex.: 01/04 a 30/04 contra 02/03 a 31/03, 30 dias cada). Mês ou trimestre fechado pode ser comparado com o mês ou trimestre civil anterior inteiro, dizendo os dias de cada um. Confira antes o `created_at` de cada integração (item 1).
5. Leia a resposta: `values` é o número do período; `trend.data` é a série (um valor por dia, na ordem); `comparison.values` é o período anterior; `comparison.difference` é a **variação em %**; `comparison.absoluteDifference` é a diferença bruta; `null` em comparação quer dizer **sem dado** no período anterior, não zero.
6. **Tabelas (`datatable_v1`) não trazem comparação** e **não vêm ordenadas** pelo `sort`. Para comparar uma tabela, faça uma segunda chamada com o período anterior; para ranking, ordene você.
7. **Unidade de taxas:** confira recalculando com as bases (cliques ÷ impressões). CTR e taxas de conversão vêm ora em fração, ora em pontos percentuais, conforme a plataforma.
8. Poucas métricas por chamada, uma chamada por vez. Use as ferramentas de resumo só como atalho, com os limites acima.

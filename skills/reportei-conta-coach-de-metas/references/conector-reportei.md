# Conector MCP do Reportei: catálogo das ferramentas

Referência das ferramentas do conector oficial do Reportei (MCP) usadas pelas skills. Os nomes abaixo são os nomes das ferramentas no conector; no seu cliente eles podem aparecer com um prefixo (ex.: `mcp__<id>__list_projects`).

Só vale o que o conector expõe. Se uma informação não vem por ele, a skill diz que não tem acesso a ela, em vez de supor. O conector tem **50 ferramentas**: 34 de leitura e 16 que escrevem (criam, alteram, ativam, desativam ou apagam algo na conta).

## Vocabulário do Reportei

| Termo no conector | O que é | Sinônimos que a pessoa usa |
|---|---|---|
| **company** | A conta do Reportei (agência ou empresa). Dona de todos os projetos. | conta, empresa, agência |
| **project** | Um cliente dentro da conta. Agrupa integrações, relatórios, dashboards, metas, automações e linha do tempo. O parâmetro se chama `projectId`, mas as respostas trazem `client_id`. | projeto, cliente |
| **integration** | Uma conta de plataforma conectada a um projeto (um Instagram, uma conta de anúncios Meta, um GA4). Tem `id` (número) e `source_id` (texto, o id da conta na plataforma). | conta, rede, fonte, source, network |
| **slug** | O **tipo** de integração (`instagram_business`, `facebook_ads`). Métricas pertencem ao tipo, não à conta. | plataforma |
| **report** | Relatório **estático**: retrato dos dados no momento em que foi criado. Não atualiza. | relatório |
| **dashboard** | Painel **ao vivo**: busca os dados de novo a cada visualização. | painel, dashboard |
| **template** | Layout de widgets. `kind` `report` serve para relatório e automação; `kind` `dashboard` serve para dashboard. | modelo |
| **automation** | Envio programado de relatório (semanal, quinzenal, mensal) por email, notificação no app ou WhatsApp. | automação, relatório automático |
| **goal / tracked metric** | Meta de uma métrica de uma integração, com alvo e período recorrente. | meta, KPI |
| **timeline event** | Marco, nota ou anotação datada de um projeto, opcionalmente ligada a um relatório. | linha do tempo, marco, anotação |

Regra que evita metade dos erros: **"conta", "rede" e "fonte" são integração (`list_integrations`); "cliente" e "projeto" são projeto (`list_projects`).** E `integrationId` nunca é `projectId`.

## Fluxo padrão

1. `list_projects` → acha o `projectId` do cliente.
2. `list_integrations` com `projectId` → vê as contas conectadas, com `id`, `source_id`, `slug` e `status`.
3. `list_metrics` com o `slug` → descobre as métricas disponíveis para aquele tipo.
4. `get_metrics_data` com o `id` da integração e os objetos de métrica → números do período.

Para visões amplas, as ferramentas de análise por projeto (grupo 2) pulam os passos 3 e 4, mas com limites sérios (uma conta por plataforma, resultado parcial, métricas faltando): leia "Ferramentas de resumo" abaixo antes de confiar nelas.

## Regras de uso que valem para toda chamada

1. **Uma chamada ao Reportei por vez.** Em chamadas simultâneas, o conector já devolveu a resposta de uma ferramenta no lugar de outra e dados de um projeto na chamada de outro (ex.: `list_integrations` voltando com conteúdo de `list_templates`; `list_automations` voltando com a meta de outro projeto). Espere cada resposta antes de chamar a próxima, inclusive nas releituras depois de uma escrita.
2. **Confira cada resposta antes de usar.** O formato bate com a ferramenta chamada (lista com `data` e `meta` numa `list_*`, objeto único numa `get_*`)? O `project_id` ou `client_id` é o do projeto pedido? Se não bater, descarte e repita a chamada. Nunca conclua "projeto sem integrações" ou "relatório de outro período" a partir de uma resposta que não confere.
3. **Erro de servidor** ("server isn't responding", sem ser limite de requisições): em leitura, tente de novo uma vez. Em escrita, **liste antes de repetir**, porque a criação pode ter sido gravada.
4. **Listas paginadas:** o padrão é 100 por página em `list_projects`, `list_integrations` e `list_metrics`, e **15** nas demais (`list_reports`, `list_dashboards`, `list_templates`, `list_timeline_events`, `list_webhooks`). Peça `perPage` 100 e confira `meta.last_page`. **Lista vazia volta com `last_page` 0**: não é erro, é "nenhum item".
5. **Comece pelo inventário.** Antes de qualquer análise de projeto, `list_integrations` (`perPage` 100). É ele que diz quantas contas existem por plataforma, quais estão ativas e desde quando (`created_at`). Sem `projectId`, ele lista as integrações da conta inteira numa chamada, o que serve para varrer a carteira.

## 1. Projetos, conta e integrações (leitura)

| Ferramenta | Para que serve | Parâmetros | Devolve | Armadilhas |
|---|---|---|---|---|
| `get_company_settings` | Conferir a conta autenticada | nenhum | id, nome, logo, tipo, `total_clients` (número de projetos), especialidade | Bom primeiro passo para confirmar **em qual conta** o conector está logado. |
| `list_projects` | Achar clientes | `search` (nome, parcial), `page`, `perPage` (padrão 100), `sortBy` (`name`, `created_at`, `updated_at`), `descending` | id, nome, logo, `timezone`, `locale`, `date_format`, `decimal_separator_format` | **Paginado:** se `meta.last_page` for maior que 1, você não viu todos os projetos. Busque as outras páginas antes de contar ou dizer "todos". **A busca é literal:** um espaço, acento ou grafia diferente do nome cadastrado devolve vazio (ex.: "Cliente Acao" não acha "ClienteAção"). Se vier vazio, tente um trecho mais curto do nome antes de dizer que o projeto não existe. |
| `get_project` | Configuração de um projeto | `projectId` | id, nome, logo, fuso, idioma, formato de data e de decimal | Use o fuso do projeto para interpretar "ontem" e "este mês". |
| `list_integrations` | Contas conectadas | `projectId` (recomendado), `slug`, `name` ou `search`, `page`, `perPage` (padrão 100), `sortBy` (`created_at`, `source_name`, `updated_at`) | id, `source_id`, nome, slug, `status` (`active`/`inactive`), projeto, datas | **Paginado** (`meta.last_page`). Um projeto pode ter **várias contas com o mesmo nome** (ex.: duas contas de anúncios com o mesmo nome): são integrações diferentes, com ids diferentes; liste todas e nunca junte. `status` `active` não garante que a coleta esteja em dia; ver `metricas-e-integracoes.md`. `created_at` é a data em que a conta foi conectada: antes dela, não há dado. |
| `get_integration` | Detalhe de uma conta | `integrationId` | id, nome, slug, status, projeto, datas | O `slug` daqui vai para `list_metrics`. |

## 2. Métricas e análises (leitura)

| Ferramenta | Para que serve | Parâmetros obrigatórios | Devolve | Armadilhas |
|---|---|---|---|---|
| `list_metrics` | Catálogo de métricas de um **tipo** de integração | `integrationSlug`; úteis: `page`, `perPage` (padrão 100) | Para cada widget: `reference_key` (ex.: `ig:reach`), `component`, `metrics`, e quando houver `dimensions`, `sort`, `type`, `custom`, `chart_type`, mais `references` (título, descrição e etiquetas de origem do dado) | Não busca dado. **Paginado e grande:** Instagram Business tem 129 widgets, Facebook Ads 345, TikTok Ads mais de 400; GA4 e Google Ads têm cerca de 95 numa página só, que passa de 100 mil caracteres. Os widgets básicos (investimento, cliques, impressões) ficam no começo do catálogo: `perPage` entre 15 e 40 deixa cada página legível. Pagine até achar o widget e guarde só o que vai usar. Ver `metricas-e-integracoes.md`. |
| `get_metrics_data` | Números exatos de métricas escolhidas, de **uma** integração | `integrationId`, `start`, `end`, `metrics` (lista de objetos); úteis: `comparisonStart` + `comparisonEnd` (juntos) | Por `reference_key`: `values`; em gráfico diário, `trend.data`; com comparação, `comparison.values`, `comparison.difference` (variação **em %**) e `comparison.absoluteDifference` | Copie de `list_metrics` os campos do widget (`reference_key`, `component`, `metrics` e, se vierem, `dimensions`, `sort`, `type`, `custom`, `chart_type`), sem `references` nem chaves fora do schema (ex.: `container_type`). O schema exige `id` em cada objeto: use o `id` que `list_metrics` trouxer e, se ele não vier, o `reference_key` como `id` (é aceito). **Tabelas (`datatable_v1`) não trazem comparação** mesmo pedindo, e **não vêm ordenadas** pelo `sort` do widget: ordene você. Tabela sem dado volta como `warning` ("There is no data"), não como lista vazia. É a ferramenta mais confiável para número de uma conta. |
| `get_performance_summary` | Visão geral das integrações do projeto | `projectId`, `startDate`, `endDate` | KPIs principais por plataforma, em lista, com série diária | Sem comparação. **Mostra uma conta por plataforma** e pode pular integrações por tempo. Ver "Ferramentas de resumo". |
| `get_channel_breakdown` | Comparar **categorias** de canal | `projectId`, `startDate`, `endDate` | KPIs agrupados em `social_media`, `ads`, `web_analytics`, `crm`, `ecommerce`, `email_marketing` | Sem comparação de períodos; poucas métricas por plataforma; uma conta por plataforma. Traz `comparison.values: null` mesmo sem pedido de comparação: é ruído, não "sem dado anterior". |
| `get_campaign_summary` | Prévia da mídia paga | `projectId`, `startDate`, `endDate` | Métricas das plataformas de anúncio | **Não traz investimento de Meta Ads nem custo de Google Ads** (só alcance, impressões e CPC na Meta; cliques, conversões e CTR no Google); outras redes de anúncio trazem investimento. **Mostra uma conta por plataforma**, sem dizer qual, e não soma. Sem comparação: para dois períodos, chame duas vezes. Não serve para "quanto investiu": use `get_metrics_data` conta por conta. |
| `get_top_content` | Melhores posts | `projectId`, `startDate`, `endDate`; útil: `limit` (padrão 10 por plataforma) | Tabelas de conteúdo das redes sociais | Só redes sociais. **Pode devolver só tabelas de público (cidade, país) e nenhum post**, sem sinalizar falha (`partial_results: false`, sem erros). Se não vier tabela de posts, busque pelos widgets de posts de cada rede (`ig:media_datatable`, `ig:reels_datatable`, `li:all_posts` e equivalentes) com `get_metrics_data`. Só diga "não houve posts" depois disso. |
| `get_audience_insights` | Perfil do público | `projectId`, `startDate`, `endDate` | Idade, gênero, país, cidade, das redes que fornecem (Instagram, Facebook, YouTube, LinkedIn, TikTok; Threads também, observado no uso, embora não esteja na descrição da ferramenta) | Dado demográfico é **retrato atual**, não histórico do período. **Pode voltar parcial** (ver "Ferramentas de resumo"), e uma rede pode sumir da resposta sem aparecer nos erros: compare `integrations_requested` com as lidas mais as com erro. Quando a pessoa cita uma rede só, vá direto em `get_metrics_data` dela. |
| `compare_periods` | Variação entre dois períodos | `projectId`, `startDate`, `endDate`, `comparisonStartDate`, `comparisonEndDate` | `current_value`, `previous_value`, diferença absoluta e `percentage_change` por métrica | **Traz só as primeiras métricas `number_v1` do catálogo de cada plataforma:** sem investimento de Meta Ads e sem custo de Google Ads. **Uma conta por plataforma**, sem id. **Pode voltar parcial.** `previous_value: 0` aparece para conta que não existia no período anterior (confira `created_at`). Ver "Ferramentas de resumo". |
| `get_report_data` | Os **números** de um relatório ou dashboard já existente | `reportId` (serve para id de dashboard também); úteis: `sourceId` (restringe a uma integração do relatório), `sortByColumn` + `descending` (ordena tabelas antes de amostrar) | `sources[]` com plataforma, nome da conta, `data_status` e widgets: KPIs com comparação, séries, linhas de tabela | Tabelas grandes vêm **amostradas** (`rows_truncated`). Para achar o maior ou menor de verdade, use `sortByColumn`. `sources[]` vem sempre completo. O resto do formato da resposta está truncado na descrição: trate os demais campos conforme vierem. |
| `get_custom_table_data` | Tabela com combinação própria de métricas e dimensões | `integrationId`, `start`, `end`, `referenceKey` (de um preset), `metrics`; úteis: `dimensions`, `sort`, `limit`, comparação | `spec_used`, `rows`, `rows_total`, `rows_truncated`, ou `{error, type, message}` | Não grava nada. Depende de `list_table_fields`. Prefira **uma** dimensão; duas só se forem hierárquicas (campanha + conjunto). Erros possíveis: `not_found`, `not_editable`, `invalid_reference_key`, `invalid_metrics`, `invalid_dimensions`, `too_many_metrics`, `too_many_dimensions`. |
| `list_table_fields` | Catálogo de colunas combináveis de um tipo de integração | `integrationSlug` | `editable`, `datatable_presets`, `available_metrics`, `available_dimensions` | **Pode travar.** Use só quando nenhum preset de `list_metrics` tem as colunas pedidas, e com uma integração por vez. |

### Ferramentas de resumo: o que elas escondem

`get_performance_summary`, `compare_periods`, `get_campaign_summary`, `get_channel_breakdown` e `get_audience_insights` leem o projeto inteiro de uma vez. São atalhos, não fonte final. Três problemas já observados:

**1. Uma conta por plataforma, sem dizer qual.** Quando o projeto tem duas ou mais contas da mesma plataforma (duas contas de Meta Ads, duas de Google Ads), essas ferramentas mostram **uma só**, com nome genérico ("Meta Ads"), e cada ferramenta pode escolher **uma conta diferente** para o mesmo período. O campo `integrations_fetched` pode dizer que leu todas mesmo assim. Regra:
- Comece sempre por `list_integrations` (`perPage` 100) e conte as contas por plataforma.
- Com mais de uma conta da mesma plataforma, leia **conta por conta** com `get_metrics_data`.
- Nunca some, compare ou ponha na mesma linha "anterior → atual" números de contas diferentes como se fossem uma, nem números da mesma plataforma vindos de ferramentas diferentes.

**2. Resultado parcial.** `compare_periods`, `get_performance_summary` e `get_audience_insights` têm um orçamento de tempo interno. A resposta traz `partial_results`, `sources_with_errors` (com `error_type: "skipped_time_budget"` e o `integration_id`), `integrations_requested`, `integrations_fetched` e `integrations_capped` (`true` quer dizer que nem todas foram tentadas). Regra:
- Leia esses campos em toda resposta.
- Se vier parcial, repita **uma vez** (às vezes a segunda chamada lê mais; às vezes vem igual).
- O que continuar pulado, busque direto com `get_metrics_data` (com comparação, se for o caso).
- O que ficou sem leitura vai para "Limites" como **não consultado**, com o nome da conta. Integração pulada não é "sem dado".

**3. Métricas faltando.** `compare_periods` e `get_campaign_summary` não trazem investimento de Meta Ads nem custo de Google Ads. Para investimento, busque conta por conta com `get_metrics_data` (`fb_ads:spend`, `gads:cost_micros` e o widget de investimento das outras redes).

## 3. Relatórios, dashboards e templates

| Ferramenta | Lê ou escreve | Para que serve | Parâmetros | Devolve / armadilhas |
|---|---|---|---|---|
| `list_reports` | Lê | Relatórios gerados | `projectId`, `search` (título e subtítulo), `createdAt`/`updatedAt` (a partir de), `page`, `perPage` (padrão 15), `sortBy`, `descending` | id, título, subtítulo, `start_date`, `end_date`, período de comparação, `template_id`, `client_id`, `created_at`, `internal_url`, `external_url`. **Paginado** com `meta.total` e `meta.last_page`. Não filtra por período do relatório: `createdAt` é "criado em ou depois de". `search` procura texto no título, que varia ("Set", "Setembro", "Sep"): para achar o relatório de um período, compare `start_date` e `end_date`. |
| `get_report` | Lê | Metadados e links de um relatório | `reportId` | Mesmos campos. Não traz números (para eles, `get_report_data`) **nem as integrações incluídas** (`get_report_data` traz `sources[]`, se precisar conferir). |
| `create_report` | **Escreve** | Relatório estático | obrigatórios: `title`, `subtitle`, `start`, `end`, `templateId`, `integrationIds` (lista, mesmo com um só: `[123]`), `projectId`; úteis: `comparisonStart` + `comparisonEnd` (juntos) | id, título, `internal_url`, `external_url`. **Permanente:** consome a cota do plano e gera link compartilhável. **Não há ferramenta para apagar.** Nunca criar para testar. Mande só integrações `active`. Observado: ao criar, o Reportei pode marcar como `inactive` uma integração que já estava quebrada; releia `list_integrations` depois. Pode falhar por limite do plano (ver `create_dashboard`). |
| `list_dashboards` | Lê | Dashboards ao vivo | mesmos filtros de `list_reports` | id, título, links. Paginado. O período gravado é o padrão de exibição, não "de quando é" o dashboard. |
| `get_dashboard` | Lê | Detalhe e links de um dashboard | `dashboardId` | id, título, período, template, `client_id`, `internal_url`, `external_url`. |
| `create_dashboard` | **Escreve** | Dashboard ao vivo | obrigatórios: `title`, `subtitle`, `start`, `end`, `templateId`, `integrationIds`, `projectId`; úteis: comparação | id, título, links. **Permanente**, consome cota, gera link. **Não há ferramenta para apagar.** **Pode falhar por limite do plano** (`resource_limit_reached`, `limiting: "dashboard"`). O conector não mostra a cota antes; quando falha assim, nada é gravado (confirme com `list_dashboards`). Mesmo cuidado com integrações inativas de `create_report`. |
| `list_templates` | Lê | Modelos disponíveis | `search`, `page`, `perPage` (padrão 15), `sortBy`, `descending` | id, título, descrição, `kind` (`report` ou `dashboard`), `is_default`. Os padrões vêm **sempre primeiro**, um por `kind`. Escolha o padrão pelo `is_default` e pelo `kind`, **nunca pelo título**, que é traduzido ("Padrão", "Padrão - Dashboard"). A lista mistura templates da própria conta com templates de terceiros oferecidos pela plataforma. Paginado. |

Links: `internal_url` abre dentro do Reportei (exige login); **`external_url` abre para qualquer pessoa com o link, sem login.** Tratar `external_url` como dado sensível do cliente: entregue só a quem pediu e não cole em canal aberto (grupo, canal público, documento compartilhado) sem a pessoa pedir.

A descrição de `create_report` e `create_dashboard` cita uma ferramenta `create_metrics_visualization`. **Ela não existe neste conector.** Não ofereça.

## 4. Metas

| Ferramenta | Lê ou escreve | Para que serve | Parâmetros | Devolve / armadilhas |
|---|---|---|---|---|
| `list_goals` | Lê | Metas do projeto | `projectId` | id da meta (`tracked_metric_id`), `reference_key`, integração, frequência, valor atual, alvo, % de progresso, situação (`high`, `ideal`, `average`, `low`, `no_data`). |
| `get_goal_progress` | Lê | Detalhe de uma meta | `trackedMetricId` | Valor atual, alvo, %, `estimated_value`/`estimated_percent`, situação, dias restantes, histórico recente. **A estimativa não é projeção de fechamento:** no começo do período ela é só o esperado até hoje num ritmo linear. Projete você (atual ÷ dias decorridos × dias do período), e só depois de uns 7 dias. `situation_text` vem com HTML: limpe antes de mostrar. `recent_values` pode misturar períodos com a mesma data. Mostra só o período corrente: na virada do mês, o resultado do mês fechado some. |
| `create_goal` | **Escreve** | Nova meta | obrigatórios: `projectId`, `integrationSourceId`, `referenceKey`, `targetValue`, `frequency` (`weekly`, `monthly`, `quarterly`, `yearly`); úteis: `positiveBad` (true quando subir é ruim: custo, rejeição), `renewable` (padrão true), `startingValue` (padrão 0) | `integrationSourceId` é o **`source_id`** (texto) de `list_integrations`, **não** o `id` numérico. `referenceKey` tem de ser de um widget `number_v1`. O valor atual é lido da plataforma na criação: nunca informe. **Meta não tem campo de nome nem descrição:** é identificada por projeto, métrica e conta; para registrar contexto (motivo do alvo, demanda), crie um marco na linha do tempo. Em métrica de total acumulado (seguidores), `startingValue` é ignorado e **o progresso parte do valor atual** (ex.: de 1.000 para 1.050, não de 0). Para total acumulado ou meta de um mês só, use `renewable: false`: renovar repete o mesmo alvo absoluto. A meta começa no dia da criação. Recém-criada, pode aparecer `no_data` ou "sem dado" no início do período: é normal. **Não há ferramenta para apagar meta.** |
| `update_goal` | **Escreve** | Mudar alvo ou alertas | `trackedMetricId`; úteis: `targetValue`, `startingValue`, `renewable`, alertas `targetReachedAlert`, `targetNotReachedAlert`, `aboveAverageAlert`, `belowAverageAlert` | Mudar o alvo **cria um novo período de meta** a partir do período atual. Não é uma simples troca de número. |

## 5. Linha do tempo

| Ferramenta | Lê ou escreve | Para que serve | Parâmetros | Devolve / armadilhas |
|---|---|---|---|---|
| `list_timeline_events` | Lê | Marcos e anotações | `projectId`, `reportId`, `date` (data exata), `search` (título e conteúdo), `page`, `perPage` (padrão 15), `sortBy`, `descending` | id, título, `content` (HTML), projeto, relatório ligado, data, `created_at`. Paginado (padrão 15). **`date` filtra só um dia exato:** não há filtro de período. Para um período, ordene por data decrescente com `perPage` 100, pagine e pare quando passar do início do intervalo; a ordem nem sempre é estrita, então confira as datas da página inteira. A data do marco pode ser bem diferente de `created_at`. Alguns títulos antigos trazem entidades HTML (`&amp;quot;`): converta ao mostrar. |
| `get_timeline_event` | Lê | Um marco completo | `timelineEventId` | Mesmos campos. Para um id apagado, devolve erro `not_found`: é a confirmação de que o delete funcionou. |
| `create_timeline_event` | **Escreve** | Registrar marco | obrigatórios: `title`, `content` (HTML, nunca vazio), `projectId`; úteis: `date` (padrão hoje), `reportId` | O conteúdo é renderizado como HTML: use `<b>`, `<ul>`/`<ol>`/`<li>`, `<br>` e seções (texto puro também é aceito). Título vai como texto puro, sem entidades HTML. Dispara o evento de webhook `timeline_milestone_added`, se houver assinatura. |
| `update_timeline_event` | **Escreve** | Corrigir marco | `timelineEventId`; úteis: `title`, `content`, `date`, `projectId` (move de projeto), `reportId` | Só muda o que for enviado. Nunca mande `content` vazio. Mover de projeto muda quem vê. |
| `delete_timeline_event` | **Escreve** | Apagar marco | `timelineEventId` | **Definitivo**, sem desfazer. Confirmar antes. |

## 6. Automações (relatórios programados)

| Ferramenta | Lê ou escreve | Para que serve | Parâmetros | Devolve / armadilhas |
|---|---|---|---|---|
| `list_automations` | Lê | Automações do projeto | `projectId` | id, título, status (ativa ou não), frequência, canais, horário, próxima e última execução. **"Próximo envio" (`next_run`) aparece mesmo com a automação desligada**: só cite como envio marcado se ela estiver ligada. `next_run` pode divergir do de `get_automation` para a mesma automação. |
| `get_automation` | Lê | Configuração completa | `automationId` | Horário, canais (`notification_channels`), destinatários, `whatsapp_url`, `whatsapp_type`, última execução, integrações, template, período e comparação. **Contém emails e URL:** dado sensível. `template_name` pode vir `null` com o template preenchido. É a leitura que vale para saber se está ligada. |
| `create_automation` | **Escreve** | Nova automação | obrigatórios: `projectId`, `templateId` (de `kind` `report`), `title`, `frequency` (`weekly`, `biweekly`, `monthly`), `scheduleHour` (ex.: `08:00`), `sourceIds` (ids de integração); úteis: `notificationChannels` (`email`, `in-app`, `whatsapp`, combináveis; padrão `["email"]`), `recipients` (obrigatório com email), `whatsappUrl` (obrigatório com WhatsApp), `whatsappType` (`text` ou `json`), `frequencyWeekday` (`MO`...`SU`, ou `DAY`), `frequencyOnThe` (1 a 4 ou dia 1 a 28; -1 é o último), `comparisonPeriod` (1 ou 2), `emailSubject`, `emailReplyTo`, `alertEmail` (um só), `subtitle` | **A resposta diz "disabled", mas não confie.** Já foi observado a criação responder `status: disabled` e a releitura logo depois mostrar `enabled`, com envio agendado. Depois de criar, **sempre** releia com `get_automation`; se vier ligada, desligue na hora com `toggle_automation` (`enabled: false`) e releia (ver `seguranca-de-escrita.md`). `sourceIds` pode ser gravado em parte, sem erro: mande só integrações ativas e compare quantas foram gravadas. Sem `emailSubject`, o assunto padrão sai em inglês ("<título> - Report"): proponha um assunto em português. Se `alertEmail` faltar, o conector usa o primeiro destinatário. A descrição completa dos parâmetros opcionais está truncada no schema: o que não está listado aqui, use conforme a descrição da ferramenta. |
| `update_automation` | **Escreve** | Mudar automação | `automationId`; úteis: `title`, `subtitle`, `scheduleHour`, `notificationChannels`, `recipients`, `alertEmail`, `whatsappUrl`, `whatsappType`, `sourceIds`, `comparisonPeriod` | Só muda o que for enviado, e não muda o estado ligado ou desligado. `recipients` **substitui** a lista inteira: para acrescentar uma pessoa, leia a lista com `get_automation` e envie a lista completa. "Trocar o email" é ambíguo: pergunte se é o de alerta (`alertEmail`, só um), a lista de destinatários, ou os dois. Não muda frequência nem template (não há parâmetro para isso). |
| `toggle_automation` | **Escreve** | Ativar ou desativar | `automationId`, `enabled` | Idempotente. Ativar faz relatórios **saírem para fora** no próximo horário. Desativar é a forma de "desfazer" uma automação: **não há ferramenta para apagar automação.** |

## 7. Webhooks

| Ferramenta | Lê ou escreve | Para que serve | Parâmetros | Devolve / armadilhas |
|---|---|---|---|---|
| `list_webhooks` | Lê | Assinaturas existentes | `projectId`, `eventType`, `status`, `source`, `search` (url e evento), `page`, `perPage` (padrão 15), `sortBy`, `descending` | id, url, `event_type`, `project_id`, status, `source`. Webhook **sem `project_id` vale para a conta inteira** e recebe eventos de todos os projetos. Status vem como `1`/`0` aqui e `true`/`false` na criação: escreva "ativo" ou "inativo". `search` casa com parte da URL. |
| `create_webhook` | **Escreve** | Mandar avisos a uma URL externa | obrigatórios: `url`, `events` (lista); útil: `projectId` | Cria **uma assinatura por evento** e devolve `created`, `created_count` e `errors` (pode criar só parte): leia `errors` antes de dizer "criado". **Webhook não tem nome nem descrição:** é identificado por URL, evento e projeto. O conector **não mostra se o aviso chegou** (sem histórico de entregas nem falhas): para isso, confira no sistema de destino. Eventos: `report_viewed`, `report_created`, `dashboard_created`, `automation_executed`, `control_goal_met`, `control_goal_not_met`, `timeline_milestone_added`. **Sem `projectId`, vira webhook da conta inteira**: numa agência, isso pode mandar dado de um cliente ao sistema de outro. Quem só tem acesso a alguns projetos precisa passar `projectId`. |
| `update_webhook` | **Escreve** | Mudar URL, evento ou escopo | `webhookId`; úteis: `url`, `eventType`, `projectId`, `clearProjectScope` (transforma em webhook da conta inteira) | Webhook da conta inteira só pode ser alterado por quem acessa todos os projetos. |
| `delete_webhook` | **Escreve** | Remover assinatura | `webhookId` | **Definitivo.** Mesma restrição de escopo. Confirmar antes. |

## 8. Ajuda

| Ferramenta | Para que serve | Parâmetros | Devolve |
|---|---|---|---|
| `search_help_center` | Dúvida de "como faço no Reportei" | `query` | Até 5 artigos (slug, título, resumo). Se vier vazio, amplie o termo e tente **uma** vez mais. |
| `get_help_article` | Ler um artigo | `slug` (só de `search_help_center`, nunca inventado) | Conteúdo em Markdown. Resuma para a pessoa; não cole o texto inteiro. |

Problema de cobrança, acesso ou erro da plataforma não se resolve pela central de ajuda: oriente a pessoa a falar com o suporte do Reportei.

## 9. Análise da empresa e recomendações

| Ferramenta | Lê ou escreve | Para que serve | Parâmetros | Armadilhas |
|---|---|---|---|---|
| `run_company_analysis` | Lê, mas **dispara trabalho em segundo plano** | Ranking, total, quebra ou comparação de métricas entre **vários projetos** de uma vez | obrigatórios: `aggregation` (`ranking`, `total`, `breakdown`, `comparison`), `startDate`, `endDate`; úteis: `preset` (ex.: `ads_spend`, investimento somado de todas as redes de anúncio), `metricKeys` (quando nenhum preset serve; ex. de chave na descrição: `fb_ads:spend`, `gads:cost_micros`), `filters` (`project_ids`, `integration_types`, `max_projects`), `groupBy` (`project` ou `source_type`), `sort`, `limit` | Responde na hora só `{status: "queued"}`; a resposta chega depois, e pode levar minutos. Segundo a descrição, o chat fica travado enquanto roda. Não faz série temporal nem métrica calculada (ROAS, CTR, taxa de conversão): peça as métricas base e calcule. Prefira `preset` a `metricKeys`. Use com parcimônia e avise a pessoa antes. |
| `get_opportunity_score` | Lê | Nota de oportunidade de otimização de Meta Ads de um projeto | `projectId` | É **a nota do próprio Reportei**, calculada com os dados que ele coletou; não é a nota do Gerenciador de Anúncios da Meta, e as duas não precisam bater. Diga isso ao citar. |
| `get_recommendations` | Lê | Recomendações de Meta Ads por trás da nota | `projectId`; útil: `includeObjects` (padrão true, traz campanhas e anúncios afetados) | Também do Reportei, não da Meta. **Não aplica nada:** o conector não tem ação para aplicar recomendação. |

## 10. Tabelas personalizadas

`list_table_fields` e `get_custom_table_data` (detalhadas no grupo 2) montam uma tabela com colunas escolhidas sem gravar nada. Fluxo: `list_table_fields(slug)` → escolher um `reference_key` de `datatable_presets` → `get_custom_table_data` com métricas e dimensões que existem em `available_metrics` e `available_dimensions`. Os limites de métricas, dimensões e linhas são configurados no servidor e não aparecem no schema; se vier `too_many_*`, reduza. Lembre que `list_table_fields` pode travar: só use quando a pergunta exige.

## 11. Cartões de análise em relatório

Um cartão de análise é um texto fixo colocado no topo do bloco de uma integração, dentro de um relatório ou dashboard. Ele não se atualiza com os dados e aparece para quem abre o `external_url`, sem login.

| Ferramenta | Lê ou escreve | Para que serve | Parâmetros | Armadilhas |
|---|---|---|---|---|
| `add_report_analysis` | **Escreve** | Pôr uma análise escrita dentro de um relatório ou dashboard | obrigatórios: `reportId` (serve para dashboard também), `sourceId` (o `sources[].source_id` de `get_report_data`); úteis: `content` (fragmento HTML com estilo só em `style=""`, sem `<script>` nem `<style>`) ou `useArtifact: true` | **Só quando a pessoa pedir que a análise vá para o relatório**, nunca por iniciativa própria nem no lugar de responder na conversa. Escreva o período analisado dentro do texto: num dashboard, os números em volta mudam e o cartão não. O cliente lê o cartão pelo link sem login: nada de bastidor da agência. Devolve o `widgetId` do cartão. |
| `get_report_analysis` | Lê | Ler o HTML exato de um cartão | `reportId`; útil: `widgetId` (omita se o relatório tiver um cartão só) | É a única forma de saber o que está no cartão. Leia sempre antes de alterar. |
| `update_report_analysis` | **Escreve** | Trocar o texto de um cartão | `reportId`; úteis: `widgetId`, `replacements` (lista de `{find, replace}`), `content`, `useArtifact` | Prefira `replacements`, depois de `get_report_analysis`, para mudar só o trecho pedido. Sem `widgetId` e com mais de um cartão, volta a lista de candidatos. |
| `remove_report_analysis` | **Escreve** | Apagar um cartão de análise | `reportId`; útil: `widgetId` | **Definitivo.** Só apaga cartões postos pelo chat; os widgets de métrica do relatório não são afetados. Sem `widgetId` e com mais de um cartão, volta a lista de candidatos. |

## Comportamentos observados

Já observado no uso do conector, não documentado pelo Reportei:

- **Respostas trocadas em chamadas simultâneas.** Ver "Regras de uso": uma chamada por vez e conferência de projeto e formato em cada resposta.
- **`list_metrics` pode vir sem `id`**, embora a descrição oficial diga que devolve e `get_metrics_data` exija `id` em cada objeto. Quando não vier, usar o `reference_key` como `id` é aceito.
- **`get_metrics_data` não recusou um objeto com a chave de `metrics` diferente da do catálogo** (devolveu valor mesmo assim). Não conte com isso: se aceitar sem reclamar, pode devolver outra coisa. Copie os campos do widget como vieram.
- **`comparison.difference` é a variação em %** (ex.: 25,0 quer dizer +25%), e `absoluteDifference` é a diferença bruta. Com base anterior muito pequena, a % explode e não serve como manchete; mostre o valor absoluto junto.
- **`null` na comparação nem sempre é "antes da conexão".** Métrica não retroativa volta com `comparison.values: null` quando não havia coleta no período anterior, mas algumas voltam `null` mesmo com a conta conectada há meses. Em qualquer caso, não é zero.
- **`compare_periods` usa outro formato:** `previous_value: 0` (não `null`) para conta que não existia no período anterior, e `percentage_change: null` com base zero. Cruze com `created_at`.
- **Gráficos diários trazem dias com 0** dentro de séries que em outros dias têm milhares. Antes de ler o 0 como queda, confira se a integração estava coletando (ver `disciplina-de-evidencia.md`).
- **Números vêm ora como texto (`"1500"`), ora como número**, conforme a fonte. Converta antes de somar ou comparar.
- **Unidade de taxa varia por plataforma e por widget:** um CTR pode vir como fração (0,0250 = 2,5%) e outro em pontos percentuais (2,5 = 2,5%). Confira recalculando com as bases (cliques ÷ impressões).
- **Custo por resultado igual ao investimento total com taxa de conversão 0** quer dizer zero conversões (o cálculo divide por 1), não um custo real.
- **`gads:cost_micros` já vem na moeda da conta**, não em milionésimos: não divida por 1.000.000.
- **`create_automation` responde "disabled" e pode gravar ligada** (ver grupo 6).
- **Criar relatório ou dashboard pode mudar o status de integrações quebradas** para `inactive` no mesmo instante. Releia `list_integrations` depois.

## Lê ou escreve, e dá para desfazer pelo conector

| Ferramenta | Lê ou escreve | Dá para desfazer pelo conector? |
|---|---|---|
| Todas as `list_*` e `get_*`, `compare_periods`, `search_help_center` | Lê | Não se aplica |
| `get_custom_table_data` | Lê (consulta montada na hora, não grava) | Não se aplica |
| `run_company_analysis` | Lê, com trabalho em segundo plano | Não se aplica; não dá para cancelar pelo conector |
| `create_report` | Escreve | **Não.** Não há delete; o relatório e o link ficam, e a cota é consumida. |
| `create_dashboard` | Escreve | **Não.** Não há delete; o dashboard e o link ficam, e a cota é consumida. |
| `create_goal` | Escreve | **Não.** Não há delete de meta. |
| `update_goal` | Escreve | Só em parte: dá para mudar de novo, mas a troca de alvo já abriu um novo período. |
| `create_automation` | Escreve (diz que nasce desativada, mas pode gravar ligada: releia) | Em parte: não há delete; dá para deixar desativada com `toggle_automation`. |
| `update_automation` | Escreve | Em parte: dá para voltar os valores antigos **se você os leu antes** com `get_automation`. |
| `toggle_automation` | Escreve | Sim, com outro `toggle_automation`. Mas um relatório **já enviado** não volta. |
| `create_timeline_event` | Escreve | Sim, com `delete_timeline_event` (o webhook que já disparou não volta). |
| `update_timeline_event` | Escreve | Em parte: dá para reescrever **se você leu o conteúdo antes**. |
| `delete_timeline_event` | Escreve | **Não.** Definitivo. |
| `create_webhook` | Escreve | Sim, com `delete_webhook` (o que já foi enviado à URL não volta). |
| `update_webhook` | Escreve | Em parte: dá para voltar **se você leu antes** com `list_webhooks`. |
| `delete_webhook` | Escreve | **Não.** Definitivo; dá só para criar outro igual. |
| `add_report_analysis` | Escreve | Sim, com `remove_report_analysis` (quem abriu o link antes já viu). |
| `update_report_analysis` | Escreve | Em parte: dá para voltar o texto **se você leu antes** com `get_report_analysis`. |
| `remove_report_analysis` | Escreve | **Não.** Definitivo. |

Toda escrita segue `seguranca-de-escrita.md`.

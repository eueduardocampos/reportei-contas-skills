# Disciplina de evidência

Regras para toda skill que lê dados do Reportei e tira conclusões deles. Elas existem porque o erro mais comum em análise de marketing é o indício escrito como fato: um zero lido como queda, uma % sobre base minúscula vendida como crescimento, uma recomendação de cortar verba sem olhar o que estava medido.

## 1. Todo número tem fonte

Cada número diz de onde veio. Uma vez por tabela ou seção, ou entre parênteses:

- **Ferramenta:** `get_metrics_data`, `get_performance_summary`, `get_report_data`...
- **Período:** DD/MM/AAAA a DD/MM/AAAA (e o de comparação, se houver).
- **Projeto:** nome e, em material interno, id.
- **Integração:** plataforma e nome da conta (e o id, se houver duas contas de mesmo nome).
- **Widget**, quando for um número de `get_metrics_data`: o `reference_key` ou o título dele.

Antes de usar uma resposta, confira se ela é do projeto e da ferramenta pedidos (`project_id` ou `client_id`, formato). Uma resposta que não confere é descartada e repetida, nunca usada (ver `conector-reportei.md`).

Exemplo: "Alcance de 12.000 (Instagram Business do Cliente A, `ig:reach`, 01/04/2026 a 30/04/2026, `get_metrics_data`)".

Quando o número vem de um relatório existente (`get_report_data`), diga qual relatório e que os números são **os do relatório**: num relatório estático, eles são o retrato do dia em que ele foi gerado.

## 2. Três níveis de certeza, sempre escritos

| Nível | Quando | Como escrever |
|---|---|---|
| **Medido** | Veio direto de uma ferramenta, para o período e a conta citados | Afirmação direta, com fonte |
| **Calculado** | Conta feita por você com números medidos (soma de contas, CPL = investimento ÷ leads, variação) | "calculado", com a regra: "CPL calculado = R$ 3.200,00 ÷ 160 leads" |
| **Deduzido** | Hipótese a partir dos dados (sazonalidade, efeito de criativo, pixel quebrado) | "provável", "possível", "indica", nunca afirmação |

Além disso, o próprio catálogo diz como a plataforma produziu o número (`references.tags.calculation` em `list_metrics`):
- `Passed through the network`: repassado pela plataforma.
- `calculated`: calculado pelo Reportei (ex.: `ig:reach` soma o alcance de cada dia e conta duas vezes quem viu em dois dias).
- `Estimated by the network`: **estimado** pela plataforma. Diga "estimado".

Exemplos:
- "Alcance somado de 30 dias" e não "30 mil pessoas alcançadas", quando a métrica é soma diária.
- "Nota de oportunidade do Reportei", nunca "nota da Meta" (`get_opportunity_score`).
- "Provável efeito do feriado" e não "caiu por causa do feriado".

## 3. Períodos explícitos e comparáveis

- Sempre com data de início e fim, nunca "mês passado" sozinho. Se a pessoa disse "mês passado", traduza: "01/03/2026 a 31/03/2026".
- **Mês sem ano** ("abril"): é o mais recente já começado, no fuso do projeto. Se vier vazio, diga isso primeiro; se mostrar outro ano como referência, deixe claro que é outro ano.
- **Mesmo tamanho:** 30 dias contra 30 dias. Abril (30 dias) contra março (31) é aceitável se você disser; um período de 7 dias contra um de 30, não.
- **Mesmos dias da semana** quando o período é curto: segunda a domingo contra segunda a domingo.
- **Período em andamento:** "este mês" até hoje não se compara com o mês anterior inteiro. Compare com o mesmo número de dias do mês anterior, ou diga que o período está incompleto.
- **Fuso:** use o do projeto (`get_project`).
- **Ano contra ano** quando o negócio é sazonal (captação de clientes, datas de varejo). Diga que escolheu e por quê.
- **Métrica de "últimos 30 dias":** alguns widgets dizem isso no título. Se o período pedido for outro, avise.
- **Métrica não retroativa** (`history: not retroactive`): só existe desde que a integração foi conectada. Comparação com antes disso volta nula.

## 4. Zero não é igual a sem dado

Antes de escrever "caiu a zero", "não teve resultado" ou "parou de funcionar", confira:

1. **A integração existia no período?** `created_at` em `list_integrations`. Se a conta foi conectada depois do início do período (ou do período de comparação), o zero de antes da conexão **não é zero**: é sem dado. `compare_periods` mostra isso como `previous_value: 0`, o que parece queda ou "partiu do zero". Escreva "sem dado antes de DD/MM/AAAA (conta conectada nessa data)", nunca "caiu" nem "cresceu".
2. **A coleta está viva?** Uma série com milhares por dia e, de repente, dias de 0 seguidos, numa métrica que nunca é zero (alcance, impressões de conta ativa), indica coleta parada (token vencido, permissão perdida, conta desconectada na origem), não queda real. Escreva "possível falha de coleta" e sugira conferir a integração no Reportei.
3. **`null` não é 0.** `comparison.values: null` quer dizer que não há dado do período anterior. Escreva "sem comparação disponível", nunca "cresceu infinito" nem "partiu do zero".
4. **Campanha pausada é zero real**; integração quebrada é sem dado. Só dá para separar olhando os dois: investimento zero com impressões zero numa conta que tinha campanhas ativas pede conferência.
5. **`data_status` em `get_report_data`:** leia o status de cada fonte antes de comentar os números dela.
6. **A integração foi pulada?** Em `compare_periods`, `get_performance_summary` e `get_audience_insights`, uma conta em `sources_with_errors` (`skipped_time_budget`) ou ausente da resposta não foi lida. Isso é "não consultado", não "sem dado" (ver seção 7).
7. **Métrica pouco madura.** Meta recém-criada aparece "sem dado" (`no_data`) ou com situação oscilando nos primeiros dias do período: é normal, não é falha.

Na dúvida, escreva os dois cenários: "zero no período; pode ser ausência de entrega ou falha de coleta: conferir a integração".

## 5. Variação em % com cuidado

- `comparison.difference` é a variação **em %**; mostre junto o valor absoluto (`absoluteDifference`) e os dois valores.
- **Base pequena engana:** de 100 para 1.000 é +900%. Com base anterior pequena, troque a % pela frase "de X para Y" e diga que a base era baixa.
- **Pontos percentuais para taxas:** CTR de 1,2% para 1,5% é "+0,3 p.p." (e +25% relativo). Diga qual das duas está usando.
- Número pequeno (dezenas de leads, poucas vendas) oscila muito. Informe o n. A regra de base pequena vale para contagem; valor em dinheiro se lê pelo valor.
- **Unidade de taxa:** antes de escrever um CTR ou taxa de conversão, recalcule com as bases (cliques ÷ impressões). Algumas plataformas devolvem fração (0,0250), outras pontos percentuais (2,5): o erro é de 100 vezes.
- **Custo por resultado igual ao investimento, com taxa de conversão 0**, quer dizer zero conversões, não um custo.

## 6. Somar e comparar contas e plataformas

- **Mais de uma conta da mesma plataforma no projeto:** as ferramentas de resumo (`compare_periods`, `get_performance_summary`, `get_campaign_summary`, `get_channel_breakdown`) mostram **uma conta só**, sem dizer qual, e cada uma pode escolher uma conta diferente. Podem dizer que leram todas mesmo assim. Nesse caso, leia conta por conta com `get_metrics_data` e **nunca some ou compare números de contas diferentes como se fossem uma**, nem ponha na mesma linha "anterior → atual" números vindos de ferramentas diferentes.
- Só some o que mede a mesma coisa: alcance de Instagram + alcance de Facebook **não é** público único (as pessoas se repetem). Escreva "soma do alcance das duas redes, com sobreposição".
- Investimento soma; CTR, CPC e CPM não somam (recalcule a partir das bases).
- Conversão de Meta Ads, Google Ads e GA4 **não somam**: cada plataforma atribui de um jeito e a mesma conversão aparece em mais de uma. Compare tendências, não some.
- **Engajamento não se compara entre redes sem conferir a definição:** a taxa de engajamento do LinkedIn inclui cliques; a do Instagram, não.
- Duas contas de mesmo nome no projeto: diga se somou as duas ou usou uma.

## 6a. Conversão: confira o que está sendo contado

"Conversão" no Reportei é o que a plataforma de anúncio chama de conversão, e pode ser um evento raso: visualização de página, clique em botão, etapa de formulário, evento de pixel que dispara mais de uma vez por pessoa. Antes de concluir sobre custo por resultado, custo por lead ou "a campanha converte bem":

1. **Abra o detalhe das ações de conversão:** `fb_ads:actions_by_type` e o resultado por campanha (`fb_ads:insights_by_campaign`) na Meta; `gads:custom_conversion_actions` no Google.
2. **Sinais de evento raso ou duplicado:** mais conversões que visitas à página de destino; taxa de conversão acima de 20% em captação de leads; custo por conversão muito abaixo do normal do negócio (centavos); uma única ação respondendo pela maior parte das conversões.
3. Com qualquer um desses sinais, escreva "conversão provavelmente rasa ou duplicada: conferir a configuração" e não use o número como lead ou venda.

## 6b. Metas: estimativa não é projeção

- `estimated_value` e `estimated_percent` de `get_goal_progress`, no começo do período, são só o esperado até hoje num ritmo linear. Não escreva "vai fechar em X" a partir deles.
- Projeção é cálculo seu (valor atual ÷ dias decorridos × dias do período), marcado como "calculado", e só depois de uns 7 dias de período.
- Na virada do período, as metas já mostram o período novo: o resultado do período fechado não aparece pelo conector.

## 7. Separe "não consultado" de "não existe"

- **Fora do escopo (escolha):** a skill não olhou aquela integração ou período.
- **Não consultado (limite):** a chamada falhou, travou, foi deixada de fora por custo, ou a ferramenta de resumo pulou a integração (`partial_results`, `skipped_time_budget`, ou conta ausente da resposta). Repita uma vez; se continuar, busque a integração direto com `get_metrics_data` e liste o que ficou sem leitura, com o nome da conta.
- **Não exposto pelo conector:** o conector não traz aquele dado (ex.: não aplica recomendações, não apaga relatório, não mostra a configuração da campanha).
- **Sem dado na plataforma:** a ferramenta respondeu e não havia dado.

Use a mesma formulação em todas as seções. "Não encontrei" nunca vira "não existe".

## 8. Antes de recomendar cortar verba ou mudar estratégia

Recomendação de **pausar campanha, cortar ou realocar investimento, trocar canal, mudar público ou criativo** só sai com esta lista conferida e escrita na resposta:

1. **Período suficiente:** pelo menos duas a quatro semanas, ou o ciclo de venda do cliente. Uma semana ruim não basta.
2. **Comparação justa:** mesmo tamanho, mesma sazonalidade (ver item 3).
3. **Coleta conferida:** sem dias zerados suspeitos nem integração desconectada (item 4).
4. **Métrica de resultado, não de vaidade:** custo por lead, por venda, ROAS. CTR e CPM sozinhos não justificam corte.
5. **Conversão medida de verdade:** a conversão que a campanha otimiza está chegando, e é um evento que vale (seção 6a)? Leads da plataforma batem, em ordem de grandeza, com o CRM ou o site, quando há integração para conferir?
6. **Volume:** n de conversões suficiente para a diferença não ser acaso. Diga o n.
7. **O que não foi visto:** configuração da campanha, orçamento por conjunto, mudanças feitas no período (a linha do tempo do projeto pode ter marcos: `list_timeline_events`).
8. **Recomendação condicional e reversível:** "se o custo por lead seguir acima de R$ X por mais duas semanas, reduzir o orçamento da campanha Y em 20%", não "desligue a campanha".
9. **Fecho:** "confirme com quem opera a conta antes de mudar".

## 9. Revisão final de palavras

Antes de entregar, procure e troque pela forma certa do nível de certeza:
- "caiu", "zerou", "parou" sobre um 0 não conferido;
- "pessoas alcançadas" sobre soma diária de alcance;
- "nota da Meta" sobre a nota do Reportei;
- "cresceu X%" com base pequena;
- "por causa de" sobre hipótese;
- "todos os projetos", "todas as contas" sem ter olhado todas as páginas (`meta.last_page`) e sem ter conferido se a ferramenta de resumo leu cada conta;
- "caiu" ou "cresceu" sobre conta conectada no meio do período;
- "custo por lead" sobre conversão não conferida.

## 10. Seções obrigatórias no fim

Toda resposta com análise termina com estas duas seções, com estes nomes (os mesmos de `formato-de-resposta.md`):

- **O que assumi:** período e comparação escolhidos, fuso, contas incluídas ou somadas, métricas usadas e por quê.
- **Limites:** o que não foi visto e por quê: chamadas que falharam, integrações puladas ou sem dado, contas conectadas no meio do período, o que o conector não expõe, com o próximo passo para fechar cada ponto.

Numa resposta curta, as duas cabem em até três linhas no rodapé, mas com esses dois nomes.

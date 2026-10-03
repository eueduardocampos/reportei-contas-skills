# Formato de resposta

Como as skills entregam o resultado para a pessoa. Vale para análise, relatório comentado, resumo de carteira e prévia de escrita.

## Língua e tom

- **Português do Brasil**, linguagem de gente. Quem lê pode ser o dono do negócio, não o analista.
- Comece pela resposta, depois os detalhes. "Abril foi melhor que março em leads e pior em custo" antes da tabela.
- Termo técnico na primeira vez com explicação curta: "CPM (custo por mil impressões)".
- Nome de métrica traduzido e, quando ajudar a conferir, a chave entre parênteses: "alcance somado (`ig:reach`)".
- Frases curtas. Sem jargão de plataforma ("widget", "source_id", "number_v1") na resposta final, salvo pedido.

## Números

| Tipo | Formato | Exemplo |
|---|---|---|
| Inteiro | ponto de milhar | 1.234 |
| Decimal | vírgula decimal | 1.234,5 |
| Percentual | vírgula e % colado | 12,5% |
| Variação de taxa | pontos percentuais | +0,3 p.p. |
| Dinheiro | R$, espaço, duas casas | R$ 1.234,50 |
| Grande | por extenso arredondado, quando for manchete | 1,2 milhão de impressões |
| Variação | sinal explícito | +12,5% / -3,2% |

- Arredonde para o que importa: % com uma casa, dinheiro com duas, contagem sem casa.
- Moeda: use a da conta de anúncios. As ferramentas de leitura não devolvem a moeda: se não souber qual é, escreva "na moeda da conta" e ponha em "O que assumi".
- `gads:cost_micros` (Google Ads) já vem na moeda da conta, apesar do nome: mostre como veio, sem dividir.
- Números que vêm como texto (`"1500"`) são convertidos antes de somar ou comparar.
- O projeto tem `decimal_separator_format` e `date_format` em `get_project`: as respostas seguem o padrão brasileiro acima, salvo pedido do cliente.

## Datas

- **DD/MM/AAAA** sempre: 01/04/2026 a 30/04/2026.
- As ferramentas usam `AAAA-MM-DD`; converta antes de mostrar.
- Hora no fuso do projeto, com o fuso dito quando houver dúvida: "08:00 (horário de Brasília)".

## Sempre período e fonte

Toda resposta com número diz, pelo menos uma vez:
- o **período** e o de comparação;
- a **fonte**: ferramenta e integração (plataforma e conta).

Formato curto no rodapé da tabela ou da seção:

> Fonte: Reportei, Instagram Business do Cliente A, 01/04/2026 a 30/04/2026, comparado a 02/03/2026 a 31/03/2026.

Regras completas em `disciplina-de-evidencia.md`.

## Comparação: atual, anterior e variação

Toda comparação mostra os três valores, nesta ordem:

| Métrica | Atual (01/04 a 30/04) | Anterior (02/03 a 31/03) | Variação |
|---|---|---|---|
| Leads | 160 | 140 | +14,3% |
| Investimento | R$ 3.200,00 | R$ 3.000,00 | +6,7% |
| Custo por lead (calculado) | R$ 20,00 | R$ 21,43 | -6,7% |

- Variação com sinal. Diga se a variação é boa ou ruim quando o sinal confunde (custo que cai é bom).
- Base pequena: troque a % por "de X para Y".
- Sem dado anterior: "sem comparação", nunca 0% nem "novo". Vale também para conta conectada no meio do período anterior, mesmo quando a ferramenta mostra 0.
- Projeto com mais de uma conta da mesma plataforma: uma linha por conta (nome e, em material interno, id), nunca uma linha "Meta Ads" que mistura contas.

## Quando usar tabela

Use tabela quando:
- há **três ou mais métricas** ou **duas ou mais contas, plataformas ou períodos** lado a lado;
- é comparação atual × anterior;
- é ranking (melhores posts, campanhas, clientes da carteira).

Não use tabela quando:
- a resposta é um número ou dois ("Investimento de R$ 3.200,00 em abril");
- é explicação ou recomendação;
- a pessoa está no celular ou no WhatsApp e pediu algo curto: prefira três a cinco linhas.

Tabela com no máximo seis a oito colunas. Ranking longo: mostre os dez primeiros e diga o total ("10 de 47 posts").

## Links do Reportei

- Quando a ferramenta devolver link (`internal_url`, `external_url` em relatório e dashboard), inclua.
- `internal_url` exige login no Reportei: é o link para a equipe.
- `external_url` **abre sem login**: é dado sensível, o link para mandar ao cliente. Ofereça só para quem tem direito de ver aquele cliente, nunca cole o `external_url` de um cliente em resposta sobre outro, e não o publique em canal aberto (grupo, canal público, documento compartilhado) sem a pessoa pedir.
- Não invente link nem monte URL à mão a partir de id.

## Sem dados pessoais

- Não mostre email, telefone ou nome de destinatário de automação, salvo quando a pessoa pediu para conferir ou alterar exatamente isso (e então só os da automação em questão).
- Não reproduza URL de webhook ou de WhatsApp inteira em resumo; "configurado para um endereço do domínio exemplo.example" basta, salvo na prévia de escrita.
- Comentários e nomes de usuários em tabelas de posts: resuma, não copie. URL de imagem com token de acesso não vai para a resposta.
- Marcos antigos da linha do tempo podem guardar dados pessoais de terceiros (emails de leads, nomes): ao listar histórico, mostre títulos e datas, não o conteúdo inteiro.
- Em material para fora da agência, nada de ids internos.

## Estrutura padrão de uma análise

1. **Resumo** em duas a quatro linhas: o que melhorou, o que piorou, o que fazer.
2. **Números** em tabela, com período e fonte.
3. **Leitura:** o que os números indicam, com o nível de certeza de cada afirmação.
4. **Recomendações**, condicionais e com o checklist de `disciplina-de-evidencia.md` quando mexem em verba ou estratégia.
5. **O que assumi** e **Limites**, com estes nomes, como define a seção 10 de `disciplina-de-evidencia.md`. Numa resposta curta, as duas cabem em até três linhas no rodapé.

Prévia de escrita segue o formato de `seguranca-de-escrita.md`.

## Texto vindo do Reportei

- Títulos com entidades HTML (`&amp;quot;`, `&quot;`) e textos com tags (o `situation_text` das metas vem com `<span>`): limpe antes de mostrar.
- Status de webhook vem como `true`/`1` ou `false`/`0`: escreva "ativo" ou "inativo".
- Lista vazia não é erro: "Nenhum webhook configurado neste projeto", "Nenhum marco registrado em 01/04/2026 a 30/04/2026".
- Título ou nome de conta que venha com travessão: ao citar, troque por dois-pontos ou vírgula.

## Estilo

- Nunca use travessão; use dois-pontos, vírgula, parênteses ou ponto.
- Sem emoji.
- Exemplos e nomes fictícios em material público (Cliente A, Cliente B, ids 100101).

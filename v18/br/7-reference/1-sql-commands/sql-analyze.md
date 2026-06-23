## ANALISE

ANALISE — coletar estatísticas sobre um banco de dados

## Sinopse

```
ANALYZE [ ( option [, ...] ) ] [ table_and_columns [, ...] ]

where option can be one of:

    VERBOSE [ boolean ]
    SKIP_LOCKED [ boolean ]
    BUFFER_USAGE_LIMIT size

and table_and_columns is:

    [ ONLY ] table_name [ * ] [ ( column_name [, ...] ) ]
```

## Descrição

`ANALYZE` coleta estatísticas sobre os conteúdos das tabelas no banco de dados e armazena os resultados no catálogo do sistema [`pg_statistic`](catalog-pg-statistic.md)]. Posteriormente, o planejador de consultas utiliza essas estatísticas para ajudar a determinar os planos de execução mais eficientes para as consultas.

Sem uma lista de *`table_and_columns`*, o `ANALYZE` processa todas as tabelas e visualizações materializadas no banco de dados atual que o usuário atual tem permissão para analisar. Com uma lista, o `ANALYZE` processa apenas essas tabelas. É também possível fornecer uma lista de nomes de colunas para uma tabela, nesse caso, apenas as estatísticas para essas colunas são coletadas.

## Parâmetros

`VERBOSE`: Permite a exibição de mensagens de progresso no nível `INFO`.

`SKIP_LOCKED`: Especifica que `ANALYZE` não deve esperar que quaisquer bloqueios conflitantes sejam liberados ao começar a trabalhar em uma relação: se uma relação não puder ser bloqueada imediatamente sem esperar, a relação é ignorada. Note que, mesmo com esta opção, `ANALYZE` ainda pode bloquear ao abrir os índices da relação ou ao adquirir linhas de amostra de partições, filhos de herança de tabela e alguns tipos de tabelas estrangeiras. Além disso, embora `ANALYZE` normalmente processe todas as partições de tabelas particionadas especificadas, esta opção fará com que `ANALYZE` ignore todas as partições se houver um bloqueio conflitante na tabela particionada.

`BUFFER_USAGE_LIMIT`: Especifica o tamanho do buffer de acesso (glossary.md#GLOSSARY-BUFFER-ACCESS-STRATEGY "Buffer Access Strategy") (glossário.md#GLOSSARY-BUFFER-ACCESS-STRATEGY) para `ANALYZE`. Esse tamanho é usado para calcular o número de buffers compartilhados que serão reutilizados como parte dessa estratégia. `0` desabilita o uso de um `Buffer Access Strategy`. Quando essa opção não é especificada, `ANALYZE` usa o valor de [limite_uso_buffer_vacuum](runtime-config-resource.md#GUC-VACUUM-BUFFER-USAGE-LIMIT). Configurações mais altas podem permitir que `ANALYZE` seja executado mais rapidamente, mas ter uma configuração muito grande pode causar que muitas outras páginas úteis sejam expulsas dos buffers compartilhados. O valor mínimo é `128 kB` e o valor máximo é `16 GB`.

*`boolean`*: Especifica se a opção selecionada deve ser ativada ou desativada. Você pode escrever `TRUE`, `ON` ou `1` para ativar a opção, e `FALSE`, `OFF` ou `0` para desativá-la. O valor *`boolean`* também pode ser omitido, no qual caso `TRUE` é assumido.

*`size`*: Especifica uma quantidade de memória em kilobytes. Os tamanhos também podem ser especificados como uma string que contém o tamanho numérico seguido de uma das seguintes unidades de memória: `B` (bytes), `kB` (kilobytes), `MB` (megabytes), `GB` (gigabytes) ou `TB` (terabytes).

*`table_name`*: O nome (possivelmente qualificado por esquema) de uma tabela específica a ser analisada. Se omitido, todas as tabelas regulares, tabelas particionadas e visualizações materializadas no banco de dados atual são analisadas (mas não tabelas externas). Se `ONLY` é especificado antes do nome da tabela, apenas essa tabela é analisada. Se `ONLY` não é especificado, a tabela e todas as suas tabelas filhas de herança ou particionamentos (se houver) são analisadas. Opcionalmente, `*` pode ser especificado após o nome da tabela para indicar explicitamente que as tabelas filhas de herança (ou particionamentos) devem ser analisadas.

*`column_name`*: O nome de uma coluna específica para análise. Por padrão, são todas as colunas.

## Saídas

Quando `VERBOSE` é especificado, `ANALYZE` emite mensagens de progresso para indicar qual tabela está sendo processada atualmente. Várias estatísticas sobre as tabelas também são impressas.

## Notas

Para analisar uma tabela, é necessário, normalmente, ter o privilégio `MAINTAIN` na tabela. No entanto, os proprietários do banco de dados podem analisar todas as tabelas em seus bancos de dados, exceto catálogos compartilhados. `ANALYZE` ignorará quaisquer tabelas que o usuário que está fazendo a chamada não tenha permissão para analisar.

As tabelas externas são analisadas apenas quando explicitamente selecionadas. Nem todos os wrappers de dados externos suportam `ANALYZE`. Se o wrapper da tabela não suportar `ANALYZE`, o comando exibe um aviso e não faz nada.

Na configuração padrão do PostgreSQL, o daemon de autovazamento (consulte [Seção 24.1.6](routine-vacuuming.md#AUTOVACUUM)) cuida da análise automática das tabelas quando elas são carregadas com dados pela primeira vez e conforme elas mudam durante o funcionamento regular. Quando o autovazamento é desativado, é uma boa ideia executar `ANALYZE` periodicamente, ou logo após fazer alterações importantes no conteúdo de uma tabela. Estatísticas precisas ajudarão o planejador a escolher o plano de consulta mais apropriado, e assim melhorarão a velocidade do processamento da consulta. Uma estratégia comum para bancos que recebem leitura predominante é executar `VACUUM` e `ANALYZE` uma vez por dia durante um período de baixa utilização do dia. (Isso não será suficiente se houver uma atividade de atualização pesada.)

Enquanto o `ANALYZE` está em execução, o [search_path](runtime-config-client.md#GUC-SEARCH-PATH) é temporariamente alterado para `pg_catalog, pg_temp`.

`ANALYZE` exige apenas um bloqueio de leitura na tabela alvo, portanto, pode ser executado em paralelo com outras atividades que não são DDL na tabela.

As estatísticas coletadas pelo `ANALYZE` geralmente incluem uma lista dos valores mais comuns em cada coluna e um histograma que mostra a distribuição aproximada dos dados em cada coluna. Um ou ambos podem ser omitidos se o `ANALYZE` os considerar pouco interessantes (por exemplo, em uma coluna de chave única, não há valores comuns) ou se o tipo de dados da coluna não suporte os operadores apropriados. Há mais informações sobre as estatísticas em [Capítulo 24](maintenance.md "Chapter 24. Routine Database Maintenance Tasks").

Para tabelas grandes, `ANALYZE` tira uma amostra aleatória do conteúdo da tabela, em vez de examinar cada linha. Isso permite que até mesmo tabelas muito grandes sejam analisadas em um pequeno período de tempo. No entanto, observe que as estatísticas são apenas aproximadas e mudarão ligeiramente cada vez que `ANALYZE` é executado, mesmo que o conteúdo real da tabela não tenha mudado. Isso pode resultar em pequenas mudanças nos custos estimados do planejador mostrados por `EXPLAIN`(sql-explain.md "EXPLAIN"). Em situações raras, esse não-determinismo fará com que as escolhas do planejador de planos de consulta mudem após `ANALYZE` ser executado. Para evitar isso, aumente a quantidade de estatísticas coletadas por `ANALYZE`, conforme descrito abaixo.

A extensão da análise pode ser controlada ajustando a variável de configuração [default_statistics_target](runtime-config-query.md#GUC-DEFAULT-STATISTICS-TARGET). Ou, de forma coluna por coluna, definindo o alvo de estatísticas por coluna com [`ALTER TABLE ... ALTER COLUMN ... SET STATISTICS`](sql-altertable.md). O valor alvo define o número máximo de entradas na lista de valores mais comuns e o número máximo de bins no histograma. O valor padrão do alvo é 100, mas isso pode ser ajustado para cima ou para baixo para equilibrar a precisão das estimativas do planejador contra o tempo gasto para `ANALYZE` e a quantidade de espaço ocupado em `pg_statistic`. Em particular, definir o alvo de estatísticas como zero desativa a coleta de estatísticas para aquela coluna. Pode ser útil fazer isso para colunas que nunca são usadas como parte das cláusulas `WHERE`, `GROUP BY` ou `ORDER BY` das consultas, pois o planejador não terá uso para estatísticas nessas colunas.

O maior alvo estatístico entre as colunas que estão sendo analisadas determina o número de linhas de tabela amostradas para preparar as estatísticas. Aumentar o alvo causa um aumento proporcional no tempo e no espaço necessários para fazer `ANALYZE`.

Um dos valores estimados por `ANALYZE` é o número de valores distintos que aparecem em cada coluna. Como apenas um subconjunto das linhas é examinado, essa estimativa pode, às vezes, ser bastante imprecisa, mesmo com o objetivo de estatísticas mais amplos. Se essa imprecisão levar a planos de consulta ruins, um valor mais preciso pode ser determinado manualmente e, em seguida, instalado com `ALTER TABLE ... ALTER COLUMN ... SET (n_distinct = ...)`(sql-altertable.md "ALTER TABLE").

Se a tabela que está sendo analisada tiver filhos por herança, o `ANALYZE` reúne dois conjuntos de estatísticas: um nas linhas da tabela pai apenas e um segundo que inclui as linhas tanto da tabela pai quanto de todos os seus filhos. Este segundo conjunto de estatísticas é necessário ao planejar consultas que processam a árvore de herança como um todo. O daemon de autovazamento, no entanto, só considerará inserções ou atualizações na própria tabela pai ao decidir se deve desencadear um análise automática para aquela tabela. Se essa tabela for raramente inserida ou atualizada, as estatísticas de herança não estarão atualizadas, a menos que você execute manualmente o `ANALYZE`. Por padrão, o `ANALYZE` também coletará e atualizará recursivamente as estatísticas para cada tabela de filho de herança. A palavra-chave `ONLY` pode ser usada para desabilitar isso.

Para tabelas particionadas, `ANALYZE` reúne estatísticas através da amostragem de linhas de todas as particionamentos. Por padrão, `ANALYZE` também coletará e atualizará recursivamente as estatísticas para cada particionamento. A palavra-chave `ONLY` pode ser usada para desabilitar isso.

O daemon de autovacuum não processa tabelas particionadas, nem processa pais de herança se apenas as crianças forem modificadas. Geralmente é necessário executar periodicamente um `ANALYZE` manual para manter as estatísticas da hierarquia da tabela atualizadas.

Se alguma tabela ou partição de criança for uma tabela estrangeira cujos wrappers de dados estrangeiros não suportam `ANALYZE`, essas tabelas são ignoradas durante a coleta de estatísticas de herança.

Se a tabela que está sendo analisada estiver completamente vazia, `ANALYZE` não registrará novas estatísticas para essa tabela. Todas as estatísticas existentes serão mantidas.

Cada backend que executa `ANALYZE` informará seu progresso na visão `pg_stat_progress_analyze`. Consulte [Seção 27.4.1](progress-reporting.md#ANALYZE-PROGRESS-REPORTING) para obter detalhes.

## Compatibilidade

Não há nenhuma declaração `ANALYZE` no padrão SQL.

A sintaxe a seguir foi usada antes da versão 11 do PostgreSQL e ainda é suportada:

```
ANALYZE [ VERBOSE ] [ table_and_columns [, ...] ]
```

## Veja também

[VACUUM](sql-vacuum.md "VACUUM"), [vacuumdb](app-vacuumdb.md "vacuumdb"), [Seção 19.10.2](runtime-config-vacuum.md#RUNTIME-CONFIG-RESOURCE-VACUUM-COST "19.10.2. Cost-based Vacuum Delay"), [Seção 24.1.6](routine-vacuuming.md#AUTOVACUUM "24.1.6. The Autovacuum Daemon"), [Seção 27.4.1](progress-reporting.md#ANALYZE-PROGRESS-REPORTING "27.4.1. ANALYZE Progress Reporting")
## VACÚO

VACUUM — recolhe lixo e, opcionalmente, analisa um banco de dados

## Sinopse

```
VACUUM [ ( option [, ...] ) ] [ table_and_columns [, ...] ]

where option can be one of:

    FULL [ boolean ]
    FREEZE [ boolean ]
    VERBOSE [ boolean ]
    ANALYZE [ boolean ]
    DISABLE_PAGE_SKIPPING [ boolean ]
    SKIP_LOCKED [ boolean ]
    INDEX_CLEANUP { AUTO | ON | OFF }
    PROCESS_MAIN [ boolean ]
    PROCESS_TOAST [ boolean ]
    TRUNCATE [ boolean ]
    PARALLEL integer
    SKIP_DATABASE_STATS [ boolean ]
    ONLY_DATABASE_STATS [ boolean ]
    BUFFER_USAGE_LIMIT size

and table_and_columns is:

    [ ONLY ] table_name [ * ] [ ( column_name [, ...] ) ]
```

## Descrição

`VACUUM` reivindica o armazenamento ocupado por tuplas mortas. Na operação normal do PostgreSQL, as tuplas que são excluídas ou obsoletas por uma atualização não são removidas fisicamente de sua tabela; elas permanecem presentes até que um `VACUUM` seja realizado. Portanto, é necessário realizar `VACUUM` periodicamente, especialmente em tabelas frequentemente atualizadas.

Sem uma lista de *`table_and_columns`*, o `VACUUM` processa todas as tabelas e visualizações materializadas no banco de dados atual que o usuário atual tem permissão para vacúmen. Com uma lista, o `VACUUM` processa apenas essas tabelas.

`VACUUM ANALYZE` realiza um `VACUUM` e, em seguida, um `ANALYZE` para cada tabela selecionada. Este é um formulário de combinação útil para scripts de manutenção de rotina. Consulte [ANALYZE](sql-analyze.md "ANALYZE") para obter mais detalhes sobre seu processamento.

A forma simples `VACUUM` (sem `FULL`) simplesmente reclama espaço e o torna disponível para uso novamente. Esta forma do comando pode operar em paralelo com a leitura e escrita normais da tabela, pois não é obtido um bloqueio exclusivo. No entanto, o espaço extra não é devolvido ao sistema operacional (na maioria dos casos); ele é apenas mantido disponível para uso novamente dentro da mesma tabela. Também nos permite aproveitar múltiplos CPUs para processar índices. Esta funcionalidade é conhecida como *vazamento paralelo*. Para desabilitar esta funcionalidade, pode-se usar a opção `PARALLEL` e especificar trabalhadores paralelos como zero. `VACUUM FULL` reescreve todo o conteúdo da tabela em um novo arquivo de disco sem espaço extra, permitindo que o espaço não utilizado seja devolvido ao sistema operacional. Esta forma é muito mais lenta e requer um bloqueio `ACCESS EXCLUSIVE` em cada tabela enquanto ela está sendo processada.

## Parâmetros

`FULL`: Seleciona o vácuo "completo", que pode recuperar mais espaço, mas leva muito mais tempo e bloqueia exclusivamente a tabela. Esse método também requer espaço em disco adicional, pois escreve uma nova cópia da tabela e não libera a cópia antiga até que a operação esteja completa. Geralmente, isso deve ser usado apenas quando uma quantidade significativa de espaço precisa ser recuperada dentro da tabela.

`FREEZE`: Seleciona o "congelamento" agressivo de tuplas. Especificar `FREEZE` é equivalente a realizar `VACUUM` com os parâmetros [vacuum_freeze_min_age](runtime-config-vacuum.md#GUC-VACUUM-FREEZE-MIN-AGE) e [vacuum_freeze_table_age](runtime-config-vacuum.md#GUC-VACUUM-FREEZE-TABLE-AGE) definidos como zero. O congelamento agressivo é sempre realizado quando a tabela é reescrita, portanto, essa opção é redundante quando `FULL` é especificada.

`VERBOSE`: Imprime um relatório detalhado sobre a atividade de vácuo para cada tabela no nível `INFO`.

`ANALYZE`: Atualiza as estatísticas usadas pelo planejador para determinar a maneira mais eficiente de executar uma consulta.

`DISABLE_PAGE_SKIPPING`: Normalmente, `VACUUM` ignorará páginas com base no mapa de visibilidade (routine-vacuuming.md#VACUUM-FOR-VISIBILITY-MAP "24.1.4. Updating the Visibility Map"). As páginas em que todos os tuplos são conhecidos como congelados podem ser sempre ignoradas, e aquelas em que todos os tuplos são conhecidos como visíveis para todas as transações podem ser ignoradas, exceto quando se está realizando um vácuo agressivo. Além disso, exceto quando se está realizando um vácuo agressivo, algumas páginas podem ser ignoradas para evitar a espera de outras sessões para usá-las. Esta opção desativa todo o comportamento de ignorar páginas e é destinada a ser usada apenas quando o conteúdo do mapa de visibilidade é suspeito, o que deve acontecer apenas se houver um problema de hardware ou software causando corrupção do banco de dados.

`SKIP_LOCKED`: Especifica que `VACUUM` não deve esperar que quaisquer bloqueios conflitantes sejam liberados ao começar a trabalhar em uma relação: se uma relação não puder ser bloqueada imediatamente sem esperar, a relação é ignorada. Note que, mesmo com esta opção, `VACUUM` ainda pode bloquear ao abrir os índices da relação. Além disso, `VACUUM ANALYZE` ainda pode bloquear ao adquirir linhas de amostra de partições, filhos de herança de tabela e alguns tipos de tabelas estrangeiras. Além disso, embora `VACUUM` normalmente processe todas as partições das tabelas particionadas especificadas, esta opção fará com que `VACUUM` ignore todas as partições se houver um bloqueio conflitante na tabela particionada.

`INDEX_CLEANUP`: Normalmente, `VACUUM` ignorará o varredura de índices quando houver poucos tuplos mortos na tabela. O custo do processamento de todos os índices da tabela é esperado que ultrapasse significativamente o benefício da remoção de tuplos de índice mortos quando isso acontece. Esta opção pode ser usada para forçar `VACUUM` a processar índices quando houver mais de zero tuplos mortos. A opção padrão é `AUTO`, que permite que `VACUUM` ignore a varredura de índices quando apropriado. Se `INDEX_CLEANUP` estiver definido como `ON`, `VACUUM` removerá de forma conservadora todos os tuplos mortos dos índices. Isso pode ser útil para compatibilidade reversa com versões anteriores do PostgreSQL, onde esse era o comportamento padrão.

`INDEX_CLEANUP` também pode ser configurado para `OFF` para forçar que o `VACUUM` *sempre* ignore o rastreamento de índices, mesmo quando há muitos tuplos mortos na tabela. Isso pode ser útil quando é necessário fazer o `VACUUM` funcionar o mais rápido possível para evitar o enrolamento iminente do ID de transação (ver [Seção 24.1.5](routine-vacuuming.md#VACUUM-FOR-WRAPAROUND)). No entanto, o mecanismo de segurança de enrolamento controlado por [vacuum_failsafe_age](runtime-config-vacuum.md#GUC-VACUUM-FAILSAFE-AGE) geralmente será acionado automaticamente para evitar a falha do enrolamento do ID de transação, e deve ser preferido. Se a limpeza de índices não for realizada regularmente, o desempenho pode sofrer, pois, à medida que a tabela é modificada, os índices acumulam tuplos mortos e a própria tabela acumula ponteiros de linha mortos que não podem ser removidos até que a limpeza de índices seja concluída.

Esta opção não tem efeito para tabelas que não possuem índice e é ignorada se a opção `FULL` for usada. Também não tem efeito no mecanismo de falha de envolvimento de ID de transação. Quando acionado, ele ignorará o vácuo de índice, mesmo quando `INDEX_CLEANUP` está definido como `ON`.

`PROCESS_MAIN`: Especifica que `VACUUM` deve tentar processar a relação principal. Esse é geralmente o comportamento desejado e é o padrão. Definir essa opção como falsa pode ser útil quando é necessário apenas aspirar a tabela correspondente `TOAST` de uma relação.

`PROCESS_TOAST`: Especifica que `VACUUM` deve tentar processar a tabela correspondente `TOAST` para cada relação, se existir. Esse é geralmente o comportamento desejado e é o padrão. Definir essa opção como falsa pode ser útil quando é necessário apenas vacumar a relação principal. Essa opção é necessária quando a opção `FULL` é usada.

`TRUNCATE`: Especifica que `VACUUM` deve tentar truncar quaisquer páginas vazias no final da tabela e permitir que o espaço em disco para as páginas truncadas seja devolvido ao sistema operacional. Esse é normalmente o comportamento desejado e é o padrão, a menos que [vacuum_truncate](runtime-config-vacuum.md#GUC-VACUUM-TRUNCATE) seja definido como falso ou que a opção `vacuum_truncate` tenha sido definida como falsa para a tabela que será vacumada. Definir essa opção como falsa pode ser útil para evitar o bloqueio `ACCESS EXCLUSIVE` na tabela que a truncação requer. Esta opção é ignorada se a opção `FULL` for usada.

`PARALLEL`: Realize as fases de vácuo de índice e limpeza de índice de `VACUUM` em paralelo usando *`integer`* trabalhadores de fundo (para os detalhes de cada fase de vácuo, consulte [Tabela 27.46](progress-reporting.md#VACUUM-PHASES "Table 27.46. VACUUM Phases")). O número de trabalhadores usados para realizar a operação é igual ao número de índices na relação que suportam vácuo em paralelo, que é limitado pelo número de trabalhadores especificados com a opção `PARALLEL`, se houver, que é ainda limitado por [max_parallel_maintenance_workers](runtime-config-resource.md#GUC-MAX-PARALLEL-MAINTENANCE-WORKERS). Um índice pode participar em vácuo em paralelo se e somente se o tamanho do índice for maior que [min_parallel_index_scan_size](runtime-config-query.md#GUC-MIN-PARALLEL-INDEX-SCAN-SIZE). Observe que não é garantido que o número de trabalhadores paralelos especificados em *`integer`* será usado durante a execução. É possível que um vácuo seja executado com menos trabalhadores do que o especificado, ou até mesmo sem nenhum trabalhador. Apenas um trabalhador pode ser usado por índice. Portanto, os trabalhadores paralelos são lançados apenas quando há pelo menos `2` índices na tabela. Os trabalhadores para vácuo são lançados antes do início de cada fase e saem no final da fase. Esses comportamentos podem mudar em uma versão futura. Esta opção não pode ser usada com a opção `FULL`.

`SKIP_DATABASE_STATS`: Especifica que `VACUUM` deve ignorar a atualização das estatísticas de nível de banco sobre os XIDs mais antigos não congelados. Normalmente, `VACUUM` atualizará essas estatísticas uma vez no final do comando. No entanto, isso pode levar algum tempo em um banco de dados com um número muito grande de tabelas, e não fará nada a menos que a tabela que continha o XID mais antigo não congelado esteja entre as que foram varridas. Além disso, se vários comandos `VACUUM` forem emitidos em paralelo, apenas um deles pode atualizar as estatísticas de nível de banco de cada vez. Portanto, se um aplicativo pretende emitir uma série de muitos comandos `VACUUM`, pode ser útil definir essa opção em todos, exceto no último desses comandos; ou defini-la em todos os comandos e emitir `VACUUM (ONLY_DATABASE_STATS)` separadamente depois.

`ONLY_DATABASE_STATS`: Especifica que `VACUUM` não deve fazer nada além de atualizar as estatísticas em relação aos XIDs mais antigos não congelados em toda a base de dados. Quando esta opção é especificada, a lista *`table_and_columns`* deve estar vazia e nenhuma outra opção pode ser habilitada, exceto `VERBOSE`.

`BUFFER_USAGE_LIMIT`: Especifica o tamanho do buffer de acesso de anel (glossary.md#GLOSSARY-BUFFER-ACCESS-STRATEGY "Buffer Access Strategy") (glossário.md#GLOSSARY-BUFFER-ACCESS-STRATEGY) para `VACUUM`. Esse tamanho é usado para calcular o número de buffers compartilhados que serão reutilizados como parte dessa estratégia. `0` desabilita o uso de um `Buffer Access Strategy`. Se `ANALYZE` também for especificado, o valor de `BUFFER_USAGE_LIMIT` é usado tanto para as etapas de vácuo quanto de análise. Esta opção não pode ser usada com a opção `FULL`, exceto se `ANALYZE` também for especificado. Quando esta opção não é especificada, `VACUUM` usa o valor de [limite_uso_buffer_de_vazamento](runtime-config-resource.md#GUC-VACUUM-BUFFER-USAGE-LIMIT). Configurações mais altas podem permitir que `VACUUM` seja executado mais rapidamente, mas ter uma configuração muito grande pode causar que muitas outras páginas úteis sejam expulsas dos buffers compartilhados. O valor mínimo é `128 kB` e o valor máximo é `16 GB`.

*`boolean`*: Especifica se a opção selecionada deve ser ativada ou desativada. Você pode escrever `TRUE`, `ON` ou `1` para ativar a opção, e `FALSE`, `OFF` ou `0` para desativá-la. O valor *`boolean`* também pode ser omitido, no qual caso `TRUE` é assumido.

*`integer`*: Especifica um valor inteiro não negativo passado para a opção selecionada.

*`size`*: Especifica uma quantidade de memória em kilobytes. Os tamanhos também podem ser especificados como uma string que contém o tamanho numérico seguido por uma das seguintes unidades de memória: `B` (bytes), `kB` (kilobytes), `MB` (megabytes), `GB` (gigabytes) ou `TB` (terabytes).

*`table_name`*: O nome (opcionalmente qualificado por esquema) de uma tabela específica ou visão materializada para ser vacumada. Se `ONLY` é especificado antes do nome da tabela, apenas essa tabela é vacumada. Se `ONLY` não é especificado, a tabela e todas as suas tabelas filhas de herança ou partições (se houver) também são vacumadas. Opcionalmente, `*` pode ser especificado após o nome da tabela para indicar explicitamente que as tabelas filhas de herança (ou partições) devem ser vacumadas.

*`column_name`*: O nome de uma coluna específica para análise. Por padrão, são todas as colunas. Se uma lista de colunas for especificada, `ANALYZE` também deve ser especificado.

## Saídas

Quando `VERBOSE` é especificado, `VACUUM` emite mensagens de progresso para indicar qual tabela está sendo processada atualmente. Várias estatísticas sobre as tabelas também são impressas.

## Notas

Para realizar uma limpeza de tabela, é necessário, normalmente, ter o privilégio `MAINTAIN` na tabela. No entanto, os proprietários do banco de dados podem realizar a limpeza de todas as tabelas em seus bancos de dados, exceto catálogos compartilhados. `VACUUM` ignorará quaisquer tabelas que o usuário que está fazendo a chamada não tenha permissão para limpar.

Enquanto o `VACUUM` está em execução, o [search_path](runtime-config-client.md#GUC-SEARCH-PATH) é temporariamente alterado para `pg_catalog, pg_temp`.

`VACUUM` não pode ser executado dentro de um bloco de transação.

Para tabelas com índices GIN, `VACUUM` (em qualquer forma) também completa quaisquer inserções de índice pendentes, movendo as entradas de índice pendentes para os lugares apropriados na estrutura principal do índice GIN. Consulte [Seção 65.4.4.1](gin.md#GIN-FAST-UPDATE) para detalhes.

Recomendamos que todas as bases de dados sejam limpas regularmente para remover as linhas mortas. O PostgreSQL inclui uma funcionalidade de "autovacuum" que pode automatizar a manutenção de limpeza de rotina. Para mais informações sobre a limpeza automática e manual, consulte [Seção 24.1](routine-vacuuming.md).

A opção `FULL` não é recomendada para uso rotineiro, mas pode ser útil em casos especiais. Um exemplo é quando você excluiu ou atualizou a maioria das linhas de uma tabela e gostaria que a tabela encolhesse fisicamente para ocupar menos espaço em disco e permitir pesquisas mais rápidas na tabela. `VACUUM FULL` geralmente encolherá a tabela mais do que um simples `VACUUM` faria.

A opção `PARALLEL` é usada apenas para fins de vácuo. Se esta opção for especificada com a opção `ANALYZE`, ela não afeta `ANALYZE`.

`VACUUM` provoca um aumento substancial no tráfego de I/O, o que pode causar um desempenho ruim para outras sessões ativas. Portanto, às vezes é aconselhável usar o recurso de atraso de vácuo baseado no custo. Para o vácuo paralelo, cada trabalhador dorme na proporção do trabalho realizado por esse trabalhador. Consulte [Seção 19.10.2](runtime-config-vacuum.md#RUNTIME-CONFIG-RESOURCE-VACUUM-COST) para obter detalhes.

Os backends que executam `VACUUM` sem a opção `FULL` informarão seu progresso na visualização `pg_stat_progress_vacuum`. Os backends que executam `VACUUM FULL` informarão, em vez disso, seu progresso na visualização `pg_stat_progress_cluster`. Consulte [Seção 27.4.5](progress-reporting.md#VACUUM-PROGRESS-REPORTING "27.4.5. VACUUM Progress Reporting") e [Seção 27.4.2](progress-reporting.md#CLUSTER-PROGRESS-REPORTING "27.4.2. CLUSTER Progress Reporting") para obter detalhes.

## Exemplos

Para limpar uma única tabela `onek`, analise-a para o otimizador e imprima um relatório detalhado de atividade de vácuo:

```
VACUUM (VERBOSE, ANALYZE) onek;
```

## Compatibilidade

Não há nenhuma declaração `VACUUM` no padrão SQL.

A sintaxe a seguir foi usada antes da versão 9.0 do PostgreSQL e ainda é suportada:

```
VACUUM [ FULL ] [ FREEZE ] [ VERBOSE ] [ ANALYZE ] [ table_and_columns [, ...] ]
```

Observe que, nesta sintaxe, as opções devem ser especificadas exatamente na ordem mostrada.

## Veja também

[vacuumdb](app-vacuumdb.md), [Seção 19.10.2](runtime-config-vacuum.md#RUNTIME-CONFIG-RESOURCE-VACUUM-COST), [Seção 24.1.6](routine-vacuuming.md#AUTOVACUUM), [Seção 27.4.5](progress-reporting.md#VACUUM-PROGRESS-REPORTING), [Seção 27.4.2](progress-reporting.md#CLUSTER-PROGRESS-REPORTING)
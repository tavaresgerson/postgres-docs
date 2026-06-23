## F.29. pg_overexplain — permitir que o EXPLAIN descarregue ainda mais detalhes [#](#PGOVEREXPLAIN)

* [F.29.1. EXPLAIN (DEBUG)](pgoverexplain.md#PGOVEREXPLAIN-DEBUG)
* [F.29.2. EXPLAIN (RANGE_TABLE)](pgoverexplain.md#PGOVEREXPLAIN-RANGE-TABLE)
* [F.29.3. Autor](pgoverexplain.md#PGOVEREXPLAIN-AUTHOR)

O módulo `pg_overexplain` estende o `EXPLAIN` com novas opções que fornecem saída adicional. Ele é principalmente destinado a auxiliar no depuração e desenvolvimento do planejador, e não para uso geral. Como este módulo exibe detalhes internos das estruturas de dados do planejador, pode ser necessário consultar o código-fonte para entender a saída. Além disso, a saída provavelmente mudará sempre que (e tão frequentemente quanto) essas estruturas de dados mudarem.

Para usá-lo, basta carregá-lo no servidor. Você pode carregá-lo em uma sessão individual:

```
LOAD 'pg_overexplain';
```

Você também pode pré-carregá-lo em algumas ou todas as sessões, incluindo `pg_overexplain` em [session_preload_libraries](runtime-config-client.md#GUC-SESSION-PRELOAD-LIBRARIES) ou [shared_preload_libraries](runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES) em `postgresql.conf`.

### F.29.1. EXPLIQUE (DE DETALHO) [#](#PGOVEREXPLAIN-DEBUG)

A opção `DEBUG` exibe informações diversas da árvore do plano que normalmente não são mostradas, pois não se espera que sejam de interesse geral. Para cada nó individual do plano, ela exibirá os seguintes campos. Consulte `Plan` em `nodes/plannodes.h` para documentação adicional desses campos.

* `Disabled Nodes`. O `EXPLAIN` normal determina se um nó está desativado, verificando se o número de nós desativados do nó é maior que a soma dos números dos nós subjacentes. Esta opção exibe o valor bruto do contador.
* `Parallel Safe`. Indica se seria seguro que um nó da árvore de plano aparecesse abaixo de um nó `Gather` ou `Gather Merge`, independentemente de ele realmente estar abaixo de tal nó.
* `Plan Node ID`. Um número de ID interno que deve ser único para cada nó na árvore de plano. É usado para coordenar a atividade de consulta paralela.
* `extParam` e `allParam`. Informações sobre quais parâmetros numerados afetam este nó do plano ou seus filhos. No modo de texto, esses campos são exibidos apenas se forem conjuntos não vazios.

Uma vez por consulta, a opção `DEBUG` exibirá os seguintes campos. Consulte `PlannedStmt` em `nodes/plannodes.h` para obter detalhes adicionais.

* `Command Type`. Por exemplo, `select` ou `update`.
* `Flags`. Uma lista de nomes de membros da estrutura de Booleano separados por vírgula da `PlannedStmt` que são definidos como `true`. Cobre os seguintes membros da estrutura: `hasReturning`, `hasModifyingCTE`, `canSetTag`, `transientPlan`, `dependsOnRole`, `parallelModeNeeded`.
* `Subplans Needing Rewind`. IDs inteiros de subplanos que podem precisar ser rewindados pelo executor.
* `Relation OIDs`. OIDs de relações sobre as quais este plano depende.
* `Executor Parameter Types`. OID do tipo para cada parâmetro do executor (por exemplo, quando uma alça aninhada é escolhida e um parâmetro é usado para passar um valor para uma varredura de índice interno). Não inclui parâmetros fornecidos a uma declaração preparada pelo usuário.
* `Parse Location`. Localização dentro da string de consulta fornecida ao planejador onde o texto desta consulta pode ser encontrado. Pode ser `Unknown` em alguns contextos. Caso contrário, pode ser `NNN to end` para alguns IDs inteiros `NNN` ou `NNN for MMM bytes` para alguns IDs inteiros `NNN` e `MMM`.

### F.29.2. EXPLICAR (TABELA_ÁREA) [#](#PGOVEREXPLAIN-RANGE-TABLE)

A opção `RANGE_TABLE` exibe informações da árvore de planos especificamente relacionadas à tabela de intervalo da consulta. As entradas da tabela de intervalo correspondem aproximadamente aos itens que aparecem na cláusula `FROM` da consulta, mas com várias exceções. Por exemplo, subconsultas que são propostas como desnecessárias podem ser excluídas completamente da tabela de intervalo, enquanto a expansão de herança adiciona entradas da tabela de intervalo para tabelas filhas que não são nomeadas diretamente na consulta.

As entradas da tabela de intervalo são geralmente referenciadas no plano da consulta por um índice de tabela de intervalo, ou RTI. Os nós do plano que fazem referência a um ou mais RTIs serão rotulados conforme necessário, usando um dos seguintes campos: `Scan RTI`, `Nominal RTI`, `Exclude Relation RTI`, `Append RTIs`.

Além disso, a consulta como um todo pode manter listas de índices de tabela de intervalo que são necessários para vários propósitos. Essas listas serão exibidas uma vez por consulta, rotuladas conforme apropriado como `Unprunable RTIs` ou `Result RTIs`. No modo de texto, esses campos são exibidos apenas se forem conjuntos não vazios.

Por fim, mas o mais importante, a opção `RANGE_TABLE` exibirá um dump da tabela completa da faixa da consulta. Cada entrada da tabela de faixa é rotulada com o índice apropriado da tabela de faixa, o tipo de entrada da tabela de faixa (por exemplo, `relation`, `subquery` ou `join`), seguido pelos conteúdos dos vários campos de entrada da tabela de faixa que normalmente não fazem parte da saída do `EXPLAIN`. Alguns desses campos são exibidos apenas para certos tipos de entradas da tabela de faixa. Por exemplo, `Eref` é exibido para todos os tipos de entradas da tabela de faixa, mas `CTE Name` é exibido apenas para entradas da tabela de faixa do tipo `cte`.

Para mais informações sobre as entradas da tabela de classificação, consulte a definição de `RangeTblEntry` em `nodes/parsenodes.h`.

### F.29.3. Autor [#](#PGOVEREXPLAIN-AUTHOR)

Robert Haas `<rhaas@postgresql.org>`
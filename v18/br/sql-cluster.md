## CLUSTER

CLUSTER — agrupar uma tabela de acordo com um índice

## Sinopse

```
CLUSTER [ ( option [, ...] ) ] [ table_name [ USING index_name ] ]

where option can be one of:

    VERBOSE [ boolean ]
```

## Descrição

`CLUSTER` instrui o PostgreSQL a agrupar a tabela especificada por *`table_name`* com base no índice especificado por *`index_name`*. O índice deve ter sido definido anteriormente em *`table_name`*.

Quando uma tabela é agrupada, ela é reorganizada fisicamente com base nas informações do índice. O agrupamento é uma operação única: quando a tabela é posteriormente atualizada, as alterações não são agrupadas. Isso significa que não há tentativa de armazenar novas ou atualizadas linhas de acordo com seu pedido de índice. (Se alguém desejar, pode periodicamente reagrupar, emitindo o comando novamente. Além disso, definir o parâmetro de armazenamento `fillfactor` da tabela para menos de 100% pode ajudar a preservar a ordem do agrupamento durante as atualizações, uma vez que as linhas atualizadas são mantidas na mesma página se houver espaço suficiente disponível lá.)

Quando uma tabela é agrupada, o PostgreSQL lembra-se do índice pelo qual foi agrupada. O formulário `CLUSTER table_name` reagrupa a tabela usando o mesmo índice que antes. Você também pode usar os formulários `CLUSTER` ou `SET WITHOUT CLUSTER` do [`ALTER TABLE`](sql-altertable.md "ALTER TABLE") para definir o índice a ser usado para operações futuras de agrupamento, ou para limpar qualquer configuração anterior.

`CLUSTER` sem um *`table_name`* reclusteriza todas as tabelas previamente agrupadas no banco de dados atual para as quais o usuário que está fazendo a chamada tenha privilégios. Essa forma de `CLUSTER` não pode ser executada dentro de um bloco de transação.

Quando uma tabela está sendo agrupada, um bloqueio `ACCESS EXCLUSIVE` é adquirido sobre ela. Isso impede que outras operações de banco de dados (leitura e escrita) operem na tabela até que o `CLUSTER` esteja concluído.

## Parâmetros

*`table_name`*: O nome (possivelmente qualificado por esquema) de uma tabela.

*`index_name`*: O nome de um índice.

`VERBOSE`: Imprime um relatório de progresso à medida que cada tabela é agrupada no nível `INFO`.

*`boolean`*: Especifica se a opção selecionada deve ser ativada ou desativada. Você pode escrever `TRUE`, `ON` ou `1` para ativar a opção, e `FALSE`, `OFF` ou `0` para desativá-la. O valor *`boolean`* também pode ser omitido, no qual caso `TRUE` é assumido.

## Notas

Para agrupar uma tabela, é necessário ter o privilégio `MAINTAIN` na tabela.

Nos casos em que você está acessando linhas únicas aleatoriamente dentro de uma tabela, a ordem real dos dados na tabela não é importante. No entanto, se você tende a acessar alguns dados mais do que outros, e há um índice que os agrupa juntos, você se beneficiará ao usar `CLUSTER`. Se você está solicitando uma faixa de valores indexados de uma tabela ou um único valor indexado que tem várias linhas que correspondem, `CLUSTER` ajudará porque, uma vez que o índice identifica a página da tabela para a primeira linha que corresponde, todas as outras linhas que correspondem provavelmente já estão na mesma página da tabela, e assim você economiza acessos de disco e acelera a consulta.

`CLUSTER` pode reordenar a tabela usando uma varredura de índice no índice especificado, ou (se o índice for uma árvore b) uma varredura sequencial seguida de ordenação. Ele tentará escolher o método que será mais rápido, com base nos parâmetros de custo do planejador e nas informações estatísticas disponíveis.

Enquanto o `CLUSTER` está em execução, o [search_path](runtime-config-client.md#GUC-SEARCH-PATH) é temporariamente alterado para `pg_catalog, pg_temp`.

Quando um varredura de índice é usada, uma cópia temporária da tabela é criada que contém os dados da tabela na ordem do índice. Cópias temporárias de cada índice na tabela também são criadas. Portanto, você precisa de espaço livre no disco, pelo menos igual à soma do tamanho da tabela e dos tamanhos dos índices.

Quando um varredura e ordenação sequencial são usados, um arquivo temporário de ordenação também é criado, de modo que o requisito temporário máximo de espaço seja o dobro do tamanho da tabela, mais os tamanhos dos índices. Esse método é frequentemente mais rápido do que o método de varredura de índice, mas se o requisito de espaço em disco for intolerável, você pode desabilitar essa opção, definindo temporariamente [enable_sort][(runtime-config-query.md#GUC-ENABLE-SORT)] como `off`.

É aconselhável definir [maintenance_work_mem][(runtime-config-resource.md#GUC-MAINTENANCE-WORK-MEM)] para um valor razoavelmente grande (mas não mais do que a quantidade de RAM que você pode dedicar à operação `CLUSTER` antes do agrupamento.

Como o planejador registra estatísticas sobre a ordenação de tabelas, é aconselhável executar `ANALYZE` (sql-analyze.md "ANALYZE") na tabela recém-agrupada. Caso contrário, o planejador pode fazer escolhas ruins em relação aos planos de consulta.

Como o `CLUSTER` lembra quais índices estão agrupados, é possível agrupar as tabelas que se deseja agrupar manualmente na primeira vez, e, em seguida, configurar um script de manutenção periódico que execute o `CLUSTER` sem quaisquer parâmetros, para que as tabelas desejadas sejam reclasificadas periodicamente.

Cada backend que executa `CLUSTER` informará seu progresso na visualização `pg_stat_progress_cluster`. Consulte [Seção 27.4.2][(progress-reporting.md#CLUSTER-PROGRESS-REPORTING "27.4.2. CLUSTER Progress Reporting")] para obter detalhes.

Agrupar uma tabela particionada agrupa cada uma de suas partições usando a partição do índice particionado especificado. Ao agrupar uma tabela particionada, o índice não pode ser omitido. `CLUSTER` em uma tabela particionada não pode ser executado dentro de um bloco de transação.

## Exemplos

Agrupe a tabela `employees` com base em seu índice `employees_ind`:

```
CLUSTER employees USING employees_ind;
```

Agrupe a tabela `employees` usando o mesmo índice que foi usado anteriormente:

```
CLUSTER employees;
```

Agrupe todas as tabelas no banco de dados que já foram agrupadas:

```
CLUSTER;
```

## Compatibilidade

Não há nenhuma declaração `CLUSTER` no padrão SQL.

A sintaxe a seguir foi usada antes do PostgreSQL 17 e ainda é suportada:

```
CLUSTER [ VERBOSE ] [ table_name [ USING index_name ] ]
```

A sintaxe a seguir foi usada antes do PostgreSQL 8.3 e ainda é suportada:

```
CLUSTER index_name ON table_name
```

## Veja também

[clusterdb](app-clusterdb.md "clusterdb"), [Seção 27.4.2](progress-reporting.md#CLUSTER-PROGRESS-REPORTING "27.4.2. CLUSTER Progress Reporting")
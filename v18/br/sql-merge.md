## MERGUE

MERGE — inserir, atualizar ou excluir condicionalmente linhas de uma tabela

## Sinopse

```
[ WITH with_query [, ...] ]
MERGE INTO [ ONLY ] target_table_name [ * ] [ [ AS ] target_alias ]
    USING data_source ON join_condition
    when_clause [...]
    [ RETURNING [ WITH ( { OLD | NEW } AS output_alias [, ...] ) ]
                { * | output_expression [ [ AS ] output_name ] } [, ...] ]

where data_source is:

    { [ ONLY ] source_table_name [ * ] | ( source_query ) } [ [ AS ] source_alias ]

and when_clause is:

    { WHEN MATCHED [ AND condition ] THEN { merge_update | merge_delete | DO NOTHING } |
      WHEN NOT MATCHED BY SOURCE [ AND condition ] THEN { merge_update | merge_delete | DO NOTHING } |
      WHEN NOT MATCHED [ BY TARGET ] [ AND condition ] THEN { merge_insert | DO NOTHING } }

and merge_insert is:

    INSERT [( column_name [, ...] )]
        [ OVERRIDING { SYSTEM | USER } VALUE ]
        { VALUES ( { expression | DEFAULT } [, ...] ) | DEFAULT VALUES }

and merge_update is:

    UPDATE SET { column_name = { expression | DEFAULT } |
                 ( column_name [, ...] ) = [ ROW ] ( { expression | DEFAULT } [, ...] ) |
                 ( column_name [, ...] ) = ( sub-SELECT )
               } [, ...]

and merge_delete is:

    DELETE
```

## Descrição

`MERGE` realiza ações que modificam linhas na tabela de destino identificadas como *`target_table_name`*, usando o *`data_source`*. `MERGE` fornece uma única declaração SQL que pode condicionalmente `INSERT`, `UPDATE` ou `DELETE` linhas, uma tarefa que, de outra forma, exigiria múltiplas declarações em linguagem procedural.

Primeiro, o comando `MERGE` realiza uma junção de *`data_source`* para a tabela de destino, produzindo zero ou mais linhas de mudança candidatas. Para cada linha de mudança candidata, o status de `MATCHED`, `NOT MATCHED BY SOURCE` ou `NOT MATCHED [BY TARGET]` é definido apenas uma vez, após o que as cláusulas `WHEN` são avaliadas na ordem especificada. Para cada linha de mudança candidata, a primeira cláusula a ser avaliada como verdadeira é executada. Não mais de uma cláusula `WHEN` é executada para qualquer linha de mudança candidata.

As ações `MERGE` têm o mesmo efeito que os comandos regulares `UPDATE`, `INSERT` ou `DELETE` dos mesmos nomes. A sintaxe desses comandos é diferente, notavelmente, não há cláusula `WHERE` e nenhum nome de tabela é especificado. Todas as ações referem-se à tabela alvo, embora modificações em outras tabelas possam ser feitas usando gatilhos.

Quando `DO NOTHING` é especificado, a linha de origem é ignorada. Como as ações são avaliadas em seu respectivo ordem, `DO NOTHING` pode ser útil para ignorar linhas de origem que não são interessantes antes de uma manipulação mais detalhada.

A cláusula opcional `RETURNING` faz com que `MERGE` calcule e retorne(m) valores com base em cada linha inserida, atualizada ou excluída. Qualquer expressão que utilize as colunas da tabela de origem ou de destino, ou a função [`merge_action()`(functions-merge-support.md#MERGE-ACTION) pode ser calculada. Por padrão, quando uma ação `INSERT` ou `UPDATE` é realizada, os novos valores das colunas da tabela de destino são usados, e quando uma `DELETE` é realizada, os valores antigos das colunas da tabela de destino são usados, mas também é possível solicitar explicitamente valores antigos e novos. A sintaxe da lista `RETURNING` é idêntica à da lista de saída de `SELECT`.

Não há privilégio separado `MERGE`. Se você especificar uma ação de atualização, você deve ter o privilégio `UPDATE` na(s) coluna(s) da tabela de destino que são referenciadas na cláusula `SET`. Se você especificar uma ação de inserção, você deve ter o privilégio `INSERT` na tabela de destino. Se você especificar uma ação de exclusão, você deve ter o privilégio `DELETE` na tabela de destino. Se você especificar uma ação de `DO NOTHING`, você deve ter o privilégio `SELECT` em pelo menos uma coluna da tabela de destino. Você também precisará do privilégio `SELECT` em qualquer coluna(s) do *`data_source`* e da tabela de destino referenciada em qualquer `condition` (incluindo `join_condition`) ou `expression`. Os privilégios são testados uma vez no início da declaração e verificados se particular `WHEN` cláusulas são executadas ou

`MERGE` não é suportado se a tabela de destino for uma visão materializada, uma tabela estrangeira ou se tiver quaisquer regras definidas nela.

## Parâmetros

*`with_query`*: A cláusula `WITH` permite especificar uma ou mais subconsultas que podem ser referenciadas pelo nome na consulta `MERGE`. Veja [Seção 7.8](queries-with.md "7.8. WITH Queries (Common Table Expressions)) e [SELECT](sql-select.md "SELECT") para detalhes. Observe que `WITH RECURSIVE` não é suportada por `MERGE`.

*`target_table_name`*: O nome (opcionalmente qualificado por esquema) da tabela ou visão de destino a ser integrada. Se `ONLY` é especificado antes de um nome de tabela, as linhas correspondentes são atualizadas ou excluídas apenas na tabela nomeada. Se `ONLY` não é especificado, as linhas correspondentes também são atualizadas ou excluídas em quaisquer tabelas que herdem da tabela nomeada. Opcionalmente, `*` pode ser especificado após o nome da tabela para indicar explicitamente que as tabelas descendentes são incluídas. As palavras-chave `ONLY` e a opção `*` não afetam as ações de inserção, que sempre inserem apenas na tabela nomeada.

Se *`target_table_name`* for uma visão, ela deve ser automaticamente atualizável sem `INSTEAD OF` gatilhos, ou deve ter `INSTEAD OF` gatilhos para cada tipo de ação (`INSERT`, `UPDATE` e `DELETE`) especificados nas cláusulas `WHEN`. Visões com regras não são suportadas.

*`target_alias`*: Um nome alternativo para a tabela-alvo. Quando um alias é fornecido, ele oculta completamente o nome real da tabela. Por exemplo, dado `MERGE INTO foo AS f`, o restante da declaração `MERGE` deve se referir a esta tabela como `f` e não `foo`.

*`source_table_name`*: O nome (opcionalmente qualificado por esquema) da tabela de origem, visão ou tabela de transição. Se `ONLY` for especificado antes do nome da tabela, as linhas correspondentes são incluídas apenas da tabela nomeada. Se `ONLY` não for especificado, as linhas correspondentes também são incluídas de quaisquer tabelas que herdem da tabela nomeada. Opcionalmente, `*` pode ser especificado após o nome da tabela para indicar explicitamente que as tabelas descendentes são incluídas.

*`source_query`*: Uma consulta (declaração `SELECT` ou declaração `VALUES`) que fornece as linhas a serem mescladas na tabela de destino. Consulte a declaração [SELECT](sql-select.md "SELECT") ou declaração [VALUES](sql-values.md "VALUES") para uma descrição da sintaxe.

*`source_alias`*: Um nome alternativo para a fonte de dados. Quando um alias é fornecido, ele oculta completamente o nome real da tabela ou o fato de que uma consulta foi emitida.

*`join_condition`*: *`join_condition`* é uma expressão que resulta em um valor do tipo `boolean` (semelhante a uma cláusula `WHERE`) que especifica quais linhas no *`data_source`* correspondem a linhas na tabela de destino.

### Aviso

Apenas as colunas da tabela-alvo que tentam corresponder a *`data_source`* linhas devem aparecer em *`join_condition`*. As subexpressões *`join_condition`* que fazem referência apenas às colunas da tabela-alvo podem afetar a ação a ser tomada, muitas vezes de maneiras surpreendentes.

Se ambas as cláusulas `WHEN NOT MATCHED BY SOURCE` e `WHEN NOT MATCHED [BY TARGET]` forem especificadas, o comando `MERGE` realizará uma junção `FULL` entre *`data_source`* e a tabela de destino. Para que isso funcione, pelo menos uma subexpressão *`join_condition`* deve usar um operador que possa suportar uma junção hash, ou todas as subexpressões devem usar operadores que possam suportar uma junção de fusão.

*`when_clause`*: Pelo menos uma cláusula `WHEN` é necessária.

A cláusula `WHEN` pode especificar `WHEN MATCHED`, `WHEN NOT MATCHED BY SOURCE` ou `WHEN NOT MATCHED [BY TARGET]`. Observe que o padrão SQL define apenas `WHEN MATCHED` e `WHEN NOT MATCHED` (que é definido como não havendo uma linha alvo correspondente). `WHEN NOT MATCHED BY SOURCE` é uma extensão do padrão SQL, assim como a opção de anexar `BY TARGET` a `WHEN NOT MATCHED`, para tornar seu significado mais explícito.

Se a cláusula `WHEN` especificar `WHEN MATCHED` e a linha de mudança do candidato corresponder a uma linha no *`data_source`* a uma linha na tabela de destino, a cláusula `WHEN` é executada se o *`condition`* estiver ausente ou se avaliar a `true`.

Se a cláusula `WHEN` especificar `WHEN NOT MATCHED BY SOURCE` e a linha de alteração do candidato representar uma linha na tabela de destino que não corresponde a uma linha no *`data_source`*, a cláusula `WHEN` é executada se o *`condition`* estiver ausente ou seja avaliado como `true`.

Se a cláusula `WHEN` especificar `WHEN NOT MATCHED [BY TARGET]` e a linha de mudança do candidato representar uma linha no *`data_source`* que não corresponde a uma linha na tabela de destino, a cláusula `WHEN` é executada se o *`condition`* estiver ausente ou se avaliar a `true`.

*`condition`*: Uma expressão que retorna um valor do tipo `boolean`. Se essa expressão para uma cláusula `WHEN` retornar `true`, então a ação para essa cláusula é executada para essa linha.

Uma condição em uma cláusula `WHEN MATCHED` pode se referir a colunas tanto nas relações de origem quanto na relação de destino. Uma condição em uma cláusula `WHEN NOT MATCHED BY SOURCE` pode se referir apenas a colunas da relação de destino, uma vez que, por definição, não há uma linha de origem correspondente. Uma condição em uma cláusula `WHEN NOT MATCHED [BY TARGET]` pode se referir apenas a colunas da relação de origem, uma vez que, por definição, não há uma linha de destino correspondente. Apenas os atributos do sistema da tabela de destino são acessíveis.

*`merge_insert`*: A especificação de uma ação `INSERT` que insere uma linha na tabela de destino. Os nomes das colunas de destino podem ser listados em qualquer ordem. Se não for fornecida nenhuma lista de nomes de colunas, o padrão é todas as colunas da tabela em sua ordem declarada.

Cada coluna que não esteja presente na lista explícita ou implícita de colunas será preenchida com um valor padrão, seja seu valor padrão declarado ou nulo, se não houver nenhum.

Se a tabela de destino for uma tabela particionada, cada linha é encaminhada para a partição apropriada e inserida nela. Se a tabela de destino for uma partição, ocorrerá um erro se qualquer linha de entrada violar a restrição de partição.

Os nomes das colunas não podem ser especificados mais de uma vez. As ações `INSERT` não podem conter subseleções.

Apenas uma cláusula `VALUES` pode ser especificada. A cláusula `VALUES` só pode se referir a colunas da relação de origem, uma vez que, por definição, não há uma linha alvo correspondente.

*`merge_update`*: A especificação de uma ação `UPDATE` que atualiza a linha atual da tabela de destino. Os nomes das colunas não podem ser especificados mais de uma vez.

Nem o nome de uma tabela nem uma cláusula `WHERE` são permitidas.

*`merge_delete`*: Especifica uma ação `DELETE` que exclui a linha atual da tabela de destino. Não inclua o nome da tabela ou quaisquer outras cláusulas, como você normalmente faria com um comando [DELETE](sql-delete.md "DELETE").

*`column_name`*: O nome de uma coluna na tabela de destino. O nome da coluna pode ser qualificado com um nome de subcampo ou índice de matriz, se necessário. (Inserir apenas em alguns campos de uma coluna composta deixa os outros campos nulos.) Não inclua o nome da tabela na especificação de uma coluna de destino.

`OVERRIDING SYSTEM VALUE`: Sem essa cláusula, é um erro especificar um valor explícito (diferente de `DEFAULT`) para uma coluna de identidade definida como `GENERATED ALWAYS`. Essa cláusula anula essa restrição.

`OVERRIDING USER VALUE`: Se esta cláusula for especificada, quaisquer valores fornecidos para as colunas de identidade definidas como `GENERATED BY DEFAULT` serão ignorados e os valores gerados pela sequência padrão serão aplicados.

`DEFAULT VALUES`: Todas as colunas serão preenchidas com seus valores padrão. (Uma cláusula `OVERRIDING` não é permitida neste formulário.)

*`expression`*: Uma expressão para atribuir à coluna. Se usada em uma cláusula `WHEN MATCHED`, a expressão pode usar valores da linha original na tabela de destino e valores da linha *`data_source`*. Se usada em uma cláusula `WHEN NOT MATCHED BY SOURCE`, a expressão só pode usar valores da linha original na tabela de destino. Se usada em uma cláusula `WHEN NOT MATCHED [BY TARGET]`, a expressão só pode usar valores da linha *`data_source`*.

`DEFAULT`: Defina a coluna para seu valor padrão (que será `NULL` se não tiver sido atribuído um valor padrão específico para ela).

*`sub-SELECT`*: Uma subconsulta `SELECT` que produz tantas colunas de saída quanto estão listadas na lista de colunas entre parênteses que a precedem. A subconsulta não deve produzir mais de uma linha quando executada. Se produzir uma linha, seus valores de coluna são atribuídos às colunas de destino; se não produzir nenhuma linha, valores NULL são atribuídos às colunas de destino. Se usada em uma cláusula `WHEN MATCHED`, a subconsulta pode referir-se a valores da linha original na tabela de destino e valores do *`data_source`*. Se usada em uma cláusula `WHEN NOT MATCHED BY SOURCE`, a subconsulta pode apenas referir-se a valores da linha original na tabela de destino.

*`output_alias`*: Um nome alternativo opcional para as linhas `OLD` ou `NEW` na lista `RETURNING`.

Por padrão, os valores antigos da tabela de destino podem ser retornados escrevendo `OLD.column_name` ou `OLD.*`, e novos valores podem ser retornados escrevendo `NEW.column_name` ou `NEW.*`. Quando um alias é fornecido, esses nomes são ocultados e as linhas antigas ou novas devem ser referenciadas usando o alias. Por exemplo, `RETURNING WITH (OLD AS o, NEW AS n) o.*, n.*`.

*`output_expression`*: Uma expressão que será calculada e devolvida pelo comando `MERGE` após cada linha ser alterada (se inserida, atualizada ou excluída). A expressão pode usar qualquer coluna das tabelas de origem ou destino, ou a função [`merge_action()`(functions-merge-support.md#MERGE-ACTION) para retornar informações adicionais sobre a ação executada.

Escrevendo `*`, você obterá todas as colunas da tabela de origem, seguidas de todas as colunas da tabela de destino. Muitas vezes, isso resulta em muita duplicação, pois é comum que as tabelas de origem e destino tenham muitas das mesmas colunas. Isso pode ser evitado qualificando o `*` com o nome ou alias da tabela de origem ou de destino.

Um nome de coluna ou `*` também pode ser qualificado usando `OLD` ou `NEW`, ou o *`output_alias`* correspondente para `OLD` ou `NEW`, para retornar valores antigos ou novos da tabela de destino. Um nome de coluna não qualificado da tabela de destino, ou um nome de coluna ou `*` qualificado usando o nome ou alias da tabela de destino, retornará novos valores para as ações `INSERT` e `UPDATE`, e valores antigos para as ações `DELETE`.

*`output_name`*: Um nome a ser usado para uma coluna retornada.

## Saídas

Após a conclusão bem-sucedida, um comando `MERGE` retorna uma tag de comando na forma de

```
MERGE total_count
```

O *`total_count`* é o número total de linhas alteradas (se inseridas, atualizadas ou excluídas). Se *`total_count`* for 0, nenhuma linha foi alterada de qualquer forma.

Se o comando `MERGE` contiver uma cláusula `RETURNING`, o resultado será semelhante ao de uma declaração `SELECT` que contém as colunas e valores definidos na lista `RETURNING`, calculados sobre a(s) linha(s) inserida(s), atualizada(s) ou excluída(s) pelo comando.

## Notas

Os seguintes passos ocorrem durante a execução do `MERGE`.

1. Realize quaisquer gatilhos `BEFORE STATEMENT` para todas as ações especificadas, independentemente de suas cláusulas `WHEN` corresponderem ou não.
2. Realize uma junção da tabela de origem para a tabela de destino. A consulta resultante será otimizada normalmente e produzirá um conjunto de linhas de mudança candidatas. Para cada linha de mudança candidata,

1. Avalie se cada linha é `MATCHED`, `NOT MATCHED BY SOURCE` ou `NOT MATCHED [BY TARGET]`.
2. Teste cada condição `WHEN` na ordem especificada até que uma retorne verdadeira.
3. Quando uma condição retornar verdadeira, realize as ações a seguir:

1. Realize quaisquer gatilhos `BEFORE ROW` que acionem para o tipo de evento da ação.
2. Realize a ação especificada, invocando quaisquer restrições de verificação na tabela alvo.
3. Realize quaisquer gatilhos `AFTER ROW` que acionem para o tipo de evento da ação.

Se a relação alvo for uma visão com gatilhos `INSTEAD OF ROW` para o tipo de evento da ação, eles são usados para realizar a ação em vez disso.
3. Realize quaisquer gatilhos `AFTER STATEMENT` para ações especificadas, independentemente de realmente ocorrerem. Isso é semelhante ao comportamento de uma declaração `UPDATE` que não modifica nenhuma linha.

Em resumo, os gatilhos de declaração para um tipo de evento (digamos, `INSERT`) serão disparados sempre que *especificarmos* uma ação desse tipo. Em contraste, os gatilhos de nível de linha serão disparados apenas para o tipo específico de evento que está sendo *executado*. Assim, um comando `MERGE` pode disparar gatilhos de declaração tanto para `UPDATE` quanto para `INSERT`, mesmo que apenas os gatilhos de linha `UPDATE` tenham sido disparados.

Você deve garantir que a junção produza no máximo uma linha de mudança de candidato para cada linha alvo. Em outras palavras, uma linha alvo não deve se unir a mais de uma linha de fonte de dados. Se isso ocorrer, então apenas uma das linhas de mudança de candidato será usada para modificar a linha alvo; tentativas posteriores de modificar a linha causarão um erro. Isso também pode ocorrer se os gatilhos de linha fizerem alterações na tabela alvo e as linhas assim modificadas sejam posteriormente também modificadas por `MERGE`. Se a ação repetida for um `INSERT`, isso causará uma violação de unicidade, enquanto um `UPDATE` ou `DELETE` repetido causará uma violação de cardinalidade; o comportamento deste último é exigido pelo padrão SQL. Isso difere do comportamento histórico do PostgreSQL de junções nas declarações de `UPDATE` e `DELETE`, onde as segundas e subsequentes tentativas de modificar a mesma linha são simplesmente ignoradas.

Se uma cláusula `WHEN` omitir uma subcláusula `AND`, ela se torna a cláusula final alcançável desse tipo (`MATCHED`, `NOT MATCHED BY SOURCE` ou `NOT MATCHED [BY TARGET]`). Se uma cláusula `WHEN` posterior desse tipo for especificada, ela seria probatamente inacessível e um erro será gerado. Se nenhuma cláusula final alcançável de qualquer tipo for especificada, é possível que nenhuma ação seja realizada para uma linha de alteração candidata.

A ordem em que as linhas são geradas a partir da fonte de dados é indeterminada por padrão. Um *`source_query`* pode ser usado para especificar uma ordem consistente, se necessário, o que pode ser necessário para evitar deadlocks entre transações concorrentes.

Quando o `MERGE` é executado simultaneamente com outros comandos que modificam a tabela de destino, as regras usuais de isolamento de transação se aplicam; consulte [Seção 13.2][(transaction-iso.md "13.2. Transaction Isolation")] para uma explicação sobre o comportamento em cada nível de isolamento. Você também pode desejar considerar o uso do `INSERT ... ON CONFLICT` como uma declaração alternativa que oferece a capacidade de executar um `UPDATE` se ocorrer uma `INSERT` concorrente. Há uma variedade de diferenças e restrições entre os dois tipos de declarações e eles não são intercambiáveis.

## Exemplos

Realize a manutenção em `customer_accounts` com base no novo `recent_transactions`.

```
MERGE INTO customer_account ca
USING recent_transactions t
ON t.customer_id = ca.customer_id
WHEN MATCHED THEN
  UPDATE SET balance = balance + transaction_value
WHEN NOT MATCHED THEN
  INSERT (customer_id, balance)
  VALUES (t.customer_id, t.transaction_value);
```

Tente inserir um novo item de estoque juntamente com a quantidade de estoque. Se o item já existir, atualize, em vez disso, o número de estoque do item existente. Não permita entradas que tenham estoque zero. Retorne os detalhes de todas as alterações feitas.

```
MERGE INTO wines w
USING wine_stock_changes s
ON s.winename = w.winename
WHEN NOT MATCHED AND s.stock_delta > 0 THEN
  INSERT VALUES(s.winename, s.stock_delta)
WHEN MATCHED AND w.stock + s.stock_delta > 0 THEN
  UPDATE SET stock = w.stock + s.stock_delta
WHEN MATCHED THEN
  DELETE
RETURNING merge_action(), w.winename, old.stock AS old_stock, new.stock AS new_stock;
```

A tabela `wine_stock_changes` pode ser, por exemplo, uma tabela temporária recentemente carregada no banco de dados.

Atualize `wines` com base em uma nova lista de vinhos, inserindo linhas para qualquer novo estoque, atualizando as entradas de estoque modificadas e excluindo quaisquer vinhos que não estejam presentes na nova lista.

```
MERGE INTO wines w
USING new_wine_list s
ON s.winename = w.winename
WHEN NOT MATCHED BY TARGET THEN
  INSERT VALUES(s.winename, s.stock)
WHEN MATCHED AND w.stock != s.stock THEN
  UPDATE SET stock = s.stock
WHEN NOT MATCHED BY SOURCE THEN
  DELETE;
```

## Compatibilidade

Este comando está de acordo com o padrão SQL.

As cláusulas `WITH`, `BY SOURCE` e `BY TARGET` para a ação `WHEN NOT MATCHED`, `DO NOTHING` e a cláusula `RETURNING` são extensões do padrão SQL.
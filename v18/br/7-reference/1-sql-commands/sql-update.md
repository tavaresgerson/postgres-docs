## ATUALIZAÇÃO

ATUALIZAÇÃO — atualizar linhas de uma tabela

## Sinopse

```
[ WITH [ RECURSIVE ] with_query [, ...] ]
UPDATE [ ONLY ] table_name [ * ] [ [ AS ] alias ]
    SET { column_name = { expression | DEFAULT } |
          ( column_name [, ...] ) = [ ROW ] ( { expression | DEFAULT } [, ...] ) |
          ( column_name [, ...] ) = ( sub-SELECT )
        } [, ...]
    [ FROM from_item [, ...] ]
    [ WHERE condition | WHERE CURRENT OF cursor_name ]
    [ RETURNING [ WITH ( { OLD | NEW } AS output_alias [, ...] ) ]
                { * | output_expression [ [ AS ] output_name ] } [, ...] ]
```

## Descrição

`UPDATE` altera os valores das colunas especificadas em todas as linhas que satisfazem a condição. Apenas as colunas que devem ser modificadas devem ser mencionadas na cláusula `SET`; as colunas que não são explicitamente modificadas retêm seus valores anteriores.

Existem duas maneiras de modificar uma tabela usando informações contidas em outras tabelas no banco de dados: usando subseleções ou especificando tabelas adicionais na cláusula `FROM`. A técnica mais apropriada depende das circunstâncias específicas.

A cláusula opcional `RETURNING` faz com que `UPDATE` calcule e retorne(m) valores com base em cada linha realmente atualizada. Qualquer expressão que utilize as colunas da tabela e/ou colunas de outras tabelas mencionadas em `FROM` pode ser calculada. Por padrão, os novos (valores pós-atualização) das colunas da tabela são usados, mas também é possível solicitar os valores antigos (pré-atualização). A sintaxe da lista `RETURNING` é idêntica à da lista de saída de `SELECT`.

Você deve ter o privilégio `UPDATE` na tabela, ou pelo menos nas colunas listadas que devem ser atualizadas. Você também deve ter o privilégio `SELECT` em qualquer coluna cujos valores são lidos no *`expressions`* ou *`condition`*.

## Parâmetros

*`with_query`*: A cláusula `WITH` permite que você especifique uma ou mais subconsultas que podem ser referenciadas pelo nome na consulta `UPDATE`. Veja [Seção 7.8](queries-with.md "7.8. WITH Queries (Common Table Expressions) e [SELECT](sql-select.md "SELECT") para detalhes.

*`table_name`*: O nome (opcionalmente qualificado por esquema) da tabela a ser atualizada. Se `ONLY` for especificado antes do nome da tabela, as linhas correspondentes são atualizadas apenas na tabela nomeada. Se `ONLY` não for especificado, as linhas correspondentes também são atualizadas em quaisquer tabelas que herdem da tabela nomeada. Opcionalmente, `*` pode ser especificado após o nome da tabela para indicar explicitamente que as tabelas descendentes são incluídas.

*`alias`*: Um nome alternativo para a tabela-alvo. Quando um alias é fornecido, ele oculta completamente o nome real da tabela. Por exemplo, dado `UPDATE foo AS f`, o restante da declaração `UPDATE` deve se referir a esta tabela como `f` e não `foo`.

*`column_name`*: O nome de uma coluna na tabela denominada por *`table_name`*. O nome da coluna pode ser qualificado com um nome de subcampo ou índice de matriz, se necessário. Não inclua o nome da tabela na especificação de uma coluna alvo — por exemplo, `UPDATE table_name SET table_name.col = 1` é inválido.

*`expression`*: Uma expressão para atribuir à coluna. A expressão pode usar os valores antigos desta e de outras colunas na tabela.

`DEFAULT`: Defina a coluna para seu valor padrão (que será NULL se não tiver sido atribuído um valor padrão específico a ela). Uma coluna de identidade será definida para um novo valor gerado pela sequência associada. Para uma coluna gerada, especificar isso é permitido, mas simplesmente especifica o comportamento normal de computação da coluna a partir de sua expressão de geração.

*`sub-SELECT`*: Uma subconsulta `SELECT` que produz tantas colunas de saída quanto estão listadas na lista de colunas entre parênteses que a precedem. A subconsulta não deve produzir mais de uma linha quando executada. Se produzir uma linha, seus valores de coluna são atribuídos às colunas de destino; se não produzir nenhuma linha, valores NULL são atribuídos às colunas de destino. A subconsulta pode referir-se a valores antigos da linha atual da tabela que está sendo atualizada.

*`from_item`*: Uma expressão de tabela que permite que colunas de outras tabelas apareçam nas expressões de condição e atualização do `WHERE` e (sql-select.md#SQL-FROM "FROM Clause"). Utiliza a mesma sintaxe que a cláusula `FROM`(sql-select.md#SQL-FROM "FROM Clause") de uma declaração `SELECT`; por exemplo, pode ser especificado um alias para o nome da tabela. Não repita a tabela-alvo como *`from_item`* a menos que você pretenda uma auto-joa (neste caso, ela deve aparecer com um alias no *`from_item`*).

*`condition`*: Uma expressão que retorna um valor do tipo `boolean`. Apenas as linhas para as quais essa expressão retorna `true` serão atualizadas.

*`cursor_name`*: O nome do cursor a ser usado em uma condição `WHERE CURRENT OF`. A linha a ser atualizada é a que foi obtida mais recentemente a partir deste cursor. O cursor deve ser uma consulta que não agrupa na tabela-alvo do `UPDATE`. Observe que `WHERE CURRENT OF` não pode ser especificado junto com uma condição booleana. Consulte [DECLARE](sql-declare.md "DECLARE") para obter mais informações sobre o uso de cursors com `WHERE CURRENT OF`.

*`output_alias`*: Um nome alternativo opcional para as linhas `OLD` ou `NEW` na lista `RETURNING`.

Por padrão, os valores antigos da tabela de destino podem ser retornados escrevendo `OLD.column_name` ou `OLD.*`, e novos valores podem ser retornados escrevendo `NEW.column_name` ou `NEW.*`. Quando um alias é fornecido, esses nomes são ocultados e as linhas antigas ou novas devem ser referenciadas usando o alias. Por exemplo, `RETURNING WITH (OLD AS o, NEW AS n) o.*, n.*`.

*`output_expression`*: Uma expressão que será calculada e devolvida pelo comando `UPDATE` após cada linha ser atualizada. A expressão pode usar quaisquer nomes de colunas da tabela denominada por *`table_name`* ou tabelas listadas em `FROM`. Escreva `*` para retornar todas as colunas.

Um nome de coluna ou `*` pode ser qualificado usando `OLD` ou `NEW`, ou o *`output_alias`* correspondente para `OLD` ou `NEW`, para causar o retorno de valores antigos ou novos. Um nome de coluna não qualificado, ou `*`, ou um nome de coluna ou `*` qualificado usando o nome da tabela de destino ou alias retornará novos valores.

*`output_name`*: Um nome a ser usado para uma coluna retornada.

## Saídas

Após a conclusão bem-sucedida, um comando `UPDATE` retorna uma tag de comando na forma de

```
UPDATE count
```

O *`count`* é o número de linhas atualizadas, incluindo as linhas correspondentes cujos valores não mudaram. Observe que o número pode ser menor que o número de linhas que correspondiam ao *`condition`* quando as atualizações foram suprimidas por um gatilho *`BEFORE UPDATE`*. Se *`count`* for 0, nenhuma linha foi atualizada pela consulta (isso não é considerado um erro).

Se o comando `UPDATE` contiver uma cláusula `RETURNING`, o resultado será semelhante ao de uma declaração `SELECT` que contém as colunas e valores definidos na lista `RETURNING`, calculados sobre a(s) linha(s) atualizada(s) pelo comando.

## Notas

Quando uma cláusula `FROM` está presente, o que essencialmente acontece é que a tabela-alvo é unida às tabelas mencionadas na lista *`from_item`*, e cada linha de saída da junção representa uma operação de atualização para a tabela-alvo. Ao usar `FROM`, você deve garantir que a junção produza no máximo uma linha de saída para cada linha a ser modificada. Em outras palavras, uma linha-alvo não deve se unir a mais de uma linha da(s) outra(s) tabela(s). Se isso acontecer, então apenas uma das linhas da junção será usada para atualizar a linha-alvo, mas qual será usada não é facilmente previsível.

Devido a essa indeterminação, referenciar outras tabelas apenas dentro de subseleções é mais seguro, embora muitas vezes mais difícil de ler e mais lento do que usar uma junção.

No caso de uma tabela dividida, a atualização de uma linha pode fazer com que ela deixe de satisfazer a restrição de divisão da partição que a contém. Nesse caso, se houver alguma outra partição na árvore de partições para a qual essa linha satisfaça sua restrição de divisão, então a linha é movida para essa partição. Se não houver tal partição, ocorrerá um erro. Nos bastidores, o movimento da linha é na verdade uma operação `DELETE` e `INSERT`.

Há uma possibilidade de que um `UPDATE` ou `DELETE` concorrente na linha que está sendo movida receba um erro de falha de serialização. Suponha que a sessão 1 esteja realizando um `UPDATE` em uma chave de partição, e, enquanto isso, uma sessão concorrente 2 para a qual essa linha é visível realize uma operação de `UPDATE` ou `DELETE` nesta linha. Nesse caso, o `UPDATE` ou `DELETE` da sessão 2 detectará o movimento da linha e levantará um erro de falha de serialização (que sempre retorna com um código SQLSTATE '40001'). As aplicações podem desejar repetir a transação se isso ocorrer. No caso usual, onde a tabela não está particionada ou onde não há movimento de linha, a sessão 2 identificaria a nova versão da linha atualizada e realizaria o `UPDATE`/`DELETE` nesta nova versão da linha.

Observe que, embora as linhas possam ser movidas de partições locais para uma partição de tabela estrangeira (desde que o wrapper de dados estrangeiro suporte roteamento de tupla), elas não podem ser movidas de uma partição de tabela estrangeira para outra partição.

Uma tentativa de mover uma linha de uma partição para outra falhará se uma chave estrangeira for encontrada diretamente referenciando um antecessor da partição de origem que não é o mesmo que o antecessor mencionado na consulta `UPDATE`.

## Exemplos

Altere a palavra `Drama` para `Dramatic` na coluna `kind` da tabela `films`:

```
UPDATE films SET kind = 'Dramatic' WHERE kind = 'Drama';
```

Ajuste as entradas de temperatura e redefina a precipitação para seu valor padrão em uma linha da tabela `weather`:

```
UPDATE weather SET temp_lo = temp_lo+1, temp_hi = temp_lo+15, prcp = DEFAULT
  WHERE city = 'San Francisco' AND date = '2003-07-03';
```

Realize a mesma operação e retorne as entradas atualizadas e o valor antigo da precipitação:

```
UPDATE weather SET temp_lo = temp_lo+1, temp_hi = temp_lo+15, prcp = DEFAULT
  WHERE city = 'San Francisco' AND date = '2003-07-03'
  RETURNING temp_lo, temp_hi, prcp, old.prcp AS old_prcp;
```

Use a sintaxe alternativa de lista de colunas para fazer a mesma atualização:

```
UPDATE weather SET (temp_lo, temp_hi, prcp) = (temp_lo+1, temp_lo+15, DEFAULT)
  WHERE city = 'San Francisco' AND date = '2003-07-03';
```

Incremente o número de vendas do vendedor que gerencia a conta da Acme Corporation, usando a sintaxe da cláusula `FROM`:

```
UPDATE employees SET sales_count = sales_count + 1 FROM accounts
  WHERE accounts.name = 'Acme Corporation'
  AND employees.id = accounts.sales_person;
```

Realize a mesma operação, utilizando um subseleto na cláusula `WHERE`:

```
UPDATE employees SET sales_count = sales_count + 1 WHERE id =
  (SELECT sales_person FROM accounts WHERE name = 'Acme Corporation');
```

Atualize os nomes dos contatos em uma tabela de contas para corresponder aos vendedores atualmente atribuídos:

```
UPDATE accounts SET (contact_first_name, contact_last_name) =
    (SELECT first_name, last_name FROM employees
     WHERE employees.id = accounts.sales_person);
```

Um resultado semelhante pode ser alcançado com uma junção:

```
UPDATE accounts SET contact_first_name = first_name,
                    contact_last_name = last_name
  FROM employees WHERE employees.id = accounts.sales_person;
```

No entanto, a segunda consulta pode fornecer resultados inesperados se `employees`.`id` não for uma chave única, enquanto a primeira consulta é garantida para gerar um erro se houver múltiplos `id` correspondentes. Além disso, se não houver correspondência para uma entrada específica de `accounts`.`sales_person`, a primeira consulta definirá os campos de nome correspondentes como NULL, enquanto a segunda consulta não atualizará essa linha de forma alguma.

Atualize as estatísticas em uma tabela de resumo para corresponder aos dados atuais:

```
UPDATE summary s SET (sum_x, sum_y, avg_x, avg_y) =
    (SELECT sum(x), sum(y), avg(x), avg(y) FROM data d
     WHERE d.group_id = s.group_id);
```

Tente inserir um novo item de estoque juntamente com a quantidade de estoque. Se o item já existir, atualize, em vez disso, o número de estoque do item existente. Para fazer isso sem falhar toda a transação, use pontos de salvamento:

```
BEGIN;
-- other operations
SAVEPOINT sp1;
INSERT INTO wines VALUES('Chateau Lafite 2003', '24');
-- Assume the above fails because of a unique key violation,
-- so now we issue these commands:
ROLLBACK TO sp1;
UPDATE wines SET stock = stock + 24 WHERE winename = 'Chateau Lafite 2003';
-- continue with other operations, and eventually
COMMIT;
```

Altere a coluna `kind` da tabela `films` na linha na qual o cursor `c_films` está posicionado atualmente:

```
UPDATE films SET kind = 'Dramatic' WHERE CURRENT OF c_films;
```

As atualizações que afetam muitas linhas podem ter efeitos negativos no desempenho do sistema, como bloat de tabela, aumento do atraso de replicação e aumento da disputa por bloqueio. Nessas situações, pode fazer sentido realizar a operação em lotes menores, possivelmente com uma operação `VACUUM` na tabela entre os lotes. Embora não haja uma cláusula `LIMIT` para `UPDATE`, é possível obter um efeito semelhante através do uso de uma [Expressão de Tabela Comum](queries-with.md "7.8. WITH Queries (Common Table Expressions))] e um auto-join. Com o método padrão de acesso a tabela do PostgreSQL, um auto-join na coluna do sistema [ctid](ddl-system-columns.md#DDL-SYSTEM-COLUMNS-CTID) é muito eficiente:

```
WITH exceeded_max_retries AS (
  SELECT w.ctid FROM work_item AS w
    WHERE w.status = 'active' AND w.num_retries > 10
    ORDER BY w.retry_timestamp
    FOR UPDATE
    LIMIT 5000
)
UPDATE work_item SET status = 'failed'
  FROM exceeded_max_retries AS emr
  WHERE work_item.ctid = emr.ctid;
```

Esse comando precisará ser repetido até que não restarão mais linhas a serem atualizadas. (Esse uso de `ctid` é seguro apenas porque a consulta é executada repetidamente, evitando o problema de `ctid`s alterados.) O uso de uma cláusula `ORDER BY` permite que o comando priorize quais linhas serão atualizadas; também pode evitar impasse com outras operações de atualização se elas usarem o mesmo ordenamento. Se a disputa por bloqueio é uma preocupação, então `SKIP LOCKED` pode ser adicionado ao CTE para evitar que vários comandos atualizem a mesma linha. No entanto, então será necessário um `UPDATE` final sem `SKIP LOCKED` ou `LIMIT` para garantir que nenhuma linha correspondente tenha sido ignorada.

## Compatibilidade

Este comando está de acordo com o padrão SQL, exceto pelo fato de que as cláusulas `FROM` e `RETURNING` são extensões do PostgreSQL, assim como a capacidade de usar `WITH` com `UPDATE`.

Alguns outros sistemas de banco de dados oferecem uma opção `FROM` na qual a tabela alvo deve ser listada novamente dentro de `FROM`. Não é assim que o PostgreSQL interpreta `FROM`. Tenha cuidado ao transferir aplicativos que utilizam essa extensão.

De acordo com a norma, o valor da fonte para uma sublista entre parênteses de nomes de colunas de destino pode ser qualquer expressão com valor de linha que produza o número correto de colunas. O PostgreSQL só permite que o valor da fonte seja um [construtor de linha](sql-expressions.md#SQL-SYNTAX-ROW-CONSTRUCTORS) ou um sub-[`SELECT`]. O valor atualizado de uma coluna individual pode ser especificado como `DEFAULT` no caso do construtor de linha, mas não dentro de um sub-[`SELECT`].
## DELETA

DELETE — excluir linhas de uma tabela

## Sinopse

```
[ WITH [ RECURSIVE ] with_query [, ...] ]
DELETE FROM [ ONLY ] table_name [ * ] [ [ AS ] alias ]
    [ USING from_item [, ...] ]
    [ WHERE condition | WHERE CURRENT OF cursor_name ]
    [ RETURNING [ WITH ( { OLD | NEW } AS output_alias [, ...] ) ]
                { * | output_expression [ [ AS ] output_name ] } [, ...] ]
```

## Descrição

`DELETE` exclui linhas que satisfazem a cláusula `WHERE` da tabela especificada. Se a cláusula `WHERE` estiver ausente, o efeito é excluir todas as linhas da tabela. O resultado é uma tabela válida, mas vazia.

DICA

`TRUNCATE`](sql-truncate.md "TRUNCATE") oferece um mecanismo mais rápido para remover todas as linhas de uma tabela.

Existem duas maneiras de excluir linhas em uma tabela usando informações contidas em outras tabelas no banco de dados: usando subseleções ou especificando tabelas adicionais na cláusula `USING`. A técnica mais apropriada depende das circunstâncias específicas.

A cláusula opcional `RETURNING` faz com que `DELETE` calcule e retorne(m) valores com base em cada linha realmente excluída. Qualquer expressão que utilize as colunas da tabela e/ou colunas de outras tabelas mencionadas em `USING` pode ser calculada. A sintaxe da lista `RETURNING` é idêntica à da lista de saída de `SELECT`.

Você deve ter o privilégio `DELETE` na tabela para excluí-la, bem como o privilégio `SELECT` para qualquer tabela na cláusula `USING` ou cujos valores são lidos no *`condition`*.

## Parâmetros

*`with_query`*: A cláusula `WITH` permite que você especifique uma ou mais subconsultas que podem ser referenciadas pelo nome na consulta `DELETE`. Veja [Seção 7.8](queries-with.md "7.8. WITH Queries (Common Table Expressions)) e [SELECT](sql-select.md "SELECT") para detalhes.

*`table_name`*: O nome (opcionalmente qualificado por esquema) da tabela a partir da qual as linhas serão excluídas. Se `ONLY` for especificado antes do nome da tabela, as linhas correspondentes serão excluídas apenas da tabela nomeada. Se `ONLY` não for especificado, as linhas correspondentes também serão excluídas de quaisquer tabelas que herdem da tabela nomeada. Opcionalmente, `*` pode ser especificado após o nome da tabela para indicar explicitamente que as tabelas descendentes são incluídas.

*`alias`*: Um nome alternativo para a tabela-alvo. Quando um alias é fornecido, ele oculta completamente o nome real da tabela. Por exemplo, dado `DELETE FROM foo AS f`, o restante da declaração `DELETE` deve se referir a esta tabela como `f` e não `foo`.

*`from_item`*: Uma expressão de tabela que permite que as colunas de outras tabelas apareçam na condição do `WHERE`. Isso usa a mesma sintaxe que a cláusula [`FROM`](sql-select.md#SQL-FROM "FROM Clause") de uma declaração `SELECT`; por exemplo, pode ser especificado um alias para o nome da tabela. Não repita a tabela de destino como um *`from_item`* a menos que você queira configurar uma autojunção (neste caso, ela deve aparecer com um alias no *`from_item`*).

*`condition`*: Uma expressão que retorna um valor do tipo `boolean`. Apenas as linhas para as quais essa expressão retorna `true` serão excluídas.

*`cursor_name`*: O nome do cursor a ser usado em uma condição de `WHERE CURRENT OF`. A linha a ser excluída é a que foi obtida mais recentemente a partir deste cursor. O cursor deve ser uma consulta não agrupada na tabela de destino do `DELETE`. Observe que `WHERE CURRENT OF` não pode ser especificado junto com uma condição booleana. Consulte [DECLARE](sql-declare.md "DECLARE") para obter mais informações sobre o uso de cursors com `WHERE CURRENT OF`.

*`output_alias`*: Um nome alternativo opcional para as linhas `OLD` ou `NEW` na lista `RETURNING`.

Por padrão, os valores antigos da tabela de destino podem ser retornados escrevendo `OLD.column_name` ou `OLD.*`, e novos valores podem ser retornados escrevendo `NEW.column_name` ou `NEW.*`. Quando um alias é fornecido, esses nomes são ocultados e as linhas antigas ou novas devem ser referenciadas usando o alias. Por exemplo, `RETURNING WITH (OLD AS o, NEW AS n) o.*, n.*`.

*`output_expression`*: Uma expressão que será calculada e devolvida pelo comando `DELETE` após cada linha ser excluída. A expressão pode usar qualquer nome de coluna da tabela denominada por *`table_name`* ou tabela(s) listadas em `USING`. Escreva `*` para retornar todas as colunas.

Um nome de coluna ou `*` pode ser qualificado usando `OLD` ou `NEW`, ou o *`output_alias`* correspondente para `OLD` ou `NEW`, para causar o retorno de valores antigos ou novos. Um nome de coluna não qualificado, ou `*`, ou um nome de coluna ou `*` qualificado usando o nome da tabela de destino ou alias retornará valores antigos.

Para um simples `DELETE`, todos os novos valores serão `NULL`. No entanto, se uma regra `ON DELETE` causar que um `INSERT` ou `UPDATE` seja executado em vez disso, os novos valores podem não ser `NULL`.

*`output_name`*: Um nome a ser usado para uma coluna retornada.

## Saídas

Após a conclusão bem-sucedida, um comando `DELETE` retorna uma etiqueta de comando na forma de

```
DELETE count
```

O *`count`* é o número de linhas excluídas. Observe que o número pode ser menor que o número de linhas que correspondiam ao *`condition`* quando as exclusões foram suprimidas por um gatilho *`BEFORE DELETE`*. Se *`count`* for 0, nenhuma linha foi excluída pela consulta (isso não é considerado um erro).

Se o comando `DELETE` contiver uma cláusula `RETURNING`, o resultado será semelhante ao de uma declaração `SELECT` que contém as colunas e valores definidos na lista `RETURNING`, calculados sobre a(s) linha(s) excluída(s) pelo comando.

## Notas

O PostgreSQL permite que você faça referência a colunas de outras tabelas na condição `WHERE` especificando as outras tabelas na cláusula `USING`. Por exemplo, para excluir todos os filmes produzidos por um determinado produtor, pode-se fazer:

```
DELETE FROM films USING producers
  WHERE producer_id = producers.id AND producers.name = 'foo';
```

O que está acontecendo essencialmente aqui é uma junção entre `films` e `producers`, com todas as linhas `films` que foram bem-sucedidas sendo marcadas para exclusão. Essa sintaxe não é padrão. Uma maneira mais padrão de fazer isso é:

```
DELETE FROM films
  WHERE producer_id IN (SELECT id FROM producers WHERE name = 'foo');
```

Em alguns casos, o estilo de junção é mais fácil de escrever ou mais rápido de executar do que o estilo de subseleção.

## Exemplos

Exclua todos os filmes, exceto os musicais:

```
DELETE FROM films WHERE kind <> 'Musical';
```

Limpe a tabela `films`:

```
DELETE FROM films;
```

Exclua as tarefas concluídas, retornando todos os detalhes das linhas excluídas:

```
DELETE FROM tasks WHERE status = 'DONE' RETURNING *;
```

Exclua a linha de `tasks` na qual o cursor `c_tasks` está posicionado atualmente:

```
DELETE FROM tasks WHERE CURRENT OF c_tasks;
```

Embora não haja uma cláusula `LIMIT` para `DELETE`, é possível obter um efeito semelhante usando o mesmo método descrito na [documentação de `UPDATE`](sql-update.md#UPDATE-LIMIT):

```
WITH delete_batch AS (
  SELECT l.ctid FROM user_logs AS l
    WHERE l.status = 'archived'
    ORDER BY l.creation_date
    FOR UPDATE
    LIMIT 10000
)
DELETE FROM user_logs AS dl
  USING delete_batch AS del
  WHERE dl.ctid = del.ctid;
```

Esse uso do `ctid` é seguro apenas porque a consulta é executada repetidamente, evitando o problema de `ctid`s alterados.

## Compatibilidade

Este comando está de acordo com o padrão SQL, exceto pelo fato de que as cláusulas `USING` e `RETURNING` são extensões do PostgreSQL, assim como a capacidade de usar `WITH` com `DELETE`.

## Veja também

[TRUNCATE](sql-truncate.md "TRUNCATE")

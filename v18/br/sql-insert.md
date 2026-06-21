## INSERIR

INSERT — criar novas linhas em uma tabela

## Sinopse

```
[ WITH [ RECURSIVE ] with_query [, ...] ]
INSERT INTO table_name [ AS alias ] [ ( column_name [, ...] ) ]
    [ OVERRIDING { SYSTEM | USER } VALUE ]
    { DEFAULT VALUES | VALUES ( { expression | DEFAULT } [, ...] ) [, ...] | query }
    [ ON CONFLICT [ conflict_target ] conflict_action ]
    [ RETURNING [ WITH ( { OLD | NEW } AS output_alias [, ...] ) ]
                { * | output_expression [ [ AS ] output_name ] } [, ...] ]

where conflict_target can be one of:

    ( { index_column_name | ( index_expression ) } [ COLLATE collation ] [ opclass ] [, ...] ) [ WHERE index_predicate ]
    ON CONSTRAINT constraint_name

and conflict_action is one of:

    DO NOTHING
    DO UPDATE SET { column_name = { expression | DEFAULT } |
                    ( column_name [, ...] ) = [ ROW ] ( { expression | DEFAULT } [, ...] ) |
                    ( column_name [, ...] ) = ( sub-SELECT )
                  } [, ...]
              [ WHERE condition ]
```

## Descrição

`INSERT` insere novas linhas em uma tabela. Pode-se inserir uma ou mais linhas especificadas por expressões de valor, ou zero ou mais linhas resultantes de uma consulta.

Os nomes das colunas alvo podem ser listados em qualquer ordem. Se não for fornecida nenhuma lista de nomes de colunas, o padrão é todas as colunas da tabela em sua ordem declarada; ou os primeiros nomes de colunas *`N`*, se houver apenas colunas *`N`* fornecidas pela cláusula `VALUES` ou *`query`*. Os valores fornecidos pela cláusula `VALUES` ou *`query`* são associados à lista de colunas explícita ou implícita da esquerda para a direita.

Cada coluna que não esteja presente na lista explícita ou implícita de colunas será preenchida com um valor padrão, seja seu valor padrão declarado ou nulo, se não houver nenhum.

Se a expressão para qualquer coluna não for do tipo de dados correto, a conversão automática de tipo será realizada.

`INSERT` em tabelas que não possuem índices exclusivos não serão bloqueadas por atividades concorrentes. As tabelas com índices exclusivos podem bloquear se sessões concorrentes realizarem ações que bloqueiam ou modificam linhas que correspondem aos valores do índice exclusivo que estão sendo inseridos; os detalhes são abordados em [Seção 63.5](index-unique-checks.md "63.5. Index Uniqueness Checks") `ON CONFLICT`. `ON CONFLICT` pode ser usado para especificar uma ação alternativa para o erro de violação de restrição exclusiva ou de exclusão. (Veja a Cláusula ON CONFLICT abaixo (sql-insert.md#SQL-ON-CONFLICT "ON CONFLICT Clause").)

A cláusula opcional `RETURNING` faz com que `INSERT` calcule e retorne(m) valores com base em cada linha inserida (ou atualizada, se uma cláusula `ON CONFLICT DO UPDATE` foi usada). Isso é principalmente útil para obter valores fornecidos por padrão, como um número de sequência serial. No entanto, qualquer expressão que use as colunas da tabela é permitida. A sintaxe da lista `RETURNING` é idêntica à da lista de saída de `SELECT`. Apenas as linhas que foram inseridas ou atualizadas com sucesso serão retornadas. Por exemplo, se uma linha foi bloqueada, mas não atualizada porque uma cláusula `ON CONFLICT DO UPDATE ... WHERE` *`condition`* não foi satisfeita, a linha não será retornada.

Você deve ter o privilégio `INSERT` em uma tabela para inseri-la. Se `ON CONFLICT DO UPDATE` estiver presente, também é necessário o privilégio `UPDATE` na tabela.

Se uma lista de colunas for especificada, você só precisa do privilégio `INSERT` nas colunas listadas. Da mesma forma, quando `ON CONFLICT DO UPDATE` é especificado, você só precisa do privilégio `UPDATE` nas(s) coluna(s) que estão listadas para serem atualizadas. No entanto, todas as formas de `ON CONFLICT` também exigem o privilégio `SELECT` em qualquer coluna cujos valores são lidos. Isso inclui qualquer coluna mencionada em *`conflict_target`* (incluindo colunas referenciadas pela restrição do árbitro), e qualquer coluna mencionada em um *`ON CONFLICT DO UPDATE`* *`expression`*, ou uma cláusula *`WHERE`* *`condition`*.

O uso da cláusula `RETURNING` requer o privilégio `SELECT` em todas as colunas mencionadas em `RETURNING`. Se você usar a cláusula *`query`* para inserir linhas de uma consulta, é claro que você precisa ter o privilégio `SELECT` em qualquer tabela ou coluna usada na consulta.

## Parâmetros

### Inserindo

Esta seção abrange os parâmetros que podem ser usados apenas ao inserir novas linhas. Os parâmetros que são usados exclusivamente com a cláusula `ON CONFLICT` são descritos separadamente.

*`with_query`*: A cláusula `WITH` permite que você especifique uma ou mais subconsultas que podem ser referenciadas pelo nome na consulta `INSERT`. Veja [Seção 7.8](queries-with.md "7.8. WITH Queries (Common Table Expressions)) e [SELECT](sql-select.md "SELECT") para detalhes.

É possível que o *`query`* (declaração `SELECT`) também contenha uma cláusula `WITH`. Nesse caso, ambos os conjuntos de *`with_query`* podem ser referenciados dentro do *`query`*, mas o segundo tem precedência, uma vez que está mais intimamente aninhado.

*`table_name`*: O nome (opcionalmente qualificado por esquema) de uma tabela existente.

*`alias`*: Um nome alternativo para *`table_name`*. Quando um alias é fornecido, ele oculta completamente o nome real da tabela. Isso é particularmente útil quando o `ON CONFLICT DO UPDATE` visa uma tabela chamada `excluded`, pois, caso contrário, será considerado o nome da tabela especial que representa a linha proposta para inserção.

*`column_name`*: O nome de uma coluna na tabela denominada por *`table_name`*. O nome da coluna pode ser qualificado com um nome de subcampo ou índice de matriz, se necessário. (Inserir em apenas alguns campos de uma coluna composta deixa os outros campos nulos.) Ao referenciar uma coluna com `ON CONFLICT DO UPDATE`, não inclua o nome da tabela na especificação de uma coluna alvo. Por exemplo, `INSERT INTO table_name ... ON CONFLICT DO UPDATE SET table_name.col = 1` é inválido (isso segue o comportamento geral para `UPDATE`).

`OVERRIDING SYSTEM VALUE`: Se esta cláusula for especificada, quaisquer valores fornecidos para as colunas de identidade substituirão os valores gerados pela sequência padrão.

Para uma coluna de identidade definida como `GENERATED ALWAYS`, é um erro inserir um valor explícito (diferente de `DEFAULT`) sem especificar `OVERRIDING SYSTEM VALUE` ou `OVERRIDING USER VALUE`. (Para uma coluna de identidade definida como `GENERATED BY DEFAULT`, `OVERRIDING SYSTEM VALUE` é o comportamento normal e especificá-la não faz nada, mas o PostgreSQL permite isso como uma extensão.)

`OVERRIDING USER VALUE`: Se esta cláusula for especificada, então quaisquer valores fornecidos para as colunas de identidade serão ignorados e os valores gerados pela sequência padrão serão aplicados.

Essa cláusula é útil, por exemplo, ao copiar valores entre tabelas. Escrever `INSERT INTO tbl2 OVERRIDING USER VALUE SELECT * FROM tbl1` copiará de `tbl1` todas as colunas que não são colunas de identidade em `tbl2`, enquanto os valores para as colunas de identidade em `tbl2` serão gerados pelas sequências associadas a `tbl2`.

`DEFAULT VALUES`: Todas as colunas serão preenchidas com seus valores padrão, como se `DEFAULT` estivesse explicitamente especificado para cada coluna. (Uma cláusula `OVERRIDING` não é permitida nesta forma.)

*`expression`*: Uma expressão ou valor a ser atribuído à coluna correspondente.

`DEFAULT`: A coluna correspondente será preenchida com seu valor padrão. Uma coluna de identidade será preenchida com um novo valor gerado pela sequência associada. Para uma coluna gerada, especificar isso é permitido, mas simplesmente especifica o comportamento normal de computação da coluna a partir de sua expressão de geração.

*`query`*: Uma consulta (declaração `SELECT`) que fornece as linhas a serem inseridas. Consulte a declaração [[SELECT](sql-select.md "SELECT") para uma descrição da sintaxe.

*`output_alias`*: Um nome alternativo opcional para as linhas `OLD` ou `NEW` na lista `RETURNING`.

Por padrão, os valores antigos da tabela de destino podem ser retornados escrevendo `OLD.column_name` ou `OLD.*`, e os novos valores podem ser retornados escrevendo `NEW.column_name` ou `NEW.*`. Quando um alias é fornecido, esses nomes são ocultados e as linhas antigas ou novas devem ser referenciadas usando o alias. Por exemplo, `RETURNING WITH (OLD AS o, NEW AS n) o.*, n.*`.

*`output_expression`*: Uma expressão que deve ser calculada e devolvida pelo comando `INSERT` após cada linha ser inserida ou atualizada. A expressão pode usar qualquer nome de coluna da tabela denominada por *`table_name`*. Escreva `*` para retornar todas as colunas da(s) linha(s) inserida(s) ou atualizada(s).

Um nome de coluna ou `*` pode ser qualificado usando `OLD` ou `NEW`, ou o *`output_alias`* correspondente para `OLD` ou `NEW`, para causar o retorno de valores antigos ou novos. Um nome de coluna não qualificado, ou `*`, ou um nome de coluna ou `*` qualificado usando o nome da tabela de destino ou alias retornará novos valores.

Para um simples `INSERT`, todos os valores antigos serão `NULL`. No entanto, para um `INSERT` com uma cláusula `ON CONFLICT DO UPDATE`, os valores antigos podem não ser `NULL`.

*`output_name`*: Um nome a ser usado para uma coluna retornada.

### `ON CONFLICT` Cláusula

A cláusula opcional `ON CONFLICT` especifica uma ação alternativa para a criação de um erro de violação ou violação de restrição de exclusão exclusiva. Para cada linha individual proposta para inserção, a inserção prossegue, ou, se uma restrição *arbiter* ou índice especificado por *`conflict_target`* for violada, a *`conflict_action`* alternativa é tomada. `ON CONFLICT DO NOTHING` simplesmente evita a inserção de uma linha como sua ação alternativa. `ON CONFLICT DO UPDATE` atualiza a linha existente que conflita com a linha proposta para inserção como sua ação alternativa.

*`conflict_target`* pode realizar *inferência de índice único*. Ao realizar a inferência, consiste em uma ou mais *`index_column_name`* colunas e/ou *`index_expression`* expressões, e uma expressão opcional *`index_predicate`*. Todos os *`table_name`* índices únicos que, independentemente da ordem, contenham exatamente as colunas/expressões especificadas no *`conflict_target`* são inferidos (escolhidos) como índices arbítrios. Se um *`index_predicate`* for especificado, ele deve, como requisito adicional para a inferência, satisfazer os índices arbítrios. Note que isso significa que um índice único não parcial (um índice único sem um predicado) será inferido (e, portanto, usado por `ON CONFLICT`) se tal índice que satisfaça todos os outros critérios estiver disponível. Se uma tentativa de inferência não for bem-sucedida, um erro é gerado.

`ON CONFLICT DO UPDATE` garante um resultado atômico `INSERT` ou `UPDATE`; desde que não haja erro independente, um desses dois resultados é garantido, mesmo sob alta concorrência. Isso também é conhecido como *UPSERT* — “ATUALIZAR ou INSERIR”.

*`conflict_target`*: Especifica quais conflitos `ON CONFLICT` assume a ação alternativa, escolhendo *índices de árbitro*. Ou executa *inferência de índice único*, ou nomeia uma restrição explicitamente. Para `ON CONFLICT DO NOTHING`, é opcional especificar um *`conflict_target`*; quando omitido, os conflitos com todas as restrições (e índices únicos) utilizáveis são tratados. Para `ON CONFLICT DO UPDATE`, um *`conflict_target`* *deve* ser fornecido.

*`conflict_action`*: *`conflict_action`* especifica uma ação alternativa `ON CONFLICT`. Pode ser `DO NOTHING`, ou uma cláusula `DO UPDATE` que especifica os detalhes exatos da ação `UPDATE` a ser realizada em caso de conflito. As cláusulas `SET` e `WHERE` em `ON CONFLICT DO UPDATE` têm acesso à linha existente usando o nome da tabela (ou um alias) e à linha proposta para inserção usando a tabela especial `excluded`. O privilégio `SELECT` é necessário em qualquer coluna da tabela de destino onde as colunas correspondentes `excluded` são lidas.

Observe que os efeitos de todos os gatilhos `BEFORE INSERT` por linha são refletidos nos valores de `excluded`, uma vez que esses efeitos podem ter contribuído para a linha ser excluída da inserção.

*`index_column_name`*: O nome de uma coluna *`table_name`*. Usada para inferir índices de árbitro. Seguindo o formato `CREATE INDEX`. O privilégio `SELECT` em *`index_column_name`* é necessário.

*`index_expression`*: Semelhante a *`index_column_name`*, mas usado para inferir expressões em colunas de *`table_name`* que aparecem dentro das definições de índice (não são colunas simples). Segue o formato `CREATE INDEX`. É necessário o privilégio `SELECT` em qualquer coluna que apareça dentro de *`index_expression`*.

*`collation`*: Quando especificado, exige que o *`index_column_name`* ou *`index_expression`* correspondente use uma determinada ordenação para ser correspondido durante a inferência. Normalmente, isso é omitido, pois as ordenações geralmente não afetam se uma violação de restrição ocorre ou não. Segue o formato `CREATE INDEX`.

*`opclass`*: Quando especificado, exige que os correspondentes *`index_column_name`* ou *`index_expression`* usem uma classe de operador específica para serem correspondidos durante a inferência. Tipicamente, isso é omitido, pois a semântica de *igualdade* é frequentemente equivalente entre as classes de operadores de um tipo de qualquer maneira, ou porque é suficiente confiar que os índices únicos definidos têm a definição pertinente de igualdade. Segue o formato `CREATE INDEX`.

*`index_predicate`*: Usado para permitir a inferência de índices únicos parciais. Quaisquer índices que satisfaçam o predicado (que não precisam ser necessariamente índices parciais) podem ser inferidos. Segue o formato `CREATE INDEX`. É necessário o privilégio `SELECT` em qualquer coluna que apareça dentro de *`index_predicate`*.

*`constraint_name`*: Especifica explicitamente uma *restrição* de árbitro pelo nome, em vez de inferir uma restrição ou índice.

*`condition`*: Uma expressão que retorna um valor do tipo `boolean`. Apenas as linhas para as quais essa expressão retorna `true` serão atualizadas, embora todas as linhas sejam bloqueadas quando a ação `ON CONFLICT DO UPDATE` for realizada. Note que *`condition`* é avaliado por último, após um conflito ter sido identificado como um candidato a ser atualizado.

Observe que as restrições de exclusão não são suportadas como arbitradores com `ON CONFLICT DO UPDATE`. Em todos os casos, apenas as restrições `NOT DEFERRABLE` e índices únicos são suportados como arbitradores.

`INSERT` com uma cláusula `ON CONFLICT DO UPDATE` é uma declaração “determinística”. Isso significa que o comando não terá permissão para afetar nenhuma única linha existente mais de uma vez; um erro de violação de cardinalidade será levantado quando essa situação surgir. As linhas propostas para inserção não devem duplicar entre si em termos de atributos restritos por um índice ou restrição arbítrizável.

Observe que, atualmente, não é suportada para a cláusula `ON CONFLICT DO UPDATE` de uma `INSERT` aplicada a uma tabela particionada para atualizar a chave de partição de uma linha em conflito, de modo que seja necessário mover a linha para uma nova partição.

### DICA

É frequentemente preferível usar a inferência de índice único em vez de nomear uma restrição diretamente usando `ON CONFLICT ON CONSTRAINT` *`constraint_name`*. A inferência continuará a funcionar corretamente quando o índice subjacente for substituído por outro índice mais ou menos equivalente de maneira sobreposta, por exemplo, ao usar `CREATE UNIQUE INDEX ... CONCURRENTLY` antes de descartar o índice que está sendo substituído.

### Aviso

Enquanto o `CREATE INDEX CONCURRENTLY` ou o `REINDEX CONCURRENTLY` está rodando em um índice único, as declarações `INSERT ... ON CONFLICT` na mesma tabela podem falhar inesperadamente com uma violação única.

## Saídas

Após a conclusão bem-sucedida, um comando `INSERT` retorna uma tag de comando na forma de

```
INSERT oid count
```

O *`count` é o número de linhas inseridas ou atualizadas. *`oid`* é sempre 0 (anteriormente era o OID atribuído à linha inserida se *`count`* fosse exatamente um e a tabela de destino fosse declarada como `WITH OIDS`, e 0 caso contrário, mas a criação de uma tabela `WITH OIDS` não é mais suportada).

Se o comando `INSERT` contiver uma cláusula `RETURNING`, o resultado será semelhante ao de uma declaração `SELECT` que contém as colunas e valores definidos na lista `RETURNING`, calculados sobre a(s) linha(s) inserida(s) ou atualizada(s) pelo comando.

## Notas

Se a tabela especificada for uma tabela particionada, cada linha é encaminhada para a partição apropriada e inserida nela. Se a tabela especificada for uma partição, ocorrerá um erro se uma das linhas de entrada violar a restrição de partição.

Você também pode desejar considerar o uso de `MERGE`, pois isso permite a mistura de `INSERT`, `UPDATE` e `DELETE` em uma única declaração. Veja [MERGE](sql-merge.md "MERGE").

## Exemplos

Insira uma única linha na tabela `films`:

```
INSERT INTO films VALUES
    ('UA502', 'Bananas', 105, '1971-07-13', 'Comedy', '82 minutes');
```

Neste exemplo, a coluna `len` é omitida e, portanto, terá o valor padrão:

```
INSERT INTO films (code, title, did, date_prod, kind)
    VALUES ('T_601', 'Yojimbo', 106, '1961-06-16', 'Drama');
```

Este exemplo usa a cláusula `DEFAULT` para as colunas de data, em vez de especificar um valor:

```
INSERT INTO films VALUES
    ('UA502', 'Bananas', 105, DEFAULT, 'Comedy', '82 minutes');
INSERT INTO films (code, title, did, date_prod, kind)
    VALUES ('T_601', 'Yojimbo', 106, DEFAULT, 'Drama');
```

Para inserir uma linha composta inteiramente por valores padrão:

```
INSERT INTO films DEFAULT VALUES;
```

Para inserir várias linhas usando a sintaxe multirow `VALUES`:

```
INSERT INTO films (code, title, did, date_prod, kind) VALUES
    ('B6717', 'Tampopo', 110, '1985-02-10', 'Comedy'),
    ('HG120', 'The Dinner Game', 140, DEFAULT, 'Comedy');
```

Este exemplo insere algumas linhas na tabela `films` a partir de uma tabela `tmp_films` com o mesmo layout de coluna que `films`:

```
INSERT INTO films SELECT * FROM tmp_films WHERE date_prod < '2004-05-07';
```

Este exemplo insere nas colunas da matriz:

```
-- Create an empty 3x3 gameboard for noughts-and-crosses
INSERT INTO tictactoe (game, board[1:3][1:3])
    VALUES (1, '{{" "," "," "},{" "," "," "},{" "," "," "}}');
-- The subscripts in the above example aren't really needed
INSERT INTO tictactoe (game, board)
    VALUES (2, '{{X," "," "},{" ",O," "},{" ",X," "}}');
```

Insira uma única linha na tabela `distributors`, retornando o número de sequência gerado pela cláusula `DEFAULT`:

```
INSERT INTO distributors (did, dname) VALUES (DEFAULT, 'XYZ Widgets')
   RETURNING did;
```

Incremente o número de vendas do vendedor que gerencia a conta da Acme Corporation e registre toda a linha atualizada, juntamente com a hora atual, em uma tabela de registro:

```
WITH upd AS (
  UPDATE employees SET sales_count = sales_count + 1 WHERE id =
    (SELECT sales_person FROM accounts WHERE name = 'Acme Corporation')
    RETURNING *
)
INSERT INTO employees_log SELECT *, current_timestamp FROM upd;
```

Insira ou atualize novos distribuidores conforme apropriado. Assume-se que um índice único foi definido que restringe os valores que aparecem na coluna `did`. Note que a tabela especial `excluded` é usada para referenciar valores propostos originalmente para inserção:

```
INSERT INTO distributors (did, dname)
    VALUES (5, 'Gizmo Transglobal'), (6, 'Associated Computing, Inc')
    ON CONFLICT (did) DO UPDATE SET dname = EXCLUDED.dname;
```

Insira ou atualize novos distribuidores conforme o acima, retornando informações sobre quaisquer valores existentes que foram atualizados, juntamente com os novos dados inseridos. Note que os valores retornados para `old_did` e `old_dname` serão `NULL` para linhas não conflitantes:

```
INSERT INTO distributors (did, dname)
    VALUES (5, 'Gizmo Transglobal'), (6, 'Associated Computing, Inc')
    ON CONFLICT (did) DO UPDATE SET dname = EXCLUDED.dname
    RETURNING old.did AS old_did, old.dname AS old_dname,
              new.did AS new_did, new.dname AS new_dname;
```

Insira um distribuidor ou não faça nada para as linhas propostas para inserção quando uma linha existente, excluída (uma linha com uma coluna ou colunas restritas correspondentes após os gatilhos de inserção da linha antes de ser inserida) existe. O exemplo assume que um índice único foi definido que restringe os valores que aparecem na coluna `did`:

```
INSERT INTO distributors (did, dname) VALUES (7, 'Redline GmbH')
    ON CONFLICT (did) DO NOTHING;
```

Insira ou atualize novos distribuidores conforme necessário. O exemplo assume que um índice único foi definido que restringe os valores que aparecem na coluna `did`. A cláusula `WHERE` é usada para limitar as linhas que são realmente atualizadas (qualquer linha existente que não seja atualizada ainda será bloqueada, embora):

```
-- Don't update existing distributors based in a certain ZIP code
INSERT INTO distributors AS d (did, dname) VALUES (8, 'Anvil Distribution')
    ON CONFLICT (did) DO UPDATE
    SET dname = EXCLUDED.dname || ' (formerly ' || d.dname || ')'
    WHERE d.zipcode <> '21201';

-- Name a constraint directly in the statement (uses associated
-- index to arbitrate taking the DO NOTHING action)
INSERT INTO distributors (did, dname) VALUES (9, 'Antwerp Design')
    ON CONFLICT ON CONSTRAINT distributors_pkey DO NOTHING;
```

Insira um novo distribuidor, se possível; caso contrário, `DO NOTHING`. O exemplo assume que um índice único foi definido que restringe os valores que aparecem na coluna `did` em um subconjunto de linhas onde a coluna binária `is_active` avalia em `true`:

```
-- This statement could infer a partial unique index on "did"
-- with a predicate of "WHERE is_active", but it could also
-- just use a regular unique constraint on "did"
INSERT INTO distributors (did, dname) VALUES (10, 'Conrad International')
    ON CONFLICT (did) WHERE is_active DO NOTHING;
```

## Compatibilidade

`INSERT` está em conformidade com o padrão SQL, exceto pelo fato de que a cláusula `RETURNING` é uma extensão do PostgreSQL, assim como a capacidade de usar `WITH` com `INSERT`, e a capacidade de especificar uma ação alternativa com `ON CONFLICT`. Além disso, o caso em que uma lista de nomes de coluna é omitida, mas nem todas as colunas são preenchidas a partir da cláusula `VALUES` ou *`query`*, é proibido pelo padrão. Se você prefere uma declaração mais conforme ao padrão SQL do que `ON CONFLICT`, veja [MERGE](sql-merge.md "MERGE").

O padrão SQL especifica que `OVERRIDING SYSTEM VALUE` só pode ser especificado se uma coluna de identidade que é gerada sempre existir. O PostgreSQL permite a cláusula em qualquer caso e a ignora se não for aplicável.

Possíveis limitações da cláusula *`query`* estão documentadas em [SELECT][(sql-select.md "SELECT")].
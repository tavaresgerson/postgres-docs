## 41.7. Cursor [#](#PLPGSQL-CURSORS)

* [41.7.1. Declarando variáveis de cursor](plpgsql-cursors.md#PLPGSQL-CURSOR-DECLARATIONS)
* [41.7.2. Abrir cursors](plpgsql-cursors.md#PLPGSQL-CURSOR-OPENING)
* [41.7.3. Usando cursors](plpgsql-cursors.md#PLPGSQL-CURSOR-USING)
* [41.7.4. Percorrendo o resultado de um cursor](plpgsql-cursors.md#PLPGSQL-CURSOR-FOR-LOOP)

Em vez de executar uma consulta inteira de uma vez, é possível configurar um *cursor* que encapsula a consulta e, em seguida, ler o resultado da consulta algumas linhas de cada vez. Uma razão para fazer isso é evitar o excesso de memória quando o resultado contém um grande número de linhas. (No entanto, os usuários do PL/pgSQL normalmente não precisam se preocupar com isso, uma vez que os loops `FOR` usam automaticamente um cursor internamente para evitar problemas de memória.) Um uso mais interessante é retornar uma referência a um cursor que uma função criou, permitindo que o chamador leia as linhas. Isso fornece uma maneira eficiente de retornar grandes conjuntos de linhas a partir de funções.

### 41.7.1. Declaração de variáveis de cursor [#](#PLPGSQL-CURSOR-DECLARATIONS)

Todo acesso a cursor em PL/pgSQL passa por variáveis de cursor, que são sempre do tipo de dados especial `refcursor`. Uma maneira de criar uma variável de cursor é simplesmente declará-la como uma variável do tipo `refcursor`. Outra maneira é usar a sintaxe de declaração de cursor, que, em geral, é:

```
name [ [ NO ] SCROLL ] CURSOR [ ( arguments ) ] FOR query;
```

(`FOR` pode ser substituído por `IS` para compatibilidade com Oracle.) Se `SCROLL` for especificado, o cursor será capaz de rolar para trás; se `NO SCROLL` for especificado, as fetches para trás serão rejeitadas; se nenhuma das especificações aparecer, depende da consulta se as fetches para trás serão permitidas. *`arguments`*, se especificado, é uma lista de pares separados por vírgula `name datatype` que definem nomes que serão substituídos por valores de parâmetro na consulta dada. Os valores reais para substituir esses nomes serão especificados mais tarde, quando o cursor for aberto.

Alguns exemplos:

```
DECLARE
    curs1 refcursor;
    curs2 CURSOR FOR SELECT * FROM tenk1;
    curs3 CURSOR (key integer) FOR SELECT * FROM tenk1 WHERE unique1 = key;
```

Todas essas três variáveis têm o tipo de dados `refcursor`, mas a primeira pode ser usada com qualquer consulta, enquanto a segunda tem uma consulta totalmente especificada já *ligada* a ela, e a última tem uma consulta parametrizada ligada a ela. (`key` será substituído por um valor de parâmetro inteiro quando o cursor for aberto.) A variável `curs1` é dita *não ligada* porque não está ligada a nenhuma consulta específica.

A opção `SCROLL` não pode ser usada quando a consulta do cursor usa `FOR UPDATE/SHARE`. Além disso, é melhor usar `NO SCROLL` com uma consulta que envolva funções voláteis. A implementação de `SCROLL` assume que a re-leitura do resultado da consulta dará resultados consistentes, o que uma função volátil pode não fazer.

### 41.7.2. Abertura de cursor [#](#PLPGSQL-CURSOR-OPENING)

Antes que um cursor possa ser usado para recuperar linhas, ele deve ser *aberto*. (Essa é a ação equivalente ao comando SQL `DECLARE CURSOR` (sql-declare.md "DECLARE"). PL/pgSQL tem três formas da declaração `OPEN`, das quais duas usam variáveis de cursor não vinculadas, enquanto a terceira usa uma variável de cursor vinculada.

Nota

As variáveis de cursor vinculado também podem ser usadas sem abrir explicitamente o cursor, através da declaração `FOR` descrita em [Seção 41.7.4](plpgsql-cursors.md#PLPGSQL-CURSOR-FOR-LOOP). Um loop `FOR` abrirá o cursor e o fechará novamente quando o loop for concluído.

Abrir um cursor envolve a criação de uma estrutura de dados interna do servidor chamada *portal*, que contém o estado de execução da consulta do cursor. Um portal tem um nome, que deve ser único dentro da sessão durante a existência do portal. Por padrão, o PL/pgSQL atribuirá um nome único a cada portal que cria. No entanto, se você atribuir um valor de cadeia de caracteres não nulo a uma variável de cursor, essa cadeia de caracteres será usada como o nome do seu portal. Esse recurso pode ser usado conforme descrito em [Seção 41.7.3.5](plpgsql-cursors.md#PLPGSQL-CURSOR-RETURNING).

#### 41.7.2.1. `OPEN FOR` *`query`* [#](#PLPGSQL-CURSOR-OPENING-OPEN-FOR-QUERY)

```
OPEN unbound_cursorvar [ [ NO ] SCROLL ] FOR query;
```

A variável cursor é aberta e dada a consulta especificada para ser executada. O cursor não pode estar aberto já, e deve ter sido declarado como uma variável de cursor não vinculada (ou seja, como uma simples variável `refcursor`). A consulta deve ser uma `SELECT`, ou algo mais que retorne linhas (como `EXPLAIN`). A consulta é tratada da mesma forma que outros comandos SQL no PL/pgSQL: os nomes das variáveis PL/pgSQL são substituídos e o plano da consulta é armazenado em cache para possível uso posterior. Quando uma variável PL/pgSQL é substituída na consulta do cursor, o valor que é substituído é o que ela tem no momento do `OPEN`; as alterações subsequentes na variável não afetarão o comportamento do cursor. As opções `SCROLL` e `NO SCROLL` têm os mesmos significados que para um cursor vinculado.

Um exemplo:

```
OPEN curs1 FOR SELECT * FROM foo WHERE key = mykey;
```

#### 41.7.2.2. `OPEN FOR EXECUTE` [#](#PLPGSQL-CURSOR-OPENING-OPEN-FOR-EXECUTE)

```
OPEN unbound_cursorvar [ [ NO ] SCROLL ] FOR EXECUTE query_string
                                     [ USING expression [, ... ] ];
```

A variável cursor é aberta e dada a consulta especificada para ser executada. O cursor não pode estar aberto já, e deve ter sido declarado como uma variável de cursor não vinculada (ou seja, como uma simples variável `refcursor`). A consulta é especificada como uma expressão de string, da mesma forma que no comando `EXECUTE`. Como de costume, isso dá flexibilidade para que o plano da consulta possa variar de uma execução para a outra (ver [Seção 41.11.2](plpgsql-implementation.md#PLPGSQL-PLAN-CACHING)), e também significa que a substituição de variáveis não é feita na string do comando. Como com `EXECUTE`, os valores dos parâmetros podem ser inseridos no comando dinâmico via `format()` e `USING`. As opções `SCROLL` e `NO SCROLL` têm os mesmos significados que para um cursor vinculado.

Um exemplo:

```
OPEN curs1 FOR EXECUTE format('SELECT * FROM %I WHERE col1 = $1',tabname) USING keyvalue;
```

Neste exemplo, o nome da tabela é inserido na consulta através de `format()`. O valor de comparação para `col1` é inserido através de um parâmetro `USING`, portanto, não precisa de aspas.

#### 41.7.2.3. Abertura de um cursor vinculado [#](#PLPGSQL-OPEN-BOUND-CURSOR)

```
OPEN bound_cursorvar [ ( [ argument_name { := | => } ] argument_value [, ...] ) ];
```

Essa forma de `OPEN` é usada para abrir uma variável de cursor cuja consulta foi vinculada a ela quando foi declarada. O cursor não pode ser aberto já. Uma lista de expressões de valor de argumento real deve aparecer se e somente se o cursor foi declarado para receber argumentos. Esses valores serão substituídos na consulta.

O plano de consulta para um cursor vinculado é sempre considerado cacheável; não há um equivalente de `EXECUTE` neste caso. Observe que `SCROLL` e `NO SCROLL` não podem ser especificados em `OPEN`, pois o comportamento de rolagem do cursor já foi determinado.

Os valores dos argumentos podem ser passados usando notação *posicionada* ou *denominada*. Na notação posicionada, todos os argumentos são especificados em ordem. Na notação denominada, o nome de cada argumento é especificado usando `:=` ou `=>` para separá-lo da expressão do argumento. Semelhante à chamada de funções, descrita em [Seção 4.3](sql-syntax-calling-funcs.md), também é permitido misturar notação posicionada e denominada.

Exemplos (estes usam os exemplos de declaração do cursor acima):

```
OPEN curs2;
OPEN curs3(42);
OPEN curs3(key := 42);
OPEN curs3(key => 42);
```

Como a substituição de variáveis é feita na consulta de um cursor vinculado, existem realmente duas maneiras de passar valores para o cursor: ou com um argumento explícito para `OPEN`, ou implicitamente referenciando uma variável PL/pgSQL na consulta. No entanto, apenas as variáveis declaradas antes da declaração do cursor vinculado serão substituídas nele. Em qualquer caso, o valor a ser passado é determinado no momento do `OPEN`. Por exemplo, outra maneira de obter o mesmo efeito que o exemplo `curs3` acima é

```
DECLARE
    key integer;
    curs4 CURSOR FOR SELECT * FROM tenk1 WHERE unique1 = key;
BEGIN
    key := 42;
    OPEN curs4;
```

### 41.7.3. Uso de cursor [#](#PLPGSQL-CURSOR-USING)

Uma vez que um cursor tenha sido aberto, ele pode ser manipulado com as declarações descritas aqui.

Essas manipulações não precisam ocorrer na mesma função que abriu o cursor inicialmente. Você pode retornar um valor `refcursor` de uma função e deixar o chamador operar no cursor. (Internamente, um valor `refcursor` é simplesmente o nome da string do portal que contém a consulta ativa para o cursor. Esse nome pode ser passado, atribuído a outras variáveis `refcursor` e assim por diante, sem perturbar o portal.)

Todos os portais são implicitamente fechados no final da transação. Portanto, um valor `refcursor` pode ser usado para referenciar um cursor aberto apenas até o final da transação.

#### 41.7.3.1. `FETCH` [#](#PLPGSQL-CURSOR-USING-FETCH)

```
FETCH [ direction { FROM | IN } ] cursor INTO target;
```

`FETCH` recupera a próxima linha (na direção indicada) do cursor para um alvo, que pode ser uma variável de linha, uma variável de registro ou uma lista de variáveis simples separadas por vírgula, assim como `SELECT INTO`. Se não houver uma linha adequada, o alvo é definido como NULL(s). Assim como em `SELECT INTO`, a variável especial `FOUND` pode ser verificada para determinar se uma linha foi obtida ou não. Se nenhuma linha for obtida, o cursor é posicionado após a última linha ou antes da primeira linha, dependendo da direção do movimento.

A cláusula *`direction`* pode ser qualquer uma das variantes permitidas no comando SQL [FETCH](sql-fetch.md), exceto as que podem recuperar mais de uma linha; ou seja, pode ser `NEXT`, `PRIOR`, `FIRST`, `LAST`, `ABSOLUTE` *`count`*, `RELATIVE` *`count`*, `FORWARD`, ou `BACKWARD`. O omitindo *`direction`* é o mesmo que especificar `NEXT`. Nos formulários que utilizam um *`count`*, o *`count`* pode ser qualquer expressão com valor inteiro (ao contrário do comando SQL `FETCH`, que só permite uma constante inteira). Os valores de *`direction`* que exigem recuo provavelmente falharão, a menos que o cursor tenha sido declarado ou aberto com a opção `SCROLL`.

*`cursor`* deve ser o nome de uma variável `refcursor` que faça referência a um portal de cursor aberto.

Exemplos:

```
FETCH curs1 INTO rowvar;
FETCH curs2 INTO foo, bar, baz;
FETCH LAST FROM curs3 INTO x, y;
FETCH RELATIVE -2 FROM curs4 INTO x;
```

#### 41.7.3.2. `MOVE` [#](#PLPGSQL-CURSOR-USING-MOVE)

```
MOVE [ direction { FROM | IN } ] cursor;
```

`MOVE` reposiciona um cursor sem recuperar nenhum dado. `MOVE` funciona como o comando `FETCH`, exceto que apenas reposiciona o cursor e não retorna a linha movida. A cláusula *`direction`* pode ser qualquer uma das variantes permitidas no comando SQL [FETCH](sql-fetch.md "FETCH"), incluindo aquelas que podem recuperar mais de uma linha; o cursor é posicionado na última linha desse tipo. (No entanto, o caso em que a cláusula *`direction`* é simplesmente uma expressão *`count`* sem palavra-chave é desaconselhada no PL/pgSQL. Essa sintaxe é ambígua com o caso em que a cláusula *`direction`* é omitida completamente, e, portanto, pode falhar se o *`count`* não for uma constante.) Como com `SELECT INTO`, a variável especial `FOUND` pode ser verificada para ver se havia uma linha para mover. Se não houver tal linha, o cursor é posicionado após a última linha ou antes da primeira linha, dependendo da direção do movimento.

Exemplos:

```
MOVE curs1;
MOVE LAST FROM curs3;
MOVE RELATIVE -2 FROM curs4;
MOVE FORWARD 2 FROM curs4;
```

#### 41.7.3.3. `UPDATE/DELETE WHERE CURRENT OF` [#](#PLPGSQL-CURSOR-USING-UPDATE-DELETE)

```
UPDATE table SET ... WHERE CURRENT OF cursor;
DELETE FROM table WHERE CURRENT OF cursor;
```

Quando o cursor é posicionado em uma linha de tabela, essa linha pode ser atualizada ou excluída usando o cursor para identificar a linha. Há restrições sobre o que a consulta do cursor pode ser (em particular, sem agrupamento) e é melhor usar `FOR UPDATE` no cursor. Para mais informações, consulte a página de referência [DECLARE](sql-declare.md "DECLARE").

Um exemplo:

```
UPDATE foo SET dataval = myval WHERE CURRENT OF curs1;
```

#### 41.7.3.4. `CLOSE` [#](#PLPGSQL-CURSOR-USING-CLOSE)

```
CLOSE cursor;
```

`CLOSE` fecha o portal subjacente a um cursor aberto. Isso pode ser usado para liberar recursos antes do fim da transação, ou para liberar a variável do cursor a ser aberta novamente.

Um exemplo:

```
CLOSE curs1;
```

#### 41.7.3.5. Retornando os cursors [#](#PLPGSQL-CURSOR-RETURNING)

As funções PL/pgSQL podem retornar cursors para o chamador. Isso é útil para retornar várias linhas ou colunas, especialmente em conjuntos de resultados muito grandes. Para fazer isso, a função abre o cursor e retorna o nome do cursor para o chamador (ou simplesmente abre o cursor usando um nome de portal especificado pelo chamador ou conhecido por ele). O chamador pode, então, buscar linhas do cursor. O cursor pode ser fechado pelo chamador, ou será fechado automaticamente quando a transação for fechada.

O nome do portal utilizado para um cursor pode ser especificado pelo programador ou gerado automaticamente. Para especificar um nome de portal, basta atribuir uma string à variável `refcursor` antes de abri-la. O valor da string da variável `refcursor` será utilizado por `OPEN` como o nome do portal subjacente. No entanto, se o valor da variável `refcursor` for nulo (como será por padrão), então `OPEN` gera automaticamente um nome que não conflita com nenhum portal existente e o atribui à variável `refcursor`.

Nota

Antes do PostgreSQL 16, as variáveis de cursor vinculadas eram inicializadas para conter seus próprios nomes, em vez de serem deixadas como nulos, para que o nome do portal subjacente fosse o mesmo que o nome da variável de cursor por padrão. Isso foi alterado porque isso criava um risco excessivo de conflitos entre cursors com nomes semelhantes em diferentes funções.

O exemplo a seguir mostra uma maneira de um nome de cursor ser fornecido pelo chamador:

```
CREATE TABLE test (col text);
INSERT INTO test VALUES ('123');

CREATE FUNCTION reffunc(refcursor) RETURNS refcursor AS '
BEGIN
    OPEN $1 FOR SELECT col FROM test;
    RETURN $1;
END;
' LANGUAGE plpgsql;

BEGIN;
SELECT reffunc('funccursor');
FETCH ALL IN funccursor;
COMMIT;
```

O exemplo a seguir utiliza a geração automática de nome do cursor:

```
CREATE FUNCTION reffunc2() RETURNS refcursor AS '
DECLARE
    ref refcursor;
BEGIN
    OPEN ref FOR SELECT col FROM test;
    RETURN ref;
END;
' LANGUAGE plpgsql;

-- need to be in a transaction to use cursors.
BEGIN;
SELECT reffunc2();

      reffunc2
--------------------
 <unnamed cursor 1>
(1 row)

FETCH ALL IN "<unnamed cursor 1>";
COMMIT;
```

O exemplo a seguir mostra uma maneira de retornar vários cursors a partir de uma única função:

```
CREATE FUNCTION myfunc(refcursor, refcursor) RETURNS SETOF refcursor AS $$
BEGIN
    OPEN $1 FOR SELECT * FROM table_1;
    RETURN NEXT $1;
    OPEN $2 FOR SELECT * FROM table_2;
    RETURN NEXT $2;
END;
$$ LANGUAGE plpgsql;

-- need to be in a transaction to use cursors.
BEGIN;

SELECT * FROM myfunc('a', 'b');

FETCH ALL FROM a;
FETCH ALL FROM b;
COMMIT;
```

### 41.7.4. Percorrer o resultado de um cursor [#](#PLPGSQL-CURSOR-FOR-LOOP)

Existe uma variante da declaração `FOR` que permite a iteração das linhas devolvidas por um cursor. A sintaxe é:

```
[ <<label>> ]
FOR recordvar IN bound_cursorvar [ ( [ argument_name { := | => } ] argument_value [, ...] ) ] LOOP
    statements
END LOOP [ label ];
```

A variável cursor deve ter sido vinculada a alguma consulta quando foi declarada, e *não pode* estar aberta já. A declaração `FOR` abre o cursor automaticamente e o fecha novamente quando o loop sai. Uma lista de expressões de valores de argumento deve aparecer se e somente se o cursor foi declarado para receber argumentos. Esses valores serão substituídos na consulta, da mesma maneira que durante uma `OPEN` (consulte [Seção 41.7.2.3] (plpgsql-cursors.md#PLPGSQL-OPEN-BOUND-CURSOR "41.7.2.3. Opening a Bound Cursor")).

A variável *`recordvar`* é definida automaticamente como tipo `record` e existe apenas dentro do loop (qualquer definição existente do nome da variável é ignorada dentro do loop). Cada linha devolvida pelo cursor é sucessivamente atribuída a esta variável de registro e o corpo do loop é executado.
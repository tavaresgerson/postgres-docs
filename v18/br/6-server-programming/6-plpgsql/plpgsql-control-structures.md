## 41.6. Estruturas de controle [#](#PLPGSQL-CONTROL-STRUCTURES)

* [41.6.1. Retorno de uma função][(plpgsql-control-structures.md#PLPGSQL-STATEMENTS-RETURNING)
* [41.6.2. Retorno de um procedimento][(plpgsql-control-structures.md#PLPGSQL-STATEMENTS-RETURNING-PROCEDURE)
* [41.6.3. Chamada de um procedimento][(plpgsql-control-structures.md#PLPGSQL-STATEMENTS-CALLING-PROCEDURE)
* [41.6.4. Condicionais][(plpgsql-control-structures.md#PLPGSQL-CONDITIONALS)
* [41.6.5. Loops simples][(plpgsql-control-structures.md#PLPGSQL-CONTROL-STRUCTURES-LOOPS)
* [41.6.6. Percurso por resultados de consulta][(plpgsql-control-structures.md#PLPGSQL-RECORDS-ITERATING)
* [41.6.7. Percurso por arrays][(plpgsql-control-structures.md#PLPGSQL-FOREACH-ARRAY)
* [41.6.8. Captura de erros][(plpgsql-control-structures.md#PLPGSQL-ERROR-TRAPPING)
* [41.6.9. Obtenção de informações sobre a localização de execução][(plpgsql-control-structures.md#PLPGSQL-CALL-STACK)

As estruturas de controle são provavelmente a parte mais útil (e importante) do PL/pgSQL. Com as estruturas de controle do PL/pgSQL, você pode manipular os dados do PostgreSQL de uma maneira muito flexível e poderosa.

### 41.6.1. Retornando de uma função [#](#PLPGSQL-STATEMENTS-RETURNING)

Existem dois comandos disponíveis que permitem retornar dados de uma função: `RETURN` e `RETURN NEXT`.

#### 41.6.1.1. `RETURN` [#](#PLPGSQL-STATEMENTS-RETURNING-RETURN)

```
RETURN expression;
```

`RETURN` com uma expressão termina a função e retorna o valor de *`expression`* para o chamador. Esta forma é usada para funções PL/pgSQL que não retornam um conjunto.

Em uma função que retorna um tipo escalar, o resultado da expressão será automaticamente convertido para o tipo de retorno da função, conforme descrito para atribuições. Mas para retornar um valor composto (linha), você deve escrever uma expressão que forneça exatamente o conjunto de colunas solicitado. Isso pode exigir o uso de conversão explícita.

Se você declarou a função com parâmetros de saída, escreva apenas `RETURN` sem expressão. Os valores atuais das variáveis do parâmetro de saída serão retornados.

Se você declarou a função para retornar `void`, uma declaração `RETURN` pode ser usada para sair da função precocemente; mas não escreva uma expressão após `RETURN`.

O valor de retorno de uma função não pode ser deixado indefinido. Se o controle atingir o final do bloco de nível superior da função sem atingir uma declaração `RETURN`, ocorrerá um erro de execução. Esta restrição, no entanto, não se aplica a funções com parâmetros de saída e funções que retornam `void`. Nesses casos, uma declaração `RETURN` é executada automaticamente se o bloco de nível superior terminar.

Alguns exemplos:

```
-- functions returning a scalar type
RETURN 1 + 2;
RETURN scalar_var;

-- functions returning a composite type
RETURN composite_type_var;
RETURN (1, 2, 'three'::text);  -- must cast columns to correct types
```

#### 41.6.1.2. `RETURN NEXT` e `RETURN QUERY` [#](#PLPGSQL-STATEMENTS-RETURNING-RETURN-NEXT)

```
RETURN NEXT expression;
RETURN QUERY query;
RETURN QUERY EXECUTE command-string [ USING expression [, ... ] ];
```

Quando uma função PL/pgSQL é declarada para retornar `SETOF sometype`, o procedimento a seguir é um pouco diferente. Nesse caso, os itens individuais a serem retornados são especificados por uma sequência de comandos `RETURN NEXT` ou `RETURN QUERY`, e então um comando final `RETURN` sem argumento é usado para indicar que a função terminou a execução. `RETURN NEXT` pode ser usado com tipos de dados escalares e compostos; com um tipo de resultado composto, será retornado um "tabela" inteira de resultados. `RETURN QUERY` anexa os resultados da execução de uma consulta ao conjunto de resultados da função. `RETURN NEXT` e `RETURN QUERY` podem ser misturados livremente em uma única função que retorna um conjunto, no caso, seus resultados serão concatenados.

`RETURN NEXT` e `RETURN QUERY` não retornam realmente da função — eles simplesmente anexam zero ou mais linhas ao conjunto de resultados da função. A execução então continua com a próxima instrução na função PL/pgSQL. À medida que os comandos sucessivos `RETURN NEXT` ou `RETURN QUERY` são executados, o conjunto de resultados é construído. Um `RETURN` final, que não deve ter argumento, faz com que o controle saia da função (ou você pode simplesmente deixar o controle chegar ao final da função).

`RETURN QUERY` tem uma variante `RETURN QUERY EXECUTE`, que especifica a consulta a ser executada dinamicamente. Expressões de parâmetro podem ser inseridas na consulta calculada via `USING`, da mesma maneira que no comando `EXECUTE`.

Se você declarou a função com parâmetros de saída, escreva apenas `RETURN NEXT` sem expressão. Em cada execução, os valores atuais dos(s) parâmetro(s) de saída serão salvos para eventual retorno como uma linha do resultado. Note que você deve declarar a função como retornando `SETOF record` quando houver vários parâmetros de saída, ou `SETOF sometype` quando houver apenas um parâmetro de saída do tipo *`sometype`*, a fim de criar uma função que retorne um conjunto com parâmetros de saída.

Aqui está um exemplo de uma função que usa `RETURN NEXT`:

```
CREATE TABLE foo (fooid INT, foosubid INT, fooname TEXT);
INSERT INTO foo VALUES (1, 2, 'three');
INSERT INTO foo VALUES (4, 5, 'six');

CREATE OR REPLACE FUNCTION get_all_foo() RETURNS SETOF foo AS
$BODY$
DECLARE
    r foo%rowtype;
BEGIN
    FOR r IN
        SELECT * FROM foo WHERE fooid > 0
    LOOP
        -- can do some processing here
        RETURN NEXT r; -- return current row of SELECT
    END LOOP;
    RETURN;
END;
$BODY$
LANGUAGE plpgsql;

SELECT * FROM get_all_foo();
```

Aqui está um exemplo de uma função que utiliza `RETURN QUERY`:

```
CREATE FUNCTION get_available_flightid(date) RETURNS SETOF integer AS
$BODY$
BEGIN
    RETURN QUERY SELECT flightid
                   FROM flight
                  WHERE flightdate >= $1
                    AND flightdate < ($1 + 1);

    -- Since execution is not finished, we can check whether rows were returned
    -- and raise exception if not.
    IF NOT FOUND THEN
        RAISE EXCEPTION 'No flight at %.', $1;
    END IF;

    RETURN;
 END;
$BODY$
LANGUAGE plpgsql;

-- Returns available flights or raises exception if there are no
-- available flights.
SELECT * FROM get_available_flightid(CURRENT_DATE);
```

Nota

A implementação atual de `RETURN NEXT` e `RETURN QUERY` armazena todo o conjunto de resultados antes de retornar da função, conforme discutido acima. Isso significa que, se uma função PL/pgSQL produzir um conjunto de resultados muito grande, o desempenho pode ser ruim: os dados serão escritos em disco para evitar o esgotamento da memória, mas a própria função não retornará até que todo o conjunto de resultados tenha sido gerado. Uma versão futura do PL/pgSQL pode permitir que os usuários definam funções que retornam conjuntos e que não tenham essa limitação. Atualmente, o ponto em que os dados começam a ser escritos em disco é controlado pela variável de configuração [work_mem](runtime-config-resource.md#GUC-WORK-MEM). Os administradores que têm memória suficiente para armazenar conjuntos de resultados maiores na memória devem considerar aumentar esse parâmetro.

### 41.6.2. Retorno após procedimento [#](#PLPGSQL-STATEMENTS-RETURNING-PROCEDURE)

Um procedimento não tem um valor de retorno. Portanto, um procedimento pode terminar sem uma declaração `RETURN`. Se você deseja usar uma declaração `RETURN` para sair do código precocemente, escreva apenas `RETURN` sem expressão.

Se o procedimento tiver parâmetros de saída, os valores finais das variáveis do parâmetro de saída serão devolvidos ao solicitante.

### 41.6.3. Chamada de um procedimento [#](#PLPGSQL-STATEMENTS-CALLING-PROCEDURE)

Uma função, procedimento ou bloco `DO` do PL/pgSQL pode chamar um procedimento usando `CALL`. Os parâmetros de saída são tratados de maneira diferente da forma como o `CALL` funciona no SQL simples. Cada parâmetro `OUT` ou `INOUT` do procedimento deve corresponder a uma variável na declaração `CALL`, e o que o procedimento retorna é atribuído de volta a essa variável após retornar. Por exemplo:

```
CREATE PROCEDURE triple(INOUT x int)
LANGUAGE plpgsql
AS $$
BEGIN
    x := x * 3;
END;
$$;

DO $$
DECLARE myvar int := 5;
BEGIN
  CALL triple(myvar);
  RAISE NOTICE 'myvar = %', myvar;  -- prints 15
END;
$$;
```

A variável correspondente a um parâmetro de saída pode ser uma variável simples ou um campo de uma variável de tipo composto. Atualmente, não pode ser um elemento de um array.

### 41.6.4. Condicionais [#](#PLPGSQL-CONDITIONALS)

As declarações `IF` e `CASE` permitem que você execute comandos alternativos com base em certas condições. O PL/pgSQL tem três formas de `IF`:

* `IF ... THEN ... END IF`
* `IF ... THEN ... ELSE ... END IF`
* `IF ... THEN ... ELSIF ... THEN ... ELSE ... END IF`

e duas formas de `CASE`:

* `CASE ... WHEN ... THEN ... ELSE ... END CASE`
* `CASE WHEN ... THEN ... ELSE ... END CASE`

#### 41.6.4.1. `IF-THEN` [#](#PLPGSQL-CONDITIONALS-IF-THEN)

```
IF boolean-expression THEN
    statements
END IF;
```

As declarações `IF-THEN` são a forma mais simples de `IF`. As declarações entre `THEN` e `END IF` serão executadas se a condição for verdadeira. Caso contrário, elas são ignoradas.

Exemplo:

```
IF v_user_id <> 0 THEN
    UPDATE users SET email = v_email WHERE user_id = v_user_id;
END IF;
```

#### 41.6.4.2. `IF-THEN-ELSE` [#](#PLPGSQL-CONDITIONALS-IF-THEN-ELSE)

```
IF boolean-expression THEN
    statements
ELSE
    statements
END IF;
```

As declarações `IF-THEN-ELSE` são complementares às `IF-THEN`, permitindo que você especifique um conjunto alternativo de declarações que devem ser executadas se a condição não for verdadeira. (Observe que isso inclui o caso em que a condição avalia como NULL.)

Exemplos:

```
IF parentid IS NULL OR parentid = ''
THEN
    RETURN fullname;
ELSE
    RETURN hp_true_filename(parentid) || '/' || fullname;
END IF;
```

```
IF v_count > 0 THEN
    INSERT INTO users_count (count) VALUES (v_count);
    RETURN 't';
ELSE
    RETURN 'f';
END IF;
```

#### 41.6.4.3. `IF-THEN-ELSIF` [#](#PLPGSQL-CONDITIONALS-IF-THEN-ELSIF)

```
IF boolean-expression THEN
    statements
[ ELSIF boolean-expression THEN
    statements
[ ELSIF boolean-expression THEN
    statements
    ...
]
]
[ ELSE
    statements ]
END IF;
```

Às vezes, há mais do que apenas duas alternativas. `IF-THEN-ELSIF` fornece um método conveniente para verificar várias alternativas em sequência. As condições `IF` são testadas sucessivamente até que a primeira que é verdadeira seja encontrada. Em seguida, as declarações associadas são executadas, após o que o controle passa para a próxima declaração após `END IF`. (Quaisquer condições subsequentes `IF` não são testadas.) Se nenhuma das condições `IF` é verdadeira, então o bloco `ELSE` (se houver) é executado.

Aqui está um exemplo:

```
IF number = 0 THEN
    result := 'zero';
ELSIF number > 0 THEN
    result := 'positive';
ELSIF number < 0 THEN
    result := 'negative';
ELSE
    -- hmm, the only other possibility is that number is null
    result := 'NULL';
END IF;
```

A palavra-chave `ELSIF` também pode ser escrita como `ELSEIF`.

Uma maneira alternativa de realizar a mesma tarefa é aninhar as declarações `IF-THEN-ELSE`, como no exemplo a seguir:

```
IF demo_row.sex = 'm' THEN
    pretty_sex := 'man';
ELSE
    IF demo_row.sex = 'f' THEN
        pretty_sex := 'woman';
    END IF;
END IF;
```

No entanto, esse método exige a escrita de um `END IF` correspondente para cada `IF`, portanto, é muito mais complicado do que usar `ELSIF` quando há muitas alternativas.

#### 41.6.4.4. `CASE` simples [#](#PLPGSQL-CONDITIONALS-SIMPLE-CASE)

```
CASE search-expression
    WHEN expression [, expression [ ... ]] THEN
      statements
  [ WHEN expression [, expression [ ... ]] THEN
      statements
    ... ]
  [ ELSE
      statements ]
END CASE;
```

A forma simples de `CASE` fornece execução condicional com base na igualdade dos operandos. O *`search-expression`* é avaliado (uma vez) e comparado sucessivamente a cada *`expression`* nas cláusulas de `WHEN`. Se uma correspondência for encontrada, então os *`statements`* correspondentes são executados, e então o controle passa para a próxima declaração após `END CASE`. (As expressões subsequentes de `WHEN` não são avaliadas.) Se não for encontrada nenhuma correspondência, os *`statements`* de `ELSE` são executados; mas se `CASE_NOT_FOUND` não estiver presente, então uma exceção de `CASE_NOT_FOUND` é levantada.

Aqui está um exemplo simples:

```
CASE x
    WHEN 1, 2 THEN
        msg := 'one or two';
    ELSE
        msg := 'other value than one or two';
END CASE;
```

#### 41.6.4.5. `CASE` pesquisado [#](#PLPGSQL-CONDITIONALS-SEARCHED-CASE)

```
CASE
    WHEN boolean-expression THEN
      statements
  [ WHEN boolean-expression THEN
      statements
    ... ]
  [ ELSE
      statements ]
END CASE;
```

O formulário pesquisado de `CASE` fornece execução condicional com base na verdade de expressões lógicas. O *`boolean-expression`* de cada cláusula `WHEN` é avaliado em ordem, até que seja encontrado um que produza `true`. Em seguida, os *`statements`* correspondentes são executados, e o controle passa para a próxima declaração após `END CASE`. (As expressões subsequentes de `WHEN` não são avaliadas.) Se nenhum resultado verdadeiro for encontrado, os *`ELSE`* são executados; mas se `ELSE` não estiver presente, então uma exceção `CASE_NOT_FOUND` é levantada.

Aqui está um exemplo:

```
CASE
    WHEN x BETWEEN 0 AND 10 THEN
        msg := 'value is between zero and ten';
    WHEN x BETWEEN 11 AND 20 THEN
        msg := 'value is between eleven and twenty';
END CASE;
```

Essa forma de `CASE` é totalmente equivalente a `IF-THEN-ELSIF`, exceto pela regra de que alcançar uma cláusula `ELSE` omitida resulta em um erro em vez de não fazer nada.

### 41.6.5. **Loops Simples [#](#PLPGSQL-CONTROL-STRUCTURES-LOOPS)**

Com as declarações `LOOP`, `EXIT`, `CONTINUE`, `WHILE`, `FOR` e `FOREACH`, você pode fazer com que sua função PL/pgSQL repita uma série de comandos.

#### 41.6.5.1. `LOOP` [#](#PLPGSQL-CONTROL-STRUCTURES-LOOPS-LOOP)

```
[ <<label>> ]
LOOP
    statements
END LOOP [ label ];
```

`LOOP` define um loop incondicional que é repetido indefinidamente até ser terminado por uma declaração `EXIT` ou `RETURN`. O opcional *`label`* pode ser usado por declarações `EXIT` e `CONTINUE` dentro de loops aninhados para especificar qual loop essas declarações se referem.

#### 41.6.5.2. `EXIT` [#](#PLPGSQL-CONTROL-STRUCTURES-LOOPS-EXIT)

```
EXIT [ label ] [ WHEN boolean-expression ];
```

Se não for fornecido um *`label`*, o laço mais interno é terminado e a declaração que segue `END LOOP` é executada a seguir. Se *`label`* for fornecido, ele deve ser o rótulo do nível atual ou de algum nível externo de laço ou bloco aninhado. Então, o laço ou bloco nomeado é terminado e o controle continua com a declaração após o `END` correspondente ao laço/bloco.

Se `WHEN` for especificado, a saída do loop ocorre apenas se *`boolean-expression`* for verdadeiro. Caso contrário, o controle passa para a instrução após `EXIT`.

`EXIT` pode ser usado com todos os tipos de loops; não é limitado ao uso com loops incondicionais.

Quando usado com um bloco `BEGIN`, o `EXIT` passa o controle para a próxima declaração após o fim do bloco. Note que uma etiqueta deve ser usada para esse propósito; um `EXIT` não rotulado nunca é considerado para corresponder a um bloco `BEGIN`. (Essa é uma mudança em relação às versões anteriores à versão 8.4 do PostgreSQL, que permitiria que um `EXIT` não rotulado correspondesse a um bloco `BEGIN`.

Exemplos:

```
LOOP
    -- some computations
    IF count > 0 THEN
        EXIT;  -- exit loop
    END IF;
END LOOP;

LOOP
    -- some computations
    EXIT WHEN count > 0;  -- same result as previous example
END LOOP;

<<ablock>>
BEGIN
    -- some computations
    IF stocks > 100000 THEN
        EXIT ablock;  -- causes exit from the BEGIN block
    END IF;
    -- computations here will be skipped when stocks > 100000
END;
```

#### 41.6.5.3. `CONTINUE` [#](#PLPGSQL-CONTROL-STRUCTURES-LOOPS-CONTINUE)

```
CONTINUE [ label ] [ WHEN boolean-expression ];
```

Se não for fornecido um *`label`*, a próxima iteração do laço mais interno é iniciada. Isso significa que todas as declarações restantes no corpo do laço são ignoradas e o controle retorna à expressão de controle do laço (se houver) para determinar se outra iteração do laço é necessária. Se *`label`* estiver presente, ele especifica a etiqueta do laço cuja execução será continuada.

Se `WHEN` for especificado, a próxima iteração do loop é iniciada apenas se *`boolean-expression`* for verdadeiro. Caso contrário, o controle passa para a declaração após `CONTINUE`.

`CONTINUE` pode ser usado com todos os tipos de loops; não é limitado ao uso com loops incondicionais.

Exemplos:

```
LOOP
    -- some computations
    EXIT WHEN count > 100;
    CONTINUE WHEN count < 50;
    -- some computations for count IN [50 .. 100]
END LOOP;
```

#### 41.6.5.4. `WHILE` [#](#PLPGSQL-CONTROL-STRUCTURES-LOOPS-WHILE)

```
[ <<label>> ]
WHILE boolean-expression LOOP
    statements
END LOOP [ label ];
```

A declaração `WHILE` repete uma sequência de declarações enquanto o *`boolean-expression`* é avaliado como verdadeiro. A expressão é verificada logo antes de cada entrada no corpo do laço.

Por exemplo:

```
WHILE amount_owed > 0 AND gift_certificate_balance > 0 LOOP
    -- some computations here
END LOOP;

WHILE NOT done LOOP
    -- some computations here
END LOOP;
```

#### 41.6.5.5. `FOR` (Variante de número inteiro) [#](#PLPGSQL-INTEGER-FOR)

```
[ <<label>> ]
FOR name IN [ REVERSE ] expression .. expression [ BY expression ] LOOP
    statements
END LOOP [ label ];
```

Essa forma de `FOR` cria um laço que itera sobre uma faixa de valores inteiros. A variável *`name`* é definida automaticamente como tipo `integer` e existe apenas dentro do laço (qualquer definição existente do nome da variável é ignorada dentro do laço). As duas expressões que fornecem o limite inferior e superior da faixa são avaliadas uma vez ao entrar no laço. Se a cláusula `BY` não for especificada, o passo de iteração é 1, caso contrário, é o valor especificado na cláusula `BY`, que, novamente, é avaliada uma vez na entrada do laço. Se `REVERSE` for especificado, então o valor do passo é subtraído, em vez de adicionado, após cada iteração.

Alguns exemplos de loops de número inteiro `FOR`:

```
FOR i IN 1..10 LOOP
    -- i will take on the values 1,2,3,4,5,6,7,8,9,10 within the loop
END LOOP;

FOR i IN REVERSE 10..1 LOOP
    -- i will take on the values 10,9,8,7,6,5,4,3,2,1 within the loop
END LOOP;

FOR i IN REVERSE 10..1 BY 2 LOOP
    -- i will take on the values 10,8,6,4,2 within the loop
END LOOP;
```

Se a faixa inferior for maior que a faixa superior (ou menor, no caso do `REVERSE`, o corpo do loop não é executado. Não é gerado nenhum erro.

Se um *`label`* estiver anexado ao laço `FOR`, a variável de laço inteiro pode ser referenciada com um nome qualificado, usando o *`label`*.

### 41.6.6. Percorrer resultados de consulta [#](#PLPGSQL-RECORDS-ITERATING)

Usando um tipo diferente de loop `FOR`, você pode iterar pelos resultados de uma consulta e manipular esses dados conforme necessário. A sintaxe é:

```
[ <<label>> ]
FOR target IN query LOOP
    statements
END LOOP [ label ];
```

O *`target`* é uma variável de registro, uma variável de linha ou uma lista de variáveis escalares separadas por vírgula. O *`target`* é atribuído sucessivamente a cada linha resultante do *`query`* e o corpo do loop é executado para cada linha. Aqui está um exemplo:

```
CREATE FUNCTION refresh_mviews() RETURNS integer AS $$
DECLARE
    mviews RECORD;
BEGIN
    RAISE NOTICE 'Refreshing all materialized views...';

    FOR mviews IN
       SELECT n.nspname AS mv_schema,
              c.relname AS mv_name,
              pg_catalog.pg_get_userbyid(c.relowner) AS owner
         FROM pg_catalog.pg_class c
    LEFT JOIN pg_catalog.pg_namespace n ON (n.oid = c.relnamespace)
        WHERE c.relkind = 'm'
     ORDER BY 1
    LOOP

        -- Now "mviews" has one record with information about the materialized view

        RAISE NOTICE 'Refreshing materialized view %.% (owner: %)...',
                     quote_ident(mviews.mv_schema),
                     quote_ident(mviews.mv_name),
                     quote_ident(mviews.owner);
        EXECUTE format('REFRESH MATERIALIZED VIEW %I.%I', mviews.mv_schema, mviews.mv_name);
    END LOOP;

    RAISE NOTICE 'Done refreshing materialized views.';
    RETURN 1;
END;
$$ LANGUAGE plpgsql;
```

Se o loop for finalizado por uma declaração `EXIT`, o último valor atribuído da linha ainda é acessível após o loop.

O *`query` usado neste tipo de declaração `FOR` pode ser qualquer comando SQL que retorne linhas para o solicitante: `SELECT` é o caso mais comum, mas você também pode usar `INSERT`, `UPDATE`, `DELETE` ou `MERGE` com uma cláusula `RETURNING`. Alguns comandos utilitários, como `EXPLAIN`, também funcionarão.

As variáveis PL/pgSQL são substituídas por parâmetros de consulta, e o plano de consulta é armazenado em cache para possível reutilização, conforme discutido em detalhes na [Seção 41.11.1] (plpgsql-implementation.md#PLPGSQL-VAR-SUBST "41.11.1. Variable Substitution") e [Seção 41.11.2] (plpgsql-implementation.md#PLPGSQL-PLAN-CACHING "41.11.2. Plan Caching").

A declaração `FOR-IN-EXECUTE` é outra maneira de iterar sobre linhas:

```
[ <<label>> ]
FOR target IN EXECUTE text_expression [ USING expression [, ... ] ] LOOP
    statements
END LOOP [ label ];
```

Isso é semelhante à forma anterior, exceto que a consulta de origem é especificada como uma expressão em cadeia, que é avaliada e reprojetada em cada entrada no loop `FOR`. Isso permite que o programador escolha a velocidade de uma consulta pré-planejada ou a flexibilidade de uma consulta dinâmica, assim como com uma simples declaração `EXECUTE`. Assim como em `EXECUTE`, os valores dos parâmetros podem ser inseridos no comando dinâmico via `USING`.

Outra maneira de especificar a consulta cujos resultados devem ser iterados é declará-la como um cursor. Isso é descrito em [Seção 41.7.4](plpgsql-cursors.md#PLPGSQL-CURSOR-FOR-LOOP).

### 41.6.7. Percorrer matrizes em laço [#](#PLPGSQL-FOREACH-ARRAY)

O loop `FOREACH` é muito semelhante ao loop `FOR`, mas, em vez de iterar pelas linhas retornadas por uma consulta SQL, ele itera pelos elementos de um valor de matriz. (Em geral, `FOREACH` é destinado a fazer o loop por componentes de uma expressão de valor composto; variantes para fazer o loop por compostos além de matrizes podem ser adicionadas no futuro.) A declaração `FOREACH` para fazer o loop por uma matriz é:

```
[ <<label>> ]
FOREACH target [ SLICE number ] IN ARRAY expression LOOP
    statements
END LOOP [ label ];
```

Sem `SLICE`, ou se `SLICE 0` for especificado, o loop itera por elementos individuais da matriz produzida pela avaliação do *`expression`*. A variável *`target`* recebe o valor de cada elemento em sequência, e o corpo do loop é executado para cada elemento. Aqui está um exemplo de loop por elementos de uma matriz de inteiros:

```
CREATE FUNCTION sum(int[]) RETURNS int8 AS $$
DECLARE
  s int8 := 0;
  x int;
BEGIN
  FOREACH x IN ARRAY $1
  LOOP
    s := s + x;
  END LOOP;
  RETURN s;
END;
$$ LANGUAGE plpgsql;
```

Os elementos são visitados em ordem de armazenamento, independentemente do número de dimensões da matriz. Embora o *`target`* geralmente seja apenas uma única variável, ele pode ser uma lista de variáveis ao percorrer uma matriz de valores compostos (registros). Nesse caso, para cada elemento da matriz, as variáveis são atribuídas a partir de colunas sucessivas do valor composto.

Com um valor positivo de `SLICE`, `FOREACH` percorre fatias do array em vez de elementos individuais. O valor de `SLICE` deve ser uma constante inteira não maior que o número de dimensões do array. A variável *`target`* deve ser um array, e ela recebe fatias sucessivas do valor do array, onde cada fatia tem o número de dimensões especificadas por `SLICE`. Aqui está um exemplo de iteração por fatias unidimensionais:

```
CREATE FUNCTION scan_rows(int[]) RETURNS void AS $$
DECLARE
  x int[];
BEGIN
  FOREACH x SLICE 1 IN ARRAY $1
  LOOP
    RAISE NOTICE 'row = %', x;
  END LOOP;
END;
$$ LANGUAGE plpgsql;

SELECT scan_rows(ARRAY[[1,2,3],[4,5,6],[7,8,9],[10,11,12]]);

NOTICE:  row = {1,2,3}
NOTICE:  row = {4,5,6}
NOTICE:  row = {7,8,9}
NOTICE:  row = {10,11,12}
```

### 41.6.8. Erros de captura [#](#PLPGSQL-ERROR-TRAPPING)

Por padrão, qualquer erro que ocorra em uma função PL/pgSQL interrompe a execução da função e da transação envolvente. Você pode capturar erros e se recuperar deles usando um bloco `BEGIN` com uma cláusula `EXCEPTION`. A sintaxe é uma extensão da sintaxe normal para um bloco `BEGIN`:

```
[ <<label>> ]
[ DECLARE
    declarations ]
BEGIN
    statements
EXCEPTION
    WHEN condition [ OR condition ... ] THEN
        handler_statements
    [ WHEN condition [ OR condition ... ] THEN
          handler_statements
      ... ]
END;
```

Se não ocorrer nenhum erro, essa forma de bloqueio simplesmente executa todos os *`statements`*, e então o controle passa para a próxima declaração após `END`. Mas se ocorrer um erro dentro do *`statements`*, o processamento adicional do *`statements`* é abandonado, e o controle passa para a lista `EXCEPTION`. A lista é pesquisada para o primeiro *`condition`* que corresponda ao erro que ocorreu. Se uma correspondência for encontrada, os *`handler_statements`* correspondentes são executados, e então o controle passa para a próxima declaração após `END`. Se não for encontrada nenhuma correspondência, o erro se propaga como se a cláusula `EXCEPTION` não estivesse lá em tudo: o erro pode ser detectado por um bloco envolvente com `EXCEPTION`, ou se não houver nenhum, ele interrompe o processamento da função.

Os nomes *`condition`* podem ser qualquer um dos mostrados em [Apêndice A](errcodes-appendix.md "Appendix A. PostgreSQL Error Codes"). Um nome de condição corresponde a qualquer erro dentro de sua categoria. O nome da condição especial `OTHERS` corresponde a todo tipo de erro, exceto `QUERY_CANCELED` e `ASSERT_FAILURE`. (É possível, mas muitas vezes imprudente, capturar esses dois tipos de erro pelo nome.) Os nomes das condições não são sensíveis ao caso. Além disso, uma condição de erro pode ser especificada pelo código `SQLSTATE`; por exemplo, estes são equivalentes:

```
WHEN division_by_zero THEN ...
WHEN SQLSTATE '22012' THEN ...
```

Se um novo erro ocorrer dentro do *`handler_statements`* selecionado, ele não pode ser detectado por esta cláusula `EXCEPTION`, mas é propagado. Uma cláusula `EXCEPTION` circundante poderia detectá-lo.

Quando um erro é detectado por uma cláusula `EXCEPTION`, as variáveis locais da função PL/pgSQL permanecem como estavam quando o erro ocorreu, mas todas as alterações no estado persistente do banco de dados dentro do bloco são revertidas. Como exemplo, considere este fragmento:

```
INSERT INTO mytab(firstname, lastname) VALUES('Tom', 'Jones');
BEGIN
    UPDATE mytab SET firstname = 'Joe' WHERE lastname = 'Jones';
    x := x + 1;
    y := x / 0;
EXCEPTION
    WHEN division_by_zero THEN
        RAISE NOTICE 'caught division_by_zero';
        RETURN x;
END;
```

Quando o controle atingir a atribuição para `y`, ele falhará com um erro `division_by_zero`. Isso será detectado pela cláusula `EXCEPTION`. O valor retornado na declaração `RETURN` será o valor incrementado de `x`, mas os efeitos do comando `UPDATE` terão sido revertidos. O comando `INSERT` que precede o bloco, no entanto, não é revertido, portanto, o resultado final é que o banco de dados contém `Tom Jones` e não `Joe Jones`.

DICA

Um bloco que contém uma cláusula `EXCEPTION` é significativamente mais caro para entrar e sair do que um bloco sem uma. Portanto, não use `EXCEPTION` sem necessidade.

**Exemplo 41.2. Exceções com `UPDATE`/`INSERT`**

Este exemplo usa o tratamento de exceções para realizar `UPDATE` ou `INSERT`, conforme apropriado. Recomenda-se que as aplicações usem `INSERT` com `ON CONFLICT DO UPDATE` em vez de realmente usar este padrão. Este exemplo serve principalmente para ilustrar o uso das estruturas de fluxo de controle do PL/pgSQL:

```
CREATE TABLE db (a INT PRIMARY KEY, b TEXT);

CREATE FUNCTION merge_db(key INT, data TEXT) RETURNS VOID AS
$$
BEGIN
    LOOP
        -- first try to update the key
        UPDATE db SET b = data WHERE a = key;
        IF found THEN
            RETURN;
        END IF;
        -- not there, so try to insert the key
        -- if someone else inserts the same key concurrently,
        -- we could get a unique-key failure
        BEGIN
            INSERT INTO db(a,b) VALUES (key, data);
            RETURN;
        EXCEPTION WHEN unique_violation THEN
            -- Do nothing, and loop to try the UPDATE again.
        END;
    END LOOP;
END;
$$
LANGUAGE plpgsql;

SELECT merge_db(1, 'david');
SELECT merge_db(1, 'dennis');
```

Essa codificação assume que o erro `unique_violation` é causado pelo `INSERT`, e não, por exemplo, por um `INSERT` em uma função de gatilho na tabela. Também pode se comportar mal se houver mais de um índice único na tabela, pois ele repetirá a operação independentemente do índice que causou o erro. Mais segurança pode ser obtida usando as características discutidas a seguir para verificar se o erro capturado era o esperado.



#### 41.6.8.1. Obter informações sobre um erro [#](#PLPGSQL-EXCEPTION-DIAGNOSTICS)

Os manipuladores de exceções frequentemente precisam identificar o erro específico que ocorreu. Existem duas maneiras de obter informações sobre a exceção atual no PL/pgSQL: variáveis especiais e o comando `GET STACKED DIAGNOSTICS`.

Dentro de um manipulador de exceção, a variável especial `SQLSTATE` contém o código de erro que corresponde à exceção que foi levantada (consulte [Tabela A.1](errcodes-appendix.md#ERRCODES-TABLE) para uma lista de códigos de erro possíveis). A variável especial `SQLERRM` contém a mensagem de erro associada à exceção. Essas variáveis são indefinidas fora dos manipuladores de exceção.

Dentro de um manipulador de exceção, também é possível recuperar informações sobre a exceção atual usando o comando `GET STACKED DIAGNOSTICS`, que tem a seguinte forma:

```
GET STACKED DIAGNOSTICS variable { = | := } item [ , ... ];
```

Cada *`item`* é uma palavra-chave que identifica um valor de status a ser atribuído ao *`variable`* especificado (que deve ter o tipo de dado correto para recebê-lo). Os itens de status atualmente disponíveis são mostrados na [Tabela 41.2](plpgsql-control-structures.md#PLPGSQL-EXCEPTION-DIAGNOSTICS-VALUES "Table 41.2. Error Diagnostics Items").

**Tabela 41.2. Itens de Diagnóstico de Erros**



<table>
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
  <col class="col3"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Name
   </th>
   <th>
    Type
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     RETURNED_SQLSTATE
    </code>
   </td>
   <td>
    <code>
     text
    </code>
   </td>
   <td>
    o código de erro SQLSTATE da exceção
   </td>
  </tr>
  <tr>
   <td>
    <code>
     COLUMN_NAME
    </code>
   </td>
   <td>
    <code>
     text
    </code>
   </td>
   <td>
    o nome da coluna relacionada à exceção
   </td>
  </tr>
  <tr>
   <td>
    <code>
     CONSTRAINT_NAME
    </code>
   </td>
   <td>
    <code>
     text
    </code>
   </td>
   <td>
    o nome da restrição relacionada à exceção
   </td>
  </tr>
  <tr>
   <td>
    <code>
     PG_DATATYPE_NAME
    </code>
   </td>
   <td>
    <code>
     text
    </code>
   </td>
   <td>
    o nome do tipo de dados relacionado à exceção
   </td>
  </tr>
  <tr>
   <td>
    <code>
     MESSAGE_TEXT
    </code>
   </td>
   <td>
    <code>
     text
    </code>
   </td>
   <td>
    o texto da mensagem principal da exceção
   </td>
  </tr>
  <tr>
   <td>
    <code>
     TABLE_NAME
    </code>
   </td>
   <td>
    <code>
     text
    </code>
   </td>
   <td>
    o nome da tabela relacionada à exceção
   </td>
  </tr>
  <tr>
   <td>
    <code>
     SCHEMA_NAME
    </code>
   </td>
   <td>
    <code>
     text
    </code>
   </td>
   <td>
    o nome do esquema relacionado à exceção
   </td>
  </tr>
  <tr>
   <td>
    <code>
     PG_EXCEPTION_DETAIL
    </code>
   </td>
   <td>
    <code>
     text
    </code>
   </td>
   <td>
    o texto da mensagem de detalhe da exceção, se houver
   </td>
  </tr>
  <tr>
   <td>
    <code>
     PG_EXCEPTION_HINT
    </code>
   </td>
   <td>
    <code>
     text
    </code>
   </td>
   <td>
    o texto da mensagem de dica da exceção, se houver
   </td>
  </tr>
  <tr>
   <td>
    <code>
     PG_EXCEPTION_CONTEXT
    </code>
   </td>
   <td>
    <code>
     text
    </code>
   </td>
   <td>
    linha(s) de texto descrevendo a pilha de chamadas no momento da exceção (ver
    <a class="xref" href="plpgsql-control-structures.md#PLPGSQL-CALL-STACK" title="41.6.9. Obtaining Execution Location Information">
     Seção 41.6.9
    </a>
    )
   </td>
  </tr>
 </tbody>
</table>










Se a exceção não definir um valor para um item, uma string vazia será devolvida.

Aqui está um exemplo:

```
DECLARE
  text_var1 text;
  text_var2 text;
  text_var3 text;
BEGIN
  -- some processing which might cause an exception
  ...
EXCEPTION WHEN OTHERS THEN
  GET STACKED DIAGNOSTICS text_var1 = MESSAGE_TEXT,
                          text_var2 = PG_EXCEPTION_DETAIL,
                          text_var3 = PG_EXCEPTION_HINT;
END;
```

### 41.6.9. Obter informações sobre a localização da execução [#](#PLPGSQL-CALL-STACK)

O comando `GET DIAGNOSTICS`, descrito anteriormente na [Seção 41.5.5](plpgsql-statements.md#PLPGSQL-STATEMENTS-DIAGNOSTICS), recupera informações sobre o estado atual de execução (enquanto o comando `GET STACKED DIAGNOSTICS`, discutido acima, relata informações sobre o estado de execução a partir de um erro anterior). Seu item de status `PG_CONTEXT` é útil para identificar a localização atual de execução. `PG_CONTEXT` retorna uma string de texto com(s) linha(s) de texto descrevendo a pilha de chamadas. A primeira linha se refere à função atual e ao comando `GET DIAGNOSTICS` atualmente em execução. A segunda e quaisquer linhas subsequentes se referem a funções chamadas mais acima na pilha de chamadas. Por exemplo:

```
CREATE OR REPLACE FUNCTION outer_func() RETURNS integer AS $$
BEGIN
  RETURN inner_func();
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION inner_func() RETURNS integer AS $$
DECLARE
  stack text;
BEGIN
  GET DIAGNOSTICS stack = PG_CONTEXT;
  RAISE NOTICE E'--- Call Stack ---\n%', stack;
  RETURN 1;
END;
$$ LANGUAGE plpgsql;

SELECT outer_func();

NOTICE:  --- Call Stack ---
PL/pgSQL function inner_func() line 5 at GET DIAGNOSTICS
PL/pgSQL function outer_func() line 3 at RETURN
CONTEXT:  PL/pgSQL function outer_func() line 3 at RETURN
 outer_func
 ------------
           1
(1 row)
```

`GET STACKED DIAGNOSTICS ... PG_EXCEPTION_CONTEXT` retorna o mesmo tipo de rastreamento de pilha, mas descrevendo a localização na qual um erro foi detectado, em vez da localização atual.
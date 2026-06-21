## 36.5. Linguagem de consulta (SQL) [#](#XFUNC-SQL)

* [36.5.1. Argumentos para Funções SQL][(xfunc-sql.md#XFUNC-SQL-FUNCTION-ARGUMENTS)]
* [36.5.2. Funções SQL em Tipos Básicos][(xfunc-sql.md#XFUNC-SQL-BASE-FUNCTIONS)]
* [36.5.3. Funções SQL em Tipos Compostos][(xfunc-sql.md#XFUNC-SQL-COMPOSITE-FUNCTIONS)]
* [36.5.4. Funções SQL com Parâmetros de Saída][(xfunc-sql.md#XFUNC-OUTPUT-PARAMETERS)]
* [36.5.5. Procedimentos SQL com Parâmetros de Saída][(xfunc-sql.md#XFUNC-OUTPUT-PARAMETERS-PROC)]
* [36.5.6. Funções SQL com Número Variável de Argumentos][(xfunc-sql.md#XFUNC-SQL-VARIADIC-FUNCTIONS)]
* [36.5.7. Funções SQL com Valores Padrão para Argumentos][(xfunc-sql.md#XFUNC-SQL-PARAMETER-DEFAULTS)]
* [36.5.8. Funções SQL como Fontes de Tabela][(xfunc-sql.md#XFUNC-SQL-TABLE-FUNCTIONS)]
* [36.5.9. Funções SQL que Retornam Conjuntos][(xfunc-sql.md#XFUNC-SQL-FUNCTIONS-RETURNING-SET)]
* [36.5.10. Funções SQL que Retornam `TABLE`][(xfunc-sql.md#XFUNC-SQL-FUNCTIONS-RETURNING-TABLE)]
* [36.5.11. Funções SQL Polimorfas][(xfunc-sql.md#XFUNC-SQL-POLYMORPHIC-FUNCTIONS)]
* [36.5.12. Funções SQL com Colagens][(xfunc-sql.md#XFUNC-SQL-COLLATIONS)]

As funções SQL executam uma lista arbitrária de instruções SQL, retornando o resultado da última consulta na lista. No caso simples (não definido), a primeira linha do resultado da última consulta será devolvida. (Tenha em mente que a “primeira linha” de um resultado de várias linhas não é bem definida, a menos que você use `ORDER BY`. Se a última consulta não retornar nenhuma linha, o valor nulo será devolvido.

Alternativamente, uma função SQL pode ser declarada para retornar um conjunto (ou seja, várias linhas) especificando o tipo de retorno da função como `SETOF sometype`, ou, de forma equivalente, declarando-a como `RETURNS TABLE(columns)`. Neste caso, todas as linhas do resultado da última consulta são retornadas. Mais detalhes aparecem abaixo.

O corpo de uma função SQL deve ser uma lista de instruções SQL separadas por pontos e virgulas. Um ponto e vírgula após a última instrução é opcional. A menos que a função seja declarada para retornar `void`, a última instrução deve ser uma `SELECT`, ou uma `INSERT`, `UPDATE`, `DELETE`, ou `MERGE` que tenha uma cláusula `RETURNING`.

Qualquer coleção de comandos no idioma SQL pode ser embalada e definida como uma função. Além das consultas `SELECT`, os comandos podem incluir consultas de modificação de dados (`INSERT`, `UPDATE`, `DELETE` e `MERGE`), bem como outros comandos SQL. (Você não pode usar comandos de controle de transação, por exemplo, `COMMIT`, `SAVEPOINT` e alguns comandos utilitários, por exemplo, `VACUUM`, em funções SQL. No entanto, o comando final deve ser um `SELECT` ou ter uma cláusula `RETURNING` que retorne o que for especificado como o tipo de retorno do função. Alternativamente, se você deseja definir uma função SQL que realize ações, mas não tenha um valor útil para retornar, pode defini-la como retornando `void`. Por exemplo, esta função remove linhas com salários negativos da tabela `emp`:

```
CREATE FUNCTION clean_emp() RETURNS void AS '
    DELETE FROM emp
        WHERE salary < 0;
' LANGUAGE SQL;

SELECT clean_emp();

 clean_emp
-----------

(1 row)
```

Você também pode escrever isso como um procedimento, evitando assim o problema do tipo de retorno. Por exemplo:

```
CREATE PROCEDURE clean_emp() AS '
    DELETE FROM emp
        WHERE salary < 0;
' LANGUAGE SQL;

CALL clean_emp();
```

Em casos simples como este, a diferença entre uma função que retorna `void` e um procedimento é, na maioria dos casos, estilística. No entanto, os procedimentos oferecem funcionalidades adicionais, como controle de transação que não estão disponíveis em funções. Além disso, os procedimentos são padrão SQL, enquanto retornar `void` é uma extensão do PostgreSQL.

A sintaxe do comando `CREATE FUNCTION` exige que o corpo da função seja escrito como uma constante de string. Geralmente, é mais conveniente usar aspas de dólar (ver [Seção 4.1.2.4] (sql-syntax-lexical.md#SQL-SYNTAX-DOLLAR-QUOTING "4.1.2.4. Dollar-Quoted String Constants")) para a constante de string. Se você optar por usar a sintaxe regular de constante de string com aspas simples, deve duplicar as aspas simples (`'`) e barras invertidas (`\`) (assumindo a sintaxe de string de escape) no corpo da função (ver [Seção 4.1.2.1] (sql-syntax-lexical.md#SQL-SYNTAX-STRINGS "4.1.2.1. String Constants")).

### 36.5.1. Argumentos para funções SQL [#](#XFUNC-SQL-FUNCTION-ARGUMENTS)

Os argumentos de uma função SQL podem ser referenciados no corpo da função usando nomes ou números. Exemplos de ambos os métodos aparecem abaixo.

Para usar um nome, declare o argumento da função como tendo um nome e, em seguida, escreva esse nome no corpo da função. Se o nome do argumento for o mesmo que qualquer nome de coluna no comando SQL atual dentro da função, o nome da coluna terá precedência. Para sobrescrever isso, qualifique o nome do argumento com o nome da própria função, ou seja, `function_name.argument_name`. (Se isso entrar em conflito com um nome de coluna qualificado, novamente o nome da coluna vence. Você pode evitar a ambiguidade escolhendo um alias diferente para a tabela dentro do comando SQL.)

Na abordagem numérica mais antiga, os argumentos são referenciados usando a sintaxe `$n`: `$1` refere-se ao primeiro argumento de entrada, `$2` ao segundo, e assim por diante. Isso funcionará independentemente de o argumento específico ter sido declarado com um nome ou

Se um argumento for de um tipo composto, então a notação de ponto, por exemplo, `argname.fieldname` ou `$1.fieldname`, pode ser usada para acessar os atributos do argumento. Novamente, você pode precisar qualificar o nome do argumento com o nome da função para tornar o formulário com um nome de argumento inconfundível.

Os argumentos das funções SQL só podem ser usados como valores de dados, não como identificadores. Assim, por exemplo, isso é razoável:

```
INSERT INTO mytable VALUES ($1);
```

mas isso não vai funcionar:

```
INSERT INTO $1 VALUES (42);
```

### Nota

A capacidade de usar nomes para referenciar argumentos de funções SQL foi adicionada no PostgreSQL 9.2. As funções que devem ser usadas em servidores mais antigos devem usar a notação `$n`.

### 36.5.2. Funções SQL em Tipos de Base [#](#XFUNC-SQL-BASE-FUNCTIONS)

A função SQL mais simples possível não tem argumentos e simplesmente retorna um tipo de base, como `integer`:

```
CREATE FUNCTION one() RETURNS integer AS $$
    SELECT 1 AS result;
$$ LANGUAGE SQL;

-- Alternative syntax for string literal:
CREATE FUNCTION one() RETURNS integer AS '
    SELECT 1 AS result;
' LANGUAGE SQL;

SELECT one();

 one
-----
   1
```

Observe que definimos um alias de coluna dentro do corpo da função para o resultado da função (com o nome `result`), mas esse alias de coluna não é visível fora da função. Portanto, o resultado é rotulado como `one` em vez de `result`.

É quase tão fácil definir funções SQL que aceitam tipos básicos como argumentos:

```
CREATE FUNCTION add_em(x integer, y integer) RETURNS integer AS $$
    SELECT x + y;
$$ LANGUAGE SQL;

SELECT add_em(1, 2) AS answer;

 answer
--------
      3
```

Alternativamente, poderíamos dispensar os nomes dos argumentos e usar números:

```
CREATE FUNCTION add_em(integer, integer) RETURNS integer AS $$
    SELECT $1 + $2;
$$ LANGUAGE SQL;

SELECT add_em(1, 2) AS answer;

 answer
--------
      3
```

Aqui está uma função mais útil, que pode ser usada para debitar uma conta bancária:

```
CREATE FUNCTION tf1 (accountno integer, debit numeric) RETURNS numeric AS $$
    UPDATE bank
        SET balance = balance - debit
        WHERE accountno = tf1.accountno;
    SELECT 1;
$$ LANGUAGE SQL;
```

Um usuário pode executar essa função para debitar a conta 17 por $100,00 da seguinte forma:

```
SELECT tf1(17, 100.0);
```

Neste exemplo, escolhemos o nome `accountno` para o primeiro argumento, mas este é o mesmo nome de uma coluna na tabela `bank`. Dentro do comando `UPDATE`, `accountno` refere-se à coluna `bank.accountno`, então `tf1.accountno` deve ser usado para referenciar o argumento. Obviamente, poderíamos evitar isso usando um nome diferente para o argumento.

Na prática, provavelmente se gostaria de um resultado mais útil da função do que um valor constante de 1, então uma definição mais provável é:

```
CREATE FUNCTION tf1 (accountno integer, debit numeric) RETURNS numeric AS $$
    UPDATE bank
        SET balance = balance - debit
        WHERE accountno = tf1.accountno;
    SELECT balance FROM bank WHERE accountno = tf1.accountno;
$$ LANGUAGE SQL;
```

que ajusta o saldo e retorna o novo saldo. A mesma coisa pode ser feita em um comando usando `RETURNING`:

```
CREATE FUNCTION tf1 (accountno integer, debit numeric) RETURNS numeric AS $$
    UPDATE bank
        SET balance = balance - debit
        WHERE accountno = tf1.accountno
    RETURNING balance;
$$ LANGUAGE SQL;
```

Se a cláusula final `SELECT` ou `RETURNING` em uma função SQL não retornar exatamente o tipo de resultado declarado da função, o PostgreSQL converterá automaticamente o valor para o tipo requerido, se isso for possível com uma conversão implícita ou de atribuição. Caso contrário, você deve escrever uma conversão explícita. Por exemplo, suponha que quiséssemos que a função anterior `add_em` retornasse o tipo `float8` em vez disso. É suficiente escrever

```
CREATE FUNCTION add_em(integer, integer) RETURNS float8 AS $$
    SELECT $1 + $2;
$$ LANGUAGE SQL;
```

já que a soma `integer` pode ser implicitamente convertida para `float8`. (Consulte o [Capítulo 10](typeconv.md "Chapter 10. Type Conversion") ou [CREATE CAST](sql-createcast.md "CREATE CAST") para mais informações sobre conversões.)

### 36.5.3. Funções SQL em Tipos Compostos [#](#XFUNC-SQL-COMPOSITE-FUNCTIONS)

Ao escrever funções com argumentos de tipos compostos, não devemos apenas especificar qual argumento queremos, mas também o atributo desejado (campo) desse argumento. Por exemplo, suponha que `emp` seja uma tabela contendo dados de funcionários, e, portanto, também o nome do tipo composto de cada linha da tabela. Aqui está uma função `double_salary` que calcula qual seria o salário de alguém se fosse dobrado:

```
CREATE TABLE emp (
    name        text,
    salary      numeric,
    age         integer,
    cubicle     point
);

INSERT INTO emp VALUES ('Bill', 4200, 45, '(2,1)');

CREATE FUNCTION double_salary(emp) RETURNS numeric AS $$
    SELECT $1.salary * 2 AS salary;
$$ LANGUAGE SQL;

SELECT name, double_salary(emp.*) AS dream
    FROM emp
    WHERE emp.cubicle ~= point '(2,1)';

 name | dream
------+-------
 Bill |  8400
```

Observe o uso da sintaxe `$1.salary` para selecionar um campo da linha de argumento. Também observe como o comando `SELECT` está usando *`table_name`*`.*` para selecionar toda a linha atual de uma tabela como um valor composto. A linha da tabela também pode ser referenciada alternativamente usando apenas o nome da tabela, como este:

```
SELECT name, double_salary(emp) AS dream
    FROM emp
    WHERE emp.cubicle ~= point '(2,1)';
```

Mas esse uso é desaconselhável, pois é fácil se confundir. (Consulte a [Seção 8.16.5] para obter detalhes sobre essas duas notações para o valor composto de uma linha de tabela.)

Às vezes, é útil construir um valor de argumento composto em tempo real. Isso pode ser feito com o construtor `ROW`. Por exemplo, podemos ajustar os dados que são passados para a função:

```
SELECT name, double_salary(ROW(name, salary*1.1, age, cubicle)) AS dream
    FROM emp;
```

Também é possível construir uma função que retorne um tipo composto. Este é um exemplo de uma função que retorna uma única linha `emp`:

```
CREATE FUNCTION new_emp() RETURNS emp AS $$
    SELECT text 'None' AS name,
        1000.0 AS salary,
        25 AS age,
        point '(2,2)' AS cubicle;
$$ LANGUAGE SQL;
```

Neste exemplo, especificamos cada um dos atributos com um valor constante, mas qualquer cálculo poderia ter sido substituído por essas constantes.

Observe duas coisas importantes sobre a definição da função:

* A ordem da lista selecionada na consulta deve ser exatamente a mesma em que as colunas aparecem no tipo composto. (Nomear as colunas, como fizemos acima, é irrelevante para o sistema.)
* Devemos garantir que o tipo de cada expressão possa ser convertido para o da coluna correspondente ao tipo composto. Caso contrário, obteremos erros como este:

  ```
  ERROR:  return type mismatch in function declared to return emp
  DETAIL:  Final statement returns text instead of point at column 4.
  ```

Assim como no caso do tipo de base, o sistema não inserirá casts explícitos automaticamente, apenas casts implícitos ou de atribuição.

Uma maneira diferente de definir a mesma função é:

```
CREATE FUNCTION new_emp() RETURNS emp AS $$
    SELECT ROW('None', 1000.0, 25, '(2,2)')::emp;
$$ LANGUAGE SQL;
```

Aqui, escrevemos um `SELECT` que retorna apenas uma única coluna do tipo composto correto. Isso não é realmente melhor nesta situação, mas é uma alternativa útil em alguns casos — por exemplo, se precisarmos calcular o resultado chamando outra função que retorne o valor composto desejado. Outro exemplo é que, se estivermos tentando escrever uma função que retorne um domínio sobre composto, em vez de um tipo composto simples, é sempre necessário escrevê-la como retornando uma única coluna, pois não há como causar uma coação do resultado da linha inteira.

Podemos chamar essa função diretamente, usando-a em uma expressão de valor:

```
SELECT new_emp();

         new_emp
--------------------------
 (None,1000.0,25,"(2,2)")
```

ou chamando-a como uma função de tabela:

```
SELECT * FROM new_emp();

 name | salary | age | cubicle
------+--------+-----+---------
 None | 1000.0 |  25 | (2,2)
```

A segunda maneira é descrita mais detalhadamente em [Seção 36.5.8][(xfunc-sql.md#XFUNC-SQL-TABLE-FUNCTIONS "36.5.8. SQL Functions as Table Sources")].

Quando você usa uma função que retorna um tipo composto, você pode querer apenas um campo (atributo) de seu resultado. Você pode fazer isso com a sintaxe desta forma:

```
SELECT (new_emp()).name;

 name
------
 None
```

As aspas extras são necessárias para evitar que o analisador fique confuso. Se você tentar fazer isso sem elas, você obtém algo como este:

```
SELECT new_emp().name;
ERROR:  syntax error at or near "."
LINE 1: SELECT new_emp().name;
                        ^
```

Outra opção é usar notação funcional para extrair um atributo:

```
SELECT name(new_emp());

 name
------
 None
```

Como explicado na [Seção 8.16.5][(rowtypes.md#ROWTYPES-USAGE "8.16.5. Using Composite Types in Queries")], a notação de campo e a notação funcional são equivalentes.

Outra maneira de usar uma função que retorna um tipo composto é passar o resultado para outra função que aceita o tipo de linha correto como entrada:

```
CREATE FUNCTION getname(emp) RETURNS text AS $$
    SELECT $1.name;
$$ LANGUAGE SQL;

SELECT getname(new_emp());
 getname
---------
 None
(1 row)
```

### 36.5.4. Funções SQL com Parâmetros de Saída [#](#XFUNC-OUTPUT-PARAMETERS)

Uma maneira alternativa de descrever os resultados de uma função é defini-la com *parâmetros de saída*, como neste exemplo:

```
CREATE FUNCTION add_em (IN x int, IN y int, OUT sum int)
AS 'SELECT x + y'
LANGUAGE SQL;

SELECT add_em(3,7);
 add_em
--------
     10
(1 row)
```

Isso não é essencialmente diferente da versão do `add_em` mostrada em [Seção 36.5.2][(xfunc-sql.md#XFUNC-SQL-BASE-FUNCTIONS "36.5.2. SQL Functions on Base Types")]. O verdadeiro valor dos parâmetros de saída é que eles fornecem uma maneira conveniente de definir funções que retornam várias colunas. Por exemplo,

```
CREATE FUNCTION sum_n_product (x int, y int, OUT sum int, OUT product int)
AS 'SELECT x + y, x * y'
LANGUAGE SQL;

 SELECT * FROM sum_n_product(11,42);
 sum | product
-----+---------
  53 |     462
(1 row)
```

O que essencialmente aconteceu aqui é que criamos um tipo composto anônimo para o resultado da função. O exemplo acima tem o mesmo resultado final que

```
CREATE TYPE sum_prod AS (sum int, product int);

CREATE FUNCTION sum_n_product (int, int) RETURNS sum_prod
AS 'SELECT $1 + $2, $1 * $2'
LANGUAGE SQL;
```

Mas não ter que se preocupar com a definição separada do tipo composto é muitas vezes útil. Observe que os nomes anexados aos parâmetros de saída não são apenas decoração, mas determinam os nomes das colunas do tipo composto anônimo. (Se você omitir um nome para um parâmetro de saída, o sistema escolherá um nome por si só.)

Observe que os parâmetros de saída não são incluídos na lista de argumentos de chamada ao invocar tal função a partir do SQL. Isso ocorre porque o PostgreSQL considera apenas os parâmetros de entrada para definir a assinatura de chamada da função. Isso significa que, também, apenas os parâmetros de entrada importam ao fazer referência à função para fins como sua eliminação. Podemos eliminar a função acima com qualquer uma das

```
DROP FUNCTION sum_n_product (x int, y int, OUT sum int, OUT product int);
DROP FUNCTION sum_n_product (int, int);
```

Os parâmetros podem ser marcados como `IN` (padrão), `OUT`, `INOUT` ou `VARIADIC`. Um parâmetro `INOUT` serve como um parâmetro de entrada (parte da lista de argumentos de chamada) e um parâmetro de saída (parte do tipo de registro de resultado). Os parâmetros `VARIADIC` são parâmetros de entrada, mas são tratados especialmente como descrito abaixo.

### 36.5.5. Procedimentos SQL com Parâmetros de Saída [#](#XFUNC-OUTPUT-PARAMETERS-PROC)

Os parâmetros de saída também são suportados em procedimentos, mas eles funcionam um pouco diferente das funções. Nos comandos `CALL`, os parâmetros de saída devem ser incluídos na lista de argumentos. Por exemplo, a rotina de débitos da conta bancária anterior pode ser escrita da seguinte forma:

```
CREATE PROCEDURE tp1 (accountno integer, debit numeric, OUT new_balance numeric) AS $$
    UPDATE bank
        SET balance = balance - debit
        WHERE accountno = tp1.accountno
    RETURNING balance;
$$ LANGUAGE SQL;
```

Para chamar esse procedimento, um argumento que corresponda ao parâmetro `OUT` deve ser incluído. É costume escrever `NULL`:

```
CALL tp1(17, 100.0, NULL);
```

Se você escrever algo mais, deve ser uma expressão que seja implicitamente coerente com o tipo declarado do parâmetro, assim como para os parâmetros de entrada. No entanto, observe que tal expressão não será avaliada.

Ao chamar um procedimento a partir do PL/pgSQL, em vez de escrever `NULL`, você deve escrever uma variável que receberá a saída do procedimento. Consulte [Seção 41.6.3][(plpgsql-control-structures.md#PLPGSQL-STATEMENTS-CALLING-PROCEDURE "41.6.3. Calling a Procedure")] para obter detalhes.

### 36.5.6. Funções SQL com Número Variável de Argumentos [#](#XFUNC-SQL-VARIADIC-FUNCTIONS)

As funções SQL podem ser declaradas para aceitar um número variável de argumentos, desde que todos os argumentos "opcionais" sejam do mesmo tipo de dados. Os argumentos opcionais serão passados à função como um array. A função é declarada marcando o último parâmetro como `VARIADIC`; este parâmetro deve ser declarado como sendo de um tipo de array. Por exemplo:

```
CREATE FUNCTION mleast(VARIADIC arr numeric[]) RETURNS numeric AS $$
    SELECT min($1[i]) FROM generate_subscripts($1, 1) g(i);
$$ LANGUAGE SQL;

SELECT mleast(10, -1, 5, 4.4);
 mleast
--------
     -1
(1 row)
```

Efetivamente, todos os argumentos reais na posição `VARIADIC` ou além dela são reunidos em um array unidimensional, como se você tivesse escrito

```
SELECT mleast(ARRAY[10, -1, 5, 4.4]);    -- doesn't work
```

Na verdade, você não pode escrever isso — ou, pelo menos, isso não corresponderá à definição dessa função. Um parâmetro marcado `VARIADIC` corresponde a uma ou mais ocorrências de seu tipo de elemento, não do seu próprio tipo.

Às vezes, é útil ser capaz de passar uma matriz já construída para uma função variável; isso é particularmente útil quando uma função variável deseja passar seu parâmetro de matriz para outra. Além disso, essa é a única maneira segura de chamar uma função variável encontrada em um esquema que permite que usuários não confiáveis criem objetos; veja [Seção 10.3][(typeconv-func.md "10.3. Functions")]. Você pode fazer isso especificando `VARIADIC` na chamada:

```
SELECT mleast(VARIADIC ARRAY[10, -1, 5, 4.4]);
```

Isso impede a expansão do parâmetro variadic da função em seu tipo de elemento, permitindo assim que o valor do argumento da matriz se ajuste normalmente. `VARIADIC` só pode ser anexado ao último argumento real de uma chamada de função.

Especificar `VARIADIC` na chamada é também a única maneira de passar um array vazio para uma função variável, por exemplo:

```
SELECT mleast(VARIADIC ARRAY[]::numeric[]);
```

Simplesmente escrever `SELECT mleast()` não funciona porque um parâmetro variável deve corresponder a pelo menos um argumento real. (Você poderia definir uma segunda função também com o nome `mleast`, sem parâmetros, se quisesse permitir tais chamadas.)

Os parâmetros dos elementos da matriz gerados a partir de um parâmetro variável são tratados como não tendo nomes próprios. Isso significa que não é possível chamar uma função variável usando argumentos nomeados ([Seção 4.3][(sql-syntax-calling-funcs.md "4.3. Calling Functions")]), exceto quando você especifica `VARIADIC`. Por exemplo, isso funcionará:

```
SELECT mleast(VARIADIC arr => ARRAY[10, -1, 5, 4.4]);
```

mas não estas:

```
SELECT mleast(arr => 10);
SELECT mleast(arr => ARRAY[10, -1, 5, 4.4]);
```

### 36.5.7. Funções SQL com valores padrão para argumentos [#](#XFUNC-SQL-PARAMETER-DEFAULTS)

As funções podem ser declaradas com valores padrão para alguns ou todos os argumentos de entrada. Os valores padrão são inseridos sempre que a função é chamada com um número insuficiente de argumentos reais. Como os argumentos só podem ser omitidos do final da lista de argumentos reais, todos os parâmetros após um parâmetro com um valor padrão devem ter valores padrão também. (Embora o uso da notação de argumentos nomeados possa permitir que essa restrição seja relaxada, ainda é aplicada para que a notação de argumentos posicionais funcione sensatamente.) Se você a usa ou não, essa capacidade cria a necessidade de precauções ao chamar funções em bancos de dados onde alguns usuários não confiam em outros usuários; veja [Seção 10.3] [(typeconv-func.md "10.3. Functions")].

Por exemplo:

```
CREATE FUNCTION foo(a int, b int DEFAULT 2, c int DEFAULT 3)
RETURNS int
LANGUAGE SQL
AS $$
    SELECT $1 + $2 + $3;
$$;

SELECT foo(10, 20, 30);
 foo
-----
  60
(1 row)

SELECT foo(10, 20);
 foo
-----
  33
(1 row)

SELECT foo(10);
 foo
-----
  15
(1 row)

SELECT foo();  -- fails since there is no default for the first argument
ERROR:  function foo() does not exist
```

O sinal `=` também pode ser usado no lugar da palavra-chave `DEFAULT`.

### 36.5.8. Funções SQL como fontes de tabela [#](#XFUNC-SQL-TABLE-FUNCTIONS)

Todas as funções SQL podem ser usadas na cláusula `FROM` de uma consulta, mas é particularmente útil para funções que retornam tipos compostos. Se a função for definida para retornar um tipo de base, a função de tabela produz uma tabela de um único campo. Se a função for definida para retornar um tipo composto, a função de tabela produz uma coluna para cada atributo do tipo composto.

Aqui está um exemplo:

```
CREATE TABLE foo (fooid int, foosubid int, fooname text);
INSERT INTO foo VALUES (1, 1, 'Joe');
INSERT INTO foo VALUES (1, 2, 'Ed');
INSERT INTO foo VALUES (2, 1, 'Mary');

CREATE FUNCTION getfoo(int) RETURNS foo AS $$
    SELECT * FROM foo WHERE fooid = $1;
$$ LANGUAGE SQL;

SELECT *, upper(fooname) FROM getfoo(1) AS t1;

 fooid | foosubid | fooname | upper
-------+----------+---------+-------
     1 |        1 | Joe     | JOE
(1 row)
```

Como o exemplo mostra, podemos trabalhar com as colunas do resultado da função da mesma forma que se tratasse de colunas de uma tabela comum.

Observe que só obtivemos uma linha da função. Isso ocorre porque não usamos `SETOF`. Isso é descrito na próxima seção.

### 36.5.9. Funções SQL que retornam conjuntos [#](#XFUNC-SQL-FUNCTIONS-RETURNING-SET)

Quando uma função SQL é declarada como retornando `SETOF sometype`, a consulta final da função é executada até o término, e cada linha que ela produz é devolvida como um elemento do conjunto de resultados.

Esse recurso é normalmente usado ao chamar a função na cláusula `FROM`. Nesse caso, cada linha devolvida pela função se torna uma linha da tabela vista pela consulta. Por exemplo, suponha que a tabela `foo` tenha o mesmo conteúdo que o acima, e digamos:

```
CREATE FUNCTION getfoo(int) RETURNS SETOF foo AS $$
    SELECT * FROM foo WHERE fooid = $1;
$$ LANGUAGE SQL;

SELECT * FROM getfoo(1) AS t1;
```

Então, teríamos:

```
 fooid | foosubid | fooname
-------+----------+---------
     1 |        1 | Joe
     1 |        2 | Ed
(2 rows)
```

Também é possível retornar várias linhas com as colunas definidas pelos parâmetros de saída, como este:

```
CREATE TABLE tab (y int, z int);
INSERT INTO tab VALUES (1, 2), (3, 4), (5, 6), (7, 8);

CREATE FUNCTION sum_n_product_with_tab (x int, OUT sum int, OUT product int)
RETURNS SETOF record
AS $$
    SELECT $1 + tab.y, $1 * tab.y FROM tab;
$$ LANGUAGE SQL;

SELECT * FROM sum_n_product_with_tab(10);
 sum | product
-----+---------
  11 |      10
  13 |      30
  15 |      50
  17 |      70
(4 rows)
```

O ponto chave aqui é que você deve escrever `RETURNS SETOF record` para indicar que a função retorna várias linhas em vez de apenas uma. Se houver apenas um parâmetro de saída, escreva o tipo desse parâmetro em vez de `record`.

É frequentemente útil construir o resultado de uma consulta invocando uma função que retorna um conjunto várias vezes, com os parâmetros para cada invocação provenientes de linhas sucessivas de uma tabela ou subconsulta. A maneira preferencial de fazer isso é usar a palavra-chave `LATERAL`, que é descrita em [Seção 7.2.1.5][(queries-table-expressions.md#QUERIES-LATERAL "7.2.1.5. LATERAL Subqueries")]. Aqui está um exemplo usando uma função que retorna um conjunto para enumerar elementos de uma estrutura de árvore:

```
SELECT * FROM nodes;
   name    | parent
-----------+--------
 Top       |
 Child1    | Top
 Child2    | Top
 Child3    | Top
 SubChild1 | Child1
 SubChild2 | Child1
(6 rows)

CREATE FUNCTION listchildren(text) RETURNS SETOF text AS $$
    SELECT name FROM nodes WHERE parent = $1
$$ LANGUAGE SQL STABLE;

SELECT * FROM listchildren('Top');
 listchildren
--------------
 Child1
 Child2
 Child3
(3 rows)

SELECT name, child FROM nodes, LATERAL listchildren(name) AS child;
  name  |   child
--------+-----------
 Top    | Child1
 Top    | Child2
 Top    | Child3
 Child1 | SubChild1
 Child1 | SubChild2
(5 rows)
```

Esse exemplo não faz nada que não pudéssemos fazer com uma simples junção, mas em cálculos mais complexos, a opção de colocar parte do trabalho em uma função pode ser bastante conveniente.

Funções que retornam conjuntos também podem ser chamadas na lista de seleção de uma consulta. Para cada linha que a consulta gera por si mesma, a função que retorna conjuntos é invocada, e uma linha de saída é gerada para cada elemento do conjunto de resultados da função. O exemplo anterior também pode ser feito com consultas como essas:

```
SELECT listchildren('Top');
 listchildren
--------------
 Child1
 Child2
 Child3
(3 rows)

SELECT name, listchildren(name) FROM nodes;
  name  | listchildren
--------+--------------
 Top    | Child1
 Top    | Child2
 Top    | Child3
 Child1 | SubChild1
 Child1 | SubChild2
(5 rows)
```

Na última `SELECT`, observe que nenhuma linha de saída aparece para `Child2`, `Child3`, etc. Isso acontece porque `listchildren` retorna um conjunto vazio para esses argumentos, então nenhuma linha de resultado é gerada. Esse é o mesmo comportamento que obtivemos de uma junção interna ao resultado da função ao usar a sintaxe `LATERAL`.

O comportamento do PostgreSQL para uma função que retorna um conjunto na lista select de uma consulta é quase exatamente o mesmo como se a função que retorna o conjunto tivesse sido escrita em um item da cláusula `LATERAL FROM`. Por exemplo,

```
SELECT x, generate_series(1,5) AS g FROM tab;
```

é quase equivalente a

```
SELECT x, g FROM tab, LATERAL generate_series(1,5) AS g;
```

Seria exatamente o mesmo, exceto que, neste exemplo específico, o planejador poderia optar por colocar `g` no lado de fora da junção de laços aninhados, uma vez que `g` não tem dependência lateral real em `tab`. Isso resultaria em uma ordem diferente das linhas de saída. As funções que retornam conjuntos na lista de seleção são sempre avaliadas como se estivessem no interior de uma junção de laços aninhados com o resto da cláusula `FROM`, de modo que as funções são executadas até o fim antes de considerar a próxima linha da cláusula `FROM`.

Se houver mais de um conjunto de funções de retorno na lista de seleção da consulta, o comportamento é semelhante ao que se obtém ao colocar as funções em um único item da cláusula `LATERAL ROWS FROM( ... )` `FROM`. Para cada linha da consulta subjacente, há uma linha de saída usando o primeiro resultado de cada função, seguida de uma linha de saída usando o segundo resultado, e assim por diante. Se algumas das funções de retorno de conjunto produzem menos saídas do que outras, valores nulos são substituídos pelos dados ausentes, de modo que o número total de linhas emitidas para uma linha subjacente seja o mesmo para a função de retorno de conjunto que produziu o maior número de saídas. Assim, as funções de retorno de conjunto são executadas “em sintonia” até que todas sejam esgotadas, e então a execução continua com a próxima linha subjacente.

As funções de retorno de conjunto podem ser aninhadas em uma lista selecionada, embora isso não seja permitido em itens de cláusulas `FROM`. Nesses casos, cada nível de aninhamento é tratado separadamente, como se fosse um item `LATERAL ROWS FROM( ... )` separado. Por exemplo, em

```
SELECT srf1(srf2(x), srf3(y)), srf4(srf5(z)) FROM tab;
```

as funções de retorno de conjunto `srf2`, `srf3` e `srf5` seriam executadas em sincronia para cada linha de `tab`, e então `srf1` e `srf4` seriam aplicados em sincronia para cada linha produzida pelas funções inferiores.

As funções de retorno de conjunto não podem ser usadas em construções de avaliação condicional, como `CASE` ou `COALESCE`. Por exemplo, considere

```
SELECT x, CASE WHEN x > 0 THEN generate_series(1, 5) ELSE 0 END FROM tab;
```

Pode parecer que isso deve produzir cinco repetições de linhas de entrada que têm `x > 0`, e uma única repetição das que não têm; mas, na verdade, porque `generate_series(1, 5)` seria executado em um item implícito `LATERAL FROM` antes que a expressão `CASE` seja avaliada, ele produziria cinco repetições de cada linha de entrada. Para reduzir a confusão, esses casos produzem um erro de tempo de análise em vez disso.

### Nota

Se o último comando de uma função for `INSERT`, `UPDATE`, `DELETE` ou `MERGE` com `RETURNING`, esse comando será sempre executado até o final, mesmo que a função não seja declarada com `SETOF` ou se a consulta que a chama não extrair todas as linhas do resultado. Quaisquer linhas extras produzidas pela cláusula `RETURNING` são silenciosamente descartadas, mas as modificações de tabela comandadas ainda acontecem (e todas são concluídas antes de retornar da função).

### Nota

Antes do PostgreSQL 10, colocar mais de uma função que retorna um conjunto na mesma lista de seleção não se comportava de forma sensível, a menos que elas sempre produzissem números iguais de linhas. Caso contrário, o que você obteve foi um número de linhas de saída igual ao mínimo múltiplo comum dos números de linhas produzidos pelas funções que retornam um conjunto. Além disso, as funções que retornam um conjunto aninhadas não funcionavam como descrito acima; em vez disso, uma função que retorna um conjunto poderia ter no máximo um argumento que retorna um conjunto, e cada ninho de funções que retornam um conjunto era executado de forma independente. Além disso, a execução condicional (funções que retornam um conjunto dentro de `CASE` etc.) era anteriormente permitida, complicando ainda mais as coisas. É recomendado o uso da sintaxe `LATERAL` ao escrever consultas que precisam funcionar em versões anteriores do PostgreSQL, porque isso dará resultados consistentes em diferentes versões. Se você tem uma consulta que depende da execução condicional de uma função que retorna um conjunto, você pode ser capaz de corrigir isso movendo o teste condicional para uma função que retorna um conjunto personalizada. Por exemplo,

```
SELECT x, CASE WHEN y > 0 THEN generate_series(1, z) ELSE 5 END FROM tab;
```

poderia se tornar

```
CREATE FUNCTION case_generate_series(cond bool, start int, fin int, els int)
  RETURNS SETOF int AS $$
BEGIN
  IF cond THEN
    RETURN QUERY SELECT generate_series(start, fin);
  ELSE
    RETURN QUERY SELECT els;
  END IF;
END$$ LANGUAGE plpgsql;

SELECT x, case_generate_series(y > 0, 1, z, 5) FROM tab;
```

Essa formulação funcionará da mesma forma em todas as versões do PostgreSQL.

### 36.5.10. Funções SQL que retornam `TABLE` [#](#XFUNC-SQL-FUNCTIONS-RETURNING-TABLE)

Existe outra maneira de declarar uma função como retornando um conjunto, que é usar a sintaxe `RETURNS TABLE(columns)`. Isso é equivalente a usar um ou mais parâmetros `OUT` e marcar a função como retornando `SETOF record` (ou `SETOF` um único parâmetro de saída, conforme apropriado). Essa notação é especificada em versões recentes do padrão SQL, e, portanto, pode ser mais portátil do que usar `SETOF`.

Por exemplo, o exemplo anterior de soma e produto também pode ser feito dessa maneira:

```
CREATE FUNCTION sum_n_product_with_tab (x int)
RETURNS TABLE(sum int, product int) AS $$
    SELECT $1 + tab.y, $1 * tab.y FROM tab;
$$ LANGUAGE SQL;
```

Não é permitido usar explicitamente os parâmetros `OUT` ou `INOUT` com a notação `RETURNS TABLE` — você deve colocar todas as colunas de saída na lista `TABLE`.

### 36.5.11. Funções SQL polimórficas [#](#XFUNC-SQL-POLYMORPHIC-FUNCTIONS)

As funções SQL podem ser declaradas para aceitar e retornar os tipos polimórficos descritos em [Seção 36.2.5][(extend-type-system.md#EXTEND-TYPES-POLYMORPHIC "36.2.5. Polymorphic Types")]. Aqui está uma função polimórfica `make_array` que constrói um array a partir de dois elementos de tipos de dados arbitrários:

```
CREATE FUNCTION make_array(anyelement, anyelement) RETURNS anyarray AS $$
    SELECT ARRAY[$1, $2];
$$ LANGUAGE SQL;

SELECT make_array(1, 2) AS intarray, make_array('a'::text, 'b') AS textarray;
 intarray | textarray
----------+-----------
 {1,2}    | {a,b}
(1 row)
```

Observe o uso do typecast `'a'::text` para especificar que o argumento é do tipo `text`. Isso é necessário se o argumento for apenas uma literal de string, pois, caso contrário, seria tratado como tipo `unknown`, e o array de `unknown` não é um tipo válido. Sem o typecast, você receberá erros como este:

```
ERROR:  could not determine polymorphic type because input has type unknown
```

Com `make_array` declarado acima, você deve fornecer dois argumentos que sejam exatamente do mesmo tipo de dados; o sistema não tentará resolver quaisquer diferenças de tipo. Assim, por exemplo, isso não funciona:

```
SELECT make_array(1, 2.5) AS numericarray;
ERROR:  function make_array(integer, numeric) does not exist
```

Uma abordagem alternativa é usar a família "comum" de tipos polimórficos, que permite ao sistema tentar identificar um tipo comum adequado:

```
CREATE FUNCTION make_array2(anycompatible, anycompatible)
RETURNS anycompatiblearray AS $$
    SELECT ARRAY[$1, $2];
$$ LANGUAGE SQL;

SELECT make_array2(1, 2.5) AS numericarray;
 numericarray
--------------
 {1,2.5}
(1 row)
```

Como as regras para resolução de tipo comum têm como padrão a escolha do tipo `text` quando todos os inputs são de tipos desconhecidos, isso também funciona:

```
SELECT make_array2('a', 'b') AS textarray;
 textarray
-----------
 {a,b}
(1 row)
```

É permitido ter argumentos polimórficos com um tipo de retorno fixo, mas o contrário não é permitido. Por exemplo:

```
CREATE FUNCTION is_greater(anyelement, anyelement) RETURNS boolean AS $$
    SELECT $1 > $2;
$$ LANGUAGE SQL;

SELECT is_greater(1, 2);
 is_greater
------------
 f
(1 row)

CREATE FUNCTION invalid_func() RETURNS anyelement AS $$
    SELECT 1;
$$ LANGUAGE SQL;
ERROR:  cannot determine result data type
DETAIL:  A result of type anyelement requires at least one input of type anyelement, anyarray, anynonarray, anyenum, or anyrange.
```

O polimorfismo pode ser usado com funções que têm argumentos de saída. Por exemplo:

```
CREATE FUNCTION dup (f1 anyelement, OUT f2 anyelement, OUT f3 anyarray)
AS 'select $1, array[$1,$1]' LANGUAGE SQL;

SELECT * FROM dup(22);
 f2 |   f3
----+---------
 22 | {22,22}
(1 row)
```

O polimorfismo também pode ser usado com funções variáveis. Por exemplo:

```
CREATE FUNCTION anyleast (VARIADIC anyarray) RETURNS anyelement AS $$
    SELECT min($1[i]) FROM generate_subscripts($1, 1) g(i);
$$ LANGUAGE SQL;

SELECT anyleast(10, -1, 5, 4);
 anyleast
----------
       -1
(1 row)

SELECT anyleast('abc'::text, 'def');
 anyleast
----------
 abc
(1 row)

CREATE FUNCTION concat_values(text, VARIADIC anyarray) RETURNS text AS $$
    SELECT array_to_string($2, $1);
$$ LANGUAGE SQL;

SELECT concat_values('|', 1, 4, 2);
 concat_values
---------------
 1|4|2
(1 row)
```

### 36.5.12. Funções SQL com Colagens [#](#XFUNC-SQL-COLLATIONS)

Quando uma função SQL tem um ou mais parâmetros de tipos de dados colidíveis, uma codificação é identificada para cada chamada de função, dependendo das codificações atribuídas aos argumentos reais, conforme descrito em [Seção 23.2][(collation.md "23.2. Collation Support")]. Se uma codificação for identificada com sucesso (ou seja, não houver conflitos de codificações implícitas entre os argumentos), todos os parâmetros colidíveis são tratados como tendo aquela codificação implicitamente. Isso afetará o comportamento das operações sensíveis à codificação dentro da função. Por exemplo, usando a função `anyleast` descrita acima, o resultado de

```
SELECT anyleast('abc'::text, 'ABC');
```

Dependerá da collation padrão do banco de dados. No local `C`, o resultado será `ABC`, mas em muitos outros locais, será `abc`. A collation a ser usada pode ser forçada adicionando uma cláusula `COLLATE` a qualquer um dos argumentos, por exemplo:

```
SELECT anyleast('abc'::text, 'ABC' COLLATE "C");
```

Como alternativa, se você deseja que uma função opere com uma determinada ordenação, independentemente do nome que ela recebe, insira cláusulas `COLLATE` conforme necessário na definição da função. Esta versão do `anyleast` sempre usaria o local `en_US` para comparar strings:

```
CREATE FUNCTION anyleast (VARIADIC anyarray) RETURNS anyelement AS $$
    SELECT min($1[i] COLLATE "en_US") FROM generate_subscripts($1, 1) g(i);
$$ LANGUAGE SQL;
```

Mas observe que isso lançará um erro se aplicado a um tipo de dados não colidível.

Se não for possível identificar uma combinação de ordenação comum entre os argumentos reais, uma função SQL trata seus parâmetros como tendo a combinação de ordenação padrão dos seus tipos de dados (que geralmente é a combinação de ordenação padrão do banco de dados, mas pode ser diferente para os parâmetros de tipos de domínio).

O comportamento dos parâmetros colidíveis pode ser considerado uma forma limitada de polimorfismo, aplicável apenas a tipos de dados textuais.
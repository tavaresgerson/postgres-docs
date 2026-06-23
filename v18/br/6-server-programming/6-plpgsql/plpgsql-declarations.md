## 41.3. Declarações [#](#PLPGSQL-DECLARATIONS)

* [41.3.1. Declaração de Parâmetros de Função](plpgsql-declarations.md#PLPGSQL-DECLARATION-PARAMETERS)
* [41.3.2. `ALIAS`](plpgsql-declarations.md#PLPGSQL-DECLARATION-ALIAS)
* [41.3.3. Copiar Tipos](plpgsql-declarations.md#PLPGSQL-DECLARATION-TYPE)
* [41.3.4. Tipos de Linha](plpgsql-declarations.md#PLPGSQL-DECLARATION-ROWTYPES)
* [41.3.5. Tipos de Registro](plpgsql-declarations.md#PLPGSQL-DECLARATION-RECORDS)
* [41.3.6. Colaboração de Variáveis PL/pgSQL](plpgsql-declarations.md#PLPGSQL-DECLARATION-COLLATION)

Todas as variáveis utilizadas em um bloco devem ser declaradas na seção de declarações do bloco. (As únicas exceções são que a variável do laço de um loop `FOR` que itera sobre uma faixa de valores inteiros é automaticamente declarada como uma variável inteira, e da mesma forma, a variável do laço de um loop `FOR` que itera sobre o resultado de um cursor é automaticamente declarada como uma variável de registro.)

As variáveis PL/pgSQL podem ter qualquer tipo de dados SQL, como `integer`, `varchar` e `char`.

Aqui estão alguns exemplos de declarações de variáveis:

```
user_id integer;
quantity numeric(5);
url varchar;
myrow tablename%ROWTYPE;
myfield tablename.columnname%TYPE;
arow RECORD;
```

A sintaxe geral de uma declaração de variável é:

```
name [ CONSTANT ] type [ COLLATE collation_name ] [ NOT NULL ] [ { DEFAULT | := | = } expression ];
```

A cláusula `DEFAULT`, se fornecida, especifica o valor inicial atribuído à variável quando o bloco é entrado. Se a cláusula `DEFAULT` não for fornecida, a variável é inicializada com o valor nulo do SQL. A opção `CONSTANT` impede que a variável seja atribuída após a inicialização, de modo que seu valor permanecerá constante durante a duração do bloco. A opção `COLLATE` especifica uma collation a ser usada para a variável (ver [Seção 41.3.6](plpgsql-declarations.md#PLPGSQL-DECLARATION-COLLATION)). Se `NOT NULL` for especificado, uma atribuição de um valor nulo resulta em um erro de tempo de execução. Todas as variáveis declaradas como `NOT NULL` devem ter um valor padrão não nulo especificado. Igual (`=`) pode ser usado em vez de `:=` compatível com PL/SQL.

O valor padrão de uma variável é avaliado e atribuído à variável cada vez que o bloco é inserido (não apenas uma vez por chamada de função). Por exemplo, atribuir `now()` a uma variável do tipo `timestamp` faz com que a variável tenha o tempo da chamada de função atual, e não o tempo em que a função foi pré-compilada.

Exemplos:

```
quantity integer DEFAULT 32;
url varchar := 'http://mysite.com';
transaction_time CONSTANT timestamp with time zone := now();
```

Uma vez declarada, o valor de uma variável pode ser usado em expressões de inicialização posteriores no mesmo bloco, por exemplo:

```
DECLARE
  x integer := 1;
  y integer := x + 1;
```

### 41.3.1. Declaração de Parâmetros de Função [#](#PLPGSQL-DECLARATION-PARAMETERS)

Os parâmetros passados para as funções são nomeados com os identificadores `$1`, `$2`, etc. Opcionalmente, aliases podem ser declarados para os nomes de parâmetros `$n` para aumentar a legibilidade. Ou o alias ou o identificador numérico pode então ser usado para referenciar o valor do parâmetro.

Existem duas maneiras de criar um alias. A maneira preferida é dar um nome ao parâmetro no comando `CREATE FUNCTION`, por exemplo:

```
CREATE FUNCTION sales_tax(subtotal real) RETURNS real AS $$
BEGIN
    RETURN subtotal * 0.06;
END;
$$ LANGUAGE plpgsql;
```

A outra maneira é declarar explicitamente um alias, usando a sintaxe de declaração

```
name ALIAS FOR $n;
```

O mesmo exemplo nesse estilo fica assim:

```
CREATE FUNCTION sales_tax(real) RETURNS real AS $$
DECLARE
    subtotal ALIAS FOR $1;
BEGIN
    RETURN subtotal * 0.06;
END;
$$ LANGUAGE plpgsql;
```

Nota

Esses dois exemplos não são perfeitamente equivalentes. No primeiro caso, `subtotal` poderia ser referenciado como `sales_tax.subtotal`, mas no segundo caso não poderia. (Se tivéssemos anexado uma etiqueta ao bloco interno, `subtotal` poderia ser qualificado com essa etiqueta, em vez disso.)

Alguns exemplos mais:

```
CREATE FUNCTION instr(varchar, integer) RETURNS integer AS $$
DECLARE
    v_string ALIAS FOR $1;
    index ALIAS FOR $2;
BEGIN
    -- some computations using v_string and index here
END;
$$ LANGUAGE plpgsql;


CREATE FUNCTION concat_selected_fields(in_t sometablename) RETURNS text AS $$
BEGIN
    RETURN in_t.f1 || in_t.f3 || in_t.f5 || in_t.f7;
END;
$$ LANGUAGE plpgsql;
```

Quando uma função PL/pgSQL é declarada com parâmetros de saída, os parâmetros de saída recebem nomes `$n` e aliases opcionais da mesma maneira que os parâmetros de entrada normais. Um parâmetro de saída é efetivamente uma variável que começa com NULL; ele deve ser atribuído durante a execução da função. O valor final do parâmetro é o que é retornado. Por exemplo, o exemplo de imposto de vendas também pode ser feito dessa maneira:

```
CREATE FUNCTION sales_tax(subtotal real, OUT tax real) AS $$
BEGIN
    tax := subtotal * 0.06;
END;
$$ LANGUAGE plpgsql;
```

Observe que omitimos `RETURNS real` — poderíamos tê-lo incluído, mas seria redundante.

Para chamar uma função com parâmetros `OUT`, omita o(s) parâmetro(es) de saída na chamada da função:

```
SELECT sales_tax(100.00);
```

Os parâmetros de saída são mais úteis quando retornam vários valores. Um exemplo trivial é:

```
CREATE FUNCTION sum_n_product(x int, y int, OUT sum int, OUT prod int) AS $$
BEGIN
    sum := x + y;
    prod := x * y;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM sum_n_product(2, 4);
 sum | prod
-----+------
   6 |    8
```

Como discutido na [Seção 36.5.4](xfunc-sql.md#XFUNC-OUTPUT-PARAMETERS), isso efetivamente cria um tipo de registro anônimo para os resultados da função. Se uma cláusula `RETURNS` for dada, ela deve dizer `RETURNS record`.

Isso também funciona com procedimentos, por exemplo:

```
CREATE PROCEDURE sum_n_product(x int, y int, OUT sum int, OUT prod int) AS $$
BEGIN
    sum := x + y;
    prod := x * y;
END;
$$ LANGUAGE plpgsql;
```

Em uma chamada a um procedimento, todos os parâmetros devem ser especificados. Para parâmetros de saída, `NULL` pode ser especificado ao chamar o procedimento a partir de SQL simples:

```
CALL sum_n_product(2, 4, NULL, NULL);
 sum | prod
-----+------
   6 |    8
```

No entanto, ao chamar um procedimento a partir do PL/pgSQL, você deve, em vez disso, escrever uma variável para qualquer parâmetro de saída; a variável receberá o resultado da chamada. Consulte [Seção 41.6.3] para obter detalhes.

Outra maneira de declarar uma função PL/pgSQL é com `RETURNS TABLE`, por exemplo:

```
CREATE FUNCTION extended_sales(p_itemno int)
RETURNS TABLE(quantity int, total numeric) AS $$
BEGIN
    RETURN QUERY SELECT s.quantity, s.quantity * s.price FROM sales AS s
                 WHERE s.itemno = p_itemno;
END;
$$ LANGUAGE plpgsql;
```

Isso é exatamente equivalente a declarar um ou mais parâmetros `OUT` e especificar `RETURNS SETOF sometype`.

Quando o tipo de retorno de uma função PL/pgSQL é declarado como um tipo polimórfico (consulte [Seção 36.2.5](extend-type-system.md#EXTEND-TYPES-POLYMORPHIC)), um parâmetro especial `$0` é criado. Seu tipo de dado é o tipo de retorno real da função, conforme deduzido dos tipos de entrada reais. Isso permite que a função acesse seu tipo de retorno real, conforme mostrado em [Seção 41.3.3](plpgsql-declarations.md#PLPGSQL-DECLARATION-TYPE). `$0` é inicializado para null e pode ser modificado pela função, portanto, pode ser usado para armazenar o valor de retorno, se desejado, embora isso não seja necessário. `$0` também pode receber um alias. Por exemplo, esta função funciona em qualquer tipo de dado que tenha um operador `+`:

```
CREATE FUNCTION add_three_values(v1 anyelement, v2 anyelement, v3 anyelement)
RETURNS anyelement AS $$
DECLARE
    result ALIAS FOR $0;
BEGIN
    result := v1 + v2 + v3;
    RETURN result;
END;
$$ LANGUAGE plpgsql;
```

O mesmo efeito pode ser obtido declarando um ou mais parâmetros de saída como tipos polimórficos. Neste caso, o parâmetro especial `$0` não é usado; os próprios parâmetros de saída servem ao mesmo propósito. Por exemplo:

```
CREATE FUNCTION add_three_values(v1 anyelement, v2 anyelement, v3 anyelement,
                                 OUT sum anyelement)
AS $$
BEGIN
    sum := v1 + v2 + v3;
END;
$$ LANGUAGE plpgsql;
```

Na prática, pode ser mais útil declarar uma função polimórfica usando a família de tipos `anycompatible`, para que a promoção automática dos argumentos de entrada para um tipo comum ocorra. Por exemplo:

```
CREATE FUNCTION add_three_values(v1 anycompatible, v2 anycompatible, v3 anycompatible)
RETURNS anycompatible AS $$
BEGIN
    RETURN v1 + v2 + v3;
END;
$$ LANGUAGE plpgsql;
```

Com este exemplo, uma chamada como

```
SELECT add_three_values(1, 2, 4.7);
```

funcionarão, promovendo automaticamente as entradas inteiras para numéricas. A função que usa `anyelement` exigiria que você realize a conversão dos três inputs para o mesmo tipo manualmente.

### 41.3.2. `ALIAS` [#](#PLPGSQL-DECLARATION-ALIAS)

```
newname ALIAS FOR oldname;
```

A sintaxe `ALIAS` é mais geral do que o sugerido na seção anterior: você pode declarar um alias para qualquer variável, não apenas para parâmetros de função. O principal uso prático disso é atribuir um nome diferente para variáveis com nomes predeterminados, como `NEW` ou `OLD` dentro de uma função de gatilho.

Exemplos:

```
DECLARE
  prior ALIAS FOR old;
  updated ALIAS FOR new;
```

Como o `ALIAS` cria duas maneiras diferentes de nomear o mesmo objeto, o uso irrestrito pode ser confuso. É melhor usá-lo apenas para o propósito de sobrepor nomes predeterminados.

### 41.3.3. Copiar tipos [#](#PLPGSQL-DECLARATION-TYPE)

```
name table.column%TYPE
name variable%TYPE
```

`%TYPE` fornece o tipo de dados de uma coluna de tabela ou uma variável PL/pgSQL previamente declarada. Você pode usar isso para declarar variáveis que irão conter valores do banco de dados. Por exemplo, digamos que você tenha uma coluna chamada `user_id` em sua tabela `users`. Para declarar uma variável com o mesmo tipo de dados que `users.user_id`, escreva:

```
user_id users.user_id%TYPE;
```

Também é possível escrever a decoração de matriz após `%TYPE`, criando assim uma variável que contém uma matriz do tipo referenciado:

```
user_ids users.user_id%TYPE[];
user_ids users.user_id%TYPE ARRAY[4];  -- equivalent to the above
```

Assim como ao declarar colunas de tabela que são matrizes, não importa se você escreve múltiplos pares de chaves ou dimensões específicas de matriz: o PostgreSQL trata todos os arrays de um tipo de elemento dado como o mesmo tipo, independentemente da dimensionalidade. (Veja [Seção 8.15.1](arrays.md#ARRAYS-DECLARATION).)

Ao usar `%TYPE`, você não precisa saber o tipo de dados da estrutura que você está referenciando, e o mais importante é que, se o tipo de dados do item referenciado mudar no futuro (por exemplo: você muda o tipo de `user_id` de `integer` para `real`, você pode não precisar alterar a definição da sua função.

`%TYPE` é particularmente valioso em funções polimórficas, uma vez que os tipos de dados necessários para as variáveis internas podem mudar de uma chamada para a próxima. Variáveis apropriadas podem ser criadas aplicando `%TYPE` aos argumentos ou marcadores de resultado da função.

### 41.3.4. Tipos de fileiras [#](#PLPGSQL-DECLARATION-ROWTYPES)

```
name table_name%ROWTYPE;
name composite_type_name;
```

Uma variável de tipo composto é chamada de variável *de linha* (ou variável *de tipo de linha*). Tal variável pode conter uma linha inteira de um resultado de consulta `SELECT` ou `FOR`, desde que o conjunto de colunas daquela consulta corresponda ao tipo declarado da variável. Os campos individuais do valor da linha são acessados usando a notação usual em ponto, por exemplo, `rowvar.field`.

Uma variável de linha pode ser declarada para ter o mesmo tipo que as linhas de uma tabela ou visão existente, usando a notação *`table_name`*`%ROWTYPE`; ou pode ser declarada dando o nome de um tipo composto. (Como cada tabela tem um tipo composto associado com o mesmo nome, na verdade não importa no PostgreSQL se você escreve `%ROWTYPE` ou não. Mas o formulário com `%ROWTYPE` é mais portátil.)

Assim como em `%TYPE`, `%ROWTYPE` pode ser seguido por uma decoração de matriz para declarar uma variável que contém uma matriz do tipo composto referenciado.

Os parâmetros de uma função podem ser tipos compostos (linhas completas de tabela). Nesse caso, o identificador correspondente `$n` será uma variável de linha, e os campos podem ser selecionados a partir dela, por exemplo `$1.user_id`.

Aqui está um exemplo de uso de tipos compostos. `table1` e `table2` são tabelas existentes que possuem pelo menos os campos mencionados:

```
CREATE FUNCTION merge_fields(t_row table1) RETURNS text AS $$
DECLARE
    t2_row table2%ROWTYPE;
BEGIN
    SELECT * INTO t2_row FROM table2 WHERE ... ;
    RETURN t_row.f1 || t2_row.f3 || t_row.f5 || t2_row.f7;
END;
$$ LANGUAGE plpgsql;

SELECT merge_fields(t.*) FROM table1 t WHERE ... ;
```

### 41.3.5. Tipos de registro [#](#PLPGSQL-DECLARATION-RECORDS)

```
name RECORD;
```

As variáveis de registro são semelhantes às variáveis de tipo de linha, mas não possuem uma estrutura pré-definida. Elas assumem a estrutura real da linha que são atribuídas durante um comando `SELECT` ou `FOR`. A subestrutura de uma variável de registro pode mudar a cada vez que ela é atribuída. Uma consequência disso é que, até que uma variável de registro seja atribuída pela primeira vez, ela não possui subestrutura, e qualquer tentativa de acessar um campo nela resultará em um erro de execução.

Observe que `RECORD` não é um tipo de dado verdadeiro, apenas um marcador. Também deve-se perceber que, quando uma função PL/pgSQL é declarada para retornar o tipo `record`, esse não é exatamente o mesmo conceito que uma variável de registro, embora tal função possa usar uma variável de registro para armazenar seu resultado. Em ambos os casos, a estrutura da linha real é desconhecida quando a função é escrita, mas para uma função que retorna `record`, a estrutura real é determinada quando a consulta de chamada é analisada, enquanto uma variável de registro pode alterar sua estrutura de linha em tempo real.

### 41.3.6. Colaboração de variáveis PL/pgSQL [#](#PLPGSQL-DECLARATION-COLLATION)

Quando uma função PL/pgSQL tem um ou mais parâmetros de tipos de dados colidíveis, uma codificação é identificada para cada chamada de função, dependendo das codificações atribuídas aos argumentos reais, conforme descrito em [Seção 23.2](collation.md). Se uma codificação for identificada com sucesso (ou seja, não houver conflitos de codificações implícitas entre os argumentos), todos os parâmetros colidíveis são tratados como tendo aquela codificação implicitamente. Isso afetará o comportamento das operações sensíveis à codificação dentro da função. Por exemplo, considere

```
CREATE FUNCTION less_than(a text, b text) RETURNS boolean AS $$
BEGIN
    RETURN a < b;
END;
$$ LANGUAGE plpgsql;

SELECT less_than(text_field_1, text_field_2) FROM table1;
SELECT less_than(text_field_1, text_field_2 COLLATE "C") FROM table1;
```

O primeiro uso de `less_than` utilizará a collation comum de `text_field_1` e `text_field_2` para a comparação, enquanto o segundo uso utilizará a collation de `C`.

Além disso, a collation identificada também é assumida como a collation de quaisquer variáveis locais que sejam de tipos colidíveis. Assim, essa função não funcionaria de maneira diferente se fosse escrita como

```
CREATE FUNCTION less_than(a text, b text) RETURNS boolean AS $$
DECLARE
    local_a text := a;
    local_b text := b;
BEGIN
    RETURN local_a < local_b;
END;
$$ LANGUAGE plpgsql;
```

Se não houver parâmetros de tipos de dados colidíveis ou se não for possível identificar uma ordenação comum para eles, os parâmetros e as variáveis locais utilizam a ordenação padrão de seu tipo de dados (que geralmente é a ordenação padrão do banco de dados, mas pode ser diferente para variáveis de tipos de domínio).

Uma variável local de um tipo de dados colidível pode ter uma collation diferente associada a ela, incluindo a opção `COLLATE` em sua declaração, por exemplo:

```
DECLARE
    local_a text COLLATE "en_US";
```

Esta opção substitui a ordenação que, de outra forma, seria dada à variável de acordo com as regras acima.

Além disso, é claro que cláusulas explícitas `COLLATE` podem ser escritas dentro de uma função, se for desejado forçar a utilização de uma determinada ordenação em uma operação específica. Por exemplo,

```
CREATE FUNCTION less_than_c(a text, b text) RETURNS boolean AS $$
BEGIN
    RETURN a < b COLLATE "C";
END;
$$ LANGUAGE plpgsql;
```

Isso substitui as colasções associadas às colunas da tabela, aos parâmetros ou às variáveis locais usadas na expressão, assim como aconteceria em um comando SQL simples.
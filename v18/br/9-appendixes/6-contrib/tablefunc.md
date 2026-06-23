## F.43. tablefunc — funções que retornam tabelas (`crosstab` e outras) [#](#TABLEFUNC)

* [F.43.1. Funções Fornecidas](tablefunc.md#TABLEFUNC-FUNCTIONS-SECT)
* [F.43.2. Autor](tablefunc.md#TABLEFUNC-AUTHOR)

O módulo `tablefunc` inclui várias funções que retornam tabelas (ou seja, múltiplas linhas). Essas funções são úteis tanto por si mesmas quanto como exemplos de como escrever funções em C que retornam múltiplas linhas.

Este módulo é considerado "confiável", ou seja, pode ser instalado por usuários não superusuários que possuem privilégio `CREATE` no banco de dados atual.

### F.43.1. Funções Fornecidas [#](#TABLEFUNC-FUNCTIONS-SECT)

[Tabela F.33](tablefunc.md#TABLEFUNC-FUNCTIONS "Table F.33. tablefunc Functions") resume as funções fornecidas pelo módulo `tablefunc`.

**Tabela F.33. `tablefunc` Funções**



<table border="1" class="table" summary="tablefunc Functions">
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Função
    </p>
    <p>
     Descrição
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      normal_rand
     </code>
     (
     <em class="parameter">
      <code>
       numvals
      </code>
     </em>
     <code class="type">
      integer
     </code>
     ,
     <em class="parameter">
      <code>
       mean
      </code>
     </em>
     <code class="type">
      float8
     </code>
     ,
     <em class="parameter">
      <code>
       stddev
      </code>
     </em>
     <code class="type">
      float8
     </code>
     )
     <code class="returnvalue">
      setof float8
     </code>
    </p>
    <p>
     Produz um conjunto de valores aleatórios distribuídos normalmente.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      crosstab
     </code>
     (
     <em class="parameter">
      <code>
       sql
      </code>
     </em>
     <code class="type">
      text
     </code>
     )
     <code class="returnvalue">
      setof record
     </code>
    </p>
    <p>
     Produz um
     <span class="quote">
      “
      <span class="quote">
       tabela pivot
      </span>
      ”
     </span>
     contendo nomes de linha, além de
     <em class="replaceable">
      <code>
       N
      </code>
     </em>
     colunas de valor, onde
     <em class="replaceable">
      <code>
       N
      </code>
     </em>
     é determinada pelo tipo de linha especificado na consulta de chamada.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      crosstab
      <em class="replaceable">
       <code>
        N
       </code>
      </em>
     </code>
     (
     <em class="parameter">
      <code>
       sql
      </code>
     </em>
     <code class="type">
      text
     </code>
     )
     <code class="returnvalue">
      setof table_crosstab_
      <em class="replaceable">
       <code>
        N
       </code>
      </em>
     </code>
    </p>
    <p>
     Produz um
     <span class="quote">
      “
      <span class="quote">
       tabela pivot
      </span>
      ”
     </span>
     contendo nomes de linha, além de
     <em class="replaceable">
      <code>
       N
      </code>
     </em>
     colunas de valor.
     <code class="function">
      crosstab2
     </code>
     ,
     <code class="function">
      crosstab3
     </code>
     , e
     <code class="function">
      crosstab4
     </code>
     são pré-definidos, mas você pode criar outros
     <code class="function">
      crosstab
      <em class="replaceable">
       <code>
        N
       </code>
      </em>
     </code>
     funciona conforme descrito abaixo.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      crosstab
     </code>
     (
     <em class="parameter">
      <code>
       source_sql
      </code>
     </em>
     <code class="type">
      text
     </code>
     ,
     <em class="parameter">
      <code>
       category_sql
      </code>
     </em>
     <code class="type">
      text
     </code>
     )
     <code class="returnvalue">
      setof record
     </code>
    </p>
    <p>
     Produz um
     <span class="quote">
      “
      <span class="quote">
       tabela pivot
      </span>
      ”
     </span>
     com as colunas de valor especificadas por uma segunda consulta.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      crosstab
     </code>
     (
     <em class="parameter">
      <code>
       sql
      </code>
     </em>
     <code class="type">
      text
     </code>
     ,
     <em class="parameter">
      <code>
       N
      </code>
     </em>
     <code class="type">
      integer
     </code>
     )
     <code class="returnvalue">
      setof record
     </code>
    </p>
    <p>
     Versão obsoleta de
     <code class="function">
      crosstab(text)
     </code>
     O parâmetro
     <em class="parameter">
      <code>
       N
      </code>
     </em>
     agora é ignorado, uma vez que o número de colunas de valor é sempre determinado pela consulta que está chamando.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      connectby
     </code>
     (
     <em class="parameter">
      <code>
       relname
      </code>
     </em>
     <code class="type">
      text
     </code>
     ,
     <em class="parameter">
      <code>
       keyid_fld
      </code>
     </em>
     <code class="type">
      text
     </code>
     ,
     <em class="parameter">
      <code>
       parent_keyid_fld
      </code>
     </em>
     <code class="type">
      text
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        orderby_fld
       </code>
      </em>
      <code class="type">
       text
      </code>
     </span>
     ],
     <em class="parameter">
      <code>
       start_with
      </code>
     </em>
     <code class="type">
      text
     </code>
     ,
     <em class="parameter">
      <code>
       max_depth
      </code>
     </em>
     <code class="type">
      integer
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        branch_delim
       </code>
      </em>
      <code class="type">
       text
      </code>
     </span>
     ] ) →
     <code class="returnvalue">
      setof record
     </code>
    </p>
    <p>
     Produz uma representação de uma estrutura de árvore hierárquica.
    </p>
   </td>
  </tr>
 </tbody>
</table>










#### F.43.1.1. `normal_rand` [#](#TABLEFUNC-FUNCTIONS-NORMAL-RAND)

```
normal_rand(int numvals, float8 mean, float8 stddev) returns setof float8
```

`normal_rand` produz um conjunto de valores aleatórios distribuídos normalmente (distribuição gaussiana).

*`numvals`* é o número de valores que devem ser retornados pela função. *`mean`* é a média da distribuição normal dos valores e *`stddev`* é a desvio padrão da distribuição normal dos valores.

Por exemplo, esta chamada solicita 1000 valores com uma média de 5 e um desvio padrão de 3:

```
test=# SELECT * FROM normal_rand(1000, 5, 3);
     normal_rand
----------------------
     1.56556322244898
     9.10040991424657
     5.36957140345079
   -0.369151492880995
    0.283600703686639
       .
       .
       .
     4.82992125404908
     9.71308014517282
     2.49639286969028
(1000 rows)
```

#### F.43.1.2. `crosstab(text)` [#](#TABLEFUNC-FUNCTIONS-CROSSTAB-TEXT)

```
crosstab(text sql)
crosstab(text sql, int N)
```

A função `crosstab` é usada para produzir exibições de "pivô", na qual os dados são listados na página em vez de em linha reta. Por exemplo, podemos ter dados como

```
row1    val11
row1    val12
row1    val13
...
row2    val21
row2    val22
row2    val23
...
```

que desejamos exibir como

```
row1    val11   val12   val13   ...
row2    val21   val22   val23   ...
...
```

A função `crosstab` recebe um parâmetro de texto que é uma consulta SQL que produz dados brutos formatados da primeira maneira, e produz uma tabela formatada da segunda maneira.

O parâmetro *`sql`* é uma declaração SQL que produz o conjunto de dados de origem. Esta declaração deve retornar uma coluna `row_name`, uma coluna `category` e uma coluna `value`. *`N`* é um parâmetro obsoleto, ignorado se fornecido (anteriormente, isso tinha que corresponder ao número de colunas de valor de saída, mas agora isso é determinado pela consulta que está solicitando).

Por exemplo, a consulta fornecida pode produzir um conjunto como algo assim:

```
 row_name    cat    value
----------+-------+-------
  row1      cat1    val1
  row1      cat2    val2
  row1      cat3    val3
  row1      cat4    val4
  row2      cat1    val5
  row2      cat2    val6
  row2      cat3    val7
  row2      cat4    val8
```

A função `crosstab` é declarada para retornar `setof record`, portanto, os nomes e tipos reais das colunas de saída devem ser definidos na cláusula `FROM` da declaração `SELECT` chamada, por exemplo:

```
SELECT * FROM crosstab('...') AS ct(row_name text, category_1 text, category_2 text);
```

Este exemplo produz um conjunto algo como:

```
           <== value  columns  ==>
 row_name   category_1   category_2
----------+------------+------------
  row1        val1         val2
  row2        val5         val6
```

A cláusula `FROM` deve definir a saída como uma coluna `row_name` (do mesmo tipo de dados que a primeira coluna de resultado da consulta SQL) seguida por N colunas `value` (todas do mesmo tipo de dados que a terceira coluna de resultado da consulta SQL). Você pode configurar quantas colunas de valor de saída desejar. Os nomes das colunas de saída são de sua escolha.

A função `crosstab` produz uma linha de saída para cada grupo consecutivo de linhas de entrada com o mesmo valor `row_name`. Ela preenche as colunas de saída `value`, da esquerda para a direita, com os campos `value` dessas linhas. Se houver menos linhas em um grupo do que colunas de saída `value`, as colunas de saída extras são preenchidas com nulos; se houver mais linhas, as linhas de entrada extras são ignoradas.

Na prática, a consulta SQL deve sempre especificar `ORDER BY 1,2` para garantir que as linhas de entrada estejam corretamente ordenadas, ou seja, os valores com o mesmo `row_name` são reunidos e corretamente ordenados dentro da linha. Observe que o próprio `crosstab` não presta atenção na segunda coluna do resultado da consulta; ele está apenas lá para ser ordenado, para controlar a ordem em que os valores da terceira coluna aparecem em toda a página.

Aqui está um exemplo completo:

```
CREATE TABLE ct(id SERIAL, rowid TEXT, attribute TEXT, value TEXT);
INSERT INTO ct(rowid, attribute, value) VALUES('test1','att1','val1');
INSERT INTO ct(rowid, attribute, value) VALUES('test1','att2','val2');
INSERT INTO ct(rowid, attribute, value) VALUES('test1','att3','val3');
INSERT INTO ct(rowid, attribute, value) VALUES('test1','att4','val4');
INSERT INTO ct(rowid, attribute, value) VALUES('test2','att1','val5');
INSERT INTO ct(rowid, attribute, value) VALUES('test2','att2','val6');
INSERT INTO ct(rowid, attribute, value) VALUES('test2','att3','val7');
INSERT INTO ct(rowid, attribute, value) VALUES('test2','att4','val8');

SELECT *
FROM crosstab(
  'select rowid, attribute, value
   from ct
   where attribute = ''att2'' or attribute = ''att3''
   order by 1,2')
AS ct(row_name text, category_1 text, category_2 text, category_3 text);

 row_name | category_1 | category_2 | category_3
----------+------------+------------+------------
 test1    | val2       | val3       |
 test2    | val6       | val7       |
(2 rows)
```

Você pode evitar a necessidade de sempre escrever uma cláusula `FROM` para definir as colunas de saída, configurando uma função de cruzamento personalizada que tenha o tipo de linha de saída desejado integrado à sua definição. Isso é descrito na próxima seção. Outra possibilidade é incorporar a cláusula `FROM` necessária em uma definição de visualização.

Nota

Veja também o comando `\crosstabview` em psql, que oferece funcionalidades semelhantes ao `crosstab()`.

#### F.43.1.3. `crosstabN(text)` [#](#TABLEFUNC-FUNCTIONS-CROSSTAB-N-TEXT)

```
crosstabN(text sql)
```

As funções `crosstabN` são exemplos de como configurar wrappers personalizados para a função geral `crosstab`, para que você não precise escrever os nomes e tipos das colunas na consulta `SELECT` que está chamando. O módulo `tablefunc` inclui `crosstab2`, `crosstab3` e `crosstab4`, cujos tipos de linha de saída são definidos como

```
CREATE TYPE tablefunc_crosstab_N AS (
    row_name TEXT,
    category_1 TEXT,
    category_2 TEXT,
        .
        .
        .
    category_N TEXT
);
```

Assim, essas funções podem ser usadas diretamente quando a consulta de entrada produz as colunas `row_name` e `value` do tipo `text`, e você deseja 2, 3 ou 4 colunas de valores de saída. De todas as outras maneiras, elas se comportam exatamente como descrito acima para a função geral `crosstab`.

Por exemplo, o exemplo dado na seção anterior também funcionaria como

```
SELECT *
FROM crosstab3(
  'select rowid, attribute, value
   from ct
   where attribute = ''att2'' or attribute = ''att3''
   order by 1,2');
```

Essas funções são fornecidas principalmente para fins ilustrativos. Você pode criar seus próprios tipos de retorno e funções com base na função subjacente `crosstab()`. Existem duas maneiras de fazer isso:

* Crie um tipo composto que descreva as colunas de saída desejadas, semelhante aos exemplos em `contrib/tablefunc/tablefunc--1.0.sql`. Em seguida, defina um nome de função único que aceite um parâmetro `text` e retorne `setof your_type_name`, mas que faça referência à mesma função C `crosstab` subjacente. Por exemplo, se seus dados de origem produzem nomes de linha que são `text`, e valores que são `float8`, e você deseja 5 colunas de valor:

```
  CREATE TYPE my_crosstab_float8_5_cols AS (
      my_row_name text,
      my_category_1 float8,
      my_category_2 float8,
      my_category_3 float8,
      my_category_4 float8,
      my_category_5 float8
  );

  CREATE OR REPLACE FUNCTION crosstab_float8_5_cols(text)
      RETURNS setof my_crosstab_float8_5_cols
      AS '$libdir/tablefunc','crosstab' LANGUAGE C STABLE STRICT;
```

```
CREATE OR REPLACE FUNCTION crosstab_float8_5_cols(
    IN text,
    OUT my_row_name text,
    OUT my_category_1 float8,
    OUT my_category_2 float8,
    OUT my_category_3 float8,
    OUT my_category_4 float8,
    OUT my_category_5 float8)
  RETURNS setof record
  AS '$libdir/tablefunc','crosstab' LANGUAGE C STABLE STRICT;
```

#### F.43.1.4. `crosstab(text, text)` [#](#TABLEFUNC-FUNCTIONS-CROSSTAB-TEXT-2)

```
crosstab(text source_sql, text category_sql)
```

A principal limitação da forma de um único parâmetro do `crosstab` é que ela trata todos os valores de um grupo da mesma forma, inserindo cada valor na primeira coluna disponível. Se você deseja que as colunas de valor correspondam a categorias específicas de dados, e alguns grupos não tenham dados para algumas das categorias, isso não funciona bem. A forma de dois parâmetros do `crosstab` lida com esse caso, fornecendo uma lista explícita das categorias correspondentes às colunas de saída.

*`source_sql`* é uma declaração SQL que produz o conjunto de dados fonte. Esta declaração deve retornar uma coluna `row_name`, uma coluna `category` e uma coluna `value`. Também pode ter uma ou mais colunas “extra”. A coluna `row_name` deve ser a primeira. As colunas `category` e `value` devem ser as duas últimas colunas, nessa ordem. Quaisquer colunas entre `row_name` e `category` são tratadas como “extra”. Espera-se que as colunas “extra” sejam as mesmas para todas as linhas com o mesmo valor `row_name`.

Por exemplo, *`source_sql`* pode gerar um conjunto parecido com o seguinte:

```
SELECT row_name, extra_col, cat, value FROM foo ORDER BY 1;

 row_name    extra_col   cat    value
----------+------------+-----+---------
  row1         extra1    cat1    val1
  row1         extra1    cat2    val2
  row1         extra1    cat4    val4
  row2         extra2    cat1    val5
  row2         extra2    cat2    val6
  row2         extra2    cat3    val7
  row2         extra2    cat4    val8
```

*`category_sql`* é uma declaração SQL que produz o conjunto de categorias. Essa declaração deve retornar apenas uma coluna. Deve produzir pelo menos uma linha, ou um erro será gerado. Além disso, não deve produzir valores duplicados, ou um erro será gerado. *`category_sql`* pode ser algo como:

```
SELECT DISTINCT cat FROM foo ORDER BY 1;
    cat
  -------
    cat1
    cat2
    cat3
    cat4
```

A função `crosstab` é declarada para retornar `setof record`, portanto, os nomes e tipos reais das colunas de saída devem ser definidos na cláusula `FROM` da declaração `SELECT` chamada, por exemplo:

```
SELECT * FROM crosstab('...', '...')
    AS ct(row_name text, extra text, cat1 text, cat2 text, cat3 text, cat4 text);
```

Isso produzirá um resultado algo como:

```
                  <==  value  columns   ==>
row_name   extra   cat1   cat2   cat3   cat4
---------+-------+------+------+------+------
  row1     extra1  val1   val2          val4
  row2     extra2  val5   val6   val7   val8
```

A cláusula `FROM` deve definir o número adequado de colunas de saída dos tipos de dados adequados. Se houver *`N`* colunas no resultado da consulta *`source_sql`*, o primeiro *`N`*-2 delas deve corresponder às primeiras *`N`*-2 colunas de saída. As colunas de saída restantes devem ter o tipo da última coluna do resultado da consulta *`source_sql`*, e deve haver exatamente tantas delas quanto houver linhas no resultado da consulta *`category_sql`*.

A função `crosstab` produz uma linha de saída para cada grupo consecutivo de linhas de entrada com o mesmo valor de `row_name`. A coluna de saída `row_name`, além de quaisquer colunas “extras”, são copiadas da primeira linha do grupo. As colunas de saída `value` são preenchidas com os campos `value` das linhas que possuem valores correspondentes de `category`. Se o `category` de uma linha não corresponder a nenhuma saída da consulta *`category_sql`*, seu `value` é ignorado. As colunas de saída cujas categorias correspondentes não estão presentes em nenhuma linha de entrada do grupo são preenchidas com nulos.

Na prática, a consulta *`source_sql`* deve sempre especificar `ORDER BY 1` para garantir que os valores com o mesmo `row_name` sejam reunidos. No entanto, a ordem das categorias dentro de um grupo não é importante. Além disso, é essencial ter certeza de que a ordem da saída da consulta *`category_sql`* corresponda ao pedido de coluna de saída especificado.

Aqui estão dois exemplos completos:

```
create table sales(year int, month int, qty int);
insert into sales values(2007, 1, 1000);
insert into sales values(2007, 2, 1500);
insert into sales values(2007, 7, 500);
insert into sales values(2007, 11, 1500);
insert into sales values(2007, 12, 2000);
insert into sales values(2008, 1, 1000);

select * from crosstab(
  'select year, month, qty from sales order by 1',
  'select m from generate_series(1,12) m'
) as (
  year int,
  "Jan" int,
  "Feb" int,
  "Mar" int,
  "Apr" int,
  "May" int,
  "Jun" int,
  "Jul" int,
  "Aug" int,
  "Sep" int,
  "Oct" int,
  "Nov" int,
  "Dec" int
);
 year | Jan  | Feb  | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov  | Dec
------+------+------+-----+-----+-----+-----+-----+-----+-----+-----+------+------
 2007 | 1000 | 1500 |     |     |     |     | 500 |     |     |     | 1500 | 2000
 2008 | 1000 |      |     |     |     |     |     |     |     |     |      |
(2 rows)
```

```
CREATE TABLE cth(rowid text, rowdt timestamp, attribute text, val text);
INSERT INTO cth VALUES('test1','01 March 2003','temperature','42');
INSERT INTO cth VALUES('test1','01 March 2003','test_result','PASS');
INSERT INTO cth VALUES('test1','01 March 2003','volts','2.6987');
INSERT INTO cth VALUES('test2','02 March 2003','temperature','53');
INSERT INTO cth VALUES('test2','02 March 2003','test_result','FAIL');
INSERT INTO cth VALUES('test2','02 March 2003','test_startdate','01 March 2003');
INSERT INTO cth VALUES('test2','02 March 2003','volts','3.1234');

SELECT * FROM crosstab
(
  'SELECT rowid, rowdt, attribute, val FROM cth ORDER BY 1',
  'SELECT DISTINCT attribute FROM cth ORDER BY 1'
)
AS
(
       rowid text,
       rowdt timestamp,
       temperature int4,
       test_result text,
       test_startdate timestamp,
       volts float8
);
 rowid |          rowdt           | temperature | test_result |      test_startdate      | volts
-------+--------------------------+-------------+-------------+--------------------------+--------
 test1 | Sat Mar 01 00:00:00 2003 |          42 | PASS        |                          | 2.6987
 test2 | Sun Mar 02 00:00:00 2003 |          53 | FAIL        | Sat Mar 01 00:00:00 2003 | 3.1234
(2 rows)
```

Você pode criar funções predefinidas para evitar ter que escrever os nomes e tipos das colunas de resultado em cada consulta. Veja os exemplos na seção anterior. A função C subjacente para essa forma de `crosstab` é chamada `crosstab_hash`.

#### F.43.1.5. `connectby` [#](#TABLEFUNC-FUNCTIONS-CONNECTBY)

```
connectby(text relname, text keyid_fld, text parent_keyid_fld
          [, text orderby_fld ], text start_with, int max_depth
          [, text branch_delim ])
```

A função `connectby` produz uma exibição de dados hierárquicos que são armazenados em uma tabela. A tabela deve ter um campo chave que identifique de forma única as linhas e um campo chave-pai que faça referência ao pai (se houver) de cada linha. `connectby` pode exibir a subárvore descendente de qualquer linha.

[Tabela F.34](tablefunc.md#TABLEFUNC-CONNECTBY-PARAMETERS "Table F.34. connectby Parameters") explica os parâmetros.

**Tabela F.34. `connectby` Parâmetros**



<table border="1" class="table" summary="connectby Parameters">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Parameter
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <em class="parameter">
     <code>
      relname
     </code>
    </em>
   </td>
   <td>
    Nome da relação de fonte
   </td>
  </tr>
  <tr>
   <td>
    <em class="parameter">
     <code>
      keyid_fld
     </code>
    </em>
   </td>
   <td>
    Nome do campo chave
   </td>
  </tr>
  <tr>
   <td>
    <em class="parameter">
     <code>
      parent_keyid_fld
     </code>
    </em>
   </td>
   <td>
    Nome do campo chave-pai
   </td>
  </tr>
  <tr>
   <td>
    <em class="parameter">
     <code>
      orderby_fld
     </code>
    </em>
   </td>
   <td>
    Nome do campo para ordenar os irmãos (opcional)
   </td>
  </tr>
  <tr>
   <td>
    <em class="parameter">
     <code>
      start_with
     </code>
    </em>
   </td>
   <td>
    Valor chave da linha para onde começar
   </td>
  </tr>
  <tr>
   <td>
    <em class="parameter">
     <code>
      max_depth
     </code>
    </em>
   </td>
   <td>
    Profundidade máxima para descida, ou zero para profundidade ilimitada
   </td>
  </tr>
  <tr>
   <td>
    <em class="parameter">
     <code>
      branch_delim
     </code>
    </em>
   </td>
   <td>
    String para separar as chaves em uma saída de ramo (opcional)
   </td>
  </tr>
 </tbody>
</table>










Os campos chave e chave-pai podem ser qualquer tipo de dado, mas devem ser do mesmo tipo. Observe que o valor *`start_with`* deve ser inserido como uma string de texto, independentemente do tipo do campo chave.

A função `connectby` é declarada para retornar `setof record`, portanto, os nomes e tipos reais das colunas de saída devem ser definidos na cláusula `FROM` da declaração `SELECT` chamada, por exemplo:

```
SELECT * FROM connectby('connectby_tree', 'keyid', 'parent_keyid', 'pos', 'row2', 0, '~')
    AS t(keyid text, parent_keyid text, level int, branch text, pos int);
```

As duas primeiras colunas de saída são usadas para a chave da linha atual e a chave da linha de origem; elas devem corresponder ao tipo do campo de chave da tabela. A terceira coluna de saída é a profundidade na árvore e deve ser do tipo `integer`. Se um parâmetro *`branch_delim`* foi dado, a próxima coluna de saída é a exibição do ramo e deve ser do tipo `text`. Finalmente, se um parâmetro *`orderby_fld`* foi dado, a última coluna de saída é um número de série e deve ser do tipo `integer`.

A coluna de saída "ramificação" mostra o caminho das chaves utilizadas para alcançar a linha atual. As chaves são separadas pela string especificada *`branch_delim`*. Se não se deseja exibir nenhuma ramificação, omita tanto o parâmetro *`branch_delim`* quanto a coluna de ramificação na lista de colunas de saída.

Se a ordem dos irmãos de um mesmo pai for importante, inclua o parâmetro *`orderby_fld`* para especificar pelo qual campo os irmãos devem ser ordenados. Este campo pode ser de qualquer tipo de dados ordenável. A lista de colunas de saída deve incluir uma coluna de número serial inteiro final, se e somente se *`orderby_fld`* for especificado.

Os parâmetros que representam os nomes de tabela e campo são copiados como estão nas consultas SQL que o `connectby` gera internamente. Portanto, inclua aspas duplas se os nomes forem em maiúsculas ou contiverem caracteres especiais. Você também pode precisar qualificar o esquema do nome da tabela.

Em tabelas grandes, o desempenho será ruim, a menos que haja um índice no campo chave-pai.

É importante que a string *`branch_delim`* não apareça em nenhum valor de chave, caso contrário, o `connectby` pode relatar incorretamente um erro de recursão infinita. Observe que, se *`branch_delim`* não for fornecido, um valor padrão de `~` é usado para fins de detecção de recursão.

Aqui está um exemplo:

```
CREATE TABLE connectby_tree(keyid text, parent_keyid text, pos int);

INSERT INTO connectby_tree VALUES('row1',NULL, 0);
INSERT INTO connectby_tree VALUES('row2','row1', 0);
INSERT INTO connectby_tree VALUES('row3','row1', 0);
INSERT INTO connectby_tree VALUES('row4','row2', 1);
INSERT INTO connectby_tree VALUES('row5','row2', 0);
INSERT INTO connectby_tree VALUES('row6','row4', 0);
INSERT INTO connectby_tree VALUES('row7','row3', 0);
INSERT INTO connectby_tree VALUES('row8','row6', 0);
INSERT INTO connectby_tree VALUES('row9','row5', 0);

-- with branch, without orderby_fld (order of results is not guaranteed)
SELECT * FROM connectby('connectby_tree', 'keyid', 'parent_keyid', 'row2', 0, '~')
 AS t(keyid text, parent_keyid text, level int, branch text);
 keyid | parent_keyid | level |       branch
-------+--------------+-------+---------------------
 row2  |              |     0 | row2
 row4  | row2         |     1 | row2~row4
 row6  | row4         |     2 | row2~row4~row6
 row8  | row6         |     3 | row2~row4~row6~row8
 row5  | row2         |     1 | row2~row5
 row9  | row5         |     2 | row2~row5~row9
(6 rows)

-- without branch, without orderby_fld (order of results is not guaranteed)
SELECT * FROM connectby('connectby_tree', 'keyid', 'parent_keyid', 'row2', 0)
 AS t(keyid text, parent_keyid text, level int);
 keyid | parent_keyid | level
-------+--------------+-------
 row2  |              |     0
 row4  | row2         |     1
 row6  | row4         |     2
 row8  | row6         |     3
 row5  | row2         |     1
 row9  | row5         |     2
(6 rows)

-- with branch, with orderby_fld (notice that row5 comes before row4)
SELECT * FROM connectby('connectby_tree', 'keyid', 'parent_keyid', 'pos', 'row2', 0, '~')
 AS t(keyid text, parent_keyid text, level int, branch text, pos int);
 keyid | parent_keyid | level |       branch        | pos
-------+--------------+-------+---------------------+-----
 row2  |              |     0 | row2                |   1
 row5  | row2         |     1 | row2~row5           |   2
 row9  | row5         |     2 | row2~row5~row9      |   3
 row4  | row2         |     1 | row2~row4           |   4
 row6  | row4         |     2 | row2~row4~row6      |   5
 row8  | row6         |     3 | row2~row4~row6~row8 |   6
(6 rows)

-- without branch, with orderby_fld (notice that row5 comes before row4)
SELECT * FROM connectby('connectby_tree', 'keyid', 'parent_keyid', 'pos', 'row2', 0)
 AS t(keyid text, parent_keyid text, level int, pos int);
 keyid | parent_keyid | level | pos
-------+--------------+-------+-----
 row2  |              |     0 |   1
 row5  | row2         |     1 |   2
 row9  | row5         |     2 |   3
 row4  | row2         |     1 |   4
 row6  | row4         |     2 |   5
 row8  | row6         |     3 |   6
(6 rows)
```

### F.43.2. Autor [#](#TABLEFUNC-AUTHOR)

Joe Conway
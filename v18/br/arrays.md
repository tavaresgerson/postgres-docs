## 8.15. Arrays [#](#ARRAYS)

* [8.15.1. Declaração de Tipos de Array](arrays.md#ARRAYS-DECLARATION)
* [8.15.2. Entrada de Valor de Array](arrays.md#ARRAYS-INPUT)
* [8.15.3. Acesso a Arrays](arrays.md#ARRAYS-ACCESSING)
* [8.15.4. Modificação de Arrays](arrays.md#ARRAYS-MODIFYING)
* [8.15.5. Pesquisa em Arrays](arrays.md#ARRAYS-SEARCHING)
* [8.15.6. Sintaxe de Entrada e Saída de Array](arrays.md#ARRAYS-IO)

O PostgreSQL permite que as colunas de uma tabela sejam definidas como matrizes multidimensionais de comprimento variável. Pode-se criar matrizes de qualquer tipo de base embutido ou definido pelo usuário, tipo enum, tipo composto, tipo de intervalo ou domínio.

### 8.15.1. Declaração de tipos de matriz [#](#ARRAYS-DECLARATION)

Para ilustrar o uso dos tipos de matriz, criamos esta tabela:

```
CREATE TABLE sal_emp (
    name            text,
    pay_by_quarter  integer[],
    schedule        text[][]
);
```

Como mostrado, um tipo de dados de matriz é nomeado anexando-se chaves quadradas (`[]`) ao nome do tipo de dados dos elementos da matriz. O comando acima criará uma tabela denominada `sal_emp` com uma coluna do tipo `text` (`name`), uma matriz unidimensional do tipo `integer` (`pay_by_quarter`), que representa o salário do empregado por trimestre, e uma matriz bidimensional do tipo `text` (`schedule`), que representa o cronograma semanal do empregado.

A sintaxe para `CREATE TABLE` permite especificar o tamanho exato dos arrays, por exemplo:

```
CREATE TABLE tictactoe (
    squares   integer[3][3]
);
```

No entanto, a implementação atual ignora quaisquer limites de tamanho de matriz fornecidos, ou seja, o comportamento é o mesmo para matrizes de comprimento não especificado.

A implementação atual também não exige o número declarado de dimensões. Os arrays de um tipo de elemento específico são todos considerados do mesmo tipo, independentemente do tamanho ou número de dimensões. Portanto, declarar o tamanho do array ou o número de dimensões em `CREATE TABLE` é simplesmente documentação; isso não afeta o comportamento em tempo de execução.

Uma sintaxe alternativa, que se conforma ao padrão SQL usando a palavra-chave `ARRAY`, pode ser usada para matrizes unidimensionais. `pay_by_quarter` poderia ter sido definido como:

```
    pay_by_quarter  integer ARRAY[4],
```

Ou, se não se deseja especificar o tamanho do array:

```
    pay_by_quarter  integer ARRAY,
```

Como antes, no entanto, o PostgreSQL não aplica a restrição de tamanho em nenhum caso.

### 8.15.2. Entrada de valor de matriz [#](#ARRAYS-INPUT)

Para escrever um valor de matriz como uma constante literal, coloque os valores dos elementos entre chaves angulares e separe-os por vírgulas. (Se você conhece C, isso não é diferente da sintaxe C para inicializar estruturas.) Você pode colocar aspas duplas em torno de qualquer valor de elemento e deve fazê-lo se ele contiver vírgulas ou chaves angulares. (Mais detalhes aparecem abaixo.) Assim, o formato geral de uma constante de matriz é o seguinte:

```
'{ val1 delim val2 delim ... }'
```

onde *`delim`* é o caractere delimitador para o tipo, conforme registrado em sua entrada `pg_type`. Entre os tipos de dados padrão fornecidos na distribuição PostgreSQL, todos usam uma vírgula (`,`), exceto pelo tipo `box`, que usa um ponto e vírgula (`;`). Cada *`val`* é uma constante do tipo do elemento da matriz, ou um submatriz. Um exemplo de uma constante de matriz é:

```
'{{1,2,3},{4,5,6},{7,8,9}}'
```

Essa constante é uma matriz bidimensional, 3 x 3, composta por três submatrizes de inteiros.

Para definir um elemento de um array como constante NULL, escreva `NULL` para o valor do elemento. (Qualquer variante maiúscula ou minúscula de `NULL` servirá.) Se você deseja um valor de string real "NULL", você deve colocá-lo entre aspas duplas.

(Esses tipos de constantes de matriz são, na verdade, apenas um caso especial das constantes de tipo genérico discutidas na [Seção 4.1.2.7](sql-syntax-lexical.md#SQL-SYNTAX-CONSTANTS-GENERIC). A constante é inicialmente tratada como uma string e passada para a rotina de conversão de entrada de matriz. Pode ser necessária uma especificação explícita do tipo.)

Agora podemos mostrar algumas declarações `INSERT`:

```
INSERT INTO sal_emp
    VALUES ('Bill',
    '{10000, 10000, 10000, 10000}',
    '{{"meeting", "lunch"}, {"training", "presentation"}}');

INSERT INTO sal_emp
    VALUES ('Carol',
    '{20000, 25000, 25000, 25000}',
    '{{"breakfast", "consulting"}, {"meeting", "lunch"}}');
```

O resultado dos dois insertos anteriores é o seguinte:

```
SELECT * FROM sal_emp;
 name  |      pay_by_quarter       |                 schedule
-------+---------------------------+-------------------------------------------
 Bill  | {10000,10000,10000,10000} | {{meeting,lunch},{training,presentation}}
 Carol | {20000,25000,25000,25000} | {{breakfast,consulting},{meeting,lunch}}
(2 rows)
```

Os arrays multidimensionais devem ter extensões correspondentes para cada dimensão. Uma incompatibilidade causa um erro, por exemplo:

```
INSERT INTO sal_emp
    VALUES ('Bill',
    '{10000, 10000, 10000, 10000}',
    '{{"meeting", "lunch"}, {"meeting"}}');
ERROR:  malformed array literal: "{{"meeting", "lunch"}, {"meeting"}}"
DETAIL:  Multidimensional arrays must have sub-arrays with matching dimensions.
```

A sintaxe do construtor `ARRAY` também pode ser usada:

```
INSERT INTO sal_emp
    VALUES ('Bill',
    ARRAY[10000, 10000, 10000, 10000],
    ARRAY[['meeting', 'lunch'], ['training', 'presentation']]);

INSERT INTO sal_emp
    VALUES ('Carol',
    ARRAY[20000, 25000, 25000, 25000],
    ARRAY[['breakfast', 'consulting'], ['meeting', 'lunch']]);
```

Observe que os elementos da matriz são constantes ou expressões comuns do SQL; por exemplo, as literais de string são citadas com aspas simples, em vez de aspas duplas, como faria em uma literal de matriz. A sintaxe do construtor `ARRAY` é discutida com mais detalhes em [Seção 4.2.12](sql-expressions.md#SQL-SYNTAX-ARRAY-CONSTRUCTORS).

### 8.15.3. Acessando Arrays [#](#ARRAYS-ACCESSING)

Agora, podemos executar algumas consultas na tabela. Primeiro, mostramos como acessar um único elemento de um array. Essa consulta recupera os nomes dos funcionários cuja remuneração mudou no segundo trimestre:

```
SELECT name FROM sal_emp WHERE pay_by_quarter[1] <> pay_by_quarter[2];

 name
-------
 Carol
(1 row)
```

Os números dos subíndices da matriz são escritos entre colchetes. Por padrão, o PostgreSQL usa uma convenção de numeração de base um para matrizes, ou seja, uma matriz de elementos de *`n`* começa com `array[1]` e termina com `array[n]`.

Essa consulta recupera o pagamento do terceiro trimestre de todos os funcionários:

```
SELECT pay_by_quarter[3] FROM sal_emp;

 pay_by_quarter
----------------
          10000
          25000
(2 rows)
```

Também podemos acessar fatias retangulares arbitrárias de uma matriz ou submatrizes. Uma fatia de matriz é indicada escrevendo `lower-bound:upper-bound` para uma ou mais dimensões da matriz. Por exemplo, esta consulta recupera o primeiro item no cronograma de Bill nos dois primeiros dias da semana:

```
SELECT schedule[1:2][1:1] FROM sal_emp WHERE name = 'Bill';

        schedule
------------------------
 {{meeting},{training}}
(1 row)
```

Se qualquer dimensão for escrita como uma fatia, ou seja, contém um colon, todas as dimensões são tratadas como fatias. Qualquer dimensão que tenha apenas um único número (sem colon) é tratada como sendo de 1 até o número especificado. Por exemplo, `[2]` é tratado como `[1:2]`, como neste exemplo:

```
SELECT schedule[1:2][2] FROM sal_emp WHERE name = 'Bill';

                 schedule
-------------------------------------------
 {{meeting,lunch},{training,presentation}}
(1 row)
```

Para evitar confusão com o caso sem fatias, é melhor usar a sintaxe de fatias para todas as dimensões, por exemplo, `[1:2][1:1]`, e não `[2][1:1]`.

É possível omitir o *`lower-bound`* e/ou *`upper-bound`* de um especificador de fatias; o limite ausente é substituído pelo limite inferior ou superior dos subíndices da matriz. Por exemplo:

```
SELECT schedule[:2][2:] FROM sal_emp WHERE name = 'Bill';

        schedule
------------------------
 {{lunch},{presentation}}
(1 row)

SELECT schedule[:][1:1] FROM sal_emp WHERE name = 'Bill';

        schedule
------------------------
 {{meeting},{training}}
(1 row)
```

Uma expressão de índice de matriz retornará null se o próprio array ou qualquer uma das expressões de índice forem null. Além disso, null é retornado se um índice estiver fora dos limites da matriz (este caso não gera um erro). Por exemplo, se `schedule` atualmente tem as dimensões `[1:3][1:2]`, então referenciar `schedule[3][3]` retorna NULL. Da mesma forma, uma referência de matriz com o número errado de índices gera um null em vez de um erro.

Uma expressão de fatiamento de matriz também retorna null se a própria matriz ou qualquer uma das expressões de índice forem null. No entanto, em outros casos, como selecionar uma fatia de matriz que esteja completamente fora dos limites da matriz atual, uma expressão de fatia retorna uma matriz vazia (de dimensão zero) em vez de null. (Isso não corresponde ao comportamento não-fatia e é feito por razões históricas.) Se a fatia solicitada sobrepõe-se parcialmente aos limites da matriz, então ela é silenciosamente reduzida apenas à região que sobrepõe-se, em vez de retornar null.

As dimensões atuais de qualquer valor da matriz podem ser recuperadas com a função `array_dims`:

```
SELECT array_dims(schedule) FROM sal_emp WHERE name = 'Carol';

 array_dims
------------
 [1:2][1:2]
(1 row)
```

`array_dims` produz um resultado `text`, que é conveniente para as pessoas lerem, mas talvez inconveniente para os programas. As dimensões também podem ser recuperadas com `array_upper` e `array_lower`, que retornam o limite superior e inferior de uma dimensão de matriz especificada, respectivamente:

```
SELECT array_upper(schedule, 1) FROM sal_emp WHERE name = 'Carol';

 array_upper
-------------
           2
(1 row)
```

`array_length` retornará o comprimento de uma dimensão de matriz especificada:

```
SELECT array_length(schedule, 1) FROM sal_emp WHERE name = 'Carol';

 array_length
--------------
            2
(1 row)
```

`cardinality` retorna o número total de elementos em um array em todas as dimensões. É efetivamente o número de linhas que uma chamada a `unnest` produziria:

```
SELECT cardinality(schedule) FROM sal_emp WHERE name = 'Carol';

 cardinality
-------------
           4
(1 row)
```

### 8.15.4. Modificando Arrays [#](#ARRAYS-MODIFYING)

Um valor de matriz pode ser substituído completamente:

```
UPDATE sal_emp SET pay_by_quarter = '{25000,25000,27000,27000}'
    WHERE name = 'Carol';
```

ou usando a sintaxe da expressão `ARRAY`:

```
UPDATE sal_emp SET pay_by_quarter = ARRAY[25000,25000,27000,27000]
    WHERE name = 'Carol';
```

Uma matriz também pode ser atualizada em um único elemento:

```
UPDATE sal_emp SET pay_by_quarter[4] = 15000
    WHERE name = 'Bill';
```

ou atualizado em uma fatia:

```
UPDATE sal_emp SET pay_by_quarter[1:2] = '{27000,27000}'
    WHERE name = 'Carol';
```

As sintaxe de fatiamento com *`lower-bound`* e/ou *`upper-bound`* omitidos também podem ser usadas, mas apenas ao atualizar um valor de matriz que não é NULL ou de dimensão zero (caso contrário, não há limite de índice existente para substituir).

Um valor de matriz armazenada pode ser ampliado atribuindo-se a elementos que não estão presentes. Quaisquer posições entre os elementos previamente presentes e os elementos recém-atribuídos serão preenchidos com nulos. Por exemplo, se a matriz `myarray` atualmente tem 4 elementos, ela terá seis elementos após uma atualização que atribui `myarray[6]`; `myarray[5]` conterá nulos. Atualmente, a ampliação dessa maneira só é permitida para matrizes unidimensionais, não para matrizes multidimensionais.

A atribuição com índice permite a criação de matrizes que não utilizam índices com base em um. Por exemplo, pode-se atribuir a `myarray[-2:7]` para criar uma matriz com valores de índice de -2 a 7.

Novos valores de matriz também podem ser construídos usando o operador de concatenação, `||`:

```
SELECT ARRAY[1,2] || ARRAY[3,4];
 ?column?
-----------
 {1,2,3,4}
(1 row)

SELECT ARRAY[5,6] || ARRAY[[1,2],[3,4]];
      ?column?
---------------------
 {{5,6},{1,2},{3,4}}
(1 row)
```

O operador de concatenação permite que um único elemento seja empurrado para o início ou para o final de uma matriz unidimensional. Ele também aceita duas matrizes *`N`*-dimensionais, ou uma matriz *`N`*-dimensional e uma *`N+1`*-dimensional.

Quando um único elemento é empurrado para o início ou para o final de uma matriz unidimensional, o resultado é uma matriz com o mesmo índice de limite inferior que o operando da matriz. Por exemplo:

```
SELECT array_dims(1 || '[0:1]={2,3}'::int[]);
 array_dims
------------
 [0:2]
(1 row)

SELECT array_dims(ARRAY[1,2] || 3);
 array_dims
------------
 [1:3]
(1 row)
```

Quando dois arrays com um número igual de dimensões são concatenados, o resultado mantém o índice de índice inferior do operador externo do operador de mão esquerda. O resultado é um array que compreende cada elemento do operador de mão esquerda seguido por cada elemento do operador de mão direita. Por exemplo:

```
SELECT array_dims(ARRAY[1,2] || ARRAY[3,4,5]);
 array_dims
------------
 [1:5]
(1 row)

SELECT array_dims(ARRAY[[1,2],[3,4]] || ARRAY[[5,6],[7,8],[9,0]]);
 array_dims
------------
 [1:5][1:2]
(1 row)
```

Quando uma matriz *`N`*-dimensional é empurrada para o início ou para o fim de uma matriz *`N+1`*-dimensional, o resultado é análogo ao caso da matriz de elementos acima. Cada submatriz *`N`*-dimensional é essencialmente um elemento da dimensão externa da matriz *`N+1`*-dimensional. Por exemplo:

```
SELECT array_dims(ARRAY[1,2] || ARRAY[[3,4],[5,6]]);
 array_dims
------------
 [1:3][1:2]
(1 row)
```

Uma matriz também pode ser construída usando as funções `array_prepend`, `array_append` ou `array_cat`. As duas primeiras apenas suportam matrizes unidimensionais, mas `array_cat` suporta matrizes multidimensionais. Alguns exemplos:

```
SELECT array_prepend(1, ARRAY[2,3]);
 array_prepend
---------------
 {1,2,3}
(1 row)

SELECT array_append(ARRAY[1,2], 3);
 array_append
--------------
 {1,2,3}
(1 row)

SELECT array_cat(ARRAY[1,2], ARRAY[3,4]);
 array_cat
-----------
 {1,2,3,4}
(1 row)

SELECT array_cat(ARRAY[[1,2],[3,4]], ARRAY[5,6]);
      array_cat
---------------------
 {{1,2},{3,4},{5,6}}
(1 row)

SELECT array_cat(ARRAY[5,6], ARRAY[[1,2],[3,4]]);
      array_cat
---------------------
 {{5,6},{1,2},{3,4}}
```

Em casos simples, o operador de concatenação discutido acima é preferido em relação ao uso direto dessas funções. No entanto, como o operador de concatenação é sobrecarregado para atender a todos os três casos, há situações em que o uso de uma das funções é útil para evitar ambiguidade. Por exemplo, considere:

```
SELECT ARRAY[1, 2] || '{3, 4}';  -- the untyped literal is taken as an array
 ?column?
-----------
 {1,2,3,4}

SELECT ARRAY[1, 2] || '7';                 -- so is this one
ERROR:  malformed array literal: "7"

SELECT ARRAY[1, 2] || NULL;                -- so is an undecorated NULL
 ?column?
----------
 {1,2}
(1 row)

SELECT array_append(ARRAY[1, 2], NULL);    -- this might have been meant
 array_append
--------------
 {1,2,NULL}
```

Nos exemplos acima, o analisador vê um array de inteiros de um lado do operador de concatenação e uma constante de tipo indeterminado do outro. A heurística que ele usa para resolver o tipo da constante é assumir que é do mesmo tipo que a outra entrada do operador — neste caso, array de inteiros. Portanto, presume-se que o operador de concatenação represente `array_cat`, não `array_append`. Quando essa é a escolha errada, ela pode ser corrigida ao converter a constante para o tipo do elemento do array; mas o uso explícito de `array_append` pode ser uma solução preferível.

### 8.15.5. Pesquisando em Arrays [#](#ARRAYS-SEARCHING)

Para procurar um valor em um array, cada valor deve ser verificado. Isso pode ser feito manualmente, se você conhece o tamanho do array. Por exemplo:

```
SELECT * FROM sal_emp WHERE pay_by_quarter[1] = 10000 OR
                            pay_by_quarter[2] = 10000 OR
                            pay_by_quarter[3] = 10000 OR
                            pay_by_quarter[4] = 10000;
```

No entanto, isso rapidamente se torna tedioso para grandes matrizes e não é útil se o tamanho da matriz é desconhecido. Um método alternativo é descrito em [Seção 9.25](functions-comparisons.md). A consulta acima pode ser substituída por:

```
SELECT * FROM sal_emp WHERE 10000 = ANY (pay_by_quarter);
```

Além disso, você pode encontrar linhas onde o array tem todos os valores iguais a 10000 com:

```
SELECT * FROM sal_emp WHERE 10000 = ALL (pay_by_quarter);
```

Como alternativa, pode ser usada a função `generate_subscripts`. Por exemplo:

```
SELECT * FROM
   (SELECT pay_by_quarter,
           generate_subscripts(pay_by_quarter, 1) AS s
      FROM sal_emp) AS foo
 WHERE pay_by_quarter[s] = 10000;
```

Essa função é descrita em [Tabela 9.70](functions-srf.md#FUNCTIONS-SRF-SUBSCRIPTS).

Você também pode pesquisar um array usando o operador `&&`, que verifica se o operando esquerdo sobrepõe-se ao operando direito. Por exemplo:

```
SELECT * FROM sal_emp WHERE pay_by_quarter && ARRAY[10000];
```

Isso e outros operadores de matriz são descritos mais adiante na [Seção 9.19](functions-array.md). Pode ser acelerado por um índice apropriado, conforme descrito na [Seção 11.2](indexes-types.md).

Você também pode procurar valores específicos em um array usando as funções `array_position` e `array_positions`. A primeira delas retorna o índice da primeira ocorrência de um valor em um array; a segunda retorna um array com os índices de todas as ocorrências do valor no array. Por exemplo:

```
SELECT array_position(ARRAY['sun','mon','tue','wed','thu','fri','sat'], 'mon');
 array_position
----------------
              2
(1 row)

SELECT array_positions(ARRAY[1, 4, 3, 1, 3, 4, 2, 1], 1);
 array_positions
-----------------
 {1,4,8}
(1 row)
```

### DICA

Os arrays não são conjuntos; procurar por elementos específicos de um array pode ser um sinal de um mau projeto de banco de dados. Considere usar uma tabela separada com uma linha para cada item que seria um elemento do array. Isso será mais fácil de pesquisar e provavelmente escalará melhor para um grande número de elementos.

### 8.15.6. Sintaxe de entrada e saída de matriz [#](#ARRAYS-IO)

A representação textual externa de um valor de matriz consiste em itens que são interpretados de acordo com as regras de conversão de E/S para o tipo de elemento da matriz, além de uma decoração que indica a estrutura da matriz. A decoração consiste em chaves angulares (`{` e `}`) ao redor do valor da matriz, além de caracteres de delimitador entre itens adjacentes. O caractere de delimitador é geralmente uma vírgula (`,`, mas pode ser algo mais: é determinado pelo ajuste `typdelim` para o tipo de elemento da matriz. Entre os tipos de dados padrão fornecidos na distribuição PostgreSQL, todos usam uma vírgula, exceto pelo tipo `box`, que usa um ponto e vírgula (`;`). Em uma matriz multidimensional, cada dimensão (linha, plano, cubo, etc.) recebe seu próprio nível de chaves angulares, e os delimitadores devem ser escritos entre entidades angulares adjacentes do mesmo nível.

A rotina de saída da matriz colocará aspas duplas nas valores dos elementos se eles forem cadeias vazias, contenham chaves, caracteres de delimitador, aspas duplas, barras invertidas ou espaços em branco, ou correspondam à palavra `NULL`. Aspas duplas e barras invertidas embutidas nos valores dos elementos serão escapadas por barra invertida. Para os tipos de dados numéricos, é seguro assumir que as aspas nunca aparecerão, mas para os tipos de dados textuais, deve-se estar preparado para lidar com a presença ou ausência de aspas.

Por padrão, o valor inferior do índice de uma dimensão de um array é definido como um. Para representar arrays com outros limites inferiores, os intervalos de subscrito de array podem ser especificados explicitamente antes de escrever o conteúdo do array. Essa decoração consiste em chaves quadradas (`[]`) ao redor dos limites inferiores e superiores de cada dimensão do array, com um caractere de delimitador de colon (`:`). A decoração da dimensão do array é seguida por um sinal de igual (`=`). Por exemplo:

```
SELECT f1[1][-2][3] AS e1, f1[1][-1][5] AS e2
 FROM (SELECT '[1:1][-2:-1][3:5]={{{1,2,3},{4,5,6}}}'::int[] AS f1) AS ss;

 e1 | e2
----+----
  1 |  6
(1 row)
```

A rotina de saída de matriz incluirá dimensões explícitas em seu resultado apenas quando houver um ou mais limites inferiores diferentes de um.

Se o valor escrito para um elemento for `NULL` (em qualquer caso, variante), o elemento é considerado NULL. A presença de quaisquer aspas ou barras invertidas desativa isso e permite que o valor literal da string “NULL” seja inserido. Além disso, para compatibilidade reversa com versões anteriores à versão 8.2 do PostgreSQL, o parâmetro de configuração [array_nulls](runtime-config-compatible.md#GUC-ARRAY-NULLS) pode ser convertido em `off` para suprimir o reconhecimento de `NULL` como NULL.

Como mostrado anteriormente, ao escrever um valor de matriz, você pode usar aspas duplas em torno de qualquer elemento individual da matriz. Você *deve* fazer isso se o valor do elemento de outra forma confundir o analisador de valor de matriz. Por exemplo, elementos que contêm chaves, vírgulas (ou o caractere delimitador do tipo de dados), aspas duplas, barras invertidas ou espaços em branco no início ou no fim devem ser citados. Strings vazias e strings que correspondem à palavra `NULL` também devem ser citadas. Para colocar uma aspa dupla ou barra invertida em um valor de elemento de matriz com aspas duplas, preceda-a com uma barra invertida. Alternativamente, você pode evitar aspas e usar escapagem de barra invertida para proteger todos os caracteres de dados que de outra forma seriam tomados como sintaxe de matriz.

Você pode adicionar espaços em branco antes de uma brace esquerda ou após uma brace direita. Você também pode adicionar espaços em branco antes ou depois de qualquer item de cadeia individual. Em todos esses casos, os espaços em branco serão ignorados. No entanto, os espaços em branco dentro de elementos com aspas duplas, ou cercados em ambos os lados por caracteres não-espaçados de um elemento, não são ignorados.

### DICA

A sintaxe do construtor `ARRAY` (ver [Seção 4.2.12](sql-expressions.md#SQL-SYNTAX-ARRAY-CONSTRUCTORS)) é frequentemente mais fácil de trabalhar do que a sintaxe de literal de matriz ao escrever valores de matriz em comandos SQL. Em `ARRAY`, os valores de elementos individuais são escritos da mesma maneira que seriam escritos quando não são membros de uma matriz.
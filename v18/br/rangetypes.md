## 8.17. Tipos de intervalo [#](#RANGETYPES)

* [8.17.1. Tipos de intervalo embutido e multiintervalo][(rangetypes.md#RANGETYPES-BUILTIN)
* [8.17.2. Exemplos][(rangetypes.md#RANGETYPES-EXAMPLES)
* [8.17.3. Limites inclusivos e exclusivos][(rangetypes.md#RANGETYPES-INCLUSIVITY)
* [8.17.4. Intervalos infinitos (sem limites][(rangetypes.md#RANGETYPES-INFINITE)
* [8.17.5. Entrada/saída de intervalo][(rangetypes.md#RANGETYPES-IO)
* [8.17.6. Construção de intervalos e multiintervalos][(rangetypes.md#RANGETYPES-CONSTRUCT)
* [8.17.7. Tipos de intervalo discreto][(rangetypes.md#RANGETYPES-DISCRETE)
* [8.17.8. Definição de novos tipos de intervalo][(rangetypes.md#RANGETYPES-DEFINING)
* [8.17.9. Indexação][(rangetypes.md#RANGETYPES-INDEXING)
* [8.17.10. Restrições em intervalos][(rangetypes.md#RANGETYPES-CONSTRAINT)

Os tipos de intervalo são tipos de dados que representam uma faixa de valores de algum tipo de elemento (chamado de *subtipo* do intervalo). Por exemplo, os intervalos de `timestamp` podem ser usados para representar as faixas de tempo em que uma sala de reunião é reservada. Neste caso, o tipo de dados é `tsrange` (abreviação de “faixa de temporização”), e `timestamp` é o subtipo. O subtipo deve ter uma ordem total para que seja bem definido se os valores do elemento estão dentro, antes ou depois de uma faixa de valores.

Os tipos de intervalo são úteis porque representam muitos valores de elementos em um único valor de intervalo, e porque conceitos como intervalos sobrepostos podem ser expressos claramente. O uso de intervalos de tempo e data para fins de programação é o exemplo mais claro; mas intervalos de preço, intervalos de medição de um instrumento, e assim por diante também podem ser úteis.

Cada tipo de intervalo tem um tipo correspondente de multiintervalo. Um multiintervalo é uma lista ordenada de intervalos não contíguos, não vazios e não nulos. A maioria dos operadores de intervalo também funciona em multiintervalos, e eles têm algumas funções próprias.

### 8.17.1. Tipos de faixa integrada e multifaixa [#](#RANGETYPES-BUILTIN)

O PostgreSQL vem com os seguintes tipos de intervalo embutidos:

* `int4range` — Gama de `integer`, `int4multirange` — Multigama correspondente
* `int8range` — Gama de `bigint`, `int8multirange` — Multigama correspondente
* `numrange` — Gama de `numeric`, `nummultirange` — Multigama correspondente
* `tsrange` — Gama de `timestamp without time zone`, `tsmultirange` — Multigama correspondente
* `tstzrange` — Gama de `timestamp with time zone`, `tstzmultirange` — Multigama correspondente
* `daterange` — Gama de `date`, `datemultirange` — Multigama correspondente

Além disso, você pode definir seus próprios tipos de intervalo; consulte [CREATE TYPE](sql-createtype.md "CREATE TYPE") para mais informações.

### 8.17.2. Exemplos [#](#RANGETYPES-EXAMPLES)

```
CREATE TABLE reservation (room int, during tsrange);
INSERT INTO reservation VALUES
    (1108, '[2010-01-01 14:30, 2010-01-01 15:30)');

-- Containment
SELECT int4range(10, 20) @> 3;

-- Overlaps
SELECT numrange(11.1, 22.2) && numrange(20.0, 30.0);

-- Extract the upper bound
SELECT upper(int8range(15, 25));

-- Compute the intersection
SELECT int4range(10, 20) * int4range(15, 25);

-- Is the range empty?
SELECT isempty(numrange(1, 5));
```

Consulte as tabelas [Tabela 9.58](functions-range.md#RANGE-OPERATORS-TABLE) e [Tabela 9.60](functions-range.md#RANGE-FUNCTIONS-TABLE) para obter listas completas dos operadores e funções sobre os tipos de intervalo.

### 8.17.3. Limites inclusivos e exclusivos [#](#RANGETYPES-INCLUSIVITY)

Cada intervalo não vazio tem dois limites, o limite inferior e o limite superior. Todos os pontos entre esses valores estão incluídos no intervalo. Um limite inclusivo significa que o próprio ponto de limite está incluído no intervalo, enquanto um limite exclusivo significa que o ponto de limite não está incluído no intervalo.

Na forma textual de uma faixa, uma faixa inferior inclusiva é representada por “`[`”, enquanto uma faixa inferior exclusiva é representada por “`(`”. Da mesma forma, uma faixa superior inclusiva é representada por “`]`”, enquanto uma faixa superior exclusiva é representada por “`)`”. (Veja [Seção 8.17.5](rangetypes.md#RANGETYPES-IO "8.17.5. Range Input/Output") para mais detalhes.)

As funções `lower_inc` e `upper_inc` testam a inclusividade dos limites inferior e superior de um valor de intervalo, respectivamente.

### 8.17.4. Intervalos infinitos (sem limites) [#](#RANGETYPES-INFINITE)

O limite inferior de uma faixa pode ser omitido, o que significa que todos os valores menores que o limite superior são incluídos na faixa, por exemplo, `(,3]`. Da mesma forma, se o limite superior da faixa for omitido, então todos os valores maiores que o limite inferior são incluídos na faixa. Se ambos os limites inferior e superior forem omitidos, todos os valores do tipo de elemento são considerados na faixa. Especificar um limite ausente como inclusivo é automaticamente convertido para exclusivo, por exemplo, `[,]` é convertido para `(,)`. Você pode pensar nesses valores ausentes como +/-infinito, mas eles são valores especiais do tipo de faixa e são considerados além de quaisquer valores +/-infinito de qualquer tipo de elemento de faixa.

Os tipos de elemento que possuem a noção de “infinito” podem usá-los como valores de limite explícitos. Por exemplo, com intervalos de marcação de tempo, `[today,infinity)` exclui o valor especial `timestamp`, enquanto `[today,infinity]` o inclui, assim como `[today,)` e `[today,]`.

As funções `lower_inf` e `upper_inf` testam limites inferiores e superiores infinitos, respectivamente.

### 8.17.5. Entrada/Saída de alcance [#](#RANGETYPES-IO)

A entrada para um valor de intervalo deve seguir um dos seguintes padrões:

```
(lower-bound,upper-bound)
(lower-bound,upper-bound]
[lower-bound,upper-bound)
[lower-bound,upper-bound]
empty
```

As chaves ou parênteses indicam se os limites inferior e superior são exclusivos ou inclusivos, conforme descrito anteriormente. Observe que o padrão final é `empty`, que representa uma faixa vazia (uma faixa que não contém pontos).

O *`lower-bound`* pode ser uma cadeia de caracteres que é uma entrada válida para o subtipo, ou vazio para indicar nenhuma restrição inferior. Da mesma forma, *`upper-bound`* pode ser uma cadeia de caracteres que é uma entrada válida para o subtipo, ou vazio para indicar nenhuma restrição superior.

Cada valor vinculado pode ser citado usando caracteres `"` (aspas duplas). Isso é necessário se o valor vinculado contiver parênteses, colchetes, vírgulas, aspas duplas ou barras invertidas, pois, caso contrário, esses caracteres seriam considerados parte da sintaxe de intervalo. Para colocar uma aspa dupla ou barra invertida em um valor vinculado citado, anteceda-a com uma barra invertida. (Além disso, um par de aspas duplas dentro de um valor vinculado com aspas duplas é considerado uma representação de um caractere de aspa dupla, de forma análoga às regras para aspas simples em strings literais SQL.) Alternativamente, você pode evitar a citação e usar escapagem com barra invertida para proteger todos os caracteres de dados que, caso contrário, seriam considerados sintaxe de intervalo. Além disso, para escrever um valor vinculado que é uma string vazia, escreva `""`, pois escrever nada significa um intervalo infinito.

Espaços em branco são permitidos antes e depois do valor da faixa, mas quaisquer espaços em branco entre os parênteses ou chaves são considerados parte do valor da faixa inferior ou superior. (Dependendo do tipo de elemento, pode ou não ser significativo.)

### Nota

Essas regras são muito semelhantes às que se aplicam à escrita de valores de campo em literais de tipo composto. Consulte [Seção 8.16.6] para comentários adicionais.

Exemplos:

```
-- includes 3, does not include 7, and does include all points in between
SELECT '[3,7)'::int4range;

-- does not include either 3 or 7, but includes all points in between
SELECT '(3,7)'::int4range;

-- includes only the single point 4
SELECT '[4,4]'::int4range;

-- includes no points (and will be normalized to 'empty')
SELECT '[4,4)'::int4range;
```

A entrada para um multirange é entre chaves espirais (`{` e `}`) que contêm zero ou mais intervalos válidos, separados por vírgulas. Espaços em branco são permitidos ao redor das chaves e vírgulas. Isso é destinado a lembrar a sintaxe de matriz, embora os multiranges sejam muito mais simples: eles têm apenas uma dimensão e não há necessidade de citar seus conteúdos. (Os limites de seus intervalos podem ser citados como acima, no entanto.)

Exemplos:

```
SELECT '{}'::int4multirange;
SELECT '{[3,7)}'::int4multirange;
SELECT '{[3,7), [8,9)}'::int4multirange;
```

### 8.17.6. Construção de intervalos e multiintervalos [#](#RANGETYPES-CONSTRUCT)

Cada tipo de intervalo tem uma função construtor com o mesmo nome que o tipo de intervalo. Usar a função construtor é frequentemente mais conveniente do que escrever uma constante literal de intervalo, pois evita a necessidade de citação extra dos valores de limite. A função construtor aceita dois ou três argumentos. A forma de dois argumentos constrói um intervalo na forma padrão (limite inferior inclusivo, limite superior exclusivo), enquanto a forma de três argumentos constrói um intervalo com limites da forma especificada pelo terceiro argumento. O terceiro argumento deve ser uma das strings “`()`”, “`(]`”, “`[)`” ou “`[]`”. Por exemplo:

```
-- The full form is: lower bound, upper bound, and text argument indicating
-- inclusivity/exclusivity of bounds.
SELECT numrange(1.0, 14.0, '(]');

-- If the third argument is omitted, '[)' is assumed.
SELECT numrange(1.0, 14.0);

-- Although '(]' is specified here, on display the value will be converted to
-- canonical form, since int8range is a discrete range type (see below).
SELECT int8range(1, 14, '(]');

-- Using NULL for either bound causes the range to be unbounded on that side.
SELECT numrange(NULL, 2.2);
```

Cada tipo de intervalo também tem um construtor multirange com o mesmo nome que o tipo multirange. A função construtor recebe zero ou mais argumentos, que são todos os intervalos do tipo apropriado. Por exemplo:

```
SELECT nummultirange();
SELECT nummultirange(numrange(1.0, 14.0));
SELECT nummultirange(numrange(1.0, 14.0), numrange(20.0, 25.0));
```

### 8.17.7. Tipos de intervalo discreto [#](#RANGETYPES-DISCRETE)

Uma faixa discreta é aquela cujo tipo de elemento tem um "passo" bem definido, como `integer` ou `date`. Nesses tipos, pode-se dizer que dois elementos são adjacentes quando não há valores válidos entre eles. Isso contrasta com as faixas contínuas, onde é sempre (ou quase sempre) possível identificar outros valores de elementos entre dois valores dados. Por exemplo, uma faixa sobre o tipo `numeric` é contínua, assim como uma faixa sobre `timestamp`. (Embora `timestamp` tenha precisão limitada, e portanto, teoricamente, possa ser tratado como discreto, é melhor considerá-lo contínuo, uma vez que o tamanho do passo normalmente não é de interesse.)

Outra maneira de pensar em um tipo de intervalo discreto é que há uma ideia clara de um valor "próximo" ou "anterior" para cada valor do elemento. Sabendo disso, é possível converter entre representações inclusivas e exclusivas dos limites de uma faixa, escolhendo o valor do próximo ou anterior elemento em vez do original dado. Por exemplo, em um tipo de intervalo de número inteiro `[4,8]` e `(3,9)` denotam o mesmo conjunto de valores; mas isso não seria o mesmo para uma faixa sobre números.

Um tipo de intervalo discreto deve ter uma função de *canonicização* que esteja ciente do tamanho desejado do passo para o tipo de elemento. A função de canonicização é responsável por converter valores equivalentes do tipo de intervalo para ter representações idênticas, em particular limites consistentemente inclusivos ou exclusivos. Se uma função de canonicização não for especificada, então os intervalos com diferentes formatos serão sempre tratados como desiguais, mesmo que possam representar o mesmo conjunto de valores na realidade.

Os tipos de intervalo embutidos `int4range`, `int8range` e `daterange` utilizam uma forma canônica que inclui o limite inferior e exclui o limite superior; ou seja, `[)`. No entanto, os tipos de intervalo definidos pelo usuário podem utilizar outras convenções.

### 8.17.8. Definindo novos tipos de faixa [#](#RANGETYPES-DEFINING)

Os usuários podem definir seus próprios tipos de intervalo. A razão mais comum para fazer isso é usar intervalos sobre subtipos que não estão fornecidos entre os tipos de intervalo pré-definidos. Por exemplo, para definir um novo tipo de intervalo de subtipo `float8`:

```
CREATE TYPE floatrange AS RANGE (
    subtype = float8,
    subtype_diff = float8mi
);

SELECT '[1.234, 5.678]'::floatrange;
```

Como o `float8` não tem um "passo" significativo, não definimos uma função de normalização neste exemplo.

Quando você define sua própria faixa, você automaticamente obtém um tipo de faixa correspondente.

Definir o próprio tipo de intervalo também permite especificar uma classe de operador de árvore B-subtipo diferente ou uma correção de colocação a ser usada, para alterar a ordem de classificação que determina quais valores caem em um intervalo dado.

Se o subtipo for considerado ter valores discretos em vez de contínuos, o comando `CREATE TYPE` deve especificar uma função `canonical`. A função de canonicização recebe um valor de intervalo de entrada e deve retornar um valor equivalente que pode ter limites e formatação diferentes. A saída canônica para dois intervalos que representam o mesmo conjunto de valores, por exemplo, os intervalos inteiros `[1, 7]` e `[1, 8)`, deve ser idêntica. Não importa qual representação você escolha como a canônica, desde que dois valores equivalentes com formatações diferentes sempre sejam mapeados para o mesmo valor com a mesma formatação. Além de ajustar o formato de limites inclusivo/exclusivo, uma função de canonicização pode arredondar valores de limite, no caso de o tamanho do passo desejado ser maior do que o que o subtipo é capaz de armazenar. Por exemplo, um tipo de intervalo sobre `timestamp` pode ser definido para ter um tamanho de passo de uma hora, nesse caso, a função de canonicização precisaria arredondar limites que não fossem múltiplo de uma hora, ou talvez lançar um erro em vez disso.

Além disso, qualquer tipo de intervalo que seja destinado a ser usado com índices GiST ou SP-GiST deve definir uma função de diferença de subtipo, ou `subtype_diff`, (O índice ainda funcionará sem `subtype_diff`, mas é provável que seja consideravelmente menos eficiente do que se uma função de diferença for fornecida). A função de diferença de subtipo recebe dois valores de entrada do subtipo e retorna sua diferença (ou seja, *`X`* menos *`Y`*) representada como um valor de `float8`. No nosso exemplo acima, a função `float8mi` que está por trás do operador regular de menos `float8` pode ser usada; mas para qualquer outro subtipo, seria necessário algum tipo de conversão. Também pode ser necessário algum pensamento criativo sobre como representar diferenças como números. Na medida do possível, a função `subtype_diff` deve concordar com a ordem de classificação implícita pela classe de operador e correção selecionada; ou seja, seu resultado deve ser positivo sempre que seu primeiro argumento for maior que seu segundo de acordo com a ordem de classificação.

Um exemplo menos simplificado de uma função `subtype_diff` é:

```
CREATE FUNCTION time_subtype_diff(x time, y time) RETURNS float8 AS
'SELECT EXTRACT(EPOCH FROM (x - y))' LANGUAGE sql STRICT IMMUTABLE;

CREATE TYPE timerange AS RANGE (
    subtype = time,
    subtype_diff = time_subtype_diff
);

SELECT '[11:10, 23:00]'::timerange;
```

Veja [CREATE TYPE](sql-createtype.md "CREATE TYPE") para mais informações sobre a criação de tipos de intervalo.

### 8.17.9. Indexação [#](#RANGETYPES-INDEXING)

Os índices GiST e SP-GiST podem ser criados para colunas de tabela de tipos de intervalo. Os índices GiST também podem ser criados para colunas de tabela de tipos de multiintervalo. Por exemplo, para criar um índice GiST:

```
CREATE INDEX reservation_idx ON reservation USING GIST (during);
```

Um índice GiST ou SP-GiST em intervalos pode acelerar consultas que envolvem esses operadores de intervalo: `=`, `&&`, `<@`, `@>`, `<<`, `>>`, `-|-`, `&<` e `&>`. Um índice GiST em intervalos múltiplos pode acelerar consultas que envolvem o mesmo conjunto de operadores de intervalo múltiplos. Um índice GiST em intervalos e um índice GiST em intervalos múltiplos também pode acelerar consultas que envolvem esses operadores de tipo cruzado de intervalo para múltiplos e de múltiplos para intervalo, respectivamente: `&&`, `<@`, `@>`, `<<`, `>>`, `-|-`, `&<` e `&>`. Consulte [Tabela 9.58](functions-range.md#RANGE-OPERATORS-TABLE) para mais informações.

Além disso, índices de árvore B e de hash podem ser criados para as colunas de tabelas de tipos de intervalo. Para esses tipos de índice, basicamente a única operação de intervalo útil é a igualdade. Existe uma ordenação de classificação de árvore B definida para valores de intervalo, com operadores correspondentes `<` e `>`, mas a ordenação é bastante arbitrária e geralmente não é útil no mundo real. O suporte de árvore B e de hash dos tipos de intervalo é destinado principalmente a permitir a classificação e a hashing internamente em consultas, em vez da criação de índices reais.

### 8.17.10. Restrições em intervalos [#](#RANGETYPES-CONSTRAINT)

Embora `UNIQUE` seja uma restrição natural para valores escalares, geralmente é inadequado para tipos de intervalo. Em vez disso, uma restrição de exclusão é frequentemente mais apropriada (consulte [CREATE TABLE ... CONSTRAINT ... EXCLUDE](sql-createtable.md#SQL-CREATETABLE-EXCLUDE)). As restrições de exclusão permitem a especificação de restrições, como "não sobreposição", em um tipo de intervalo. Por exemplo:

```
CREATE TABLE reservation (
    during tsrange,
    EXCLUDE USING GIST (during WITH &&)
);
```

Essa restrição impedirá que valores sobrepostos existam na tabela ao mesmo tempo:

```
INSERT INTO reservation VALUES
    ('[2010-01-01 11:30, 2010-01-01 15:00)');
INSERT 0 1

INSERT INTO reservation VALUES
    ('[2010-01-01 14:45, 2010-01-01 15:45)');
ERROR:  conflicting key value violates exclusion constraint "reservation_during_excl"
DETAIL:  Key (during)=(["2010-01-01 14:45:00","2010-01-01 15:45:00")) conflicts
with existing key (during)=(["2010-01-01 11:30:00","2010-01-01 15:00:00")).
```

Você pode usar a extensão `btree_gist`](btree-gist.md) para definir restrições de exclusão em tipos de dados escalares simples, que podem ser combinadas com exclusões de intervalo para máxima flexibilidade. Por exemplo, após o `btree_gist` ser instalado, a seguinte restrição rejeitará os intervalos sobrepostos apenas se os números das salas de reunião forem iguais:

```
CREATE EXTENSION btree_gist;
CREATE TABLE room_reservation (
    room text,
    during tsrange,
    EXCLUDE USING GIST (room WITH =, during WITH &&)
);

INSERT INTO room_reservation VALUES
    ('123A', '[2010-01-01 14:00, 2010-01-01 15:00)');
INSERT 0 1

INSERT INTO room_reservation VALUES
    ('123A', '[2010-01-01 14:30, 2010-01-01 15:30)');
ERROR:  conflicting key value violates exclusion constraint "room_reservation_room_during_excl"
DETAIL:  Key (room, during)=(123A, ["2010-01-01 14:30:00","2010-01-01 15:30:00")) conflicts
with existing key (room, during)=(123A, ["2010-01-01 14:00:00","2010-01-01 15:00:00")).

INSERT INTO room_reservation VALUES
    ('123B', '[2010-01-01 14:30, 2010-01-01 15:30)');
INSERT 0 1
```

### 8.16. Tipos compostos [#](#ROWTYPES)

* [8.16.1. Declaração de Tipos Compostos](rowtypes.md#ROWTYPES-DECLARING)
* [8.16.2. Construção de Valores Compostos](rowtypes.md#ROWTYPES-CONSTRUCTING)
* [8.16.3. Acesso a Tipos Compostos](rowtypes.md#ROWTYPES-ACCESSING)
* [8.16.4. Modificação de Tipos Compostos](rowtypes.md#ROWTYPES-MODIFYING)
* [8.16.5. Uso de Tipos Compostos em Consultas](rowtypes.md#ROWTYPES-USAGE)
* [8.16.6. Sintaxe de Entrada e Saída de Tipos Compostos](rowtypes.md#ROWTYPES-IO-SYNTAX)

Um *tipo composto* representa a estrutura de uma linha ou registro; ele é essencialmente apenas uma lista de nomes de campos e seus tipos de dados. O PostgreSQL permite que tipos compostos sejam usados de muitas das mesmas maneiras que os tipos simples podem ser usados. Por exemplo, uma coluna de uma tabela pode ser declarada como um tipo composto.

#### 8.16.1. Declaração de tipos compostos [#](#ROWTYPES-DECLARING)

Aqui estão dois exemplos simples de definição de tipos compostos:

```sql
CREATE TYPE complex AS (
    r       double precision,
    i       double precision
);

CREATE TYPE inventory_item AS (
    name            text,
    supplier_id     integer,
    price           numeric
);
```

A sintaxe é comparável a `CREATE TABLE`, exceto que apenas os nomes e tipos de campo podem ser especificados; não é possível incluir restrições (como `NOT NULL`) atualmente. Note que a palavra-chave `AS` é essencial; sem ela, o sistema pensará que um tipo diferente de comando `CREATE TYPE` é pretendido, e você receberá erros de sintaxe estranhos.

Definindo os tipos, podemos usá-los para criar tabelas:

```sql
CREATE TABLE on_hand (
    item      inventory_item,
    count     integer
);

INSERT INTO on_hand VALUES (ROW('fuzzy dice', 42, 1.99), 1000);
```

ou funções:

```sql
CREATE FUNCTION price_extension(inventory_item, integer) RETURNS numeric
AS 'SELECT $1.price * $2' LANGUAGE SQL;

SELECT price_extension(item, 10) FROM on_hand;
```

Sempre que você cria uma tabela, um tipo composto também é criado automaticamente, com o mesmo nome da tabela, para representar o tipo de linha da tabela. Por exemplo, se tivéssemos dito:

```sql
CREATE TABLE inventory_item (
    name            text,
    supplier_id     integer REFERENCES suppliers,
    price           numeric CHECK (price > 0)
);
```

então, o mesmo tipo composto `inventory_item` mostrado acima seria criado como um subproduto e poderia ser usado da mesma forma que acima. No entanto, observe uma restrição importante da implementação atual: como não há restrições associadas a um tipo composto, as restrições mostradas na definição da tabela *não se aplicam* a valores do tipo composto fora da tabela. (Para contornar isso, crie um [*[domain](glossary.md#GLOSSARY-DOMAIN "Domain")*](glossary.md#GLOSSARY-DOMAIN) sobre o tipo composto e aplique as restrições desejadas como restrições `CHECK` do domínio.)

#### 8.16.2. Construção de Valores Compostos [#](#ROWTYPES-CONSTRUCTING)

Para escrever um valor composto como uma constante literal, coloque os valores do campo entre parênteses e separe-os por vírgulas. Você pode colocar aspas duplas em torno de qualquer valor do campo e deve fazê-lo se ele contiver vírgulas ou parênteses. (Mais detalhes aparecem [abaixo](rowtypes.md#ROWTYPES-IO-SYNTAX).). Assim, o formato geral de uma constante composta é o seguinte:

```sql
'( val1 , val2 , ... )'
```

Um exemplo é:

```sql
'("fuzzy dice",42,1.99)'
```

que seria um valor válido do tipo `inventory_item` definido acima. Para fazer um campo ser NULL, não escreva nenhum caractere em sua posição na lista. Por exemplo, esta constante especifica um terceiro campo NULL:

```sql
'("fuzzy dice",42,)'
```

Se você deseja uma string vazia em vez de NULL, escreva aspas duplas:

```sql
'("",42,)'
```

Aqui, o primeiro campo é uma string vazia não nula, o terceiro é NULL.

(Essas constantes são, na verdade, apenas um caso especial das constantes de tipo genérico discutidas na [Seção 4.1.2.7] (sql-syntax-lexical.md#SQL-SYNTAX-CONSTANTS-GENERIC "4.1.2.7. Constants of Other Types"). A constante é inicialmente tratada como uma string e passada para a rotina de conversão de entrada de tipo composto. Pode ser necessário uma especificação explícita do tipo para dizer qual tipo converter a constante.)

A sintaxe da expressão `ROW` também pode ser usada para construir valores compostos. Na maioria dos casos, essa sintaxe é consideravelmente mais simples de usar do que a sintaxe de literal de string, pois você não precisa se preocupar com múltiplas camadas de citação. Já usamos esse método acima:

```sql
ROW('fuzzy dice', 42, 1.99)
ROW('', 42, NULL)
```

A palavra-chave ROW é, na verdade, opcional, desde que você tenha mais de um campo na expressão, então esses podem ser simplificados para:

```sql
('fuzzy dice', 42, 1.99)
('', 42, NULL)
```

A sintaxe da expressão `ROW` é discutida em mais detalhes em [Seção 4.2.13](sql-expressions.md#SQL-SYNTAX-ROW-CONSTRUCTORS).

#### 8.16.3. Acesso a Tipos Compostos [#](#ROWTYPES-ACCESSING)

Para acessar um campo de uma coluna composta, escreve-se um ponto e o nome do campo, muito parecido com selecionar um campo de um nome de tabela. De fato, é tão parecido com selecionar de um nome de tabela que você muitas vezes tem que usar parênteses para não confundir o analisador. Por exemplo, você pode tentar selecionar alguns subcampos da nossa tabela exemplo `on_hand` com algo como:

```sql
SELECT item.name FROM on_hand WHERE item.price > 9.99;
```

Isso não funcionará, pois o nome `item` é considerado um nome de tabela, não um nome de coluna de `on_hand`, de acordo com as regras de sintaxe do SQL. Você deve escrevê-lo assim:

```sql
SELECT (item).name FROM on_hand WHERE (item).price > 9.99;
```

ou se você precisar usar o nome da tabela também (por exemplo, em uma consulta multitabela), como este:

```sql
SELECT (on_hand.item).name FROM on_hand WHERE (on_hand.item).price > 9.99;
```

Agora, o objeto entre parênteses é interpretado corretamente como uma referência à coluna `item`, e então o subcampo pode ser selecionado a partir dela.

Problemas sintáticos semelhantes se aplicam sempre que você seleciona um campo de um valor composto. Por exemplo, para selecionar apenas um campo do resultado de uma função que retorna um valor composto, você precisaria escrever algo como:

```sql
SELECT (my_func(...)).field FROM ...
```

Sem as chaves adicionais, isso gerará um erro de sintaxe.

O nome especial do campo `*` significa “todos os campos”, conforme explicado mais detalhadamente em [Seção 8.16.5](rowtypes.md#ROWTYPES-USAGE).

#### 8.16.4. Modificando tipos compostos [#](#ROWTYPES-MODIFYING)

Aqui estão alguns exemplos da sintaxe correta para inserir e atualizar colunas compostas. Primeiro, inserir ou atualizar uma coluna inteira:

```sql
INSERT INTO mytab (complex_col) VALUES((1.1,2.2));

UPDATE mytab SET complex_col = ROW(1.1,2.2) WHERE ...;
```

O primeiro exemplo omite `ROW`, o segundo o usa; poderíamos ter feito de qualquer jeito.

Podemos atualizar um subcampo individual de uma coluna composta:

```sql
UPDATE mytab SET complex_col.r = (complex_col).r + 1 WHERE ...;
```

Observe aqui que não precisamos (e de fato não podemos) colocar parênteses ao redor do nome da coluna que aparece logo após `SET`, mas precisamos de parênteses quando referenciamos a mesma coluna na expressão à direita do sinal de igual.

E podemos especificar subcampos como alvos para `INSERT`, também:

```sql
INSERT INTO mytab (complex_col.r, complex_col.i) VALUES(1.1, 2.2);
```

Se não tivéssemos fornecido valores para todos os subcampos da coluna, os subcampos restantes teriam sido preenchidos com valores nulos.

#### 8.16.5. Uso de tipos compostos em consultas [#](#ROWTYPES-USAGE)

Existem várias regras de sintaxe especiais e comportamentos associados a tipos compostos em consultas. Essas regras fornecem atalhos úteis, mas podem ser confusas se você não conhece a lógica por trás delas.

Em PostgreSQL, uma referência a um nome de tabela (ou alias) em uma consulta é, efetivamente, uma referência ao valor composto da linha atual da tabela. Por exemplo, se tivéssemos uma tabela `inventory_item` como mostrado acima (rowtypes.md#ROWTYPES-DECLARING "8.16.1. Declaration of Composite Types"), poderíamos escrever:

```sql
SELECT c FROM inventory_item c;
```

Essa consulta produz uma coluna com valor composto único, então podemos obter uma saída como:

```sql
           c
------------------------
 ("fuzzy dice",42,1.99)
(1 row)
```

Observe, no entanto, que os nomes simples são correspondidos aos nomes das colunas antes dos nomes das tabelas, então este exemplo funciona apenas porque não há uma coluna com o nome `c` nas tabelas da consulta.

A sintaxe comum de nome de coluna qualificada *`table_name`*`.`*`column_name`* pode ser entendida como a aplicação de [seleção de campo](sql-expressions.md#FIELD-SELECTION) ao valor composto da linha atual da tabela. (Por razões de eficiência, na verdade, não é implementada dessa maneira.)

Quando escrevemos

```sql
SELECT c.* FROM inventory_item c;
```

Então, de acordo com o padrão SQL, devemos obter o conteúdo da tabela expandido em colunas separadas:

```sql
    name    | supplier_id | price
------------+-------------+-------
 fuzzy dice |          42 |  1.99
(1 row)
```

como se a consulta fosse

```sql
SELECT c.name, c.supplier_id, c.price FROM inventory_item c;
```

O PostgreSQL aplicará esse comportamento de expansão a qualquer expressão com valor composto, embora, como mostrado acima, (rowtypes.md#ROWTYPES-ACCESSING "8.16.3. Accessing Composite Types"), você precisa escrever parênteses ao redor do valor para o qual `.*` é aplicado, sempre que não seja um nome simples de tabela. Por exemplo, se `myfunc()` é uma função que retorna um tipo composto com colunas `a`, `b` e `c`, então essas duas consultas têm o mesmo resultado:

```sql
SELECT (myfunc(x)).* FROM some_table;
SELECT (myfunc(x)).a, (myfunc(x)).b, (myfunc(x)).c FROM some_table;
```

DICA

O PostgreSQL trata a expansão de colunas, transformando efetivamente a primeira forma na segunda. Assim, neste exemplo, `myfunc()` seria invocado três vezes por linha com qualquer sintaxe. Se for uma função cara, você pode querer evitá-la, o que pode ser feito com uma consulta como:

```sql
SELECT m.* FROM some_table, LATERAL myfunc(x) AS m;
```

Colocar a função em um item `LATERAL` `FROM` impede que ela seja invocada mais de uma vez por linha. `m.*` ainda é expandido em `m.a, m.b, m.c`, mas agora essas variáveis são apenas referências para o resultado do item `FROM`. (A palavra-chave `LATERAL` é opcional aqui, mas mostramos isso para esclarecer que a função está obtendo `x` de `some_table`.)

A sintaxe *`composite_value`*`.*` resulta na expansão de coluna desse tipo quando aparece no nível superior de uma lista de saída [(queries-select-lists.md "7.3. Select Lists") [`SELECT`], uma lista [(dml-returning.md "6.4. Returning Data from Modified Rows") [`RETURNING`], uma cláusula [`INSERT`/`UPDATE`/`DELETE`/`MERGE` [`VALUES`], ou um [construtor de linha](sql-expressions.md#SQL-SYNTAX-ROW-CONSTRUCTORS "4.2.13. Row Constructors"). Em todos os outros contextos (incluindo quando aninhados dentro desses construtos), anexar `.*` a um valor composto não altera o valor, pois significa “todas as colunas” e, portanto, o mesmo valor composto é produzido novamente. Por exemplo, se `somefunc()` aceita um argumento com valor composto, essas consultas são as mesmas:

```sql
SELECT somefunc(c.*) FROM inventory_item c;
SELECT somefunc(c) FROM inventory_item c;
```

Em ambos os casos, a linha atual de `inventory_item` é passada para a função como um argumento composto único. Embora `.*` não faça nada nesses casos, usar isso é um bom estilo, pois torna claro que um valor composto é pretendido. Em particular, o analisador considerará `c` em `c.*` para se referir a um nome de tabela ou alias, e não a um nome de coluna, para que não haja ambiguidade; enquanto, sem `.*`, não está claro se `c` significa um nome de tabela ou um nome de coluna, e, de fato, a interpretação de nome de coluna será preferida se houver uma coluna com o nome `c`.

Outro exemplo que demonstra esses conceitos é que todas essas consultas significam a mesma coisa:

```sql
SELECT * FROM inventory_item c ORDER BY c;
SELECT * FROM inventory_item c ORDER BY c.*;
SELECT * FROM inventory_item c ORDER BY ROW(c.*);
```

Todas essas cláusulas `ORDER BY` especificam o valor composto da linha, resultando na ordenação das linhas de acordo com as regras descritas em [Seção 9.25.6](functions-comparisons.md#COMPOSITE-TYPE-COMPARISON). No entanto, se `inventory_item` contrasse uma coluna denominada `c`, o primeiro caso seria diferente dos outros, pois significaria ordenar por essa coluna apenas. Dadas as colunas de nomes mostradas anteriormente, essas consultas também são equivalentes às acima:

```sql
SELECT * FROM inventory_item c ORDER BY ROW(c.name, c.supplier_id, c.price);
SELECT * FROM inventory_item c ORDER BY (c.name, c.supplier_id, c.price);
```

(O último caso utiliza um construtor de linha com a palavra-chave `ROW` omitida.)

Outro comportamento sintático especial associado a valores compostos é que podemos usar *notação funcional* para extrair um campo de um valor composto. A maneira simples de explicar isso é que as notações `field(table)` e `table.field` são intercambiáveis. Por exemplo, essas consultas são equivalentes:

```sql
SELECT c.name FROM inventory_item c WHERE c.price > 1000;
SELECT name(c) FROM inventory_item c WHERE price(c) > 1000;
```

Além disso, se tivermos uma função que aceita um único argumento de um tipo composto, podemos chamá-la com qualquer uma dessas notações. Essas consultas são todas equivalentes:

```sql
SELECT somefunc(c) FROM inventory_item c;
SELECT somefunc(c.*) FROM inventory_item c;
SELECT c.somefunc FROM inventory_item c;
```

Essa equivalência entre a notação funcional e a notação de campo permite que funções sejam aplicadas a tipos compostos para implementar "campos calculados". Uma aplicação que utilize a última consulta acima não precisaria estar diretamente ciente de que `somefunc` não é uma coluna real da tabela.

DICA

Devido a esse comportamento, não é prudente dar a uma função que recebe um argumento de tipo composto o mesmo nome que qualquer um dos campos desse tipo composto. Se houver ambiguidade, a interpretação do nome do campo será escolhida se a sintaxe do nome do campo for usada, enquanto a função será escolhida se a sintaxe da chamada for usada. No entanto, as versões do PostgreSQL anteriores à versão 11 sempre escolheram a interpretação do nome do campo, a menos que a sintaxe da chamada exigisse que fosse uma chamada de função. Uma maneira de forçar a interpretação da função em versões mais antigas é qualificar o nome da função no esquema, ou seja, escrever `schema.func(compositevalue)`.

#### 8.16.6. Sintaxe de entrada e saída de tipo composto [#](#ROWTYPES-IO-SYNTAX)

A representação textual externa de um valor composto consiste em itens que são interpretados de acordo com as regras de conversão de E/S para os tipos de campo individuais, além de uma decoração que indica a estrutura composta. A decoração consiste em parênteses (`(` e `)`) ao redor de todo o valor, além de vírgulas (`,`) entre itens adjacentes. Espaços em branco fora dos parênteses são ignorados, mas dentro dos parênteses são considerados parte do valor do campo, e podem ou não ser significativos, dependendo das regras de conversão de entrada para o tipo de dados do campo. Por exemplo, em:

```sql
'(  42)'
```

os espaços em branco serão ignorados se o tipo de campo for inteiro, mas não se for texto.

Como mostrado anteriormente, ao escrever um valor composto, você pode escrever aspas em torno de qualquer valor de campo individual. Você *deve* fazer isso se o valor do campo de outra forma confundir o analisador de valor composto. Em particular, campos que contêm parênteses, vírgulas, aspas duplas ou barras invertidas devem ser aspas duplas. Para colocar uma aspa ou barra invertida em um valor de campo composto com aspas, anteceda-a com uma barra invertida. (Além disso, um par de aspas duplas dentro de um valor de campo com aspas duplas é considerado para representar um caractere de aspa, analogamente às regras para aspas simples em strings de literal SQL.) Alternativamente, você pode evitar aspas e usar escapagem com barra invertida para proteger todos os caracteres de dados que de outra forma seriam considerados sintaxe composta.

Um valor de campo completamente vazio (sem caracteres entre as vírgulas ou parênteses) representa um NULL. Para escrever um valor que é uma string vazia em vez de NULL, escreva `""`.

A rotina de saída composta colocará aspas duplas ao redor dos valores do campo se eles forem cadeias vazias ou contenham parênteses, vírgulas, aspas duplas, barras invertidas ou espaços em branco. (Fazer isso para espaços em branco não é essencial, mas ajuda na legibilidade.) Aspas duplas e barras invertidas incorporadas nos valores do campo serão duplicadas.

Nota

Lembre-se de que o que você escreve em um comando SQL será interpretado primeiro como um literal de string e, em seguida, como um composto. Isso dobra o número de barras invertidas que você precisa (assumindo que a sintaxe de string de escape é usada). Por exemplo, para inserir um campo `text` contendo uma citação dupla e uma barra invertida em um valor composto, você precisaria escrever:

```sql
INSERT ... VALUES ('("\"\\")');
```

O processador de caracteres de cadeia remove um nível de barras invertidas, de modo que o que chega ao analisador de valores compostos parece `("\"\\")`. Por sua vez, a cadeia de caracteres alimentada na rotina de entrada do tipo de dados `text` se torna `"\`. (Se estivessemos trabalhando com um tipo de dados cuja rotina de entrada também tratasse as barras invertidas de forma especial, `bytea`, por exemplo, precisaríamos de até oito barras invertidas no comando para obter uma barra invertida no campo composto armazenado.) A citação de dólares (ver [Seção 4.1.2.4](sql-syntax-lexical.md#SQL-SYNTAX-DOLLAR-QUOTING)) pode ser usada para evitar a necessidade de duplicar as barras invertidas.

DICA

A sintaxe do construtor `ROW` geralmente é mais fácil de trabalhar do que a sintaxe de literal composto ao escrever valores compostos em comandos SQL. Em `ROW`, os valores individuais dos campos são escritos da mesma maneira que seriam escritos quando não fossem membros de um composto.
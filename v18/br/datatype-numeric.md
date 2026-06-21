## 8.1. Tipos Numéricos [#](#DATATYPE-NUMERIC)

* [8.1.1. Tipos de Inteiros](datatype-numeric.md#DATATYPE-INT)
* [8.1.2. Números de Precisão Arbitrária](datatype-numeric.md#DATATYPE-NUMERIC-DECIMAL)
* [8.1.3. Tipos de Ponto Flutuante](datatype-numeric.md#DATATYPE-FLOAT)
* [8.1.4. Tipos de Série](datatype-numeric.md#DATATYPE-SERIAL)

Os tipos numéricos consistem em inteiros de dois, quatro e oito bytes, números de ponto flutuante de quatro e oito bytes e decimais de precisão selecionável. A tabela [(datatype-numeric.md#DATATYPE-NUMERIC-TABLE "Table 8.2. Numeric Types")](datatype-numeric.md#DATATYPE-NUMERIC-TABLE) lista os tipos disponíveis.

**Tabela 8.2. Tipos numéricos**



<table border="1" class="table" summary="Numeric Types">
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
  <col class="col3"/>
  <col class="col4"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Name
   </th>
   <th>
    Storage Size
   </th>
   <th>
    Description
   </th>
   <th>
    Gama
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="type">
     smallint
    </code>
   </td>
   <td>
    2 bytes
   </td>
   <td>
    small-range integer
   </td>
   <td>
    -32768 a +32767
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     integer
    </code>
   </td>
   <td>
    4 bytes
   </td>
   <td>
    typical choice for integer
   </td>
   <td>
    -2147483648 a +2147483647
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     bigint
    </code>
   </td>
   <td>
    8 bytes
   </td>
   <td>
    large-range integer
   </td>
   <td>
    -9223372036854775808 a +9223372036854775807
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     decimal
    </code>
   </td>
   <td>
    variable
   </td>
   <td>
    user-specified precision, exact
   </td>
   <td>
    até 131072 dígitos antes do ponto decimal; até 16383 dígitos após o ponto decimal
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     numeric
    </code>
   </td>
   <td>
    variable
   </td>
   <td>
    user-specified precision, exact
   </td>
   <td>
    até 131072 dígitos antes do ponto decimal; até 16383 dígitos após o ponto decimal
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     real
    </code>
   </td>
   <td>
    4 bytes
   </td>
   <td>
    variable-precision, inexact
   </td>
   <td>
    Precisão de 6 dígitos decimais
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     double precision
    </code>
   </td>
   <td>
    8 bytes
   </td>
   <td>
    variable-precision, inexact
   </td>
   <td>
    Precisão de 15 dígitos decimais
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     smallserial
    </code>
   </td>
   <td>
    2 bytes
   </td>
   <td>
    small autoincrementing integer
   </td>
   <td>
    1 a 32767
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     serial
    </code>
   </td>
   <td>
    4 bytes
   </td>
   <td>
    autoincrementing integer
   </td>
   <td>
    1 a 2147483647
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     bigserial
    </code>
   </td>
   <td>
    8 bytes
   </td>
   <td>
    large autoincrementing integer
   </td>
   <td>
    1 a 9223372036854775807
   </td>
  </tr>
 </tbody>
</table>









A sintaxe das constantes para os tipos numéricos é descrita em [Seção 4.1.2](sql-syntax-lexical.md#SQL-SYNTAX-CONSTANTS). Os tipos numéricos têm um conjunto completo de operadores e funções aritméticas correspondentes. Consulte [Capítulo 9](functions.md) para mais informações. As seções a seguir descrevem os tipos em detalhes.

### 8.1.1. Tipos de Inteiros [#](#DATATYPE-INT)

Os tipos `smallint`, `integer` e `bigint` armazenam números inteiros, ou seja, números sem componentes fracionários, de vários intervalos. Tentativas de armazenar valores fora do intervalo permitido resultarão em um erro.

O tipo `integer` é a escolha mais comum, pois oferece o melhor equilíbrio entre alcance, tamanho de armazenamento e desempenho. O tipo `smallint` é geralmente usado apenas se o espaço em disco estiver escasso. O tipo `bigint` é projetado para ser usado quando o alcance do tipo `integer` é insuficiente.

O SQL especifica apenas os tipos de número inteiro `integer` (ou `int`), `smallint` e `bigint`. Os nomes dos tipos `int2`, `int4` e `int8` são extensões, que também são usadas por outros sistemas de banco de dados SQL.

### 8.1.2. Números com precisão arbitrária [#](#DATATYPE-NUMERIC-DECIMAL)

O tipo `numeric` pode armazenar números com um número muito grande de dígitos. É especialmente recomendado para armazenar quantias monetárias e outras quantidades onde a exatidão é necessária. Os cálculos com valores de `numeric` produzem resultados exatos quando possível, por exemplo, adição, subtração, multiplicação. No entanto, os cálculos com valores de `numeric` são muito lentos em comparação com os tipos inteiros ou com os tipos de ponto flutuante descritos na próxima seção.

Usamos os termos a seguir abaixo: A *precisão* de um `numeric` é o número total de dígitos significativos no número inteiro, ou seja, o número de dígitos de ambos os lados do ponto decimal. A *escala* de um `numeric` é o número de dígitos decimais na parte fracionária, à direita do ponto decimal. Assim, o número 23,5141 tem uma precisão de 6 e uma escala de 4. Os inteiros podem ser considerados como tendo uma escala de zero.

Tanto a precisão máxima quanto a escala máxima de uma coluna `numeric` podem ser configuradas. Para declarar uma coluna do tipo `numeric`, use a sintaxe:

```
NUMERIC(precision, scale)
```

A precisão deve ser positiva, enquanto a escala pode ser positiva ou negativa (veja abaixo). Alternativamente:

```
NUMERIC(precision)
```

seleciona uma escala de 0. Especificando:

```
NUMERIC
```

sem qualquer precisão ou escala cria uma coluna "numérica não limitada" na qual valores numéricos de qualquer comprimento podem ser armazenados, até os limites de implementação. Uma coluna desse tipo não coagirá os valores de entrada para qualquer escala específica, enquanto as colunas `numeric` com uma escala declarada coagirão os valores de entrada para essa escala. (O padrão SQL exige uma escala padrão de 0, ou seja, coerência para precisão inteira. Acreditamos que isso é um pouco inútil. Se você está preocupado com a portabilidade, especifique sempre a precisão e a escala explicitamente.)

### Nota

A máxima precisão que pode ser explicitamente especificada em uma declaração de tipo `numeric` é de 1000. Uma coluna `numeric` sem restrições está sujeita aos limites descritos na [Tabela 8.2](datatype-numeric.md#DATATYPE-NUMERIC-TABLE).

Se a escala de um valor a ser armazenado for maior que a escala declarada da coluna, o sistema arredondará o valor para o número especificado de dígitos fracionários. Em seguida, se o número de dígitos à esquerda do ponto decimal exceder a precisão declarada menos a escala declarada, um erro é gerado. Por exemplo, uma coluna declarada como

```
NUMERIC(3, 1)
```

os valores serão arredondados para 1 casa decimal e poderão armazenar valores entre -99,9 e 99,9, inclusive.

A partir do PostgreSQL 15, é permitido declarar uma coluna `numeric` com uma escala negativa. Em seguida, os valores serão arredondados à esquerda do ponto decimal. A precisão ainda representa o número máximo de dígitos não arredondados. Assim, uma coluna declarada como

```
NUMERIC(2, -3)
```

irá arredondar os valores para o próximo mil e poderá armazenar valores entre -99000 e 99000, inclusive. Também é permitido declarar uma escala maior que a precisão declarada. Tal coluna só pode conter valores fracionários, e exige que o número de dígitos nulos logo à direita do ponto decimal seja, no mínimo, a escala declarada menos a precisão declarada. Por exemplo, uma coluna declarada como

```
NUMERIC(3, 5)
```

os valores serão arredondados para 5 casas decimais e poderão armazenar valores entre -0,00999 e 0,00999, inclusive.

### Nota

O PostgreSQL permite que a escala em uma declaração de tipo `numeric` seja qualquer valor no intervalo de -1000 a 1000. No entanto, o padrão SQL exige que a escala esteja no intervalo de 0 a *`precision`*. Usar escalas fora desse intervalo pode não ser portátil para outros sistemas de banco de dados.

Os valores numéricos são armazenados fisicamente sem quaisquer zeros adicionais no início ou no fim. Assim, a precisão e a escala declaradas de uma coluna são máximos, não alocações fixas. (Nesse sentido, o tipo `numeric` é mais semelhante ao `varchar(n)` do que ao `char(n)`). O requisito real de armazenamento é de dois bytes para cada grupo de quatro dígitos decimais, mais três a oito bytes de sobrecarga.

Além dos valores numéricos comuns, o tipo `numeric` possui vários valores especiais:

`Infinity` `-Infinity` `NaN`

Esses valores são adaptados do padrão IEEE 754 e representam, respectivamente, “infinitos”, “infinitos negativos” e “não um número”. Ao escrever esses valores como constantes em um comando SQL, você deve colocá-los entre aspas, por exemplo, `UPDATE table SET x = '-Infinity'`. Na entrada, essas strings são reconhecidas de forma insensível ao caso. Os valores de infinitos podem ser escritos como `inf` e `-inf`, como alternativa.

Os valores infinitos se comportam conforme as expectativas matemáticas. Por exemplo, `Infinity` mais qualquer valor finito é igual a `Infinity`, assim como `Infinity` mais `Infinity`; mas `Infinity` menos `Infinity` resulta em `NaN` (não é um número), porque não tem uma interpretação bem definida. Note que um infinito só pode ser armazenado em uma coluna `numeric` sem restrições, porque conceitualmente excede qualquer limite de precisão finito.

O valor `NaN` (não é um número) é usado para representar resultados de cálculo indefinidos. Em geral, qualquer operação com uma entrada `NaN` resulta em outro `NaN`. A única exceção é quando as outras entradas da operação são tais que a mesma saída seria obtida se o `NaN` fosse substituído por qualquer valor numérico finito ou infinito; então, esse valor de saída é usado para `NaN` também. (Um exemplo desse princípio é que `NaN` elevado ao poder zero resulta em um.)

### Nota

Na maioria das implementações do conceito de “não é um número”, `NaN` não é considerado igual a qualquer outro valor numérico (incluindo `NaN`). Para permitir que os valores de `numeric` sejam ordenados e utilizados em índices baseados em árvore, o PostgreSQL trata os valores de `NaN` como iguais e maiores que todos os valores que não são `NaN`.

Os tipos `decimal` e `numeric` são equivalentes. Ambos os tipos fazem parte do padrão SQL.

Ao arredondar valores, o tipo `numeric` arredonda os empates para longe de zero, enquanto (na maioria das máquinas) os tipos `real` e `double precision` arredondam os empates para o número par mais próximo. Por exemplo:

```
SELECT x,
  round(x::numeric) AS num_round,
  round(x::double precision) AS dbl_round
FROM generate_series(-3.5, 3.5, 1) as x;
  x   | num_round | dbl_round
------+-----------+-----------
 -3.5 |        -4 |        -4
 -2.5 |        -3 |        -2
 -1.5 |        -2 |        -2
 -0.5 |        -1 |        -0
  0.5 |         1 |         0
  1.5 |         2 |         2
  2.5 |         3 |         2
  3.5 |         4 |         4
(8 rows)
```

### 8.1.3. Tipos de Ponto Flutuante [#](#DATATYPE-FLOAT)

Os tipos de dados `real` e `double precision` são tipos numéricos de precisão variável inexatos. Em todas as plataformas atualmente suportadas, esses tipos são implementações do Padrão IEEE 754 para Aritmética de Ponto Flutuante Binária (precisão simples e dupla, respectivamente), na medida em que o processador subjacente, o sistema operacional e o compilador o suportem.

Inexact significa que alguns valores não podem ser convertidos exatamente para o formato interno e são armazenados como aproximações, de modo que armazenar e recuperar um valor pode mostrar discrepâncias leves. Gerenciar esses erros e como eles se propagam através dos cálculos é o assunto de um ramo inteiro de matemática e ciência da computação e não será discutido aqui, exceto pelos seguintes pontos:

* Se você precisar de armazenamento e cálculos exatos (como para valores monetários), use o tipo `numeric`.
* Se você quiser fazer cálculos complicados com esses tipos para algo importante, especialmente se você depende de certo comportamento em casos de limite (infinito, subfluxo), você deve avaliar a implementação cuidadosamente.
* Comparar dois valores de ponto flutuante para igualdade nem sempre funciona como esperado.

Em todas as plataformas atualmente suportadas, o tipo `real` tem um intervalo de cerca de 1E-37 a 1E+37 com uma precisão de pelo menos 6 dígitos decimais. O tipo `double precision` tem um intervalo de cerca de 1E-307 a 1E+308 com uma precisão de pelo menos 15 dígitos. Valores que são muito grandes ou muito pequenos causarão um erro. A arredondamento pode ocorrer se a precisão de um número de entrada for muito alta. Números muito próximos de zero que não podem ser representados como distintos de zero causarão um erro de subfluxo.

Por padrão, os valores de ponto flutuante são exibidos em formato de texto na sua representação decimal mais precisa e curta; o valor decimal produzido está mais próximo do verdadeiro valor binário armazenado do que de qualquer outro valor que possa ser representado na mesma precisão binária. (No entanto, o valor de saída atualmente nunca é exatamente no meio entre dois valores representáveis, a fim de evitar um bug generalizado em que as rotinas de entrada não respeitam adequadamente a regra de arredondamento para o número par mais próximo.) Este valor usará, no máximo, 17 dígitos decimais significativos para os valores de `float8` e, no máximo, 9 dígitos para os valores de `float4`.

### Nota

Esse formato de saída mais preciso e mais curto é muito mais rápido de gerar do que o formato arredondado histórico.

Para compatibilidade com a saída gerada por versões mais antigas do PostgreSQL, e para permitir que a precisão da saída seja reduzida, o parâmetro [extra_float_digits](runtime-config-client.md#GUC-EXTRA-FLOAT-DIGITS) pode ser usado para selecionar saída decimal arredondada. Definir um valor de 0 restaura o valor padrão anterior de arredondamento do valor para 6 (para `float4`) ou 15 (para `float8`) dígitos decimais significativos. Definir um valor negativo reduz ainda mais o número de dígitos; por exemplo, -2 arredondaria a saída para 4 ou 13 dígitos, respectivamente.

Qualquer valor de [extra_float_digits][(runtime-config-client.md#GUC-EXTRA-FLOAT-DIGITS) maior que 0 seleciona o formato mais preciso.

### Nota

Aplicações que desejavam valores precisos historicamente tiveram que definir [extra_float_digits](runtime-config-client.md#GUC-EXTRA-FLOAT-DIGITS) para 3 para obtê-los. Para obter a máxima compatibilidade entre as versões, elas devem continuar a fazer isso.

Além dos valores numéricos comuns, os tipos de ponto flutuante têm vários valores especiais:

`Infinity` `-Infinity` `NaN`

Estes representam os valores especiais IEEE 754 “infinitas”, “infinitas negativas” e “não um número”, respectivamente. Ao escrever esses valores como constantes em um comando SQL, você deve colocá-los entre aspas, por exemplo, `UPDATE table SET x = '-Infinity'`. Na entrada, essas strings são reconhecidas de forma insensível ao caso. Os valores infinitos podem ser escritos como `inf` e `-inf`, como alternativa.

### Nota

A IEEE 754 especifica que `NaN` não deve ser comparado a qualquer outro valor de ponto flutuante (incluindo `NaN`). Para permitir que os valores de ponto flutuante sejam ordenados e utilizados em índices baseados em árvores, o PostgreSQL trata os valores de `NaN` como iguais e maiores que todos os valores que não são `NaN`.

O PostgreSQL também suporta as notações padrão do SQL `float` e `float(p)` para especificar tipos numéricos inexatos. Aqui, *`p`* especifica a precisão mínima aceitável em *dígitos binários*. O PostgreSQL aceita `float(1)` a `float(24)` como seleção do tipo `real`, enquanto `float(25)` a `float(53)` selecionam `double precision`. Os valores de *`p`* fora do intervalo permitido geram um erro. `float` sem precisão especificada é interpretado como `double precision`.

### 8.1.4. Tipos de série [#](#DATATYPE-SERIAL)

### Nota

Esta seção descreve uma maneira específica do PostgreSQL para criar uma coluna de autoincremento. Outra maneira é usar a característica da coluna de identidade padrão do SQL, descrita em [Seção 5.3](ddl-identity-columns.md).

Os tipos de dados `smallserial`, `serial` e `bigserial` não são tipos verdadeiros, mas apenas uma conveniência notarial para criar colunas de identificador único (semelhante à propriedade `AUTO_INCREMENT` suportada por alguns outros bancos de dados). Na implementação atual, especificando:

```
CREATE TABLE tablename (
    colname SERIAL
);
```

é equivalente a especificar:

```
CREATE SEQUENCE tablename_colname_seq AS integer;
CREATE TABLE tablename (
    colname integer NOT NULL DEFAULT nextval('tablename_colname_seq')
);
ALTER SEQUENCE tablename_colname_seq OWNED BY tablename.colname;
```

Assim, criamos uma coluna inteira e configuramos para que seus valores padrão sejam atribuídos a partir de um gerador de sequência. Uma restrição `NOT NULL` é aplicada para garantir que um valor nulo não possa ser inserido. (Na maioria dos casos, você também deseja anexar uma restrição `UNIQUE` ou `PRIMARY KEY` para evitar que valores duplicados sejam inseridos acidentalmente, mas isso não é automático.) Por último, a sequência é marcada como “de propriedade” da coluna, para que seja descartada se a coluna ou a tabela forem descartadas.

### Nota

Como `smallserial`, `serial` e `bigserial` são implementados usando sequências, pode haver "lacunas" ou lacunas na sequência de valores que aparece na coluna, mesmo que nunca sejam excluídas linhas. Um valor alocado a partir da sequência ainda é "usado" mesmo que uma linha contendo esse valor nunca seja inserida com sucesso na coluna da tabela. Isso pode acontecer, por exemplo, se a transação de inserção for revertida. Consulte `nextval()` em [Seção 9.17](functions-sequence.md) para obter detalhes.

Para inserir o próximo valor da sequência na coluna `serial`, especifique que a coluna `serial` deve receber seu valor padrão. Isso pode ser feito excluindo a coluna da lista de colunas na declaração `INSERT`, ou através do uso da palavra-chave `DEFAULT`.

Os nomes de tipo `serial` e `serial4` são equivalentes: ambos criam colunas `integer`. Os nomes de tipo `bigserial` e `serial8` funcionam da mesma maneira, exceto que criam uma coluna `bigint`. `bigserial` deve ser usado se você antecipar o uso de mais de 231 identificadores ao longo da vida útil da tabela. Os nomes de tipo `smallserial` e `serial2` também funcionam da mesma maneira, exceto que criam uma coluna `smallint`.

A sequência criada para uma coluna `serial` é automaticamente descartada quando a coluna proprietária é descartada. Você pode descartar a sequência sem descartar a coluna, mas isso forçará a remoção da expressão padrão da coluna.
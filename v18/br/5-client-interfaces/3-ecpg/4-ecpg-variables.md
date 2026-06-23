## 34.4. Usando variáveis de host [#](#ECPG-VARIABLES)

* [34.4.1. Visão geral](ecpg-variables.md#ECPG-VARIABLES-OVERVIEW)
* [34.4.2. Declarar seções](ecpg-variables.md#ECPG-DECLARE-SECTIONS)
* [34.4.3. Recuperação de resultados de consulta](ecpg-variables.md#ECPG-RETRIEVING)
* [34.4.4. Mapeamento de tipos de dados SQL não primitivos](ecpg-variables.md#ECPG-VARIABLES-TYPE-MAPPING)
* [34.4.5. Tratamento de tipos de dados SQL não primitivos](ecpg-variables.md#ECPG-VARIABLES-NONPRIMITIVE-SQL)
* [34.4.6. Indicadores](ecpg-variables.md#ECPG-INDICATORS)

Na [Seção 34.3] (ecpg-commands.md "34.3. Running SQL Commands") você viu como você pode executar instruções SQL a partir de um programa SQL incorporado. Algumas dessas instruções usavam apenas valores fixos e não forneciam uma maneira de inserir valores fornecidos pelo usuário nas instruções ou fazer com que o programa processasse os valores retornados pela consulta. Esse tipo de instruções não é realmente útil em aplicações reais. Esta seção explica em detalhes como você pode passar dados entre seu programa em C e as instruções SQL incorporadas usando um mecanismo simples chamado *variáveis hospedeira*. Em um programa SQL incorporado, consideramos as instruções SQL como *hóspedes* no código do programa em C, que é a *linguagem hospedeira*. Portanto, as variáveis do programa em C são chamadas de *variáveis hospedeira*.

Outra maneira de trocar valores entre backends do PostgreSQL e aplicações do ECPG é o uso de descritores SQL, descritos em [Seção 34.7](ecpg-descriptors.md).

### 34.4.1. Visão geral [#](#ECPG-VARIABLES-OVERVIEW)

Passar dados entre o programa C e as instruções SQL é particularmente simples no SQL embutido. Em vez de o programa colar os dados na instrução, o que implica várias complicações, como a citação adequada do valor, você pode simplesmente escrever o nome de uma variável C na instrução SQL, precedida por um colon. Por exemplo:

```
EXEC SQL INSERT INTO sometable VALUES (:v1, 'foo', :v2);
```

Essa declaração se refere a duas variáveis C nomeadas `v1` e `v2` e também utiliza uma literal de string SQL regular, para ilustrar que você não está restrito a usar um tipo de dados ou outro.

Esse estilo de inserção de variáveis C em declarações SQL funciona em qualquer lugar onde uma expressão de valor é esperada em uma declaração SQL.

### 34.4.2. Declaração de seções [#](#ECPG-DECLARE-SECTIONS)

Para passar dados do programa para o banco de dados, por exemplo, como parâmetros em uma consulta, ou para passar dados do banco de dados de volta para o programa, as variáveis C que pretendem conter esses dados precisam ser declaradas em seções marcadas especialmente, para que o preprocessador de SQL embutido seja informado sobre elas.

Esta seção começa com:

```
EXEC SQL BEGIN DECLARE SECTION;
```

e termina com:

```
EXEC SQL END DECLARE SECTION;
```

Entre essas linhas, devem haver declarações normais de variáveis C, como:

```
int   x = 4;
char  foo[16], bar[16];
```

Como você pode ver, você pode, opcionalmente, atribuir um valor inicial à variável. O escopo da variável é determinado pela localização de sua seção declarativa dentro do programa. Você também pode declarar variáveis com a seguinte sintaxe, que implicitamente cria uma seção declarativa:

```
EXEC SQL int i = 4;
```

Você pode ter tantas seções de declaração em um programa quanto desejar.

As declarações também são refletidas no arquivo de saída como variáveis C normais, portanto não há necessidade de as declarar novamente. Variáveis que não são destinadas a serem usadas em comandos SQL podem ser declaradas normalmente fora dessas seções especiais.

A definição de uma estrutura ou união também deve ser listada dentro de uma seção `DECLARE`. Caso contrário, o pré-processador não pode lidar com esses tipos, uma vez que não conhece a definição.

### 34.4.3. Recuperação de resultados de consulta [#](#ECPG-RETRIEVING)

Agora você deve ser capaz de passar dados gerados por seu programa em um comando SQL. Mas como você recupera os resultados de uma consulta? Para esse propósito, o SQL embutido fornece variantes especiais dos comandos usuais `SELECT` e `FETCH`. Esses comandos têm uma cláusula especial `INTO` que especifica em quais variáveis do host os valores recuperados devem ser armazenados. `SELECT` é usado para uma consulta que retorna apenas uma única linha, e `FETCH` é usado para uma consulta que retorna várias linhas, usando um cursor.

Aqui está um exemplo:

```
/*
 * assume this table:
 * CREATE TABLE test1 (a int, b varchar(50));
 */

EXEC SQL BEGIN DECLARE SECTION;
int v1;
VARCHAR v2;
EXEC SQL END DECLARE SECTION;

 ...

EXEC SQL SELECT a, b INTO :v1, :v2 FROM test;
```

Assim, a cláusula `INTO` aparece entre a lista de seleção e a cláusula `FROM`. O número de elementos na lista de seleção e a lista após `INTO` (também chamada de lista de alvo) devem ser iguais.

Aqui está um exemplo usando o comando `FETCH`:

```
EXEC SQL BEGIN DECLARE SECTION;
int v1;
VARCHAR v2;
EXEC SQL END DECLARE SECTION;

 ...

EXEC SQL DECLARE foo CURSOR FOR SELECT a, b FROM test;

 ...

do
{
    ...
    EXEC SQL FETCH NEXT FROM foo INTO :v1, :v2;
    ...
} while (...);
```

Aqui a cláusula `INTO` aparece após todas as cláusulas normais.

### 34.4.4. Mapeamento de Tipo [#](#ECPG-VARIABLES-TYPE-MAPPING)

Quando as aplicações ECPG trocam valores entre o servidor PostgreSQL e a aplicação C, como quando obtêm resultados de consulta do servidor ou executam declarações SQL com parâmetros de entrada, os valores precisam ser convertidos entre os tipos de dados do PostgreSQL e os tipos de variáveis da linguagem de destino (tipos de dados da linguagem C, especificamente). Um dos principais pontos da ECPG é que ela cuida disso automaticamente na maioria dos casos.

Nesse sentido, existem dois tipos de dados: Alguns tipos de dados simples do PostgreSQL, como `integer` e `text`, podem ser lidos e escritos diretamente pela aplicação. Outros tipos de dados do PostgreSQL, como `timestamp` e `numeric`, só podem ser acessados por meio de funções especiais da biblioteca; veja [Seção 34.4.4.2](ecpg-variables.md#ECPG-SPECIAL-TYPES).

[Tabela 34.1](ecpg-variables.md#ECPG-DATATYPE-HOSTVARS-TABLE) mostra quais tipos de dados do PostgreSQL correspondem a quais tipos de dados C. Quando você deseja enviar ou receber um valor de um determinado tipo de dados do PostgreSQL, você deve declarar uma variável C do tipo de dados C correspondente na seção declare.

**Tabela 34.1. Mapeamento entre os tipos de dados do PostgreSQL e os tipos de variáveis em C**



<table border="1" class="table" summary="Mapping Between PostgreSQL Data Types and C Variable Types">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    PostgreSQL data type
   </th>
   <th>
    Host variable type
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
    <code class="type">
     short
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     integer
    </code>
   </td>
   <td>
    <code class="type">
     int
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     bigint
    </code>
   </td>
   <td>
    <code class="type">
     long long int
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     decimal
    </code>
   </td>
   <td>
    <code class="type">
     decimal
    </code>
    <a class="footnote" href="#ftn.ECPG-DATATYPE-TABLE-FN">
     <sup class="footnote" id="ECPG-DATATYPE-TABLE-FN">
      [a]
     </sup>
    </a>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     numeric
    </code>
   </td>
   <td>
    <code class="type">
     numeric
    </code>
    <a class="footnoteref" href="ecpg-variables.md#ftn.ECPG-DATATYPE-TABLE-FN">
     <sup class="footnoteref">
      [a]
     </sup>
    </a>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     real
    </code>
   </td>
   <td>
    <code class="type">
     float
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     double precision
    </code>
   </td>
   <td>
    <code class="type">
     double
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     smallserial
    </code>
   </td>
   <td>
    <code class="type">
     short
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     serial
    </code>
   </td>
   <td>
    <code class="type">
     int
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     bigserial
    </code>
   </td>
   <td>
    <code class="type">
     long long int
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     oid
    </code>
   </td>
   <td>
    <code class="type">
     unsigned int
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     character(
     <em class="replaceable">
      <code>
       n
      </code>
     </em>
     )
    </code>
    ,
    <code class="type">
     varchar(
     <em class="replaceable">
      <code>
       n
      </code>
     </em>
     )
    </code>
    ,
    <code class="type">
     text
    </code>
   </td>
   <td>
    <code class="type">
     char[
     <em class="replaceable">
      <code>
       n
      </code>
     </em>
     +1]
    </code>
    ,
    <code class="type">
     VARCHAR[
     <em class="replaceable">
      <code>
       n
      </code>
     </em>
     +1]
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     name
    </code>
   </td>
   <td>
    <code class="type">
     char[NAMEDATALEN]
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     timestamp
    </code>
   </td>
   <td>
    <code class="type">
     timestamp
    </code>
    <a class="footnoteref" href="ecpg-variables.md#ftn.ECPG-DATATYPE-TABLE-FN">
     <sup class="footnoteref">
      [a]
     </sup>
    </a>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     interval
    </code>
   </td>
   <td>
    <code class="type">
     interval
    </code>
    <a class="footnoteref" href="ecpg-variables.md#ftn.ECPG-DATATYPE-TABLE-FN">
     <sup class="footnoteref">
      [a]
     </sup>
    </a>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     date
    </code>
   </td>
   <td>
    <code class="type">
     date
    </code>
    <a class="footnoteref" href="ecpg-variables.md#ftn.ECPG-DATATYPE-TABLE-FN">
     <sup class="footnoteref">
      [a]
     </sup>
    </a>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     boolean
    </code>
   </td>
   <td>
    <code class="type">
     bool
    </code>
    <a class="footnote" href="#ftn.id-1.7.5.10.7.5.2.2.17.2.2">
     <sup class="footnote" id="id-1.7.5.10.7.5.2.2.17.2.2">
      [b]
     </sup>
    </a>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     bytea
    </code>
   </td>
   <td>
    <code class="type">
     char *
    </code>
    ,
    <code class="type">
     bytea[
     <em class="replaceable">
      <code>
       n
      </code>
     </em>
     ]
    </code>
   </td>
  </tr>
 </tbody>
 <tbody class="footnotes">
  <tr>
   <td colspan="2">
    <div class="footnote" id="ftn.ECPG-DATATYPE-TABLE-FN">
     <p>
      <a class="para" href="#ECPG-DATATYPE-TABLE-FN">
       <sup class="para">
        [a]
       </sup>
      </a>
      This type can only be accessed through special library functions; see
      <a class="xref" href="ecpg-variables.md#ECPG-SPECIAL-TYPES" title="34.4.4.2. Accessing Special Data Types">
       Section 34.4.4.2
      </a>
      .
     </p>
    </div>
    <div class="footnote" id="ftn.id-1.7.5.10.7.5.2.2.17.2.2">
     <p>
      <a class="para" href="#id-1.7.5.10.7.5.2.2.17.2.2">
       <sup class="para">
        [b]
       </sup>
      </a>
      declared in
      <code class="filename">
       ecpglib.h
      </code>
      if not native
     </p>
    </div>
   </td>
  </tr>
 </tbody>
</table>










#### 34.4.4.1. Tratamento de cadeias de caracteres [#](#ECPG-CHAR)

Para lidar com tipos de dados de cadeia de caracteres SQL, como `varchar` e `text`, existem duas maneiras possíveis de declarar as variáveis hostis.

Uma maneira é usar `char[]`, um array de `char`, que é a maneira mais comum de lidar com dados de caracteres em C.

```
EXEC SQL BEGIN DECLARE SECTION;
    char str[50];
EXEC SQL END DECLARE SECTION;
```

Observe que você precisa cuidar do comprimento por si mesmo. Se você usar essa variável de host como a variável alvo de uma consulta que retorna uma string com mais de 49 caracteres, ocorre um estouro de buffer.

A outra maneira é usar o tipo `VARCHAR`, que é um tipo especial fornecido pelo ECPG. A definição em um array do tipo `VARCHAR` é convertido em um `struct` nomeado para cada variável. Uma declaração como:

```
VARCHAR var[180];
```

é convertido em:

```
struct varchar_var { int len; char arr[180]; } var;
```

O membro `arr` aloja a cadeia de caracteres, incluindo um byte de término nulo. Assim, para armazenar uma cadeia de caracteres em uma variável de host `VARCHAR`, a variável de host deve ser declarada com o comprimento incluindo o byte de término nulo. O membro `len` contém o comprimento da cadeia de caracteres armazenada no `arr`, sem o byte de término nulo. Quando uma variável de host é usada como entrada para uma consulta, se `strlen(arr)` e `len` forem diferentes, a mais curta é usada.

`VARCHAR` pode ser escrito em maiúsculas ou minúsculas, mas não em maiúsculas e minúsculas mistas.

As variáveis hospedeiras `char` e `VARCHAR` também podem conter valores de outros tipos de SQL, que serão armazenados em suas formas de string.

#### 34.4.4.2. Acesso a tipos de dados especiais [#](#ECPG-SPECIAL-TYPES)

O ECPG contém alguns tipos especiais que ajudam você a interagir facilmente com alguns tipos de dados especiais do servidor PostgreSQL. Em particular, ele implementou suporte para os tipos `numeric`, `decimal`, `date`, `timestamp` e `interval`. Esses tipos de dados não podem ser mapeados de forma útil para tipos de variáveis hostis primitivas (como `int`, `long long int` ou `char[]`), porque eles têm uma estrutura interna complexa. As aplicações lidam com esses tipos ao declarar variáveis hostis em tipos especiais e acessá-los usando funções na biblioteca pgtypes. A biblioteca pgtypes, descrita em detalhes na [Seção 34.6](ecpg-pgtypes.md) contém funções básicas para lidar com esses tipos, de modo que você não precise enviar uma consulta ao servidor SQL apenas para adicionar um intervalo a um rótulo de tempo, por exemplo.

Os subtítulos seguintes descrevem esses tipos de dados especiais. Para mais detalhes sobre as funções da biblioteca pgtypes, consulte [Seção 34.6](ecpg-pgtypes.md).

##### 34.4.4.2.1. data e hora de registro [#](#ECPG-SPECIAL-TYPES-TIMESTAMP-DATE)

Aqui está um padrão para o tratamento das variáveis `timestamp` na aplicação hospedeira do ECPG.

Primeiro, o programa deve incluir o arquivo de cabeçalho para o tipo `timestamp`:

```
#include <pgtypes_timestamp.h>
```

Em seguida, declare uma variável hospedeira como tipo `timestamp` na seção declare:

```
EXEC SQL BEGIN DECLARE SECTION;
timestamp ts;
EXEC SQL END DECLARE SECTION;
```

E, após ler um valor na variável host, processe-o usando as funções da biblioteca pgtypes. No exemplo a seguir, o valor `timestamp` é convertido para formato de texto (ASCII) com a função `PGTYPEStimestamp_to_asc()`:

```
EXEC SQL SELECT now()::timestamp INTO :ts;

printf("ts = %s\n", PGTYPEStimestamp_to_asc(ts));
```

Este exemplo mostrará alguns resultados como o seguinte:

```
ts = 2010-06-27 18:03:56.949343
```

Além disso, o tipo DATE pode ser tratado da mesma maneira. O programa deve incluir `pgtypes_date.h`, declarar uma variável hospedeira como o tipo de data e converter um valor DATE em um formato de texto usando a função `PGTYPESdate_to_asc()`. Para mais detalhes sobre as funções da biblioteca pgtypes, consulte [Seção 34.6](ecpg-pgtypes.md).

##### 34.4.4.2.2. intervalo [#](#ECPG-TYPE-INTERVAL)

O manuseio do tipo `interval` também é semelhante aos tipos `timestamp` e `date`. No entanto, é necessário alocar memória para um valor do tipo `interval`. Em outras palavras, o espaço de memória para a variável deve ser alocado na memória heap, e não na memória de pilha.

Aqui está um exemplo de programa:

```
#include <stdio.h>
#include <stdlib.h>
#include <pgtypes_interval.h>

int
main(void)
{
EXEC SQL BEGIN DECLARE SECTION;
    interval *in;
EXEC SQL END DECLARE SECTION;

    EXEC SQL CONNECT TO testdb;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;

    in = PGTYPESinterval_new();
    EXEC SQL SELECT '1 min'::interval INTO :in;
    printf("interval = %s\n", PGTYPESinterval_to_asc(in));
    PGTYPESinterval_free(in);

    EXEC SQL COMMIT;
    EXEC SQL DISCONNECT ALL;
    return 0;
}
```

##### 34.4.4.2.3. numérico, decimal [#](#ECPG-TYPE-NUMERIC-DECIMAL)

O manuseio dos tipos `numeric` e `decimal` é semelhante ao tipo `interval`: requer a definição de um ponteiro, alocação de algum espaço de memória na pilha e acesso à variável usando as funções da biblioteca pgtypes. Para mais detalhes sobre as funções da biblioteca pgtypes, consulte [Seção 34.6](ecpg-pgtypes.md).

Não são fornecidas funções especificamente para o tipo `decimal`. Uma aplicação deve convertê-lo em uma variável `numeric` usando uma função da biblioteca pgtypes para realizar o processamento adicional.

Aqui está um exemplo de programa que lida com as variáveis do tipo `numeric` e `decimal`.

```
#include <stdio.h>
#include <stdlib.h>
#include <pgtypes_numeric.h>

EXEC SQL WHENEVER SQLERROR STOP;

int
main(void)
{
EXEC SQL BEGIN DECLARE SECTION;
    numeric *num;
    numeric *num2;
    decimal *dec;
EXEC SQL END DECLARE SECTION;

    EXEC SQL CONNECT TO testdb;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;

    num = PGTYPESnumeric_new();
    dec = PGTYPESdecimal_new();

    EXEC SQL SELECT 12.345::numeric(4,2), 23.456::decimal(4,2) INTO :num, :dec;

    printf("numeric = %s\n", PGTYPESnumeric_to_asc(num, 0));
    printf("numeric = %s\n", PGTYPESnumeric_to_asc(num, 1));
    printf("numeric = %s\n", PGTYPESnumeric_to_asc(num, 2));

    /* Convert decimal to numeric to show a decimal value. */
    num2 = PGTYPESnumeric_new();
    PGTYPESnumeric_from_decimal(dec, num2);

    printf("decimal = %s\n", PGTYPESnumeric_to_asc(num2, 0));
    printf("decimal = %s\n", PGTYPESnumeric_to_asc(num2, 1));
    printf("decimal = %s\n", PGTYPESnumeric_to_asc(num2, 2));

    PGTYPESnumeric_free(num2);
    PGTYPESdecimal_free(dec);
    PGTYPESnumeric_free(num);

    EXEC SQL COMMIT;
    EXEC SQL DISCONNECT ALL;
    return 0;
}
```

##### 34.4.4.2.4. bytea [#](#ECPG-SPECIAL-TYPES-BYTEA)

O manuseio do tipo `bytea` é semelhante ao do `VARCHAR`. A definição em um array do tipo `bytea` é convertida em uma estrutura nomeada para cada variável. Uma declaração como:

```
bytea var[180];
```

é convertido em:

```
struct bytea_var { int len; char arr[180]; } var;
```

O membro `arr` hospeda dados em formato binário. Ele também pode lidar com `'\0'` como parte dos dados, ao contrário de `VARCHAR`. Os dados são convertidos de/para formato hexadecimal e enviados/recebidos pelo ecpglib.

### Nota

A variável `bytea` pode ser usada apenas quando [bytea_output](runtime-config-client.md#GUC-BYTEA-OUTPUT) está definido como `hex`.

#### 34.4.4.3. Variáveis de anfitrião com tipos não primitivos [#](#ECPG-VARIABLES-NONPRIMITIVE-C)

Como uma variável hospedeira, você também pode usar arrays, typedef, estruturas e ponteiros.

##### 34.4.4.3.1. Arrays [#](#ECPG-VARIABLES-ARRAYS)

Existem dois casos de uso para arrays como variáveis hostis. O primeiro é uma maneira de armazenar uma string de texto em `char[]` ou `VARCHAR[]`, conforme explicado em [Seção 34.4.4.1](ecpg-variables.md#ECPG-CHAR). O segundo caso de uso é recuperar várias linhas de um resultado de consulta sem usar um cursor. Sem um array, para processar um resultado de consulta composto por várias linhas, é necessário usar um cursor e o comando `FETCH`. Mas com variáveis hostis de array, várias linhas podem ser recebidas de uma só vez. O comprimento do array deve ser definido para poder acomodar todas as linhas, caso contrário, é provável que ocorra um estouro de buffer.

O exemplo a seguir examina a tabela do sistema `pg_database` e mostra todos os OIDs e nomes dos bancos de dados disponíveis:

```
int
main(void)
{
EXEC SQL BEGIN DECLARE SECTION;
    int dbid[8];
    char dbname[8][16];
    int i;
EXEC SQL END DECLARE SECTION;

    memset(dbname, 0, sizeof(char)* 16 * 8);
    memset(dbid, 0, sizeof(int) * 8);

    EXEC SQL CONNECT TO testdb;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;

    /* Retrieve multiple rows into arrays at once. */
    EXEC SQL SELECT oid,datname INTO :dbid, :dbname FROM pg_database;

    for (i = 0; i < 8; i++)
        printf("oid=%d, dbname=%s\n", dbid[i], dbname[i]);

    EXEC SQL COMMIT;
    EXEC SQL DISCONNECT ALL;
    return 0;
}
```

Este exemplo mostra o seguinte resultado. (Os valores exatos dependem das circunstâncias locais.)

```
oid=1, dbname=template1
oid=11510, dbname=template0
oid=11511, dbname=postgres
oid=313780, dbname=testdb
oid=0, dbname=
oid=0, dbname=
oid=0, dbname=
```

##### 34.4.4.3.2. Estruturas [#](#ECPG-VARIABLES-STRUCT)

Uma estrutura cujos nomes de membros correspondem aos nomes das colunas de um resultado de consulta pode ser usada para recuperar várias colunas de uma só vez. A estrutura permite o tratamento de vários valores de coluna em uma única variável hospedeira.

O exemplo a seguir recupera OIDs, nomes e tamanhos dos bancos de dados disponíveis da tabela do sistema `pg_database` e usando a função `pg_database_size()`. Neste exemplo, uma variável de estrutura `dbinfo_t` com membros cujos nomes correspondem a cada coluna no resultado do `SELECT` é usada para recuperar uma linha de resultado sem colocar várias variáveis de host na declaração `FETCH`.

```
EXEC SQL BEGIN DECLARE SECTION;
    typedef struct
    {
       int oid;
       char datname[65];
       long long int size;
    } dbinfo_t;

    dbinfo_t dbval;
EXEC SQL END DECLARE SECTION;

    memset(&dbval, 0, sizeof(dbinfo_t));

    EXEC SQL DECLARE cur1 CURSOR FOR SELECT oid, datname, pg_database_size(oid) AS size FROM pg_database;
    EXEC SQL OPEN cur1;

    /* when end of result set reached, break out of while loop */
    EXEC SQL WHENEVER NOT FOUND DO BREAK;

    while (1)
    {
        /* Fetch multiple columns into one structure. */
        EXEC SQL FETCH FROM cur1 INTO :dbval;

        /* Print members of the structure. */
        printf("oid=%d, datname=%s, size=%lld\n", dbval.oid, dbval.datname, dbval.size);
    }

    EXEC SQL CLOSE cur1;
```

Este exemplo mostra o seguinte resultado. (Os valores exatos dependem das circunstâncias locais.)

```
oid=1, datname=template1, size=4324580
oid=11510, datname=template0, size=4243460
oid=11511, datname=postgres, size=4324580
oid=313780, datname=testdb, size=8183012
```

As variáveis de estrutura "absorvem" tantas colunas quanto o número de campos na estrutura. Colunas adicionais podem ser atribuídas a outras variáveis de estrutura. Por exemplo, o programa acima também pode ser reestruturado da seguinte forma, com a variável `size` fora da estrutura:

```
EXEC SQL BEGIN DECLARE SECTION;
    typedef struct
    {
       int oid;
       char datname[65];
    } dbinfo_t;

    dbinfo_t dbval;
    long long int size;
EXEC SQL END DECLARE SECTION;

    memset(&dbval, 0, sizeof(dbinfo_t));

    EXEC SQL DECLARE cur1 CURSOR FOR SELECT oid, datname, pg_database_size(oid) AS size FROM pg_database;
    EXEC SQL OPEN cur1;

    /* when end of result set reached, break out of while loop */
    EXEC SQL WHENEVER NOT FOUND DO BREAK;

    while (1)
    {
        /* Fetch multiple columns into one structure. */
        EXEC SQL FETCH FROM cur1 INTO :dbval, :size;

        /* Print members of the structure. */
        printf("oid=%d, datname=%s, size=%lld\n", dbval.oid, dbval.datname, size);
    }

    EXEC SQL CLOSE cur1;
```

##### 34.4.4.3.3. Definições de tipos [#](#ECPG-VARIABLES-NONPRIMITIVE-C-TYPEDEFS)

Use a palavra-chave `typedef` para mapear novos tipos a tipos já existentes.

```
EXEC SQL BEGIN DECLARE SECTION;
    typedef char mychartype[40];
    typedef long serial_t;
EXEC SQL END DECLARE SECTION;
```

Observe que você também pode usar:

```
EXEC SQL TYPE serial_t IS long;
```

Essa declaração não precisa fazer parte de uma seção de declaração; ou seja, você também pode escrever typedefs como declarações normais de C.

Qualquer palavra que você declare como `typedef` não pode ser usada como uma palavra-chave SQL nos comandos `EXEC SQL` mais tarde no mesmo programa. Por exemplo, isso não funcionará:

```
EXEC SQL BEGIN DECLARE SECTION;
    typedef int start;
EXEC SQL END DECLARE SECTION;
...
EXEC SQL START TRANSACTION;
```

A ECPG reportará um erro de sintaxe para `START TRANSACTION`, porque ele não reconhece mais `START` como uma palavra-chave SQL, apenas como um typedef. (Se você tiver um conflito como esse e o typedef parecer impraticável, você pode escrever o comando SQL usando [SQL dinâmico](ecpg-dynamic.md).).

### Nota

Em versões do PostgreSQL anteriores à v16, o uso de palavras-chave SQL como nomes de typedef provavelmente resultaria em erros de sintaxe associados ao uso do próprio typedef, e não ao uso do nome como uma palavra-chave SQL. O novo comportamento é menos propenso a causar problemas quando uma aplicação existente do ECPG é recompilando em uma nova versão do PostgreSQL com novas palavras-chave.

##### 34.4.4.3.4. Pontos [#](#ECPG-VARIABLES-NONPRIMITIVE-C-POINTERS)

Você pode declarar ponteiros para os tipos mais comuns. No entanto, não pode usar ponteiros como variáveis-alvo de consultas sem auto-alocação. Consulte [Seção 34.7](ecpg-descriptors.md) para obter mais informações sobre auto-alocação.

```
EXEC SQL BEGIN DECLARE SECTION;
    int   *intp;
    char **charp;
EXEC SQL END DECLARE SECTION;
```

### 34.4.5. Gerenciamento de tipos de dados SQL não primitivos [#](#ECPG-VARIABLES-NONPRIMITIVE-SQL)

Esta seção contém informações sobre como lidar com tipos de dados não escalares e definidos pelo usuário em aplicativos ECPG. Observe que isso é distinto do tratamento de variáveis hostis de tipos não primitivos, descrito na seção anterior.

#### 34.4.5.1. Arrays [#](#ECPG-VARIABLES-NONPRIMITIVE-SQL-ARRAYS)

Os arrays multidimensionais em nível de SQL não são diretamente suportados no ECPG. Arrays unidimensionais em nível de SQL podem ser mapeados em variáveis hostis de matriz C e vice-versa. No entanto, ao criar uma declaração, o ecpg não conhece os tipos das colunas, de modo que não pode verificar se uma matriz C é inserida em um array correspondente em nível de SQL. Ao processar a saída de uma declaração SQL, o ecpg tem as informações necessárias e, portanto, verifica se ambos são arrays.

Se uma consulta acessar *elementos* de um array separadamente, isso evita o uso de arrays no ECPG. Em seguida, deve-se usar uma variável hospedeira com um tipo que possa ser mapeado para o tipo de elemento. Por exemplo, se um tipo de coluna é um array de `integer`, pode-se usar uma variável hospedeira do tipo `int`. Além disso, se o tipo de elemento for `varchar` ou `text`, pode-se usar uma variável hospedeira do tipo `char[]` ou `VARCHAR[]`.

Aqui está um exemplo. Suponha que a tabela a seguir:

```
CREATE TABLE t3 (
    ii integer[]
);

testdb=> SELECT * FROM t3;
     ii
-------------
 {1,2,3,4,5}
(1 row)
```

O programa a seguir recupera o 4º elemento da matriz e o armazena em uma variável hospedeira do tipo `int`:

```
EXEC SQL BEGIN DECLARE SECTION;
int ii;
EXEC SQL END DECLARE SECTION;

EXEC SQL DECLARE cur1 CURSOR FOR SELECT ii[4] FROM t3;
EXEC SQL OPEN cur1;

EXEC SQL WHENEVER NOT FOUND DO BREAK;

while (1)
{
    EXEC SQL FETCH FROM cur1 INTO :ii ;
    printf("ii=%d\n", ii);
}

EXEC SQL CLOSE cur1;
```

Este exemplo mostra o seguinte resultado:

```
ii=4
```

Para mapear vários elementos de uma matriz em variáveis hospedeiras com vários elementos de um tipo de matriz, cada elemento da coluna da matriz e cada elemento da matriz de variáveis hospedeiras deve ser gerenciado separadamente, por exemplo:

```
EXEC SQL BEGIN DECLARE SECTION;
int ii_a[8];
EXEC SQL END DECLARE SECTION;

EXEC SQL DECLARE cur1 CURSOR FOR SELECT ii[1], ii[2], ii[3], ii[4] FROM t3;
EXEC SQL OPEN cur1;

EXEC SQL WHENEVER NOT FOUND DO BREAK;

while (1)
{
    EXEC SQL FETCH FROM cur1 INTO :ii_a[0], :ii_a[1], :ii_a[2], :ii_a[3];
    ...
}
```

Observe novamente que

```
EXEC SQL BEGIN DECLARE SECTION;
int ii_a[8];
EXEC SQL END DECLARE SECTION;

EXEC SQL DECLARE cur1 CURSOR FOR SELECT ii FROM t3;
EXEC SQL OPEN cur1;

EXEC SQL WHENEVER NOT FOUND DO BREAK;

while (1)
{
    /* WRONG */
    EXEC SQL FETCH FROM cur1 INTO :ii_a;
    ...
}
```

não funcionaria corretamente neste caso, porque você não pode mapear uma coluna de tipo de matriz para uma variável hospedeira de matriz diretamente.

Outra solução é armazenar matrizes em sua representação de string externa em variáveis hostis do tipo `char[]` ou `VARCHAR[]`. Para mais detalhes sobre essa representação, consulte [Seção 8.15.2](arrays.md#ARRAYS-INPUT). Observe que isso significa que a matriz não pode ser acessada naturalmente como uma matriz no programa hostis (sem processamento adicional que analise a representação de texto).

#### 34.4.5.2. Tipos compostos [#](#ECPG-VARIABLES-NONPRIMITIVE-SQL-COMPOSITE)

Os tipos compostos não são diretamente suportados no ECPG, mas uma solução fácil é possível. As soluções disponíveis são semelhantes às descritas para arrays acima: ou acesse cada atributo separadamente ou use a representação de string externa.

Para os exemplos a seguir, vamos assumir o seguinte tipo e tabela:

```
CREATE TYPE comp_t AS (intval integer, textval varchar(32));
CREATE TABLE t4 (compval comp_t);
INSERT INTO t4 VALUES ( (256, 'PostgreSQL') );
```

A solução mais óbvia é acessar cada atributo separadamente. O seguinte programa recupera dados da tabela de exemplo, selecionando cada atributo do tipo `comp_t` separadamente:

```
EXEC SQL BEGIN DECLARE SECTION;
int intval;
varchar textval[33];
EXEC SQL END DECLARE SECTION;

/* Put each element of the composite type column in the SELECT list. */
EXEC SQL DECLARE cur1 CURSOR FOR SELECT (compval).intval, (compval).textval FROM t4;
EXEC SQL OPEN cur1;

EXEC SQL WHENEVER NOT FOUND DO BREAK;

while (1)
{
    /* Fetch each element of the composite type column into host variables. */
    EXEC SQL FETCH FROM cur1 INTO :intval, :textval;

    printf("intval=%d, textval=%s\n", intval, textval.arr);
}

EXEC SQL CLOSE cur1;
```

Para melhorar este exemplo, as variáveis de host para armazenar valores no comando `FETCH` podem ser reunidas em uma estrutura. Para mais detalhes sobre a variável de host na forma de estrutura, consulte [Seção 34.4.4.3.2](ecpg-variables.md#ECPG-VARIABLES-STRUCT). Para alternar para a estrutura, o exemplo pode ser modificado conforme a seguir. As duas variáveis de host, `intval` e `textval`, tornam-se membros da estrutura `comp_t`, e a estrutura é especificada no comando `FETCH`.

```
EXEC SQL BEGIN DECLARE SECTION;
typedef struct
{
    int intval;
    varchar textval[33];
} comp_t;

comp_t compval;
EXEC SQL END DECLARE SECTION;

/* Put each element of the composite type column in the SELECT list. */
EXEC SQL DECLARE cur1 CURSOR FOR SELECT (compval).intval, (compval).textval FROM t4;
EXEC SQL OPEN cur1;

EXEC SQL WHENEVER NOT FOUND DO BREAK;

while (1)
{
    /* Put all values in the SELECT list into one structure. */
    EXEC SQL FETCH FROM cur1 INTO :compval;

    printf("intval=%d, textval=%s\n", compval.intval, compval.textval.arr);
}

EXEC SQL CLOSE cur1;
```

Embora uma estrutura seja usada no comando `FETCH`, os nomes dos atributos na cláusula `SELECT` são especificados um por um. Isso pode ser aprimorado usando um `*` para solicitar todos os atributos do valor do tipo composto.

```
...
EXEC SQL DECLARE cur1 CURSOR FOR SELECT (compval).* FROM t4;
EXEC SQL OPEN cur1;

EXEC SQL WHENEVER NOT FOUND DO BREAK;

while (1)
{
    /* Put all values in the SELECT list into one structure. */
    EXEC SQL FETCH FROM cur1 INTO :compval;

    printf("intval=%d, textval=%s\n", compval.intval, compval.textval.arr);
}
...
```

Dessa forma, os tipos compostos podem ser mapeados em estruturas quase sem problemas, mesmo que o ECPG não entenda o próprio tipo composto.

Por fim, também é possível armazenar valores de tipo composto em sua representação de string externa em variáveis hostis do tipo `char[]` ou `VARCHAR[]`. Mas dessa forma, não é facilmente possível acessar os campos do valor do programa hostis.

#### 34.4.5.3. Tipos básicos definidos pelo usuário [#](#ECPG-VARIABLES-NONPRIMITIVE-SQL-USER-DEFINED-BASE-TYPES)

Os novos tipos de base definidos pelo usuário não são diretamente suportados pelo ECPG. Você pode usar a representação de string externa e as variáveis hostis do tipo `char[]` ou `VARCHAR[]`, e essa solução é, de fato, apropriada e suficiente para muitos tipos.

Aqui está um exemplo usando o tipo de dados `complex` do exemplo em [Seção 36.13](xtypes.md "36.13. User-Defined Types"). A representação externa da string desse tipo é `(%f,%f)`, que é definida nas funções `complex_in()` e `complex_out()` em [Seção 36.13](xtypes.md "36.13. User-Defined Types"). O exemplo a seguir insere os valores do tipo complexo `(1,1)` e `(3,3)` nas colunas `a` e `b`, e depois seleciona-os da tabela.

```
EXEC SQL BEGIN DECLARE SECTION;
    varchar a[64];
    varchar b[64];
EXEC SQL END DECLARE SECTION;

    EXEC SQL INSERT INTO test_complex VALUES ('(1,1)', '(3,3)');

    EXEC SQL DECLARE cur1 CURSOR FOR SELECT a, b FROM test_complex;
    EXEC SQL OPEN cur1;

    EXEC SQL WHENEVER NOT FOUND DO BREAK;

    while (1)
    {
        EXEC SQL FETCH FROM cur1 INTO :a, :b;
        printf("a=%s, b=%s\n", a.arr, b.arr);
    }

    EXEC SQL CLOSE cur1;
```

Este exemplo mostra o seguinte resultado:

```
a=(1,1), b=(3,3)
```

Outra solução é evitar o uso direto dos tipos definidos pelo usuário no ECPG e, em vez disso, criar uma função ou uma conversão que converta entre o tipo definido pelo usuário e um tipo primitivo que o ECPG possa manipular. No entanto, é importante notar que as conversões de tipo, especialmente as implícitas, devem ser introduzidas no sistema de tipos com muito cuidado.

Por exemplo,

```
CREATE FUNCTION create_complex(r double, i double) RETURNS complex
LANGUAGE SQL
IMMUTABLE
AS $$ SELECT $1 * complex '(1,0')' + $2 * complex '(0,1)' $$;
```

Após essa definição, o que se segue

```
EXEC SQL BEGIN DECLARE SECTION;
double a, b, c, d;
EXEC SQL END DECLARE SECTION;

a = 1;
b = 2;
c = 3;
d = 4;

EXEC SQL INSERT INTO test_complex VALUES (create_complex(:a, :b), create_complex(:c, :d));
```

tem o mesmo efeito que

```
EXEC SQL INSERT INTO test_complex VALUES ('(1,2)', '(3,4)');
```

### 34.4.6. Indicadores [#](#ECPG-INDICATORS)

Os exemplos acima não lidam com valores nulos. Na verdade, os exemplos de recuperação irão gerar um erro se eles recuperarem um valor nulo do banco de dados. Para poder passar valores nulos para o banco de dados ou recuperar valores nulos do banco de dados, é necessário adicionar uma segunda especificação de variável de host a cada variável de host que contém dados. Essa segunda variável de host é chamada de *indicador* e contém uma bandeira que indica se o dado é nulo, no caso, o valor da variável de host real é ignorado. Aqui está um exemplo que lida corretamente com a recuperação de valores nulos:

```
EXEC SQL BEGIN DECLARE SECTION;
VARCHAR val;
int val_ind;
EXEC SQL END DECLARE SECTION:

 ...

EXEC SQL SELECT b INTO :val :val_ind FROM test1;
```

A variável de indicador `val_ind` será zero se o valor não for nulo, e será negativa se o valor for nulo. (Consulte [Seção 34.16] para habilitar o comportamento específico da Oracle.)

O indicador tem outra função: se o valor do indicador for positivo, isso significa que o valor não é nulo, mas foi truncado quando foi armazenado na variável hospedeira.

Se o argumento `-r no_indicator` for passado ao pré-processador `ecpg`, ele funciona no modo “sem indicador”. No modo sem indicador, se nenhuma variável de indicador for especificada, valores nulos são sinalizados (na entrada e na saída) para tipos de cadeia de caracteres como string vazia e para tipos inteiros como o valor mínimo possível para o tipo (por exemplo, `INT_MIN` para `int`).
## 34.7. Uso de Áreas de Descrição [#](#ECPG-DESCRIPTORS)

* [34.7.1. Áreas de Descrição SQL](ecpg-descriptors.md#ECPG-NAMED-DESCRIPTORS)
* [34.7.2. Áreas de Descrição SQLDA](ecpg-descriptors.md#ECPG-SQLDA-DESCRIPTORS)

Uma área de descritor SQL é um método mais sofisticado para processar o resultado de uma declaração `SELECT`, `FETCH` ou `DESCRIBE`. Uma área de descritor SQL agrupa os dados de uma linha de dados junto com itens de metadados em uma estrutura de dados. Os metadados são particularmente úteis ao executar declarações SQL dinâmicas, onde a natureza das colunas de resultado pode não ser conhecida antecipadamente. O PostgreSQL oferece duas maneiras de usar Áreas de Descritor: as Áreas de Descritor SQL nomeadas e as SQLDAs de estrutura C.

### 34.7.1. Áreas de descriptografia SQL com nome [#](#ECPG-NAMED-DESCRIPTORS)

Uma área de descriptografia SQL com nome consiste em um cabeçalho, que contém informações sobre todo o descriptograma, e uma ou mais áreas de descriptografia de itens, que, basicamente, descrevem cada uma uma coluna na linha de resultado.

Antes de poder usar uma área de descriptografia SQL, você precisa alocar uma:

```
EXEC SQL ALLOCATE DESCRIPTOR identifier;
```

O identificador serve como o "nome de variável" da área de descriptografia. Quando você não precisa mais do descriptografado, você deve liberar o espaço ocupado por ele:

```
EXEC SQL DEALLOCATE DESCRIPTOR identifier;
```

Para usar uma área de descriptografia, especifique-a como alvo de armazenamento em uma cláusula `INTO`, em vez de listar variáveis de host:

```
EXEC SQL FETCH NEXT FROM mycursor INTO SQL DESCRIPTOR mydesc;
```

Se o conjunto de resultados estiver vazio, a Área de Descrição ainda conterá os metadados da consulta, ou seja, os nomes dos campos.

Para consultas preparadas que ainda não foram executadas, a declaração `DESCRIBE` pode ser usada para obter os metadados do conjunto de resultados:

```
EXEC SQL BEGIN DECLARE SECTION;
char *sql_stmt = "SELECT * FROM table1";
EXEC SQL END DECLARE SECTION;

EXEC SQL PREPARE stmt1 FROM :sql_stmt;
EXEC SQL DESCRIBE stmt1 INTO SQL DESCRIPTOR mydesc;
```

Antes do PostgreSQL 9.0, a palavra-chave `SQL` era opcional, então o uso de `DESCRIPTOR` e `SQL DESCRIPTOR` produzia Áreas de Descritor SQL com nome. Agora, é obrigatório, omitindo a palavra-chave `SQL` produz Áreas de Descritor SQLDA, veja [Seção 34.7.2](ecpg-descriptors.md#ECPG-SQLDA-DESCRIPTORS).

Nas declarações `DESCRIBE` e `FETCH`, as palavras-chave `INTO` e `USING` podem ser usadas de maneira semelhante: elas produzem o conjunto de resultados e os metadados em uma Área de Descrição.

Agora, como você obtém os dados da área do descritor? Você pode pensar na área do descritor como uma estrutura com campos nomeados. Para recuperar o valor de um campo do cabeçalho e armazená-lo em uma variável do host, use o seguinte comando:

```
EXEC SQL GET DESCRIPTOR name :hostvar = field;
```

Atualmente, há apenas um campo de cabeçalho definido: *`COUNT`*, que indica quantas áreas de descritor de item existem (ou seja, quantas colunas estão contidas no resultado). A variável host precisa ser do tipo inteiro. Para obter um campo da área de descritor de item, use o seguinte comando:

```
EXEC SQL GET DESCRIPTOR name VALUE num :hostvar = field;
```

*`num`* pode ser um inteiro literal ou uma variável de host que contém um inteiro. Os campos possíveis são:

`CARDINALITY` (número inteiro) [#](#ECPG-NAMED-DESCRIPTORS-CARDINALITY): número de linhas no conjunto de resultados

`DATA` [#](#ECPG-NAMED-DESCRIPTORS-DATA): item de dados atual (portanto, o tipo de dados deste campo depende da consulta)

`DATETIME_INTERVAL_CODE` (número inteiro) [#](#ECPG-NAMED-DESCRIPTORS-DATETIME-INTERVAL-CODE): Quando `TYPE` é `9`, `DATETIME_INTERVAL_CODE` terá um valor de `1` para `DATE`, `2` para `TIME`, `3` para `TIMESTAMP`, `4` para `TIME WITH TIME ZONE`, ou `5` para `TIMESTAMP WITH TIME ZONE`.

`DATETIME_INTERVAL_PRECISION` (número inteiro) [#](#ECPG-NAMED-DESCRIPTORS-DATETIME-INTERVAL-PRECISION): não implementado

`INDICATOR` (número inteiro) [#](#ECPG-NAMED-DESCRIPTORS-INDICATOR): o indicador (indicando um valor nulo ou um corte de valor)

`KEY_MEMBER` (número inteiro) [#](#ECPG-NAMED-DESCRIPTORS-KEY-MEMBER): não implementado

`LENGTH` (número inteiro) [#](#ECPG-NAMED-DESCRIPTORS-LENGTH): comprimento do dado em caracteres

`NAME` (string) [#](#ECPG-NAMED-DESCRIPTORS-NAME): nome da coluna

`NULLABLE` (número inteiro) [#](#ECPG-NAMED-DESCRIPTORS-NULLABLE): não implementado

`OCTET_LENGTH` (número inteiro) [#](#ECPG-NAMED-DESCRIPTORS-OCTET-LENGTH): comprimento da representação de caracteres do dado em bytes

`PRECISION` (número inteiro) [#](#ECPG-NAMED-DESCRIPTORS-PRECISION): precisão (para o tipo `numeric`)

`RETURNED_LENGTH` (número inteiro) [#](#ECPG-NAMED-DESCRIPTORS-RETURNED-LENGTH): comprimento do dado em caracteres

`RETURNED_OCTET_LENGTH` (número inteiro) [#](#ECPG-NAMED-DESCRIPTORS-RETURNED-OCTET-LENGTH): comprimento da representação de caracteres do dado em bytes

`SCALE` (número inteiro) [#](#ECPG-NAMED-DESCRIPTORS-SCALE): escala (para o tipo `numeric`)

`TYPE` (número inteiro) [#](#ECPG-NAMED-DESCRIPTORS-TYPE): código numérico do tipo de dados da coluna

Nas declarações `EXECUTE`, `DECLARE` e `OPEN`, o efeito das palavras-chave `INTO` e `USING` é diferente. Uma Área de Descrição pode também ser construída manualmente para fornecer os parâmetros de entrada para uma consulta ou um cursor e `USING SQL DESCRIPTOR name` é a maneira de passar os parâmetros de entrada em uma consulta parametrizada. A declaração para construir uma Área de Descrição SQL nomeada está abaixo:

```
EXEC SQL SET DESCRIPTOR name VALUE num field = :hostvar;
```

O PostgreSQL suporta a recuperação de mais de um registro em uma declaração `FETCH` e o armazenamento dos dados em variáveis hostis. Nesse caso, assume-se que a variável é um array. Exemplo:

```
EXEC SQL BEGIN DECLARE SECTION;
int id[5];
EXEC SQL END DECLARE SECTION;

EXEC SQL FETCH 5 FROM mycursor INTO SQL DESCRIPTOR mydesc;

EXEC SQL GET DESCRIPTOR mydesc VALUE 1 :id = DATA;
```

### 34.7.2. Áreas de descriptografia SQLDA [#](#ECPG-SQLDA-DESCRIPTORS)

Uma Área de Descritor SQLDA é uma estrutura em linguagem C que também pode ser usada para obter o conjunto de resultados e os metadados de uma consulta. Uma estrutura armazena um registro do conjunto de resultados.

```
EXEC SQL include sqlda.h;
sqlda_t         *mysqlda;

EXEC SQL FETCH 3 FROM mycursor INTO DESCRIPTOR mysqlda;
```

Observe que a palavra-chave `SQL` é omitida. Os parágrafos sobre os casos de uso das palavras-chave `INTO` e `USING` na [Seção 34.7.1](ecpg-descriptors.md#ECPG-NAMED-DESCRIPTORS "34.7.1. Named SQL Descriptor Areas") também se aplicam aqui com uma adição. Em uma declaração `DESCRIBE`, a palavra-chave `DESCRIPTOR` pode ser completamente omitida se a palavra-chave `INTO` for usada:

```
EXEC SQL DESCRIBE prepared_statement INTO mysqlda;
```

O fluxo geral de um programa que utiliza SQLDA é:

1. Prepare uma consulta e declare um cursor para ela.
2. Declare um SQLDA para as linhas de resultado.
3. Declare um SQLDA para os parâmetros de entrada e inicialize-os (alocação de memória, configurações de parâmetro).
4. Abra um cursor com o SQLDA de entrada.
5. Pegue as linhas do cursor e armazene-as em um SQLDA de saída.
6. Leia os valores do SQLDA de saída nas variáveis hostis (com conversão, se necessário).
7. Feche o cursor.
8. Liberte a área de memória alocada para o SQLDA de entrada.

#### 34.7.2.1. Estrutura de dados SQLDA [#](#ECPG-SQLDA-DESCRIPTORS-SQLDA)

O SQLDA utiliza três tipos de estruturas de dados: `sqlda_t`, `sqlvar_t` e `struct sqlname`.

DICA

O SQLDA do PostgreSQL tem uma estrutura de dados semelhante à do IBM DB2 Universal Database, então algumas informações técnicas sobre o SQLDA do DB2 podem ajudar a entender melhor o do PostgreSQL.

##### 34.7.2.1.1. Estrutura sqlda_t [#](#ECPG-SQLDA-SQLDA)

O tipo de estrutura `sqlda_t` é o tipo do SQLDA real. Ele contém um registro. E duas ou mais estruturas `sqlda_t` podem ser conectadas em uma lista vinculada com o ponteiro no campo `desc_next`, representando assim uma coleção ordenada de linhas. Portanto, quando duas ou mais linhas são obtidas, o aplicativo pode lê-las seguindo o ponteiro `desc_next` em cada nó `sqlda_t`.

A definição de `sqlda_t` é:

```
struct sqlda_struct
{
    char            sqldaid[8];
    long            sqldabc;
    short           sqln;
    short           sqld;
    struct sqlda_struct *desc_next;
    struct sqlvar_struct sqlvar[1];
};

typedef struct sqlda_struct sqlda_t;
```

O significado dos campos é:

`sqldaid` [#](#ECPG-SQLDA-SQLDA-SQLDAID): Contém a string literal `"SQLDA "`.

`sqldabc` [#](#ECPG-SQLDA-SQLDA-SQLDABC): Contém o tamanho do espaço alocado em bytes.

`sqln` [#](#ECPG-SQLDA-SQLDA-SQLN): Contém o número de parâmetros de entrada para uma consulta parametrizada, caso seja passada nas declarações `OPEN`, `DECLARE` ou `EXECUTE` usando a palavra-chave `USING`. No caso de ser usada como saída das declarações `SELECT`, `EXECUTE` ou `FETCH`, seu valor é o mesmo da declaração `sqld`

`sqld` [#](#ECPG-SQLDA-SQLDA-SQLD): Contém o número de campos em um conjunto de resultados.

`desc_next` [#](#ECPG-SQLDA-SQLDA-DESC-NEXT): Se a consulta retornar mais de um registro, são retornadas várias estruturas de SQLDA vinculadas, e `desc_next` contém um ponteiro para a próxima entrada na lista.

`sqlvar` [#](#ECPG-SQLDA-SQLDA-SQLVAR): Esta é a matriz das colunas no conjunto de resultados.

##### 34.7.2.1.2. Estrutura sqlvar_t [#](#ECPG-SQLDA-SQLVAR)

O tipo de estrutura `sqlvar_t` contém um valor de coluna e metadados, como tipo e comprimento. A definição do tipo é:

```
struct sqlvar_struct
{
    short          sqltype;
    short          sqllen;
    char          *sqldata;
    short         *sqlind;
    struct sqlname sqlname;
};

typedef struct sqlvar_struct sqlvar_t;
```

O significado dos campos é:

`sqltype` [#](#ECPG-SQLDA-SQLVAR-SQLTYPE): Contém o identificador do tipo do campo. Para valores, consulte `enum ECPGttype` em `ecpgtype.h`.

`sqllen` [#](#ECPG-SQLDA-SQLVAR-SQLLEN): Contém o comprimento binário do campo. Exemplo: 4 bytes para `ECPGt_int`.

`sqldata` [#](#ECPG-SQLDA-SQLVAR-SQLDATA): Indica os dados. O formato dos dados é descrito em [Seção 34.4.4](ecpg-variables.md#ECPG-VARIABLES-TYPE-MAPPING "34.4.4. Type Mapping").

`sqlind` [#](#ECPG-SQLDA-SQLVAR-SQLIND): Indica o indicador nulo. 0 significa não nulo, -1 significa nulo.

`sqlname` [#](#ECPG-SQLDA-SQLVAR-SQLNAME): O nome do campo.

##### 34.7.2.1.3. estrutura sqlname Estrutura [#](#ECPG-SQLDA-SQLNAME)

Uma estrutura `struct sqlname` contém o nome de uma coluna. É usada como membro da estrutura `sqlvar_t`. A definição da estrutura é:

```
#define NAMEDATALEN 64

struct sqlname
{
        short           length;
        char            data[NAMEDATALEN];
};
```

O significado dos campos é:

`length` [#](#ECPG-SQLDA-SQLNAME-LENGTH): Contém o comprimento do nome do campo.

`data` [#](#ECPG-SQLDA-SQLNAME-DATA): Contém o nome do campo real.

#### 34.7.2.2. Recuperação de um Conjunto de Resultados Usando um SQLDA [#](#ECPG-SQLDA-OUTPUT)

Os passos gerais para recuperar um conjunto de resultados de consulta através de um SQLDA são:

1. Declare uma estrutura `sqlda_t` para receber o conjunto de resultados.
2. Execute os comandos `FETCH`/`EXECUTE`/`DESCRIBE` para processar uma consulta especificando o SQLDA declarado.
3. Verifique o número de registros no conjunto de resultados olhando para `sqln`, um membro da estrutura `sqlda_t`.
4. Obtenha os valores de cada coluna de `sqlvar[0]`, `sqlvar[1]`, etc., membros da estrutura `sqlda_t`.
5. Vá para a próxima linha (estrutura `sqlda_t`) seguindo o ponteiro `desc_next`, um membro da estrutura `sqlda_t`.
6. Repita o acima conforme necessário.

Aqui está um exemplo de como recuperar um conjunto de resultados através de um SQLDA.

Primeiro, declare uma estrutura `sqlda_t` para receber o conjunto de resultados.

```
sqlda_t *sqlda1;
```

Em seguida, especifique o SQLDA em um comando. Este é um exemplo de comando `FETCH`.

```
EXEC SQL FETCH NEXT FROM cur1 INTO DESCRIPTOR sqlda1;
```

Execute um loop seguindo a lista vinculada para recuperar as linhas.

```
sqlda_t *cur_sqlda;

for (cur_sqlda = sqlda1;
     cur_sqlda != NULL;
     cur_sqlda = cur_sqlda->desc_next)
{
    ...
}
```

Dentro do loop, execute outro loop para recuperar cada dado da coluna (estrutura `sqlvar_t`) da linha.

```
for (i = 0; i < cur_sqlda->sqld; i++)
{
    sqlvar_t v = cur_sqlda->sqlvar[i];
    char *sqldata = v.sqldata;
    short sqllen  = v.sqllen;
    ...
}
```

Para obter o valor de uma coluna, verifique o valor `sqltype`, um membro da estrutura `sqlvar_t`. Em seguida, mude para uma maneira apropriada, dependendo do tipo de coluna, para copiar dados do campo `sqlvar` para uma variável hospedeira.

```
char var_buf[1024];

switch (v.sqltype)
{
    case ECPGt_char:
        memset(&var_buf, 0, sizeof(var_buf));
        memcpy(&var_buf, sqldata, (sizeof(var_buf) <= sqllen ? sizeof(var_buf) - 1 : sqllen));
        break;

    case ECPGt_int: /* integer */
        memcpy(&intval, sqldata, sqllen);
        snprintf(var_buf, sizeof(var_buf), "%d", intval);
        break;

    ...
}
```

#### 34.7.2.3. Passagem de parâmetros de consulta usando um SQLDA [#](#ECPG-SQLDA-INPUT)

Os passos gerais para usar um SQLDA para passar parâmetros de entrada para uma consulta preparada são:

1. Crie uma consulta preparada (declaração preparada)
2. Declare uma estrutura sqlda_t como um SQLDA de entrada.
3. Aloque uma área de memória (como estrutura sqlda_t) para o SQLDA de entrada.
4. Defina (copie) os valores de entrada na memória alocada.
5. Abra um cursor, especificando o SQLDA de entrada.

Aqui está um exemplo.

Primeiro, crie uma declaração preparada.

```
EXEC SQL BEGIN DECLARE SECTION;
char query[1024] = "SELECT d.oid, * FROM pg_database d, pg_stat_database s WHERE d.oid = s.datid AND (d.datname = ? OR d.oid = ?)";
EXEC SQL END DECLARE SECTION;

EXEC SQL PREPARE stmt1 FROM :query;
```

Em seguida, aloque memória para um SQLDA e defina o número de parâmetros de entrada em `sqln`, uma variável membro da estrutura `sqlda_t`. Quando são necessários dois ou mais parâmetros de entrada para a consulta preparada, o aplicativo deve alocar espaço de memória adicional, que é calculado por (número de parâmetros - 1) * sizeof(sqlvar_t). O exemplo mostrado aqui aloca espaço de memória para dois parâmetros de entrada.

```
sqlda_t *sqlda2;

sqlda2 = (sqlda_t *) malloc(sizeof(sqlda_t) + sizeof(sqlvar_t));
memset(sqlda2, 0, sizeof(sqlda_t) + sizeof(sqlvar_t));

sqlda2->sqln = 2; /* number of input variables */
```

Após a alocação de memória, armazene os valores dos parâmetros na matriz `sqlvar[]`. (Esta é a mesma matriz usada para recuperar os valores das colunas quando o SQLDA está recebendo um conjunto de resultados.) Neste exemplo, os parâmetros de entrada são `"postgres"`, com um tipo de string, e `1`, com um tipo inteiro.

```
sqlda2->sqlvar[0].sqltype = ECPGt_char;
sqlda2->sqlvar[0].sqldata = "postgres";
sqlda2->sqlvar[0].sqllen  = 8;

int intval = 1;
sqlda2->sqlvar[1].sqltype = ECPGt_int;
sqlda2->sqlvar[1].sqldata = (char *) &intval;
sqlda2->sqlvar[1].sqllen  = sizeof(intval);
```

Ao abrir um cursor e especificar o SQLDA que foi configurado previamente, os parâmetros de entrada são passados para a declaração preparada.

```
EXEC SQL OPEN cur1 USING DESCRIPTOR sqlda2;
```

Por fim, após usar os SQLDAs de entrada, o espaço de memória alocado deve ser liberado explicitamente, ao contrário dos SQLDAs usados para receber resultados de consulta.

```
free(sqlda2);
```

#### 34.7.2.4. Um aplicativo de amostra usando SQLDA [#](#ECPG-SQLDA-EXAMPLE)

Aqui está um exemplo de programa, que descreve como obter estatísticas de acesso dos bancos de dados, especificados pelos parâmetros de entrada, dos catálogos do sistema.

Este aplicativo une duas tabelas do sistema, pg_database e pg_stat_database, no OID do banco de dados, e também recupera e exibe as estatísticas do banco de dados que são obtidas por dois parâmetros de entrada (um banco de dados `postgres` e OID `1`).

Primeiro, declare um SQLDA para entrada e um SQLDA para saída.

```
EXEC SQL include sqlda.h;

sqlda_t *sqlda1; /* an output descriptor */
sqlda_t *sqlda2; /* an input descriptor  */
```

Em seguida, conecte-se ao banco de dados, prepare uma declaração e declare um cursor para a declaração preparada.

```
int
main(void)
{
    EXEC SQL BEGIN DECLARE SECTION;
    char query[1024] = "SELECT d.oid,* FROM pg_database d, pg_stat_database s WHERE d.oid=s.datid AND ( d.datname=? OR d.oid=? )";
    EXEC SQL END DECLARE SECTION;

    EXEC SQL CONNECT TO testdb AS con1 USER testuser;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;

    EXEC SQL PREPARE stmt1 FROM :query;
    EXEC SQL DECLARE cur1 CURSOR FOR stmt1;
```

Em seguida, coloque alguns valores no SQLDA de entrada para os parâmetros de entrada. Aloque memória para o SQLDA de entrada e defina o número de parâmetros de entrada para `sqln`. Armazene o tipo, o valor e o comprimento do valor em `sqltype`, `sqldata` e `sqllen` na estrutura `sqlvar`.

```
    /* Create SQLDA structure for input parameters. */
    sqlda2 = (sqlda_t *) malloc(sizeof(sqlda_t) + sizeof(sqlvar_t));
    memset(sqlda2, 0, sizeof(sqlda_t) + sizeof(sqlvar_t));
    sqlda2->sqln = 2; /* number of input variables */

    sqlda2->sqlvar[0].sqltype = ECPGt_char;
    sqlda2->sqlvar[0].sqldata = "postgres";
    sqlda2->sqlvar[0].sqllen  = 8;

    intval = 1;
    sqlda2->sqlvar[1].sqltype = ECPGt_int;
    sqlda2->sqlvar[1].sqldata = (char *)&intval;
    sqlda2->sqlvar[1].sqllen  = sizeof(intval);
```

Após configurar o SQLDA de entrada, abra um cursor com o SQLDA de entrada.

```
    /* Open a cursor with input parameters. */
    EXEC SQL OPEN cur1 USING DESCRIPTOR sqlda2;
```

Pegue as linhas no SQLDA de saída a partir do cursor aberto. (Geralmente, você precisa chamar `FETCH` repetidamente no loop, para pegar todas as linhas no conjunto de resultados.)

```
    while (1)
    {
        sqlda_t *cur_sqlda;

        /* Assign descriptor to the cursor  */
        EXEC SQL FETCH NEXT FROM cur1 INTO DESCRIPTOR sqlda1;
```

Em seguida, retorne os registros obtidos do SQLDA, seguindo a lista vinculada da estrutura `sqlda_t`.

```
    for (cur_sqlda = sqlda1 ;
         cur_sqlda != NULL ;
         cur_sqlda = cur_sqlda->desc_next)
    {
        ...
```

Leia cada coluna no primeiro registro. O número de colunas é armazenado em `sqld`, os dados reais da primeira coluna são armazenados em `sqlvar[0]`, ambos membros da estrutura `sqlda_t`.

```
        /* Print every column in a row. */
        for (i = 0; i < sqlda1->sqld; i++)
        {
            sqlvar_t v = sqlda1->sqlvar[i];
            char *sqldata = v.sqldata;
            short sqllen  = v.sqllen;

            strncpy(name_buf, v.sqlname.data, v.sqlname.length);
            name_buf[v.sqlname.length] = '\0';
```

Agora, os dados da coluna são armazenados na variável `v`. Copie cada dado nas variáveis hostis, observando `v.sqltype` para o tipo da coluna.

```
            switch (v.sqltype) {
                int intval;
                double doubleval;
                unsigned long long int longlongval;

                case ECPGt_char:
                    memset(&var_buf, 0, sizeof(var_buf));
                    memcpy(&var_buf, sqldata, (sizeof(var_buf) <= sqllen ? sizeof(var_buf)-1 : sqllen));
                    break;

                case ECPGt_int: /* integer */
                    memcpy(&intval, sqldata, sqllen);
                    snprintf(var_buf, sizeof(var_buf), "%d", intval);
                    break;

                ...

                default:
                    ...
            }

            printf("%s = %s (type: %d)\n", name_buf, var_buf, v.sqltype);
        }
```

Feche o cursor após processar todos os registros e desconecte-se do banco de dados.

```
    EXEC SQL CLOSE cur1;
    EXEC SQL COMMIT;

    EXEC SQL DISCONNECT ALL;
```

Todo o programa é mostrado em [Exemplo 34.1](ecpg-descriptors.md#ECPG-SQLDA-EXAMPLE-EXAMPLE).

**Exemplo 34.1. Programa SQLDA**

```
#include <stdlib.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

EXEC SQL include sqlda.h;

sqlda_t *sqlda1; /* descriptor for output */
sqlda_t *sqlda2; /* descriptor for input */

EXEC SQL WHENEVER NOT FOUND DO BREAK;
EXEC SQL WHENEVER SQLERROR STOP;

int
main(void)
{
    EXEC SQL BEGIN DECLARE SECTION;
    char query[1024] = "SELECT d.oid,* FROM pg_database d, pg_stat_database s WHERE d.oid=s.datid AND ( d.datname=? OR d.oid=? )";

    int intval;
    unsigned long long int longlongval;
    EXEC SQL END DECLARE SECTION;

    EXEC SQL CONNECT TO uptimedb AS con1 USER uptime;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;

    EXEC SQL PREPARE stmt1 FROM :query;
    EXEC SQL DECLARE cur1 CURSOR FOR stmt1;

    /* Create an SQLDA structure for an input parameter */
    sqlda2 = (sqlda_t *)malloc(sizeof(sqlda_t) + sizeof(sqlvar_t));
    memset(sqlda2, 0, sizeof(sqlda_t) + sizeof(sqlvar_t));
    sqlda2->sqln = 2; /* a number of input variables */

    sqlda2->sqlvar[0].sqltype = ECPGt_char;
    sqlda2->sqlvar[0].sqldata = "postgres";
    sqlda2->sqlvar[0].sqllen  = 8;

    intval = 1;
    sqlda2->sqlvar[1].sqltype = ECPGt_int;
    sqlda2->sqlvar[1].sqldata = (char *) &intval;
    sqlda2->sqlvar[1].sqllen  = sizeof(intval);

    /* Open a cursor with input parameters. */
    EXEC SQL OPEN cur1 USING DESCRIPTOR sqlda2;

    while (1)
    {
        sqlda_t *cur_sqlda;

        /* Assign descriptor to the cursor  */
        EXEC SQL FETCH NEXT FROM cur1 INTO DESCRIPTOR sqlda1;

        for (cur_sqlda = sqlda1 ;
             cur_sqlda != NULL ;
             cur_sqlda = cur_sqlda->desc_next)
        {
            int i;
            char name_buf[1024];
            char var_buf[1024];

            /* Print every column in a row. */
            for (i=0 ; i<cur_sqlda->sqld ; i++)
            {
                sqlvar_t v = cur_sqlda->sqlvar[i];
                char *sqldata = v.sqldata;
                short sqllen  = v.sqllen;

                strncpy(name_buf, v.sqlname.data, v.sqlname.length);
                name_buf[v.sqlname.length] = '\0';

                switch (v.sqltype)
                {
                    case ECPGt_char:
                        memset(&var_buf, 0, sizeof(var_buf));
                        memcpy(&var_buf, sqldata, (sizeof(var_buf)<=sqllen ? sizeof(var_buf)-1 : sqllen) );
                        break;

                    case ECPGt_int: /* integer */
                        memcpy(&intval, sqldata, sqllen);
                        snprintf(var_buf, sizeof(var_buf), "%d", intval);
                        break;

                    case ECPGt_long_long: /* bigint */
                        memcpy(&longlongval, sqldata, sqllen);
                        snprintf(var_buf, sizeof(var_buf), "%lld", longlongval);
                        break;

                    default:
                    {
                        int i;
                        memset(var_buf, 0, sizeof(var_buf));
                        for (i = 0; i < sqllen; i++)
                        {
                            char tmpbuf[16];
                            snprintf(tmpbuf, sizeof(tmpbuf), "%02x ", (unsigned char) sqldata[i]);
                            strncat(var_buf, tmpbuf, sizeof(var_buf));
                        }
                    }
                        break;
                }

                printf("%s = %s (type: %d)\n", name_buf, var_buf, v.sqltype);
            }

            printf("\n");
        }
    }

    EXEC SQL CLOSE cur1;
    EXEC SQL COMMIT;

    EXEC SQL DISCONNECT ALL;

    return 0;
}
```

A saída deste exemplo deve parecer algo como o seguinte (alguns números variam).

```
oid = 1 (type: 1)
datname = template1 (type: 1)
datdba = 10 (type: 1)
encoding = 0 (type: 5)
datistemplate = t (type: 1)
datallowconn = t (type: 1)
dathasloginevt = f (type: 1)
datconnlimit = -1 (type: 5)
datfrozenxid = 379 (type: 1)
dattablespace = 1663 (type: 1)
datconfig =  (type: 1)
datacl = {=c/uptime,uptime=CTc/uptime} (type: 1)
datid = 1 (type: 1)
datname = template1 (type: 1)
numbackends = 0 (type: 5)
xact_commit = 113606 (type: 9)
xact_rollback = 0 (type: 9)
blks_read = 130 (type: 9)
blks_hit = 7341714 (type: 9)
tup_returned = 38262679 (type: 9)
tup_fetched = 1836281 (type: 9)
tup_inserted = 0 (type: 9)
tup_updated = 0 (type: 9)
tup_deleted = 0 (type: 9)

oid = 11511 (type: 1)
datname = postgres (type: 1)
datdba = 10 (type: 1)
encoding = 0 (type: 5)
datistemplate = f (type: 1)
datallowconn = t (type: 1)
dathasloginevt = f (type: 1)
datconnlimit = -1 (type: 5)
datfrozenxid = 379 (type: 1)
dattablespace = 1663 (type: 1)
datconfig =  (type: 1)
datacl =  (type: 1)
datid = 11511 (type: 1)
datname = postgres (type: 1)
numbackends = 0 (type: 5)
xact_commit = 221069 (type: 9)
xact_rollback = 18 (type: 9)
blks_read = 1176 (type: 9)
blks_hit = 13943750 (type: 9)
tup_returned = 77410091 (type: 9)
tup_fetched = 3253694 (type: 9)
tup_inserted = 0 (type: 9)
tup_updated = 0 (type: 9)
tup_deleted = 0 (type: 9)
```

## 34.15. Modo de compatibilidade Informix [#](#ECPG-INFORMIX-COMPAT)

* [34.15.1. Tipos adicionais](ecpg-informix-compat.md#ECPG-INFORMIX-TYPES)
* [34.15.2. Declarações SQL incorporadas adicionais/faltantes](ecpg-informix-compat.md#ECPG-INFORMIX-STATEMENTS)
* [34.15.3. Áreas de descritor SQLDA compatíveis com Informix](ecpg-informix-compat.md#ECPG-INFORMIX-SQLDA)
* [34.15.4. Funções adicionais](ecpg-informix-compat.md#ECPG-INFORMIX-FUNCTIONS)
* [34.15.5. Constantes adicionais](ecpg-informix-compat.md#ECPG-INFORMIX-CONSTANTS)

`ecpg` pode ser executado em um modo de compatibilidade denominado *Informix*. Se esse modo estiver ativo, ele tenta se comportar como se fosse o pré-compilador Informix para Informix E/SQL. Geralmente, isso permitirá que você use o sinal de dólar em vez da primitiva `EXEC SQL` para introduzir comandos SQL embutidos:

```
$int j = 3;
$CONNECT TO :dbname;
$CREATE TABLE test(i INT PRIMARY KEY, j INT);
$INSERT INTO test(i, j) VALUES (7, :j);
$COMMIT;
```

### Nota

Não deve haver espaço em branco entre o `$` e uma directiva de pré-processador subsequente, ou seja, `include`, `define`, `ifdef`, etc. Caso contrário, o pré-processador analisará o token como uma variável de host.

Existem dois modos de compatibilidade: `INFORMIX`, `INFORMIX_SE`

Ao vincular programas que utilizam este modo de compatibilidade, lembre-se de vincular contra `libcompat` que é fornecido com ECPG.

Além do açúcar sintático explicado anteriormente, o modo de compatibilidade Informix oferece algumas funções para entrada, saída e transformação de dados, bem como instruções SQL embutidas conhecidas do E/SQL para ECPG.

O modo de compatibilidade Informix está intimamente ligado à biblioteca pgtypeslib do ECPG. O pgtypeslib mapeia os tipos de dados SQL para tipos de dados dentro do programa hospedeiro C e a maioria das funções adicionais do modo de compatibilidade Informix permite que você opere nesses tipos de programa hospedeiro C. No entanto, é importante notar que o alcance da compatibilidade é limitado. Ele não tenta copiar o comportamento do Informix; permite que você faça operações mais ou menos as mesmas e lhe dá funções que têm o mesmo nome e o mesmo comportamento básico, mas não é um substituto direto se você estiver usando o Informix no momento. Além disso, alguns dos tipos de dados são diferentes. Por exemplo, os tipos datetime e interval do PostgreSQL não conhecem faixas, como, por exemplo, `YEAR TO MINUTE`, então você também não encontrará suporte no ECPG para isso.

### 34.15.1. Tipos adicionais [#](#ECPG-INFORMIX-TYPES)

O pseudo-tipo "string" especial do Informix para armazenar dados de cadeia de caracteres com recorte à direita é agora suportado no modo Informix sem o uso de `typedef`. Na verdade, no modo Informix, o ECPG se recusa a processar arquivos de origem que contenham `typedef sometype string;`

```
EXEC SQL BEGIN DECLARE SECTION;
string userid; /* this variable will contain trimmed data */
EXEC SQL END DECLARE SECTION;

EXEC SQL FETCH MYCUR INTO :userid;
```

### 34.15.2. Declarações SQL incorporadas adicionais/faltantes [#](#ECPG-INFORMIX-STATEMENTS)

`CLOSE DATABASE` [#](#ECPG-INFORMIX-STATEMENTS-CLOSE-DATABASE): Esta declaração fecha a conexão atual. De fato, isso é sinônimo do `DISCONNECT CURRENT` da ECPG:

```
$CLOSE DATABASE;                /* close the current connection */ EXEC SQL CLOSE DATABASE;
```

`FREE cursor_name` [#](#ECPG-INFORMIX-STATEMENTS-FREE-CURSOR-NAME): Devido às diferenças na forma como o ECPG funciona em comparação com o ESQL/C do Informix (nomeadamente, quais etapas são transformações puramente gramaticais e quais etapas dependem da biblioteca de execução subjacente) não há uma declaração `FREE cursor_name` no ECPG. Isso ocorre porque, no ECPG, `DECLARE CURSOR` não se traduz em uma chamada de função na biblioteca de execução que usa o nome do cursor. Isso significa que não há contabilidade de execução de cursors SQL na biblioteca de execução do ECPG, apenas no servidor PostgreSQL.

`FREE statement_name` [#](#ECPG-INFORMIX-STATEMENTS-FREE-STATEMENT-NAME): `FREE statement_name` é sinônimo de `DEALLOCATE PREPARE statement_name`.

### 34.15.3. Áreas de descritor SQLDA compatíveis com Informix [#](#ECPG-INFORMIX-SQLDA)

O modo compatível com Informix suporta uma estrutura diferente daquela descrita em [Seção 34.7.2](ecpg-descriptors.md#ECPG-SQLDA-DESCRIPTORS). Veja abaixo:

```
struct sqlvar_compat { short   sqltype; int     sqllen; char   *sqldata; short  *sqlind; char   *sqlname; char   *sqlformat; short   sqlitype; short   sqlilen; char   *sqlidata; int     sqlxid; char   *sqltypename; short   sqltypelen; short   sqlownerlen; short   sqlsourcetype; char   *sqlownername; int     sqlsourceid; char   *sqlilongdata; int     sqlflags; void   *sqlreserved; };

struct sqlda_compat { short  sqld; struct sqlvar_compat *sqlvar; char   desc_name[19]; short  desc_occ; struct sqlda_compat *desc_next; void  *reserved; };

typedef struct sqlvar_compat    sqlvar_t; typedef struct sqlda_compat     sqlda_t;
```

As propriedades globais são:

`sqld` [#](#ECPG-INFORMIX-SQLDA-SQLD): O número de campos no descritor `SQLDA`.

`sqlvar` [#](#ECPG-INFORMIX-SQLDA-SQLVAR): Ponteiro para as propriedades por campo.

`desc_name` [#](#ECPG-INFORMIX-SQLDA-DESC-NAME): Desutilizado, preenchido com bytes nulos.

`desc_occ` [#](#ECPG-INFORMIX-SQLDA-DESC-OCC): Tamanho da estrutura alocada.

`desc_next` [#](#ECPG-INFORMIX-SQLDA-DESC-NEXT): Ponte para a próxima estrutura SQLDA se o conjunto de resultados contiver mais de um registro.

`reserved` [#](#ECPG-INFORMIX-SQLDA-RESERVED): Ponteiro não utilizado, contém NULL. Mantido para compatibilidade com Informix.

As propriedades por campo estão abaixo, elas são armazenadas no array `sqlvar`:

`sqltype` [#](#ECPG-INFORMIX-SQLDA-SQLTYPE): Tipo do campo. As constantes estão em `sqltypes.h`

`sqllen` [#](#ECPG-INFORMIX-SQLDA-SQLLEN): Comprimento dos dados do campo.

`sqldata` [#](#ECPG-INFORMIX-SQLDA-SQLDATA): Ponteiro para os dados do campo. O ponteiro é do tipo `char *`, os dados apontados por ele estão em um formato binário. Exemplo:

```
int intval;

switch (sqldata->sqlvar[i].sqltype) { case SQLINTEGER: intval = *(int *)sqldata->sqlvar[i].sqldata; break; ... }
```

`sqlind` [#](#ECPG-INFORMIX-SQLDA-SQLIND): Indicador para NULL. Se retornado por DESCRIBE ou FETCH, é sempre um ponteiro válido. Se usado como entrada para `EXECUTE ... USING sqlda;`, o valor NULL-pointer significa que o valor deste campo não é NULL. Caso contrário, um ponteiro válido e `sqlitype` deve ser configurado corretamente. Exemplo:

```
if (*(int2 *)sqldata->sqlvar[i].sqlind != 0) printf("value is NULL\n");
```

`sqlname` [#](#ECPG-INFORMIX-SQLDA-SQLNAME): Nome do campo. String terminada em 0.

`sqlformat` [#](#ECPG-INFORMIX-SQLDA-SQLFORMAT): Reservado em Informix, valor de [`PQfformat`](libpq-exec.md#LIBPQ-PQFFORMAT) para o campo.

`sqlitype` [#](#ECPG-INFORMIX-SQLDA-SQLITYPE): Tipo dos dados do indicador NULL. É sempre SQLSMINT ao retornar dados do servidor. Quando o `SQLDA` é usado para uma consulta parametrizada, os dados são tratados de acordo com o tipo definido.

`sqlilen` [#](#ECPG-INFORMIX-SQLDA-SQLILEN): Comprimento dos dados do indicador NULL.

`sqlxid` [#](#ECPG-INFORMIX-SQLDA-SQLXID): Tipo estendido do campo, resultado de [`PQftype`](libpq-exec.md#LIBPQ-PQFTYPE).

`sqltypename` `sqltypelen` `sqlownerlen` `sqlsourcetype` `sqlownername` `sqlsourceid` `sqlflags` `sqlreserved` [#](#ECPG-INFORMIX-SQLDA-SQLTYPENAME): Não utilizado.

`sqlilongdata` [#](#ECPG-INFORMIX-SQLDA-SQLILONGDATA): É igual a `sqldata` se `sqllen` for maior que 32 kB.

Exemplo:

```
EXEC SQL INCLUDE sqlda.h;

    sqlda_t        *sqlda; /* This doesn't need to be under embedded DECLARE SECTION */

    EXEC SQL BEGIN DECLARE SECTION; char *prep_stmt = "select * from table1"; int i; EXEC SQL END DECLARE SECTION;

    ...

    EXEC SQL PREPARE mystmt FROM :prep_stmt;

    EXEC SQL DESCRIBE mystmt INTO sqlda;

    printf("# of fields: %d\n", sqlda->sqld); for (i = 0; i < sqlda->sqld; i++) printf("field %d: \"%s\"\n", sqlda->sqlvar[i]->sqlname);

    EXEC SQL DECLARE mycursor CURSOR FOR mystmt; EXEC SQL OPEN mycursor; EXEC SQL WHENEVER NOT FOUND GOTO out;

    while (1) { EXEC SQL FETCH mycursor USING sqlda; }

    EXEC SQL CLOSE mycursor;

    free(sqlda); /* The main structure is all to be free(),
                  * sqlda and sqlda->sqlvar is in one allocated area */
```

Para mais informações, consulte o cabeçalho `sqlda.h` e o teste de regressão `src/interfaces/ecpg/test/compat_informix/sqlda.pgc`.

### 34.15.4. Funções adicionais [#](#ECPG-INFORMIX-FUNCTIONS)

`decadd` [#](#ECPG-INFORMIX-FUNCTIONS-DECADD): Adicione dois valores de tipo decimal.

```
int decadd(decimal *arg1, decimal *arg2, decimal *sum);
```

A função recebe um ponteiro para o primeiro operando do tipo decimal (`arg1`), um ponteiro para o segundo operando do tipo decimal (`arg2`) e um ponteiro para um valor do tipo decimal que conterá a soma (`sum`). Se for bem-sucedido, a função retorna 0. `ECPG_INFORMIX_NUM_OVERFLOW` é retornado em caso de excesso e `ECPG_INFORMIX_NUM_UNDERFLOW` em caso de insuficiência. -1 é retornado para outros erros e `errno` é definido para o respectivo número `errno` do pgtypeslib.

`deccmp` [#](#ECPG-INFORMIX-FUNCTIONS-DECCMP): Compare duas variáveis do tipo decimal.

```
int deccmp(decimal *arg1, decimal *arg2);
```

A função recebe um ponteiro para o primeiro valor decimal (`arg1`), um ponteiro para o segundo valor decimal (`arg2`) e retorna um valor inteiro que indica qual é o valor maior.

* 1, se o valor que `arg1` aponta for maior que o valor que `var2` aponta
* -1, se o valor que `arg1` aponta for menor que o valor que `arg2` aponta
* 0, se o valor que `arg1` aponta e o valor que `arg2` aponta forem iguais

`deccopy` [#](#ECPG-INFORMIX-FUNCTIONS-DECCOPY) : Copie um valor decimal.

```
void deccopy(decimal *src, decimal *target);
```

A função recebe um ponteiro para o valor decimal que deve ser copiado como o primeiro argumento (`src`) e um ponteiro para a estrutura de destino do tipo decimal (`target`) como o segundo argumento.

`deccvasc` [#](#ECPG-INFORMIX-FUNCTIONS-DECCVASC): Converte um valor da sua representação ASCII para um tipo decimal.

```
int deccvasc(char *cp, int len, decimal *np);
```

A função recebe um ponteiro para uma string que contém a representação em string do número a ser convertido (`cp`) e também seu comprimento `len`. `np` é um ponteiro para o valor decimal que salva o resultado da operação.

Os formatos válidos são, por exemplo: `-2`, `.794`, `+3.44`, `592.49E07` ou `-32.84e-4`.

A função retorna 0 em caso de sucesso. Se ocorrer overflow ou underflow, `ECPG_INFORMIX_NUM_OVERFLOW` ou `ECPG_INFORMIX_NUM_UNDERFLOW` é retornado. Se a representação ASCII não puder ser analisada, `ECPG_INFORMIX_BAD_NUMERIC` é retornado ou `ECPG_INFORMIX_BAD_EXPONENT` se este problema ocorrer durante a análise do expoente.

`deccvdbl` [#](#ECPG-INFORMIX-FUNCTIONS-DECCVDBL): Converte um valor do tipo double para um valor do tipo decimal.

```
int deccvdbl(double dbl, decimal *np);
```

A função recebe a variável do tipo double que deve ser convertida como seu primeiro argumento (`dbl`). Como segundo argumento (`np`), a função recebe um ponteiro para a variável decimal que deve conter o resultado da operação.

A função retorna 0 em caso de sucesso e um valor negativo se a conversão falhou.

`deccvint` [#](#ECPG-INFORMIX-FUNCTIONS-DECCVINT): Converte um valor do tipo int para um valor do tipo decimal.

```
int deccvint(int in, decimal *np);
```

A função recebe a variável do tipo int que deve ser convertida como seu primeiro argumento (`in`). Como segundo argumento (`np`), a função recebe um ponteiro para a variável decimal que deve conter o resultado da operação.

A função retorna 0 em caso de sucesso e um valor negativo se a conversão falhou.

`deccvlong` [#](#ECPG-INFORMIX-FUNCTIONS-DECCVLONG): Converte um valor do tipo long para um valor do tipo decimal.

```
int deccvlong(long lng, decimal *np);
```

A função recebe a variável do tipo longo que deve ser convertida como seu primeiro argumento (`lng`). Como segundo argumento (`np`, a função recebe um ponteiro para a variável decimal que deve conter o resultado da operação.

A função retorna 0 em caso de sucesso e um valor negativo se a conversão falhou.

`decdiv` [#](#ECPG-INFORMIX-FUNCTIONS-DECDIV) : Divide duas variáveis do tipo decimal.

```
int decdiv(decimal *n1, decimal *n2, decimal *result);
```

A função recebe ponteiros para as variáveis que são os primeiros operandos (`n1`) e o segundo (`n2`) e calcula `n1`/`n2`. `result` é um ponteiro para a variável que deve conter o resultado da operação.

Em caso de sucesso, é retornado 0 e um valor negativo se a divisão falhar. Se ocorrer excesso ou sub-excesso, a função retorna `ECPG_INFORMIX_NUM_OVERFLOW` ou `ECPG_INFORMIX_NUM_UNDERFLOW`, respectivamente. Se for observada uma tentativa de divisão por zero, a função retorna `ECPG_INFORMIX_DIVIDE_ZERO`.

`decmul` [#](#ECPG-INFORMIX-FUNCTIONS-DECMUL): Multiplicar dois valores decimais.

```
int decmul(decimal *n1, decimal *n2, decimal *result);
```

A função recebe ponteiros para as variáveis que são os primeiros operandos (`n1`) e o segundo (`n2`) e calcula `n1`*`n2`. `result` é um ponteiro para a variável que deve conter o resultado da operação.

Em caso de sucesso, é retornado 0 e um valor negativo se a multiplicação falhar. Se ocorrer excesso ou insuficiência, a função retorna `ECPG_INFORMIX_NUM_OVERFLOW` ou `ECPG_INFORMIX_NUM_UNDERFLOW`, respectivamente.

`decsub` [#](#ECPG-INFORMIX-FUNCTIONS-DECSUB) :   Subtraia um valor decimal de outro.

```
int decsub(decimal *n1, decimal *n2, decimal *result);
```

A função recebe ponteiros para as variáveis que são os primeiros operandos (`n1`) e o segundo (`n2`) e calcula `n1`-`n2`. `result` é um ponteiro para a variável que deve conter o resultado da operação.

Em caso de sucesso, é retornado 0 e um valor negativo se a subtração falhar. Se ocorrer excesso ou insuficiência, a função retorna `ECPG_INFORMIX_NUM_OVERFLOW` ou `ECPG_INFORMIX_NUM_UNDERFLOW`, respectivamente.

`dectoasc` [#](#ECPG-INFORMIX-FUNCTIONS-DECTOASC): Converte uma variável de tipo decimal para sua representação ASCII em uma string de caracteres `char*`.

```
int dectoasc(decimal *np, char *cp, int len, int right)
```

A função recebe um ponteiro para uma variável do tipo decimal (`np`) que ela converte para sua representação textual. `cp` é o buffer que deve conter o resultado da operação. O parâmetro `right` especifica quantos dígitos à direita do ponto decimal devem ser incluídos na saída. O resultado será arredondado para este número de dígitos decimais. Definir `right` para -1 indica que todos os dígitos decimais disponíveis devem ser incluídos na saída. Se o comprimento do buffer de saída, que é indicado por `len`, não for suficiente para manter a representação textual, incluindo o byte de zero final, apenas um único caractere `*` é armazenado no resultado e -1 é retornado.

A função retorna -1 se o buffer `cp` fosse muito pequeno ou `ECPG_INFORMIX_OUT_OF_MEMORY` se a memória fosse esgotada.

`dectodbl` [#](#ECPG-INFORMIX-FUNCTIONS-DECTODBL): Converte uma variável de tipo decimal para um duplo.

```
int dectodbl(decimal *np, double *dblp);
```

A função recebe um ponteiro para o valor decimal a ser convertido (`np`) e um ponteiro para a variável dupla que deve conter o resultado da operação (`dblp`).

Em caso de sucesso, é retornado 0 e um valor negativo se a conversão falhou.

`dectoint` [#](#ECPG-INFORMIX-FUNCTIONS-DECTOINT): Converte uma variável de tipo decimal em um inteiro.

```
int dectoint(decimal *np, int *ip);
```

A função recebe um ponteiro para o valor decimal a ser convertido (`np`) e um ponteiro para a variável inteira que deve conter o resultado da operação (`ip`).

Em caso de sucesso, é retornado 0 e um valor negativo se a conversão falhou. Se ocorrer um excesso, é retornado `ECPG_INFORMIX_NUM_OVERFLOW`.

Observe que a implementação do ECPG difere da implementação do Informix. O Informix limita um inteiro ao intervalo de -32767 a 32767, enquanto os limites na implementação do ECPG dependem da arquitetura (`INT_MIN .. INT_MAX`).

`dectolong` [#](#ECPG-INFORMIX-FUNCTIONS-DECTOLONG): Converte uma variável de tipo decimal em um inteiro longo.

```
int dectolong(decimal *np, long *lngp);
```

A função recebe um ponteiro para o valor decimal a ser convertido (`np`) e um ponteiro para a variável longa que deve conter o resultado da operação (`lngp`).

Em caso de sucesso, é retornado 0 e um valor negativo se a conversão falhou. Se ocorrer um excesso, é retornado `ECPG_INFORMIX_NUM_OVERFLOW`.

Observe que a implementação do ECPG difere da implementação do Informix. O Informix limita um inteiro longo para o intervalo de -2.147.483.647 a 2.147.483.647, enquanto os limites na implementação do ECPG dependem da arquitetura (`-LONG_MAX .. LONG_MAX`).

`rdatestr` [#](#ECPG-INFORMIX-FUNCTIONS-RDATESTR): Converte uma data em uma cadeia de caracteres C.

```
int rdatestr(date d, char *str);
```

A função recebe dois argumentos, o primeiro é a data a ser convertida (`d`) e o segundo é um ponteiro para a string de destino. O formato de saída é sempre `yyyy-mm-dd`, então você precisa alocar pelo menos 11 bytes (incluindo o terminator de zero bytes) para a string.

A função retorna 0 em caso de sucesso e um valor negativo em caso de erro.

Observe que a implementação do ECPG difere da implementação do Informix. No Informix, o formato pode ser influenciado pela definição de variáveis de ambiente. No entanto, no ECPG, você não pode alterar o formato de saída.

`rstrdate` [#](#ECPG-INFORMIX-FUNCTIONS-RSTRDATE): Analise a representação textual de uma data.

```
int rstrdate(char *str, date *d);
```

A função recebe a representação textual da data a ser convertida (`str`) e um ponteiro para uma variável do tipo data (`d`). Esta função não permite que você especifique uma máscara de formato. Ela usa a máscara de formato padrão do Informix, que é `mm/dd/yyyy`. Internamente, esta função é implementada por meio de `rdefmtdate`. Portanto, `rstrdate` não é mais rápida e, se você tiver a opção, deve optar por `rdefmtdate`, que permite especificar a máscara de formato explicitamente.

A função retorna os mesmos valores que `rdefmtdate`.

`rtoday` [#](#ECPG-INFORMIX-FUNCTIONS-RTODAY) : Obter a data atual.

```
void rtoday(date *d);
```

A função recebe um ponteiro para uma variável de data (`d`) que ela define como a data atual.

Internamente, essa função utiliza a função `PGTYPESdate_today`(ecpg-pgtypes.md#PGTYPESDATETODAY).

`rjulmdy` [#](#ECPG-INFORMIX-FUNCTIONS-RJULMDY): Extraia os valores do dia, mês e ano de uma variável do tipo data.

```
int rjulmdy(date d, short mdy[3]);
```

A função recebe a data `d` e um ponteiro para um array de 3 valores inteiros curtos `mdy`. O nome da variável indica a ordem sequencial: `mdy[0]` será definido para conter o número do mês, `mdy[1]` será definido para o valor do dia e `mdy[2]` conterá o ano.

A função sempre retorna 0 no momento.

Internally, the function uses the `PGTYPESdate_julmdy`(ecpg-pgtypes.md#PGTYPESDATEJULMDY) function.

`rdefmtdate` [#](#ECPG-INFORMIX-FUNCTIONS-RDEFMTDATE): Use uma máscara de formato para converter uma cadeia de caracteres em um valor do tipo data.

```
int rdefmtdate(date *d, char *fmt, char *str);
```

A função recebe um ponteiro para o valor da data que deve conter o resultado da operação (`d`), a máscara de formato a ser usada para a análise da data (`fmt`) e a cadeia de caracteres C * que contém a representação textual da data (`str`). A representação textual deve corresponder à máscara de formato. No entanto, você não precisa ter uma correspondência 1:1 entre a cadeia de caracteres e a máscara de formato. A função analisa apenas a ordem sequencial e procura os literais `yy` ou `yyyy` que indicam a posição do ano, `mm` para indicar a posição do mês e `dd` para indicar a posição do dia.

A função retorna os seguintes valores:

* 0 - A função foi encerrada com sucesso.
* `ECPG_INFORMIX_ENOSHORTDATE` - A data não contém delimitadores entre dia, mês e ano. Neste caso, a string de entrada deve ter exatamente 6 ou 8 bytes, mas não tem.
* `ECPG_INFORMIX_ENOTDMY` - A string de formato não indicou corretamente a ordem sequencial do ano, mês e dia.
* `ECPG_INFORMIX_BAD_DAY` - A string de entrada não contém um dia válido.
* `ECPG_INFORMIX_BAD_MONTH` - A string de entrada não contém um mês válido.
* `ECPG_INFORMIX_BAD_YEAR` - A string de entrada não contém um ano válido.

Internamente, essa função é implementada para usar a função `PGTYPESdate_defmt_asc`(ecpg-pgtypes.md#PGTYPESDATEDEFMTASC). Veja a referência lá para uma tabela de entrada de exemplo.

`rfmtdate` [#](#ECPG-INFORMIX-FUNCTIONS-RFMTDATE): Converte uma variável do tipo data para sua representação textual usando uma máscara de formato.

```
int rfmtdate(date d, char *fmt, char *str);
```

A função recebe a data a ser convertida (`d`), a máscara de formato (`fmt`) e a string que conterá a representação textual da data (`str`).

Em caso de sucesso, é retornado 0 e um valor negativo se ocorrer um erro.

Internamente, essa função usa a função `PGTYPESdate_fmt_asc`(ecpg-pgtypes.md#PGTYPESDATEFMTASC), veja a referência lá para exemplos.

`rmdyjul` [#](#ECPG-INFORMIX-FUNCTIONS-RMDYJUL): Crie um valor de data a partir de um array de 3 números inteiros curtos que especificam o dia, o mês e o ano da data.

```
int rmdyjul(short mdy[3], date *d);
```

A função recebe o array dos 3 inteiros curtos (`mdy`) e um ponteiro para uma variável do tipo data que deve conter o resultado da operação.

Atualmente, a função sempre retorna 0.

Internamente, a função é implementada para usar a função `PGTYPESdate_mdyjul`(ecpg-pgtypes.md#PGTYPESDATEMDYJUL).

`rdayofweek` [#](#ECPG-INFORMIX-FUNCTIONS-RDAYOFWEEK): Retorne um número que representa o dia da semana para um valor de data.

```
int rdayofweek(date d);
```

A função recebe a variável de data `d` como seu único argumento e retorna um inteiro que indica o dia da semana para essa data.

* 0 - Domingo
* 1 - Segunda-feira
* 2 - Segunda-feira
* 3 - Terça-feira
* 4 - Quarta-feira
* 5 - Quinta-feira
* 6 - Sábado

Internamente, a função é implementada para usar a função `PGTYPESdate_dayofweek`(ecpg-pgtypes.md#PGTYPESDATEDAYOFWEEK).

`dtcurrent` [#](#ECPG-INFORMIX-FUNCTIONS-DTCURRENT): Obtenha o timestamp atual.

```
void dtcurrent(timestamp *ts);
```

A função recupera o timestamp atual e o salva na variável timestamp que a `ts` aponta.

`dtcvasc` [#](#ECPG-INFORMIX-FUNCTIONS-DTCVASC): Analisa um marcador de tempo a partir de sua representação textual em uma variável de marcador de tempo.

```
int dtcvasc(char *str, timestamp *ts);
```

A função recebe a string a ser analisada (`str`) e um ponteiro para a variável de marcação de tempo que deve conter o resultado da operação (`ts`).

A função retorna 0 em caso de sucesso e um valor negativo em caso de erro.

Internamente, essa função utiliza a função `PGTYPEStimestamp_from_asc`(ecpg-pgtypes.md#PGTYPESTIMESTAMPFROMASC). Veja a referência lá para uma tabela com entradas de exemplo.

`dtcvfmtasc` [#](#ECPG-INFORMIX-FUNCTIONS-DTCVFMTASC): Analisa um marcador de tempo a partir de sua representação textual, usando uma máscara de formato, em uma variável de marcador de tempo.

```
dtcvfmtasc(char *inbuf, char *fmtstr, timestamp *dtvalue)
```

A função recebe a string a ser analisada (`inbuf`), a máscara de formato a ser usada (`fmtstr`) e um ponteiro para a variável de marcação de tempo que deve conter o resultado da operação (`dtvalue`).

Essa função é implementada por meio da função `PGTYPEStimestamp_defmt_asc` (ecpg-pgtypes.md#PGTYPESTIMESTAMPDEFMTASC). Veja a documentação para uma lista de especificadores de formato que podem ser usados.

A função retorna 0 em caso de sucesso e um valor negativo em caso de erro.

`dtsub` [#](#ECPG-INFORMIX-FUNCTIONS-DTSUB): Subtraia um timestamp de outro e retorne uma variável do tipo intervalo.

```
int dtsub(timestamp *ts1, timestamp *ts2, interval *iv);
```

A função subtrairá a variável de marcação de tempo que `ts2` aponta da variável de marcação de tempo que `ts1` aponta e armazenará o resultado na variável de intervalo que `iv` aponta.

Se o sucesso for alcançado, a função retorna 0 e um valor negativo se ocorrer um erro.

`dttoasc` [#](#ECPG-INFORMIX-FUNCTIONS-DTTOASC): Converte uma variável de data e hora em uma cadeia de caracteres C * char.

```
int dttoasc(timestamp *ts, char *output);
```

A função recebe um ponteiro para a variável de marcação de tempo a ser convertida (`ts`) e a string que deve conter o resultado da operação (`output`). Ela converte `ts` em sua representação textual de acordo com o padrão SQL, que é `YYYY-MM-DD HH:MM:SS`.

Se o sucesso for alcançado, a função retorna 0 e um valor negativo se ocorrer um erro.

`dttofmtasc` [#](#ECPG-INFORMIX-FUNCTIONS-DTTOFMTASC): Converte uma variável de data e hora em um C char* usando uma máscara de formato.

```
int dttofmtasc(timestamp *ts, char *output, int str_len, char *fmtstr);
```

A função recebe um ponteiro para o timestamp a ser convertido como seu primeiro argumento (`ts`), um ponteiro para o buffer de saída (`output`), o comprimento máximo que foi alocado para o buffer de saída (`str_len`) e a máscara de formato a ser usada para a conversão (`fmtstr`).

Se o sucesso for alcançado, a função retorna 0 e um valor negativo se ocorrer um erro.

Internally, essa função usa a função `PGTYPEStimestamp_fmt_asc`(ecpg-pgtypes.md#PGTYPESTIMESTAMPFMTASC). Veja a referência lá para obter informações sobre quais máscaras de especificadores de formato podem ser usadas.

`intoasc` [#](#ECPG-INFORMIX-FUNCTIONS-INTOASC): Converte uma variável de intervalo em uma cadeia de caracteres C * char.

```
int intoasc(interval *i, char *str);
```

A função recebe um ponteiro para a variável de intervalo a ser convertida (`i`) e a string que deve conter o resultado da operação (`str`). Ela converte `i` em sua representação textual de acordo com o padrão SQL, que é `YYYY-MM-DD HH:MM:SS`.

Se o sucesso for alcançado, a função retorna 0 e um valor negativo se ocorrer um erro.

`rfmtlong` [#](#ECPG-INFORMIX-FUNCTIONS-RFMTLONG): Converte um valor de inteiro longo para sua representação textual usando uma máscara de formato.

```
int rfmtlong(long lng_val, char *fmt, char *outbuf);
```

A função recebe o valor longo `lng_val`, a máscara de formato `fmt` e um ponteiro para o buffer de saída `outbuf`. Ela converte o valor longo de acordo com a máscara de formato para sua representação textual.

A máscara de formato pode ser composta pelos seguintes caracteres que especificam o formato:

* `*` (asterisco) - se esta posição ficar em branco
* `&` (símbolo e) - se esta posição ficar em branco
* `#` - transformar zeros anteriores em espaços em branco.
* `<` - alinhar o número à esquerda na string.
* `,` (ponto e vírgula) - agrupar números de quatro ou mais dígitos em grupos de três dígitos separados por vírgulas.
* `.` (ponto) - este caractere separa a parte numérica inteira do número da parte fracionária.
* `-` (menos) - o sinal menos aparece se o número for um valor negativo.
* `+` (mais) - o sinal mais aparece se o número for um valor positivo.
* `(` - este substitui o sinal menos na frente do número negativo. O sinal menos não aparecerá.
* `)` - este caractere substitui o sinal menos e é impresso atrás do valor negativo.
* `$` - o símbolo da moeda.

`rupshift` [#](#ECPG-INFORMIX-FUNCTIONS-RUPSHIFT) :   Converter uma string para maiúsculas.

```
void rupshift(char *str);
```

A função recebe um ponteiro para a string e transforma cada caractere em minúsculas para maiúsculas.

`byleng` [#](#ECPG-INFORMIX-FUNCTIONS-BYLENG): Retorne o número de caracteres em uma string sem contar espaços em branco finais.

```
int byleng(char *str, int len);
```

A função espera uma string de comprimento fixo como seu primeiro argumento (`str`) e seu comprimento como seu segundo argumento ([`len`]). Ela retorna o número de caracteres significativos, ou seja, o comprimento da string sem espaços finais.

`ldchar` [#](#ECPG-INFORMIX-FUNCTIONS-LDCHAR): Copie uma string de comprimento fixo em uma string terminada por nulo.

```
void ldchar(char *src, int len, char *dest);
```

A função recebe a string de comprimento fixo a ser copiada (`src`), seu comprimento (`len`) e um ponteiro para a memória de destino (`dest`). Observe que você precisa reservar pelo menos `len+1` bytes para a string a que `dest` aponta. A função copia no máximo `len` bytes para a nova localização (menos se a string de origem tiver espaços finais) e adiciona o terminator nulo.

`rgetmsg` [#](#ECPG-INFORMIX-FUNCTIONS-RGETMSG): ``` int rgetmsg(int msgnum, char *s, int maxsize);
```

Essa função existe, mas não está implementada no momento!

`rtypalign` [#](#ECPG-INFORMIX-FUNCTIONS-RTYPALIGN): ``` int rtypalign(int offset, int type);
```

Essa função existe, mas não está implementada no momento!

`rtypmsize` [#](#ECPG-INFORMIX-FUNCTIONS-RTYPMSIZE): ``` int rtypmsize(int type, int len);
```

Essa função existe, mas não está implementada no momento!

`rtypwidth` [#](#ECPG-INFORMIX-FUNCTIONS-RTYPWIDTH): ``` int rtypwidth(int sqltype, int sqllen);
```

Essa função existe, mas não está implementada no momento!

`rsetnull` [#](#RSETNULL) :   Defina uma variável como NULL.

```
int rsetnull(int t, char *ptr);
```

A função recebe um inteiro que indica o tipo da variável e um ponteiro para a própria variável, que é convertido em um ponteiro C char*.

Existem os seguintes tipos:

* `CCHARTYPE` - Para uma variável do tipo `char` ou `char*`
* `CSHORTTYPE` - Para uma variável do tipo `short int`
* `CINTTYPE` - Para uma variável do tipo `int`
* `CBOOLTYPE` - Para uma variável do tipo `boolean`
* `CFLOATTYPE` - Para uma variável do tipo `float`
* `CLONGTYPE` - Para uma variável do tipo `long`
* `CDOUBLETYPE` - Para uma variável do tipo `double`
* `CDECIMALTYPE` - Para uma variável do tipo `decimal`
* `CDATETYPE` - Para uma variável do tipo `date`
* `CDTIMETYPE` - Para uma variável do tipo `timestamp`

Aqui está um exemplo de uma chamada a essa função:

```
$char c[] = "abc       "; $short s = 17; $int i = -74874;

rsetnull(CCHARTYPE, (char *) c); rsetnull(CSHORTTYPE, (char *) &s); rsetnull(CINTTYPE, (char *) &i);
```

`risnull` [#](#ECPG-INFORMIX-FUNCTIONS-RISNULL) : Verifique se uma variável é NULL.

```
int risnull(int t, char *ptr);
```

A função recebe o tipo da variável a ser testada (`t`) e também um ponteiro para essa variável (`ptr`). Observe que este último precisa ser convertido em char*. Consulte a função `rsetnull`(ecpg-informix-compat.md#RSETNULL) para uma lista dos possíveis tipos de variáveis.

Aqui está um exemplo de como usar essa função:

```
$char c[] = "abc       "; $short s = 17; $int i = -74874;

risnull(CCHARTYPE, (char *) c); risnull(CSHORTTYPE, (char *) &s); risnull(CINTTYPE, (char *) &i);
```

### 34.15.5. Constantes adicionais [#](#ECPG-INFORMIX-CONSTANTS)

Observe que todas as constantes aqui descrevem erros e todas elas são definidas para representar valores negativos. Nas descrições das diferentes constantes, você também pode encontrar o valor que as constantes representam na implementação atual. No entanto, você não deve confiar nesse número. No entanto, você pode confiar no fato de que todas elas são definidas para representar valores negativos.

`ECPG_INFORMIX_NUM_OVERFLOW` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-NUM-OVERFLOW): As funções retornam esse valor se ocorrer um excesso em um cálculo. Internamente, é definido como -1200 (a definição da Informix).

`ECPG_INFORMIX_NUM_UNDERFLOW` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-NUM-UNDERFLOW): As funções retornam esse valor se ocorrer um subfluxo em um cálculo. Internally, é definido como -1201 (a definição Informix).

`ECPG_INFORMIX_DIVIDE_ZERO` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-DIVIDE-ZERO): As funções retornam esse valor se uma tentativa de divisão por zero for observada. Internamente, é definido como -1202 (a definição Informix).

`ECPG_INFORMIX_BAD_YEAR` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-YEAR): As funções retornam esse valor se um valor inválido para um ano for encontrado durante a paráfrase de uma data. Internamente, é definido como -1204 (a definição Informix).

`ECPG_INFORMIX_BAD_MONTH` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-MONTH): As funções retornam esse valor se um valor inválido para um mês for encontrado durante a paráfrase de uma data. Internamente, é definido como -1205 (a definição Informix).

`ECPG_INFORMIX_BAD_DAY` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-DAY): As funções retornam esse valor se um valor inválido para um dia for encontrado durante a paráfrase de uma data. Internamente, é definido como -1206 (a definição Informix).

`ECPG_INFORMIX_ENOSHORTDATE` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-ENOSHORTDATE): As funções retornam esse valor se uma rotina de análise precisar de uma representação curta de data, mas não recebeu a string de data no comprimento correto. Internamente, é definido como -1209 (a definição Informix).

`ECPG_INFORMIX_DATE_CONVERT` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-DATE-CONVERT): As funções retornam esse valor se ocorrer um erro durante a formatação da data. Internamente, é definido como -1210 (a definição da Informix).

`ECPG_INFORMIX_OUT_OF_MEMORY` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-OUT-OF-MEMORY): As funções retornam esse valor se a memória tiver sido esgotada durante sua operação. Internamente, é definido como -1211 (a definição da Informix).

`ECPG_INFORMIX_ENOTDMY` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-ENOTDMY): As funções retornam esse valor se uma rotina de análise deveria receber uma máscara de formato (como `mmddyy`) mas não todos os campos foram listados corretamente. Internamente, é definido como -1212 (a definição da Informix).

`ECPG_INFORMIX_BAD_NUMERIC` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-NUMERIC): As funções retornam esse valor se uma rotina de análise não conseguir analisar a representação textual para um valor numérico porque contém erros ou se uma rotina não conseguir completar um cálculo envolvendo variáveis numéricas porque pelo menos uma das variáveis numéricas é inválida. Internamente, é definido como -1213 (a definição da Informix).

`ECPG_INFORMIX_BAD_EXPONENT` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-EXPONENT): As funções retornam esse valor se uma rotina de análise não conseguir analisar um expoente. Internamente, é definido como -1216 (a definição da Informix).

`ECPG_INFORMIX_BAD_DATE` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-DATE): As funções retornam esse valor se uma rotina de análise não conseguir analisar uma data. Internamente, é definido como -1218 (a definição da Informix).

`ECPG_INFORMIX_EXTRA_CHARS` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-EXTRA-CHARS): As funções retornam esse valor se uma rotina de análise for passada caracteres extras que ela não consegue analisar. Internamente, é definido como -1264 (a definição da Informix).
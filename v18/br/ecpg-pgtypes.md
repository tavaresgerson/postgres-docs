## 34.6. Biblioteca pgtypes [#](#ECPG-PGTYPES)

* [34.6.1. Strings de caractere](ecpg-pgtypes.md#ECPG-PGTYPES-CSTRINGS)
* [34.6.2. O tipo numérico](ecpg-pgtypes.md#ECPG-PGTYPES-NUMERIC)
* [34.6.3. O tipo de data](ecpg-pgtypes.md#ECPG-PGTYPES-DATE)
* [34.6.4. O tipo de marca de tempo](ecpg-pgtypes.md#ECPG-PGTYPES-TIMESTAMP)
* [34.6.5. O tipo de intervalo](ecpg-pgtypes.md#ECPG-PGTYPES-INTERVAL)
* [34.6.6. O tipo decimal](ecpg-pgtypes.md#ECPG-PGTYPES-DECIMAL)
* [34.6.7. Valores de errno de pgtypeslib](ecpg-pgtypes.md#ECPG-PGTYPES-ERRNO)
* [34.6.8. Constantes especiais de pgtypeslib](ecpg-pgtypes.md#ECPG-PGTYPES-CONSTANTS)

A biblioteca pgtypes mapeia os tipos de banco de dados do PostgreSQL para equivalentes em C que podem ser usados em programas em C. Ela também oferece funções para realizar cálculos básicos com esses tipos dentro do C, ou seja, sem a ajuda do servidor PostgreSQL. Veja o exemplo a seguir:

```
EXEC SQL BEGIN DECLARE SECTION;
   date date1;
   timestamp ts1, tsout;
   interval iv1;
   char *out;
EXEC SQL END DECLARE SECTION;

PGTYPESdate_today(&date1);
EXEC SQL SELECT started, duration INTO :ts1, :iv1 FROM datetbl WHERE d=:date1;
PGTYPEStimestamp_add_interval(&ts1, &iv1, &tsout);
out = PGTYPEStimestamp_to_asc(&tsout);
printf("Started + duration: %s\n", out);
PGTYPESchar_free(out);
```

### 34.6.1. Strings de caracteres [#](#ECPG-PGTYPES-CSTRINGS)

Algumas funções, como `PGTYPESnumeric_to_asc`, retornam um ponteiro para uma cadeia de caracteres recém-alocada. Esses resultados devem ser liberados com `PGTYPESchar_free` em vez de `free`. (Isso é importante apenas no Windows, onde a alocação e liberação de memória às vezes precisam ser feitas pela mesma biblioteca.)

### 34.6.2. O tipo numérico [#](#ECPG-PGTYPES-NUMERIC)

O tipo numérico oferece a possibilidade de realizar cálculos com precisão arbitrária. Consulte a [Seção 8.1](datatype-numeric.md) para obter o tipo equivalente no servidor PostgreSQL. Devido à precisão arbitrária, essa variável precisa ser capaz de se expandir e contrair dinamicamente. É por isso que você só pode criar variáveis numéricas no heap, por meio das funções `PGTYPESnumeric_new` e `PGTYPESnumeric_free`. O tipo decimal, que é semelhante, mas limitado em precisão, pode ser criado tanto na pilha quanto no heap.

As funções a seguir podem ser usadas para trabalhar com o tipo numérico:

`PGTYPESnumeric_new` [#](#ECPG-PGTYPES-NUMERIC-NEW): Solicite um ponteiro para uma variável numérica recém-alocada.

```
numeric *PGTYPESnumeric_new(void);
```

`PGTYPESnumeric_free` [#](#ECPG-PGTYPES-NUMERIC-FREE): Liberar um tipo numérico, liberar toda a sua memória.

```
void PGTYPESnumeric_free(numeric *var);
```

`PGTYPESnumeric_from_asc` [#](#ECPG-PGTYPES-NUMERIC-FROM-ASC): Parsear um tipo numérico a partir de sua notação em cadeia.

```
numeric *PGTYPESnumeric_from_asc(char *str, char **endptr);
```

Os formatos válidos são, por exemplo: `-2`, `.794`, `+3.44`, `592.49E07` ou `-32.84e-4`. Se o valor puder ser analisado com sucesso, um ponteiro válido é retornado, caso contrário, o ponteiro NULL. No momento, o ECPG sempre analisa a string completa e, portanto, atualmente não suporta armazenar o endereço do primeiro caractere inválido em `*endptr`. Você pode definir seguramente `endptr` como NULL.

`PGTYPESnumeric_to_asc` [#](#ECPG-PGTYPES-NUMERIC-TO-ASC): Retorna um ponteiro para uma string alocada por `malloc` que contém a representação de string do tipo numérico `num`.

```
char *PGTYPESnumeric_to_asc(numeric *num, int dscale);
```

O valor numérico será impresso com `dscale` dígitos decimais, com arredondamento aplicado, se necessário. O resultado deve ser liberado com `PGTYPESchar_free()`.

`PGTYPESnumeric_add` [#](#ECPG-PGTYPES-NUMERIC-ADD): Adicione duas variáveis numéricas a uma terceira.

```
int PGTYPESnumeric_add(numeric *var1, numeric *var2, numeric *result);
```

A função adiciona as variáveis `var1` e `var2` à variável de resultado `result`. A função retorna 0 em caso de sucesso e -1 em caso de erro.

`PGTYPESnumeric_sub` [#](#ECPG-PGTYPES-NUMERIC-SUB): Subtraia duas variáveis numéricas e retorne o resultado em uma terceira.

```
int PGTYPESnumeric_sub(numeric *var1, numeric *var2, numeric *result);
```

A função subtrai a variável `var2` da variável `var1`. O resultado da operação é armazenado na variável `result`. A função retorna 0 em caso de sucesso e -1 em caso de erro.

`PGTYPESnumeric_mul` [#](#ECPG-PGTYPES-NUMERIC-MUL): Multiplique duas variáveis numéricas e retorne o resultado em uma terceira.

```
int PGTYPESnumeric_mul(numeric *var1, numeric *var2, numeric *result);
```

A função multiplica as variáveis `var1` e `var2`. O resultado da operação é armazenado na variável `result`. A função retorna 0 em caso de sucesso e -1 em caso de erro.

`PGTYPESnumeric_div` [#](#ECPG-PGTYPES-NUMERIC-DIV): Divide duas variáveis numéricas e retorna o resultado em uma terceira.

```
int PGTYPESnumeric_div(numeric *var1, numeric *var2, numeric *result);
```

A função divide as variáveis `var1` por `var2`. O resultado da operação é armazenado na variável `result`. A função retorna 0 em caso de sucesso e -1 em caso de erro.

`PGTYPESnumeric_cmp` [#](#ECPG-PGTYPES-NUMERIC-CMP) :   Compare duas variáveis numéricas.

```
int PGTYPESnumeric_cmp(numeric *var1, numeric *var2)
```

Essa função compara duas variáveis numéricas. Em caso de erro, `INT_MAX` é retornado. Se for bem-sucedido, a função retorna um dos três resultados possíveis:

* 1, se `var1` for maior que `var2`
* -1, se `var1` for menor que `var2`
* 0, se `var1` e `var2` forem iguais

`PGTYPESnumeric_from_int` [#](#ECPG-PGTYPES-NUMERIC-FROM-INT): Converte uma variável int em uma variável numérica.

```
int PGTYPESnumeric_from_int(signed int int_val, numeric *var);
```

Essa função aceita uma variável do tipo int assinado e a armazena na variável numérica `var`. Se for bem-sucedida, 0 é retornado e -1 no caso de falha.

`PGTYPESnumeric_from_long` [#](#ECPG-PGTYPES-NUMERIC-FROM-LONG): Converte uma variável de tipo inteiro longo em uma variável numérica.

```
int PGTYPESnumeric_from_long(signed long int long_val, numeric *var);
```

Essa função aceita uma variável do tipo signed long int e a armazena na variável numérica `var`. Se for bem-sucedida, é retornado 0 e -1 em caso de falha.

`PGTYPESnumeric_copy` [#](#ECPG-PGTYPES-NUMERIC-COPY): Copie uma variável numérica para outra.

```
int PGTYPESnumeric_copy(numeric *src, numeric *dst);
```

Essa função copia o valor da variável que `src` aponta para a variável que `dst` aponta. Ela retorna 0 em caso de sucesso e -1 se ocorrer um erro.

`PGTYPESnumeric_from_double` [#](#ECPG-PGTYPES-NUMERIC-FROM-DOUBLE): Converte uma variável do tipo double em numérico.

```
int  PGTYPESnumeric_from_double(double d, numeric *dst);
```

Essa função aceita uma variável do tipo double e armazena o resultado na variável que `dst` aponta. Ela retorna 0 em caso de sucesso e -1 se ocorrer um erro.

`PGTYPESnumeric_to_double` [#](#ECPG-PGTYPES-NUMERIC-TO-DOUBLE): Converte uma variável de tipo numérico para double.

```
int PGTYPESnumeric_to_double(numeric *nv, double *dp)
```

A função converte o valor numérico da variável que `nv` aponta para a variável dupla que `dp` aponta. Ela retorna 0 em caso de sucesso e -1 se ocorrer um erro, incluindo overflow. Em caso de overflow, a variável global `errno` será definida adicionalmente como `PGTYPES_NUM_OVERFLOW`.

`PGTYPESnumeric_to_int` [#](#ECPG-PGTYPES-NUMERIC-TO-INT): Converte uma variável de tipo numérico para int.

```
int PGTYPESnumeric_to_int(numeric *nv, int *ip);
```

A função converte o valor numérico da variável que `nv` aponta para a variável inteira que `ip` aponta para. Ela retorna 0 em caso de sucesso e -1 se ocorrer um erro, incluindo overflow. Em caso de overflow, a variável global `errno` será definida adicionalmente como `PGTYPES_NUM_OVERFLOW`.

`PGTYPESnumeric_to_long` [#](#ECPG-PGTYPES-NUMERIC-TO-LONG): Converte uma variável de tipo numérico para longo.

```
int PGTYPESnumeric_to_long(numeric *nv, long *lp);
```

A função converte o valor numérico da variável que `nv` aponta para a variável de inteiro longo que `lp` aponta para. Ela retorna 0 em caso de sucesso e -1 se ocorrer um erro, incluindo overflow e underflow. Em overflow, a variável global `errno` será definida como `PGTYPES_NUM_OVERFLOW` e em underflow `errno` será definida como `PGTYPES_NUM_UNDERFLOW`.

`PGTYPESnumeric_to_decimal` [#](#ECPG-PGTYPES-NUMERIC-TO-DECIMAL): Converte uma variável de tipo numérico para decimal.

```
int PGTYPESnumeric_to_decimal(numeric *src, decimal *dst);
```

A função converte o valor numérico da variável que `src` aponta para a variável decimal que `dst` aponta para. Ela retorna 0 em caso de sucesso e -1 se ocorrer um erro, incluindo overflow. Em caso de overflow, a variável global `errno` será definida como `PGTYPES_NUM_OVERFLOW` adicionalmente.

`PGTYPESnumeric_from_decimal` [#](#ECPG-PGTYPES-NUMERIC-FROM-DECIMAL): Converte uma variável de tipo decimal em numérico.

```
int PGTYPESnumeric_from_decimal(decimal *src, numeric *dst);
```

A função converte o valor decimal da variável que `src` aponta para a variável numérica que `dst` aponta. Ela retorna 0 em caso de sucesso e -1 se ocorrer um erro. Como o tipo decimal é implementado como uma versão limitada do tipo numérico, não pode ocorrer excesso com essa conversão.

### 34.6.3. A data do tipo [#](#ECPG-PGTYPES-DATE)

O tipo de data em C permite que seus programas lidem com dados do tipo SQL date. Consulte [Seção 8.5](datatype-datetime.md) para o tipo equivalente no servidor PostgreSQL.

As seguintes funções podem ser usadas para trabalhar com o tipo de data:

`PGTYPESdate_from_timestamp` [#](#PGTYPESDATEFROMTIMESTAMP): Extrair a parte da data de um timestamp.

```
date PGTYPESdate_from_timestamp(timestamp dt);
```

A função recebe um timestamp como seu único argumento e retorna a parte da data extraída desse timestamp.

`PGTYPESdate_from_asc` [#](#PGTYPESDATEFROMASC): Parse a date from its textual representation.

```
date PGTYPESdate_from_asc(char *str, char **endptr);
```

A função recebe uma cadeia de caracteres C char* `str` e um ponteiro para uma cadeia de caracteres C char* `endptr`. No momento, o ECPG sempre analisa a cadeia completa e, portanto, atualmente não suporta armazenar o endereço do primeiro caractere inválido em `*endptr`. Você pode definir com segurança `endptr` como NULL.

Observe que a função sempre assume datas formatadas MDY e, atualmente, não há uma variável para alterar isso dentro do ECPG.

[Tabela 34.2] (ecpg-pgtypes.md#ECPG-PGTYPESDATE-FROM-ASC-TABLE "Table 34.2. Valid Input Formats for PGTYPESdate_from_asc") mostra os formatos de entrada permitidos.

**Tabela 34.2. Formatos de entrada válidos para `PGTYPESdate_from_asc`**



<table border="1" class="table" summary="Valid Input Formats for PGTYPESdate_from_asc">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Input
   </th>
   <th>
    Resultado
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     January 8, 1999
    </code>
   </td>
   <td>
    <code class="literal">
     January 8, 1999
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     1999-01-08
    </code>
   </td>
   <td>
    <code class="literal">
     January 8, 1999
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     1/8/1999
    </code>
   </td>
   <td>
    <code class="literal">
     January 8, 1999
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     1/18/1999
    </code>
   </td>
   <td>
    <code class="literal">
     January 18, 1999
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     01/02/03
    </code>
   </td>
   <td>
    <code class="literal">
     February 1, 2003
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     1999-Jan-08
    </code>
   </td>
   <td>
    <code class="literal">
     January 8, 1999
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     Jan-08-1999
    </code>
   </td>
   <td>
    <code class="literal">
     January 8, 1999
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     08-Jan-1999
    </code>
   </td>
   <td>
    <code class="literal">
     January 8, 1999
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     99-Jan-08
    </code>
   </td>
   <td>
    <code class="literal">
     January 8, 1999
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     08-Jan-99
    </code>
   </td>
   <td>
    <code class="literal">
     January 8, 1999
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     08-Jan-06
    </code>
   </td>
   <td>
    <code class="literal">
     January 8, 2006
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     Jan-08-99
    </code>
   </td>
   <td>
    <code class="literal">
     January 8, 1999
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     19990108
    </code>
   </td>
   <td>
    <code class="literal">
     ISO 8601; January 8, 1999
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     990108
    </code>
   </td>
   <td>
    <code class="literal">
     ISO 8601; January 8, 1999
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     1999.008
    </code>
   </td>
   <td>
    <code class="literal">
     year and day of year
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     J2451187
    </code>
   </td>
   <td>
    <code class="literal">
     Julian day
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     January 8, 99 BC
    </code>
   </td>
   <td>
    <code class="literal">
     year 99 before the Common Era
    </code>
   </td>
  </tr>
 </tbody>
</table>







`PGTYPESdate_to_asc` [#](#PGTYPESDATETOASC) :   Retorne a representação textual de uma variável de data.

```
char *PGTYPESdate_to_asc(date dDate);
```

A função recebe a data `dDate` como seu único parâmetro. Ela retornará a data na forma `1999-01-18`, ou seja, no formato `YYYY-MM-DD`. O resultado deve ser liberado com `PGTYPESchar_free()`.

`PGTYPESdate_julmdy` [#](#PGTYPESDATEJULMDY): Extraia os valores do dia, mês e ano de uma variável do tipo data.

```
void PGTYPESdate_julmdy(date d, int *mdy);
```

A função recebe a data `d` e um ponteiro para um array de 3 valores inteiros `mdy`. O nome da variável indica a ordem sequencial: `mdy[0]` será definido para conter o número do mês, `mdy[1]` será definido para o valor do dia e `mdy[2]` conterá o ano.

`PGTYPESdate_mdyjul` [#](#PGTYPESDATEMDYJUL): Crie um valor de data a partir de um array de 3 inteiros que especificam o dia, o mês e o ano da data.

```
void PGTYPESdate_mdyjul(int *mdy, date *jdate);
```

A função recebe o array dos 3 inteiros (`mdy`) como seu primeiro argumento e, como segundo argumento, um ponteiro para uma variável do tipo data que deve conter o resultado da operação.

`PGTYPESdate_dayofweek` [#](#PGTYPESDATEDAYOFWEEK): Retorne um número que representa o dia da semana para um valor de data.

```
int PGTYPESdate_dayofweek(date d);
```

A função recebe a variável de data `d` como seu único argumento e retorna um inteiro que indica o dia da semana para essa data.

* 0 - Domingo
* 1 - Segunda-feira
* 2 - Segunda-feira
* 3 - Terça-feira
* 4 - Quarta-feira
* 5 - Quinta-feira
* 6 - Sábado

`PGTYPESdate_today` [#](#PGTYPESDATETODAY) : Obter a data atual.

```
void PGTYPESdate_today(date *d);
```

A função recebe um ponteiro para uma variável de data (`d`) que ela define como a data atual.

`PGTYPESdate_fmt_asc` [#](#PGTYPESDATEFMTASC): Converte uma variável do tipo data para sua representação textual usando uma máscara de formato.

```
int PGTYPESdate_fmt_asc(date dDate, char *fmtstring, char *outbuf);
```

A função recebe a data a ser convertida (`dDate`), a máscara de formato (`fmtstring`) e a string que conterá a representação textual da data (`outbuf`).

Em caso de sucesso, é retornado 0 e um valor negativo se ocorrer um erro.

Os seguintes literais são os especificadores de campo que você pode usar:

* `dd` - O número do dia do mês.
* `mm` - O número do mês do ano.
* `yy` - O número do ano como número de duas casas decimais.
* `yyyy` - O número do ano como número de quatro casas decimais.
* `ddd` - O nome do dia (abreviado).
* `mmm` - O nome do mês (abreviado).

Todos os outros caracteres são copiados 1:1 para a string de saída.

[Tabela 34.3](ecpg-pgtypes.md#ECPG-PGTYPESDATE-FMT-ASC-EXAMPLE-TABLE) indica alguns formatos possíveis. Isso lhe dará uma ideia de como usar essa função. Todas as linhas de saída são baseadas na mesma data: 23 de novembro de 1959.

**Tabela 34.3. Formatos de entrada válidos para `PGTYPESdate_fmt_asc`**



<table border="1" class="table" summary="Valid Input Formats for PGTYPESdate_fmt_asc">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Format
   </th>
   <th>
    Result
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     mmddyy
    </code>
   </td>
   <td>
    <code class="literal">
     112359
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ddmmyy
    </code>
   </td>
   <td>
    <code class="literal">
     231159
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     yymmdd
    </code>
   </td>
   <td>
    <code class="literal">
     591123
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     yy/mm/dd
    </code>
   </td>
   <td>
    <code class="literal">
     59/11/23
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     yy mm dd
    </code>
   </td>
   <td>
    <code class="literal">
     59 11 23
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     yy.mm.dd
    </code>
   </td>
   <td>
    <code class="literal">
     59.11.23
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     .mm.yyyy.dd.
    </code>
   </td>
   <td>
    <code class="literal">
     .11.1959.23.
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     mmm. dd, yyyy
    </code>
   </td>
   <td>
    <code class="literal">
     Nov. 23, 1959
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     mmm dd yyyy
    </code>
   </td>
   <td>
    <code class="literal">
     Nov 23 1959
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     yyyy dd mm
    </code>
   </td>
   <td>
    <code class="literal">
     1959 23 11
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ddd, mmm. dd, yyyy
    </code>
   </td>
   <td>
    <code class="literal">
     Mon, Nov. 23, 1959
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     (ddd) mmm. dd, yyyy
    </code>
   </td>
   <td>
    <code class="literal">
     (Mon) Nov. 23, 1959
    </code>
   </td>
  </tr>
 </tbody>
</table>







`PGTYPESdate_defmt_asc` [#](#PGTYPESDATEDEFMTASC) : Use uma máscara de formato para converter uma string de C `char*` em um valor do tipo data.

```
int PGTYPESdate_defmt_asc(date *d, char *fmt, char *str);
```

A função recebe um ponteiro para o valor da data que deve conter o resultado da operação (`d`), a máscara de formato a ser usada para a análise da data (`fmt`) e a cadeia de caracteres C * que contém a representação textual da data (`str`). A representação textual deve corresponder à máscara de formato. No entanto, você não precisa ter uma correspondência 1:1 entre a cadeia de caracteres e a máscara de formato. A função analisa apenas a ordem sequencial e procura os literais `yy` ou `yyyy` que indicam a posição do ano, `mm` para indicar a posição do mês e `dd` para indicar a posição do dia.

[Tabela 34.4](ecpg-pgtypes.md#ECPG-RDEFMTDATE-EXAMPLE-TABLE) indica alguns formatos possíveis. Isso lhe dará uma ideia de como usar essa função.

**Tabela 34.4. Formatos de entrada válidos para `rdefmtdate`**



<table border="1" class="table" summary="Valid Input Formats for rdefmtdate">
 <colgroup>
  <col/>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Format
   </th>
   <th>
    String
   </th>
   <th>
    Result
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     ddmmyy
    </code>
   </td>
   <td>
    <code class="literal">
     21-2-54
    </code>
   </td>
   <td>
    <code class="literal">
     1954-02-21
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ddmmyy
    </code>
   </td>
   <td>
    <code class="literal">
     2-12-54
    </code>
   </td>
   <td>
    <code class="literal">
     1954-12-02
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ddmmyy
    </code>
   </td>
   <td>
    <code class="literal">
     20111954
    </code>
   </td>
   <td>
    <code class="literal">
     1954-11-20
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ddmmyy
    </code>
   </td>
   <td>
    <code class="literal">
     130464
    </code>
   </td>
   <td>
    <code class="literal">
     1964-04-13
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     mmm.dd.yyyy
    </code>
   </td>
   <td>
    <code class="literal">
     MAR-12-1967
    </code>
   </td>
   <td>
    <code class="literal">
     1967-03-12
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     yy/mm/dd
    </code>
   </td>
   <td>
    <code class="literal">
     1954, February 3rd
    </code>
   </td>
   <td>
    <code class="literal">
     1954-02-03
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     mmm.dd.yyyy
    </code>
   </td>
   <td>
    <code class="literal">
     041269
    </code>
   </td>
   <td>
    <code class="literal">
     1969-04-12
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     yy/mm/dd
    </code>
   </td>
   <td>
    <code class="literal">
     In the year 2525, in the month of July, mankind will be alive on the 28th day
    </code>
   </td>
   <td>
    <code class="literal">
     2525-07-28
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     dd-mm-yy
    </code>
   </td>
   <td>
    <code class="literal">
     I said on the 28th of July in the year 2525
    </code>
   </td>
   <td>
    <code class="literal">
     2525-07-28
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     mmm.dd.yyyy
    </code>
   </td>
   <td>
    <code class="literal">
     9/14/58
    </code>
   </td>
   <td>
    <code class="literal">
     1958-09-14
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     yy/mm/dd
    </code>
   </td>
   <td>
    <code class="literal">
     47/03/29
    </code>
   </td>
   <td>
    <code class="literal">
     1947-03-29
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     mmm.dd.yyyy
    </code>
   </td>
   <td>
    <code class="literal">
     oct 28 1975
    </code>
   </td>
   <td>
    <code class="literal">
     1975-10-28
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     mmddyy
    </code>
   </td>
   <td>
    <code class="literal">
     Nov 14th, 1985
    </code>
   </td>
   <td>
    <code class="literal">
     1985-11-14
    </code>
   </td>
  </tr>
 </tbody>
</table>







### 34.6.4. O tipo de marcação de tempo [#](#ECPG-PGTYPES-TIMESTAMP)

O tipo de marcação de tempo em C permite que seus programas lidem com dados do tipo timestamp do SQL. Consulte a [Seção 8.5](datatype-datetime.md) para o tipo equivalente no servidor PostgreSQL.

As seguintes funções podem ser usadas para trabalhar com o tipo de marca-texto:

`PGTYPEStimestamp_from_asc` [#](#PGTYPESTIMESTAMPFROMASC): Parsear um timestamp de sua representação textual em uma variável de timestamp.

```
timestamp PGTYPEStimestamp_from_asc(char *str, char **endptr);
```

A função recebe a string a ser analisada (`str`) e um ponteiro para um C char* (`endptr`). No momento, o ECPG sempre analisa a string completa e, portanto, atualmente não suporta armazenar o endereço do primeiro caractere inválido em `*endptr`. Você pode, com segurança, definir `endptr` como NULL.

A função retorna o horário de data e hora analisado em caso de sucesso. Em caso de erro, `PGTYPESInvalidTimestamp` é retornado e `errno` é `PGTYPES_TS_BAD_TIMESTAMP`. Consulte [`PGTYPESInvalidTimestamp`](ecpg-pgtypes.md#PGTYPESINVALIDTIMESTAMP) para notas importantes sobre esse valor.

Em geral, a string de entrada pode conter qualquer combinação de uma especificação de data permitida, um caractere de espaço em branco e uma especificação de hora permitida. Note que os fusos horários não são suportados pelo ECPG. Ele pode analisá-los, mas não aplica nenhum cálculo como o servidor PostgreSQL, por exemplo. Os especificadores de fuso horário são descartados silenciosamente.

[Tabela 34.5](ecpg-pgtypes.md#ECPG-PGTYPESTIMESTAMP-FROM-ASC-EXAMPLE-TABLE) contém alguns exemplos de strings de entrada.

**Tabela 34.5. Formatos de entrada válidos para `PGTYPEStimestamp_from_asc`**



<table border="1" class="table" summary="Valid Input Formats for PGTYPEStimestamp_from_asc">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Input
   </th>
   <th>
    Resultado
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     1999-01-08 04:05:06
    </code>
   </td>
   <td>
    <code class="literal">
     1999-01-08 04:05:06
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     January 8 04:05:06 1999 PST
    </code>
   </td>
   <td>
    <code class="literal">
     1999-01-08 04:05:06
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     1999-Jan-08 04:05:06.789-8
    </code>
   </td>
   <td>
    <code class="literal">
     1999-01-08 04:05:06.789 (time zone specifier ignored)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     J2451187 04:05-08:00
    </code>
   </td>
   <td>
    <code class="literal">
     1999-01-08 04:05:00 (time zone specifier ignored)
    </code>
   </td>
  </tr>
 </tbody>
</table>







`PGTYPEStimestamp_to_asc` [#](#PGTYPESTIMESTAMPTOASC) : Converte uma data em uma cadeia de caracteres C.

```
char *PGTYPEStimestamp_to_asc(timestamp tstamp);
```

A função recebe o timestamp `tstamp` como seu único argumento e retorna uma string alocada que contém a representação textual do timestamp. O resultado deve ser liberado com `PGTYPESchar_free()`.

`PGTYPEStimestamp_current` [#](#PGTYPESTIMESTAMPCURRENT): Obtenha o timestamp atual.

```
void PGTYPEStimestamp_current(timestamp *ts);
```

A função recupera o timestamp atual e o salva na variável timestamp que a `ts` aponta.

`PGTYPEStimestamp_fmt_asc` [#](#PGTYPESTIMESTAMPFMTASC): Converte uma variável de data e hora em um C char* usando uma máscara de formato.

```
int PGTYPEStimestamp_fmt_asc(timestamp *ts, char *output, int str_len, char *fmtstr);
```

A função recebe um ponteiro para o timestamp a ser convertido como seu primeiro argumento (`ts`), um ponteiro para o buffer de saída (`output`), o comprimento máximo que foi alocado para o buffer de saída (`str_len`) e a máscara de formato a ser usada para a conversão (`fmtstr`).

Se o sucesso for alcançado, a função retorna 0 e um valor negativo se ocorrer um erro.

Você pode usar os seguintes especificadores de formato para a máscara de formato. Os especificadores de formato são os mesmos que são usados na função `strftime` na libc. Qualquer especificador de formato não formatado será copiado no buffer de saída.

* `%A` - é substituído pela representação nacional do nome completo do dia da semana.
* `%a` - é substituído pela representação nacional do nome abreviado do dia da semana.
* `%B` - é substituído pela representação nacional do nome completo do mês.
* `%b` - é substituído pela representação nacional do nome abreviado do mês.
* `%C` - é substituído por (ano / 100) como número decimal; os algarismos únicos são precedidos por um zero.
* `%c` - é substituído pela representação nacional de hora e data.
* `%D` - é equivalente a
* `%m/%d/%y`.
* `%d` - é substituído pelo dia do mês como número decimal (01–31).
* `%E*` `%O*` - extensões do local POSIX. As sequências
* `%Ec`
* `%EC`
* `%Ex`
* `%EX`
* `%Ey`
* `%EY`
* `%Od`
* `%Oe`
* `%OH`
* `%OI`
* `%Om`
* `%OM`
* `%OS`
* `%Ou`
* `%OU`
* `%OV`
* `%Ow`
* `%OW`
* `%Oy` são supostas a fornecer representações alternativas.

Além disso, `%OB` implementado para representar nomes alternativos de meses (usados isoladamente, sem o dia mencionado).
* `%e` - é substituído pelo dia do mês como um número decimal (1–31); dígitos únicos são precedidos por um espaço.
* `%F` - é equivalente a `%Y-%m-%d`.
* `%G` - é substituído por um ano como um número decimal com século. Este ano é o que contém a maior parte da semana (Segunda-feira como o primeiro dia da semana).
* `%g` - é substituído pelo mesmo ano que em `%G`, mas como um número decimal sem século (00–99).
* `%H` - é substituído pela hora (relógio de 24 horas) como um número decimal (00–23).
* `%h` - o mesmo que `%b`.
* `%I` - é substituído pela hora (relógio de 12 horas) como um número decimal (01–12).
* `%j` - é substituído pelo dia do ano como um número decimal (001–366).
* `%k` - é substituído pela hora (relógio de 24 horas) como um número decimal (0–23); dígitos únicos são precedidos por um espaço.
* `%l` - é substituído pela hora (relógio de 12 horas) como um número decimal (1–12); dígitos únicos são precedidos por um espaço.
* `%M` - é substituído pelo minuto como um número decimal (00–59).
* `%m` - é substituído pelo mês como um número decimal (01–12).
* `%n` - é substituído por uma nova linha.
* `%O*` - o mesmo que `%E*`.
* `%p` - é substituído pela representação nacional de "ante meridiem" ou "post meridiem", conforme apropriado.
* `%R` - é equivalente a `%H:%M`.
* `%r` - é equivalente a `%I:%M:%S %p`.
* `%S` - é substituído pelo número do semana do ano (Segunda-feira como o primeiro dia da semana) como um número decimal (00–53).
* `%s` - é substituído pelo número de segundos desde o Epoch, UTC.
* `%T` - é equivalente a `%H:%M:%S`
* `%t` - é substituído por uma tabulação.
* `%U` - é substituído pelo número da semana do ano (Segunda-feira como o primeiro dia da semana) como um número decimal (01–53). Se a semana contendo o dia 1 de janeiro tiver quatro ou mais dias no novo ano, então é a semana 1; caso contrário, é a última semana do ano anterior, e a próxima semana é a semana 1.
* `%v` - é equivalente a `%e-%b-%Y`.
* `%W` - é substituído pelo número da semana do ano (Segunda-feira como o primeiro dia da semana) como um número decimal (00–53).
* `%w` - é substituído pelo dia útil (Segunda-feira como o primeiro dia da semana) como um número decimal (0–6).
* `%X` - é substituído pela representação nacional do tempo.
* `%x` - é substituído pela representação nacional da data.
* `%Y` - é substituído pelo ano com século como um número decimal.
* `%y` - é substituído pelo ano sem século como um número decimal (00–99).
* `%Z` - é substituído pelo nome da zona horária.
* `%z` - é substituído pelo deslocamento do fuso horário a partir UTC; um sinal de mais no início representa leste de UTC, um sinal de menos para oeste de UTC, horas e minutos seguem com dois dígitos cada e sem delimitador entre eles (forma comum para [RFC 822](https://datatracker.ietf.org/doc/html/rfc822) cabeçalhos de data).
* `%+` - é substituído pela representação nacional da data e tempo.
* `%-*` - extensão da GNU libc. Não faça nenhum preenchimento ao realizar saídas numéricas.
* $_* - extensão da GNU libc. Especifique explicitamente espaço para preenchimento.
* `%0*` - extensão da GNU libc. Especifique explicitamente zero para preenchimento.
* `%%` - é substituído por `%`.

`PGTYPEStimestamp_sub` [#](#PGTYPESTIMESTAMPSUB): Subtraia um timestamp de outro e salve o resultado em uma variável do tipo intervalo.

```
int PGTYPEStimestamp_sub(timestamp *ts1, timestamp *ts2, interval *iv);
```

A função subtrairá a variável de marcação de tempo que `ts2` aponta da variável de marcação de tempo que `ts1` aponta e armazenará o resultado na variável de intervalo que `iv` aponta.

Se o sucesso for alcançado, a função retorna 0 e um valor negativo se ocorrer um erro.

`PGTYPEStimestamp_defmt_asc` [#](#PGTYPESTIMESTAMPDEFMTASC): Parsear um valor de data e hora a partir de sua representação textual usando uma máscara de formatação.

```
int PGTYPEStimestamp_defmt_asc(char *str, char *fmt, timestamp *d);
```

A função recebe a representação textual de um marcador de tempo na variável `str` e também a máscara de formatação a ser usada na variável `fmt`. O resultado será armazenado na variável que a variável `d` aponta.

Se a máscara de formatação `fmt` for NULL, a função voltará à máscara de formatação padrão, que é `%Y-%m-%d %H:%M:%S`.

Esta é a função inversa de `PGTYPEStimestamp_fmt_asc`(ecpg-pgtypes.md#PGTYPESTIMESTAMPFMTASC). Veja a documentação lá para descobrir sobre as possíveis entradas da máscara de formatação.

`PGTYPEStimestamp_add_interval` [#](#PGTYPESTIMESTAMPADDINTERVAL): Adicione uma variável de intervalo a uma variável de marcação de tempo.

```
int PGTYPEStimestamp_add_interval(timestamp *tin, interval *span, timestamp *tout);
```

A função recebe um ponteiro para uma variável de marcação de tempo `tin` e um ponteiro para uma variável de intervalo `span`. Ela adiciona o intervalo à marcação de tempo e salva o resultado da marcação de tempo na variável que aponta para `tout`.

Se o sucesso for alcançado, a função retorna 0 e um valor negativo se ocorrer um erro.

`PGTYPEStimestamp_sub_interval` [#](#PGTYPESTIMESTAMPSUBINTERVAL): Subtrair uma variável de intervalo de uma variável de marcação de tempo.

```
int PGTYPEStimestamp_sub_interval(timestamp *tin, interval *span, timestamp *tout);
```

A função subtrai a variável de intervalo que `span` aponta da variável de marcação de tempo que `tin` aponta e salva o resultado na variável que `tout` aponta.

Se o sucesso for alcançado, a função retorna 0 e um valor negativo se ocorrer um erro.

### 34.6.5. O intervalo Tipo [#](#ECPG-PGTYPES-INTERVAL)

O tipo de intervalo em C permite que seus programas lidem com dados do tipo intervalo do SQL. Consulte [Seção 8.5](datatype-datetime.md) para o tipo equivalente no servidor PostgreSQL.

As seguintes funções podem ser usadas para trabalhar com o tipo de intervalo:

`PGTYPESinterval_new` [#](#PGTYPESINTERVALNEW): Retorne um ponteiro para uma variável de intervalo recém-alocada.

```
interval *PGTYPESinterval_new(void);
```

`PGTYPESinterval_free` [#](#PGTYPESINTERVALFREE): Liberar a memória de uma variável de intervalo previamente alocada.

```
void PGTYPESinterval_free(interval *intvl);
```

`PGTYPESinterval_from_asc` [#](#PGTYPESINTERVALFROMASC): Parsear um intervalo a partir de sua representação textual.

```
interval *PGTYPESinterval_from_asc(char *str, char **endptr);
```

A função analisa a string de entrada `str` e retorna um ponteiro para uma variável de intervalo alocada. No momento, o ECPG sempre analisa a string completa e, portanto, atualmente não suporta armazenar o endereço do primeiro caractere inválido em `*endptr`. Você pode, com segurança, definir `endptr` para NULL.

`PGTYPESinterval_to_asc` [#](#PGTYPESINTERVALTOASC): Converte uma variável de tipo intervalo para sua representação textual.

```
char *PGTYPESinterval_to_asc(interval *span);
```

A função converte a variável de intervalo que `span` indica em um C char*. A saída tem a aparência deste exemplo: `@ 1 day 12 hours 59 mins 10 secs`. O resultado deve ser liberado com `PGTYPESchar_free()`.

`PGTYPESinterval_copy` [#](#PGTYPESINTERVALCOPY) : Copie uma variável do tipo intervalo.

```
int PGTYPESinterval_copy(interval *intvlsrc, interval *intvldest);
```

A função copia a variável de intervalo que `intvlsrc` aponta para a variável que aponta para `intvldest`. Note que você precisa alocar a memória para a variável de destino antes.

### 34.6.6. Tipo decimal [#](#ECPG-PGTYPES-DECIMAL)

O tipo decimal é semelhante ao tipo numérico. No entanto, é limitado a uma precisão máxima de 30 dígitos significativos. Em contraste com o tipo numérico, que pode ser criado apenas na pilha, o tipo decimal pode ser criado na pilha ou na memória (por meio das funções `PGTYPESdecimal_new` e `PGTYPESdecimal_free`). Há muitas outras funções que lidam com o tipo decimal no modo de compatibilidade Informix descrito em [Seção 34.15] (ecpg-informix-compat.md "34.15. Informix Compatibility Mode").

As funções a seguir podem ser usadas para trabalhar com o tipo decimal e não estão contidas apenas na biblioteca `libcompat`.

`PGTYPESdecimal_new` [#](#ECPG-PGTYPES-DECIMAL-NEW): Peça um ponteiro para uma variável decimal recém-alocada.

```
decimal *PGTYPESdecimal_new(void);
```

`PGTYPESdecimal_free` [#](#ECPG-PGTYPES-DECIMAL-FREE): Liberar um tipo decimal, liberar toda a sua memória.

```
void PGTYPESdecimal_free(decimal *var);
```

### 34.6.7. Valores de errno de pgtypeslib [#](#ECPG-PGTYPES-ERRNO)

`PGTYPES_NUM_BAD_NUMERIC` [#](#ECPG-PGTYPES-ERRNO-PGTYPES-NUM-BAD-NUMERIC): Um argumento deve conter uma variável numérica (ou apontar para uma variável numérica) mas, na verdade, sua representação de memória era inválida.

`PGTYPES_NUM_OVERFLOW` [#](#ECPG-PGTYPES-ERRNO-PGTYPES-NUM-OVERFLOW): Ocorreu um excesso. Como o tipo numérico pode lidar com uma precisão quase arbitrária, a conversão de uma variável numérica em outros tipos pode causar excesso.

`PGTYPES_NUM_UNDERFLOW` [#](#ECPG-PGTYPES-ERRNO-PGTYPES-NUM-UNDERFLOW): Ocorreu um subfluxo. Como o tipo numérico pode lidar com uma precisão quase arbitrária, a conversão de uma variável numérica em outros tipos pode causar subfluxo.

`PGTYPES_NUM_DIVIDE_ZERO` [#](#ECPG-PGTYPES-ERRNO-PGTYPES-NUM-DIVIDE-ZERO): Foi realizada uma divisão por zero.

`PGTYPES_DATE_BAD_DATE` [#](#ECPG-PGTYPES-ERRNO-PGTYPES-DATE-BAD-DATE): Uma string de data inválida foi passada para a função `PGTYPESdate_from_asc`.

`PGTYPES_DATE_ERR_EARGS` [#](#ECPG-PGTYPES-ERRNO-PGTYPES-DATE-ERR-EARGS): Argumentos inválidos foram passados para a função `PGTYPESdate_defmt_asc`.

`PGTYPES_DATE_ERR_ENOSHORTDATE` [#](#ECPG-PGTYPES-ERRNO-PGTYPES-DATE-ERR-ENOSHORTDATE): Um token inválido na string de entrada foi encontrado pela função `PGTYPESdate_defmt_asc`.

`PGTYPES_INTVL_BAD_INTERVAL` [#](#ECPG-PGTYPES-ERRNO-PGTYPES-INTVL-BAD-INTERVAL): Uma string de intervalo inválida foi passada para a função `PGTYPESinterval_from_asc` ou um valor de intervalo inválido foi passado para a `PGTYPESinterval_to_asc` função.

`PGTYPES_DATE_ERR_ENOTDMY` [#](#ECPG-PGTYPES-ERRNO-PGTYPES-DATE-ERR-ENOTDMY): Houve um desajuste na atribuição de dia/mês/ano na função `PGTYPESdate_defmt_asc`.

`PGTYPES_DATE_BAD_DAY` [#](#ECPG-PGTYPES-ERRNO-PGTYPES-DATE-BAD-DAY): Foi encontrado um valor inválido do dia do mês pela função `PGTYPESdate_defmt_asc`.

`PGTYPES_DATE_BAD_MONTH` [#](#ECPG-PGTYPES-ERRNO-PGTYPES-DATE-BAD-MONTH): Um valor de mês inválido foi encontrado pela função `PGTYPESdate_defmt_asc`.

`PGTYPES_TS_BAD_TIMESTAMP` [#](#ECPG-PGTYPES-ERRNO-PGTYPES-TS-BAD-TIMESTAMP): Uma string de marcação de tempo inválida foi passada para a função `PGTYPEStimestamp_from_asc`, ou um valor de marcação de tempo inválido foi passado para a função `PGTYPEStimestamp_to_asc`.

`PGTYPES_TS_ERR_EINFTIME` [#](#ECPG-PGTYPES-ERRNO-PGTYPES-TS-ERR-EINFTIME): Um valor de marcação de tempo infinito foi encontrado em um contexto que não pode lidar com ele.

### 34.6.8. Constantes especiais do pgtypeslib [#](#ECPG-PGTYPES-CONSTANTS)

`PGTYPESInvalidTimestamp` [#](#PGTYPESINVALIDTIMESTAMP): Um valor do tipo marca-passo que representa um rótulo de tempo inválido. Esse valor é retornado pela função `PGTYPEStimestamp_from_asc` em erro de análise. Observe que, devido à representação interna do tipo de dados `timestamp`, `PGTYPESInvalidTimestamp` também é um rótulo de tempo válido ao mesmo tempo. Ele é definido como `1899-12-31 23:59:59`. Para detectar erros, certifique-se de que sua aplicação não apenas teste para `PGTYPESInvalidTimestamp`, mas também para `errno != 0` após cada chamada para `PGTYPEStimestamp_from_asc`.
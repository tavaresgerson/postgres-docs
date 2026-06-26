### 8.5. Tipos de data/hora [#](#DATATYPE-DATETIME)

* [8.5.1. Entrada de data/hora](datatype-datetime.md#DATATYPE-DATETIME-INPUT)
* [8.5.2. Saída de data/hora](datatype-datetime.md#DATATYPE-DATETIME-OUTPUT)
* [8.5.3. Fuso horário](datatype-datetime.md#DATATYPE-TIMEZONES)
* [8.5.4. Entrada de intervalo](datatype-datetime.md#DATATYPE-INTERVAL-INPUT)
* [8.5.5. Saída de intervalo](datatype-datetime.md#DATATYPE-INTERVAL-OUTPUT)

O PostgreSQL suporta o conjunto completo dos tipos de data e hora do SQL, mostrados na [Tabela 8.9] (datatype-datetime.md#DATATYPE-DATETIME-TABLE "Table 8.9. Date/Time Types"). As operações disponíveis nesses tipos de dados são descritas na [Seção 9.9] (functions-datetime.md "9.9. Date/Time Functions and Operators"). As datas são contadas de acordo com o calendário gregoriano, mesmo em anos antes de esse calendário ser introduzido (consulte [Seção B.6] (datetime-units-history.md "B.6. History of Units") para mais informações).

**Tabela 8.9. Tipos de data/hora**

<table>
 <colgroup>
  <col/>
  <col/>
  <col/>
  <col/>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Nome
   </th>
   <th>
    Storage Size
   </th>
   <th>
    Descrição
   </th>
   <th>
    Low Value
   </th>
   <th>
    High Value
   </th>
   <th>
    Resolution
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     timestamp [ (
     <em class="replaceable">
      <code>
       p
      </code>
     </em>
     ) ] [ without time zone ]
    </code>
   </td>
   <td>
    8 bytes
   </td>
   <td>
    data e hora (sem fuso horário)
   </td>
   <td>
    4713 BC
   </td>
   <td>
    294276 AD
   </td>
   <td>
    1 microsecond
   </td>
  </tr>
  <tr>
   <td>
    <code>
     timestamp [ (
     <em class="replaceable">
      <code>
       p
      </code>
     </em>
     ) ] with time zone
    </code>
   </td>
   <td>
    8 bytes
   </td>
   <td>
    data e hora, com fuso horário
   </td>
   <td>
    4713 BC
   </td>
   <td>
    294276 AD
   </td>
   <td>
    1 microsecond
   </td>
  </tr>
  <tr>
   <td>
    <code>
     date
    </code>
   </td>
   <td>
    4 bytes
   </td>
   <td>
    data (sem horário do dia)
   </td>
   <td>
    4713 BC
   </td>
   <td>
    5874897 AD
   </td>
   <td>
    1 day
   </td>
  </tr>
  <tr>
   <td>
    <code>
     time [ (
     <em class="replaceable">
      <code>
       p
      </code>
     </em>
     ) ] [ without time zone ]
    </code>
   </td>
   <td>
    8 bytes
   </td>
   <td>
    hora do dia (sem data)
   </td>
   <td>
    00:00:00
   </td>
   <td>
    24:00:00
   </td>
   <td>
    1 microsecond
   </td>
  </tr>
  <tr>
   <td>
    <code>
     time [ (
     <em class="replaceable">
      <code>
       p
      </code>
     </em>
     ) ] with time zone
    </code>
   </td>
   <td>
    12 bytes
   </td>
   <td>
    hora do dia (sem data), com fuso horário
   </td>
   <td>
    00:00:00+1559
   </td>
   <td>
    24:00:00-1559
   </td>
   <td>
    1 microsecond
   </td>
  </tr>
  <tr>
   <td>
    <code>
     interval [
     <em class="replaceable">
      <code>
       fields
      </code>
     </em>
     ] [ (
     <em class="replaceable">
      <code>
       p
      </code>
     </em>
     ) ]
    </code>
   </td>
   <td>
    16 bytes
   </td>
   <td>
    intervalo de tempo
   </td>
   <td>
    -178000000 years
   </td>
   <td>
    178000000 years
   </td>
   <td>
    1 microsecond
   </td>
  </tr>
 </tbody>
</table>

Nota

O padrão SQL exige que a escrita apenas `timestamp` seja equivalente a `timestamp without time zone`, e o PostgreSQL respeita esse comportamento. `timestamptz` é aceito como uma abreviação para `timestamp with time zone`; essa é uma extensão do PostgreSQL.

`time`, `timestamp` e `interval` aceitam um valor de precisão opcional *`p`* que especifica o número de dígitos fracionários retidos no campo de segundos. Por padrão, não há limite explícito para a precisão. O intervalo permitido de *`p`* é de 0 a 6.

O tipo `interval` tem uma opção adicional, que é restringir o conjunto de campos armazenados, escrevendo uma dessas frases:

```sql
YEAR
MONTH
DAY
HOUR
MINUTE
SECOND
YEAR TO MONTH
DAY TO HOUR
DAY TO MINUTE
DAY TO SECOND
HOUR TO MINUTE
HOUR TO SECOND
MINUTE TO SECOND
```

Observe que, se ambos os valores de *`fields`* e *`p`* forem especificados, o *`fields`* deve incluir `SECOND`, uma vez que a precisão se aplica apenas aos segundos.

O tipo `time with time zone` é definido pelo padrão SQL, mas a definição apresenta propriedades que levam a uma utilidade questionável. Na maioria dos casos, uma combinação de `date`, `time`, `timestamp without time zone` e `timestamp with time zone` deve fornecer uma gama completa de funcionalidades de data/hora necessárias por qualquer aplicativo.

#### 8.5.1. Entrada de data/hora [#](#DATATYPE-DATETIME-INPUT)

A entrada de data e hora é aceita em quase qualquer formato razoável, incluindo ISO 8601, compatível com SQL, POSTGRES tradicional e outros. Para alguns formatos, a ordem do dia, mês e ano na entrada de data é ambígua e há suporte para especificar a ordem esperada desses campos. Defina o parâmetro [DateStyle](runtime-config-client.md#GUC-DATESTYLE) para `MDY` para selecionar a interpretação mês-dia-ano, `DMY` para selecionar a interpretação dia-mês-ano ou `YMD` para selecionar a interpretação ano-mês-dia.

O PostgreSQL é mais flexível ao lidar com a entrada de data/hora do que o padrão SQL exige. Consulte o [Apêndice B] para as regras exatas de análise da entrada de data/hora e para os campos de texto reconhecidos, incluindo meses, dias da semana e fusos horários.

Lembre-se de que qualquer entrada literal de data ou hora deve ser fechada entre aspas, como strings de texto. Consulte [Seção 4.1.2.7](sql-syntax-lexical.md#SQL-SYNTAX-CONSTANTS-GENERIC) para obter mais informações. O SQL requer a seguinte sintaxe

```sql
type [ (p) ] 'value'
```

onde *`p`* é uma especificação opcional de precisão que fornece o número de dígitos fracionários no campo de segundos. A precisão pode ser especificada para os tipos `time`, `timestamp` e `interval`, e pode variar de 0 a 6. Se nenhuma precisão for especificada em uma especificação constante, ela será definida como a precisão do valor literal (mas não mais de 6 dígitos).

##### 8.5.1.1. Datas [#](#DATATYPE-DATETIME-INPUT-DATES)

[Tabela 8.10](datatype-datetime.md#DATATYPE-DATETIME-DATE-TABLE) mostra alguns possíveis inputs para o tipo `date`.

**Tabela 8.10. Data de entrada**

<table>
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Example
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    1999-01-08
   </td>
   <td>
    ISO 8601; 8 de janeiro em qualquer modo (formato recomendado)
   </td>
  </tr>
  <tr>
   <td>
    January 8, 1999
   </td>
   <td>
    ambiguoso em qualquer
    <code>
     datestyle
    </code>
    modo de entrada
   </td>
  </tr>
  <tr>
   <td>
    1/8/1999
   </td>
   <td>
    8 de janeiro em
    <code>
     MDY
    </code>
    modo; 1º de agosto
    <code>
     DMY
    </code>
    modo
   </td>
  </tr>
  <tr>
   <td>
    1/18/1999
   </td>
   <td>
    18 de janeiro em
    <code>
     MDY
    </code>
    modo; rejeitado em outros modos
   </td>
  </tr>
  <tr>
   <td>
    01/02/03
   </td>
   <td>
    2 de janeiro de 2003 em
    <code>
     MDY
    </code>
    modo; 1 de fevereiro de 2003 em
    <code>
     DMY
    </code>
    modo; 3 de fevereiro de 2001 em
    <code>
     YMD
    </code>
    modo
   </td>
  </tr>
  <tr>
   <td>
    1999-Jan-08
   </td>
   <td>
    8 de janeiro em qualquer modo
   </td>
  </tr>
  <tr>
   <td>
    Jan-08-1999
   </td>
   <td>
    8 de janeiro em qualquer modo
   </td>
  </tr>
  <tr>
   <td>
    08-Jan-1999
   </td>
   <td>
    8 de janeiro em qualquer modo
   </td>
  </tr>
  <tr>
   <td>
    99-Jan-08
   </td>
   <td>
    8 de janeiro em
    <code>
     YMD
    </code>
    modo, caso contrário, erro
   </td>
  </tr>
  <tr>
   <td>
    08-Jan-99
   </td>
   <td>
    8 de janeiro, exceto erro em
    <code>
     YMD
    </code>
    modo
   </td>
  </tr>
  <tr>
   <td>
    Jan-08-99
   </td>
   <td>
    8 de janeiro, exceto erro em
    <code>
     YMD
    </code>
    modo
   </td>
  </tr>
  <tr>
   <td>
    19990108
   </td>
   <td>
    ISO 8601; 8 de janeiro de 1999 em qualquer modo
   </td>
  </tr>
  <tr>
   <td>
    990108
   </td>
   <td>
    ISO 8601; 8 de janeiro de 1999 em qualquer modo
   </td>
  </tr>
  <tr>
   <td>
    1999.008
   </td>
   <td>
    ano e dia do ano
   </td>
  </tr>
  <tr>
   <td>
    J2451187
   </td>
   <td>
    Data juliana
   </td>
  </tr>
  <tr>
   <td>
    January 8, 99 BC
   </td>
   <td>
    ano 99 a.C.
   </td>
  </tr>
 </tbody>
</table>

##### 8.5.1.2. Horários [#](#DATATYPE-DATETIME-INPUT-TIMES)

Os tipos de hora do dia são `time [ (p) ] without time zone` e `time [ (p) ] with time zone`. `time` sozinho é equivalente a `time without time zone`.

A entrada válida para esses tipos consiste em uma hora do dia seguida de um fuso horário opcional. (Veja [Tabela 8.11] (datatype-datetime.md#DATATYPE-DATETIME-TIME-TABLE "Table 8.11. Time Input") e [Tabela 8.12] (datatype-datetime.md#DATATYPE-TIMEZONE-TABLE "Table 8.12. Time Zone Input").). Se um fuso horário é especificado na entrada para `time without time zone`, ele é ignorado silenciosamente. Você também pode especificar uma data, mas ela será ignorada, exceto quando você usa um nome de fuso horário que envolva uma regra de mudança de hora, como `America/New_York`. Neste caso, especificar a data é necessário para determinar se o horário padrão ou o horário de verão se aplica. O deslocamento do fuso horário apropriado é registrado no valor `time with time zone` e é emitido como armazenado; ele não é ajustado para o fuso horário ativo.

**Tabela 8.11. Tempo de entrada**

<table>
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Example
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     04:05:06.789
    </code>
   </td>
   <td>
    ISO 8601
   </td>
  </tr>
  <tr>
   <td>
    <code>
     04:05:06
    </code>
   </td>
   <td>
    ISO 8601
   </td>
  </tr>
  <tr>
   <td>
    <code>
     04:05
    </code>
   </td>
   <td>
    ISO 8601
   </td>
  </tr>
  <tr>
   <td>
    <code>
     040506
    </code>
   </td>
   <td>
    ISO 8601
   </td>
  </tr>
  <tr>
   <td>
    <code>
     04:05 AM
    </code>
   </td>
   <td>
    mesmo que 04:05; AM não afeta o valor
   </td>
  </tr>
  <tr>
   <td>
    <code>
     04:05 PM
    </code>
   </td>
   <td>
    mesmo que às 16:05; a hora de entrada deve ser &lt;= 12
   </td>
  </tr>
  <tr>
   <td>
    <code>
     04:05:06.789-8
    </code>
   </td>
   <td>
    ISO 8601, com fuso horário como deslocamento UTC
   </td>
  </tr>
  <tr>
   <td>
    <code>
     04:05:06-08:00
    </code>
   </td>
   <td>
    ISO 8601, com fuso horário como deslocamento UTC
   </td>
  </tr>
  <tr>
   <td>
    <code>
     04:05-08:00
    </code>
   </td>
   <td>
    ISO 8601, com fuso horário como deslocamento UTC
   </td>
  </tr>
  <tr>
   <td>
    <code>
     040506-08
    </code>
   </td>
   <td>
    ISO 8601, com fuso horário como deslocamento UTC
   </td>
  </tr>
  <tr>
   <td>
    <code>
     040506+0730
    </code>
   </td>
   <td>
    ISO 8601, com fuso horário de hora fracionária como deslocamento UTC
   </td>
  </tr>
  <tr>
   <td>
    <code>
     040506+07:30:00
    </code>
   </td>
   <td>
    Deslocamento UTC especificado em segundos (não permitido no ISO 8601)
   </td>
  </tr>
  <tr>
   <td>
    <code>
     04:05:06 PST
    </code>
   </td>
   <td>
    fuso horário especificado por abreviação
   </td>
  </tr>
  <tr>
   <td>
    <code>
     2003-04-12 04:05:06 America/New_York
    </code>
   </td>
   <td>
    fuso horário especificado pelo nome completo
   </td>
  </tr>
 </tbody>
</table>

**Tabela 8.12. Entrada de fuso horário**

<table>
 <thead>
  <tr>
   <th>
    Example
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     PST
    </code>
   </td>
   <td>
    Abreviação (para Pacific Standard Time)
   </td>
  </tr>
  <tr>
   <td>
    <code>
     America/New_York
    </code>
   </td>
   <td>
    Nome completo do fuso horário
   </td>
  </tr>
  <tr>
   <td>
    <code>
     PST8PDT
    </code>
   </td>
   <td>
    Especificação de fuso horário em estilo POSIX
   </td>
  </tr>
  <tr>
   <td>
    <code>
     -8:00:00
    </code>
   </td>
   <td>
    Deslocamento UTC para PST
   </td>
  </tr>
  <tr>
   <td>
    <code>
     -8:00
    </code>
   </td>
   <td>
    Deslocamento UTC para PST (formato estendido ISO 8601)
   </td>
  </tr>
  <tr>
   <td>
    <code>
     -800
    </code>
   </td>
   <td>
    Deslocamento UTC para PST (formato básico ISO 8601)
   </td>
  </tr>
  <tr>
   <td>
    <code>
     -8
    </code>
   </td>
   <td>
    Deslocamento UTC para PST (formato básico ISO 8601)
   </td>
  </tr>
  <tr>
   <td>
    <code>
     zulu
    </code>
   </td>
   <td>
    Abreviação militar para UTC
   </td>
  </tr>
  <tr>
   <td>
    <code>
     z
    </code>
   </td>
   <td>
    Forma abreviada de
    <code>
     zulu
    </code>
    (também no ISO 8601)
   </td>
  </tr>
 </tbody>
</table>

Consulte [Seção 8.5.3](datatype-datetime.md#DATATYPE-TIMEZONES) para obter mais informações sobre como especificar fusos horários.

##### 8.5.1.3. Marcadores de tempo [#](#DATATYPE-DATETIME-INPUT-TIME-STAMPS)

A entrada válida para os tipos de marcação de tempo consiste na concatenação de uma data e uma hora, seguida de um fuso horário opcional, seguido de um `AD` ou `BC` opcional. (Alternativamente, `AD`/`BC` pode aparecer antes do fuso horário, mas essa não é a ordem preferida.) Assim:

```sql
1999-01-08 04:05:06
```

e:

```sql
1999-01-08 04:05:06 -8:00
```

são valores válidos, que seguem o padrão ISO 8601. Além disso, o formato comum:

```sql
January 8 04:05:06 1999 PST
```

é suportada.

O padrão SQL diferencia os literais `timestamp without time zone` e `timestamp with time zone` pela presença de um símbolo “+” ou “-” e do deslocamento do fuso horário após a hora. Portanto, de acordo com o padrão,

```sql
TIMESTAMP '2004-10-19 10:23:54'
```

é um `timestamp without time zone`, enquanto

```sql
TIMESTAMP '2004-10-19 10:23:54+02'
```

é um `timestamp with time zone`. O PostgreSQL nunca examina o conteúdo de uma string literal antes de determinar seu tipo, e, portanto, tratará os dois exemplos acima como `timestamp without time zone`. Para garantir que uma literal seja tratada como `timestamp with time zone`, dê a ela o tipo explícito correto:

```sql
TIMESTAMP WITH TIME ZONE '2004-10-19 10:23:54+02'
```

Em um valor que foi determinado como `timestamp without time zone`, o PostgreSQL ignorará silenciosamente qualquer indicação de fuso horário. Isso significa que o valor resultante é derivado dos campos de data/hora na string de entrada e não é ajustado para o fuso horário.

Para os valores de `timestamp with time zone`, uma string de entrada que inclui um fuso horário explícito será convertida para UTC ([*[Tempo Universal Coordenado](glossary.md#GLOSSARY-UTC "UTC")*](glossário.md#GLÓSSARIO-UTC)) usando o deslocamento apropriado para esse fuso horário. Se nenhuma zona horária for declarada na string de entrada, então é assumido que ela está na zona horária indicada pelo parâmetro de [TimeZone](runtime-config-client.md#GUC-TIMEZONE) do sistema, e é convertida para UTC usando o deslocamento para a zona de `timezone`. Em qualquer caso, o valor é armazenado internamente como UTC, e a zona horária originalmente declarada ou assumida não é retida.

Quando um valor de `timestamp with time zone` é exibido, ele é sempre convertido do UTC para a zona atual de `timezone` e exibido como hora local nessa zona. Para ver a hora em outra zona horária, altere `timezone` ou use a construção `AT TIME ZONE` (consulte [Seção 9.9.4](functions-datetime.md#FUNCTIONS-DATETIME-ZONECONVERT)).

As conversões entre `timestamp without time zone` e `timestamp with time zone` normalmente assumem que o valor do `timestamp without time zone` deve ser tomado ou fornecido como a hora local do `timezone`. Um fuso horário diferente pode ser especificado para a conversão usando `AT TIME ZONE`.

##### 8.5.1.4. Valores especiais [#](#DATATYPE-DATETIME-SPECIAL-VALUES)

O PostgreSQL suporta vários valores especiais de data/hora para conveniência, conforme mostrado na [Tabela 8.13](datatype-datetime.md#DATATYPE-DATETIME-SPECIAL-TABLE). Os valores (datatype-datetime.md#DATATYPE-DATETIME-SPECIAL-TABLE "Table 8.13. Special Date/Time Inputs") e [[PH_LNK_103]] são representados especialmente dentro do sistema e serão exibidos inalterados; mas os outros são simplesmente abreviações anotacionais que serão convertidas em valores normais de data/hora quando lidos. (Em particular, (datatype-datetime.md#DATATYPE-DATETIME-SPECIAL-TABLE "Table 8.13. Special Date/Time Inputs") e as strings relacionadas são convertidas em um valor específico de hora assim que são lidas.) Todos esses valores precisam ser fechados entre aspas quando usados como constantes em comandos SQL.

**Tabela 8.13. Datas/horários especiais**

<table>
 <colgroup>
  <col/>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Input String
   </th>
   <th>
    Tipos válidos
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     epoch
    </code>
   </td>
   <td>
    <code>
     date
    </code>
    ,
    <code>
     timestamp
    </code>
   </td>
   <td>
    1970-01-01 00:00:00+00 (horário do sistema Unix zero)
   </td>
  </tr>
  <tr>
   <td>
    <code>
     infinity
    </code>
   </td>
   <td>
    <code>
     date
    </code>
    ,
    <code>
     timestamp
    </code>
    ,
    <code>
     interval
    </code>
   </td>
   <td>
    mais tarde do que todos os outros marcadores de tempo
   </td>
  </tr>
  <tr>
   <td>
    <code>
     -infinity
    </code>
   </td>
   <td>
    <code>
     date
    </code>
    ,
    <code>
     timestamp
    </code>
    ,
    <code>
     interval
    </code>
   </td>
   <td>
    antes de todos os outros marcadores de tempo
   </td>
  </tr>
  <tr>
   <td>
    <code>
     now
    </code>
   </td>
   <td>
    <code>
     date
    </code>
    ,
    <code>
     time
    </code>
    ,
    <code>
     timestamp
    </code>
   </td>
   <td>
    horário de início da transação atual
   </td>
  </tr>
  <tr>
   <td>
    <code>
     today
    </code>
   </td>
   <td>
    <code>
     date
    </code>
    ,
    <code>
     timestamp
    </code>
   </td>
   <td>
    meia-noite (
    <code>
     00:00
    </code>
    ) de hoje
   </td>
  </tr>
  <tr>
   <td>
    <code>
     tomorrow
    </code>
   </td>
   <td>
    <code>
     date
    </code>
    ,
    <code>
     timestamp
    </code>
   </td>
   <td>
    meia-noite (
    <code>
     00:00
    </code>
    ) amanhã
   </td>
  </tr>
  <tr>
   <td>
    <code>
     yesterday
    </code>
   </td>
   <td>
    <code>
     date
    </code>
    ,
    <code>
     timestamp
    </code>
   </td>
   <td>
    meia-noite (
    <code>
     00:00
    </code>
    ) ontem
   </td>
  </tr>
  <tr>
   <td>
    <code>
     allballs
    </code>
   </td>
   <td>
    <code>
     time
    </code>
   </td>
   <td>
    00:00:00,00 UTC
   </td>
  </tr>
 </tbody>
</table>

As seguintes funções compatíveis com SQL também podem ser usadas para obter o valor da hora atual para o tipo de dados correspondente: `CURRENT_DATE`, `CURRENT_TIME`, `CURRENT_TIMESTAMP`, `LOCALTIME`, `LOCALTIMESTAMP`. (Veja [Seção 9.9.5](functions-datetime.md#FUNCTIONS-DATETIME-CURRENT). Observe que essas são funções SQL e *não* são reconhecidas em strings de entrada de dados.

Atenção

Embora as strings de entrada `now`, `today`, `tomorrow` e `yesterday` sejam adequadas para uso em comandos SQL interativos, elas podem apresentar comportamento surpreendente quando o comando é salvo para execução posterior, por exemplo, em declarações preparadas, visualizações e definições de funções. A string pode ser convertida em um valor de tempo específico que continua a ser usado mesmo após se tornar obsoleto. Use uma das funções SQL em vez disso, em tais contextos. Por exemplo, `CURRENT_DATE + 1` é mais seguro do que `'tomorrow'::date`.

#### 8.5.2. Saída de data/hora [#](#DATATYPE-DATETIME-OUTPUT)

O formato de saída dos tipos de data/hora pode ser definido como um dos quatro estilos ISO 8601, SQL (Ingres), tradicional POSTGRES (formato de data Unix) ou alemão. O padrão é o formato ISO. (O padrão SQL exige o uso do formato ISO 8601. O nome do formato de saída "SQL" é um acidente histórico.) [Tabela 8.14](datatype-datetime.md#DATATYPE-DATETIME-OUTPUT-TABLE "Table 8.14. Date/Time Output Styles") mostra exemplos de cada estilo de saída. A saída dos tipos `date` e `time` geralmente é apenas a parte de data ou hora de acordo com os exemplos fornecidos. No entanto, o estilo POSTGRES exibe valores apenas de data no formato ISO.

**Tabela 8.14. Estilos de saída de data/hora**

<table>
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
  <col class="col3"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Style Specification
   </th>
   <th>
    Description
   </th>
   <th>
    Exemplo
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     ISO
    </code>
   </td>
   <td>
    ISO 8601, SQL standard
   </td>
   <td>
    <code>
     1997-12-17 07:37:16-08
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     SQL
    </code>
   </td>
   <td>
    traditional style
   </td>
   <td>
    <code>
     12/17/1997 07:37:16.00 PST
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     Postgres
    </code>
   </td>
   <td>
    original style
   </td>
   <td>
    <code>
     Wed Dec 17 07:37:16 1997 PST
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     German
    </code>
   </td>
   <td>
    regional style
   </td>
   <td>
    <code>
     17.12.1997 07:37:16.00 PST
    </code>
   </td>
  </tr>
 </tbody>
</table>

Nota

A ISO 8601 especifica o uso da letra maiúscula `T` para separar a data e a hora. O PostgreSQL aceita esse formato na entrada, mas na saída ele usa um espaço em vez de `T`, como mostrado acima. Isso é para legibilidade e para consistência com [RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339), bem como em alguns outros sistemas de banco de dados.

Nos estilos SQL e POSTGRES, o dia aparece antes do mês se o campo de ordenação DMY tiver sido especificado, caso contrário, o mês aparece antes do dia. (Veja [Seção 8.5.1] para saber como essa configuração também afeta a interpretação dos valores de entrada. A [Tabela 8.15](datatype-datetime.md#DATATYPE-DATETIME-OUTPUT2-TABLE) mostra exemplos.)

**Tabela 8.15. Convenções de data de ordem**

<table>
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
  <col class="col3"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    <code>
     datestyle
    </code>
    Setting
   </th>
   <th>
    Input Ordering
   </th>
   <th>
    Exemplo de Saída
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     SQL, DMY
    </code>
   </td>
   <td>
    <em class="replaceable">
     <code>
      day
     </code>
    </em>
    /
    <em class="replaceable">
     <code>
      month
     </code>
    </em>
    /
    <em class="replaceable">
     <code>
      year
     </code>
    </em>
   </td>
   <td>
    <code>
     17/12/1997 15:37:16.00 CET
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     SQL, MDY
    </code>
   </td>
   <td>
    <em class="replaceable">
     <code>
      month
     </code>
    </em>
    /
    <em class="replaceable">
     <code>
      day
     </code>
    </em>
    /
    <em class="replaceable">
     <code>
      year
     </code>
    </em>
   </td>
   <td>
    <code>
     12/17/1997 07:37:16.00 PST
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     Postgres, DMY
    </code>
   </td>
   <td>
    <em class="replaceable">
     <code>
      day
     </code>
    </em>
    /
    <em class="replaceable">
     <code>
      month
     </code>
    </em>
    /
    <em class="replaceable">
     <code>
      year
     </code>
    </em>
   </td>
   <td>
    <code>
     Wed 17 Dec 07:37:16 1997 PST
    </code>
   </td>
  </tr>
 </tbody>
</table>

No estilo ISO, o fuso horário é sempre mostrado como um deslocamento numérico assinado em relação ao UTC, com sinal positivo usado para zonas a leste de Greenwich. O deslocamento será mostrado como *`hh`* (apenas horas) se for um número inteiro de horas, caso contrário como *`hh`*:*`mm`* se for um número inteiro de minutos, caso contrário como *`hh`*:*`mm`*:*`ss`*. (O terceiro caso não é possível com qualquer padrão moderno de fuso horário, mas pode aparecer ao trabalhar com timestamps que precedem a adoção de fusos horários padronizados.) Nos outros estilos de data, o fuso horário é mostrado como uma abreviação alfabética se uma estiver em uso comum na zona atual. Caso contrário, aparece como um deslocamento numérico assinado no formato básico do ISO (*`hh`* ou *`hhmm`*). As abreviações alfabéticas mostradas nesses estilos são retiradas da entrada do banco de dados de fuso horário da IANA atualmente selecionada pelo parâmetro de tempo de execução [TimeZone](runtime-config-client.md#GUC-TIMEZONE); elas não são afetadas pelo ajuste [timezone_abbreviations](runtime-config-client.md#GUC-TIMEZONE-ABBREVIATIONS).

O estilo de data/hora pode ser selecionado pelo usuário usando o comando `SET datestyle`, o parâmetro [DateStyle](runtime-config-client.md#GUC-DATESTYLE) no arquivo de configuração `postgresql.conf` ou a variável de ambiente `PGDATESTYLE` no servidor ou no cliente.

A função de formatação `to_char` (ver [Seção 9.8](functions-formatting.md)) também está disponível como uma maneira mais flexível de formatar a saída de data/hora.

#### 8.5.3. Fuso Horário [#](#DATATYPE-TIMEZONES)

Os fusos horários e as convenções horárias são influenciados por decisões políticas, não apenas pela geometria da Terra. Os fusos horários ao redor do mundo se tornaram um tanto padronizados durante a década de 1900, mas continuam a ser propensos a mudanças arbitrárias, especialmente em relação às regras de adiantamento de horas. O PostgreSQL utiliza o banco de dados de fuso horário IANA (Olson) amplamente utilizado para informações sobre regras históricas de fuso horário. Para os horários futuros, a suposição é que as regras mais recentes conhecidas para um determinado fuso horário continuarão a ser observadas indefinidamente no futuro.

O PostgreSQL se esforça para ser compatível com as definições padrão do SQL para uso típico. No entanto, o padrão SQL tem uma mistura estranha de tipos e capacidades de data e hora. Dois problemas óbvios são:

* Embora o tipo `date` não possa ter um fuso horário associado, o tipo `time` pode. Os fusos horários do mundo real têm pouco significado a menos que sejam associados a uma data, bem como a uma hora, uma vez que o deslocamento pode variar ao longo do ano com os limites dos horários de verão.
* O fuso horário padrão é especificado como um deslocamento numérico constante em relação ao UTC. Portanto, é impossível se adaptar ao horário de verão ao realizar cálculos de data/hora através dos limites do DST.

Para resolver essas dificuldades, recomendamos o uso de tipos de data/hora que contenham tanto data quanto hora ao usar zonas horárias. Não recomendamos o uso do tipo `time with time zone` (embora seja suportado pelo PostgreSQL para aplicações legadas e para conformidade com o padrão SQL). O PostgreSQL assume que sua zona horária local é usada para qualquer tipo que contenha apenas data ou hora.

Todas as datas e horários que consideram a fusão horária são armazenados internamente no UTC. Eles são convertidos para hora local na zona especificada pelo parâmetro de configuração [TimeZone](runtime-config-client.md#GUC-TIMEZONE) antes de serem exibidos ao cliente.

O PostgreSQL permite que você especifique fusos horários em três formas diferentes:

* Um nome de fuso horário completo, por exemplo, `America/New_York`. Os nomes de fuso horário reconhecidos estão listados na visão `pg_timezone_names` (ver [Seção 53.34](view-pg-timezone-names.md)). O PostgreSQL usa os dados de fuso horário amplamente utilizados pela IANA para esse propósito, portanto, os mesmos nomes de fuso horário são reconhecidos também por outros softwares.
* Uma abreviação de fuso horário, por exemplo, `PST`. Essa especificação simplesmente define um deslocamento particular em relação ao UTC, em contraste com os nomes de fuso horário completos que podem implicar um conjunto de regras de transição de poupança de luz solar. Os nomes reconhecidos estão listados na visão `pg_timezone_abbrevs` (ver [Seção 53.33](view-pg-timezone-abbrevs.md)). Você não pode definir os parâmetros de configuração [TimeZone](runtime-config-client.md#GUC-TIMEZONE) ou [log_timezone](runtime-config-logging.md#GUC-LOG-TIMEZONE) para uma abreviação de fuso horário, mas você pode usar abreviações em valores de entrada de data/hora e com o operador `AT TIME ZONE`.
* Além dos nomes e abreviações de fuso horário, o PostgreSQL aceitará especificações de fuso horário em estilo POSIX, conforme descrito em [Seção B.5](datetime-posix-timezone-specs.md). Esta opção normalmente não é preferível ao uso de um fuso horário nomeado, mas pode ser necessária se não houver uma entrada de fuso horário IANA adequada disponível.

Em suma, essa é a diferença entre abreviações e nomes completos: as abreviações representam um deslocamento específico em relação ao UTC, enquanto muitos dos nomes completos implicam uma regra local de horário de verão, e, portanto, têm dois deslocamentos possíveis em relação ao UTC. Como exemplo, `2014-06-04 12:00 America/New_York` representa a hora local do meio-dia em Nova York, que, para esta data específica, foi o Horário de Verão do Leste (UTC-4). Portanto, `2014-06-04 12:00 EDT` especifica o mesmo instante de tempo. Mas `2014-06-04 12:00 EST` especifica o meio-dia do Horário Padrão do Leste (UTC-5), independentemente de o horário de verão ter sido nominalmente em vigor nessa data.

Nota

O sinal nas especificações de fuso horário em estilo POSIX tem o significado oposto ao sinal nos valores de data e hora ISO-8601. Por exemplo, o fuso horário POSIX para `2014-06-04 12:00+04` seria UTC-4.

Para complicar ainda mais, algumas jurisdições usaram a mesma abreviação de fuso horário para significar diferentes deslocamentos UTC em diferentes momentos; por exemplo, em Moscou, `MSK` significou UTC+3 em alguns anos e UTC+4 em outros. O PostgreSQL interpreta tais abreviações de acordo com o que elas significaram (ou significaram mais recentemente) na data especificada; mas, como no exemplo `EST` acima, isso não é necessariamente o mesmo que o horário civil local naquela data.

Em todos os casos, os nomes e abreviações de fuso horário são reconhecidos de forma sensível ao caso (Essa é uma mudança em relação às versões do PostgreSQL anteriores a 8.2, que eram sensíveis ao caso em alguns contextos, mas não em outros).

Nem os nomes dos fusos horários nem as abreviações estão embutidos no servidor; eles são obtidos a partir de arquivos de configuração armazenados sob `.../share/timezone/` e `.../share/timezonesets/` do diretório de instalação (consulte [Seção B.4](datetime-config-files.md)).

O parâmetro de configuração [TimeZone](runtime-config-client.md#GUC-TIMEZONE) pode ser definido no arquivo `postgresql.conf`, ou de qualquer outra maneira padrão descrita em [Capítulo 19](runtime-config.md "Chapter 19. Server Configuration"). Há também algumas maneiras especiais de defini-lo:

* O comando SQL `SET TIME ZONE` define o fuso horário para a sessão. Esta é uma grafia alternativa de `SET TIMEZONE TO` com uma sintaxe mais compatível com o SQL.
* A variável de ambiente `PGTZ` é usada pelos clientes libpq para enviar um comando `SET TIME ZONE` ao servidor após a conexão.

#### 8.5.4. Entrada de intervalo [#](#DATATYPE-INTERVAL-INPUT)

Os valores de `interval` podem ser escritos usando a seguinte sintaxe verbose:

```sql
[@] quantity unit [quantity unit...] [direction]
```

onde *`quantity`* é um número (possível sinalizado); *`unit`* é `microsecond`, `millisecond`, `second`, `minute`, `hour`, `day`, `week`, `month`, `year`, `decade`, `century`, `millennium`, ou abreviações ou plurais dessas unidades; *`direction`* pode ser `ago` ou vazio. O sinal de aspas (`@`) é ruído opcional. As quantidades das diferentes unidades são adicionadas implicitamente com contabilidade de sinal apropriada. `ago` nega todos os campos. Essa sintaxe também é usada para saída de intervalo, se [IntervalStyle](runtime-config-client.md#GUC-INTERVALSTYLE) está definido como `postgres_verbose`.

As quantidades de dias, horas, minutos e segundos podem ser especificadas sem marcações explícitas de unidade. Por exemplo, `'1 12:59:10'` é lido da mesma forma que `'1 day 12 hours 59 min 10 sec'`. Além disso, uma combinação de anos e meses pode ser especificada com uma barra; por exemplo, `'200-10'` é lido da mesma forma que `'200 years 10 months'`. (Essas formas mais curtas são, de fato, as únicas permitidas pelo padrão SQL e são usadas para saída quando `IntervalStyle` é definido como `sql_standard`.)

Os valores de intervalo também podem ser escritos como intervalos de tempo ISO 8601, utilizando o "formato com designadores" da seção 4.4.3.2 do padrão ou o "formato alternativo" da seção 4.4.3.3. O formato com designadores tem a seguinte aparência:

```sql
P quantity unit [ quantity unit ...] [ T [ quantity unit ...]]
```

A string deve começar com um `P`, e pode incluir um `T` que introduz as unidades do horário. As abreviações de unidades disponíveis estão fornecidas na [Tabela 8.16](datatype-datetime.md#DATATYPE-INTERVAL-ISO8601-UNITS "Table 8.16. ISO 8601 Interval Unit Abbreviations"). As unidades podem ser omitidas e podem ser especificadas em qualquer ordem, mas as unidades menores que um dia devem aparecer após `T`. Em particular, o significado de `M` depende de ser antes ou depois de `T`.

**Tabela 8.16. Abreviações de unidades de intervalo ISO 8601**

<table>
 <thead>
  <tr>
   <th>
    Abbreviation
   </th>
   <th>
    Meaning
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    Y
   </td>
   <td>
    Years
   </td>
  </tr>
  <tr>
   <td>
    M
   </td>
   <td>
    Months (in the date part)
   </td>
  </tr>
  <tr>
   <td>
    W
   </td>
   <td>
    Weeks
   </td>
  </tr>
  <tr>
   <td>
    D
   </td>
   <td>
    Days
   </td>
  </tr>
  <tr>
   <td>
    H
   </td>
   <td>
    Hours
   </td>
  </tr>
  <tr>
   <td>
    M
   </td>
   <td>
    Minutes (in the time part)
   </td>
  </tr>
  <tr>
   <td>
    S
   </td>
   <td>
    Seconds
   </td>
  </tr>
 </tbody>
</table>

No formato alternativo:

```sql
P [ years-months-days ] [ T hours:minutes:seconds ]
```

a string deve começar com `P`, e um `T` separa as partes de data e hora do intervalo. Os valores são fornecidos como números semelhantes às datas do ISO 8601.

Ao escrever uma constante de intervalo com uma especificação *`fields`*, ou ao atribuir uma string a uma coluna de intervalo que foi definida com uma especificação *`fields`*, a interpretação das quantidades não marcadas depende do *`fields`*. Por exemplo, `INTERVAL '1' YEAR` é lido como 1 ano, enquanto `INTERVAL '1'` significa 1 segundo. Além disso, os valores dos campos “à direita” do campo menos significativo permitido pela especificação *`fields`* são silenciosamente descartados. Por exemplo, escrever `INTERVAL '1 day 2:03:04' HOUR TO MINUTE` resulta na eliminação do campo de segundos, mas não do campo de dia.

De acordo com o padrão SQL, todos os campos de um valor de intervalo devem ter o mesmo sinal, portanto, um sinal negativo inicial se aplica a todos os campos; por exemplo, o sinal negativo no literal de intervalo `'-1 2:03:04'` se aplica tanto às partes de dia quanto de hora/minuto/segundo. O PostgreSQL permite que os campos tenham sinais diferentes, e tradicionalmente trata cada campo na representação textual como independentemente sinalizado, de modo que a parte de hora/minuto/segundo é considerada positiva neste exemplo. Se `IntervalStyle` for definido como `sql_standard`, então um sinal inicial é considerado aplicável a todos os campos (mas apenas se não houver sinais adicionais). Caso contrário, é usada a interpretação tradicional do PostgreSQL. Para evitar ambiguidade, é recomendável anexar um sinal explícito a cada campo se qualquer campo for negativo.

Internamente, os valores de `interval` são armazenados como três campos inteiros: meses, dias e microsegundos. Esses campos são mantidos separados porque o número de dias em um mês varia, enquanto um dia pode ter 23 ou 25 horas, se houver uma transição de horário de verão. Uma string de entrada de intervalo que usa outras unidades é normalizada nesse formato e, em seguida, reconstruída de uma maneira padronizada para saída, por exemplo:

```sql
SELECT '2 years 15 months 100 weeks 99 hours 123456789 milliseconds'::interval;
               interval
---------------------------------------
 3 years 3 mons 700 days 133:17:36.789
```

Aqui, as semanas, que são entendidas como “7 dias”, foram mantidas separadas, enquanto as unidades de tempo menores e maiores foram combinadas e normalizadas.

Os valores dos campos de entrada podem ter partes fracionárias, por exemplo, `'1.5 weeks'` ou `'01:02:03.45'`. No entanto, porque `interval` armazena internamente apenas campos inteiros, os valores fracionários devem ser convertidos em unidades menores. As partes fracionárias de unidades maiores que meses são arredondadas para um número inteiro de meses, por exemplo, `'1.5 years'` se torna `'1 year 6 mons'`. As partes fracionárias de semanas e dias são calculadas para um número inteiro de dias e microsegundos, assumindo 30 dias por mês e 24 horas por dia, por exemplo, `'1.75 months'` se torna `1 mon 22 days 12:00:00`. Apenas segundos serão exibidos como fracionários na saída.

[Tabela 8.17](datatype-datetime.md#DATATYPE-INTERVAL-INPUT-EXAMPLES) mostra alguns exemplos de entrada válida do `interval`.

**Tabela 8.17. Entrada de intervalo**

<table>
 <thead>
  <tr>
   <th>
    Exemplo
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     1-2
    </code>
   </td>
   <td>
    Formato padrão do SQL: 1 ano e 2 meses
   </td>
  </tr>
  <tr>
   <td>
    <code>
     3 4:05:06
    </code>
   </td>
   <td>
    Formato padrão do SQL: 3 dias 4 horas 5 minutos 6 segundos
   </td>
  </tr>
  <tr>
   <td>
    <code>
     1 year 2 months 3 days 4 hours 5 minutes 6 seconds
    </code>
   </td>
   <td>
    Formato tradicional de Postgres: 1 ano 2 meses 3 dias 4 horas 5 minutos 6 segundos
   </td>
  </tr>
  <tr>
   <td>
    <code>
     P1Y2M3DT4H5M6S
    </code>
   </td>
   <td>
    ISO 8601
    <span class="quote">
     “
     <span class="quote">
      formato com designadores
     </span>
     ”
    </span>
    : o mesmo significado que acima
   </td>
  </tr>
  <tr>
   <td>
    <code>
     P0001-02-03T04:05:06
    </code>
   </td>
   <td>
    ISO 8601
    <span class="quote">
     “
     <span class="quote">
      formato alternativo
     </span>
     ”
    </span>
    : o mesmo significado que acima
   </td>
  </tr>
 </tbody>
</table>

#### 8.5.5. Saída de intervalo [#](#DATATYPE-INTERVAL-OUTPUT)

Como explicado anteriormente, o PostgreSQL armazena os valores `interval` em meses, dias e microsegundos. Para a saída, o campo meses é convertido em anos e meses dividindo por 12. O campo dias é mostrado como está. O campo microsegundos é convertido em horas, minutos, segundos e segundos fracionários. Assim, meses, minutos e segundos nunca serão mostrados excedendo os intervalos 0–11, 0–59 e 30–59, respectivamente, enquanto os campos anos, dias e horas exibidos podem ser bastante grandes. (As funções `justify_days` e (functions-datetime.md#FUNCTION-JUSTIFY-DAYS) e `justify_hours` podem ser usadas se for desejável transpô-los grandes valores de dias ou horas para o campo da próxima categoria superior.)

O formato de saída do tipo de intervalo pode ser definido como um dos quatro estilos `sql_standard`, `postgres`, `postgres_verbose` ou `iso_8601`, usando o comando `SET intervalstyle`. O padrão é o formato `postgres`. [Tabela 8.18](datatype-datetime.md#INTERVAL-STYLE-OUTPUT-TABLE "Table 8.18. Interval Output Style Examples") mostra exemplos de cada estilo de saída.

O estilo `sql_standard` produz uma saída que se conforma à especificação do padrão SQL para intervalos literais, se o valor do intervalo atender às restrições do padrão (ou seja, apenas ano-mês ou apenas dia-hora, sem mistura de componentes positivos e negativos). Caso contrário, a saída parece uma string literal padrão ano-mês seguida de uma string literal dia-hora, com sinais explícitos adicionados para desambiguar intervalos de sinal misto.

A saída do estilo `postgres` corresponde à saída dos lançamentos do PostgreSQL anteriores à versão 8.4, quando o parâmetro [DateStyle](runtime-config-client.md#GUC-DATESTYLE) estava definido como `ISO`.

A saída do estilo `postgres_verbose` corresponde à saída dos lançamentos do PostgreSQL anteriores à versão 8.4, quando o parâmetro `DateStyle` estava configurado para saída não `ISO`.

A saída do estilo `iso_8601` corresponde ao "formato com designações" descrito na seção 4.4.3.2 da norma ISO 8601.

**Tabela 8.18. Exemplos de estilo de saída de intervalo**

<table>
 <colgroup>
  <col/>
  <col/>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Style Specification
   </th>
   <th>
    Intervalo de Ano-Mês
   </th>
   <th>
    Intervalo diurno
   </th>
   <th>
    Intervalo misto
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     sql_standard
    </code>
   </td>
   <td>
    1-2
   </td>
   <td>
    3 4:05:06
   </td>
   <td>
    -1-2 +3 -4:05:06
   </td>
  </tr>
  <tr>
   <td>
    <code>
     postgres
    </code>
   </td>
   <td>
    1 ano e 2 meses
   </td>
   <td>
    3 dias 04:05:06
   </td>
   <td>
    -1 ano -2 meses +3 dias -04:05:06
   </td>
  </tr>
  <tr>
   <td>
    <code>
     postgres_verbose
    </code>
   </td>
   <td>
    @ 1 ano e 2 meses
   </td>
   <td>
    @ 3 dias 4 horas 5 mins 6 secs
   </td>
   <td>
    @ 1 ano e 2 meses -3 dias 4 horas 5 minutos 6 segundos atrás
   </td>
  </tr>
  <tr>
   <td>
    <code>
     iso_8601
    </code>
   </td>
   <td>
    P1Y2M
   </td>
   <td>
    P3DT4H5M6S
   </td>
   <td>
    P-1Y-2M3D​T-4H-5M-6S
   </td>
  </tr>
 </tbody>
</table>

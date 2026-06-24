## 9.9. Funções e operadores de data/hora [#](#FUNCTIONS-DATETIME)

* [9.9.1. `EXTRACT`, `date_part`](functions-datetime.md#FUNCTIONS-DATETIME-EXTRACT)
* [9.9.2. `date_trunc`](functions-datetime.md#FUNCTIONS-DATETIME-TRUNC)
* [9.9.3. `date_bin`](functions-datetime.md#FUNCTIONS-DATETIME-BIN)
* [9.9.4. `AT TIME ZONE` e `AT LOCAL`](functions-datetime.md#FUNCTIONS-DATETIME-ZONECONVERT)
* [9.9.5. Data/Hora Atual](functions-datetime.md#FUNCTIONS-DATETIME-CURRENT)
* [9.9.6. Atrasos na Execução](functions-datetime.md#FUNCTIONS-DATETIME-DELAY)

[Tabela 9.33](functions-datetime.md#FUNCTIONS-DATETIME-TABLE "Table 9.33. Date/Time Functions") mostra as funções disponíveis para o processamento de valores de data/hora, com detalhes aparecendo nas seções a seguir. [Tabela 9.32](functions-datetime.md#OPERATORS-DATETIME-TABLE "Table 9.32. Date/Time Operators") ilustra os comportamentos dos operadores aritméticos básicos (`+`, `*`, etc.). Para funções de formatação, consulte [Seção 9.8](functions-formatting.md "9.8. Data Type Formatting Functions"). Você deve estar familiarizado com as informações de fundo sobre os tipos de dados de data/hora de [Seção 8.5](datatype-datetime.md "8.5. Date/Time Types").

Além disso, os operadores de comparação comuns mostrados em [Tabela 9.1](functions-comparison.md#FUNCTIONS-COMPARISON-OP-TABLE) estão disponíveis para os tipos de data/hora. Datas e timestamps (com ou sem fuso horário) são todos comparáveis, enquanto horários (com ou sem fuso horário) e intervalos só podem ser comparados com outros valores do mesmo tipo de dados. Ao comparar um timestamp sem fuso horário com um timestamp com fuso horário, o valor anterior é assumido como sendo dado no fuso horário especificado pelo parâmetro de configuração [TimeZone](runtime-config-client.md#GUC-TIMEZONE), e é rotacionado para UTC para comparação com o valor posterior (que já está em UTC internamente). Da mesma forma, um valor de data é assumido para representar a meia-noite na zona `TimeZone` ao compará-lo com um timestamp.

Todas as funções e operadores descritos abaixo que recebem entradas de `time` ou `timestamp` são, na verdade, apresentados em duas variantes: uma que recebe `time with time zone` ou `timestamp with time zone`, e outra que recebe `time without time zone` ou `timestamp without time zone`. Por economia de espaço, essas variantes não são mostradas separadamente. Além disso, os operadores `+` e `*` são apresentados em pares compostos (por exemplo, tanto `date` `+` `integer` quanto `integer` `+` `date`); mostramos apenas um de cada par desse tipo.

**Tabela 9.32. Operadores de data/hora**



<table border="1" class="table" summary="Date/Time Operators">
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Operador
    </p>
    <p>
     Descrição
    </p>
    <p>
     Exemplo(s)
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      date
     </code>
     <code class="literal">
      +
     </code>
     <code class="type">
      integer
     </code>
     →
     <code class="returnvalue">
      date
     </code>
    </p>
    <p>
     Adicione um número de dias a uma data
    </p>
    <p>
     <code class="literal">
      date '2001-09-28' + 7
     </code>
     →
     <code class="returnvalue">
      2001-10-05
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      date
     </code>
     <code class="literal">
      +
     </code>
     <code class="type">
      interval
     </code>
     →
     <code class="returnvalue">
      timestamp
     </code>
    </p>
    <p>
     Adicione um intervalo a uma data
    </p>
    <p>
     <code class="literal">
      date '2001-09-28' + interval '1 hour'
     </code>
     →
     <code class="returnvalue">
      2001-09-28 01:00:00
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      date
     </code>
     <code class="literal">
      +
     </code>
     <code class="type">
      time
     </code>
     →
     <code class="returnvalue">
      timestamp
     </code>
    </p>
    <p>
     Adicione um horário a uma data
    </p>
    <p>
     <code class="literal">
      date '2001-09-28' + time '03:00'
     </code>
     →
     <code class="returnvalue">
      2001-09-28 03:00:00
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      interval
     </code>
     <code class="literal">
      +
     </code>
     <code class="type">
      interval
     </code>
     →
     <code class="returnvalue">
      interval
     </code>
    </p>
    <p>
     Adicione intervalos
    </p>
    <p>
     <code class="literal">
      interval '1 day' + interval '1 hour'
     </code>
     →
     <code class="returnvalue">
      1 day 01:00:00
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      timestamp
     </code>
     <code class="literal">
      +
     </code>
     <code class="type">
      interval
     </code>
     →
     <code class="returnvalue">
      timestamp
     </code>
    </p>
    <p>
     Adicione um intervalo a um timestamp
    </p>
    <p>
     <code class="literal">
      timestamp '2001-09-28 01:00' + interval '23 hours'
     </code>
     →
     <code class="returnvalue">
      2001-09-29 00:00:00
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      time
     </code>
     <code class="literal">
      +
     </code>
     <code class="type">
      interval
     </code>
     →
     <code class="returnvalue">
      time
     </code>
    </p>
    <p>
     Adicione um intervalo a um horário
    </p>
    <p>
     <code class="literal">
      time '01:00' + interval '3 hours'
     </code>
     →
     <code class="returnvalue">
      04:00:00
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="literal">
      -
     </code>
     <code class="type">
      interval
     </code>
     →
     <code class="returnvalue">
      interval
     </code>
    </p>
    <p>
     Negar um intervalo
    </p>
    <p>
     <code class="literal">
      - interval '23 hours'
     </code>
     →
     <code class="returnvalue">
      -23:00:00
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      date
     </code>
     <code class="literal">
      -
     </code>
     <code class="type">
      date
     </code>
     →
     <code class="returnvalue">
      integer
     </code>
    </p>
    <p>
     Subtraia as datas, produzindo o número de dias que se passaram
    </p>
    <p>
     <code class="literal">
      date '2001-10-01' - date '2001-09-28'
     </code>
     →
     <code class="returnvalue">
      3
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      date
     </code>
     <code class="literal">
      -
     </code>
     <code class="type">
      integer
     </code>
     →
     <code class="returnvalue">
      date
     </code>
    </p>
    <p>
     Subtraia um número de dias de uma data
    </p>
    <p>
     <code class="literal">
      date '2001-10-01' - 7
     </code>
     →
     <code class="returnvalue">
      2001-09-24
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      date
     </code>
     <code class="literal">
      -
     </code>
     <code class="type">
      interval
     </code>
     →
     <code class="returnvalue">
      timestamp
     </code>
    </p>
    <p>
     Subtrair um intervalo de uma data
    </p>
    <p>
     <code class="literal">
      date '2001-09-28' - interval '1 hour'
     </code>
     →
     <code class="returnvalue">
      2001-09-27 23:00:00
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      time
     </code>
     <code class="literal">
      -
     </code>
     <code class="type">
      time
     </code>
     →
     <code class="returnvalue">
      interval
     </code>
    </p>
    <p>
     Subtraia os tempos
    </p>
    <p>
     <code class="literal">
      time '05:00' - time '03:00'
     </code>
     →
     <code class="returnvalue">
      02:00:00
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      time
     </code>
     <code class="literal">
      -
     </code>
     <code class="type">
      interval
     </code>
     →
     <code class="returnvalue">
      time
     </code>
    </p>
    <p>
     Subtrair um intervalo de um horário
    </p>
    <p>
     <code class="literal">
      time '05:00' - interval '2 hours'
     </code>
     →
     <code class="returnvalue">
      03:00:00
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      timestamp
     </code>
     <code class="literal">
      -
     </code>
     <code class="type">
      interval
     </code>
     →
     <code class="returnvalue">
      timestamp
     </code>
    </p>
    <p>
     Subtrair um intervalo de um timestamp
    </p>
    <p>
     <code class="literal">
      timestamp '2001-09-28 23:00' - interval '23 hours'
     </code>
     →
     <code class="returnvalue">
      2001-09-28 00:00:00
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      interval
     </code>
     <code class="literal">
      -
     </code>
     <code class="type">
      interval
     </code>
     →
     <code class="returnvalue">
      interval
     </code>
    </p>
    <p>
     Subtraia intervalos
    </p>
    <p>
     <code class="literal">
      interval '1 day' - interval '1 hour'
     </code>
     →
     <code class="returnvalue">
      1 day -01:00:00
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      timestamp
     </code>
     <code class="literal">
      -
     </code>
     <code class="type">
      timestamp
     </code>
     →
     <code class="returnvalue">
      interval
     </code>
    </p>
    <p>
     Subtraia os timestamps (convertendo intervalos de 24 horas em dias, de forma semelhante a
     <a class="link" href="functions-datetime.md#FUNCTION-JUSTIFY-HOURS">
      <code class="function">
       justify_hours()
      </code>
     </a>
     )
    </p>
    <p>
     <code class="literal">
      timestamp '2001-09-29 03:00' - timestamp '2001-07-27 12:00'
     </code>
     →
     <code class="returnvalue">
      63 days 15:00:00
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      interval
     </code>
     <code class="literal">
      *
     </code>
     <code class="type">
      double precision
     </code>
     →
     <code class="returnvalue">
      interval
     </code>
    </p>
    <p>
     Multiplicar um intervalo por um escalar
    </p>
    <p>
     <code class="literal">
      interval '1 second' * 900
     </code>
     →
     <code class="returnvalue">
      00:15:00
     </code>
    </p>
    <p>
     <code class="literal">
      interval '1 day' * 21
     </code>
     →
     <code class="returnvalue">
      21 days
     </code>
    </p>
    <p>
     <code class="literal">
      interval '1 hour' * 3.5
     </code>
     →
     <code class="returnvalue">
      03:30:00
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      interval
     </code>
     <code class="literal">
      /
     </code>
     <code class="type">
      double precision
     </code>
     →
     <code class="returnvalue">
      interval
     </code>
    </p>
    <p>
     Dividir um intervalo por um escalar
    </p>
    <p>
     <code class="literal">
      interval '1 hour' / 1.5
     </code>
     →
     <code class="returnvalue">
      00:40:00
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>










**Tabela 9.33. Funções de data/hora**



<table border="1" class="table" summary="Date/Time Functions">
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Function
    </p>
    <p>
     Description
    </p>
    <p>
     Example(s)
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      age
     </code>
     (
     <code class="type">
      timestamp
     </code>
     ,
     <code class="type">
      timestamp
     </code>
     ) →
     <code class="returnvalue">
      interval
     </code>
    </p>
    <p>
     Subtract arguments, producing a
     <span class="quote">
      “
      <span class="quote">
       symbolic
      </span>
      ”
     </span>
     result that uses years and months, rather than just days
    </p>
    <p>
     <code class="literal">
      age(timestamp '2001-04-10', timestamp '1957-06-13')
     </code>
     →
     <code class="returnvalue">
      43 years 9 mons 27 days
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      age
     </code>
     (
     <code class="type">
      timestamp
     </code>
     ) →
     <code class="returnvalue">
      interval
     </code>
    </p>
    <p>
     Subtract argument from
     <code class="function">
      current_date
     </code>
     (at midnight)
    </p>
    <p>
     <code class="literal">
      age(timestamp '1957-06-13')
     </code>
     →
     <code class="returnvalue">
      62 years 6 mons 10 days
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      clock_timestamp
     </code>
     ( ) →
     <code class="returnvalue">
      timestamp with time zone
     </code>
    </p>
    <p>
     Current date and time (changes during statement execution); see
     <a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-CURRENT" title="9.9.5. Current Date/Time">
      Section 9.9.5
     </a>
    </p>
    <p>
     <code class="literal">
      clock_timestamp()
     </code>
     →
     <code class="returnvalue">
      2019-12-23 14:39:53.662522-05
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      current_date
     </code>
     →
     <code class="returnvalue">
      date
     </code>
    </p>
    <p>
     Current date; see
     <a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-CURRENT" title="9.9.5. Current Date/Time">
      Section 9.9.5
     </a>
    </p>
    <p>
     <code class="literal">
      current_date
     </code>
     →
     <code class="returnvalue">
      2019-12-23
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      current_time
     </code>
     →
     <code class="returnvalue">
      time with time zone
     </code>
    </p>
    <p>
     Current time of day; see
     <a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-CURRENT" title="9.9.5. Current Date/Time">
      Section 9.9.5
     </a>
    </p>
    <p>
     <code class="literal">
      current_time
     </code>
     →
     <code class="returnvalue">
      14:39:53.662522-05
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      current_time
     </code>
     (
     <code class="type">
      integer
     </code>
     ) →
     <code class="returnvalue">
      time with time zone
     </code>
    </p>
    <p>
     Current time of day, with limited precision; see
     <a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-CURRENT" title="9.9.5. Current Date/Time">
      Section 9.9.5
     </a>
    </p>
    <p>
     <code class="literal">
      current_time(2)
     </code>
     →
     <code class="returnvalue">
      14:39:53.66-05
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      current_timestamp
     </code>
     →
     <code class="returnvalue">
      timestamp with time zone
     </code>
    </p>
    <p>
     Current date and time (start of current transaction); see
     <a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-CURRENT" title="9.9.5. Current Date/Time">
      Section 9.9.5
     </a>
    </p>
    <p>
     <code class="literal">
      current_timestamp
     </code>
     →
     <code class="returnvalue">
      2019-12-23 14:39:53.662522-05
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      current_timestamp
     </code>
     (
     <code class="type">
      integer
     </code>
     ) →
     <code class="returnvalue">
      timestamp with time zone
     </code>
    </p>
    <p>
     Current date and time (start of current transaction), with limited precision; see
     <a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-CURRENT" title="9.9.5. Current Date/Time">
      Section 9.9.5
     </a>
    </p>
    <p>
     <code class="literal">
      current_timestamp(0)
     </code>
     →
     <code class="returnvalue">
      2019-12-23 14:39:53-05
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      date_add
     </code>
     (
     <code class="type">
      timestamp with time zone
     </code>
     ,
     <code class="type">
      interval
     </code>
     [
     <span class="optional">
      ,
      <code class="type">
       text
      </code>
     </span>
     ] ) →
     <code class="returnvalue">
      timestamp with time zone
     </code>
    </p>
    <p>
     Add an
     <code class="type">
      interval
     </code>
     to a
     <code class="type">
      timestamp with time zone
     </code>
     , computing times of day and daylight-savings adjustments according to the time zone named by the third argument, or the current
     <a class="xref" href="runtime-config-client.md#GUC-TIMEZONE">
      TimeZone
     </a>
     setting if that is omitted. The form with two arguments is equivalent to the
     <code class="type">
      timestamp with time zone
     </code>
     <code class="literal">
      +
     </code>
     <code class="type">
      interval
     </code>
     operator.
    </p>
    <p>
     <code class="literal">
      date_add('2021-10-31 00:00:00+02'::timestamptz, '1 day'::interval, 'Europe/Warsaw')
     </code>
     →
     <code class="returnvalue">
      2021-10-31 23:00:00+00
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      date_bin
     </code>
     (
     <code class="type">
      interval
     </code>
     ,
     <code class="type">
      timestamp
     </code>
     ,
     <code class="type">
      timestamp
     </code>
     ) →
     <code class="returnvalue">
      timestamp
     </code>
    </p>
    <p>
     Bin input into specified interval aligned with specified origin; see
     <a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-BIN" title="9.9.3. date_bin">
      Section 9.9.3
     </a>
    </p>
    <p>
     <code class="literal">
      date_bin('15 minutes', timestamp '2001-02-16 20:38:40', timestamp '2001-02-16 20:05:00')
     </code>
     →
     <code class="returnvalue">
      2001-02-16 20:35:00
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      date_part
     </code>
     (
     <code class="type">
      text
     </code>
     ,
     <code class="type">
      timestamp
     </code>
     ) →
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Get timestamp subfield (equivalent to
     <code class="function">
      extract
     </code>
     ); see
     <a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-EXTRACT" title="9.9.1. EXTRACT, date_part">
      Section 9.9.1
     </a>
    </p>
    <p>
     <code class="literal">
      date_part('hour', timestamp '2001-02-16 20:38:40')
     </code>
     →
     <code class="returnvalue">
      20
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      date_part
     </code>
     (
     <code class="type">
      text
     </code>
     ,
     <code class="type">
      interval
     </code>
     ) →
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Get interval subfield (equivalent to
     <code class="function">
      extract
     </code>
     ); see
     <a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-EXTRACT" title="9.9.1. EXTRACT, date_part">
      Section 9.9.1
     </a>
    </p>
    <p>
     <code class="literal">
      date_part('month', interval '2 years 3 months')
     </code>
     →
     <code class="returnvalue">
      3
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      date_subtract
     </code>
     (
     <code class="type">
      timestamp with time zone
     </code>
     ,
     <code class="type">
      interval
     </code>
     [
     <span class="optional">
      ,
      <code class="type">
       text
      </code>
     </span>
     ] ) →
     <code class="returnvalue">
      timestamp with time zone
     </code>
    </p>
    <p>
     Subtract an
     <code class="type">
      interval
     </code>
     from a
     <code class="type">
      timestamp with time zone
     </code>
     , computing times of day and daylight-savings adjustments according to the time zone named by the third argument, or the current
     <a class="xref" href="runtime-config-client.md#GUC-TIMEZONE">
      TimeZone
     </a>
     setting if that is omitted. The form with two arguments is equivalent to the
     <code class="type">
      timestamp with time zone
     </code>
     <code class="literal">
      -
     </code>
     <code class="type">
      interval
     </code>
     operator.
    </p>
    <p>
     <code class="literal">
      date_subtract('2021-11-01 00:00:00+01'::timestamptz, '1 day'::interval, 'Europe/Warsaw')
     </code>
     →
     <code class="returnvalue">
      2021-10-30 22:00:00+00
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      date_trunc
     </code>
     (
     <code class="type">
      text
     </code>
     ,
     <code class="type">
      timestamp
     </code>
     ) →
     <code class="returnvalue">
      timestamp
     </code>
    </p>
    <p>
     Truncate to specified precision; see
     <a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-TRUNC" title="9.9.2. date_trunc">
      Section 9.9.2
     </a>
    </p>
    <p>
     <code class="literal">
      date_trunc('hour', timestamp '2001-02-16 20:38:40')
     </code>
     →
     <code class="returnvalue">
      2001-02-16 20:00:00
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      date_trunc
     </code>
     (
     <code class="type">
      text
     </code>
     ,
     <code class="type">
      timestamp with time zone
     </code>
     ,
     <code class="type">
      text
     </code>
     ) →
     <code class="returnvalue">
      timestamp with time zone
     </code>
    </p>
    <p>
     Truncate to specified precision in the specified time zone; see
     <a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-TRUNC" title="9.9.2. date_trunc">
      Section 9.9.2
     </a>
    </p>
    <p>
     <code class="literal">
      date_trunc('day', timestamptz '2001-02-16 20:38:40+00', 'Australia/Sydney')
     </code>
     →
     <code class="returnvalue">
      2001-02-16 13:00:00+00
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      date_trunc
     </code>
     (
     <code class="type">
      text
     </code>
     ,
     <code class="type">
      interval
     </code>
     ) →
     <code class="returnvalue">
      interval
     </code>
    </p>
    <p>
     Truncate to specified precision; see
     <a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-TRUNC" title="9.9.2. date_trunc">
      Section 9.9.2
     </a>
    </p>
    <p>
     <code class="literal">
      date_trunc('hour', interval '2 days 3 hours 40 minutes')
     </code>
     →
     <code class="returnvalue">
      2 days 03:00:00
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      extract
     </code>
     (
     <em class="parameter">
      <code>
       field
      </code>
     </em>
     <code class="literal">
      from
     </code>
     <code class="type">
      timestamp
     </code>
     ) →
     <code class="returnvalue">
      numeric
     </code>
    </p>
    <p>
     Get timestamp subfield; see
     <a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-EXTRACT" title="9.9.1. EXTRACT, date_part">
      Section 9.9.1
     </a>
    </p>
    <p>
     <code class="literal">
      extract(hour from timestamp '2001-02-16 20:38:40')
     </code>
     →
     <code class="returnvalue">
      20
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      extract
     </code>
     (
     <em class="parameter">
      <code>
       field
      </code>
     </em>
     <code class="literal">
      from
     </code>
     <code class="type">
      interval
     </code>
     ) →
     <code class="returnvalue">
      numeric
     </code>
    </p>
    <p>
     Get interval subfield; see
     <a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-EXTRACT" title="9.9.1. EXTRACT, date_part">
      Section 9.9.1
     </a>
    </p>
    <p>
     <code class="literal">
      extract(month from interval '2 years 3 months')
     </code>
     →
     <code class="returnvalue">
      3
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      isfinite
     </code>
     (
     <code class="type">
      date
     </code>
     ) →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Test for finite date (not +/-infinity)
    </p>
    <p>
     <code class="literal">
      isfinite(date '2001-02-16')
     </code>
     →
     <code class="returnvalue">
      true
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      isfinite
     </code>
     (
     <code class="type">
      timestamp
     </code>
     ) →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Test for finite timestamp (not +/-infinity)
    </p>
    <p>
     <code class="literal">
      isfinite(timestamp 'infinity')
     </code>
     →
     <code class="returnvalue">
      false
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      isfinite
     </code>
     (
     <code class="type">
      interval
     </code>
     ) →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Test for finite interval (not +/-infinity)
    </p>
    <p>
     <code class="literal">
      isfinite(interval '4 hours')
     </code>
     →
     <code class="returnvalue">
      true
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      justify_days
     </code>
     (
     <code class="type">
      interval
     </code>
     ) →
     <code class="returnvalue">
      interval
     </code>
    </p>
    <p>
     Adjust interval, converting 30-day time periods to months
    </p>
    <p>
     <code class="literal">
      justify_days(interval '1 year 65 days')
     </code>
     →
     <code class="returnvalue">
      1 year 2 mons 5 days
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      justify_hours
     </code>
     (
     <code class="type">
      interval
     </code>
     ) →
     <code class="returnvalue">
      interval
     </code>
    </p>
    <p>
     Adjust interval, converting 24-hour time periods to days
    </p>
    <p>
     <code class="literal">
      justify_hours(interval '50 hours 10 minutes')
     </code>
     →
     <code class="returnvalue">
      2 days 02:10:00
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      justify_interval
     </code>
     (
     <code class="type">
      interval
     </code>
     ) →
     <code class="returnvalue">
      interval
     </code>
    </p>
    <p>
     Adjust interval using
     <code class="function">
      justify_days
     </code>
     and
     <code class="function">
      justify_hours
     </code>
     , with additional sign adjustments
    </p>
    <p>
     <code class="literal">
      justify_interval(interval '1 mon -1 hour')
     </code>
     →
     <code class="returnvalue">
      29 days 23:00:00
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      localtime
     </code>
     →
     <code class="returnvalue">
      time
     </code>
    </p>
    <p>
     Current time of day; see
     <a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-CURRENT" title="9.9.5. Current Date/Time">
      Section 9.9.5
     </a>
    </p>
    <p>
     <code class="literal">
      localtime
     </code>
     →
     <code class="returnvalue">
      14:39:53.662522
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      localtime
     </code>
     (
     <code class="type">
      integer
     </code>
     ) →
     <code class="returnvalue">
      time
     </code>
    </p>
    <p>
     Current time of day, with limited precision; see
     <a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-CURRENT" title="9.9.5. Current Date/Time">
      Section 9.9.5
     </a>
    </p>
    <p>
     <code class="literal">
      localtime(0)
     </code>
     →
     <code class="returnvalue">
      14:39:53
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      localtimestamp
     </code>
     →
     <code class="returnvalue">
      timestamp
     </code>
    </p>
    <p>
     Current date and time (start of current transaction); see
     <a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-CURRENT" title="9.9.5. Current Date/Time">
      Section 9.9.5
     </a>
    </p>
    <p>
     <code class="literal">
      localtimestamp
     </code>
     →
     <code class="returnvalue">
      2019-12-23 14:39:53.662522
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      localtimestamp
     </code>
     (
     <code class="type">
      integer
     </code>
     ) →
     <code class="returnvalue">
      timestamp
     </code>
    </p>
    <p>
     Current date and time (start of current transaction), with limited precision; see
     <a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-CURRENT" title="9.9.5. Current Date/Time">
      Section 9.9.5
     </a>
    </p>
    <p>
     <code class="literal">
      localtimestamp(2)
     </code>
     →
     <code class="returnvalue">
      2019-12-23 14:39:53.66
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      make_date
     </code>
     (
     <em class="parameter">
      <code>
       year
      </code>
     </em>
     <code class="type">
      int
     </code>
     ,
     <em class="parameter">
      <code>
       month
      </code>
     </em>
     <code class="type">
      int
     </code>
     ,
     <em class="parameter">
      <code>
       day
      </code>
     </em>
     <code class="type">
      int
     </code>
     ) →
     <code class="returnvalue">
      date
     </code>
    </p>
    <p>
     Create date from year, month and day fields (negative years signify BC)
    </p>
    <p>
     <code class="literal">
      make_date(2013, 7, 15)
     </code>
     →
     <code class="returnvalue">
      2013-07-15
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      make_interval
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        years
       </code>
      </em>
      <code class="type">
       int
      </code>
      [
      <span class="optional">
       ,
       <em class="parameter">
        <code>
         months
        </code>
       </em>
       <code class="type">
        int
       </code>
       [
       <span class="optional">
        ,
        <em class="parameter">
         <code>
          weeks
         </code>
        </em>
        <code class="type">
         int
        </code>
        [
        <span class="optional">
         ,
         <em class="parameter">
          <code>
           days
          </code>
         </em>
         <code class="type">
          int
         </code>
         [
         <span class="optional">
          ,
          <em class="parameter">
           <code>
            hours
           </code>
          </em>
          <code class="type">
           int
          </code>
          [
          <span class="optional">
           ,
           <em class="parameter">
            <code>
             mins
            </code>
           </em>
           <code class="type">
            int
           </code>
           [
           <span class="optional">
            ,
            <em class="parameter">
             <code>
              secs
             </code>
            </em>
            <code class="type">
             double precision
            </code>
           </span>
           ]
          </span>
          ]
         </span>
         ]
        </span>
        ]
       </span>
       ]
      </span>
      ]
     </span>
     ] ) →
     <code class="returnvalue">
      interval
     </code>
    </p>
    <p>
     Create interval from years, months, weeks, days, hours, minutes and seconds fields, each of which can default to zero
    </p>
    <p>
     <code class="literal">
      make_interval(days =&gt; 10)
     </code>
     →
     <code class="returnvalue">
      10 days
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      make_time
     </code>
     (
     <em class="parameter">
      <code>
       hour
      </code>
     </em>
     <code class="type">
      int
     </code>
     ,
     <em class="parameter">
      <code>
       min
      </code>
     </em>
     <code class="type">
      int
     </code>
     ,
     <em class="parameter">
      <code>
       sec
      </code>
     </em>
     <code class="type">
      double precision
     </code>
     ) →
     <code class="returnvalue">
      time
     </code>
    </p>
    <p>
     Create time from hour, minute and seconds fields
    </p>
    <p>
     <code class="literal">
      make_time(8, 15, 23.5)
     </code>
     →
     <code class="returnvalue">
      08:15:23.5
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      make_timestamp
     </code>
     (
     <em class="parameter">
      <code>
       year
      </code>
     </em>
     <code class="type">
      int
     </code>
     ,
     <em class="parameter">
      <code>
       month
      </code>
     </em>
     <code class="type">
      int
     </code>
     ,
     <em class="parameter">
      <code>
       day
      </code>
     </em>
     <code class="type">
      int
     </code>
     ,
     <em class="parameter">
      <code>
       hour
      </code>
     </em>
     <code class="type">
      int
     </code>
     ,
     <em class="parameter">
      <code>
       min
      </code>
     </em>
     <code class="type">
      int
     </code>
     ,
     <em class="parameter">
      <code>
       sec
      </code>
     </em>
     <code class="type">
      double precision
     </code>
     ) →
     <code class="returnvalue">
      timestamp
     </code>
    </p>
    <p>
     Create timestamp from year, month, day, hour, minute and seconds fields (negative years signify BC)
    </p>
    <p>
     <code class="literal">
      make_timestamp(2013, 7, 15, 8, 15, 23.5)
     </code>
     →
     <code class="returnvalue">
      2013-07-15 08:15:23.5
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      make_timestamptz
     </code>
     (
     <em class="parameter">
      <code>
       year
      </code>
     </em>
     <code class="type">
      int
     </code>
     ,
     <em class="parameter">
      <code>
       month
      </code>
     </em>
     <code class="type">
      int
     </code>
     ,
     <em class="parameter">
      <code>
       day
      </code>
     </em>
     <code class="type">
      int
     </code>
     ,
     <em class="parameter">
      <code>
       hour
      </code>
     </em>
     <code class="type">
      int
     </code>
     ,
     <em class="parameter">
      <code>
       min
      </code>
     </em>
     <code class="type">
      int
     </code>
     ,
     <em class="parameter">
      <code>
       sec
      </code>
     </em>
     <code class="type">
      double precision
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        timezone
       </code>
      </em>
      <code class="type">
       text
      </code>
     </span>
     ] ) →
     <code class="returnvalue">
      timestamp with time zone
     </code>
    </p>
    <p>
     Create timestamp with time zone from year, month, day, hour, minute and seconds fields (negative years signify BC). If
     <em class="parameter">
      <code>
       timezone
      </code>
     </em>
     is not specified, the current time zone is used; the examples assume the session time zone is
     <code class="literal">
      Europe/London
     </code>
    </p>
    <p>
     <code class="literal">
      make_timestamptz(2013, 7, 15, 8, 15, 23.5)
     </code>
     →
     <code class="returnvalue">
      2013-07-15 08:15:23.5+01
     </code>
    </p>
    <p>
     <code class="literal">
      make_timestamptz(2013, 7, 15, 8, 15, 23.5, 'America/New_York')
     </code>
     →
     <code class="returnvalue">
      2013-07-15 13:15:23.5+01
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      now
     </code>
     ( ) →
     <code class="returnvalue">
      timestamp with time zone
     </code>
    </p>
    <p>
     Current date and time (start of current transaction); see
     <a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-CURRENT" title="9.9.5. Current Date/Time">
      Section 9.9.5
     </a>
    </p>
    <p>
     <code class="literal">
      now()
     </code>
     →
     <code class="returnvalue">
      2019-12-23 14:39:53.662522-05
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      statement_timestamp
     </code>
     ( ) →
     <code class="returnvalue">
      timestamp with time zone
     </code>
    </p>
    <p>
     Current date and time (start of current statement); see
     <a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-CURRENT" title="9.9.5. Current Date/Time">
      Section 9.9.5
     </a>
    </p>
    <p>
     <code class="literal">
      statement_timestamp()
     </code>
     →
     <code class="returnvalue">
      2019-12-23 14:39:53.662522-05
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      timeofday
     </code>
     ( ) →
     <code class="returnvalue">
      text
     </code>
    </p>
    <p>
     Current date and time (like
     <code class="function">
      clock_timestamp
     </code>
     , but as a
     <code class="type">
      text
     </code>
     string); see
     <a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-CURRENT" title="9.9.5. Current Date/Time">
      Section 9.9.5
     </a>
    </p>
    <p>
     <code class="literal">
      timeofday()
     </code>
     →
     <code class="returnvalue">
      Mon Dec 23 14:39:53.662522 2019 EST
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      transaction_timestamp
     </code>
     ( ) →
     <code class="returnvalue">
      timestamp with time zone
     </code>
    </p>
    <p>
     Current date and time (start of current transaction); see
     <a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-CURRENT" title="9.9.5. Current Date/Time">
      Section 9.9.5
     </a>
    </p>
    <p>
     <code class="literal">
      transaction_timestamp()
     </code>
     →
     <code class="returnvalue">
      2019-12-23 14:39:53.662522-05
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      to_timestamp
     </code>
     (
     <code class="type">
      double precision
     </code>
     ) →
     <code class="returnvalue">
      timestamp with time zone
     </code>
    </p>
    <p>
     Convert Unix epoch (seconds since 1970-01-01 00:00:00+00) to timestamp with time zone
    </p>
    <p>
     <code class="literal">
      to_timestamp(1284352323)
     </code>
     →
     <code class="returnvalue">
      2010-09-13 04:32:03+00
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>










Além dessas funções, o operador SQL `OVERLAPS` é suportado:

```
(start1, end1) OVERLAPS (start2, end2)
(start1, length1) OVERLAPS (start2, length2)
```

Essa expressão é verdadeira quando dois períodos de tempo (definidos por seus pontos finais) se sobrepõem, falsa quando não se sobrepõem. Os pontos finais podem ser especificados como pares de datas, horários ou marcações de tempo; ou como uma data, horário ou marcação de tempo seguida de um intervalo. Quando um par de valores é fornecido, o início ou o fim pode ser escrito primeiro; `OVERLAPS` automaticamente assume o valor anterior do par como o início. Cada período de tempo é considerado para representar o intervalo semiaberto *`start`* `<=` *`time`* `<` *`end`*, a menos que *`start`* e *`end`* sejam iguais, no caso em que representa aquele instante de tempo único. Isso significa, por exemplo, que dois períodos de tempo com apenas um ponto final em comum não se sobrepõem.

```
SELECT (DATE '2001-02-16', DATE '2001-12-21') OVERLAPS
       (DATE '2001-10-30', DATE '2002-10-30');
Result: true
SELECT (DATE '2001-02-16', INTERVAL '100 days') OVERLAPS
       (DATE '2001-10-30', DATE '2002-10-30');
Result: false
SELECT (DATE '2001-10-29', DATE '2001-10-30') OVERLAPS
       (DATE '2001-10-30', DATE '2001-10-31');
Result: false
SELECT (DATE '2001-10-30', DATE '2001-10-30') OVERLAPS
       (DATE '2001-10-30', DATE '2001-10-31');
Result: true
```

Ao adicionar um valor de `interval` a (ou subtrair um valor de `interval` de) um valor de `timestamp` ou `timestamp with time zone`, os campos meses, dias e microsegundos do valor de `interval` são tratados em ordem. Primeiro, um campo de meses não nulo avança ou decrementa a data do timestamp pelo número indicado de meses, mantendo o dia do mês o mesmo, a menos que seja passado pelo final do novo mês, caso em que o último dia desse mês é usado. (Por exemplo, 31 de março mais 1 mês se torna 30 de abril, mas 31 de março mais 2 meses se torna 31 de maio.) Em seguida, o campo dias avança ou decrementa a data do timestamp pelo número indicado de dias. Em ambos os passos, o horário local do dia é mantido o mesmo. Finalmente, se houver um campo de microsegundos não nulo, ele é adicionado ou subtraído literalmente. Ao realizar cálculos em um valor de `timestamp with time zone` em um fuso horário que reconhece o DST, isso significa que adicionar ou subtrair (digamos) `interval '1 day'` não necessariamente tem o mesmo resultado que adicionar ou subtrair `interval '24 hours'`. Por exemplo, com o fuso horário de sessão definido como `America/Denver`:

```
SELECT timestamp with time zone '2005-04-02 12:00:00-07' + interval '1 day';
Result: 2005-04-03 12:00:00-06
SELECT timestamp with time zone '2005-04-02 12:00:00-07' + interval '24 hours';
Result: 2005-04-03 13:00:00-06
```

Isso acontece porque uma hora foi omitida devido a uma mudança no horário de verão em `2005-04-03 02:00:00` no fuso horário `America/Denver`.

Observe que pode haver ambiguidade no campo `months` retornado por `age`, pois diferentes meses têm diferentes números de dias. A abordagem do PostgreSQL usa o mês da data anterior entre as duas quando calculando meses parciais. Por exemplo, `age('2004-06-01', '2004-04-30')` usa abril para gerar `1 mon 1 day`, enquanto usar maio geraria `1 mon 2 days`, porque maio tem 31 dias, enquanto abril tem apenas 30.

A subtração de datas e timestamps também pode ser complexa. Uma maneira conceitualmente simples de realizar a subtração é converter cada valor em um número de segundos usando `EXTRACT(EPOCH FROM ...)`, e depois subtrair os resultados; isso produz o número de *segundos* entre os dois valores. Isso ajusta o número de dias em cada mês, mudanças de fuso horário e ajustes para o horário de verão. A subtração de valores de data ou timestamp com o operador “`-`” retorna o número de dias (24 horas) e horas/minutos/segundos entre os valores, fazendo os mesmos ajustes. A função `age` retorna anos, meses, dias e horas/minutos/segundos, realizando a subtração de campo por campo e depois ajustando para valores de campo negativos. As seguintes consultas ilustram as diferenças nessas abordagens. Os resultados da amostra foram produzidos com `timezone = 'US/Eastern'`; há uma mudança no horário de verão entre as duas datas usadas:

```
SELECT EXTRACT(EPOCH FROM timestamptz '2013-07-01 12:00:00') -
       EXTRACT(EPOCH FROM timestamptz '2013-03-01 12:00:00');
Result: 10537200.000000
SELECT (EXTRACT(EPOCH FROM timestamptz '2013-07-01 12:00:00') -
        EXTRACT(EPOCH FROM timestamptz '2013-03-01 12:00:00'))
        / 60 / 60 / 24;
Result: 121.9583333333333333
SELECT timestamptz '2013-07-01 12:00:00' - timestamptz '2013-03-01 12:00:00';
Result: 121 days 23:00:00
SELECT age(timestamptz '2013-07-01 12:00:00', timestamptz '2013-03-01 12:00:00');
Result: 4 mons
```

### 9.9.1. `EXTRACT`, `date_part` [#](#FUNCTIONS-DATETIME-EXTRACT)

```
EXTRACT(field FROM source)
```

A função `extract` recupera subcampos, como ano ou hora, a partir de valores de data/hora. *`source`* deve ser uma expressão de valor do tipo `timestamp`, `date`, `time` ou `interval`. (Os timestamps e os horários podem ser com ou sem fuso horário.) *`field`* é um identificador ou uma string que seleciona qual campo extrair do valor de origem. Nem todos os campos são válidos para todos os tipos de dados de entrada; por exemplo, campos menores que um dia não podem ser extraídos de um `date`, enquanto campos de um dia ou mais não podem ser extraídos de um `time`. A função `extract` retorna valores do tipo `numeric`.

Os seguintes nomes de campo são válidos:

`century`: O século; para os valores de `interval`, o campo ano dividido por 100

```
SELECT EXTRACT(CENTURY FROM TIMESTAMP '2000-12-16 12:21:13'); Result: 20 SELECT EXTRACT(CENTURY FROM TIMESTAMP '2001-02-16 20:38:40'); Result: 21 SELECT EXTRACT(CENTURY FROM DATE '0001-01-01 AD'); Result: 1 SELECT EXTRACT(CENTURY FROM DATE '0001-12-31 BC'); Result: -1 SELECT EXTRACT(CENTURY FROM INTERVAL '2001 years'); Result: 20
```

`day`: O dia do mês (1–31); para os valores de `interval`, o número de dias

```
SELECT EXTRACT(DAY FROM TIMESTAMP '2001-02-16 20:38:40'); Result: 16 SELECT EXTRACT(DAY FROM INTERVAL '40 days 1 minute'); Result: 40
```

`decade` :   O campo ano dividido por 10

```
SELECT EXTRACT(DECADE FROM TIMESTAMP '2001-02-16 20:38:40'); Result: 200
```

`dow` :   O dia da semana como domingo (`0`) a `6`  sábado

```
SELECT EXTRACT(DOW FROM TIMESTAMP '2001-02-16 20:38:40'); Result: 5
```

Observe que a numeração do dia da semana de `extract` difere daquela da função `to_char(..., 'D')`.

`doy` :   Dia do ano (1 a 365/366)

```
SELECT EXTRACT(DOY FROM TIMESTAMP '2001-02-16 20:38:40'); Result: 47
```

`epoch` Para os valores de `timestamp with time zone`, o número de segundos desde 1970-01-01 00:00:00 UTC (negativo para timestamps antes disso); para os valores de `date` e `timestamp`, o número nominal de segundos desde 1970-01-01 00:00:00, sem considerar o fuso horário ou as regras de mudança de hora; para os valores de `interval`, o número total de segundos no intervalo

```
SELECT EXTRACT(EPOCH FROM TIMESTAMP WITH TIME ZONE '2001-02-16 20:38:40.12-08'); Result: 982384720.120000 SELECT EXTRACT(EPOCH FROM TIMESTAMP '2001-02-16 20:38:40.12'); Result: 982355920.120000 SELECT EXTRACT(EPOCH FROM INTERVAL '5 days 3 hours'); Result: 442800.000000
```

Você pode converter um valor de época de volta para um `timestamp with time zone` com `to_timestamp`:

```
SELECT to_timestamp(982384720.12); Result: 2001-02-17 04:38:40.12+00
```

Cuidado: aplicar `to_timestamp` a uma época extraída de um valor de `date` ou `timestamp` pode produzir um resultado enganoso: o resultado efetivamente assumirá que o valor original foi dado em UTC, o que pode não ser o caso.

`hour`: O campo hora (0–23 em timestamps, sem restrições em intervalos)

```
SELECT EXTRACT(HOUR FROM TIMESTAMP '2001-02-16 20:38:40'); Result: 20
```

`isodow`: O dia da semana como Segunda-feira (`1`) a Domingo (`7`)

```
SELECT EXTRACT(ISODOW FROM TIMESTAMP '2001-02-18 20:38:40'); Result: 7
```

Isso é idêntico a `dow`, exceto no domingo. Isso corresponde à numeração do dia da semana ISO 8601.

`isoyear`: O ano de numeração de semana ISO 8601 em que a data ocorre

```
SELECT EXTRACT(ISOYEAR FROM DATE '2006-01-01'); Result: 2005 SELECT EXTRACT(ISOYEAR FROM DATE '2006-01-02'); Result: 2006
```

Cada ano numerado com base na semana ISO 8601 começa na segunda-feira da semana que contém o dia 4 de janeiro, portanto, no início de janeiro ou no final de dezembro, o ano ISO pode ser diferente do ano gregoriano. Consulte o campo `week` para obter mais informações.

`julian`: A *Data de Julho* correspondente à data ou timestamp. Os timestamps que não são meia-noite local resultam em um valor fracionário. Consulte a [Seção B.7](datetime-julian-dates.md) para mais informações.

```
SELECT EXTRACT(JULIAN FROM DATE '2006-01-01'); Result: 2453737 SELECT EXTRACT(JULIAN FROM TIMESTAMP '2006-01-01 12:00'); Result: 2453737.50000000000000000000
```

`microseconds`: Os segundos, incluindo partes fracionárias, multiplicados por 1 000 000; observe que isso inclui segundos completos

```
SELECT EXTRACT(MICROSECONDS FROM TIME '17:12:28.5'); Result: 28500000
```

`millennium`: O milênio; para os valores de `interval`, o campo ano dividido por 1000

```
SELECT EXTRACT(MILLENNIUM FROM TIMESTAMP '2001-02-16 20:38:40'); Result: 3 SELECT EXTRACT(MILLENNIUM FROM INTERVAL '2001 years'); Result: 2
```

Os anos dos anos 1900 estão no segundo milênio. O terceiro milênio começou em 1º de janeiro de 2001.

`milliseconds`: O campo segundos, incluindo partes fracionárias, multiplicado por 1000. Observe que isso inclui segundos completos.

```
SELECT EXTRACT(MILLISECONDS FROM TIME '17:12:28.5'); Result: 28500.000
```

`minute` :   campo minutos (0–59)

```
SELECT EXTRACT(MINUTE FROM TIMESTAMP '2001-02-16 20:38:40'); Result: 38
```

`month` :   O número do mês dentro do ano (1–12); para os valores de `interval`, o número de meses módulo 12 (0–11)

```
SELECT EXTRACT(MONTH FROM TIMESTAMP '2001-02-16 20:38:40'); Result: 2 SELECT EXTRACT(MONTH FROM INTERVAL '2 years 3 months'); Result: 3 SELECT EXTRACT(MONTH FROM INTERVAL '2 years 13 months'); Result: 1
```

`quarter` : O trimestre do ano (1–4) em que a data está; para os valores de `interval`, o campo mês dividido por 3 mais 1

```
SELECT EXTRACT(QUARTER FROM TIMESTAMP '2001-02-16 20:38:40'); Result: 1 SELECT EXTRACT(QUARTER FROM INTERVAL '1 year 6 months'); Result: 3
```

`second`: O campo segundos, incluindo quaisquer segundos fracionários

```
SELECT EXTRACT(SECOND FROM TIMESTAMP '2001-02-16 20:38:40'); Result: 40.000000 SELECT EXTRACT(SECOND FROM TIME '17:12:28.5'); Result: 28.500000
```

`timezone`: O deslocamento do fuso horário em relação ao UTC, medido em segundos. Valores positivos correspondem a fusos horários a leste do UTC, valores negativos a fusos horários a oeste do UTC. (Tecnicamente, o PostgreSQL não usa o UTC porque os segundos intercalares não são tratados.)

`timezone_hour`: O componente de hora do deslocamento do fuso horário

`timezone_minute`: O componente minuto do deslocamento do fuso horário

`week`: O número da semana de numeração de semanas ISO 8601 do ano. Por definição, as semanas ISO começam na segunda-feira e a primeira semana de um ano contém o dia 4 de janeiro desse ano. Em outras palavras, o primeiro sábado de um ano está na semana 1 desse ano.

No sistema de numeração de semanas ISO, é possível que datas de início de janeiro tenham como parte da 52ª ou 53ª semana do ano anterior, e que datas de final de dezembro tenham como parte da primeira semana do ano seguinte. Por exemplo, `2005-01-01` faz parte da 53ª semana do ano 2004, e `2006-01-01` faz parte da 52ª semana do ano 2005, enquanto `2012-12-31` faz parte da primeira semana de 2013. Recomenda-se usar o campo `isoyear` juntamente com `week` para obter resultados consistentes.

Para os valores de `interval`, o campo semana é simplesmente o número de dias inteiros dividido por 7.

```
SELECT EXTRACT(WEEK FROM TIMESTAMP '2001-02-16 20:38:40'); Result: 7 SELECT EXTRACT(WEEK FROM INTERVAL '13 days 24 hours'); Result: 1
```

:   O campo ano. Tenha em mente que não há `0 AD`, então subtrair `BC` anos de `AD` anos deve ser feito com cuidado.

```
SELECT EXTRACT(YEAR FROM TIMESTAMP '2001-02-16 20:38:40'); Result: 2001
```

Ao processar um valor de `interval`, a função `extract` produz valores de campo que correspondem à interpretação usada pela função de saída de intervalo. Isso pode produzir resultados surpreendentes se começar com uma representação de intervalo não normalizada, por exemplo:

```
SELECT INTERVAL '80 minutes'; Result: 01:20:00 SELECT EXTRACT(MINUTES FROM INTERVAL '80 minutes'); Result: 20
```

Nota

Quando o valor de entrada é +/-Infinity, `extract` retorna +/-Infinity para campos que são estritamente crescentes (`epoch`, `julian`, `year`, `isoyear`, `decade`, `century` e `millennium` para entradas de `timestamp`; `epoch`, `hour`, `day`, `year`, `decade`, `century` e `millennium` para `interval`. Para outros campos, é retornado NULL. As versões do PostgreSQL antes de 9.6 retornavam zero para todos os casos de entrada infinita.

A função `extract` é destinada principalmente ao processamento computacional. Para formatação de valores de data/hora para exibição, consulte [Seção 9.8](functions-formatting.md).

A função `date_part` é modelada no equivalente tradicional de Ingres ao padrão SQL, que é a função `extract`:

```
date_part('field', source)
```

Observe que, aqui, o parâmetro *`field`* precisa ser um valor de string, não um nome. Os nomes de campo válidos para `date_part` são os mesmos que para `extract`. Por razões históricas, a função `date_part` retorna valores do tipo `double precision`. Isso pode resultar em perda de precisão em certos usos. Em vez disso, é recomendado usar `extract`.

```
SELECT date_part('day', TIMESTAMP '2001-02-16 20:38:40'); Result: 16 SELECT date_part('hour', INTERVAL '4 hours 3 minutes'); Result: 4
```

### 9.9.2. `date_trunc` [#](#FUNCTIONS-DATETIME-TRUNC)

A função `date_trunc` é conceitualmente semelhante à função `trunc` para números.

```
date_trunc(field, source [, time_zone ])
```

*`source`* é uma expressão de valor do tipo `timestamp`, `timestamp with time zone`, ou `interval`.

(Os valores do tipo `date` e `time` são convertidos automaticamente para `timestamp` ou `interval`, respectivamente.) *`field`* seleciona a precisão para restringir o valor de entrada. O valor de retorno é igualmente do tipo `timestamp`, `timestamp with time zone`, ou `interval`, e possui todos os campos que são menos significativos que o selecionado definidos como zero (ou um, para dia e mês).

Os valores válidos para *`field`* são:



<table border="0" class="simplelist" summary="Simple list">
 <tr>
  <td>
   <code class="literal">
    microseconds
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="literal">
    milliseconds
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="literal">
    second
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="literal">
    minute
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="literal">
    hour
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="literal">
    day
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="literal">
    week
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="literal">
    month
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="literal">
    quarter
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="literal">
    year
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="literal">
    decade
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="literal">
    century
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="literal">
    millennium
   </code>
  </td>
 </tr>
</table>







Quando o valor de entrada é do tipo `timestamp with time zone`, a troncamento é realizada em relação a um fuso horário específico; por exemplo, a troncamento para `day` produz um valor que é meia-noite nessa zona. Por padrão, a troncamento é feita em relação à configuração atual de [TimeZone](runtime-config-client.md#GUC-TIMEZONE), mas o argumento opcional *`time_zone`* pode ser fornecido para especificar um fuso horário diferente. O nome do fuso horário pode ser especificado em qualquer uma das maneiras descritas em [Seção 8.5.3](datatype-datetime.md#DATATYPE-TIMEZONES).

Não é possível especificar um fuso horário ao processar as entradas `timestamp without time zone` ou `interval`. Essas são sempre tomadas como verdadeiras.

Exemplos (assumindo que o fuso horário local é `America/New_York`):

```
SELECT date_trunc('hour', TIMESTAMP '2001-02-16 20:38:40'); Result: 2001-02-16 20:00:00 SELECT date_trunc('year', TIMESTAMP '2001-02-16 20:38:40'); Result: 2001-01-01 00:00:00 SELECT date_trunc('day', TIMESTAMP WITH TIME ZONE '2001-02-16 20:38:40+00'); Result: 2001-02-16 00:00:00-05 SELECT date_trunc('day', TIMESTAMP WITH TIME ZONE '2001-02-16 20:38:40+00', 'Australia/Sydney'); Result: 2001-02-16 08:00:00-05 SELECT date_trunc('hour', INTERVAL '3 days 02:47:33'); Result: 3 days 02:00:00
```

### 9.9.3. `date_bin` [#](#FUNCTIONS-DATETIME-BIN)

A função `date_bin` "armazena" o timestamp de entrada no intervalo especificado (o *passo*) alinhado com uma origem especificada.

```
date_bin(stride, source, origin)
```

*`source`* é uma expressão de valor do tipo `timestamp` ou `timestamp with time zone`. (Os valores do tipo `date` são convertidos automaticamente para `timestamp`.)*`stride`* é uma expressão de valor do tipo `interval`. O valor de retorno é igualmente do tipo `timestamp` ou `timestamp with time zone`, e marca o início do bin no qual o *`source`* é colocado.

Exemplos:

```
SELECT date_bin('15 minutes', TIMESTAMP '2020-02-11 15:44:17', TIMESTAMP '2001-01-01'); Result: 2020-02-11 15:30:00 SELECT date_bin('15 minutes', TIMESTAMP '2020-02-11 15:44:17', TIMESTAMP '2001-01-01 00:02:30'); Result: 2020-02-11 15:32:30
```

No caso de unidades completas (1 minuto, 1 hora, etc.), ele dá o mesmo resultado que a chamada `date_trunc`, mas a diferença é que `date_bin` pode ser truncada para um intervalo arbitrário.

O intervalo *`stride`* deve ser maior que zero e não pode conter unidades de mês ou maiores.

### 9.9.4. `AT TIME ZONE` e `AT LOCAL` [#](#FUNCTIONS-DATETIME-ZONECONVERT)

O operador `AT TIME ZONE` converte o rótulo de tempo *sem* fuso horário para/do rótulo de tempo *com* fuso horário, e os valores `time with time zone` para diferentes fusos horários. [Tabela 9.34](functions-datetime.md#FUNCTIONS-DATETIME-ZONECONVERT-TABLE "Table 9.34. AT TIME ZONE and AT LOCAL Variants") mostra seus variações.

**Tabela 9.34. `AT TIME ZONE` e `AT LOCAL` Variantes**



<table border="1" class="table" summary="AT TIME ZONE and AT LOCAL Variants">
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Operador
    </p>
    <p>
     Descrição
    </p>
    <p>
     Exemplo(s)
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      timestamp without time zone
     </code>
     <code class="literal">
      AT TIME ZONE
     </code>
     <em class="replaceable">
      <code>
       zone
      </code>
     </em>
     →
     <code class="returnvalue">
      timestamp with time zone
     </code>
    </p>
    <p>
     Converte o tempo de marcação
     <span class="emphasis">
      <em>
       sem
      </em>
     </span>
     fuso horário para marcador de tempo
     <span class="emphasis">
      <em>
       com
      </em>
     </span>
     fuso horário, assumindo que o valor dado está no fuso horário designado.
    </p>
    <p>
     <code class="literal">
      timestamp '2001-02-16 20:38:40' at time zone 'America/Denver'
     </code>
     →
     <code class="returnvalue">
      2001-02-17 03:38:40+00
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      timestamp without time zone
     </code>
     <code class="literal">
      AT LOCAL
     </code>
     →
     <code class="returnvalue">
      timestamp with time zone
     </code>
    </p>
    <p>
     Converte o tempo de marcação
     <span class="emphasis">
      <em>
       sem
      </em>
     </span>
     fuso horário para marcador de tempo
     <span class="emphasis">
      <em>
       com
      </em>
     </span>
     a sessão de
     <code class="varname">
      TimeZone
     </code>
     valor como fuso horário.
    </p>
    <p>
     <code class="literal">
      timestamp '2001-02-16 20:38:40' at local
     </code>
     →
     <code class="returnvalue">
      2001-02-17 03:38:40+00
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      timestamp with time zone
     </code>
     <code class="literal">
      AT TIME ZONE
     </code>
     <em class="replaceable">
      <code>
       zone
      </code>
     </em>
     →
     <code class="returnvalue">
      timestamp without time zone
     </code>
    </p>
    <p>
     Converte o tempo de marcação
     <span class="emphasis">
      <em>
       com
      </em>
     </span>
     fuso horário para marcador de tempo
     <span class="emphasis">
      <em>
       sem
      </em>
     </span>
     fuso horário, pois o horário apareceria nessa zona.
    </p>
    <p>
     <code class="literal">
      timestamp with time zone '2001-02-16 20:38:40-05' at time zone 'America/Denver'
     </code>
     →
     <code class="returnvalue">
      2001-02-16 18:38:40
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      timestamp with time zone
     </code>
     <code class="literal">
      AT LOCAL
     </code>
     →
     <code class="returnvalue">
      timestamp without time zone
     </code>
    </p>
    <p>
     Converte o tempo de marcação
     <span class="emphasis">
      <em>
       com
      </em>
     </span>
     fuso horário para marcador de tempo
     <span class="emphasis">
      <em>
       sem
      </em>
     </span>
     fuso horário, pois o horário apareceria com a sessão
     <code class="varname">
      TimeZone
     </code>
     valor como fuso horário.
    </p>
    <p>
     <code class="literal">
      timestamp with time zone '2001-02-16 20:38:40-05' at local
     </code>
     →
     <code class="returnvalue">
      2001-02-16 18:38:40
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      time with time zone
     </code>
     <code class="literal">
      AT TIME ZONE
     </code>
     <em class="replaceable">
      <code>
       zone
      </code>
     </em>
     →
     <code class="returnvalue">
      time with time zone
     </code>
    </p>
    <p>
     Converte o tempo dado
     <span class="emphasis">
      <em>
       com
      </em>
     </span>
     Para mudar a zona horária para uma nova zona horária. Como não foi fornecida uma data, este usa o deslocamento UTC atualmente ativo para a zona de destino designada.
    </p>
    <p>
     <code class="literal">
      time with time zone '05:34:17-05' at time zone 'UTC'
     </code>
     →
     <code class="returnvalue">
      10:34:17+00
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      time with time zone
     </code>
     <code class="literal">
      AT LOCAL
     </code>
     →
     <code class="returnvalue">
      time with time zone
     </code>
    </p>
    <p>
     Converte o tempo dado
     <span class="emphasis">
      <em>
       com
      </em>
     </span>
     tempo de fuso horário para uma nova zona horária. Como não foi fornecida uma data, este usa o deslocamento UTC atualmente ativo para a sessão
     <code class="varname">
      TimeZone
     </code>
     value.
    </p>
    <p>
     Supondo que a sessão seja
     <code class="varname">
      TimeZone
     </code>
     está previsto
     <code class="literal">
      UTC
     </code>
     :
    </p>
    <p>
     <code class="literal">
      time with time zone '05:34:17-05' at local
     </code>
     →
     <code class="returnvalue">
      10:34:17+00
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>










Nestas expressões, o fuso horário desejado *`zone`* pode ser especificado como um valor de texto (por exemplo, `'America/Los_Angeles'`) ou como um intervalo (por exemplo, `INTERVAL '-08:00'`). No caso de texto, um nome de fuso horário pode ser especificado de qualquer das maneiras descritas em [Seção 8.5.3](datatype-datetime.md#DATATYPE-TIMEZONES "8.5.3. Time Zones"). O caso de intervalo é útil apenas para zonas que têm deslocamentos fixos em relação ao UTC, portanto, não é muito comum na prática.

A sintaxe `AT LOCAL` pode ser usada como abreviação para `AT TIME ZONE local`, onde *`local`* é o valor da sessão `TimeZone`.

Exemplos (assumindo que o ajuste atual de [TimeZone](runtime-config-client.md#GUC-TIMEZONE) é `America/Los_Angeles`):

```
SELECT TIMESTAMP '2001-02-16 20:38:40' AT TIME ZONE 'America/Denver'; Result: 2001-02-16 19:38:40-08 SELECT TIMESTAMP WITH TIME ZONE '2001-02-16 20:38:40-05' AT TIME ZONE 'America/Denver'; Result: 2001-02-16 18:38:40 SELECT TIMESTAMP '2001-02-16 20:38:40' AT TIME ZONE 'Asia/Tokyo' AT TIME ZONE 'America/Chicago'; Result: 2001-02-16 05:38:40 SELECT TIMESTAMP WITH TIME ZONE '2001-02-16 20:38:40-05' AT LOCAL; Result: 2001-02-16 17:38:40 SELECT TIMESTAMP WITH TIME ZONE '2001-02-16 20:38:40-05' AT TIME ZONE '+05'; Result: 2001-02-16 20:38:40 SELECT TIME WITH TIME ZONE '20:38:40-05' AT LOCAL; Result: 17:38:40
```

O primeiro exemplo adiciona um fuso horário a um valor que não o possui e exibe o valor usando o ajuste atual do `TimeZone` . O segundo exemplo desloca o rótulo de tempo com valor de fuso horário para o fuso horário especificado e retorna o valor sem um fuso horário. Isso permite o armazenamento e a exibição de valores diferentes do ajuste atual do `TimeZone`. O terceiro exemplo converte o horário de Tóquio para o horário de Chicago. O quarto exemplo desloca o rótulo de tempo com valor de fuso horário para o fuso horário atualmente especificado pelo ajuste do `TimeZone` e retorna o valor sem um fuso horário. O quinto exemplo demonstra que o sinal em uma especificação de fuso horário em estilo POSIX tem o significado oposto ao sinal em um literal de data e hora ISO-8601, conforme descrito em [Seção 8.5.3](datatype-datetime.md#DATATYPE-TIMEZONES) e [Apêndice B](datetime-appendix.md).

O sexto exemplo é uma história de advertência. Devido ao fato de que não há uma data associada ao valor de entrada, a conversão é feita usando a data atual da sessão. Portanto, este exemplo estático pode mostrar um resultado errado dependendo da época do ano em que é visualizado, porque `'America/Los_Angeles'` observa o Horário de Verão.

A função `timezone(zone, timestamp)` é equivalente ao construtor conforme SQL `timestamp AT TIME ZONE zone`.

A função `timezone(zone, time)` é equivalente ao construtor conforme SQL `time AT TIME ZONE zone`.

A função `timezone(timestamp)` é equivalente ao construtivo conforme SQL `timestamp AT LOCAL`.

A função `timezone(time)` é equivalente ao construtivo conforme SQL `time AT LOCAL`.

### 9.9.5. Data/Hora atual [#](#FUNCTIONS-DATETIME-CURRENT)

O PostgreSQL oferece vários funções que retornam valores relacionados à data e hora atuais. Essas funções padrão do SQL retornam todos os valores com base no horário de início da transação atual:

```
CURRENT_DATE CURRENT_TIME CURRENT_TIMESTAMP CURRENT_TIME(precision) CURRENT_TIMESTAMP(precision) LOCALTIME LOCALTIMESTAMP LOCALTIME(precision) LOCALTIMESTAMP(precision)
```

`CURRENT_TIME` e `CURRENT_TIMESTAMP` fornecem valores com fuso horário; `LOCALTIME` e `LOCALTIMESTAMP` fornecem valores sem fuso horário.

`CURRENT_TIME`, `CURRENT_TIMESTAMP`, `LOCALTIME`, e `LOCALTIMESTAMP` podem, opcionalmente, ter um parâmetro de precisão, o que faz com que o resultado seja arredondado para tantos dígitos fracionários no campo de segundos. Sem um parâmetro de precisão, o resultado é dado à precisão completa disponível.

Alguns exemplos:

```
SELECT CURRENT_TIME; Result: 14:39:53.662522-05 SELECT CURRENT_DATE; Result: 2019-12-23 SELECT CURRENT_TIMESTAMP; Result: 2019-12-23 14:39:53.662522-05 SELECT CURRENT_TIMESTAMP(2); Result: 2019-12-23 14:39:53.66-05 SELECT LOCALTIMESTAMP; Result: 2019-12-23 14:39:53.662522
```

Como essas funções retornam o horário de início da transação atual, seus valores não mudam durante a transação. Isso é considerado uma característica: a intenção é permitir que uma única transação tenha uma noção consistente do tempo "atual", de modo que múltiplas modificações dentro da mesma transação tenham o mesmo selo de tempo.

Nota

Outros sistemas de banco de dados podem avançar esses valores com mais frequência.

O PostgreSQL também fornece funções que retornam o horário de início da declaração atual, bem como o horário atual no instante em que a função é chamada. A lista completa das funções de hora não padrão do SQL é:

```
transaction_timestamp() statement_timestamp() clock_timestamp() timeofday() now()
```

`transaction_timestamp()` é equivalente a `CURRENT_TIMESTAMP`, mas foi nomeado para refletir claramente o que ele retorna. `statement_timestamp()` retorna o horário de início da declaração atual (mais especificamente, o momento da recepção da última mensagem de comando do cliente). `statement_timestamp()` e `transaction_timestamp()` retornam o mesmo valor durante a primeira declaração de uma transação, mas podem diferir durante declarações subsequentes. `clock_timestamp()` retorna o horário atual real, e portanto, seu valor muda mesmo dentro de uma única declaração SQL. `timeofday()` é uma função histórica PostgreSQL. Como `clock_timestamp()`, ela retorna o horário atual real, mas como uma string formatada `text` em vez de um valor `timestamp with time zone`. `now()` é um equivalente PostgreSQL tradicional equivalente a `transaction_timestamp()`.

Todos os tipos de dados de data/hora também aceitam o valor literal especial `now` para especificar a data e hora atuais (novamente, interpretado como o horário de início da transação). Assim, os seguintes três retornam o mesmo resultado:

```
SELECT CURRENT_TIMESTAMP; SELECT now(); SELECT TIMESTAMP 'now';  -- but see tip below
```

DICA

Não use a terceira forma ao especificar um valor a ser avaliado mais tarde, por exemplo, em uma cláusula `DEFAULT` para uma coluna de tabela. O sistema converterá `now` para um `timestamp` assim que a constante for analisada, para que, quando o valor padrão seja necessário, o momento da criação da tabela seja usado! As duas primeiras formas não serão avaliadas até que o valor padrão seja usado, porque são chamadas de função. Assim, elas darão o comportamento desejado de retornar ao momento da inserção da linha.

(Veja também [Seção 8.5.1.4](datatype-datetime.md#DATATYPE-DATETIME-SPECIAL-VALUES).

### 9.9.6. Retardo na execução [#](#FUNCTIONS-DATETIME-DELAY)

As seguintes funções estão disponíveis para adiar a execução do processo do servidor:

```
pg_sleep ( double precision ) pg_sleep_for ( interval ) pg_sleep_until ( timestamp with time zone )
```

`pg_sleep` faz o processo da sessão atual dormir até que o número dado de segundos tenha decorrido. Atraso de fração de segundo podem ser especificados. `pg_sleep_for` é uma função de conveniência para permitir que o tempo de sono seja especificado como um `interval`. `pg_sleep_until` é uma função de conveniência para quando um horário específico de despertar é desejado. Por exemplo:

```
SELECT pg_sleep(1.5); SELECT pg_sleep_for('5 minutes'); SELECT pg_sleep_until('tomorrow 03:00');
```

Nota

A resolução efetiva do intervalo de sono é específica da plataforma; 0,01 segundos é um valor comum. O atraso de sono será pelo menos tão longo quanto especificado. Pode ser mais longo, dependendo de fatores como a carga do servidor. Em particular, `pg_sleep_until` não é garantido que acorde exatamente na hora especificada, mas não acordará mais cedo.

### Aviso

Certifique-se de que sua sessão não tenha mais bloqueios do que o necessário ao chamar `pg_sleep` ou suas variantes. Caso contrário, outras sessões podem ter que esperar pelo seu processo de sono, o que desacelera todo o sistema.
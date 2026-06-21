## 9.8. Funções de formatação de tipos de dados [#](#FUNCTIONS-FORMATTING)

As funções de formatação do PostgreSQL fornecem um conjunto poderoso de ferramentas para converter vários tipos de dados (data/hora, inteiro, ponto flutuante, numérico) em strings formatadas e para converter de strings formatadas para tipos de dados específicos. [Tabela 9.26][(functions-formatting.md#FUNCTIONS-FORMATTING-TABLE "Table 9.26. Formatting Functions")] as lista. Todas essas funções seguem uma convenção de chamada comum: o primeiro argumento é o valor a ser formatado e o segundo argumento é um modelo que define o formato de saída ou entrada.

**Tabela 9.26. Funções de formatação**



<table border="1" class="table" summary="Formatting Functions">
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
      to_char
     </code>
     (
     <code class="type">
      timestamp
     </code>
     ,
     <code class="type">
      text
     </code>
     )
        →
     <code class="returnvalue">
      text
     </code>
</p>
<p class="func_signature">
<code class="function">
      to_char
     </code>
     (
     <code class="type">
      timestamp with time zone
     </code>
     ,
     <code class="type">
      text
     </code>
     )
        →
     <code class="returnvalue">
      text
     </code>
</p>
<p>
     Converts time stamp to string according to the given format.
    </p>
<p>
<code class="literal">
      to_char(timestamp '2002-04-20 17:31:12.66', 'HH12:MI:SS')
     </code>
     →
     <code class="returnvalue">
      05:31:12
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      to_char
     </code>
     (
     <code class="type">
      interval
     </code>
     ,
     <code class="type">
      text
     </code>
     )
        →
     <code class="returnvalue">
      text
     </code>
</p>
<p>
     Converts interval to string according to the given format.
    </p>
<p>
<code class="literal">
      to_char(interval '15h 2m 12s', 'HH24:MI:SS')
     </code>
     →
     <code class="returnvalue">
      15:02:12
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      to_char
     </code>
     (
     <em class="replaceable">
<code>
       numeric_type
      </code>
</em>
     ,
     <code class="type">
      text
     </code>
     )
        →
     <code class="returnvalue">
      text
     </code>
</p>
<p>
     Converts number to string according to the given format; available for
     <code class="type">
      integer
     </code>
     ,
     <code class="type">
      bigint
     </code>
     ,
     <code class="type">
      numeric
     </code>
     ,
     <code class="type">
      real
     </code>
     ,
     <code class="type">
      double precision
     </code>
     .
    </p>
<p>
<code class="literal">
      to_char(125, '999')
     </code>
     →
     <code class="returnvalue">
      125
     </code>
</p>
<p>
<code class="literal">
      to_char(125.8::real, '999D9')
     </code>
     →
     <code class="returnvalue">
      125.8
     </code>
</p>
<p>
<code class="literal">
      to_char(-125.8, '999D99S')
     </code>
     →
     <code class="returnvalue">
      125.80-
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      to_date
     </code>
     (
     <code class="type">
      text
     </code>
     ,
     <code class="type">
      text
     </code>
     )
        →
     <code class="returnvalue">
      date
     </code>
</p>
<p>
     Converts string to date according to the given format.
    </p>
<p>
<code class="literal">
      to_date('05 Dec 2000', 'DD Mon YYYY')
     </code>
     →
     <code class="returnvalue">
      2000-12-05
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      to_number
     </code>
     (
     <code class="type">
      text
     </code>
     ,
     <code class="type">
      text
     </code>
     )
        →
     <code class="returnvalue">
      numeric
     </code>
</p>
<p>
     Converts string to numeric according to the given format.
    </p>
<p>
<code class="literal">
      to_number('12,454.8-', '99G999D9S')
     </code>
     →
     <code class="returnvalue">
      -12454.8
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
      text
     </code>
     ,
     <code class="type">
      text
     </code>
     )
        →
     <code class="returnvalue">
      timestamp with time zone
     </code>
</p>
<p>
     Converts string to time stamp according to the given format. (See also
     <code class="function">
      to_timestamp(double precision)
     </code>
     in
     <a class="xref" href="functions-datetime.md#FUNCTIONS-DATETIME-TABLE" title="Table 9.33. Date/Time Functions">
      Table 9.33
     </a>
     .)
    </p>
<p>
<code class="literal">
      to_timestamp('05 Dec 2000', 'DD Mon YYYY')
     </code>
     →
     <code class="returnvalue">
      2000-12-05 00:00:00-05
     </code>
</p>
</td>
</tr>
</tbody>
</table>




  

### DICA

`to_timestamp` e `to_date` existem para lidar com formatos de entrada que não podem ser convertidos por simples casting. Para a maioria dos formatos padrão de data/hora, simplesmente converter a string de origem para o tipo de dado necessário funciona e é muito mais fácil. Da mesma forma, `to_number` é desnecessário para representações numéricas padrão.

Em uma string de modelo de saída do `to_char`, existem certos padrões que são reconhecidos e substituídos por dados formatados adequadamente com base no valor fornecido. Qualquer texto que não seja um padrão de modelo é simplesmente copiado literalmente. Da mesma forma, em uma string de modelo de entrada (para as outras funções), os padrões de modelo identificam os valores que serão fornecidos pela string de dados de entrada. Se houver caracteres na string de modelo que não sejam padrões de modelo, os caracteres correspondentes na string de dados de entrada são simplesmente ignorados (sejam eles iguais ou não aos caracteres da string de modelo).

[Tabela 9.27][(functions-formatting.md#FUNCTIONS-FORMATTING-DATETIME-TABLE "Table 9.27. Template Patterns for Date/Time Formatting")] mostra os padrões de modelo disponíveis para formatação de valores de data e hora.

**Tabela 9.27. Padrões de modelo para formatação de data/hora**



<table border="1" class="table" summary="Template Patterns for Date/Time Formatting">
<colgroup>
<col/>
<col/>
</colgroup>
<thead>
<tr>
<th>
    Pattern
   </th>
<th>Descrição</th>
</tr>
</thead>
<tbody>
<tr>
<td>
<code class="literal">
     HH
    </code>
</td>
<td>hora do dia (01–12)</td>
</tr>
<tr>
<td>
<code class="literal">
     HH12
    </code>
</td>
<td>hora do dia (01–12)</td>
</tr>
<tr>
<td>
<code class="literal">
     HH24
    </code>
</td>
<td>hora do dia (00-23)</td>
</tr>
<tr>
<td>
<code class="literal">
     MI
    </code>
</td>
<td>minuto (00–59)</td>
</tr>
<tr>
<td>
<code class="literal">
     SS
    </code>
</td>
<td>segundo (00–59)</td>
</tr>
<tr>
<td>
<code class="literal">
     MS
    </code>
</td>
<td>milisegundo (000–999)</td>
</tr>
<tr>
<td>
<code class="literal">
     US
    </code>
</td>
<td>microssegundo (000000–999999)</td>
</tr>
<tr>
<td>
<code class="literal">
     FF1
    </code>
</td>
<td>décimo de segundo (0–9)</td>
</tr>
<tr>
<td>
<code class="literal">
     FF2
    </code>
</td>
<td>centésimo de segundo (00–99)</td>
</tr>
<tr>
<td>
<code class="literal">
     FF3
    </code>
</td>
<td>milisegundo (000–999)</td>
</tr>
<tr>
<td>
<code class="literal">
     FF4
    </code>
</td>
<td>décimo de um milissegundo (0000–9999)</td>
</tr>
<tr>
<td>
<code class="literal">
     FF5
    </code>
</td>
<td>centésimo de um milissegundo (00000–99999)</td>
</tr>
<tr>
<td>
<code class="literal">
     FF6
    </code>
</td>
<td>microssegundo (000000–999999)</td>
</tr>
<tr>
<td>
<code class="literal">
     SSSS
    </code>
    ,
    <code class="literal">
     SSSSS
    </code>
</td>
<td>segundos após a meia-noite (0–86399)</td>
</tr>
<tr>
<td>
<code class="literal">
     AM
    </code>
    ,
    <code class="literal">
     am
    </code>
    ,
    <code class="literal">
     PM
    </code>
    or
    <code class="literal">
     pm
    </code>
</td>
<td>indicador meridiem (sem períodos)</td>
</tr>
<tr>
<td>
<code class="literal">
     A.M.
    </code>
    ,
    <code class="literal">
     a.m.
    </code>
    ,
    <code class="literal">
     P.M.
    </code>
    or
    <code class="literal">
     p.m.
    </code>
</td>
<td>indicador meridiem (com períodos)</td>
</tr>
<tr>
<td>
<code class="literal">
     Y,YYY
    </code>
</td>
<td>ano (4 ou mais dígitos) com vírgula</td>
</tr>
<tr>
<td>
<code class="literal">
     YYYY
    </code>
</td>
<td>ano (4 ou mais dígitos)</td>
</tr>
<tr>
<td>
<code class="literal">
     YYY
    </code>
</td>
<td>últimos 3 dígitos do ano</td>
</tr>
<tr>
<td>
<code class="literal">
     YY
    </code>
</td>
<td>últimos 2 dígitos do ano</td>
</tr>
<tr>
<td>
<code class="literal">
     Y
    </code>
</td>
<td>última cifra do ano</td>
</tr>
<tr>
<td>
<code class="literal">
     IYYY
    </code>
</td>
<td>Ano com numeração de semana ISO 8601 (4 ou mais dígitos)</td>
</tr>
<tr>
<td>
<code class="literal">
     IYY
    </code>
</td>
<td>últimos 3 dígitos do ano de numeração de semana ISO 8601</td>
</tr>
<tr>
<td>
<code class="literal">
     IY
    </code>
</td>
<td>últimas 2 dígitos do ano de numeração de semana ISO 8601</td>
</tr>
<tr>
<td>
<code class="literal">
     I
    </code>
</td>
<td>última cifra do ano de numeração de semana ISO 8601</td>
</tr>
<tr>
<td>
<code class="literal">
     BC
    </code>
    ,
    <code class="literal">
     bc
    </code>
    ,
    <code class="literal">
     AD
    </code>
    or
    <code class="literal">
     ad
    </code>
</td>
<td>indicador de era (sem pontos)</td>
</tr>
<tr>
<td>
<code class="literal">
     B.C.
    </code>
    ,
    <code class="literal">
     b.c.
    </code>
    ,
    <code class="literal">
     A.D.
    </code>
    or
    <code class="literal">
     a.d.
    </code>
</td>
<td>indicador de era (com períodos)</td>
</tr>
<tr>
<td>
<code class="literal">
     MONTH
    </code>
</td>
<td>nome do mês em maiúsculas completas (preenchido com espaços em branco até 9 caracteres)</td>
</tr>
<tr>
<td>
<code class="literal">
     Month
    </code>
</td>
<td>nome do mês em maiúsculas (preenchido com espaços em branco até 9 caracteres)</td>
</tr>
<tr>
<td>
<code class="literal">
     month
    </code>
</td>
<td>nome do mês em minúsculas (preenchido com espaços em branco até 9 caracteres)</td>
</tr>
<tr>
<td>
<code class="literal">
     MON
    </code>
</td>
<td>nome do mês em maiúsculas abreviado (3 caracteres em inglês, comprimentos localizados variam)</td>
</tr>
<tr>
<td>
<code class="literal">
     Mon
    </code>
</td>
<td>nome do mês abreviado em maiúsculas (3 caracteres em inglês, comprimentos localizados variam)</td>
</tr>
<tr>
<td>
<code class="literal">
     mon
    </code>
</td>
<td>nome do mês em letra minúscula abreviado (3 caracteres em inglês, comprimentos localizados variam)</td>
</tr>
<tr>
<td>
<code class="literal">
     MM
    </code>
</td>
<td>número do mês (01–12)</td>
</tr>
<tr>
<td>
<code class="literal">
     DAY
    </code>
</td>
<td>nome do dia em maiúsculas completas (preenchido com espaços em branco até 9 caracteres)</td>
</tr>
<tr>
<td>
<code class="literal">
     Day
    </code>
</td>
<td>nome do dia em maiúsculas (preenchido com espaços em branco até 9 caracteres)</td>
</tr>
<tr>
<td>
<code class="literal">
     day
    </code>
</td>
<td>nome do dia em maiúsculas completas (preenchido com espaços em branco até 9 caracteres)</td>
</tr>
<tr>
<td>
<code class="literal">
     DY
    </code>
</td>
<td>nome do dia em maiúsculas abreviado (3 caracteres em inglês, comprimentos localizados variam)</td>
</tr>
<tr>
<td>
<code class="literal">
     Dy
    </code>
</td>
<td>nome do dia abreviado em maiúsculas (3 caracteres em inglês, comprimentos localizados variam)</td>
</tr>
<tr>
<td>
<code class="literal">
     dy
    </code>
</td>
<td>nome do dia em letra minúscula abreviada (3 caracteres em inglês, comprimentos localizados variam)</td>
</tr>
<tr>
<td>
<code class="literal">
     DDD
    </code>
</td>
<td>dia do ano (001–366)</td>
</tr>
<tr>
<td>
<code class="literal">
     IDDD
    </code>
</td>
<td>dia do ano de numeração de semana ISO 8601 (001-371; o dia 1 do ano é segunda-feira da primeira semana ISO)</td>
</tr>
<tr>
<td>
<code class="literal">
     DD
    </code>
</td>
<td>dia do mês (01–31)</td>
</tr>
<tr>
<td>
<code class="literal">
     D
    </code>
</td>
<td>dia da semana, domingo (<code class="literal">
     1
    </code>) até sábado (<code class="literal">
     7
    </code>)</td>
</tr>
<tr>
<td>
<code class="literal">
     ID
    </code>
</td>
<td>dia da semana segundo o ISO 8601, segunda-feira (<code class="literal">
     1
    </code>) até domingo (<code class="literal">
     7
    </code>)</td>
</tr>
<tr>
<td>
<code class="literal">
     W
    </code>
</td>
<td>semana do mês (1-5) (a primeira semana começa no primeiro dia do mês)</td>
</tr>
<tr>
<td>
<code class="literal">
     WW
    </code>
</td>
<td>número da semana do ano (1-53) (a primeira semana começa no primeiro dia do ano)</td>
</tr>
<tr>
<td>
<code class="literal">
     IW
    </code>
</td>
<td>número de semana do ano de numeração de semana ISO 8601 (01-53; o primeiro quarteirão do ano está na semana 1)</td>
</tr>
<tr>
<td>
<code class="literal">
     CC
    </code>
</td>
<td>século (2 dígitos) (o vigésimo primeiro século começa em 2001-01-01)</td>
</tr>
<tr>
<td>
<code class="literal">
     J
    </code>
</td>
<td>Julian Date (dias inteiros desde 24 de novembro de 4714 a.C., à meia-noite local; veja<a class="xref" href="datetime-julian-dates.md" title="B.7. Julian Dates">Seção B.7</a>)</td>
</tr>
<tr>
<td>
<code class="literal">
     Q
    </code>
</td>
<td>trimestre</td>
</tr>
<tr>
<td>
<code class="literal">
     RM
    </code>
</td>
<td>mês em maiúsculas de numeração romana (I–XII; I=Janeiro)</td>
</tr>
<tr>
<td>
<code class="literal">
     rm
    </code>
</td>
<td>mês em números romanos minúsculos (i–xii; i=janeiro)</td>
</tr>
<tr>
<td>
<code class="literal">
     TZ
    </code>
</td>
<td>abreviação do fuso horário em maiúsculas</td>
</tr>
<tr>
<td>
<code class="literal">
     tz
    </code>
</td>
<td>abreviação de fuso horário em minúsculas</td>
</tr>
<tr>
<td>
<code class="literal">
     TZH
    </code>
</td>
<td>horas no fuso horário</td>
</tr>
<tr>
<td>
<code class="literal">
     TZM
    </code>
</td>
<td>minutos de fuso horário</td>
</tr>
<tr>
<td>
<code class="literal">
     OF
    </code>
</td>
<td>deslocamento do fuso horário em relação ao UTC (<em class="replaceable">
<code>
      HH
     </code>
</em>ou<em class="replaceable">
<code>
      HH
     </code>
</em>
<code class="literal">
     :
    </code>
<em class="replaceable">
<code>
      MM
     </code>
</em>)</td>
</tr>
</tbody>
</table>




  

Modificadores podem ser aplicados a qualquer padrão de modelo para alterar seu comportamento. Por exemplo, `FMMonth` é o padrão `Month` com o modificador `FM`. [Tabela 9.28][(functions-formatting.md#FUNCTIONS-FORMATTING-DATETIMEMOD-TABLE "Table 9.28. Template Pattern Modifiers for Date/Time Formatting")] mostra os padrões de modificadores para formatação de data/hora.

**Tabela 9.28. Modificadores de Padrão de Modelo para Formatação de Data/Hora**



<table border="1" class="table" summary="Template Pattern Modifiers for Date/Time Formatting">
<colgroup>
<col/>
<col/>
<col/>
</colgroup>
<thead>
<tr>
<th>
    Modifier
   </th>
<th>Descrição</th>
<th>
    Example
   </th>
</tr>
</thead>
<tbody>
<tr>
<td>
<code class="literal">
     FM
    </code>
    prefix
   </td>
<td>modo de preenchimento (supressão de zeros iniciais e espaços de preenchimento)</td>
<td>
<code class="literal">
     FMMonth
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     TH
    </code>
    suffix
   </td>
<td>sufixo de número ordinal maiúsculo</td>
<td>
<code class="literal">
     DDTH
    </code>
    , e.g.,
    <code class="literal">
     12TH
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     th
    </code>
    suffix
   </td>
<td>sufixo de número ordinal em letra minúscula</td>
<td>
<code class="literal">
     DDth
    </code>
    , e.g.,
    <code class="literal">
     12th
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     FX
    </code>
    prefix
   </td>
<td>opção de formato fixo global (consulte as notas de uso)</td>
<td>
<code class="literal">
     FX Month DD Day
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     TM
    </code>
    prefix
   </td>
<td>modo de tradução (use nomes de dia e mês localizados com base em<a class="xref" href="runtime-config-client.md#GUC-LC-TIME">
     lc_time
    </a>)</td>
<td>
<code class="literal">
     TMMonth
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     SP
    </code>
    suffix
   </td>
<td>modo de digitação (não implementado)</td>
<td>
<code class="literal">
     DDSP
    </code>
</td>
</tr>
</tbody>
</table>




  

Observações de uso para formatação de data/hora:

* `FM` suprime zeros principais e espaços finais que, de outra forma, seriam adicionados para fixar a largura de saída de um padrão. No PostgreSQL, `FM` modifica apenas a próxima especificação, enquanto no Oracle `FM` afeta todas as especificações subsequentes, e os modificadores repetidos `FM` alternam o modo de preenchimento ligado e desligado.
* `TM` suprime espaços finais, independentemente de `FM` ser especificado.
* `to_timestamp` e `to_date` ignoram a grafia das letras na entrada; portanto, por exemplo, `MON`, `Mon` e `mon` aceitam todas as mesmas strings. Ao usar o modificador `TM`, a dobragem de caracteres é feita de acordo com as regras da collation de entrada da função (ver [Seção 23.2][(collation.md "23.2. Collation Support")]).
* `to_timestamp` e `to_date` ignoram múltiplos espaços em branco no início da string de entrada e ao redor dos valores de data e hora, a menos que a opção `FX` seja usada. Por exemplo, `to_timestamp(' 2000    JUN', 'YYYY MON')` e `to_timestamp('2000 - JUN', 'YYYY-MON')` funcionam, mas `to_timestamp('2000    JUN', 'FXYYYY MON')` retorna um erro porque `to_timestamp` espera apenas um único espaço. `FX` deve ser especificado como o primeiro item no modelo.
* Um separador (um espaço ou um caractere não letra/não dígito) na string de template de `to_timestamp` e `to_date` corresponde a qualquer separador único na string de entrada ou é ignorado, a menos que a opção `FX` seja usada. Por exemplo, `to_timestamp('2000JUN', 'YYYY///MON')` e `to_timestamp('2000/JUN', 'YYYY MON')` funcionam, mas `to_timestamp('2000//JUN', 'YYYY/MON')` retorna um erro porque o número de separadores na string de entrada excede o número de separadores no modelo.

Se `FX` for especificado, um separador na string de modelo corresponde exatamente a um caractere na string de entrada. Mas observe que o caractere da string de entrada não precisa ser o mesmo que o separador da string de modelo. Por exemplo, `to_timestamp('2000/JUN', 'FXYYYY MON')` funciona, mas `to_timestamp('2000/JUN', 'FXYYYY  MON')` retorna um erro porque o segundo espaço na string de modelo consome a letra `J` da string de entrada.
* Um padrão de modelo `TZH` pode corresponder a um número assinado. Sem a opção `FX`, os sinais de menos podem ser ambíguos e poderiam ser interpretados como um separador. Essa ambiguidade é resolvida da seguinte forma: Se o número de separadores antes de `TZH` na string de modelo for menor que o número de separadores antes do sinal de menos na string de entrada, o sinal de menos é interpretado como parte de `TZH`. Caso contrário, o sinal de menos é considerado um separador entre valores. Por exemplo, `to_timestamp('2000 -10', 'YYYY TZH')` corresponde a `-10` até `TZH`, mas `to_timestamp('2000 -10', 'YYYY  TZH')` corresponde a `10` até `TZH`.
* Texto comum é permitido em modelos `to_char` e será emitido literalmente. Você pode colocar uma substring em aspas duplas para forçar que seja interpretada como texto literal, mesmo que contenha padrões de modelo. Por exemplo, em `'"Hello Year "YYYY'`, o `YYYY` será substituído pelos dados do ano, mas o único `Y` em `Year` não será. Em `to_date`, `to_number` e `to_timestamp`, texto literal e strings com aspas duplas resultam na omissão do número de caracteres contidos na string; por exemplo, `"XX"` omite dois caracteres de entrada (seja ou não eles sejam `XX`).

### DICA

Antes do PostgreSQL 12, era possível ignorar texto arbitrário na string de entrada usando caracteres não letra ou não dígito. Por exemplo, `to_timestamp('2000y6m1d', 'yyyy-MM-DD')` costumava funcionar. Agora, você só pode usar caracteres letra para esse propósito. Por exemplo, `to_timestamp('2000y6m1d', 'yyyytMMtDDt')` e `to_timestamp('2000y6m1d', 'yyyy"y"MM"m"DD"d"')` ignoram `y`, `m` e `d`.
* Se você quiser ter uma citação dupla na saída, deve precedê-la com uma barra invertida, por exemplo, `'\"YYYY Month\"'`. Barras invertidas não são especiais de outra forma, exceto em strings com citações duplas. Dentro de uma string com citações duplas, uma barra invertida faz com que o próximo caractere seja tomado literalmente, o que quer que seja (mas isso não tem efeito especial a menos que o próximo caractere seja uma citação dupla ou outra barra invertida).
* Em `to_timestamp` e `to_date`, se a especificação do formato do ano tiver menos de quatro dígitos, por exemplo, `YYY`, e o ano fornecido tiver menos de quatro dígitos, o ano será ajustado para ser o mais próximo do ano 2020, por exemplo, `95` se torna 1995.
* Em `to_timestamp` e `to_date`, os anos negativos são tratados como significando BC. Se você escrever tanto um ano negativo quanto um campo explícito `BC`, você obtém AD novamente. Uma entrada de ano zero é tratada como 1 BC.
* Em `to_timestamp` e `to_date`, a conversão `YYYY` tem uma restrição ao processar anos com mais de 4 dígitos. Você deve usar algum caractere não dígito ou modelo após `YYYY`, caso contrário, o ano é sempre interpretado como 4 dígitos. Por exemplo (com o ano 20000): `to_date('200001130', 'YYYYMMDD')` será interpretado como um ano de 4 dígitos; em vez disso, use um separador não dígito após o ano, como `to_date('20000-1130', 'YYYY-MMDD')` ou `to_date('20000Nov30', 'YYYYMonDD')`.
* Em `to_timestamp` e `to_date`, o campo `CC` (século) é aceito, mas ignorado se houver um campo `YYY`, `YYYY` ou `Y,YYY`. Se `CC` é usado com `YY` ou `Y`, então o resultado é calculado como esse ano no século especificado. Se o século é especificado, mas o ano não, o primeiro ano do século é assumido.
* Em `to_timestamp` e `to_date`, os nomes ou números de dias da semana (`DAY`, `D` e tipos de campo relacionados) são aceitos, mas ignorados para fins de cálculo do resultado. O mesmo vale para campos de trimestre (`Q`).
* Em `to_timestamp` e `to_date`, uma data de numeração de semana ISO 8601 (diferente de uma data gregoriana) pode ser especificada de uma das duas maneiras:

+ Ano, número de semana e dia da semana: por exemplo, `to_date('2006-42-4', 'IYYY-IW-ID')` retorna a data `2006-10-19`. Se você omitir o dia da semana, é assumido que seja 1 (Segunda-feira).
+ Ano e dia do ano: por exemplo, `to_date('2006-291', 'IYYY-IDDD')` também retorna `2006-10-19`.

Tentar inserir uma data usando uma mistura de campos de numeração de semana ISO 8601 e campos de data gregoriana é sem sentido e causará um erro. No contexto de um ano de numeração de semana ISO 8601, o conceito de "mês" ou "dia do mês" não tem significado. No contexto de um ano gregoriano, a semana ISO não tem significado.

### Atenção

Embora `to_date` rejeite uma mistura de campos de data com numeração de semana gregoriana e ISO, `to_char` não o fará, uma vez que as especificações de formato de saída, como `YYYY-MM-DD (IYYY-IDDD)`, podem ser úteis. Mas evite escrever algo como `IYYY-MM-DD`; isso resultaria em resultados surpreendentes perto do início do ano. (Veja [Seção 9.9.1][(functions-datetime.md#FUNCTIONS-DATETIME-EXTRACT "9.9.1. EXTRACT, date_part")] para mais informações.)
* Em `to_timestamp`, campos de milissegundo (`MS`) ou microssegundo (`US`) são usados como dígitos de segundos após o ponto decimal. Por exemplo, `to_timestamp('12.3', 'SS.MS')` não é de 3 milissegundos, mas sim 300, porque a conversão o trata como 12 + 0,3 segundos. Portanto, para o formato `SS.MS`, os valores de entrada `12.3`, `12.30` e `12.300` especificam o mesmo número de milissegundos. Para obter três milissegundos, é necessário escrever `12.003`, que a conversão trata como 12 + 0,003 = 12,003 segundos.

Aqui está um exemplo mais complexo: `to_timestamp('15:12:02.020.001230', 'HH24:MI:SS.MS.US')` é de 15 horas, 12 minutos e 2 segundos + 20 milissegundos + 1230 microsegundos = 2,021230 segundos.
* O dia da semana de numeração de `to_char(..., 'ID')` corresponde à função `extract(isodow from ...)`, mas o de `to_char(..., 'D')` não corresponde ao de `extract(dow from ...)`.
* `to_char(interval)` formata `HH` e `HH12` como mostrado em um relógio de 12 horas, por exemplo, as horas zero e 36 horas, ambas saem como `12`, enquanto `HH24` emite o valor completo da hora, que pode exceder 23 em um valor de `interval`.

[Tabela 9.29][(functions-formatting.md#FUNCTIONS-FORMATTING-NUMERIC-TABLE "Table 9.29. Template Patterns for Numeric Formatting")] mostra os padrões de modelo disponíveis para formatação de valores numéricos.

**Tabela 9.29. Padrões de modelo para formatação numérica**



<table border="1" class="table" summary="Template Patterns for Numeric Formatting">
<colgroup>
<col/>
<col/>
</colgroup>
<thead>
<tr>
<th>
    Pattern
   </th>
<th>Descrição</th>
</tr>
</thead>
<tbody>
<tr>
<td>
<code class="literal">
     9
    </code>
</td>
<td>posição do dígito (pode ser descartada se insignificante)</td>
</tr>
<tr>
<td>
<code class="literal">
     0
    </code>
</td>
<td>posição do dígito (não será descartada, mesmo que insignificante)</td>
</tr>
<tr>
<td>
<code class="literal">
     .
    </code>
    (period)
   </td>
<td>ponto decimal</td>
</tr>
<tr>
<td>
<code class="literal">
     ,
    </code>
    (comma)
   </td>
<td>separador de grupo (milhares)</td>
</tr>
<tr>
<td>
<code class="literal">
     PR
    </code>
</td>
<td>valor negativo entre colchetes</td>
</tr>
<tr>
<td>
<code class="literal">
     S
    </code>
</td>
<td>assinatura ancorada ao número (usa o local)</td>
</tr>
<tr>
<td>
<code class="literal">
     L
    </code>
</td>
<td>símbolo de moeda (usa o local)</td>
</tr>
<tr>
<td>
<code class="literal">
     D
    </code>
</td>
<td>ponto decimal (utiliza o local)</td>
</tr>
<tr>
<td>
<code class="literal">
     G
    </code>
</td>
<td>separador de grupo (usa o local)</td>
</tr>
<tr>
<td>
<code class="literal">
     MI
    </code>
</td>
<td>sinal de menos na posição especificada (se o número for menor que 0)</td>
</tr>
<tr>
<td>
<code class="literal">
     PL
    </code>
</td>
<td>sinal de mais na posição especificada (se o número for maior que 0)</td>
</tr>
<tr>
<td>
<code class="literal">
     SG
    </code>
</td>
<td>sinal de mais/menos na posição especificada</td>
</tr>
<tr>
<td>
<code class="literal">
     RN
    </code>
    or
    <code class="literal">
     rn
    </code>
</td>
<td>Número romano (valores entre 1 e 3999)</td>
</tr>
<tr>
<td>
<code class="literal">
     TH
    </code>
    or
    <code class="literal">
     th
    </code>
</td>
<td>sufixo de número ordinal</td>
</tr>
<tr>
<td>
<code class="literal">
     V
    </code>
</td>
<td>alterar o número especificado de dígitos (ver notas)</td>
</tr>
<tr>
<td>
<code class="literal">
     EEEE
    </code>
</td>
<td>expoente para notação científica</td>
</tr>
</tbody>
</table>




  

Observações de uso para formatação numérica:

* `0` especifica uma posição de dígito que será sempre impressa, mesmo que contenha um zero inicial/final. `9` também especifica uma posição de dígito, mas se for um zero inicial, ele será substituído por um espaço, enquanto se for um zero final e o modo de preenchimento for especificado, ele será excluído. (Para `to_number()`, esses dois caracteres de padrão são equivalentes.)
* Se o formato fornecer menos dígitos fracionários do que o número sendo formatado, `to_char()` arredondará o número para o número especificado de dígitos fracionários.
* Os caracteres de padrão `S`, `L`, `D` e `G` representam o sinal, o símbolo de moeda, o ponto decimal e os caracteres de separador de milhares definidos pelo local atual (ver [lc_monetary][(runtime-config-client.md#GUC-LC-MONETARY)] e [lc_numeric][(runtime-config-client.md#GUC-LC-NUMERIC)]). Os caracteres de período e vírgula representam esses caracteres exatos, com os significados de ponto decimal e separador de milhares, independentemente do local.
* Se nenhuma disposição explícita for feita para um sinal no padrão de `to_char()`, uma coluna será reservada para o sinal, e ele será ancorado (aparecerá logo à esquerda) do número. Se `S` aparecer logo à esquerda de alguns de `9`, ele também será ancorado ao número.
* Um sinal formatado usando `SG`, `PL` ou `MI` não é ancorado ao número; por exemplo, `to_char(-12, 'MI9999')` produz `'-  12'`, mas `to_char(-12, 'S9999')` produz `'  -12'`. (A implementação do Oracle não permite o uso de `MI` antes de `9`, mas exige que `9` preceeda `MI`.))
* `TH` não converte valores menores que zero e não converte números fracionários.
* `PL`, `SG` e `TH` são extensões do PostgreSQL.
* Em `to_number`, se padrões de template não-dados, como `L` ou `TH`, forem usados, o número correspondente de caracteres de entrada será ignorado, independentemente de eles corresponderem ao padrão de template, a menos que sejam caracteres de dados (ou seja, dígitos, sinal, ponto decimal ou vírgula). Por exemplo, `TH` ignoraria dois caracteres não-dados.
* `V` com `to_char` multiplica os valores de entrada por `10^n`, onde *`n`* é o número de dígitos após `V`. `V` com `to_number` divide de maneira semelhante. O `V` pode ser pensado como marcando a posição de um ponto decimal implícito na string de entrada ou saída. `to_char` e `to_number` não suportam o uso de `V` combinado com um ponto decimal (e.g., `99.9V99` não é permitido).
* `EEEE` (notação científica) não pode ser usado em combinação com qualquer um dos outros padrões de formatação ou modificadores, exceto padrões de dígito e ponto decimal, e deve estar no final da string de formatação (e.g., `9.99EEEE` é um padrão válido).
* Em `to_number()`, o padrão `RN` converte números romanos (em forma padrão) em números. A entrada é insensível ao caso, então `RN` e `rn` são equivalentes. `RN` não pode ser usado em combinação com qualquer outro padrão de formatação ou modificador, exceto `FM`, que é aplicável apenas em `to_char()` e é ignorado em `to_number()`.

Certos modificadores podem ser aplicados a qualquer padrão de modelo para alterar seu comportamento. Por exemplo, `FM99.99` é o padrão `99.99` com o modificador `FM`. [Tabela 9.30](functions-formatting.md#FUNCTIONS-FORMATTING-NUMERICMOD-TABLE "Table 9.30. Template Pattern Modifiers for Numeric Formatting") mostra os padrões de modificadores para formatação numérica.

**Tabela 9.30. Modificadores de Padrão de Modelo para Formatação Numérica**



<table border="1" class="table" summary="Template Pattern Modifiers for Numeric Formatting">
<colgroup>
<col/>
<col/>
<col/>
</colgroup>
<thead>
<tr>
<th>
    Modifier
   </th>
<th>Descrição</th>
<th>
    Example
   </th>
</tr>
</thead>
<tbody>
<tr>
<td>
<code class="literal">
     FM
    </code>
    prefix
   </td>
<td>modo de preenchimento (supressão de zeros finais e espaços de preenchimento)</td>
<td>
<code class="literal">
     FM99.99
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     TH
    </code>
    suffix
   </td>
<td>sufixo de número ordinal maiúsculo</td>
<td>
<code class="literal">
     999TH
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     th
    </code>
    suffix
   </td>
<td>sufixo de número ordinal em letra minúscula</td>
<td>
<code class="literal">
     999th
    </code>
</td>
</tr>
</tbody>
</table>




  

[Tabela 9.31][(functions-formatting.md#FUNCTIONS-FORMATTING-EXAMPLES-TABLE "Table 9.31. to_char Examples")] mostra alguns exemplos do uso da função `to_char`.

**Tabela 9.31. Exemplos de `to_char`**



<table border="1" class="table" summary="to_char Examples">
<colgroup>
<col/>
<col/>
</colgroup>
<thead>
<tr>
<th>
    Expression
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
     to_char(current_timestamp, 'Day, DD  HH12:MI:SS')
    </code>
</td>
<td>
<code class="literal">
     'Tuesday  , 06  05:39:18'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(current_timestamp, 'FMDay, FMDD  HH12:MI:SS')
    </code>
</td>
<td>
<code class="literal">
     'Tuesday, 6  05:39:18'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(current_timestamp AT TIME ZONE
        'UTC', 'YYYY-MM-DD"T"HH24:MI:SS"Z"')
    </code>
</td>
<td>
<code class="literal">
     '2022-12-06T05:39:18Z'
    </code>
    ,
    <acronym class="acronym">
     ISO
    </acronym>
    8601 extended format
   </td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(-0.1, '99.99')
    </code>
</td>
<td>
<code class="literal">
     '  -.10'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(-0.1, 'FM9.99')
    </code>
</td>
<td>
<code class="literal">
     '-.1'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(-0.1, 'FM90.99')
    </code>
</td>
<td>
<code class="literal">
     '-0.1'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(0.1, '0.9')
    </code>
</td>
<td>
<code class="literal">
     ' 0.1'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(12, '9990999.9')
    </code>
</td>
<td>
<code class="literal">
     '    0012.0'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(12, 'FM9990999.9')
    </code>
</td>
<td>
<code class="literal">
     '0012.'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(485, '999')
    </code>
</td>
<td>
<code class="literal">
     ' 485'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(-485, '999')
    </code>
</td>
<td>
<code class="literal">
     '-485'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(485, '9 9 9')
    </code>
</td>
<td>
<code class="literal">
     ' 4 8 5'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(1485, '9,999')
    </code>
</td>
<td>
<code class="literal">
     ' 1,485'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(1485, '9G999')
    </code>
</td>
<td>
<code class="literal">
     ' 1 485'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(148.5, '999.999')
    </code>
</td>
<td>
<code class="literal">
     ' 148.500'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(148.5, 'FM999.999')
    </code>
</td>
<td>
<code class="literal">
     '148.5'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(148.5, 'FM999.990')
    </code>
</td>
<td>
<code class="literal">
     '148.500'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(148.5, '999D999')
    </code>
</td>
<td>
<code class="literal">
     ' 148,500'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(3148.5, '9G999D999')
    </code>
</td>
<td>
<code class="literal">
     ' 3 148,500'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(-485, '999S')
    </code>
</td>
<td>
<code class="literal">
     '485-'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(-485, '999MI')
    </code>
</td>
<td>
<code class="literal">
     '485-'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(485, '999MI')
    </code>
</td>
<td>
<code class="literal">
     '485 '
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(485, 'FM999MI')
    </code>
</td>
<td>
<code class="literal">
     '485'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(485, 'PL999')
    </code>
</td>
<td>
<code class="literal">
     '+485'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(485, 'SG999')
    </code>
</td>
<td>
<code class="literal">
     '+485'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(-485, 'SG999')
    </code>
</td>
<td>
<code class="literal">
     '-485'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(-485, '9SG99')
    </code>
</td>
<td>
<code class="literal">
     '4-85'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(-485, '999PR')
    </code>
</td>
<td>
<code class="literal">
     '&lt;485&gt;'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(485, 'L999')
    </code>
</td>
<td>
<code class="literal">
     'DM 485'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(485, 'RN')
    </code>
</td>
<td>
<code class="literal">
     '        CDLXXXV'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(485, 'FMRN')
    </code>
</td>
<td>
<code class="literal">
     'CDLXXXV'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(5.2, 'FMRN')
    </code>
</td>
<td>
<code class="literal">
     'V'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(482, '999th')
    </code>
</td>
<td>
<code class="literal">
     ' 482nd'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(485, '"Good number:"999')
    </code>
</td>
<td>
<code class="literal">
     'Good number: 485'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(485.8, '"Pre:"999" Post:" .999')
    </code>
</td>
<td>
<code class="literal">
     'Pre: 485 Post: .800'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(12, '99V999')
    </code>
</td>
<td>
<code class="literal">
     ' 12000'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(12.4, '99V999')
    </code>
</td>
<td>
<code class="literal">
     ' 12400'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(12.45, '99V9')
    </code>
</td>
<td>
<code class="literal">
     ' 125'
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     to_char(0.0004859, '9.99EEEE')
    </code>
</td>
<td>
<code class="literal">
     ' 4.86e-04'
    </code>
</td>
</tr>
</tbody>
</table>


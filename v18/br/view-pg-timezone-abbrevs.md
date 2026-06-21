## 53.33. `pg_timezone_abbrevs` [#](#VIEW-PG-TIMEZONE-ABBREVS)

A vista `pg_timezone_abbrevs` fornece uma lista de abreviações de fuso horário que são atualmente reconhecidas pelas rotinas de entrada de datetime. O conteúdo desta vista muda quando os parâmetros de tempo de execução [TimeZone](runtime-config-client.md#GUC-TIMEZONE) ou [timezone_abbreviations](runtime-config-client.md#GUC-TIMEZONE-ABBREVIATIONS) são modificados.

**Tabela 53.33. Colunas `pg_timezone_abbrevs`**



<table border="1" class="table" summary="pg_timezone_abbrevs Columns">
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="catalog_table_entry">
    <p class="column_definition">
     Tipo de coluna
    </p>
    <p>
     Descrição
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      abbrev
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Abreviação do fuso horário
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      utc_offset
     </code>
     <code class="type">
      interval
     </code>
    </p>
    <p>
     Deslocamento em relação ao UTC (positivo significa leste de Greenwich)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      is_dst
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Verdadeiro se esta é uma abreviação de horário de verão
    </p>
   </td>
  </tr>
 </tbody>
</table>









Enquanto a maioria das abreviações de fuso horário representam desvios fixos em relação ao UTC, há algumas que historicamente variaram em valor (consulte a Seção B.4 para mais informações). Nesses casos, essa visão apresenta seu significado atual.
## 53.34. `pg_timezone_names` [#](#VIEW-PG-TIMEZONE-NAMES)

A vista `pg_timezone_names` fornece uma lista de nomes de fuso horário reconhecidos por `SET TIMEZONE`, juntamente com suas abreviações associadas, deslocamentos UTC e status de poupança de luz solar. (Tecnicamente, o PostgreSQL não usa UTC porque os segundos intercalares não são tratados.) Ao contrário das abreviações mostradas em [`pg_timezone_abbrevs`](view-pg-timezone-abbrevs.md "53.33. pg_timezone_abbrevs"), muitos desses nomes implicam um conjunto de regras de data de transição de poupança de luz solar. Portanto, as informações associadas mudam através dos limites locais do DST. As informações exibidas são calculadas com base no valor atual de `CURRENT_TIMESTAMP`.

**Tabela 53.34. Colunas `pg_timezone_names`**



<table border="1" class="table" summary="pg_timezone_names Columns">
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
      name
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Nome do fuso horário
    </p>
   </td>
  </tr>
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
     Verdadeiro se atualmente está observando o horário de verão
    </p>
   </td>
  </tr>
 </tbody>
</table>






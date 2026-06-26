## 35.47. `sequences` [#](#INFOSCHEMA-SEQUENCES)

A vista `sequences` contém todas as sequências definidas no banco de dados atual. Apenas as sequências que o usuário atual tem acesso (como proprietário ou com algum privilégio) são mostradas.

**Tabela 35.45. Colunas `sequences`**



<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="catalog_table_entry">
    <p class="column_definition">
     Column Type
    </p>
    <p>
     Description
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      sequence_catalog
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the database that contains the sequence (always the current database)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      sequence_schema
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the schema that contains the sequence
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      sequence_name
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the sequence
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      data_type
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     The data type of the sequence.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      numeric_precision
     </code>
     <code>
      cardinal_number
     </code>
    </p>
    <p>
     This column contains the (declared or implicit) precision of the sequence data type (see above).  The precision indicates the number of significant digits.  It can be expressed in decimal (base 10) or binary (base 2) terms, as specified in the column
     <code>
      numeric_precision_radix
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      numeric_precision_radix
     </code>
     <code>
      cardinal_number
     </code>
    </p>
    <p>
     This column indicates in which base the values in the columns
     <code>
      numeric_precision
     </code>
     and
     <code>
      numeric_scale
     </code>
     are expressed.  The value is either 2 or 10.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      numeric_scale
     </code>
     <code>
      cardinal_number
     </code>
    </p>
    <p>
     This column contains the (declared or implicit) scale of the sequence data type (see above).  The scale indicates the number of significant digits to the right of the decimal point.  It can be expressed in decimal (base 10) or binary (base 2) terms, as specified in the column
     <code>
      numeric_precision_radix
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      start_value
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     The start value of the sequence
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      minimum_value
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     The minimum value of the sequence
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      maximum_value
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     The maximum value of the sequence
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      increment
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     The increment of the sequence
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      cycle_option
     </code>
     <code>
      yes_or_no
     </code>
    </p>
    <p>
     <code>
      YES
     </code>
     if the sequence cycles, else
     <code>
      NO
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>










Observe que, de acordo com o padrão SQL, os valores de início, mínimo, máximo e incremento são retornados como cadeias de caracteres.
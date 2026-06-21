## 35.42. `routine_routine_usage` [#](#INFOSCHEMA-ROUTINE-ROUTINE-USAGE)

A visão `routine_routine_usage` identifica todas as funções ou procedimentos que são usados por outra (ou a mesma) função ou procedimento, seja no corpo do SQL ou em expressões de padrão de parâmetro. (Isso só funciona para corpos de SQL não citados, não corpos ou funções com citação ou em outros idiomas.) Uma entrada é incluída aqui apenas se a função usada for de propriedade de um papel atualmente habilitado. (Não há tal restrição na função usando.)

Observe que as entradas para ambas as funções na visualização fazem referência ao nome “específico” da rotina, mesmo que os nomes das colunas sejam usados de uma maneira inconsistente com outras visualizações do esquema de informações sobre rotinas. Isso é de acordo com o padrão SQL, embora seja, sem dúvida, um mau projeto. Consulte [Seção 35.45](infoschema-routines.md) para obter mais informações sobre nomes específicos.

**Tabela 35.40. Colunas `routine_routine_usage`**



<table border="1" class="table" summary="routine_routine_usage Columns">
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
     <code class="structfield">
      specific_catalog
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     Name of the database containing the using function (always the current database)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      specific_schema
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     Name of the schema containing the using function
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      specific_name
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     The
     <span class="quote">
      “
      <span class="quote">
       specific name
      </span>
      ”
     </span>
     of the using function.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      routine_catalog
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     Name of the database that contains the function that is used by the first function (always the current database)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      routine_schema
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     Name of the schema that contains the function that is used by the first function
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      routine_name
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     The
     <span class="quote">
      “
      <span class="quote">
       specific name
      </span>
      ”
     </span>
     of the function that is used by the first function.
    </p>
   </td>
  </tr>
 </tbody>
</table>






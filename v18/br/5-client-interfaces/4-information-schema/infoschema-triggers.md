## 35.57. `triggers` [#](#INFOSCHEMA-TRIGGERS)

A vista `triggers` contém todos os gatilhos definidos no banco de dados atual em tabelas e vistas que o usuário atual possui ou tem algum privilégio diferente de `SELECT`.

**Tabela 35.55. Colunas `triggers`**



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
      trigger_catalog
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the database that contains the trigger (always the current database)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      trigger_schema
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the schema that contains the trigger
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      trigger_name
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the trigger
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      event_manipulation
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     Event that fires the trigger (
     <code>
      INSERT
     </code>
     ,
     <code>
      UPDATE
     </code>
     , or
     <code>
      DELETE
     </code>
     )
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      event_object_catalog
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the database that contains the table that the trigger is defined on (always the current database)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      event_object_schema
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the schema that contains the table that the trigger is defined on
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      event_object_table
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the table that the trigger is defined on
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      action_order
     </code>
     <code>
      cardinal_number
     </code>
    </p>
    <p>
     Firing order among triggers on the same table having the same
     <code>
      event_manipulation
     </code>
     ,
     <code>
      action_timing
     </code>
     , and
     <code>
      action_orientation
     </code>
     .  In
     <span class="productname">
      PostgreSQL
     </span>
     , triggers are fired in name order, so this column reflects that.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      action_condition
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     <code>
      WHEN
     </code>
     condition of the trigger, null if none (also null if the table is not owned by a currently enabled role)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      action_statement
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     Statement that is executed by the trigger (currently always
     <code>
      EXECUTE FUNCTION
      <em class="replaceable">
       <code>
        function
       </code>
      </em>
      (...)
     </code>
     )
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      action_orientation
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     Identifies whether the trigger fires once for each processed row or once for each statement (
     <code>
      ROW
     </code>
     or
     <code>
      STATEMENT
     </code>
     )
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      action_timing
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     Time at which the trigger fires (
     <code>
      BEFORE
     </code>
     ,
     <code>
      AFTER
     </code>
     , or
     <code>
      INSTEAD OF
     </code>
     )
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      action_reference_old_table
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the
     <span class="quote">
      “
      <span class="quote">
       old
      </span>
      ”
     </span>
     transition table, or null if none
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      action_reference_new_table
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the
     <span class="quote">
      “
      <span class="quote">
       new
      </span>
      ”
     </span>
     transition table, or null if none
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      action_reference_old_row
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Applies to a feature not available in
     <span class="productname">
      PostgreSQL
     </span>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      action_reference_new_row
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Applies to a feature not available in
     <span class="productname">
      PostgreSQL
     </span>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      created
     </code>
     <code>
      time_stamp
     </code>
    </p>
    <p>
     Applies to a feature not available in
     <span class="productname">
      PostgreSQL
     </span>
    </p>
   </td>
  </tr>
 </tbody>
</table>










Os gatilhos no PostgreSQL têm duas incompatibilidades com o padrão SQL que afetam a representação no esquema de informações. Primeiro, os nomes dos gatilhos são locais para cada tabela no PostgreSQL, em vez de serem objetos de esquema independentes. Portanto, pode haver nomes de gatilhos duplicados definidos em um esquema, desde que pertençam a diferentes tabelas. (`trigger_catalog` e `trigger_schema` são realmente os valores que pertencem à tabela na qual o gatilho é definido.) Segundo, os gatilhos podem ser definidos para disparar em múltiplos eventos no PostgreSQL (por exemplo, `ON INSERT OR UPDATE`), enquanto o padrão SQL só permite um. Se um gatilho é definido para disparar em múltiplos eventos, ele é representado como múltiplas linhas no esquema de informações, uma para cada tipo de evento. Como consequência dessas duas questões, a chave primária da visão `triggers` é realmente `(trigger_catalog, trigger_schema, event_object_table, trigger_name, event_manipulation)`, em vez de `(trigger_catalog, trigger_schema, trigger_name)`, o que o padrão SQL especifica. No entanto, se você definir seus gatilhos de uma maneira que esteja em conformidade com o padrão SQL (nomes de gatilho únicos no esquema e apenas um tipo de evento por gatilho), isso não o afetará.

Nota

Antes do PostgreSQL 9.1, as colunas dessa visão `action_timing`, `action_reference_old_table`, `action_reference_new_table`, `action_reference_old_row` e `action_reference_new_row` eram chamadas, respectivamente, de `condition_timing`, `condition_reference_old_table`, `condition_reference_new_table`, `condition_reference_old_row` e `condition_reference_new_row`. Foi assim que elas eram chamadas no padrão SQL:1999. O novo nomeamento está de acordo com o SQL:2003 e versões posteriores.
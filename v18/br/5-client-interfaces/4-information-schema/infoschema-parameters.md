## 35.33. `parameters` [#](#INFOSCHEMA-PARAMETERS)

A vista `parameters` contém informações sobre os parâmetros (argumentos) de todas as funções no banco de dados atual. Apenas as funções que o usuário atual tem acesso (como proprietário ou com algum privilégio) são mostradas.

**Tabela 35.31. Colunas `parameters`**



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
      specific_catalog
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the database containing the function (always the current database)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      specific_schema
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the schema containing the function
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      specific_name
     </code>
     <code>
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
     of the function.  See
     <a class="xref" href="infoschema-routines.md" title="35.45. routines">
      Section 35.45
     </a>
     for more information.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      ordinal_position
     </code>
     <code>
      cardinal_number
     </code>
    </p>
    <p>
     Ordinal position of the parameter in the argument list of the function (count starts at 1)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      parameter_mode
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     <code>
      IN
     </code>
     for input parameter,
     <code>
      OUT
     </code>
     for output parameter, and
     <code>
      INOUT
     </code>
     for input/output parameter.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      is_result
     </code>
     <code>
      yes_or_no
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
      as_locator
     </code>
     <code>
      yes_or_no
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
      parameter_name
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the parameter, or null if the parameter has no name
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
     Data type of the parameter, if it is a built-in type, or
     <code>
      ARRAY
     </code>
     if it is some array (in that case, see the view
     <code>
      element_types
     </code>
     ), else
     <code>
      USER-DEFINED
     </code>
     (in that case, the type is identified in
     <code>
      udt_name
     </code>
     and associated columns).
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      character_maximum_length
     </code>
     <code>
      cardinal_number
     </code>
    </p>
    <p>
     Always null, since this information is not applied to parameter data types in
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
      character_octet_length
     </code>
     <code>
      cardinal_number
     </code>
    </p>
    <p>
     Always null, since this information is not applied to parameter data types in
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
      character_set_catalog
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
      character_set_schema
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
      character_set_name
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
      collation_catalog
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Always null, since this information is not applied to parameter data types in
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
      collation_schema
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Always null, since this information is not applied to parameter data types in
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
      collation_name
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Always null, since this information is not applied to parameter data types in
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
      numeric_precision
     </code>
     <code>
      cardinal_number
     </code>
    </p>
    <p>
     Always null, since this information is not applied to parameter data types in
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
      numeric_precision_radix
     </code>
     <code>
      cardinal_number
     </code>
    </p>
    <p>
     Always null, since this information is not applied to parameter data types in
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
      numeric_scale
     </code>
     <code>
      cardinal_number
     </code>
    </p>
    <p>
     Always null, since this information is not applied to parameter data types in
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
      datetime_precision
     </code>
     <code>
      cardinal_number
     </code>
    </p>
    <p>
     Always null, since this information is not applied to parameter data types in
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
      interval_type
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     Always null, since this information is not applied to parameter data types in
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
      interval_precision
     </code>
     <code>
      cardinal_number
     </code>
    </p>
    <p>
     Always null, since this information is not applied to parameter data types in
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
      udt_catalog
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the database that the data type of the parameter is defined in (always the current database)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      udt_schema
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the schema that the data type of the parameter is defined in
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      udt_name
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the data type of the parameter
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      scope_catalog
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
      scope_schema
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
      scope_name
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
      maximum_cardinality
     </code>
     <code>
      cardinal_number
     </code>
    </p>
    <p>
     Always null, because arrays always have unlimited maximum cardinality in
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
      dtd_identifier
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     An identifier of the data type descriptor of the parameter, unique among the data type descriptors pertaining to the function.  This is mainly useful for joining with other instances of such identifiers.  (The specific format of the identifier is not defined and not guaranteed to remain the same in future versions.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      parameter_default
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     The default expression of the parameter, or null if none or if the function is not owned by a currently enabled role.
    </p>
   </td>
  </tr>
 </tbody>
</table>






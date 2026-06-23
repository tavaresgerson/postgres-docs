## 35.48. `sql_features` [#](#INFOSCHEMA-SQL-FEATURES)

A tabela `sql_features` contém informações sobre quais recursos formais definidos no padrão SQL são suportados pelo PostgreSQL. Essas são as mesmas informações que são apresentadas em [Apêndice D](features.md "Appendix D. SQL Conformance"). Lá, você também pode encontrar algumas informações adicionais de fundo.

**Tabela 35.46. Colunas `sql_features`**



<table border="1" class="table" summary="sql_features Columns">
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
      feature_id
     </code>
     <code class="type">
      character_data
     </code>
    </p>
    <p>
     Identifier string of the feature
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      feature_name
     </code>
     <code class="type">
      character_data
     </code>
    </p>
    <p>
     Descriptive name of the feature
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      sub_feature_id
     </code>
     <code class="type">
      character_data
     </code>
    </p>
    <p>
     Identifier string of the subfeature, or a zero-length string if not a subfeature
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      sub_feature_name
     </code>
     <code class="type">
      character_data
     </code>
    </p>
    <p>
     Descriptive name of the subfeature, or a zero-length string if not a subfeature
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      is_supported
     </code>
     <code class="type">
      yes_or_no
     </code>
    </p>
    <p>
     <code class="literal">
      YES
     </code>
     if the feature is fully supported by the current version of
     <span class="productname">
      PostgreSQL
     </span>
     ,
     <code class="literal">
      NO
     </code>
     if not
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      is_verified_by
     </code>
     <code class="type">
      character_data
     </code>
    </p>
    <p>
     Always null, since the
     <span class="productname">
      PostgreSQL
     </span>
     development group does not perform formal testing of feature conformance
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      comments
     </code>
     <code class="type">
      character_data
     </code>
    </p>
    <p>
     Possibly a comment about the supported status of the feature
    </p>
   </td>
  </tr>
 </tbody>
</table>






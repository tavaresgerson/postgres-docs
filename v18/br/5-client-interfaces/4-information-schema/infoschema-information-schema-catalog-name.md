## 35.3. `information_schema_catalog_name` [#](#INFOSCHEMA-INFORMATION-SCHEMA-CATALOG-NAME)

`information_schema_catalog_name` é uma tabela que sempre contém uma linha e uma coluna contendo o nome do banco de dados atual (catálogo atual, na terminologia SQL).

**Tabela 35.1. Colunas `information_schema_catalog_name`**



<table border="1" class="table" summary="information_schema_catalog_name Columns">
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
      catalog_name
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     Nome do banco de dados que contém este esquema de informações
    </p>
   </td>
  </tr>
 </tbody>
</table>






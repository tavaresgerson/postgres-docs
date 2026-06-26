## 35.20. `data_type_privileges` [#](#INFOSCHEMA-DATA-TYPE-PRIVILEGES)

A vista `data_type_privileges` identifica todos os descritores de tipo de dados que o usuário atual tem acesso, sendo proprietário do objeto descrito ou tendo algum privilégio para ele. Um descritor de tipo de dados é gerado sempre que um tipo de dados é usado na definição de uma coluna de tabela, um domínio ou uma função (como tipo de parâmetro ou retorno) e armazena algumas informações sobre como o tipo de dados é usado nessa instância (por exemplo, o comprimento máximo declarado, se aplicável). Cada descritor de tipo de dados é atribuído um identificador arbitrário que é único entre os identificadores de descritores de tipo de dados atribuídos para um objeto (tabela, domínio, função). Esta vista provavelmente não é útil para aplicações, mas é usada para definir outras vistas no esquema de informações.

**Tabela 35.18. Colunas `data_type_privileges`**



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
      object_catalog
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the database that contains the described object (always the current database)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      object_schema
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the schema that contains the described object
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      object_name
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the described object
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      object_type
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     The type of the described object: one of
     <code>
      TABLE
     </code>
     (the data type descriptor pertains to a column of that table),
     <code>
      DOMAIN
     </code>
     (the data type descriptors pertains to that domain),
     <code>
      ROUTINE
     </code>
     (the data type descriptor pertains to a parameter or the return data type of that function).
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
     The identifier of the data type descriptor, which is unique among the data type descriptors for that same object.
    </p>
   </td>
  </tr>
 </tbody>
</table>






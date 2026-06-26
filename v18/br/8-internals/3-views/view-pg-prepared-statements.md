## 53.16. `pg_prepared_statements` [#](#VIEW-PG-PREPARED-STATEMENTS)

A vista `pg_prepared_statements` exibe todas as declarações preparadas disponíveis na sessão atual. Consulte [PREPARE](sql-prepare.md "PREPARE") para obter mais informações sobre declarações preparadas.

`pg_prepared_statements` contém uma linha para cada declaração preparada. As linhas são adicionadas à visualização quando uma nova declaração preparada é criada e removidas quando uma declaração preparada é liberada (por exemplo, através do comando [`DEALLOCATE`](sql-deallocate.md)].

**Tabela 53.16. Colunas `pg_prepared_statements`**



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
      name
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     The identifier of the prepared statement
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      statement
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     The query string submitted by the client to create this prepared statement. For prepared statements created via SQL, this is the
     <code>
      PREPARE
     </code>
     statement submitted by the client. For prepared statements created via the frontend/backend protocol, this is the text of the prepared statement itself.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      prepare_time
     </code>
     <code>
      timestamptz
     </code>
    </p>
    <p>
     The time at which the prepared statement was created
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      parameter_types
     </code>
     <code>
      regtype[]
     </code>
    </p>
    <p>
     The expected parameter types for the prepared statement in the form of an array of
     <code>
      regtype
     </code>
     . The OID corresponding to an element of this array can be obtained by casting the
     <code>
      regtype
     </code>
     value to
     <code>
      oid
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      result_types
     </code>
     <code>
      regtype[]
     </code>
    </p>
    <p>
     The types of the columns returned by the prepared statement in the form of an array of
     <code>
      regtype
     </code>
     . The OID corresponding to an element of this array can be obtained by casting the
     <code>
      regtype
     </code>
     value to
     <code>
      oid
     </code>
     . If the prepared statement does not provide a result (e.g., a DML statement), then this field will be null.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      from_sql
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     <code>
      true
     </code>
     if the prepared statement was created via the
     <code>
      PREPARE
     </code>
     SQL command;
     <code>
      false
     </code>
     if the statement was prepared via the frontend/backend protocol
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      generic_plans
     </code>
     <code>
      int8
     </code>
    </p>
    <p>
     Number of times generic plan was chosen
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      custom_plans
     </code>
     <code>
      int8
     </code>
    </p>
    <p>
     Number of times custom plan was chosen
    </p>
   </td>
  </tr>
 </tbody>
</table>










A visão `pg_prepared_statements` é somente de leitura.
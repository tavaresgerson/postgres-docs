## 53.6. `pg_config` [#](#VIEW-PG-CONFIG)

The view `pg_config` describes the compile-time configuration parameters of the currently installed version of PostgreSQL. It is intended, for example, to be used by software packages that want to interface to PostgreSQL to facilitate finding the required header files and libraries. It provides the same basic information as the [pg_config](app-pgconfig.md "pg_config") PostgreSQL client application.

By default, the `pg_config` view can be read only by superusers.

**Table 53.6. `pg_config` Columns**



<table border="1" class="table" summary="pg_config Columns">
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
      name
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     The parameter name
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      setting
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     The parameter value
    </p>
   </td>
  </tr>
 </tbody>
</table>


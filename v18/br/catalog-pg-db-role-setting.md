## 52.16. `pg_db_role_setting` [#](#CATALOG-PG-DB-ROLE-SETTING)

O catálogo `pg_db_role_setting` registra os valores padrão que foram definidos para as variáveis de configuração de tempo de execução, para cada combinação de papel e banco de dados.

Ao contrário da maioria dos catálogos de sistema, o `pg_db_role_setting` é compartilhado em todos os bancos de dados de um clúster: há apenas uma cópia do `pg_db_role_setting` por clúster, não uma por banco de dados.

**Tabela 52.16. Colunas `pg_db_role_setting`**



<table border="1" class="table" summary="pg_db_role_setting Columns">
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
      setdatabase
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-database.md" title="52.15. pg_database">
      <code class="structname">
       pg_database
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     O OID do banco de dados ao qual o ajuste se aplica, ou zero, se não for específico do banco de dados
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      setrole
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
      <code class="structname">
       pg_authid
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     O OID do papel ao qual o ajuste se aplica, ou zero, se não for específico para o papel.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      setconfig
     </code>
     <code class="type">
      text[]
     </code>
    </p>
    <p>
     Defeitos para variáveis de configuração de tempo de execução
    </p>
   </td>
  </tr>
 </tbody>
</table>





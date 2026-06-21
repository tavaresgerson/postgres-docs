## 52.36. `pg_parameter_acl` [#](#CATALOG-PG-PARAMETER-ACL)

O catálogo `pg_parameter_acl` registra os parâmetros de configuração para os quais privilégios foram concedidos a um ou mais papéis. Não é feita nenhuma entrada para os parâmetros que têm privilégios padrão.

Ao contrário da maioria dos catálogos de sistema, o `pg_parameter_acl` é compartilhado em todos os bancos de dados de um clúster: há apenas uma cópia do `pg_parameter_acl` por clúster, não uma por banco de dados.

**Tabela 52.36. Colunas `pg_parameter_acl`**



<table border="1" class="table" summary="pg_parameter_acl Columns">
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
      oid
     </code>
     <code class="type">
      oid
     </code>
    </p>
    <p>
     Identificador da linha
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      parname
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     O nome de um parâmetro de configuração para o qual os privilégios são concedidos
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      paracl
     </code>
     <code class="type">
      aclitem[]
     </code>
    </p>
    <p>
     Privilegios de acesso; veja
     <a class="xref" href="ddl-priv.md" title="5.8. Privileges">
      Seção 5.8
     </a>
     para detalhes
    </p>
   </td>
  </tr>
 </tbody>
</table>





## 52.65. `pg_user_mapping` [#](#CATALOG-PG-USER-MAPPING)

O catálogo `pg_user_mapping` armazena as mapeamentos de usuário local para remoto. O acesso a este catálogo é restrito para usuários normais, use a visualização `pg_user_mappings`(view-pg-user-mappings.md "53.36. pg_user_mappings") em vez disso.

**Tabela 52.66. Colunas `pg_user_mapping`**



<table>
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
     <code>
      oid
     </code>
     <code>
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
     <code>
      umuser
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
      <code>
       pg_authid
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     OID do papel local que está sendo mapeado, ou zero se a mapeamento do usuário é público
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      umserver
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-foreign-server.md" title="52.24. pg_foreign_server">
      <code>
       pg_foreign_server
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     O OID do servidor estrangeiro que contém esse mapeamento
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      umoptions
     </code>
     <code>
      text[]
     </code>
    </p>
    <p>
     Mapeamento de opções específicas do usuário, como
     <span class="quote">
      “
      <span class="quote">
       palavra-chave=valor
      </span>
      ”
     </span>
     cordas
    </p>
   </td>
  </tr>
 </tbody>
</table>






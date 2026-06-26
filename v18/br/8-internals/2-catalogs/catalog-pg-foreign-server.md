## 52.24. `pg_foreign_server` [#](#CATALOG-PG-FOREIGN-SERVER)

O catálogo `pg_foreign_server` armazena definições de servidores externos. Um servidor externo descreve uma fonte de dados externos, como um servidor remoto. Servidores externos são acessados por meio de wrappers de dados externos.

**Tabela 52.24. Colunas `pg_foreign_server`**



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
      srvname
     </code>
     <code>
      name
     </code>
    </p>
    <p>
     Nome do servidor estrangeiro
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      srvowner
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
     Proprietário do servidor estrangeiro
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      srvfdw
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-foreign-data-wrapper.md" title="52.23. pg_foreign_data_wrapper">
      <code>
       pg_foreign_data_wrapper
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     OID do wrapper de dados estrangeiro deste servidor estrangeiro
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      srvtype
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Tipo do servidor (opcional)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      srvversion
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Versão do servidor (opcional)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      srvacl
     </code>
     <code>
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
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      srvoptions
     </code>
     <code>
      text[]
     </code>
    </p>
    <p>
     Opções específicas para servidores estrangeiros, como
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






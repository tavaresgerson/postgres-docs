## 52.23. `pg_foreign_data_wrapper` [#](#CATALOG-PG-FOREIGN-DATA-WRAPPER)

O catálogo `pg_foreign_data_wrapper` armazena definições de wrappers de dados externos. Um wrapper de dados externos é o mecanismo pelo qual os dados externos, que residem em servidores externos, são acessados.

**Tabela 52.23. Colunas `pg_foreign_data_wrapper`**



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
      fdwname
     </code>
     <code>
      name
     </code>
    </p>
    <p>
     Nome do wrapper de dados estrangeiros
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      fdwowner
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
     Proprietário do wrapper de dados estrangeiros
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      fdwhandler
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code>
       pg_proc
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Faz referência a uma função de manipulador que é responsável por fornecer rotinas de execução para o wrapper de dados externos. Zero se nenhum manipulador for fornecido
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      fdwvalidator
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code>
       pg_proc
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Faz referência a uma função de validação responsável por verificar a validade das opções fornecidas ao wrapper de dados externos, bem como as opções para servidores externos e mapeamentos de usuários usando o wrapper de dados externos. Zero se nenhum validador for fornecido
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      fdwacl
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
      fdwoptions
     </code>
     <code>
      text[]
     </code>
    </p>
    <p>
     Opções específicas para wrappers de dados estrangeiros, como
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






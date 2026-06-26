## 52.56. `pg_tablespace` [#](#CATALOG-PG-TABLESPACE)

O catálogo `pg_tablespace` armazena informações sobre os espaços de tabela disponíveis. As tabelas podem ser colocadas em espaços de tabela específicos para auxiliar na administração do layout do disco.

Ao contrário da maioria dos catálogos de sistema, o `pg_tablespace` é compartilhado em todos os bancos de dados de um clúster: há apenas uma cópia do `pg_tablespace` por clúster, não uma por banco de dados.

**Tabela 52.56. Colunas `pg_tablespace`**



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
      spcname
     </code>
     <code>
      name
     </code>
    </p>
    <p>
     Nome do espaço de tabela
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      spcowner
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
     Proprietário do espaço de tabela, geralmente o usuário que o criou
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      spcacl
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
      spcoptions
     </code>
     <code>
      text[]
     </code>
    </p>
    <p>
     Opções de nível de tablespace, como
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






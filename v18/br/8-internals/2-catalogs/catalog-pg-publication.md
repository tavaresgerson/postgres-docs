## 52.40. `pg_publication` [#](#CATALOG-PG-PUBLICATION)

O catálogo `pg_publication` contém todas as publicações criadas no banco de dados. Para mais informações sobre publicações, consulte [Seção 29.1](logical-replication-publication.md).

**Tabela 52.40. Colunas `pg_publication`**



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
      pubname
     </code>
     <code>
      name
     </code>
    </p>
    <p>
     Nome da publicação
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      pubowner
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
     Proprietário da publicação
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      puballtables
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Se for verdade, essa publicação inclui automaticamente todas as tabelas no banco de dados, incluindo aquelas que serão criadas no futuro.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      pubinsert
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Se for verdade,
     <a class="xref" href="sql-insert.md" title="INSERT">
      <span class="refentrytitle">
       INSERT
      </span>
     </a>
     As operações são replicadas para tabelas na publicação.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      pubupdate
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Se for verdade,
     <a class="xref" href="sql-update.md" title="UPDATE">
      <span class="refentrytitle">
       ATUALIZAÇÃO
      </span>
     </a>
     As operações são replicadas para tabelas na publicação.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      pubdelete
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Se for verdade,
     <a class="xref" href="sql-delete.md" title="DELETE">
      <span class="refentrytitle">
       DELETE
      </span>
     </a>
     As operações são replicadas para tabelas na publicação.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      pubtruncate
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Se for verdade,
     <a class="xref" href="sql-truncate.md" title="TRUNCATE">
      <span class="refentrytitle">
       TRUNCATE
      </span>
     </a>
     As operações são replicadas para tabelas na publicação.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      pubviaroot
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Se for verdade, as operações em uma partição de folha são replicadas usando a identidade e o esquema de seu ancestral particionado mais alto mencionado na publicação, em vez do seu próprio.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      pubgencols
     </code>
     <code>
      char
     </code>
    </p>
    <p>
     Controla como lidar com a replicação de coluna gerada quando não há uma lista de colunas de publicação:
     <code>
      n
     </code>
     = as colunas geradas nas tabelas associadas à publicação não devem ser replicadas,
     <code>
      s
     </code>
     = as colunas geradas armazenadas nas tabelas associadas à publicação devem ser replicadas.
    </p>
   </td>
  </tr>
 </tbody>
</table>






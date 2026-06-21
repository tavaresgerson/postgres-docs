## 52.45. `pg_rewrite` [#](#CATALOG-PG-REWRITE)

O catálogo `pg_rewrite` armazena regras de reescrita para tabelas e visualizações.

**Tabela 52.45. Colunas `pg_rewrite`**



<table border="1" class="table" summary="pg_rewrite Columns">
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
      rulename
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Nome da regra
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      ev_class
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code class="structname">
       pg_class
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     A tabela para a qual esta regra se aplica
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      ev_type
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     Tipo de evento para o qual a regra é aplicada: 1 =
     <a class="xref" href="sql-select.md" title="SELECT">
      <span class="refentrytitle">
       SELECIONE
      </span>
     </a>
     , 2 =
     <a class="xref" href="sql-update.md" title="UPDATE">
      <span class="refentrytitle">
       ATUALIZAÇÃO
      </span>
     </a>
     , 3 =
     <a class="xref" href="sql-insert.md" title="INSERT">
      <span class="refentrytitle">
       INSERT
      </span>
     </a>
     , 4 =
     <a class="xref" href="sql-delete.md" title="DELETE">
      <span class="refentrytitle">
       DELETE
      </span>
     </a>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      ev_enabled
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     Controles em que
     <a class="xref" href="runtime-config-client.md#GUC-SESSION-REPLICATION-ROLE">
      session_replication_role
     </a>
     modos que os disparos são feitos.
     <code class="literal">
      O
     </code>
     = incêndios em áreas florestais
     <span class="quote">
      “
      <span class="quote">
       origem
      </span>
      ”
     </span>
     e
     <span class="quote">
      “
      <span class="quote">
       local
      </span>
      ”
     </span>
     modos,
     <code class="literal">
      D
     </code>
     = a regra está desativada,
     <code class="literal">
      R
     </code>
     = incêndios em áreas florestais
     <span class="quote">
      “
      <span class="quote">
       replica
      </span>
      ”
     </span>
     modo,
     <code class="literal">
      A
     </code>
     = regras sempre.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      is_instead
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Verdadeiro se a regra for uma
     <code class="literal">
      INSTEAD
     </code>
     regra
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      ev_qual
     </code>
     <code class="type">
      pg_node_tree
     </code>
    </p>
    <p>
     árvore de expressão (na forma de
     <code class="function">
      nodeToString()
     </code>
     representação) para a condição qualificadora da regra
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      ev_action
     </code>
     <code class="type">
      pg_node_tree
     </code>
    </p>
    <p>
     Consulta de árvore (na forma de
     <code class="function">
      nodeToString()
     </code>
     representação) para a ação da regra
    </p>
   </td>
  </tr>
 </tbody>
</table>









### Nota

`pg_class.relhasrules` deve ser verdadeiro se uma tabela tiver alguma regra neste catálogo.
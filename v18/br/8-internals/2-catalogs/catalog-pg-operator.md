## 52.34. `pg_operator` [#](#CATALOG-PG-OPERATOR)

O catálogo `pg_operator` armazena informações sobre operadores. Consulte [CREATE OPERATOR](sql-createoperator.md "CREATE OPERATOR") e [Seção 36.14](xoper.md "36.14. User-Defined Operators") para obter mais informações.

**Tabela 52.34. Colunas `pg_operator`**



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
      oprname
     </code>
     <code>
      name
     </code>
    </p>
    <p>
     Nome do operador
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      oprnamespace
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-namespace.md" title="52.32. pg_namespace">
      <code>
       pg_namespace
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     O OID do espaço de nome que contém este operador
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      oprowner
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
     Proprietário do operador
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      oprkind
     </code>
     <code>
      char
     </code>
    </p>
    <p>
     <code>
      b
     </code>
     = operador infix (
     <span class="quote">
      “
      <span class="quote">
       ambos
      </span>
      ”
     </span>
     ), ou
     <code>
      l
     </code>
     = operador prefixo (
     <span class="quote">
      “
      <span class="quote">
       esquerda
      </span>
      ”
     </span>
     )
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      oprcanmerge
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Este operador suporta junções de fusão
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      oprcanhash
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Este operador suporta junções de hash
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      oprleft
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-type.md" title="52.64. pg_type">
      <code>
       pg_type
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Tipo do operando esquerdo (zero para um operador prefixo)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      oprright
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-type.md" title="52.64. pg_type">
      <code>
       pg_type
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Tipo do operador de direita
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      oprresult
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-type.md" title="52.64. pg_type">
      <code>
       pg_type
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Tipo do resultado (zero para ainda não definido
     <span class="quote">
      “
      <span class="quote">
       casca
      </span>
      ”
     </span>
     operador)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      oprcom
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-operator.md" title="52.34. pg_operator">
      <code>
       pg_operator
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Comutador deste operador (zero se nenhum)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      oprnegate
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-operator.md" title="52.34. pg_operator">
      <code>
       pg_operator
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Negador desse operador (zero se nenhum)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      oprcode
     </code>
     <code>
      regproc
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
     Função que implementa esse operador (zero para um ainda não definido
     <span class="quote">
      “
      <span class="quote">
       casca
      </span>
      ”
     </span>
     operador)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      oprrest
     </code>
     <code>
      regproc
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
     Função de estimativa de seletividade de restrição para este operador (zero se não houver)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      oprjoin
     </code>
     <code>
      regproc
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
     Função de estimativa de seletividade para este operador (zero se não houver)
    </p>
   </td>
  </tr>
 </tbody>
</table>






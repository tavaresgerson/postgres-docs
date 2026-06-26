## 52.57. `pg_transform` [#](#CATALOG-PG-TRANSFORM)

O catálogo `pg_transform` armazena informações sobre transformações, que são um mecanismo para adaptar tipos de dados a linguagens processuais. Consulte [CREATE TRANSFORM](sql-createtransform.md "CREATE TRANSFORM") para obter mais informações.

**Tabela 52.57. Colunas `pg_transform`**



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
      trftype
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
     OID do tipo de dados para o qual essa transformação é feita
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      trflang
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-language.md" title="52.29. pg_language">
      <code>
       pg_language
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     OID da língua para a qual essa transformação é feita
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      trffromsql
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
     O OID da função a ser usada ao converter o tipo de dados para o idioma processual (por exemplo, parâmetros da função). O valor zero é armazenado se o comportamento padrão deve ser usado.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      trftosql
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
     O OID da função a ser usada ao converter a saída do idioma procedural (por exemplo, valores de retorno) para o tipo de dados. Zero é armazenado se o comportamento padrão deve ser usado.
    </p>
   </td>
  </tr>
 </tbody>
</table>






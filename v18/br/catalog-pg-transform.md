## 52.57. `pg_transform` [#](#CATALOG-PG-TRANSFORM)

O catálogo `pg_transform` armazena informações sobre transformações, que são um mecanismo para adaptar tipos de dados a linguagens processuais. Consulte [CREATE TRANSFORM](sql-createtransform.md "CREATE TRANSFORM") para obter mais informações.

**Tabela 52.57. Colunas `pg_transform`**



<table border="1" class="table" summary="pg_transform Columns">
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
      trftype
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-type.md" title="52.64. pg_type">
      <code class="structname">
       pg_type
      </code>
     </a>
     .
     <code class="structfield">
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
     <code class="structfield">
      trflang
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-language.md" title="52.29. pg_language">
      <code class="structname">
       pg_language
      </code>
     </a>
     .
     <code class="structfield">
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
     <code class="structfield">
      trffromsql
     </code>
     <code class="type">
      regproc
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code class="structname">
       pg_proc
      </code>
     </a>
     .
     <code class="structfield">
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
     <code class="structfield">
      trftosql
     </code>
     <code class="type">
      regproc
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code class="structname">
       pg_proc
      </code>
     </a>
     .
     <code class="structfield">
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





## 52.22. `pg_extension` [#](#CATALOG-PG-EXTENSION)

O catálogo `pg_extension` armazena informações sobre as extensões instaladas. Consulte [Seção 36.17](extend-extensions.md) para obter detalhes sobre as extensões.

**Tabela 52.22. Colunas `pg_extension`**



<table border="1" class="table" summary="pg_extension Columns">
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
      extname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Nome da extensão
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      extowner
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
      <code class="structname">
       pg_authid
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     Proprietário da extensão
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      extnamespace
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-namespace.md" title="52.32. pg_namespace">
      <code class="structname">
       pg_namespace
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     Esquema contendo os objetos exportados do extensivo
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      extrelocatable
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Verdadeiro se a extensão pode ser realocada para outro esquema
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      extversion
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Nome da versão para a extensão
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      extconfig
     </code>
     <code class="type">
      oid[]
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
     Conjunto de
     <code class="type">
      regclass
     </code>
     IDOs para a(s) tabela(s) de configuração da extensão, ou
     <code class="literal">
      NULL
     </code>
     se nenhum
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      extcondition
     </code>
     <code class="type">
      text[]
     </code>
    </p>
    <p>
     Conjunto de
     <code class="literal">
      WHERE
     </code>
     - condições de filtro de cláusula para a(s) tabela(s) de configuração da extensão, ou
     <code class="literal">
      NULL
     </code>
     se nenhum
    </p>
   </td>
  </tr>
 </tbody>
</table>









Observe que, ao contrário da maioria dos catálogos com uma coluna de “namespace”, `extnamespace` não deve ser entendido como se a extensão pertencesse a esse esquema. Os nomes das extensões nunca são qualificados pelo esquema. Em vez disso, `extnamespace` indica o esquema que contém a maioria ou todos os objetos da extensão. Se `extrelocatable` for verdadeiro, então esse esquema deve, de fato, conter todos os objetos qualificáveis pelo esquema que pertencem à extensão.
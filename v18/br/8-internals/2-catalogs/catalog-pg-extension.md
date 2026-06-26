## 52.22. `pg_extension` [#](#CATALOG-PG-EXTENSION)

O catálogo `pg_extension` armazena informações sobre as extensões instaladas. Consulte [Seção 36.17](extend-extensions.md) para obter detalhes sobre as extensões.

**Tabela 52.22. Colunas `pg_extension`**



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
      extname
     </code>
     <code>
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
     <code>
      extowner
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
     Proprietário da extensão
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      extnamespace
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
     Esquema contendo os objetos exportados do extensivo
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      extrelocatable
     </code>
     <code>
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
     <code>
      extversion
     </code>
     <code>
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
     <code>
      extconfig
     </code>
     <code>
      oid[]
     </code>
     (referências
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code>
       pg_class
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Conjunto de
     <code>
      regclass
     </code>
     IDOs para a(s) tabela(s) de configuração da extensão, ou
     <code>
      NULL
     </code>
     se nenhum
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      extcondition
     </code>
     <code>
      text[]
     </code>
    </p>
    <p>
     Conjunto de
     <code>
      WHERE
     </code>
     - condições de filtro de cláusula para a(s) tabela(s) de configuração da extensão, ou
     <code>
      NULL
     </code>
     se nenhum
    </p>
   </td>
  </tr>
 </tbody>
</table>










Observe que, ao contrário da maioria dos catálogos com uma coluna de “namespace”, `extnamespace` não deve ser entendido como se a extensão pertencesse a esse esquema. Os nomes das extensões nunca são qualificados pelo esquema. Em vez disso, `extnamespace` indica o esquema que contém a maioria ou todos os objetos da extensão. Se `extrelocatable` for verdadeiro, então esse esquema deve, de fato, conter todos os objetos qualificáveis pelo esquema que pertencem à extensão.
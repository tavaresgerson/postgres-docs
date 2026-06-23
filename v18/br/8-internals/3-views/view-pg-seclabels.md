## 53.23. `pg_seclabels` [#](#VIEW-PG-SECLABELS)

A vista `pg_seclabels` fornece informações sobre etiquetas de segurança. É uma versão mais fácil de consultar do catálogo `pg_seclabel`(catalog-pg-seclabel.md "52.46. pg_seclabel").

**Tabela 53.23. Colunas `pg_seclabels`**



<table border="1" class="table" summary="pg_seclabels Columns">
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
      objoid
     </code>
     <code class="type">
      oid
     </code>
     (referência a qualquer coluna OID)
    </p>
    <p>
     O OID do objeto a que este rótulo de segurança se refere
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      classoid
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
     O OID do catálogo do sistema em que esse objeto aparece
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      objsubid
     </code>
     <code class="type">
      int4
     </code>
    </p>
    <p>
     Para uma etiqueta de segurança em uma coluna de mesa, este é o número da coluna (o
     <code class="structfield">
      objoid
     </code>
     e
     <code class="structfield">
      classoid
     </code>
     refere-se à própria tabela). Para todos os outros tipos de objeto, essa coluna é zero.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      objtype
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     O tipo de objeto ao qual este rótulo se aplica, como texto.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      objnamespace
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
     O OID do espaço de nome para este objeto, se aplicável; caso contrário, NULL.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      objname
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     O nome do objeto ao qual este rótulo se aplica, como texto.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      provider
     </code>
     <code class="type">
      text
     </code>
     (referências
     <a class="link" href="catalog-pg-seclabel.md" title="52.46. pg_seclabel">
      <code class="structname">
       pg_seclabel
      </code>
     </a>
     .
     <code class="structfield">
      provider
     </code>
     )
    </p>
    <p>
     O fornecedor de rótulos associado a este rótulo.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      label
     </code>
     <code class="type">
      text
     </code>
     (referências
     <a class="link" href="catalog-pg-seclabel.md" title="52.46. pg_seclabel">
      <code class="structname">
       pg_seclabel
      </code>
     </a>
     .
     <code class="structfield">
      label
     </code>
     )
    </p>
    <p>
     O rótulo de segurança aplicado a este objeto.
    </p>
   </td>
  </tr>
 </tbody>
</table>






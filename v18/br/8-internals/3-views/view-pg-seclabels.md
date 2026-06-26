## 53.23. `pg_seclabels` [#](#VIEW-PG-SECLABELS)

A vista `pg_seclabels` fornece informações sobre etiquetas de segurança. É uma versão mais fácil de consultar do catálogo `pg_seclabel`(catalog-pg-seclabel.md "52.46. pg_seclabel").

**Tabela 53.23. Colunas `pg_seclabels`**



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
      objoid
     </code>
     <code>
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
     <code>
      classoid
     </code>
     <code>
      oid
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
     O OID do catálogo do sistema em que esse objeto aparece
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      objsubid
     </code>
     <code>
      int4
     </code>
    </p>
    <p>
     Para uma etiqueta de segurança em uma coluna de mesa, este é o número da coluna (o
     <code>
      objoid
     </code>
     e
     <code>
      classoid
     </code>
     refere-se à própria tabela). Para todos os outros tipos de objeto, essa coluna é zero.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      objtype
     </code>
     <code>
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
     <code>
      objnamespace
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
     O OID do espaço de nome para este objeto, se aplicável; caso contrário, NULL.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      objname
     </code>
     <code>
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
     <code>
      provider
     </code>
     <code>
      text
     </code>
     (referências
     <a class="link" href="catalog-pg-seclabel.md" title="52.46. pg_seclabel">
      <code>
       pg_seclabel
      </code>
     </a>
     .
     <code>
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
     <code>
      label
     </code>
     <code>
      text
     </code>
     (referências
     <a class="link" href="catalog-pg-seclabel.md" title="52.46. pg_seclabel">
      <code>
       pg_seclabel
      </code>
     </a>
     .
     <code>
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






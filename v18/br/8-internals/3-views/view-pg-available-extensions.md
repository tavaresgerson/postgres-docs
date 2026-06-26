## 53.3. `pg_available_extensions` [#](#VIEW-PG-AVAILABLE-EXTENSIONS)

A visão `pg_available_extensions` lista as extensões disponíveis para instalação. Veja também o catálogo `pg_extension`(catalog-pg-extension.md "52.22. pg_extension"), que mostra as extensões atualmente instaladas.

**Tabela 53.3. Colunas `pg_available_extensions`**



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
      name
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
      default_version
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Nome da versão padrão, ou
     <code>
      NULL
     </code>
     se não for especificado
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      installed_version
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Atualmente, a versão instalada da extensão, ou
     <code>
      NULL
     </code>
     se não estiver instalado
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      comment
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     String de comentário do arquivo de controle da extensão
    </p>
   </td>
  </tr>
 </tbody>
</table>










A visão `pg_available_extensions` é somente de leitura.
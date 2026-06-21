## 53.4. `pg_available_extension_versions` [#](#VIEW-PG-AVAILABLE-EXTENSION-VERSIONS)

A visão `pg_available_extension_versions` lista as versões específicas de extensão disponíveis para instalação. Veja também o catálogo `pg_extension`(catalog-pg-extension.md "52.22. pg_extension"), que mostra as extensões atualmente instaladas.

**Tabela 53.4. Colunas `pg_available_extension_versions`**



<table border="1" class="table" summary="pg_available_extension_versions Columns">
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
      name
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
      version
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Nome da versão
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      installed
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Verdadeiro se esta versão desta extensão estiver instalada atualmente
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      superuser
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Verdadeiro se apenas superusuários são autorizados a instalar esta extensão (mas veja
     <code class="structfield">
      trusted
     </code>
     )
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      trusted
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Verdadeiro se a extensão pode ser instalada por usuários não superusuários com privilégios apropriados
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relocatable
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
      schema
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Nome do esquema no qual a extensão deve ser instalada, ou
     <code class="literal">
      NULL
     </code>
     se parcialmente ou totalmente relocável
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      requires
     </code>
     <code class="type">
      name[]
     </code>
    </p>
    <p>
     Nomes de extensões pré-requisitos, ou
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
      comment
     </code>
     <code class="type">
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









A visão `pg_available_extension_versions` é somente de leitura.
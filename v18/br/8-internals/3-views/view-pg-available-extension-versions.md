## 53.4. `pg_available_extension_versions` [#](#VIEW-PG-AVAILABLE-EXTENSION-VERSIONS)

A visão `pg_available_extension_versions` lista as versões específicas de extensão disponíveis para instalação. Veja também o catálogo `pg_extension`(catalog-pg-extension.md "52.22. pg_extension"), que mostra as extensões atualmente instaladas.

**Tabela 53.4. Colunas `pg_available_extension_versions`**



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
      version
     </code>
     <code>
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
     <code>
      installed
     </code>
     <code>
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
     <code>
      superuser
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Verdadeiro se apenas superusuários são autorizados a instalar esta extensão (mas veja
     <code>
      trusted
     </code>
     )
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      trusted
     </code>
     <code>
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
     <code>
      relocatable
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
      schema
     </code>
     <code>
      name
     </code>
    </p>
    <p>
     Nome do esquema no qual a extensão deve ser instalada, ou
     <code>
      NULL
     </code>
     se parcialmente ou totalmente relocável
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      requires
     </code>
     <code>
      name[]
     </code>
    </p>
    <p>
     Nomes de extensões pré-requisitos, ou
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










A visão `pg_available_extension_versions` é somente de leitura.
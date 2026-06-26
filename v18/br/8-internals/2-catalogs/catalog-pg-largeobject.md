## 52.30. `pg_largeobject` [#](#CATALOG-PG-LARGEOBJECT)

O catálogo `pg_largeobject` contém os dados que compõem os “objetos grandes”. Um objeto grande é identificado por um OID atribuído quando é criado. Cada objeto grande é dividido em segmentos ou “páginas” pequenos o suficiente para serem convenientemente armazenados como linhas em `pg_largeobject`. A quantidade de dados por página é definida como `LOBLKSIZE` (que atualmente é `BLCKSZ/4`, ou tipicamente 2 kB).

Antes do PostgreSQL 9.0, não havia uma estrutura de permissão associada a objetos grandes. Como resultado, `pg_largeobject` era legível publicamente e poderia ser usado para obter os OIDs (e conteúdos) de todos os objetos grandes no sistema. Esse não é mais o caso; use `pg_largeobject_metadata`(catalog-pg-largeobject-metadata.md "52.31. pg_largeobject_metadata") para obter uma lista dos OIDs dos objetos grandes.

**Tabela 52.30. Colunas `pg_largeobject`**



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
      loid
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-largeobject-metadata.md" title="52.31. pg_largeobject_metadata">
      <code>
       pg_largeobject_metadata
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Identificador do grande objeto que inclui esta página
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      pageno
     </code>
     <code>
      int4
     </code>
    </p>
    <p>
     Número da página desta página dentro de seu grande objeto (contando a partir de zero)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      data
     </code>
     <code>
      bytea
     </code>
    </p>
    <p>
     Dados reais armazenados no grande objeto. Isso nunca será mais do que
     <code>
      LOBLKSIZE
     </code>
     bytes e pode ser menos.
    </p>
   </td>
  </tr>
 </tbody>
</table>










Cada linha de `pg_largeobject` contém dados para uma página de um grande objeto, começando no deslocamento de byte (`pageno * LOBLKSIZE`) dentro do objeto. A implementação permite armazenamento esparso: as páginas podem estar ausentes e podem ser menores que os `LOBLKSIZE` bytes, mesmo que não sejam a última página do objeto. Regiões ausentes dentro de um grande objeto são lidas como zeros.
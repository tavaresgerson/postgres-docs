## 52.49. `pg_shdescription` [#](#CATALOG-PG-SHDESCRIPTION)

O catálogo `pg_shdescription` armazena descrições opcionais (comentários) para objetos de banco de dados compartilhados. As descrições podem ser manipuladas com o comando [`COMMENT`](sql-comment.md "COMMENT") e visualizadas com os comandos `\d` do psql.

Veja também `pg_description` (catalog-pg-description.md "52.19. pg_description"), que realiza uma função semelhante para descrições que envolvem objetos dentro de um único banco de dados.

Ao contrário da maioria dos catálogos de sistema, o `pg_shdescription` é compartilhado em todos os bancos de dados de um clúster: há apenas uma cópia do `pg_shdescription` por clúster, não uma por banco de dados.

**Tabela 52.49. Colunas `pg_shdescription`**



<table border="1" class="table" summary="pg_shdescription Columns">
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
     O OID do objeto a que esta descrição se refere
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
      description
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Texto arbitrário que serve como descrição deste objeto
    </p>
   </td>
  </tr>
 </tbody>
</table>






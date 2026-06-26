## 52.19. `pg_description` [#](#CATALOG-PG-DESCRIPTION)

O catálogo `pg_description` armazena descrições opcionais (comentários) para cada objeto do banco de dados. As descrições podem ser manipuladas com o comando [`COMMENT`](sql-comment.md "COMMENT") e visualizadas com os comandos `\d` do psql. As descrições de muitos objetos de sistema embutidos são fornecidas nos conteúdos iniciais de `pg_description`.

Veja também `pg_shdescription` (catalog-pg-shdescription.md "52.49. pg_shdescription"), que realiza uma função semelhante para descrições que envolvem objetos que são compartilhados em um clúster de banco de dados.

**Tabela 52.19. Colunas `pg_description`**



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
     O OID do objeto a que esta descrição se refere
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
     Para um comentário em uma coluna de tabela, este é o número da coluna (o
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
      description
     </code>
     <code>
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






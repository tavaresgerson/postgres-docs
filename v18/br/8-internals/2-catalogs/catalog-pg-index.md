## 52.26. `pg_index` [#](#CATALOG-PG-INDEX)

O catálogo `pg_index` contém parte das informações sobre índices. O restante está principalmente em [`pg_class`](catalog-pg-class.md "52.11. pg_class").

**Tabela 52.26. Colunas `pg_index`**



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
      indexrelid
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
     O OID do
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code>
       pg_class
      </code>
     </a>
     entrada para este índice
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      indrelid
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
     O OID do
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code>
       pg_class
      </code>
     </a>
     entrada para a tabela, este índice é para
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      indnatts
     </code>
     <code>
      int2
     </code>
    </p>
    <p>
     O número total de colunas no índice (duplicatas
     <code>
      pg_class.relnatts
     </code>
     ); esse número inclui tanto atributos chave quanto atributos incluídos
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      indnkeyatts
     </code>
     <code>
      int2
     </code>
    </p>
    <p>
     O número de
     <em class="firstterm">
      colunas-chave
     </em>
     no índice, sem contabilizar nenhum
     <em class="firstterm">
      colunas incluídas
     </em>
     , que são apenas armazenados e não participam da semântica do índice
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      indisunique
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Se for verdade, este é um índice único
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      indnullsnotdistinct
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Esse valor é usado apenas para índices únicos. Se for falso, esse índice único considerará valores nulos distintos (assim, o índice pode conter vários valores nulos em uma coluna, conforme o comportamento padrão do PostgreSQL). Se for verdadeiro, ele considerará os valores nulos como iguais (assim, o índice pode conter apenas um valor nulo em uma coluna).
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      indisprimary
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Se for verdade, este índice representa a chave primária da tabela (
     <code>
      indisunique
     </code>
     deve ser sempre verdadeiro quando isso é verdadeiro)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      indisexclusion
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Se for verdade, este índice suporta uma restrição de exclusão
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      indimmediate
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Se for verdade, a verificação de unicidade é aplicada imediatamente na inserção (irrelevant se
     <code>
      indisunique
     </code>
     não é verdade)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      indisclustered
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Se for verdade, a tabela foi agrupada pela última vez neste índice
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      indisvalid
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Se for verdade, o índice é atualmente válido para consultas. Se for falso, significa que o índice é possivelmente incompleto: ainda deve ser modificado por
     <a class="link" href="sql-insert.md" title="INSERT">
      <code>
       INSERT
      </code>
     </a>
     /
     <a class="link" href="sql-update.md" title="UPDATE">
      <code>
       UPDATE
      </code>
     </a>
     operações, mas não pode ser usado com segurança para consultas. Se for único, a propriedade de unicidade também não é garantida como verdadeira.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      indcheckxmin
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Se for verdade, as consultas não devem usar o índice até que
     <code>
      xmin
     </code>
     de isto
     <code>
      pg_index
     </code>
     A linha está abaixo deles
     <code>
      TransactionXmin
     </code>
     limite de eventos, porque a tabela pode conter quebrados
     <a class="link" href="storage-hot.md" title="66.7. Heap-Only Tuples (HOT)">
      Cadeias HOT
     </a>
     com linhas incompatíveis que eles podem ver
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      indisready
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Se for verdade, o índice está atualmente pronto para inserções. Se for falso, significa que o índice deve ser ignorado
     <a class="link" href="sql-insert.md" title="INSERT">
      <code>
       INSERT
      </code>
     </a>
     /
     <a class="link" href="sql-update.md" title="UPDATE">
      <code>
       UPDATE
      </code>
     </a>
     operations.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      indislive
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Se falso, o índice está em processo de ser descartado e deve ser ignorado para todos os propósitos (incluindo decisões de segurança HOT)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      indisreplident
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Se for verdade, este índice foi escolhido como
     <span class="quote">
      “
      <span class="quote">
       identidade replicada
      </span>
      ”
     </span>
     utilizando
     <a class="link" href="sql-altertable.md#SQL-ALTERTABLE-REPLICA-IDENTITY">
      <code>
       ALTER TABLE ... REPLICA IDENTITY USING INDEX ...
      </code>
     </a>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      indkey
     </code>
     <code>
      int2vector
     </code>
     (referências
     <a class="link" href="catalog-pg-attribute.md" title="52.7. pg_attribute">
      <code>
       pg_attribute
      </code>
     </a>
     .
     <code>
      attnum
     </code>
     )
    </p>
    <p>
     Este é um conjunto de
     <code>
      indnatts
     </code>
     valores que indicam quais colunas da tabela este índice indexa. Por exemplo, um valor de
     <code>
      1 3
     </code>
     Isso significaria que as primeiras e as terceiras colunas da tabela compõem as entradas do índice. As colunas chave vêm antes das colunas não chave (incluídas). Um zero nesse array indica que o atributo de índice correspondente é uma expressão sobre as colunas da tabela, e não uma simples referência de coluna.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      indcollation
     </code>
     <code>
      oidvector
     </code>
     (referências
     <a class="link" href="catalog-pg-collation.md" title="52.12. pg_collation">
      <code>
       pg_collation
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Para cada coluna na chave do índice (
     <code>
      indnkeyatts
     </code>
     valores), este contém o OID da correção de texto a ser usada para o índice, ou zero se a coluna não for de um tipo de dados correcionável.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      indclass
     </code>
     <code>
      oidvector
     </code>
     (referências
     <a class="link" href="catalog-pg-opclass.md" title="52.33. pg_opclass">
      <code>
       pg_opclass
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Para cada coluna na chave do índice (
     <code>
      indnkeyatts
     </code>
     valores), este contém o OID da classe de operador a ser usado. Veja
     <a class="link" href="catalog-pg-opclass.md" title="52.33. pg_opclass">
      <code>
       pg_opclass
      </code>
     </a>
     para obter mais informações.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      indoption
     </code>
     <code>
      int2vector
     </code>
    </p>
    <p>
     Este é um conjunto de
     <code>
      indnkeyatts
     </code>
     valores que armazenam bits de sinalização por coluna. O significado dos bits é definido pelo método de acesso do índice.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      indexprs
     </code>
     <code>
      pg_node_tree
     </code>
    </p>
    <p>
     árvores de expressão (em
     <code>
      nodeToString()
     </code>
     (representação) para atributos de índice que não são referências simples de coluna. Esta é uma lista com um elemento para cada entrada zero
     <code>
      indkey
     </code>
     Nulo se todos os atributos do índice forem referências simples.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      indpred
     </code>
     <code>
      pg_node_tree
     </code>
    </p>
    <p>
     árvore de expressão (em
     <code>
      nodeToString()
     </code>
     representação) para predicado de índice parcial. Nulo se não for um índice parcial.
    </p>
   </td>
  </tr>
 </tbody>
</table>






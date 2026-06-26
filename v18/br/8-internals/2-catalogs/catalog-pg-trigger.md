## 52.58. `pg_trigger` [#](#CATALOG-PG-TRIGGER)

O catálogo `pg_trigger` armazena gatilhos em tabelas e visualizações. Consulte [CREATE TRIGGER](sql-createtrigger.md "CREATE TRIGGER") para obter mais informações.

**Tabela 52.58. Colunas `pg_trigger`**



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
      tgrelid
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
     A tabela em que este gatilho está
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      tgparentid
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-trigger.md" title="52.58. pg_trigger">
      <code>
       pg_trigger
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Indicar que este gatilho é clonado a partir de (isso acontece quando as partições são criadas ou anexadas a uma tabela particionada); zero se não for um clone
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      tgname
     </code>
     <code>
      name
     </code>
    </p>
    <p>
     Nome do gatilho (deve ser único entre os gatilhos da mesma tabela)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      tgfoid
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code>
       pg_proc
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     A função a ser chamada
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      tgtype
     </code>
     <code>
      int2
     </code>
    </p>
    <p>
     Máscara de bit que identifica as condições de disparo do gatilho
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      tgenabled
     </code>
     <code>
      char
     </code>
    </p>
    <p>
     Controles em que
     <a class="xref" href="runtime-config-client.md#GUC-SESSION-REPLICATION-ROLE">
      session_replication_role
     </a>
     os modos em que o gatilho dispara.
     <code>
      O
     </code>
     = desencadeia incêndios
     <span class="quote">
      “
      <span class="quote">
       origem
      </span>
      ”
     </span>
     e
     <span class="quote">
      “
      <span class="quote">
       local
      </span>
      ”
     </span>
     modos,
     <code>
      D
     </code>
     = o gatilho está desativado,
     <code>
      R
     </code>
     = desencadeia incêndios
     <span class="quote">
      “
      <span class="quote">
       replica
      </span>
      ”
     </span>
     modo,
     <code>
      A
     </code>
     = acionam incêndios sempre.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      tgisinternal
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Verdadeiro se o gatilho é gerado internamente (geralmente, para impor a restrição identificada por
     <code>
      tgconstraint
     </code>
     )
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      tgconstrrelid
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
     A tabela referenciada por uma restrição de integridade referencial (zero se o gatilho não for para uma restrição de integridade referencial)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      tgconstrindid
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
     O índice que suporta uma chave primária única, integridade referencial ou restrição de exclusão (zero se o gatilho não for para um desses tipos de restrição)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      tgconstraint
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-constraint.md" title="52.13. pg_constraint">
      <code>
       pg_constraint
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     O
     <a class="link" href="catalog-pg-constraint.md" title="52.13. pg_constraint">
      <code>
       pg_constraint
      </code>
     </a>
     entrada associada ao gatilho (zero se o gatilho não for para uma restrição)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      tgdeferrable
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Verdadeiro se o gatilho de restrição é diferível
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      tginitdeferred
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Verdadeiro se o gatilho de restrição é inicialmente diferido
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      tgnargs
     </code>
     <code>
      int2
     </code>
    </p>
    <p>
     Número de strings de argumento passadas para a função de gatilho
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      tgattr
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
     Números de coluna, se o gatilho for específico para a coluna; caso contrário, um array vazio
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      tgargs
     </code>
     <code>
      bytea
     </code>
    </p>
    <p>
     Strings de argumento a serem passadas para o gatilho, cada uma terminada por NULL
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      tgqual
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
     representação) para o gatilho
     <code>
      WHEN
     </code>
     condição, ou nulo se nenhuma
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      tgoldtable
     </code>
     <code>
      name
     </code>
    </p>
    <p>
     <code>
      REFERENCING
     </code>
     nome da cláusula para
     <code>
      OLD TABLE
     </code>
     , ou nulo se nenhum
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      tgnewtable
     </code>
     <code>
      name
     </code>
    </p>
    <p>
     <code>
      REFERENCING
     </code>
     nome da cláusula para
     <code>
      NEW TABLE
     </code>
     , ou nulo se nenhum
    </p>
   </td>
  </tr>
 </tbody>
</table>










Atualmente, o disparo específico para coluna é suportado apenas para eventos `UPDATE`, e, portanto, `tgattr` é relevante apenas para esse tipo de evento. `tgtype` pode conter bits para outros tipos de eventos também, mas esses são presumidos serem de todo o quadro, independentemente do que está em `tgattr`.

Nota

Quando `tgconstraint` não é nulo, `tgconstrrelid`, `tgconstrindid`, `tgdeferrable` e `tginitdeferred` são em grande parte redundantes com a entrada referenciada [`pg_constraint`](catalog-pg-constraint.md "52.13. pg_constraint"). No entanto, é possível que um gatilho não diferível seja associado a uma restrição diferível: as restrições de chave estrangeira podem ter alguns gatilhos diferíveis e outros não diferíveis.

Nota

`pg_class.relhastriggers` deve ser verdadeiro se uma relação tiver quaisquer gatilhos neste catálogo.
## 52.13. `pg_constraint` [#](#CATALOG-PG-CONSTRAINT)

O catálogo `pg_constraint` armazena restrições de verificação, não nulo, chave primária, única, chave estrangeira e exclusão em tabelas. (As restrições de coluna não são tratadas especialmente. Cada restrição de coluna é equivalente a alguma restrição de tabela.)

Os gatilhos de restrição definidos pelo usuário (criados com [`CREATE CONSTRAINT TRIGGER`](sql-createtrigger.md "CREATE TRIGGER")) também geram uma entrada nesta tabela.

As restrições sobre os domínios também são armazenadas aqui.

**Tabela 52.13. Colunas `pg_constraint`**



<table border="1" class="table" summary="pg_constraint Columns">
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
      oid
     </code>
     <code class="type">
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
     <code class="structfield">
      conname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Nome da restrição (não necessariamente único!)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      connamespace
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
     O OID do espaço de nomes que contém essa restrição
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      contype
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     <code class="literal">
      c
     </code>
     = restrição de verificação,
     <code class="literal">
      f
     </code>
     = restrição de chave estrangeira,
     <code class="literal">
      n
     </code>
     = restrição não-nulo,
     <code class="literal">
      p
     </code>
     = restrição de chave primária,
     <code class="literal">
      u
     </code>
     = restrição única,
     <code class="literal">
      t
     </code>
     = gatilho de restrição,
     <code class="literal">
      x
     </code>
     = restrição de exclusão
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      condeferrable
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     A restrição é adiável?
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      condeferred
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     A restrição é deferida por padrão?
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      conenforced
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     A restrição é aplicada?
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      convalidated
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     A restrição foi validada?
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      conrelid
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
     A tabela sobre a qual essa restrição está; zero se não for uma restrição de tabela
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      contypid
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-type.md" title="52.64. pg_type">
      <code class="structname">
       pg_type
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     O domínio em que essa restrição está; zero se não for uma restrição de domínio
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      conindid
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
     O índice que suporta essa restrição, se for uma chave primária única, chave estrangeira ou restrição de exclusão; caso contrário, zero
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      conparentid
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-constraint.md" title="52.13. pg_constraint">
      <code class="structname">
       pg_constraint
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     A restrição correspondente à tabela dividida dos pais, se esta for uma restrição em uma partição; caso contrário, zero
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      confrelid
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
     Se for uma chave estrangeira, a tabela referenciada; caso contrário, zero
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      confupdtype
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     Código da ação de atualização da chave estrangeira:
     <code class="literal">
      a
     </code>
     = sem ação,
     <code class="literal">
      r
     </code>
     = restringir,
     <code class="literal">
      c
     </code>
     = cascata,
     <code class="literal">
      n
     </code>
     = definir como nulo,
     <code class="literal">
      d
     </code>
     = definir padrão
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      confdeltype
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     Código da ação de exclusão de chave estrangeira:
     <code class="literal">
      a
     </code>
     = sem ação,
     <code class="literal">
      r
     </code>
     = restringir,
     <code class="literal">
      c
     </code>
     = cascata,
     <code class="literal">
      n
     </code>
     = definir como nulo,
     <code class="literal">
      d
     </code>
     = definir padrão
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      confmatchtype
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     Tipo de correspondência de chave estrangeira:
     <code class="literal">
      f
     </code>
     = completo,
     <code class="literal">
      p
     </code>
     = parcial,
     <code class="literal">
      s
     </code>
     = simples
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      conislocal
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Essa restrição é definida localmente para a relação. Observe que uma restrição pode ser definida localmente e herdada simultaneamente.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      coninhcount
     </code>
     <code class="type">
      int2
     </code>
    </p>
    <p>
     O número de ancestrais de herança direta que essa restrição tem. Uma restrição com um número não nulo de ancestrais não pode ser descartada nem renomeada.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      connoinherit
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Essa restrição é definida localmente para a relação. É uma restrição não hereditária.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      conperiod
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Essa restrição é definida com
     <code class="literal">
      WITHOUT OVERLAPS
     </code>
     (para chaves primárias e restrições únicas) ou
     <code class="literal">
      PERIOD
     </code>
     (para chaves estrangeiras).
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      conkey
     </code>
     <code class="type">
      int2[]
     </code>
     (referências
     <a class="link" href="catalog-pg-attribute.md" title="52.7. pg_attribute">
      <code class="structname">
       pg_attribute
      </code>
     </a>
     .
     <code class="structfield">
      attnum
     </code>
     )
    </p>
    <p>
     Se uma restrição de tabela (incluindo chaves estrangeiras, mas não gatilhos de restrição), lista das colunas restringidas
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      confkey
     </code>
     <code class="type">
      int2[]
     </code>
     (referências
     <a class="link" href="catalog-pg-attribute.md" title="52.7. pg_attribute">
      <code class="structname">
       pg_attribute
      </code>
     </a>
     .
     <code class="structfield">
      attnum
     </code>
     )
    </p>
    <p>
     Se for uma chave estrangeira, uma lista das colunas referenciadas
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      conpfeqop
     </code>
     <code class="type">
      oid[]
     </code>
     (referências
     <a class="link" href="catalog-pg-operator.md" title="52.34. pg_operator">
      <code class="structname">
       pg_operator
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     Se uma chave estrangeira, lista dos operadores de igualdade para comparações PK = FK
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      conppeqop
     </code>
     <code class="type">
      oid[]
     </code>
     (referências
     <a class="link" href="catalog-pg-operator.md" title="52.34. pg_operator">
      <code class="structname">
       pg_operator
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     Se uma chave estrangeira, lista dos operadores de igualdade para comparações PK = PK
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      conffeqop
     </code>
     <code class="type">
      oid[]
     </code>
     (referências
     <a class="link" href="catalog-pg-operator.md" title="52.34. pg_operator">
      <code class="structname">
       pg_operator
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     Se uma chave estrangeira, lista dos operadores de igualdade para comparações FK = FK
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      confdelsetcols
     </code>
     <code class="type">
      int2[]
     </code>
     (referências
     <a class="link" href="catalog-pg-attribute.md" title="52.7. pg_attribute">
      <code class="structname">
       pg_attribute
      </code>
     </a>
     .
     <code class="structfield">
      attnum
     </code>
     )
    </p>
    <p>
     Se uma chave estrangeira com
     <code class="literal">
      SET NULL
     </code>
     ou
     <code class="literal">
      SET DEFAULT
     </code>
     Para a ação de exclusão, as colunas que serão atualizadas. Se nulo, todas as colunas de referência serão atualizadas.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      conexclop
     </code>
     <code class="type">
      oid[]
     </code>
     (referências
     <a class="link" href="catalog-pg-operator.md" title="52.34. pg_operator">
      <code class="structname">
       pg_operator
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     Se uma restrição de exclusão ou
     <code class="literal">
      WITHOUT OVERLAPS
     </code>
     chave primária/constrangimento único, lista dos operadores de exclusão por coluna.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      conbin
     </code>
     <code class="type">
      pg_node_tree
     </code>
    </p>
    <p>
     Se for uma restrição de verificação, uma representação interna da expressão. (Recomenda-se o uso
     <code class="function">
      pg_get_constraintdef()
     </code>
     para extrair a definição de uma restrição de verificação.)
    </p>
   </td>
  </tr>
 </tbody>
</table>










No caso de uma restrição de exclusão, `conkey` é útil apenas para elementos de restrição que são referências simples de coluna. Para outros casos, um zero aparece em `conkey` e o índice associado deve ser consultado para descobrir a expressão que está sob restrição. (O `conkey` tem, portanto, o mesmo conteúdo que [`pg_index`](catalog-pg-index.md).`indkey` para o índice.)

Nota

`pg_class.relchecks` precisa estar de acordo com o número de entradas de restrição de verificação encontradas nesta tabela para cada relação.
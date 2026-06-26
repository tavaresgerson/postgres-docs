## 52.2. `pg_aggregate` [#](#CATALOG-PG-AGGREGATE)

O catálogo `pg_aggregate` armazena informações sobre funções agregadas. Uma função agregada é uma função que opera em um conjunto de valores (tipicamente uma coluna de cada linha que corresponde a uma condição de consulta) e retorna um único valor calculado a partir de todos esses valores. As funções agregadas típicas são `sum`, `count` e `max`. Cada entrada em `pg_aggregate` é uma extensão de uma entrada em [`pg_proc`](catalog-pg-proc.md "52.39. pg_proc"). A entrada em `pg_proc` carrega o nome do agregado, os tipos de dados de entrada e saída e outras informações que são semelhantes às funções comuns.

**Tabela 52.2. Colunas `pg_aggregate`**



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
      aggfnoid
     </code>
     <code>
      regproc
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
     <code>
      pg_proc
     </code>
     OID da função agregada
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      aggkind
     </code>
     <code>
      char
     </code>
    </p>
    <p>
     Tipo agregado:
     <code>
      n
     </code>
     para
     <span class="quote">
      “
      <span class="quote">
       normal
      </span>
      ”
     </span>
     agregados,
     <code>
      o
     </code>
     para
     <span class="quote">
      “
      <span class="quote">
       conjunto ordenado
      </span>
      ”
     </span>
     agregados, ou
     <code>
      h
     </code>
     para
     <span class="quote">
      “
      <span class="quote">
       conjunto hipotético
      </span>
      ”
     </span>
     agregados
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      aggnumdirectargs
     </code>
     <code>
      int2
     </code>
    </p>
    <p>
     Número de argumentos diretos (não agregados) de um conjunto ordenado ou agregado de conjuntos hipotéticos, contando uma matriz variadic como um argumento. Se igual a
     <code>
      pronargs
     </code>
     , o agregado deve ser variadic e o array variadic descreve os argumentos agregados, bem como os argumentos diretos finais. Sempre zero para agregados normais.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      aggtransfn
     </code>
     <code>
      regproc
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
     Função de transição
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      aggfinalfn
     </code>
     <code>
      regproc
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
     Função final (zero se nenhuma)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      aggcombinefn
     </code>
     <code>
      regproc
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
     Combinação de funções (zero se nenhuma)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      aggserialfn
     </code>
     <code>
      regproc
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
     Função de serialização (zero se não houver)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      aggdeserialfn
     </code>
     <code>
      regproc
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
     Função de deserialização (zero se não houver)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      aggmtransfn
     </code>
     <code>
      regproc
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
     Função de transição para frente para o modo de agregação móvel (zero se não houver)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      aggminvtransfn
     </code>
     <code>
      regproc
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
     Função de transição inversa para modo de agregado móvel (zero se nenhum)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      aggmfinalfn
     </code>
     <code>
      regproc
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
     Função final para o modo de agregação móvel (zero se nenhum)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      aggfinalextra
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Verdadeiro para passar argumentos de teste adicionais
     <code>
      aggfinalfn
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      aggmfinalextra
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Verdadeiro para passar argumentos de teste adicionais
     <code>
      aggmfinalfn
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      aggfinalmodify
     </code>
     <code>
      char
     </code>
    </p>
    <p>
     Seja
     <code>
      aggfinalfn
     </code>
     modifica o valor do estado de transição:
     <code>
      r
     </code>
     se for somente de leitura,
     <code>
      s
     </code>
     se o
     <code>
      aggtransfn
     </code>
     não pode ser aplicada após
     <code>
      aggfinalfn
     </code>
     , ou
     <code>
      w
     </code>
     se escreve sobre o valor
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      aggmfinalmodify
     </code>
     <code>
      char
     </code>
    </p>
    <p>
     Como
     <code>
      aggfinalmodify
     </code>
     , mas para o
     <code>
      aggmfinalfn
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      aggsortop
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-operator.md" title="52.34. pg_operator">
      <code>
       pg_operator
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Operador de classificação associado (zero se nenhum)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      aggtranstype
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-type.md" title="52.64. pg_type">
      <code>
       pg_type
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Tipo de dados do conjunto de dados de transição interna (estado) da função agregada
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      aggtransspace
     </code>
     <code>
      int4
     </code>
    </p>
    <p>
     Tamanho médio aproximado (em bytes) dos dados do estado de transição, ou zero para usar uma estimativa padrão
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      aggmtranstype
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-type.md" title="52.64. pg_type">
      <code>
       pg_type
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Tipo de dados do conjunto de dados de transição interna (estado) da função agregada para o modo de agregação móvel (zero se nenhum)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      aggmtransspace
     </code>
     <code>
      int4
     </code>
    </p>
    <p>
     Tamanho médio aproximado (em bytes) dos dados do estado de transição para o modo de agregação móvel, ou zero para usar uma estimativa padrão
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      agginitval
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     O valor inicial do estado de transição. Este é um campo de texto que contém o valor inicial em sua representação de string externa. Se este campo for nulo, o valor do estado de transição começa como nulo.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      aggminitval
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     O valor inicial do estado de transição para o modo de agregados em movimento. Este é um campo de texto que contém o valor inicial em sua representação de string externa. Se este campo for nulo, o valor do estado de transição começa como nulo.
    </p>
   </td>
  </tr>
 </tbody>
</table>










Novas funções agregadas são registradas com o comando `CREATE AGGREGATE`(sql-createaggregate.md "CREATE AGGREGATE"). Consulte [Seção 36.12](xaggr.md "36.12. User-Defined Aggregates") para obter mais informações sobre a escrita de funções agregadas e o significado das funções de transição, etc.
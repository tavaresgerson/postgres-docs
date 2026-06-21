## 52.2. `pg_aggregate` [#](#CATALOG-PG-AGGREGATE)

O catálogo `pg_aggregate` armazena informações sobre funções agregadas. Uma função agregada é uma função que opera em um conjunto de valores (tipicamente uma coluna de cada linha que corresponde a uma condição de consulta) e retorna um único valor calculado a partir de todos esses valores. As funções agregadas típicas são `sum`, `count` e `max`. Cada entrada em `pg_aggregate` é uma extensão de uma entrada em [`pg_proc`](catalog-pg-proc.md "52.39. pg_proc"). A entrada em `pg_proc` carrega o nome do agregado, os tipos de dados de entrada e saída e outras informações que são semelhantes às funções comuns.

**Tabela 52.2. Colunas `pg_aggregate`**



<table border="1" class="table" summary="pg_aggregate Columns">
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
      aggfnoid
     </code>
     <code class="type">
      regproc
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code class="structname">
       pg_proc
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     <code class="structname">
      pg_proc
     </code>
     OID da função agregada
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      aggkind
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     Tipo agregado:
     <code class="literal">
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
     <code class="literal">
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
     <code class="literal">
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
     <code class="structfield">
      aggnumdirectargs
     </code>
     <code class="type">
      int2
     </code>
    </p>
    <p>
     Número de argumentos diretos (não agregados) de um conjunto ordenado ou agregado de conjuntos hipotéticos, contando uma matriz variadic como um argumento. Se igual a
     <code class="structfield">
      pronargs
     </code>
     , o agregado deve ser variadic e o array variadic descreve os argumentos agregados, bem como os argumentos diretos finais. Sempre zero para agregados normais.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      aggtransfn
     </code>
     <code class="type">
      regproc
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code class="structname">
       pg_proc
      </code>
     </a>
     .
     <code class="structfield">
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
     <code class="structfield">
      aggfinalfn
     </code>
     <code class="type">
      regproc
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code class="structname">
       pg_proc
      </code>
     </a>
     .
     <code class="structfield">
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
     <code class="structfield">
      aggcombinefn
     </code>
     <code class="type">
      regproc
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code class="structname">
       pg_proc
      </code>
     </a>
     .
     <code class="structfield">
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
     <code class="structfield">
      aggserialfn
     </code>
     <code class="type">
      regproc
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code class="structname">
       pg_proc
      </code>
     </a>
     .
     <code class="structfield">
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
     <code class="structfield">
      aggdeserialfn
     </code>
     <code class="type">
      regproc
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code class="structname">
       pg_proc
      </code>
     </a>
     .
     <code class="structfield">
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
     <code class="structfield">
      aggmtransfn
     </code>
     <code class="type">
      regproc
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code class="structname">
       pg_proc
      </code>
     </a>
     .
     <code class="structfield">
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
     <code class="structfield">
      aggminvtransfn
     </code>
     <code class="type">
      regproc
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code class="structname">
       pg_proc
      </code>
     </a>
     .
     <code class="structfield">
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
     <code class="structfield">
      aggmfinalfn
     </code>
     <code class="type">
      regproc
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code class="structname">
       pg_proc
      </code>
     </a>
     .
     <code class="structfield">
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
     <code class="structfield">
      aggfinalextra
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Verdadeiro para passar argumentos de teste adicionais
     <code class="structfield">
      aggfinalfn
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      aggmfinalextra
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Verdadeiro para passar argumentos de teste adicionais
     <code class="structfield">
      aggmfinalfn
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      aggfinalmodify
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     Seja
     <code class="structfield">
      aggfinalfn
     </code>
     modifica o valor do estado de transição:
     <code class="literal">
      r
     </code>
     se for somente de leitura,
     <code class="literal">
      s
     </code>
     se o
     <code class="structfield">
      aggtransfn
     </code>
     não pode ser aplicada após
     <code class="structfield">
      aggfinalfn
     </code>
     , ou
     <code class="literal">
      w
     </code>
     se escreve sobre o valor
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      aggmfinalmodify
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     Como
     <code class="structfield">
      aggfinalmodify
     </code>
     , mas para o
     <code class="structfield">
      aggmfinalfn
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      aggsortop
     </code>
     <code class="type">
      oid
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
     Operador de classificação associado (zero se nenhum)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      aggtranstype
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
     Tipo de dados do conjunto de dados de transição interna (estado) da função agregada
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      aggtransspace
     </code>
     <code class="type">
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
     <code class="structfield">
      aggmtranstype
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
     Tipo de dados do conjunto de dados de transição interna (estado) da função agregada para o modo de agregação móvel (zero se nenhum)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      aggmtransspace
     </code>
     <code class="type">
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
     <code class="structfield">
      agginitval
     </code>
     <code class="type">
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
     <code class="structfield">
      aggminitval
     </code>
     <code class="type">
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
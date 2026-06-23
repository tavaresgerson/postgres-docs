## 52.39. `pg_proc` [#](#CATALOG-PG-PROC)

O catálogo `pg_proc` armazena informações sobre funções, procedimentos, funções agregadas e funções de janela (coletivamente também conhecidas como rotinas). Consulte [CREATE FUNCTION](sql-createfunction.md "CREATE FUNCTION"), [CREATE PROCEDURE](sql-createprocedure.md "CREATE PROCEDURE") e [Seção 36.3](xfunc.md "36.3. User-Defined Functions") para obter mais informações.

Se `prokind` indicar que a entrada é para uma função agregada, deve haver uma linha correspondente em [`pg_aggregate`](catalog-pg-aggregate.md "52.2. pg_aggregate").

**Tabela 52.39. Colunas `pg_proc`**



<table border="1" class="table" summary="pg_proc Columns">
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
      proname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Nome da função
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      pronamespace
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
     O OID do espaço de nome que contém essa função
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      proowner
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
      <code class="structname">
       pg_authid
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     Proprietário da função
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      prolang
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-language.md" title="52.29. pg_language">
      <code class="structname">
       pg_language
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     Idioma de implementação ou interface de chamada dessa função
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      procost
     </code>
     <code class="type">
      float4
     </code>
    </p>
    <p>
     Custo estimado de execução (em unidades de
     <a class="xref" href="runtime-config-query.md#GUC-CPU-OPERATOR-COST">
      cpu_operator_cost
     </a>
     ); se
     <code class="structfield">
      proretset
     </code>
     , esse é o custo por linha devolvida
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      prorows
     </code>
     <code class="type">
      float4
     </code>
    </p>
    <p>
     Número estimado de linhas de resultado (zero se não
     <code class="structfield">
      proretset
     </code>
     )
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      provariadic
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
     Tipo de dados dos elementos do parâmetro de matriz variadic, ou zero se a função não tiver um parâmetro variadic
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      prosupport
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
     Função de suporte ao planejador para esta função (consulte
     <a class="xref" href="xfunc-optimization.md" title="36.11. Function Optimization Information">
      Seção 36.11
     </a>
     ), ou zero se nenhum
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      prokind
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     <code class="literal">
      f
     </code>
     para uma função normal,
     <code class="literal">
      p
     </code>
     para um procedimento,
     <code class="literal">
      a
     </code>
     para uma função agregada, ou
     <code class="literal">
      w
     </code>
     para uma função de janela
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      prosecdef
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     A função é um definidor de segurança (ou seja, um
     <span class="quote">
      “
      <span class="quote">
       setuid
      </span>
      ”
     </span>
     função)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      proleakproof
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     A função não tem efeitos colaterais. Nenhuma informação sobre os argumentos é transmitida, exceto através do valor de retorno. Qualquer função que possa lançar um erro dependendo dos valores de seus argumentos não é à prova de vazamento.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      proisstrict
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     A função retorna null se qualquer argumento da chamada for null. Nesse caso, a função não será realmente chamada. Funções que não
     <span class="quote">
      “
      <span class="quote">
       rigoroso
      </span>
      ”
     </span>
     deve estar preparado para lidar com entradas nulos.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      proretset
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     A função retorna um conjunto (ou seja, vários valores do tipo de dados especificado)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      provolatile
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     <code class="structfield">
      provolatile
     </code>
     indica se o resultado da função depende apenas de seus argumentos de entrada, ou se é afetado por fatores externos. É
     <code class="literal">
      i
     </code>
     para
     <span class="quote">
      “
      <span class="quote">
       immuável
      </span>
      ”
     </span>
     funções, que sempre produzem o mesmo resultado para os mesmos inputs. É
     <code class="literal">
      s
     </code>
     para
     <span class="quote">
      “
      <span class="quote">
       estável
      </span>
      ”
     </span>
     funções, cujos resultados (para entradas fixas) não mudam durante uma varredura. É
     <code class="literal">
      v
     </code>
     para
     <span class="quote">
      “
      <span class="quote">
       volátil
      </span>
      ”
     </span>
     funções, cujos resultados podem mudar a qualquer momento. (Use
     <code class="literal">
      v
     </code>
     também para funções com efeitos colaterais, para que as chamadas a elas não possam ser otimizadas.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      proparallel
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     <code class="structfield">
      proparallel
     </code>
     indica se a função pode ser executada com segurança no modo paralelo. É
     <code class="literal">
      s
     </code>
     para funções que são seguras para execução em modo paralelo sem restrições. É
     <code class="literal">
      r
     </code>
     para funções que podem ser executadas em modo paralelo, mas cuja execução é restrita ao líder do grupo paralelo; os processos de trabalho paralelos não podem invocar essas funções. É
     <code class="literal">
      u
     </code>
     para funções que são inseguras no modo paralelo; a presença de tal função obriga um plano de execução em série.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      pronargs
     </code>
     <code class="type">
      int2
     </code>
    </p>
    <p>
     Número de argumentos de entrada
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      pronargdefaults
     </code>
     <code class="type">
      int2
     </code>
    </p>
    <p>
     Número de argumentos que têm opções padrão
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      prorettype
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
     Tipo de dados do valor de retorno
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      proargtypes
     </code>
     <code class="type">
      oidvector
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
     Uma série dos tipos de dados dos argumentos da função. Isso inclui apenas argumentos de entrada (incluindo
     <code class="literal">
      INOUT
     </code>
     e
     <code class="literal">
      VARIADIC
     </code>
     argumentos), e, portanto, representa a assinatura de chamada da função.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      proallargtypes
     </code>
     <code class="type">
      oid[]
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
     Uma série dos tipos de dados dos argumentos da função. Isso inclui todos os argumentos (incluindo
     <code class="literal">
      OUT
     </code>
     e
     <code class="literal">
      INOUT
     </code>
     argumentos); no entanto, se todos os argumentos forem
     <code class="literal">
      IN
     </code>
     argumentos, este campo será nulo. Observe que a subscrita é baseada em 1, enquanto por razões históricas
     <code class="structfield">
      proargtypes
     </code>
     é subscrita a partir de 0.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      proargmodes
     </code>
     <code class="type">
      char[]
     </code>
    </p>
    <p>
     Uma série dos modos dos argumentos da função, codificados como
     <code class="literal">
      i
     </code>
     para
     <code class="literal">
      IN
     </code>
     argumentos,
     <code class="literal">
      o
     </code>
     para
     <code class="literal">
      OUT
     </code>
     argumentos,
     <code class="literal">
      b
     </code>
     para
     <code class="literal">
      INOUT
     </code>
     argumentos,
     <code class="literal">
      v
     </code>
     para
     <code class="literal">
      VARIADIC
     </code>
     argumentos,
     <code class="literal">
      t
     </code>
     para
     <code class="literal">
      TABLE
     </code>
     argumentos. Se todos os argumentos forem
     <code class="literal">
      IN
     </code>
     argumentos, este campo será nulo. Observe que os subíndices correspondem às posições de
     <code class="structfield">
      proallargtypes
     </code>
     não
     <code class="structfield">
      proargtypes
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      proargnames
     </code>
     <code class="type">
      text[]
     </code>
    </p>
    <p>
     Uma matriz com os nomes dos argumentos da função. Os argumentos sem nome são definidos como strings vazias na matriz. Se nenhum dos argumentos tiver um nome, este campo será nulo. Observe que os subíndices correspondem às posições
     <code class="structfield">
      proallargtypes
     </code>
     não
     <code class="structfield">
      proargtypes
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      proargdefaults
     </code>
     <code class="type">
      pg_node_tree
     </code>
    </p>
    <p>
     árvores de expressão (em
     <code class="function">
      nodeToString()
     </code>
     representação) para valores padrão. Esta é uma lista com
     <code class="structfield">
      pronargdefaults
     </code>
     elementos, correspondentes à última
     <em class="replaceable">
      <code>
       N
      </code>
     </em>
     <span class="emphasis">
      <em>
       entrada
      </em>
     </span>
     argumentos (ou seja, o último
     <em class="replaceable">
      <code>
       N
      </code>
     </em>
     <code class="structfield">
      proargtypes
     </code>
     posições).  Se nenhum dos argumentos tiver um valor padrão, este campo será nulo.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      protrftypes
     </code>
     <code class="type">
      oid[]
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
     Uma matriz dos tipos de dados de argumento/resultado para os quais aplicar transformações (da função)
     <code class="literal">
      TRANSFORM
     </code>
     cláusula). Vazio se não houver.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      prosrc
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Isso indica ao manipulador da função como invocar a função. Pode ser o código-fonte real da função para linguagens interpretadas, um símbolo de ligação, um nome de arquivo ou qualquer outra coisa, dependendo da linguagem de implementação/convenção de chamada.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      probin
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Informações adicionais sobre como invocar a função. Novamente, a interpretação é específica para o idioma.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      prosqlbody
     </code>
     <code class="type">
      pg_node_tree
     </code>
    </p>
    <p>
     Corpo de função SQL pré-parada. Isso é usado para funções de linguagem SQL quando o corpo é dado em notação padrão SQL, em vez de como uma literal de string. É nulo em outros casos.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      proconfig
     </code>
     <code class="type">
      text[]
     </code>
    </p>
    <p>
     Configurações locais do recurso para variáveis de configuração de tempo de execução
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      proacl
     </code>
     <code class="type">
      aclitem[]
     </code>
    </p>
    <p>
     Privilegios de acesso; veja
     <a class="xref" href="ddl-priv.md" title="5.8. Privileges">
      Seção 5.8
     </a>
     para detalhes
    </p>
   </td>
  </tr>
 </tbody>
</table>










Para funções compiladas, tanto as integradas quanto as carregadas dinamicamente, `prosrc` contém o nome da função em linguagem C (símbolo de ligação). Para funções de linguagem SQL, `prosrc` contém o texto de fonte da função, se isso for especificado como uma literal de string; mas se o corpo da função for especificado no estilo padrão SQL, `prosrc` é inutilizado (tipicamente é uma string vazia) e `prosqlbody` contém a definição pré-parada. Para todos os outros tipos de linguagem atualmente conhecidos, `prosrc` contém o texto de fonte da função. `probin` é nu, exceto para funções C carregadas dinamicamente, para as quais ele dá o nome do arquivo da biblioteca compartilhada que contém a função.
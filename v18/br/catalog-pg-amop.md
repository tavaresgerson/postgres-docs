## 52.4. `pg_amop` [#](#CATALOG-PG-AMOP)

O catálogo `pg_amop` armazena informações sobre operadores associados a famílias de métodos de acesso. Há uma linha para cada operador que é membro de uma família de operadores. Um membro da família pode ser um operador *de pesquisa* ou um operador *de ordenação*. Um operador pode aparecer em mais de uma família, mas não pode aparecer em mais de uma posição de pesquisa nem em mais de uma posição de ordenação dentro de uma família. (É permitido, embora improvável, que um operador seja usado tanto para fins de pesquisa quanto para fins de ordenação.)

**Tabela 52.4. Colunas `pg_amop`**



<table border="1" class="table" summary="pg_amop Columns">
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
      amopfamily
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-opfamily.md" title="52.35. pg_opfamily">
      <code class="structname">
       pg_opfamily
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     A família do operador esta entrada é para
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      amoplefttype
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
     Tipo de dados de entrada da mão esquerda do operador
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      amoprighttype
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
     Tipo de dados de entrada da mão direita do operador
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      amopstrategy
     </code>
     <code class="type">
      int2
     </code>
    </p>
    <p>
     Número da estratégia do operador
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      amoppurpose
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     Propósito do operador, ou seja,
     <code class="literal">
      s
     </code>
     para pesquisa ou
     <code class="literal">
      o
     </code>
     para encomendar
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      amopopr
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
     OID do operador
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      amopmethod
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-am.md" title="52.3. pg_am">
      <code class="structname">
       pg_am
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     O método de acesso ao índice é para a família de operadores
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      amopsortfamily
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-opfamily.md" title="52.35. pg_opfamily">
      <code class="structname">
       pg_opfamily
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     A família de operadores de árvore B, conforme esta entrada é classificada, se for um operador de ordenação; zero, se for um operador de busca
    </p>
   </td>
  </tr>
 </tbody>
</table>










Uma entrada de operador de pesquisa indica que um índice dessa família de operadores pode ser pesquisado para encontrar todas as linhas que satisfazem `WHERE` * `indexed_column` * `operator` * `constant`. Obviamente, tal operador deve retornar `boolean`, e seu tipo de entrada à esquerda deve corresponder ao tipo de dados da coluna do índice.

Uma entrada de operador de "ordem" indica que um índice desta família de operadores pode ser percorrido para retornar linhas na ordem representada por `ORDER BY` *`indexed_column`* *`operator`* *`constant`*. Tal operador pode retornar qualquer tipo de dados ordenável, embora, novamente, seu tipo de entrada à esquerda deve corresponder ao tipo de dados da coluna do índice. A semântica exata do `ORDER BY` é especificada pela coluna `amopsortfamily`, que deve referenciar uma família de operadores de árvore B para o tipo de resultado do operador.

### Nota

Atualmente, assume-se que a ordem de classificação para um operador de classificação é a padrão para a família de operadores referenciada, ou seja, `ASC NULLS LAST`. Isso pode ser relaxado algum dia, adicionando colunas adicionais para especificar opções de classificação explicitamente.

A entrada `amopmethod` deve corresponder ao `opfmethod` da sua família de operadores contida (incluindo `amopmethod` aqui é uma denormalização intencional da estrutura do catálogo por razões de desempenho). Além disso, `amoplefttype` e `amoprighttype` devem corresponder aos campos `oprleft` e `oprright` da entrada referenciada [`pg_operator`](catalog-pg-operator.md "52.34. pg_operator").
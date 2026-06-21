## 52.7. `pg_attribute` [#](#CATALOG-PG-ATTRIBUTE)

O catálogo `pg_attribute` armazena informações sobre as colunas da tabela. Haverá exatamente uma linha `pg_attribute` para cada coluna em todas as tabelas do banco de dados. (Também haverá entradas de atributo para índices e, de fato, todos os objetos que têm entradas [`pg_class`](catalog-pg-class.md "52.11. pg_class").)

O termo atributo é equivalente a coluna e é usado por razões históricas.

**Tabela 52.7. Colunas `pg_attribute`**



<table border="1" class="table" summary="pg_attribute Columns">
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
      attrelid
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
     A tabela a que esta coluna pertence
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      attname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     O nome da coluna
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      atttypid
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
     O tipo de dados desta coluna (zero para uma coluna descartada)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      attlen
     </code>
     <code class="type">
      int2
     </code>
    </p>
    <p>
     Uma cópia de
     <code class="literal">
      pg_type.typlen
     </code>
     do tipo desta coluna
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      attnum
     </code>
     <code class="type">
      int2
     </code>
    </p>
    <p>
     O número da coluna. As colunas comuns são numeradas de 1 em diante. As colunas do sistema, como
     <code class="structfield">
      ctid
     </code>
     , têm números (arbitrários) negativos.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      atttypmod
     </code>
     <code class="type">
      int4
     </code>
    </p>
    <p>
     <code class="structfield">
      atttypmod
     </code>
     registros de dados específicos para o tipo fornecidos no momento da criação da tabela (por exemplo, o comprimento máximo de um
     <code class="type">
      varchar
     </code>
     coluna). É passado para funções de entrada específicas para o tipo e funções de coação de comprimento. O valor geralmente será -1 para tipos que não precisam
     <code class="structfield">
      atttypmod
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      attndims
     </code>
     <code class="type">
      int2
     </code>
    </p>
    <p>
     Número de dimensões, se a coluna for um tipo de matriz; caso contrário, 0. (Atualmente, o número de dimensões de uma matriz não é exigido, então qualquer valor não nulo significa efetivamente
     <span class="quote">
      “
      <span class="quote">
       é um array
      </span>
      ”
     </span>
     .)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      attbyval
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Uma cópia de
     <code class="literal">
      pg_type.typbyval
     </code>
     do tipo desta coluna
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      attalign
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     Uma cópia de
     <code class="literal">
      pg_type.typalign
     </code>
     do tipo desta coluna
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      attstorage
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     Normalmente, uma cópia de
     <code class="literal">
      pg_type.typstorage
     </code>
     do tipo desta coluna. Para tipos de dados TOAST-áveis, isso pode ser alterado após a criação da coluna para controlar a política de armazenamento.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      attcompression
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     O método atual de compressão da coluna. Normalmente, isso
     <code class="literal">
      '\0'
     </code>
     especificar o uso da configuração padrão atual
     <a class="xref" href="runtime-config-client.md#GUC-DEFAULT-TOAST-COMPRESSION">
      default_toast_compression
     </a>
     ). Caso contrário,
     <code class="literal">
      'p'
     </code>
     seleciona a compressão pglz, enquanto
     <code class="literal">
      'l'
     </code>
     seleciona
     <span class="productname">
      LZ4
     </span>
     compressão. No entanto, este campo é ignorado sempre que
     <code class="structfield">
      attstorage
     </code>
     não permite compressão.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      attnotnull
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Esta coluna tem uma restrição (possivelmente inválida) de não nulo.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      atthasdef
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Esta coluna tem uma expressão padrão ou expressão de geração, no caso, haverá uma entrada correspondente no
     <a class="link" href="catalog-pg-attrdef.md" title="52.6. pg_attrdef">
      <code class="structname">
       pg_attrdef
      </code>
     </a>
     um catálogo que, na verdade, define a expressão. (Verifique
     <code class="structfield">
      attgenerated
     </code>
     para determinar se se trata de uma expressão padrão ou de uma expressão de geração.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      atthasmissing
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Esta coluna tem um valor que é usado quando a coluna está completamente ausente na linha, como acontece quando uma coluna é adicionada com um não volátil
     <code class="literal">
      DEFAULT
     </code>
     valor após a criação da linha. O valor real utilizado é armazenado na
     <code class="structfield">
      attmissingval
     </code>
     column.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      attidentity
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     Se um byte zero (
     <code class="literal">
      ''
     </code>
     ), então não é uma coluna de identidade. Caso contrário,
     <code class="literal">
      a
     </code>
     = gerado sempre,
     <code class="literal">
      d
     </code>
     = gerado por padrão.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      attgenerated
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     Se um byte zero (
     <code class="literal">
      ''
     </code>
     ), então não é uma coluna gerada. Caso contrário,
     <code class="literal">
      s
     </code>
     = armazenado,
     <code class="literal">
      v
     </code>
     = virtual. Uma coluna gerada armazenada é armazenada fisicamente como uma coluna normal. Uma coluna gerada virtual é armazenada fisicamente como um valor nulo, com o valor real sendo calculado no momento da execução.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      attisdropped
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Essa coluna foi descartada e não é mais válida. Uma coluna descartada ainda está fisicamente presente na tabela, mas é ignorada pelo analisador e, portanto, não pode ser acessada via SQL.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      attislocal
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Essa coluna é definida localmente na relação. Observe que uma coluna pode ser definida localmente e herdada simultaneamente.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      attinhcount
     </code>
     <code class="type">
      int2
     </code>
    </p>
    <p>
     O número de ancestrais diretos que esta coluna tem. Uma coluna com um número não nulo de ancestrais não pode ser excluída nem renomeada.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      attcollation
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-collation.md" title="52.12. pg_collation">
      <code class="structname">
       pg_collation
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     A correção definida da coluna, ou zero se a coluna não for de um tipo de dados correável
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      attstattarget
     </code>
     <code class="type">
      int2
     </code>
    </p>
    <p>
     <code class="structfield">
      attstattarget
     </code>
     controla o nível de detalhe das estatísticas acumuladas para esta coluna por
     <a class="link" href="sql-analyze.md" title="ANALYZE">
      <code class="command">
       ANALYZE
      </code>
     </a>
     Um valor nulo indica que não devem ser coletadas estatísticas. Um valor nulo diz para usar o alvo de estatísticas padrão do sistema. O significado exato dos valores positivos depende do tipo de dados. Para tipos de dados escalares,
     <code class="structfield">
      attstattarget
     </code>
     é o número alvo
     <span class="quote">
      “
      <span class="quote">
       os valores mais comuns
      </span>
      ”
     </span>
     para coletar e o número alvo de bins do histograma a serem criados.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      attacl
     </code>
     <code class="type">
      aclitem[]
     </code>
    </p>
    <p>
     Privilegios de acesso ao nível da coluna, se houver sido concedidos especificamente nesta coluna
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      attoptions
     </code>
     <code class="type">
      text[]
     </code>
    </p>
    <p>
     Opções de nível de atributo, como
     <span class="quote">
      “
      <span class="quote">
       palavra-chave=valor
      </span>
      ”
     </span>
     cordas
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      attfdwoptions
     </code>
     <code class="type">
      text[]
     </code>
    </p>
    <p>
     Opções de wrapper de dados estrangeiros em nível de atributo, como
     <span class="quote">
      “
      <span class="quote">
       palavra-chave=valor
      </span>
      ”
     </span>
     cordas
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      attmissingval
     </code>
     <code class="type">
      anyarray
     </code>
    </p>
    <p>
     Esta coluna tem um array de um elemento que contém o valor usado quando a coluna está inteiramente ausente na linha, como acontece quando a coluna é adicionada com um não volátil
     <code class="literal">
      DEFAULT
     </code>
     valor após a criação da linha. O valor é usado apenas quando
     <code class="structfield">
      atthasmissing
     </code>
     É verdade. Se não houver valor, a coluna é nula.
    </p>
   </td>
  </tr>
 </tbody>
</table>










Na entrada do `pg_attribute` de uma coluna excluída, o `atttypid` é redefinido para zero, mas o `attlen` e os outros campos copiados do [`pg_type`](catalog-pg-type.md "52.64. pg_type") ainda são válidos. Esse arranjo é necessário para lidar com a situação em que o tipo de dados da coluna excluída foi posteriormente excluído, e, portanto, não há mais uma linha de `pg_type`. O `attlen` e os outros campos podem ser usados para interpretar o conteúdo de uma linha da tabela.
## 52.7. `pg_attribute` [#](#CATALOG-PG-ATTRIBUTE)

O catálogo `pg_attribute` armazena informações sobre as colunas da tabela. Haverá exatamente uma linha `pg_attribute` para cada coluna em todas as tabelas do banco de dados. (Também haverá entradas de atributo para índices e, de fato, todos os objetos que têm entradas [`pg_class`](catalog-pg-class.md "52.11. pg_class").)

O termo atributo é equivalente a coluna e é usado por razões históricas.

**Tabela 52.7. Colunas `pg_attribute`**



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
      attrelid
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
     A tabela a que esta coluna pertence
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      attname
     </code>
     <code>
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
     <code>
      atttypid
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
     O tipo de dados desta coluna (zero para uma coluna descartada)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      attlen
     </code>
     <code>
      int2
     </code>
    </p>
    <p>
     Uma cópia de
     <code>
      pg_type.typlen
     </code>
     do tipo desta coluna
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      attnum
     </code>
     <code>
      int2
     </code>
    </p>
    <p>
     O número da coluna. As colunas comuns são numeradas de 1 em diante. As colunas do sistema, como
     <code>
      ctid
     </code>
     , têm números (arbitrários) negativos.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      atttypmod
     </code>
     <code>
      int4
     </code>
    </p>
    <p>
     <code>
      atttypmod
     </code>
     registros de dados específicos para o tipo fornecidos no momento da criação da tabela (por exemplo, o comprimento máximo de um
     <code>
      varchar
     </code>
     coluna). É passado para funções de entrada específicas para o tipo e funções de coação de comprimento. O valor geralmente será -1 para tipos que não precisam
     <code>
      atttypmod
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      attndims
     </code>
     <code>
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
     <code>
      attbyval
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Uma cópia de
     <code>
      pg_type.typbyval
     </code>
     do tipo desta coluna
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      attalign
     </code>
     <code>
      char
     </code>
    </p>
    <p>
     Uma cópia de
     <code>
      pg_type.typalign
     </code>
     do tipo desta coluna
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      attstorage
     </code>
     <code>
      char
     </code>
    </p>
    <p>
     Normalmente, uma cópia de
     <code>
      pg_type.typstorage
     </code>
     do tipo desta coluna. Para tipos de dados TOAST-áveis, isso pode ser alterado após a criação da coluna para controlar a política de armazenamento.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      attcompression
     </code>
     <code>
      char
     </code>
    </p>
    <p>
     O método atual de compressão da coluna. Normalmente, isso
     <code>
      '\0'
     </code>
     especificar o uso da configuração padrão atual
     <a class="xref" href="runtime-config-client.md#GUC-DEFAULT-TOAST-COMPRESSION">
      default_toast_compression
     </a>
     ). Caso contrário,
     <code>
      'p'
     </code>
     seleciona a compressão pglz, enquanto
     <code>
      'l'
     </code>
     seleciona
     <span class="productname">
      LZ4
     </span>
     compressão. No entanto, este campo é ignorado sempre que
     <code>
      attstorage
     </code>
     não permite compressão.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      attnotnull
     </code>
     <code>
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
     <code>
      atthasdef
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Esta coluna tem uma expressão padrão ou expressão de geração, no caso, haverá uma entrada correspondente no
     <a class="link" href="catalog-pg-attrdef.md" title="52.6. pg_attrdef">
      <code>
       pg_attrdef
      </code>
     </a>
     um catálogo que, na verdade, define a expressão. (Verifique
     <code>
      attgenerated
     </code>
     para determinar se se trata de uma expressão padrão ou de uma expressão de geração.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      atthasmissing
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Esta coluna tem um valor que é usado quando a coluna está completamente ausente na linha, como acontece quando uma coluna é adicionada com um não volátil
     <code>
      DEFAULT
     </code>
     valor após a criação da linha. O valor real utilizado é armazenado na
     <code>
      attmissingval
     </code>
     column.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      attidentity
     </code>
     <code>
      char
     </code>
    </p>
    <p>
     Se um byte zero (
     <code>
      ''
     </code>
     ), então não é uma coluna de identidade. Caso contrário,
     <code>
      a
     </code>
     = gerado sempre,
     <code>
      d
     </code>
     = gerado por padrão.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      attgenerated
     </code>
     <code>
      char
     </code>
    </p>
    <p>
     Se um byte zero (
     <code>
      ''
     </code>
     ), então não é uma coluna gerada. Caso contrário,
     <code>
      s
     </code>
     = armazenado,
     <code>
      v
     </code>
     = virtual. Uma coluna gerada armazenada é armazenada fisicamente como uma coluna normal. Uma coluna gerada virtual é armazenada fisicamente como um valor nulo, com o valor real sendo calculado no momento da execução.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      attisdropped
     </code>
     <code>
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
     <code>
      attislocal
     </code>
     <code>
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
     <code>
      attinhcount
     </code>
     <code>
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
     <code>
      attcollation
     </code>
     <code>
      oid
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
     A correção definida da coluna, ou zero se a coluna não for de um tipo de dados correável
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      attstattarget
     </code>
     <code>
      int2
     </code>
    </p>
    <p>
     <code>
      attstattarget
     </code>
     controla o nível de detalhe das estatísticas acumuladas para esta coluna por
     <a class="link" href="sql-analyze.md" title="ANALYZE">
      <code>
       ANALYZE
      </code>
     </a>
     Um valor nulo indica que não devem ser coletadas estatísticas. Um valor nulo diz para usar o alvo de estatísticas padrão do sistema. O significado exato dos valores positivos depende do tipo de dados. Para tipos de dados escalares,
     <code>
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
     <code>
      attacl
     </code>
     <code>
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
     <code>
      attoptions
     </code>
     <code>
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
     <code>
      attfdwoptions
     </code>
     <code>
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
     <code>
      attmissingval
     </code>
     <code>
      anyarray
     </code>
    </p>
    <p>
     Esta coluna tem um array de um elemento que contém o valor usado quando a coluna está inteiramente ausente na linha, como acontece quando a coluna é adicionada com um não volátil
     <code>
      DEFAULT
     </code>
     valor após a criação da linha. O valor é usado apenas quando
     <code>
      atthasmissing
     </code>
     É verdade. Se não houver valor, a coluna é nula.
    </p>
   </td>
  </tr>
 </tbody>
</table>










Na entrada do `pg_attribute` de uma coluna excluída, o `atttypid` é redefinido para zero, mas o `attlen` e os outros campos copiados do [`pg_type`](catalog-pg-type.md "52.64. pg_type") ainda são válidos. Esse arranjo é necessário para lidar com a situação em que o tipo de dados da coluna excluída foi posteriormente excluído, e, portanto, não há mais uma linha de `pg_type`. O `attlen` e os outros campos podem ser usados para interpretar o conteúdo de uma linha da tabela.
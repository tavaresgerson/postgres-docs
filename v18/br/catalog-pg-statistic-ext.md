## 52.52. `pg_statistic_ext` [#](#CATALOG-PG-STATISTIC-EXT)

O catálogo `pg_statistic_ext` contém definições de estatísticas de planejador estendido. Cada linha deste catálogo corresponde a um *objeto de estatísticas* criado com [`CREATE STATISTICS`](sql-createstatistics.md "CREATE STATISTICS").

**Tabela 52.52. Colunas `pg_statistic_ext`**



<table border="1" class="table" summary="pg_statistic_ext Columns">
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
      stxrelid
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
     Tabela contendo as colunas descritas por este objeto
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      stxname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Nome do objeto de estatísticas
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      stxnamespace
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
     O OID do espaço de nomes que contém este objeto de estatísticas
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      stxowner
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
     Proprietário do objeto de estatísticas
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      stxkeys
     </code>
     <code class="type">
      int2vector
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
     Uma série de números de atributos, indicando quais colunas da tabela são cobertas por este objeto de estatísticas; por exemplo, um valor de
     <code class="literal">
      1 3
     </code>
     significaria que as primeiras e as colunas da terceira tabela estão cobertas
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      stxstattarget
     </code>
     <code class="type">
      int2
     </code>
    </p>
    <p>
     <code class="structfield">
      stxstattarget
     </code>
     controla o nível de detalhe das estatísticas acumuladas para este objeto estatístico por
     <a class="link" href="sql-analyze.md" title="ANALYZE">
      <code class="command">
       ANALYZE
      </code>
     </a>
     Um valor nulo indica que não devem ser coletadas estatísticas. Um valor nulo diz para usar o máximo dos objetivos de estatísticas das colunas referenciadas, se configurados, ou o objetivo de estatísticas padrão do sistema. Valores positivos de
     <code class="structfield">
      stxstattarget
     </code>
     determine o número alvo de
     <span class="quote">
      “
      <span class="quote">
       os valores mais comuns
      </span>
      ”
     </span>
     para coletar.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      stxkind
     </code>
     <code class="type">
      char[]
     </code>
    </p>
    <p>
     Um array contendo códigos para os tipos de estatísticas habilitados; os valores válidos são:
     <code class="literal">
      d
     </code>
     para n estatísticas distintas,
     <code class="literal">
      f
     </code>
     para estatísticas de dependência funcional,
     <code class="literal">
      m
     </code>
     para a lista de estatísticas de valores mais comuns (MCV), e
     <code class="literal">
      e
     </code>
     para estatísticas de expressão
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      stxexprs
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
     (representação) para atributos de objeto de estatísticas que não são referências simples de coluna. Esta é uma lista com um elemento por expressão. Nulo se todos os atributos de objeto de estatísticas forem referências simples.
    </p>
   </td>
  </tr>
 </tbody>
</table>









A entrada `pg_statistic_ext` é preenchida completamente durante `CREATE STATISTICS`(sql-createstatistics.md "CREATE STATISTICS"), mas os valores estatísticos reais não são calculados nessa etapa. Os comandos subsequentes `ANALYZE`(sql-analyze.md "ANALYZE") calculam os valores desejados e preenchem uma entrada no catálogo `pg_statistic_ext_data`(catalog-pg-statistic-ext-data.md "52.53. pg_statistic_ext_data").
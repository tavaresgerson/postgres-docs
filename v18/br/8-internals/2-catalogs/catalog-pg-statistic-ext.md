## 52.52. `pg_statistic_ext` [#](#CATALOG-PG-STATISTIC-EXT)

O catálogo `pg_statistic_ext` contém definições de estatísticas de planejador estendido. Cada linha deste catálogo corresponde a um *objeto de estatísticas* criado com [`CREATE STATISTICS`](sql-createstatistics.md "CREATE STATISTICS").

**Tabela 52.52. Colunas `pg_statistic_ext`**



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
      stxrelid
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
     Tabela contendo as colunas descritas por este objeto
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      stxname
     </code>
     <code>
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
     <code>
      stxnamespace
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-namespace.md" title="52.32. pg_namespace">
      <code>
       pg_namespace
      </code>
     </a>
     .
     <code>
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
     <code>
      stxowner
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
      <code>
       pg_authid
      </code>
     </a>
     .
     <code>
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
     <code>
      stxkeys
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
     Uma série de números de atributos, indicando quais colunas da tabela são cobertas por este objeto de estatísticas; por exemplo, um valor de
     <code>
      1 3
     </code>
     significaria que as primeiras e as colunas da terceira tabela estão cobertas
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      stxstattarget
     </code>
     <code>
      int2
     </code>
    </p>
    <p>
     <code>
      stxstattarget
     </code>
     controla o nível de detalhe das estatísticas acumuladas para este objeto estatístico por
     <a class="link" href="sql-analyze.md" title="ANALYZE">
      <code>
       ANALYZE
      </code>
     </a>
     Um valor nulo indica que não devem ser coletadas estatísticas. Um valor nulo diz para usar o máximo dos objetivos de estatísticas das colunas referenciadas, se configurados, ou o objetivo de estatísticas padrão do sistema. Valores positivos de
     <code>
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
     <code>
      stxkind
     </code>
     <code>
      char[]
     </code>
    </p>
    <p>
     Um array contendo códigos para os tipos de estatísticas habilitados; os valores válidos são:
     <code>
      d
     </code>
     para n estatísticas distintas,
     <code>
      f
     </code>
     para estatísticas de dependência funcional,
     <code>
      m
     </code>
     para a lista de estatísticas de valores mais comuns (MCV), e
     <code>
      e
     </code>
     para estatísticas de expressão
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      stxexprs
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
     (representação) para atributos de objeto de estatísticas que não são referências simples de coluna. Esta é uma lista com um elemento por expressão. Nulo se todos os atributos de objeto de estatísticas forem referências simples.
    </p>
   </td>
  </tr>
 </tbody>
</table>










A entrada `pg_statistic_ext` é preenchida completamente durante `CREATE STATISTICS`(sql-createstatistics.md "CREATE STATISTICS"), mas os valores estatísticos reais não são calculados nessa etapa. Os comandos subsequentes `ANALYZE`(sql-analyze.md "ANALYZE") calculam os valores desejados e preenchem uma entrada no catálogo `pg_statistic_ext_data`(catalog-pg-statistic-ext-data.md "52.53. pg_statistic_ext_data").
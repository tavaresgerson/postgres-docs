## 52.59. `pg_ts_config` [#](#CATALOG-PG-TS-CONFIG)

O catálogo `pg_ts_config` contém entradas que representam configurações de pesquisa de texto. Uma configuração especifica um analisador de pesquisa de texto particular e uma lista de dicionários a serem usados para cada um dos tipos de token de saída do analisador. O analisador é mostrado na entrada `pg_ts_config`, mas a mapeamento de token a dicionário é definido por entradas subsidiárias em [`pg_ts_config_map`](catalog-pg-ts-config-map.md "52.60. pg_ts_config_map").

As funcionalidades de busca de texto do PostgreSQL são descritas em detalhes no [Capítulo 12](textsearch.md).

**Tabela 52.59. Colunas `pg_ts_config`**



<table border="1" class="table" summary="pg_ts_config Columns">
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
      cfgname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Nome da configuração de pesquisa de texto
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      cfgnamespace
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
     O OID do espaço de nome que contém essa configuração
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      cfgowner
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
     Proprietário da configuração
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      cfgparser
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-ts-parser.md" title="52.62. pg_ts_parser">
      <code class="structname">
       pg_ts_parser
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     O OID do analisador de busca de texto para esta configuração
    </p>
   </td>
  </tr>
 </tbody>
</table>






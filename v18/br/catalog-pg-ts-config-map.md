## 52.60. `pg_ts_config_map` [#](#CATALOG-PG-TS-CONFIG-MAP)

O catálogo `pg_ts_config_map` contém entradas que mostram quais dicionários de busca de texto devem ser consultados e na ordem correta para cada tipo de token de saída de cada analisador de configuração de busca de texto.

As funcionalidades de busca de texto do PostgreSQL são descritas em detalhes no [Capítulo 12](textsearch.md).

**Tabela 52.60. Colunas `pg_ts_config_map`**



<table border="1" class="table" summary="pg_ts_config_map Columns">
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
      mapcfg
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-ts-config.md" title="52.59. pg_ts_config">
      <code class="structname">
       pg_ts_config
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     O OID do
     <a class="link" href="catalog-pg-ts-config.md" title="52.59. pg_ts_config">
      <code class="structname">
       pg_ts_config
      </code>
     </a>
     entrada que possui esta entrada do mapa
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      maptokentype
     </code>
     <code class="type">
      int4
     </code>
    </p>
    <p>
     Um tipo de token emitido pelo analisador da configuração
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      mapseqno
     </code>
     <code class="type">
      int4
     </code>
    </p>
    <p>
     Ordem em que consultar esta entrada (inferior
     <code class="structfield">
      mapseqno
     </code>
     primeiro)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      mapdict
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-ts-dict.md" title="52.61. pg_ts_dict">
      <code class="structname">
       pg_ts_dict
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     O OID do dicionário de busca de texto a ser consultado
    </p>
   </td>
  </tr>
 </tbody>
</table>





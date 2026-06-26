## F.33. pgstattuple — obter estatísticas em nível de tupla [#](#PGSTATTUPLE)

* [F.33.1. Funções](pgstattuple.md#PGSTATTUPLE-FUNCS)
* [F.33.2. Autores](pgstattuple.md#PGSTATTUPLE-AUTHORS)

O módulo `pgstattuple` oferece várias funções para obter estatísticas em nível de tupla.

Como essas funções retornam informações detalhadas em nível de página, o acesso é restrito por padrão. Por padrão, apenas o papel `pg_stat_scan_tables` tem privilégio `EXECUTE`. Os superusuários, claro, contornam essa restrição. Após a extensão ter sido instalada, os usuários podem emitir comandos `GRANT` para alterar os privilégios das funções para permitir que outros as executem. No entanto, pode ser preferível adicionar esses usuários ao papel `pg_stat_scan_tables` em vez disso.

### F.33.1. Funções [#](#PGSTATTUPLE-FUNCS)

`pgstattuple(regclass) returns record`: `pgstattuple` retorna o comprimento físico de uma relação, a porcentagem de tuplas "mortas" e outras informações. Isso pode ajudar os usuários a determinar se o vácuo é necessário ou não. O argumento é o nome da relação alvo (opcionalmente qualificada pelo esquema) ou OID. Por exemplo:

```
test=> SELECT * FROM pgstattuple('pg_catalog.pg_proc'); -[ RECORD 1 ]------+------- table_len          | 458752 tuple_count        | 1470 tuple_len          | 438896 tuple_percent      | 95.67 dead_tuple_count   | 11 dead_tuple_len     | 3157 dead_tuple_percent | 0.69 free_space         | 8932 free_percent       | 1.95
```

As colunas de saída são descritas em [Tabela F.24](pgstattuple.md#PGSTATTUPLE-COLUMNS).

**Tabela F.24. Colunas de Saída `pgstattuple`**



<table>
 <colgroup>
  <col/>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Column
   </th>
   <th>
    Type
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     table_len
    </code>
   </td>
   <td>
    <code>
     bigint
    </code>
   </td>
   <td>
    Comprimento da relação física em bytes
   </td>
  </tr>
  <tr>
   <td>
    <code>
     tuple_count
    </code>
   </td>
   <td>
    <code>
     bigint
    </code>
   </td>
   <td>
    Número de tuplas vivas
   </td>
  </tr>
  <tr>
   <td>
    <code>
     tuple_len
    </code>
   </td>
   <td>
    <code>
     bigint
    </code>
   </td>
   <td>
    Total comprimento de tuplas vivas em bytes
   </td>
  </tr>
  <tr>
   <td>
    <code>
     tuple_percent
    </code>
   </td>
   <td>
    <code>
     float8
    </code>
   </td>
   <td>
    Porcentagem de tuplas vivas
   </td>
  </tr>
  <tr>
   <td>
    <code>
     dead_tuple_count
    </code>
   </td>
   <td>
    <code>
     bigint
    </code>
   </td>
   <td>
    Número de tuplas mortas
   </td>
  </tr>
  <tr>
   <td>
    <code>
     dead_tuple_len
    </code>
   </td>
   <td>
    <code>
     bigint
    </code>
   </td>
   <td>
    Total comprimento de tuplas mortas em bytes
   </td>
  </tr>
  <tr>
   <td>
    <code>
     dead_tuple_percent
    </code>
   </td>
   <td>
    <code>
     float8
    </code>
   </td>
   <td>
    Porcentagem de tuplas mortas
   </td>
  </tr>
  <tr>
   <td>
    <code>
     free_space
    </code>
   </td>
   <td>
    <code>
     bigint
    </code>
   </td>
   <td>
    Espaço livre total em bytes
   </td>
  </tr>
  <tr>
   <td>
    <code>
     free_percent
    </code>
   </td>
   <td>
    <code>
     float8
    </code>
   </td>
   <td>
    Porcentagem de espaço livre
   </td>
  </tr>
 </tbody>
</table>










Nota

O `table_len` será sempre maior que a soma dos `tuple_len`, `dead_tuple_len` e `free_space`. A diferença é contabilizada pelo overhead fixo da página, a tabela de per página de ponteiros para tuplas e o preenchimento para garantir que as tuplas estejam corretamente alinhadas.

`pgstattuple` adquire apenas um bloqueio de leitura na relação. Portanto, os resultados não refletem um instantâneo instantâneo; as atualizações concorrentes as afetarão.

`pgstattuple` julga que um tuplo é “morto” se `HeapTupleSatisfiesDirty` retorna falso.

`pgstattuple(text) returns record`: Isso é o mesmo que `pgstattuple(regclass)`, exceto que a relação de destino é especificada como TEXT. Esta função é mantida devido à compatibilidade reversa até o momento, e será descontinuada em algumas versões futuras.

`pgstatindex(regclass) returns record`: `pgstatindex` retorna um registro que mostra informações sobre um índice de árvore B. Por exemplo:

```
test=> SELECT * FROM pgstatindex('pg_cast_oid_index'); -[ RECORD 1 ]------+------ version            | 2 tree_level         | 0 index_size         | 16384 root_block_no      | 1 internal_pages     | 0 leaf_pages         | 1 empty_pages        | 0 deleted_pages      | 0 avg_leaf_density   | 54.27 leaf_fragmentation | 0
```

As colunas de saída são:



<table>
 <colgroup>
  <col/>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Column
   </th>
   <th>
    Type
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     version
    </code>
   </td>
   <td>
    <code>
     integer
    </code>
   </td>
   <td>
    Número da versão da árvore B
   </td>
  </tr>
  <tr>
   <td>
    <code>
     tree_level
    </code>
   </td>
   <td>
    <code>
     integer
    </code>
   </td>
   <td>
    Nível da árvore da página inicial
   </td>
  </tr>
  <tr>
   <td>
    <code>
     index_size
    </code>
   </td>
   <td>
    <code>
     bigint
    </code>
   </td>
   <td>
    Tamanho total do índice em bytes
   </td>
  </tr>
  <tr>
   <td>
    <code>
     root_block_no
    </code>
   </td>
   <td>
    <code>
     bigint
    </code>
   </td>
   <td>
    Localização da página raiz (zero se nenhuma)
   </td>
  </tr>
  <tr>
   <td>
    <code>
     internal_pages
    </code>
   </td>
   <td>
    <code>
     bigint
    </code>
   </td>
   <td>
    Número de
    <span class="quote">
     “
     <span class="quote">
      interno
     </span>
     ”
    </span>
    (páginas de nível superior)
   </td>
  </tr>
  <tr>
   <td>
    <code>
     leaf_pages
    </code>
   </td>
   <td>
    <code>
     bigint
    </code>
   </td>
   <td>
    Número de páginas de folha
   </td>
  </tr>
  <tr>
   <td>
    <code>
     empty_pages
    </code>
   </td>
   <td>
    <code>
     bigint
    </code>
   </td>
   <td>
    Número de páginas vazias
   </td>
  </tr>
  <tr>
   <td>
    <code>
     deleted_pages
    </code>
   </td>
   <td>
    <code>
     bigint
    </code>
   </td>
   <td>
    Número de páginas excluídas
   </td>
  </tr>
  <tr>
   <td>
    <code>
     avg_leaf_density
    </code>
   </td>
   <td>
    <code>
     float8
    </code>
   </td>
   <td>
    Densidade média das páginas de folha
   </td>
  </tr>
  <tr>
   <td>
    <code>
     leaf_fragmentation
    </code>
   </td>
   <td>
    <code>
     float8
    </code>
   </td>
   <td>
    Fragmentação de página de folha
   </td>
  </tr>
 </tbody>
</table>







O `index_size` relatado normalmente corresponderá a uma página a mais do que a contabilizada pelo `internal_pages + leaf_pages + empty_pages + deleted_pages`, porque também inclui a metapágina do índice.

Assim como no caso de `pgstattuple`, os resultados são acumulados página por página e não devem ser esperados para representar um instantâneo instantâneo de todo o índice.

`pgstatindex(text) returns record`: Isto é o mesmo que `pgstatindex(regclass)`, exceto que o índice alvo é especificado como TEXT. Esta função é mantida devido à compatibilidade reversa até agora, e será descontinuada em alguma versão futura.

`pgstatginindex(regclass) returns record`: `pgstatginindex` retorna um registro que mostra informações sobre um índice GIN. Por exemplo:

```
test=> SELECT * FROM pgstatginindex('test_gin_index'); -[ RECORD 1 ]--+-- version        | 1 pending_pages  | 0 pending_tuples | 0
```

As colunas de saída são:



<table>
 <colgroup>
  <col/>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Column
   </th>
   <th>
    Type
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     version
    </code>
   </td>
   <td>
    <code>
     integer
    </code>
   </td>
   <td>
    Número da versão do GIN
   </td>
  </tr>
  <tr>
   <td>
    <code>
     pending_pages
    </code>
   </td>
   <td>
    <code>
     integer
    </code>
   </td>
   <td>
    Número de páginas na lista pendente
   </td>
  </tr>
  <tr>
   <td>
    <code>
     pending_tuples
    </code>
   </td>
   <td>
    <code>
     bigint
    </code>
   </td>
   <td>
    Número de tuplas na lista pendente
   </td>
  </tr>
 </tbody>
</table>







`pgstathashindex(regclass) returns record`: `pgstathashindex` retorna um registro que mostra informações sobre um índice HASH. Por exemplo:

```
test=> select * from pgstathashindex('con_hash_index'); -[ RECORD 1 ]--+----------------- version        | 4 bucket_pages   | 33081 overflow_pages | 0 bitmap_pages   | 1 unused_pages   | 32455 live_items     | 10204006 dead_items     | 0 free_percent   | 61.8005949100872
```

As colunas de saída são:



<table>
 <colgroup>
  <col/>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Column
   </th>
   <th>
    Type
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     version
    </code>
   </td>
   <td>
    <code>
     integer
    </code>
   </td>
   <td>
    Número da versão HASH
   </td>
  </tr>
  <tr>
   <td>
    <code>
     bucket_pages
    </code>
   </td>
   <td>
    <code>
     bigint
    </code>
   </td>
   <td>
    Número de páginas do balde
   </td>
  </tr>
  <tr>
   <td>
    <code>
     overflow_pages
    </code>
   </td>
   <td>
    <code>
     bigint
    </code>
   </td>
   <td>
    Número de páginas de sobreposição
   </td>
  </tr>
  <tr>
   <td>
    <code>
     bitmap_pages
    </code>
   </td>
   <td>
    <code>
     bigint
    </code>
   </td>
   <td>
    Número de páginas em bitmap
   </td>
  </tr>
  <tr>
   <td>
    <code>
     unused_pages
    </code>
   </td>
   <td>
    <code>
     bigint
    </code>
   </td>
   <td>
    Número de páginas não utilizadas
   </td>
  </tr>
  <tr>
   <td>
    <code>
     live_items
    </code>
   </td>
   <td>
    <code>
     bigint
    </code>
   </td>
   <td>
    Número de tuplas vivas
   </td>
  </tr>
  <tr>
   <td>
    <code>
     dead_tuples
    </code>
   </td>
   <td>
    <code>
     bigint
    </code>
   </td>
   <td>
    Número de tuplas mortas
   </td>
  </tr>
  <tr>
   <td>
    <code>
     free_percent
    </code>
   </td>
   <td>
    <code>
     float
    </code>
   </td>
   <td>
    Porcentagem de espaço livre
   </td>
  </tr>
 </tbody>
</table>







`pg_relpages(regclass) returns bigint` : `pg_relpages` retorna o número de páginas na relação.

`pg_relpages(text) returns bigint`: Isto é o mesmo que `pg_relpages(regclass)`, exceto que a relação alvo é especificada como TEXT. Esta função é mantida devido à compatibilidade reversa até agora, e será descontinuada em alguma versão futura.

`pgstattuple_approx(regclass) returns record` é uma alternativa mais rápida a `pgstattuple` que retorna resultados aproximados. O argumento é o nome ou OID da relação de destino. Por exemplo:

```
test=> SELECT * FROM pgstattuple_approx('pg_catalog.pg_proc'::regclass); -[ RECORD 1 ]--------+------- table_len            | 573440 scanned_percent      | 2 approx_tuple_count   | 2740 approx_tuple_len     | 561210 approx_tuple_percent | 97.87 dead_tuple_count     | 0 dead_tuple_len       | 0 dead_tuple_percent   | 0 approx_free_space    | 11996 approx_free_percent  | 2.09
```

As colunas de saída são descritas em [Tabela F.25](pgstattuple.md#PGSTATAPPROX-COLUMNS).

Enquanto o `pgstattuple` sempre realiza uma varredura completa da tabela e retorna um contagem exata de tuplas vivas e mortas (e seus tamanhos) e espaço livre, o `pgstattuple_approx` tenta evitar a varredura completa da tabela e retorna estatísticas exatas de tuplas mortas, juntamente com uma aproximação do número e tamanho das tuplas vivas e espaço livre.

Isso é feito ignorando as páginas que possuem apenas tuplas visíveis, de acordo com o mapa de visibilidade (se uma página tiver o bit correspondente da VM definido, então é assumido que ela não contém tuplas mortas). Para essas páginas, ele deriva o valor do espaço livre a partir do mapa de espaço livre e assume que o restante do espaço na página é ocupado por tuplas vivas.

Para as páginas que não podem ser ignoradas, ele digitaliza cada tupla, registrando sua presença e tamanho nos contadores apropriados, e soma o espaço livre na página. No final, ele estima o número total de tuplas vivas com base no número de páginas e tuplas digitalizadas (do mesmo modo que o VACUUM estima pg_class.reltuples).

**Tabela F.25. Colunas de Saída `pgstattuple_approx`**



<table>
 <colgroup>
  <col/>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Column
   </th>
   <th>
    Type
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     table_len
    </code>
   </td>
   <td>
    <code>
     bigint
    </code>
   </td>
   <td>
    Comprimento da relação física em bytes (exato)
   </td>
  </tr>
  <tr>
   <td>
    <code>
     scanned_percent
    </code>
   </td>
   <td>
    <code>
     float8
    </code>
   </td>
   <td>
    Porcentagem de tabela escaneada
   </td>
  </tr>
  <tr>
   <td>
    <code>
     approx_tuple_count
    </code>
   </td>
   <td>
    <code>
     bigint
    </code>
   </td>
   <td>
    Número de tuplas vivas (estimação)
   </td>
  </tr>
  <tr>
   <td>
    <code>
     approx_tuple_len
    </code>
   </td>
   <td>
    <code>
     bigint
    </code>
   </td>
   <td>
    Total comprimento de tuplas vivas em bytes (estimação)
   </td>
  </tr>
  <tr>
   <td>
    <code>
     approx_tuple_percent
    </code>
   </td>
   <td>
    <code>
     float8
    </code>
   </td>
   <td>
    Porcentagem de tuplas vivas
   </td>
  </tr>
  <tr>
   <td>
    <code>
     dead_tuple_count
    </code>
   </td>
   <td>
    <code>
     bigint
    </code>
   </td>
   <td>
    Número de tuplas mortas (exato)
   </td>
  </tr>
  <tr>
   <td>
    <code>
     dead_tuple_len
    </code>
   </td>
   <td>
    <code>
     bigint
    </code>
   </td>
   <td>
    Total comprimento de tuplas mortas em bytes (exato)
   </td>
  </tr>
  <tr>
   <td>
    <code>
     dead_tuple_percent
    </code>
   </td>
   <td>
    <code>
     float8
    </code>
   </td>
   <td>
    Porcentagem de tuplas mortas
   </td>
  </tr>
  <tr>
   <td>
    <code>
     approx_free_space
    </code>
   </td>
   <td>
    <code>
     bigint
    </code>
   </td>
   <td>
    Espaço livre total em bytes (estimativa)
   </td>
  </tr>
  <tr>
   <td>
    <code>
     approx_free_percent
    </code>
   </td>
   <td>
    <code>
     float8
    </code>
   </td>
   <td>
    Porcentagem de espaço livre
   </td>
  </tr>
 </tbody>
</table>










Nos resultados acima, os números do espaço livre podem não corresponder exatamente ao `pgstattuple` porque o mapa do espaço livre nos dá um número exato, mas não é garantido que seja preciso até o byte.

### F.33.2. Autores [#](#PGSTATTUPLE-AUTHORS)

Tatsuo Ishii, Satoshi Nagayasu e Abhijit Menon-Sen
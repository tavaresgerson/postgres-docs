## F.25. pg_buffercache — inspecionar o estado do cache de buffer do PostgreSQL [#](#PGBUFFERCACHE)

* [F.25.1. A Visão do `pg_buffercache`](pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE)
* [F.25.2. A Visão do `pg_buffercache_numa`](pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE-NUMA)
* [F.25.3. A Função do `pg_buffercache_summary()`](pgbuffercache.md#PGBUFFERCACHE-SUMMARY)
* [F.25.4. A Função do `pg_buffercache_usage_counts()`](pgbuffercache.md#PGBUFFERCACHE-USAGE-COUNTS)
* [F.25.5. A Função do `pg_buffercache_evict()`](pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE-EVICT)
* [F.25.6. A Função do `pg_buffercache_evict_relation()`](pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE-EVICT-RELATION)
* [F.25.7. A Função do `pg_buffercache_evict_all()`](pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE-EVICT-ALL)
* [F.25.8. Saída de Amostra](pgbuffercache.md#PGBUFFERCACHE-SAMPLE-OUTPUT)
* [F.25.9. Autores](pgbuffercache.md#PGBUFFERCACHE-AUTHORS)

O módulo `pg_buffercache` fornece uma maneira de examinar o que está acontecendo no cache de buffer compartilhado em tempo real. Ele também oferece uma maneira de evocar dados de nível baixo, para fins de teste.

Este módulo fornece as funções `pg_buffercache_pages()` (envolvida na visualização `pg_buffercache`), as funções `pg_buffercache_numa_pages()` (envolvida na visualização `pg_buffercache_numa`), as funções `pg_buffercache_summary()` (envolvida na visualização `pg_buffercache_usage_counts()`), as funções `pg_buffercache_evict()` (envolvida na visualização `pg_buffercache_evict()`), as funções `pg_buffercache_evict_relation()` (envolvida na visualização `pg_buffercache_evict_relation()`), e as funções `pg_buffercache_evict_all()` (envolvida na visualização `pg_buffercache_evict_all()`).

A função `pg_buffercache_pages()` retorna um conjunto de registros, cada linha descrevendo o estado de uma entrada de buffer compartilhado. A vista `pg_buffercache` envolve a função para uso conveniente.

A função `pg_buffercache_numa_pages()` fornece mapeamentos de nós NUMA para entradas de buffer compartilhadas. Essa informação não faz parte do próprio `pg_buffercache_pages()`, pois é muito mais lenta para ser recuperada. A visão `pg_buffercache_numa` envolve a função para uso conveniente.

A função `pg_buffercache_summary()` retorna uma única linha que resume o estado do cache de buffer compartilhado.

A função `pg_buffercache_usage_counts()` retorna um conjunto de registros, cada linha descrevendo o número de buffers com um determinado número de uso.

Por padrão, o uso das funções acima é restrito a superusuários e papéis com privilégios do papel `pg_monitor`. O acesso pode ser concedido a outros usuários usando `GRANT`.

A função `pg_buffercache_evict()` permite que um bloco seja ejetado do pool de buffer, dado um identificador de buffer. O uso desta função é restrito apenas a superusuários.

A função `pg_buffercache_evict_relation()` permite que todos os buffers compartilhados não pinçados na relação sejam expulsos do pool de buffers, dado um identificador de relação. O uso desta função é restrito apenas a usuários super.

A função `pg_buffercache_evict_all()` permite que todos os buffers compartilhados não pinçados sejam expulsos no pool de buffers. O uso desta função é restrito apenas a superusuários.

### F.25.1. A `pg_buffercache` [#](#PGBUFFERCACHE-PG-BUFFERCACHE)

As definições das colunas expostas pela visualização são mostradas em [Tabela F.14](pgbuffercache.md#PGBUFFERCACHE-COLUMNS).

**Tabela F.14. Colunas `pg_buffercache`**



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
      bufferid
     </code>
     <code>
      integer
     </code>
    </p>
    <p>
     ID, na faixa de 1 a.
     <code>
      shared_buffers
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      relfilenode
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
      relfilenode
     </code>
     )
    </p>
    <p>
     Número de arquivo da relação
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      reltablespace
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-tablespace.md" title="52.56. pg_tablespace">
      <code>
       pg_tablespace
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     OID do tablespace da relação
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      reldatabase
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-database.md" title="52.15. pg_database">
      <code>
       pg_database
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     OID do banco de dados da relação
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      relforknumber
     </code>
     <code>
      smallint
     </code>
    </p>
    <p>
     Número de garfo dentro da relação; veja
     <code>
      common/relpath.h
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      relblocknumber
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número da página dentro da relação
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      isdirty
     </code>
     <code>
      boolean
     </code>
    </p>
    <p>
     A página está suja?
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      usagecount
     </code>
     <code>
      smallint
     </code>
    </p>
    <p>
     Contagem de acesso por varredura de relógio
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      pinning_backends
     </code>
     <code>
      integer
     </code>
    </p>
    <p>
     Número de backends que estão pressionando este buffer
    </p>
   </td>
  </tr>
 </tbody>
</table>










Há uma linha para cada buffer no cache compartilhado. Os buffers não utilizados são mostrados com todos os campos nulos, exceto `bufferid`. Os catálogos compartilhados do sistema são mostrados como pertencentes ao banco de dados zero.

Como o cache é compartilhado por todos os bancos de dados, normalmente haverá páginas de relações que não pertencem ao banco de dados atual. Isso significa que pode não haver linhas de junção correspondentes em `pg_class` para algumas linhas, ou que pode até haver junções incorretas. Se você está tentando fazer uma junção contra `pg_class`, é uma boa ideia restringir a junção às linhas que têm `reldatabase` igual ao OID do banco de dados atual ou zero.

Como os bloqueios do gerenciador de buffer não são tomados para copiar os dados do estado do buffer que a visualização exibirá, o acesso à visualização `pg_buffercache` tem menos impacto na atividade normal do buffer, mas não fornece um conjunto consistente de resultados em todos os buffers. No entanto, garantimos que as informações de cada buffer sejam consistentes.

### F.25.2. A `pg_buffercache_numa` [#](#PGBUFFERCACHE-PG-BUFFERCACHE-NUMA)

As definições das colunas expostas pela visualização são mostradas em [Tabela F.15](pgbuffercache.md#PGBUFFERCACHE-NUMA-COLUMNS).

**Tabela F.15. Colunas `pg_buffercache_numa`**



<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="catalog_table_entry">
    <p class="column_definition">
     Column Type
    </p>
    <p>
     Description
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      bufferid
     </code>
     <code>
      integer
     </code>
    </p>
    <p>
     ID, in the range 1..
     <code>
      shared_buffers
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      os_page_num
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     number of OS memory page for this buffer
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      numa_node
     </code>
     <code>
      int
     </code>
    </p>
    <p>
     ID of
     <acronym class="acronym">
      NUMA
     </acronym>
     node
    </p>
   </td>
  </tr>
 </tbody>
</table>










Como a consulta do ID do nó NUMA para cada página exige que as páginas de memória sejam paginadas, a primeira execução desta função pode levar um tempo notável. Em todos os casos (primeira execução ou não), a recuperação dessas informações é custosa e não é recomendada consultar a visão com alta frequência.

### Aviso

Ao determinar o nó NUMA, a visão toca todas as páginas de memória do segmento de memória compartilhada. Isso forçará a alocação da memória compartilhada, se não já tiver sido alocada, e a memória pode ser alocada em um único nó NUMA (dependendo da configuração do sistema).

### F.25.3. A função `pg_buffercache_summary()` [#](#PGBUFFERCACHE-SUMMARY)

As definições das colunas expostas pela função são mostradas em [Tabela F.16](pgbuffercache.md#PGBUFFERCACHE-SUMMARY-COLUMNS) Colunas de Saída").

**Tabela F.16. Colunas de Saída `pg_buffercache_summary()`**



<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="catalog_table_entry">
    <p class="column_definition">
     Column Type
    </p>
    <p>
     Description
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      buffers_used
     </code>
     <code>
      int4
     </code>
    </p>
    <p>
     Number of used shared buffers
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      buffers_unused
     </code>
     <code>
      int4
     </code>
    </p>
    <p>
     Number of unused shared buffers
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      buffers_dirty
     </code>
     <code>
      int4
     </code>
    </p>
    <p>
     Number of dirty shared buffers
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      buffers_pinned
     </code>
     <code>
      int4
     </code>
    </p>
    <p>
     Number of pinned shared buffers
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      usagecount_avg
     </code>
     <code>
      float8
     </code>
    </p>
    <p>
     Average usage count of used shared buffers
    </p>
   </td>
  </tr>
 </tbody>
</table>










A função `pg_buffercache_summary()` retorna uma única linha que resume o estado de todos os buffers compartilhados. Informações semelhantes e mais detalhadas são fornecidas pela visão `pg_buffercache`, mas a `pg_buffercache_summary()` é significativamente mais barata.

Assim como a visualização `pg_buffercache`, a `pg_buffercache_summary()` não adquire bloqueios do gerenciador de buffer. Portanto, a atividade concorrente pode levar a pequenas imprecisões no resultado.

### F.25.4. A função `pg_buffercache_usage_counts()` [#](#PGBUFFERCACHE-USAGE-COUNTS)

As definições das colunas expostas pela função são mostradas na [Tabela F.17] (Colunas de Saída).

**Tabela F.17. Colunas de Saída `pg_buffercache_usage_counts()`**



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
      usage_count
     </code>
     <code>
      int4
     </code>
    </p>
    <p>
     Um possível contagem de uso de buffer
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      buffers
     </code>
     <code>
      int4
     </code>
    </p>
    <p>
     Número de buffers com o número de uso
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      dirty
     </code>
     <code>
      int4
     </code>
    </p>
    <p>
     Número de buffers sujos com o número de uso
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      pinned
     </code>
     <code>
      int4
     </code>
    </p>
    <p>
     Número de buffers fixados com o número de uso
    </p>
   </td>
  </tr>
 </tbody>
</table>










A função `pg_buffercache_usage_counts()` retorna um conjunto de linhas que resumem os estados de todos os buffers compartilhados, agregados pelos possíveis valores de contagem de uso. Informações semelhantes e mais detalhadas são fornecidas pela visão `pg_buffercache`, mas a `pg_buffercache_usage_counts()` é significativamente mais barata.

Assim como a visão `pg_buffercache`, a `pg_buffercache_usage_counts()` não obtém bloqueios do gerenciador de buffer. Portanto, a atividade concorrente pode levar a pequenas imprecisões no resultado.

### F.25.5. A função `pg_buffercache_evict()` [#](#PGBUFFERCACHE-PG-BUFFERCACHE-EVICT)

A função `pg_buffercache_evict()` recebe um identificador de buffer, conforme mostrado na coluna `bufferid` da visualização `pg_buffercache`. Ela retorna informações sobre se o buffer foi ejetado e esvaziado. A coluna buffer_evicted é verdadeira em caso de sucesso, e falsa se o buffer não for válido, se não puder ser ejetado porque foi fixado, ou se se tornou sujo novamente após uma tentativa de escrevê-lo. A coluna buffer_flushed é verdadeira se o buffer foi esvaziado. Isso não significa necessariamente que o buffer foi esvaziado por nós, pois pode ser esvaziado por outra pessoa. O resultado fica imediatamente desatualizado ao retornar, pois o buffer pode se tornar válido novamente a qualquer momento devido à atividade concorrente. A função é destinada apenas para testes de desenvolvedores.

### F.25.6. A função `pg_buffercache_evict_relation()` [#](#PGBUFFERCACHE-PG-BUFFERCACHE-EVICT-RELATION)

A função `pg_buffercache_evict_relation()` é muito semelhante à função `pg_buffercache_evict()`. A diferença é que a `pg_buffercache_evict_relation()` recebe um identificador de relação em vez de um identificador de buffer. Ela tenta expulsar todos os buffers para todas as divisões nessa relação. Ela retorna o número de buffers expulsos, buffers esvaziados e o número de buffers que não puderam ser expulsos. Os buffers esvaziados não necessariamente foram esvaziados por nós, eles podem ter sido esvaziados por outra pessoa. O resultado fica imediatamente desatualizado após o retorno, pois os buffers podem ser imediatamente lidos novamente devido a atividades concorrentes. A função é destinada apenas para testes de desenvolvedores.

### F.25.7. A função `pg_buffercache_evict_all()` [#](#PGBUFFERCACHE-PG-BUFFERCACHE-EVICT-ALL)

A função `pg_buffercache_evict_all()` é muito semelhante à função `pg_buffercache_evict()`. A diferença é que a função `pg_buffercache_evict_all()` não recebe um argumento; em vez disso, tenta remover todos os buffers do pool de buffers. Ela retorna o número de buffers removidos, buffers esvaziados e o número de buffers que não puderam ser removidos. Os buffers esvaziados não foram necessariamente esvaziados por nós, eles podem ter sido esvaziados por outra pessoa. O resultado fica imediatamente desatualizado após o retorno, pois os buffers podem ser imediatamente lidos novamente devido a atividades concorrentes. A função é destinada apenas para testes de desenvolvedores.

### F.25.8. Saída de amostra [#](#PGBUFFERCACHE-SAMPLE-OUTPUT)

```
regression=# SELECT n.nspname, c.relname, count(*) AS buffers
             FROM pg_buffercache b JOIN pg_class c
             ON b.relfilenode = pg_relation_filenode(c.oid) AND
                b.reldatabase IN (0, (SELECT oid FROM pg_database
                                      WHERE datname = current_database()))
             JOIN pg_namespace n ON n.oid = c.relnamespace
             GROUP BY n.nspname, c.relname
             ORDER BY 3 DESC
             LIMIT 10;

  nspname   |        relname         | buffers
------------+------------------------+---------
 public     | delete_test_table      |     593
 public     | delete_test_table_pkey |     494
 pg_catalog | pg_attribute           |     472
 public     | quad_poly_tbl          |     353
 public     | tenk2                  |     349
 public     | tenk1                  |     349
 public     | gin_test_idx           |     306
 pg_catalog | pg_largeobject         |     206
 public     | gin_test_tbl           |     188
 public     | spgist_text_tbl        |     182
(10 rows)


regression=# SELECT * FROM pg_buffercache_summary();
 buffers_used | buffers_unused | buffers_dirty | buffers_pinned | usagecount_avg
--------------+----------------+---------------+----------------+----------------
          248 |        2096904 |            39 |              0 |       3.141129
(1 row)


regression=# SELECT * FROM pg_buffercache_usage_counts();
 usage_count | buffers | dirty | pinned
-------------+---------+-------+--------
           0 |   14650 |     0 |      0
           1 |    1436 |   671 |      0
           2 |     102 |    88 |      0
           3 |      23 |    21 |      0
           4 |       9 |     7 |      0
           5 |     164 |   106 |      0
(6 rows)
```

### F.25.9. Autores [#](#PGBUFFERCACHE-AUTHORS)

Mark Kirkwood `<markir@paradise.net.nz>`

Sugestões de design: Neil Conway `<neilc@samurai.com>`

Dicas de depuração: Tom Lane `<tgl@sss.pgh.pa.us>`
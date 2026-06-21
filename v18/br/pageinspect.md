## F.23. pageinspect — inspeção de nível baixo de páginas de banco de dados [#](#PAGEINSPECT)

* [F.23.1. Funções Gerais](pageinspect.md#PAGEINSPECT-GENERAL-FUNCS)
* [F.23.2. Funções de Pilha](pageinspect.md#PAGEINSPECT-HEAP-FUNCS)
* [F.23.3. Funções de Árvores B](pageinspect.md#PAGEINSPECT-B-TREE-FUNCS)
* [F.23.4. Funções BRIN](pageinspect.md#PAGEINSPECT-BRIN-FUNCS)
* [F.23.5. Funções GIN](pageinspect.md#PAGEINSPECT-GIN-FUNCS)
* [F.23.6. Funções GiST](pageinspect.md#PAGEINSPECT-GIST-FUNCS)
* [F.23.7. Funções Hash](pageinspect.md#PAGEINSPECT-HASH-FUNCS)

O módulo `pageinspect` fornece funções que permitem inspecionar o conteúdo das páginas do banco de dados em um nível baixo, o que é útil para fins de depuração. Todas essas funções podem ser usadas apenas por superusuários.

### F.23.1. Funções Gerais [#](#PAGEINSPECT-GENERAL-FUNCS)

`get_raw_page(relname text, fork text, blkno bigint) returns bytea`: `get_raw_page` lê o bloco especificado da relação designada e retorna uma cópia como um valor de `bytea`. Isso permite obter uma cópia consistente em relação ao tempo do bloco. *`fork`* deve ser `'main'` para o principal ramo de dados, `'fsm'` para o [mapa de espaço livre](storage-fsm.md "66.3. Free Space Map"), `'vm'` para o [mapa de visibilidade](storage-vm.md "66.4. Visibility Map"), ou `'init'` para o ramo de inicialização.

`get_raw_page(relname text, blkno bigint) returns bytea`: Uma versão abreviada de `get_raw_page`, para leitura a partir do ramo principal. É equivalente a `get_raw_page(relname, 'main', blkno)`

`page_header(page bytea) returns record`: `page_header` mostra campos que são comuns a todas as páginas de heap e índices do PostgreSQL.

Uma imagem da página obtida com `get_raw_page` deve ser passada como argumento. Por exemplo:

``` test=# SELECT * FROM page_header(get_raw_page('pg_class', 0)); lsn    | checksum | flags  | lower | upper | special | pagesize | version | prune_xid -----------+----------+--------+-------+-------+---------+----------+---------+----------- 0/24A1B50 |        0 |      1 |   232 |   368 |    8192 |     8192 |       4 |         0
    ```

As colunas devolvidas correspondem aos campos da estrutura `PageHeaderData`. Consulte `src/include/storage/bufpage.h` para obter detalhes.

O campo `checksum` é o checksum armazenado na página, que pode estar incorreto se a página estiver de alguma forma corrompida. Se os checksums de dados forem desativados para esta instância, o valor armazenado não terá significado.

`page_checksum(page bytea, blkno bigint) returns smallint`: `page_checksum` calcula o checksum da página, como se ela estivesse localizada no bloco dado.

Uma imagem da página obtida com `get_raw_page` deve ser passada como argumento. Por exemplo:

``` test=# SELECT page_checksum(get_raw_page('pg_class', 0), 0); page_checksum --------------- 13443
    ```

Observe que o checksum depende do número do bloco, então números de bloco correspondentes devem ser passados (exceto quando se está fazendo depuração esotérica).

O checksum calculado com essa função pode ser comparado com o campo de resultado `checksum` da função `page_header`. Se os checksums de dados estiverem habilitados para essa instância, então os dois valores devem ser iguais.

`fsm_page_contents(page bytea) returns text`
:   `fsm_page_contents` mostra a estrutura de nó interno de uma página FSM. Por exemplo:

    ```
    test=# SELECT fsm_page_contents(get_raw_page('pg_class', 'fsm', 0));
    ```

A saída é uma string de várias linhas, com uma linha por nó na árvore binária dentro da página. Apenas os nós que não são zero são impressos. O chamado ponteiro "próximo", que aponta para o próximo espaço a ser retornado da página, também é impresso.

Veja `src/backend/storage/freespace/README` para mais informações sobre a estrutura de uma página do FSM.

### F.23.2. Funções de pilha [#](#PAGEINSPECT-HEAP-FUNCS)

`heap_page_items(page bytea) returns setof record`
:   `heap_page_items` mostra todos os ponteiros de linha em uma página de heap. Para esses ponteiros de linha que estão em uso, os cabeçalhos dos tuplos, bem como os dados brutos dos tuplos, também são mostrados. Todos os tuplos são mostrados, independentemente de os tuplos terem sido visíveis a um instantâneo MVCC no momento em que a página bruta foi copiada.

Uma imagem de página pilha obtida com `get_raw_page` deve ser passada como argumento. Por exemplo:

    ```
    test=# SELECT * FROM heap_page_items(get_raw_page('pg_class', 0));
    ```

Veja `src/include/storage/itemid.h` e `src/include/access/htup_details.h` para explicações dos campos retornados.

A função `heap_tuple_infomask_flags` pode ser usada para desempacotar os bits de sinalização de `t_infomask` e `t_infomask2` para tuplas de heap.

`tuple_data_split(rel_oid oid, t_data bytea, t_infomask integer, t_infomask2 integer, t_bits text [, do_detoast bool]) returns bytea[]`
:   `tuple_data_split` divide os dados do tuple em atributos
    da mesma forma que os recursos internos do backend.

    ```
    test=# SELECT tuple_data_split('pg_class'::regclass, t_data, t_infomask, t_infomask2, t_bits) FROM heap_page_items(get_raw_page('pg_class', 0));
    ```

Essa função deve ser chamada com os mesmos argumentos que os atributos de retorno de `heap_page_items`.

Se *`do_detoast`* for `true`, os atributos serão desnecessários. O valor padrão é
`false`.

`heap_page_item_attrs(page bytea, rel_oid regclass [, do_detoast bool]) returns setof record`  :  `heap_page_item_attrs` é equivalente a
    `heap_page_items` exceto que ele retorna
    dados brutos em tupla como um array de atributos que podem, opcionalmente,
    ser deserializados por *`do_detoast`* que é
    `false` por padrão.

Uma imagem de página pilha obtida com `get_raw_page` deve ser passada como argumento. Por exemplo:

    ```
    test=# SELECT * FROM heap_page_item_attrs(get_raw_page('pg_class', 0), 'pg_class'::regclass);
    ```

`heap_tuple_infomask_flags(t_infomask integer, t_infomask2 integer) returns record` decodifica os
    `heap_tuple_infomask_flags` e
    `t_infomask` retornados por
    `heap_page_items` em um conjunto de matrizes legível por humanos, composto por nomes de bandeiras, com uma coluna para todas as bandeiras e uma coluna para bandeiras combinadas. Por exemplo:

    ```
    test=# SELECT t_ctid, raw_flags, combined_flags FROM heap_page_items(get_raw_page('pg_class', 0)), LATERAL heap_tuple_infomask_flags(t_infomask, t_infomask2) WHERE t_infomask IS NOT NULL OR t_infomask2 IS NOT NULL;
    ```

Essa função deve ser chamada com os mesmos argumentos que os atributos de retorno de `heap_page_items`.

As bandeiras combinadas são exibidas para macros de nível de fonte que levam em conta o valor de mais de um bit bruto, como `HEAP_XMIN_FROZEN`.

Veja `src/include/access/htup_details.h` para explicações sobre os nomes das bandeiras retornadas.

### F.23.3. Funções de Árvores B [#](#PAGEINSPECT-B-TREE-FUNCS)

`bt_metap(relname text) returns record`
:   `bt_metap` retorna informações sobre a metapágina de um índice de árvore B. Por exemplo:

    ```
    test=# SELECT * FROM bt_metap('pg_cast_oid_index'); -[ RECORD 1 ]-------------+------- magic                     | 340322 version                   | 4 root                      | 1 level                     | 0 fastroot                  | 1 fastlevel                 | 0 last_cleanup_num_delpages | 0 last_cleanup_num_tuples   | 230 allequalimage             | f
    ```

`bt_page_stats(relname text, blkno bigint) returns record`
:   `bt_page_stats` retorna informações resumidas sobre
    uma página de dados de um índice de árvore B. Por exemplo:

    ```
    test=# SELECT * FROM bt_page_stats('pg_cast_oid_index', 1); -[ RECORD 1 ]-+----- blkno         | 1 type          | l live_items    | 224 dead_items    | 0 avg_item_size | 16 page_size     | 8192 free_size     | 3668 btpo_prev     | 0 btpo_next     | 0 btpo_level    | 0 btpo_flags    | 3
    ```

`bt_multi_page_stats(relname text, blkno bigint, blk_count bigint) returns setof record`
:   `bt_multi_page_stats` retorna as mesmas informações
    que `bt_page_stats`, mas faz isso para cada página do
    intervalo de páginas que começa em *`blkno`* e
    se estende para *`blk_count`* páginas.
    Se *`blk_count`* é negativo, todas as páginas
    de *`blkno`* até o final do índice são relatadas. Por
    exemplo:

    ```
    test=# SELECT * FROM bt_multi_page_stats('pg_proc_oid_index', 5, 2); -[ RECORD 1 ]-+----- blkno         | 5 type          | l live_items    | 367 dead_items    | 0 avg_item_size | 16 page_size     | 8192 free_size     | 808 btpo_prev     | 4 btpo_next     | 6 btpo_level    | 0 btpo_flags    | 1 -[ RECORD 2 ]-+----- blkno         | 6 type          | l live_items    | 367 dead_items    | 0 avg_item_size | 16 page_size     | 8192 free_size     | 808 btpo_prev     | 5 btpo_next     | 7 btpo_level    | 0 btpo_flags    | 1
    ```

`bt_page_items(relname text, blkno bigint) returns setof record` : `bt_page_items` retorna informações detalhadas sobre todos os itens em uma página de índice de árvore B. Por exemplo:

    ```
    test=# SELECT itemoffset, ctid, itemlen, nulls, vars, data, dead, htid, tids[0:2] AS some_tids FROM bt_page_items('tenk2_hundred', 5); itemoffset |   ctid    | itemlen | nulls | vars |          data           | dead |  htid  |      some_tids ------------+-----------+---------+-------+------+-------------------------+------+--------+--------------------- 1 | (16,1)    |      16 | f     | f    | 30 00 00 00 00 00 00 00 |      |        | 2 | (16,8292) |     616 | f     | f    | 24 00 00 00 00 00 00 00 | f    | (1,6)  | {"(1,6)","(10,22)"} 3 | (16,8292) |     616 | f     | f    | 25 00 00 00 00 00 00 00 | f    | (1,18) | {"(1,18)","(4,22)"} 4 | (16,8292) |     616 | f     | f    | 26 00 00 00 00 00 00 00 | f    | (4,18) | {"(4,18)","(6,17)"} 5 | (16,8292) |     616 | f     | f    | 27 00 00 00 00 00 00 00 | f    | (1,2)  | {"(1,2)","(1,19)"} 6 | (16,8292) |     616 | f     | f    | 28 00 00 00 00 00 00 00 | f    | (2,24) | {"(2,24)","(4,11)"} 7 | (16,8292) |     616 | f     | f    | 29 00 00 00 00 00 00 00 | f    | (2,17) | {"(2,17)","(11,2)"} 8 | (16,8292) |     616 | f     | f    | 2a 00 00 00 00 00 00 00 | f    | (0,25) | {"(0,25)","(3,20)"} 9 | (16,8292) |     616 | f     | f    | 2b 00 00 00 00 00 00 00 | f    | (0,10) | {"(0,10)","(0,14)"} 10 | (16,8292) |     616 | f     | f    | 2c 00 00 00 00 00 00 00 | f    | (1,3)  | {"(1,3)","(3,9)"} 11 | (16,8292) |     616 | f     | f    | 2d 00 00 00 00 00 00 00 | f    | (6,28) | {"(6,28)","(11,1)"} 12 | (16,8292) |     616 | f     | f    | 2e 00 00 00 00 00 00 00 | f    | (0,27) | {"(0,27)","(1,13)"} 13 | (16,8292) |     616 | f     | f    | 2f 00 00 00 00 00 00 00 | f    | (4,17) | {"(4,17)","(4,21)"} (13 rows)
    ```

Esta é uma página de folha de árvore B. Todos os tuplos que apontam para a tabela
acontecem ser tuplos da lista de postagem (todos eles armazenam um total de
100 TIDs de 6 bytes). Há também um tuplo de "chave alta" em `itemoffset` número 1.
`ctid` é usado para armazenar informações codificadas sobre cada tuplo
neste exemplo, embora as páginas de folha geralmente armazenem um TID de pilha diretamente
no campo `ctid`.
`tids` é a lista de TIDs armazenada como uma lista de postagem.

Em uma página interna (não mostrada), a parte do número de bloco de
`ctid` é um "downlink",
que é um número de bloco de outra página no próprio índice.
A parte de deslocamento (o segundo número) de
`ctid` armazena informações codificadas sobre o tuplo, como o número de colunas presentes (a troncamento do sufixo pode ter removido colunas de sufixo desnecessárias). Colunas truncadas são tratadas como tendo o valor "menos infinito".

`htid` mostra um TID de pilha para o tuplo,
    independentemente da representação subjacente do tuplo. Esse valor
    pode corresponder a `ctid`, ou pode ser decodificado
    das representações alternativas usadas por tuplos de listas de postagem
    e tuplos de páginas internas. Os tuplos em páginas internas
    geralmente têm a coluna de nível de implementação TID truncada
    e representada como um valor NULL
    `htid`.

Observe que o primeiro item de qualquer página que não seja a mais à direita (qualquer página com um valor não nulo no campo `btpo_next`) é o "chave alta" da página, ou seja, seu `data` serve como um limite superior para todos os itens que aparecem na página, enquanto seu campo `ctid` não aponta para outro bloco. Além disso, em páginas internas, o primeiro item de dados reais (o primeiro item que não é uma chave alta) tem, de forma confiável, todas as colunas truncadas, não deixando nenhum valor real em seu campo `data`. Esse item, no entanto, tem um downlink válido em seu campo `ctid`.

Para mais detalhes sobre a estrutura dos índices de árvore B, consulte [Seção 65.1.4.1][(btree.md#BTREE-STRUCTURE "65.1.4.1. B-Tree Structure")]. Para mais detalhes sobre a eliminação de duplicatas e listas de publicação, consulte [Seção 65.1.4.3][(btree.md#BTREE-DEDUPLICATION "65.1.4.3. Deduplication")].

`bt_page_items(page bytea) returns setof record` É também possível passar uma página para `bt_page_items` como um valor de `bytea`. Uma imagem de página obtida com `get_raw_page` deve ser passada como argumento. Assim, o último exemplo também pode ser reescrito da seguinte forma:

    ```
    test=# SELECT itemoffset, ctid, itemlen, nulls, vars, data, dead, htid, tids[0:2] AS some_tids FROM bt_page_items(get_raw_page('tenk2_hundred', 5)); itemoffset |   ctid    | itemlen | nulls | vars |          data           | dead |  htid  |      some_tids ------------+-----------+---------+-------+------+-------------------------+------+--------+--------------------- 1 | (16,1)    |      16 | f     | f    | 30 00 00 00 00 00 00 00 |      |        | 2 | (16,8292) |     616 | f     | f    | 24 00 00 00 00 00 00 00 | f    | (1,6)  | {"(1,6)","(10,22)"} 3 | (16,8292) |     616 | f     | f    | 25 00 00 00 00 00 00 00 | f    | (1,18) | {"(1,18)","(4,22)"} 4 | (16,8292) |     616 | f     | f    | 26 00 00 00 00 00 00 00 | f    | (4,18) | {"(4,18)","(6,17)"} 5 | (16,8292) |     616 | f     | f    | 27 00 00 00 00 00 00 00 | f    | (1,2)  | {"(1,2)","(1,19)"} 6 | (16,8292) |     616 | f     | f    | 28 00 00 00 00 00 00 00 | f    | (2,24) | {"(2,24)","(4,11)"} 7 | (16,8292) |     616 | f     | f    | 29 00 00 00 00 00 00 00 | f    | (2,17) | {"(2,17)","(11,2)"} 8 | (16,8292) |     616 | f     | f    | 2a 00 00 00 00 00 00 00 | f    | (0,25) | {"(0,25)","(3,20)"} 9 | (16,8292) |     616 | f     | f    | 2b 00 00 00 00 00 00 00 | f    | (0,10) | {"(0,10)","(0,14)"} 10 | (16,8292) |     616 | f     | f    | 2c 00 00 00 00 00 00 00 | f    | (1,3)  | {"(1,3)","(3,9)"} 11 | (16,8292) |     616 | f     | f    | 2d 00 00 00 00 00 00 00 | f    | (6,28) | {"(6,28)","(11,1)"} 12 | (16,8292) |     616 | f     | f    | 2e 00 00 00 00 00 00 00 | f    | (0,27) | {"(0,27)","(1,13)"} 13 | (16,8292) |     616 | f     | f    | 2f 00 00 00 00 00 00 00 | f    | (4,17) | {"(4,17)","(4,21)"} (13 rows)
    ```

Todos os outros detalhes são os mesmos, conforme explicado no item anterior.

### F.23.4. Funções do BRIN [#](#PAGEINSPECT-BRIN-FUNCS)

`brin_page_type(page bytea) returns text`   :   `brin_page_type` retorna o tipo de página do índice BRIN fornecido. Caso a página não seja uma página válida BRIN, o programa lança um erro. Por exemplo:

    ```
    test=# SELECT brin_page_type(get_raw_page('brinidx', 0)); brin_page_type ---------------- meta
    ```

`brin_metapage_info(page bytea) returns record` `brin_metapage_info` retorna informações variadas sobre uma metapágina do índice BRIN. Por exemplo:

    ```
    test=# SELECT * FROM brin_metapage_info(get_raw_page('brinidx', 0)); magic    | version | pagesperrange | lastrevmappage ------------+---------+---------------+---------------- 0xA8109CFA |       1 |             4 |              2
    ```

`brin_revmap_data(page bytea) returns setof tid` `brin_revmap_data` retorna a lista de identificadores de tupla em uma página de mapa de intervalo de índice BRIN. Por exemplo:

    ```
    test=# SELECT * FROM brin_revmap_data(get_raw_page('brinidx', 2)) LIMIT 5; pages --------- (6,137) (6,138) (6,139) (6,140) (6,141)
    ```

`brin_page_items(page bytea, index oid) returns setof record` `brin_page_items` retorna os dados armazenados na página de dados BRIN. Por exemplo:

    ```
    test=# SELECT * FROM brin_page_items(get_raw_page('brinidx', 5), 'brinidx') ORDER BY blknum, attnum LIMIT 6; itemoffset | blknum | attnum | allnulls | hasnulls | placeholder | empty |    value ------------+--------+--------+----------+----------+-------------+-------+-------------- 137 |      0 |      1 | t        | f        | f           | f     | 137 |      0 |      2 | f        | f        | f           | f     | {1 .. 88} 138 |      4 |      1 | t        | f        | f           | f     | 138 |      4 |      2 | f        | f        | f           | f     | {89 .. 176} 139 |      8 |      1 | t        | f        | f           | f     | 139 |      8 |      2 | f        | f        | f           | f     | {177 .. 264}
    ```

As colunas devolvidas correspondem aos campos das estruturas `BrinMemTuple` e `BrinValues`. Consulte `src/include/access/brin_tuple.h` para detalhes.

### F.23.5. Funções GIN [#](#PAGEINSPECT-GIN-FUNCS)

`gin_metapage_info(page bytea) returns record` `gin_metapage_info` retorna informações sobre
    uma metapágina do índice GIN. Por exemplo:

    ```
    test=# SELECT * FROM gin_metapage_info(get_raw_page('gin_index', 0)); -[ RECORD 1 ]----+----------- pending_head     | 4294967295 pending_tail     | 4294967295 tail_free_size   | 0 n_pending_pages  | 0 n_pending_tuples | 0 n_total_pages    | 7 n_entry_pages    | 6 n_data_pages     | 0 n_entries        | 693 version          | 2
    ```

`gin_page_opaque_info(page bytea) returns record` `gin_page_opaque_info` retorna informações sobre uma área oclusa do índice GIN, como o tipo de página. Por exemplo:

    ```
    test=# SELECT * FROM gin_page_opaque_info(get_raw_page('gin_index', 2)); rightlink | maxoff |         flags -----------+--------+------------------------ 5 |      0 | {data,leaf,compressed} (1 row)
    ```

`gin_leafpage_items(page bytea) returns setof record` :   `gin_leafpage_items` retorna informações sobre os dados armazenados em uma página de folha GIN comprimida. Por exemplo:

    ```
    test=# SELECT first_tid, nbytes, tids[0:5] AS some_tids FROM gin_leafpage_items(get_raw_page('gin_test_idx', 2)); first_tid | nbytes |                        some_tids -----------+--------+---------------------------------------------------------- (8,41)    |    244 | {"(8,41)","(8,43)","(8,44)","(8,45)","(8,46)"} (10,45)   |    248 | {"(10,45)","(10,46)","(10,47)","(10,48)","(10,49)"} (12,52)   |    248 | {"(12,52)","(12,53)","(12,54)","(12,55)","(12,56)"} (14,59)   |    320 | {"(14,59)","(14,60)","(14,61)","(14,62)","(14,63)"} (167,16)  |    376 | {"(167,16)","(167,17)","(167,18)","(167,19)","(167,20)"} (170,30)  |    376 | {"(170,30)","(170,31)","(170,32)","(170,33)","(170,34)"} (173,44)  |    197 | {"(173,44)","(173,45)","(173,46)","(173,47)","(173,48)"} (7 rows)
    ```

### F.23.6. Funções GiST [#](#PAGEINSPECT-GIST-FUNCS)

`gist_page_opaque_info(page bytea) returns record` `gist_page_opaque_info` retorna informações da área opaca da página de índice GiST, como NSN, rightlink e tipo de página. Por exemplo:

    ```
    test=# SELECT * FROM gist_page_opaque_info(get_raw_page('test_gist_idx', 2)); lsn | nsn | rightlink | flags -----+-----+-----------+-------- 0/1 | 0/0 |         1 | {leaf} (1 row)
    ```

`gist_page_items(page bytea, index_oid regclass) returns setof record`
:   `gist_page_items` retorna informações sobre os dados armazenados em uma página de um índice GiST. Por exemplo:

    ```
    test=# SELECT * FROM gist_page_items(get_raw_page('test_gist_idx', 0), 'test_gist_idx'); itemoffset |   ctid    | itemlen | dead |             keys ------------+-----------+---------+------+------------------------------- 1 | (1,65535) |      40 | f    | (p)=("(185,185),(1,1)") 2 | (2,65535) |      40 | f    | (p)=("(370,370),(186,186)") 3 | (3,65535) |      40 | f    | (p)=("(555,555),(371,371)") 4 | (4,65535) |      40 | f    | (p)=("(740,740),(556,556)") 5 | (5,65535) |      40 | f    | (p)=("(870,870),(741,741)") 6 | (6,65535) |      40 | f    | (p)=("(1000,1000),(871,871)") (6 rows)
    ```

`gist_page_items_bytea(page bytea) returns setof record`
:   O mesmo que `gist_page_items`, mas retorna os dados chave
    como um blob bruto `bytea`. Como ele não tenta decodificar
    a chave, ele não precisa saber qual índice está envolvido. Por
    exemplo:

    ```
    test=# SELECT * FROM gist_page_items_bytea(get_raw_page('test_gist_idx', 0)); itemoffset |   ctid    | itemlen | dead |                                      key_data ------------+-----------+---------+------+-----------------------------------------​------------------------------------------- 1 | (1,65535) |      40 | f    | \x00000100ffff28000000000000c0644000000000​00c06440000000000000f03f000000000000f03f 2 | (2,65535) |      40 | f    | \x00000200ffff28000000000000c0744000000000​00c074400000000000e064400000000000e06440 3 | (3,65535) |      40 | f    | \x00000300ffff28000000000000207f4000000000​00207f400000000000d074400000000000d07440 4 | (4,65535) |      40 | f    | \x00000400ffff28000000000000c0844000000000​00c084400000000000307f400000000000307f40 5 | (5,65535) |      40 | f    | \x00000500ffff28000000000000f0894000000000​00f089400000000000c884400000000000c88440 6 | (6,65535) |      40 | f    | \x00000600ffff28000000000000208f4000000000​00208f400000000000f889400000000000f88940 7 | (7,65535) |      40 | f    | \x00000700ffff28000000000000408f4000000000​00408f400000000000288f400000000000288f40 (7 rows)
    ```

### F.23.7. Funções de Hash [#](#PAGEINSPECT-HASH-FUNCS)

`hash_page_type(page bytea) returns text` `hash_page_type` retorna o tipo de página do índice HASH fornecido. Por exemplo:

    ```
    test=# SELECT hash_page_type(get_raw_page('con_hash_index', 0)); hash_page_type ---------------- metapage
    ```

`hash_page_stats(page bytea) returns setof record` `hash_page_stats` retorna informações sobre
    um cache ou página de sobreposição de um índice HASH.
    Por exemplo:

    ```
    test=# SELECT * FROM hash_page_stats(get_raw_page('con_hash_index', 1)); -[ RECORD 1 ]---+----------- live_items      | 407 dead_items      | 0 page_size       | 8192 free_size       | 8 hasho_prevblkno | 4096 hasho_nextblkno | 8474 hasho_bucket    | 0 hasho_flag      | 66 hasho_page_id   | 65408
    ```

`hash_page_items(page bytea) returns setof record` `hash_page_items` retorna informações sobre os dados armazenados em um bucket ou página de overflow de uma página de índice HASH. Por exemplo:

    ```
    test=# SELECT * FROM hash_page_items(get_raw_page('con_hash_index', 1)) LIMIT 5; itemoffset |   ctid    |    data ------------+-----------+------------ 1 | (899,77)  | 1053474816 2 | (897,29)  | 1053474816 3 | (894,207) | 1053474816 4 | (892,159) | 1053474816 5 | (890,111) | 1053474816
    ```

`hash_bitmap_info(index oid, blkno bigint) returns record` :   `hash_bitmap_info` mostra o status de um bit
    na página de mapa de bits para uma página específica de sobreposição do
    HASH index. Por exemplo:

    ```
    test=# SELECT * FROM hash_bitmap_info('con_hash_index', 2052); bitmapblkno | bitmapbit | bitstatus -------------+-----------+----------- 65 |         3 | t
    ```

`hash_metapage_info(page bytea) returns record` `hash_metapage_info` retorna informações armazenadas na página meta de um índice HASH. Por exemplo:

    ```
    test=# SELECT magic, version, ntuples, ffactor, bsize, bmsize, bmshift, test-#     maxbucket, highmask, lowmask, ovflpoint, firstfree, nmaps, procid, test-#     regexp_replace(spares::text, '(,0)*}', '}') as spares, test-#     regexp_replace(mapp::text, '(,0)*}', '}') as mapp test-# FROM hash_metapage_info(get_raw_page('con_hash_index', 0)); -[ RECORD 1 ]-------------------------------------------------​------------------------------ magic     | 105121344 version   | 4 ntuples   | 500500 ffactor   | 40 bsize     | 8152 bmsize    | 4096 bmshift   | 15 maxbucket | 12512 highmask  | 16383 lowmask   | 8191 ovflpoint | 28 firstfree | 1204 nmaps     | 1 procid    | 450 spares    | {0,0,0,0,0,0,1,1,1,1,1,1,1,1,3,4,4,4,45,55,58,59,​508,567,628,704,1193,1202,1204} mapp      | {65}
    ```

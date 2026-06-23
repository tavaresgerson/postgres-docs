## F.27. pg_freespacemap — examinar o mapa de espaço livre [#](#PGFREESPACEMAP)

* [F.27.1. Funções](pgfreespacemap.md#PGFREESPACEMAP-FUNCS)
* [F.27.2. Saída de amostra](pgfreespacemap.md#PGFREESPACEMAP-SAMPLE-OUTPUT)
* [F.27.3. Autor](pgfreespacemap.md#PGFREESPACEMAP-AUTHOR)

O módulo `pg_freespacemap` fornece uma maneira de examinar o mapa de espaço livre (storage-fsm.md "66.3. Free Space Map") (FSM). Ele fornece uma função chamada `pg_freespace`, ou duas funções sobrecarregadas, para ser preciso. As funções mostram o valor registrado no mapa de espaço livre para uma página específica, ou para todas as páginas na relação.

Por padrão, o uso é restrito a superusuários e papéis com privilégios da função `pg_stat_scan_tables`. O acesso pode ser concedido a outros usuários usando `GRANT`.

### F.27.1. Funções [#](#PGFREESPACEMAP-FUNCS)

`pg_freespace(rel regclass IN, blkno bigint IN) returns int2`: Retorna o volume de espaço livre na página da relação, especificado por `blkno`, de acordo com o FSM.

`pg_freespace(rel regclass IN, blkno OUT bigint, avail OUT int2)`: Exibe a quantidade de espaço livre em cada página da relação, de acordo com o FSM. Um conjunto de tuplas `(blkno bigint, avail int2)` é retornado, uma tupla para cada página na relação.

Os valores armazenados no mapa de espaço livre não são exatos. Eles são arredondados para precisão de 1/256 da `BLCKSZ` (32 bytes com `BLCKSZ` padrão), e não são mantidos totalmente atualizados à medida que tuplas são inseridas e atualizadas.

Para índices, o que é rastreado são páginas totalmente não utilizadas, e não o espaço livre dentro das páginas. Portanto, os valores não têm significado, apenas se uma página está em uso ou vazia.

### F.27.2. Saída de amostra [#](#PGFREESPACEMAP-SAMPLE-OUTPUT)

```
postgres=# SELECT * FROM pg_freespace('foo');
 blkno | avail
-------+-------
     0 |     0
     1 |     0
     2 |     0
     3 |    32
     4 |   704
     5 |   704
     6 |   704
     7 |  1216
     8 |   704
     9 |   704
    10 |   704
    11 |   704
    12 |   704
    13 |   704
    14 |   704
    15 |   704
    16 |   704
    17 |   704
    18 |   704
    19 |  3648
(20 rows)

postgres=# SELECT * FROM pg_freespace('foo', 7);
 pg_freespace
--------------
         1216
(1 row)
```

### F.27.3. Autor [#](#PGFREESPACEMAP-AUTHOR)

Versão original de Mark Kirkwood `<markir@paradise.net.nz>`. Reescrita na versão 8.4 para se adequar à nova implementação do FSM por Heikki Linnakangas `<heikki@enterprisedb.com>`
## F.36. pg_visibility — informações e utilitários do mapa de visibilidade [#](#PGVISIBILITY)

* [F.36.1. Funções](pgvisibility.md#PGVISIBILITY-FUNCS)
* [F.36.2. Autor](pgvisibility.md#PGVISIBILITY-AUTHOR)

O módulo `pg_visibility` fornece uma maneira de examinar o mapa de visibilidade (VM) e as informações de visibilidade de nível de página de uma tabela. Ele também fornece funções para verificar a integridade de um mapa de visibilidade e para forçar a sua reconstrução.

Três bits diferentes são usados para armazenar informações sobre a visibilidade em nível de página. O bit totalmente visível no mapa de visibilidade indica que cada tupla na página correspondente da relação é visível para todas as transações atuais e futuras. O bit totalmente congelado no mapa de visibilidade indica que cada tupla na página está congelada; ou seja, nenhuma futura varredura precisará modificar a página até que uma tupla seja inserida, atualizada, excluída ou bloqueada naquela página. O bit `PD_ALL_VISIBLE` do cabeçalho da página tem o mesmo significado que o bit totalmente visível no mapa de visibilidade, mas é armazenado dentro da própria página de dados, em vez de em uma estrutura de dados separada. Esses dois bits normalmente concordam, mas o bit totalmente visível da página às vezes pode ser definido enquanto o bit do mapa de visibilidade está claro após uma recuperação de falha. Os valores relatados também podem discordar devido a uma mudança que ocorre após o `pg_visibility` examinar o mapa de visibilidade e antes de examinar a página de dados. Qualquer evento que cause corrupção de dados também pode fazer com que esses bits discordem.

As funções que exibem informações sobre os bits `PD_ALL_VISIBLE` são muito mais caras do que aquelas que apenas consultam o mapa de visibilidade, porque elas devem ler os blocos de dados da relação em vez de apenas o (muito menor) mapa de visibilidade. As funções que verificam os blocos de dados da relação são igualmente caras.

### F.36.1. Funções [#](#PGVISIBILITY-FUNCS)

`pg_visibility_map(relation regclass, blkno bigint, all_visible OUT boolean, all_frozen OUT boolean) returns record`: Retorna todos os bits visíveis e todos os bits congelados no mapa de visibilidade para o bloco dado da relação dada.

`pg_visibility(relation regclass, blkno bigint, all_visible OUT boolean, all_frozen OUT boolean, pd_all_visible OUT boolean) returns record`: Retorna todos os bits visíveis e todos os bits congelados no mapa de visibilidade para o bloco dado da relação dada, além do bit `PD_ALL_VISIBLE` desse bloco.

`pg_visibility_map(relation regclass, blkno OUT bigint, all_visible OUT boolean, all_frozen OUT boolean) returns setof record`: Retorna todos os bits visíveis e congelados no mapa de visibilidade para cada bloco da relação dada.

`pg_visibility(relation regclass, blkno OUT bigint, all_visible OUT boolean, all_frozen OUT boolean, pd_all_visible OUT boolean) returns setof record`: Retorna todos os bits visíveis e todos os bits congelados no mapa de visibilidade para cada bloco da relação dada, além do bit `PD_ALL_VISIBLE` de cada bloco.

`pg_visibility_map_summary(relation regclass, all_visible OUT bigint, all_frozen OUT bigint) returns record`: Retorna o número de páginas visíveis e o número de páginas congeladas em toda a relação de acordo com o mapa de visibilidade.

`pg_check_frozen(relation regclass, t_ctid OUT tid) returns setof tid`: Retorna os TIDs dos tuplos não congelados armazenados em páginas marcadas como totalmente congeladas no mapa de visibilidade. Se esta função retornar um conjunto não vazio de TIDs, o mapa de visibilidade está corrompido.

`pg_check_visible(relation regclass, t_ctid OUT tid) returns setof tid`: Retorna os TIDs dos tuplos não visíveis armazenados em páginas marcadas como visíveis em todo o mapa de visibilidade. Se esta função retornar um conjunto não vazio de TIDs, o mapa de visibilidade está corrompido.

`pg_truncate_visibility_map(relation regclass) returns void`: Trunca o mapa de visibilidade para a relação dada. Esta função é útil se você acredita que o mapa de visibilidade para a relação está corrompido e deseja forçar a reconstrução dele. O primeiro `VACUUM` executado na relação dada após a execução desta função irá analisar todas as páginas na relação e reconstruir o mapa de visibilidade. (Até que isso seja feito, as consultas tratarão o mapa de visibilidade como contendo todos os zeros.)

Por padrão, essas funções só podem ser executadas por superusuários e papéis com privilégios da função `pg_stat_scan_tables`, com exceção de `pg_truncate_visibility_map(relation regclass)`, que só pode ser executada por superusuários.

### F.36.2. Autor [#](#PGVISIBILITY-AUTHOR)

Robert Haas `<rhaas@postgresql.org>`
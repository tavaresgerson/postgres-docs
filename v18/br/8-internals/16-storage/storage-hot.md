## 66.7. Tuples apenas em pilha (HOT) [#](#STORAGE-HOT)

Para permitir alta concorrência, o PostgreSQL usa o controle de concorrência multiversão (mvcc-intro.md "13.1. Introduction") (MVCC) para armazenar linhas. No entanto, o MVCC tem algumas desvantagens para consultas de atualização. Especificamente, as atualizações exigem que novas versões das linhas sejam adicionadas às tabelas. Isso também pode exigir novas entradas de índice para cada linha atualizada, e a remoção das versões antigas das linhas e de suas entradas de índice pode ser cara.

Para ajudar a reduzir o overhead das atualizações, o PostgreSQL tem uma otimização chamada tuplas apenas em heap (HOT). Essa otimização é possível quando:

* A atualização não modifica quaisquer colunas referenciadas pelos índices da tabela, incluindo os índices de resumo. O único método de índice de resumo na distribuição principal do PostgreSQL é [BRIN](brin.md). * Há espaço livre suficiente na página que contém a linha antiga para a linha atualizada.

Nesses casos, os tuplos apenas de pilha oferecem duas otimizações:

* Não são necessárias novas entradas no índice para representar linhas atualizadas, no entanto, os índices resumidos ainda podem precisar ser atualizados.
* Quando uma linha é atualizada várias vezes, as versões da linha que não são as mais antigas e as mais recentes podem ser completamente removidas durante o funcionamento normal, incluindo `SELECT`, em vez de exigir operações periódicas de vácuo. (Os índices sempre se referem ao [identificador de item de página](storage-page-layout.md) da versão original da linha. Os dados do tuplo associados a essa versão da linha são removidos e seu identificador de item é convertido em um redirecionamento que aponta para a versão mais antiga que ainda pode ser visível para algumas transações concorrentes. As versões intermediárias da linha que não são mais visíveis para ninguém são completamente removidas e os identificadores de itens de página associados são disponibilizados para uso novamente.)

Você pode aumentar a probabilidade de espaço suficiente para atualizações HOT ao diminuir o `fillfactor` de uma tabela. Se você não fizer isso, as atualizações HOT ainda ocorrerão porque novas linhas migrarão naturalmente para novas páginas e páginas existentes com espaço livre suficiente para novas versões de linha. A visualização do sistema [pg_stat_all_tables](monitoring-stats.md#MONITORING-PG-STAT-ALL-TABLES-VIEW) permite o monitoramento da ocorrência de atualizações HOT e não HOT.
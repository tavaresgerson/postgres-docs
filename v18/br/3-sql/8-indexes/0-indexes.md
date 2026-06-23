## Capítulo 11. Índices

**Índice**

* [11.1. Introdução](indexes-intro.md)
* [11.2. Tipos de índice](indexes-types.md)

+ [11.2.1. B-Tree][(indexes-types.md#INDEXES-TYPES-BTREE)
+ [11.2.2. Hash][(indexes-types.md#INDEXES-TYPES-HASH)
+ [11.2.3. GiST][(indexes-types.md#INDEXES-TYPE-GIST)
+ [11.2.4. SP-GiST][(indexes-types.md#INDEXES-TYPE-SPGIST)
+ [11.2.5. GIN][(indexes-types.md#INDEXES-TYPES-GIN)
+ [11.2.6. BRIN][(indexes-types.md#INDEXES-TYPES-BRIN)

* [11.3. Índices de múltiplas colunas](indexes-multicolumn.md)
* [11.4. Índices e `ORDER BY`](indexes-ordering.md)
* [11.5. Combinando múltiplos índices](indexes-bitmap-scans.md)
* [11.6. Índices únicos](indexes-unique.md)
* [11.7. Índices em expressões](indexes-expressional.md)
* [11.8. Índices parciais](indexes-partial.md)
* [11.9. Scaneamento de índices e índices cobertores](indexes-index-only-scans.md)
* [11.10. Classes de operadores e famílias de operadores](indexes-opclass.md)
* [11.11. Índices e colatações](indexes-collations.md)
* [11.12. Examinando o uso de índices](indexes-examine.md)

Os índices são uma maneira comum de melhorar o desempenho do banco de dados. Um índice permite que o servidor do banco de dados encontre e retorne linhas específicas muito mais rápido do que poderia fazer sem um índice. Mas os índices também adicionam sobrecarga ao sistema do banco de dados como um todo, então eles devem ser usados sensatamente.
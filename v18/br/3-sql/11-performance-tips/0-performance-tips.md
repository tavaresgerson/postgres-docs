## Capítulo 14. Dicas de desempenho

**Índice**

* [14.1. Usando `EXPLAIN`](using-explain.md)

+ [14.1.1. `EXPLAIN` Fundamentos](using-explain.md#USING-EXPLAIN-BASICS)
+ [14.1.2. `EXPLAIN ANALYZE`](using-explain.md#USING-EXPLAIN-ANALYZE)
+ [14.1.3. Observações](using-explain.md#USING-EXPLAIN-CAVEATS)

* [14.2. Estatísticas utilizadas pelo planejador](planner-stats.md)

+ [14.2.1. Estatísticas de uma coluna única](planner-stats.md#PLANNER-STATS-SINGLE-COLUMN)
+ [14.2.2. Estatísticas extensas](planner-stats.md#PLANNER-STATS-EXTENDED)

* [14.3. Controle do Planejador com Cláusulas Explicitas `JOIN`](explicit-joins.md)
* [14.4. Preenchimento de um Banco de Dados](populate.md)

+ [14.4.1. Desativar o Autocommit](populate.md#DISABLE-AUTOCOMMIT)
+ [14.4.2. Usar `COPY`](populate.md#POPULATE-COPY-FROM)
+ [14.4.3. Remover índices](populate.md#POPULATE-RM-INDEXES)
+ [14.4.4. Remover restrições de chave estrangeira](populate.md#POPULATE-RM-FKEYS)
+ [14.4.5. Aumentar `maintenance_work_mem`](populate.md#POPULATE-WORK-MEM)
+ [14.4.6. Aumentar `max_wal_size`](populate.md#POPULATE-MAX-WAL-SIZE)
+ [14.4.7. Desativar a arquivamento e replicação em streaming do WAL](populate.md#POPULATE-PITR)
+ [14.4.8. Executar `ANALYZE` posteriormente](populate.md#POPULATE-ANALYZE)
+ [14.4.9. Algumas notas sobre o pg_dump](populate.md#POPULATE-PG-DUMP)

* [14.5. Configurações Não Duradouras](non-durability.md)

O desempenho da consulta pode ser afetado por muitas coisas. Algumas dessas coisas podem ser controladas pelo usuário, enquanto outras são fundamentais para o projeto subjacente do sistema. Este capítulo fornece algumas dicas sobre como entender e ajustar o desempenho do PostgreSQL.
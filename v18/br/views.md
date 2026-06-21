## Capítulo 53. Visões do sistema

**Índice**

* [53.1. Overview](views-overview.md)
* [53.2. `pg_aios`](view-pg-aios.md)
* [53.3. `pg_available_extensions`](view-pg-available-extensions.md)
* [53.4. `pg_available_extension_versions`](view-pg-available-extension-versions.md)
* [53.5. `pg_backend_memory_contexts`](view-pg-backend-memory-contexts.md)
* [53.6. `pg_config`](view-pg-config.md)
* [53.7. `pg_cursors`](view-pg-cursors.md)
* [53.8. `pg_file_settings`](view-pg-file-settings.md)
* [53.9. `pg_group`](view-pg-group.md)
* [53.10. `pg_hba_file_rules`](view-pg-hba-file-rules.md)
* [53.11. `pg_ident_file_mappings`](view-pg-ident-file-mappings.md)
* [53.12. `pg_indexes`](view-pg-indexes.md)
* [53.13. `pg_locks`](view-pg-locks.md)
* [53.14. `pg_matviews`](view-pg-matviews.md)
* [53.15. `pg_policies`](view-pg-policies.md)
* [53.16. `pg_prepared_statements`](view-pg-prepared-statements.md)
* [53.17. `pg_prepared_xacts`](view-pg-prepared-xacts.md)
* [53.18. `pg_publication_tables`](view-pg-publication-tables.md)
* [53.19. `pg_replication_origin_status`](view-pg-replication-origin-status.md)
* [53.20. `pg_replication_slots`](view-pg-replication-slots.md)
* [53.21. `pg_roles`](view-pg-roles.md)
* [53.22. `pg_rules`](view-pg-rules.md)
* [53.23. `pg_seclabels`](view-pg-seclabels.md)
* [53.24. `pg_sequences`](view-pg-sequences.md)
* [53.25. `pg_settings`](view-pg-settings.md)
* [53.26. `pg_shadow`](view-pg-shadow.md)
* [53.27. `pg_shmem_allocations`](view-pg-shmem-allocations.md)
* [53.28. `pg_shmem_allocations_numa`](view-pg-shmem-allocations-numa.md)
* [53.29. `pg_stats`](view-pg-stats.md)
* [53.30. `pg_stats_ext`](view-pg-stats-ext.md)
* [53.31. `pg_stats_ext_exprs`](view-pg-stats-ext-exprs.md)
* [53.32. `pg_tables`](view-pg-tables.md)
* [53.33. `pg_timezone_abbrevs`](view-pg-timezone-abbrevs.md)
* [53.34. `pg_timezone_names`](view-pg-timezone-names.md)
* [53.35. `pg_user`](view-pg-user.md)
* [53.36. `pg_user_mappings`](view-pg-user-mappings.md)
* [53.37. `pg_views`](view-pg-views.md)
* [53.38. `pg_wait_events`](view-pg-wait-events.md)

Além dos catálogos do sistema, o PostgreSQL oferece vários pontos de vista integrados. Alguns pontos de vista do sistema fornecem acesso conveniente a algumas consultas comumente usadas nos catálogos do sistema. Outros pontos de vista fornecem acesso ao estado interno do servidor.

O esquema de informações ([Capítulo 35](information-schema.md)) oferece um conjunto alternativo de visualizações que sobrepõem a funcionalidade das visualizações do sistema. Como o esquema de informações é padrão SQL, enquanto as visualizações descritas aqui são específicas do PostgreSQL, geralmente é melhor usar o esquema de informações se ele fornecer todas as informações de que você precisa.

[Tabela 53.1](views-overview.md#VIEW-TABLE "Table 53.1. System Views") lista as visualizações do sistema descritas aqui. Mais documentação detalhada de cada visualização segue abaixo. Existem algumas visualizações adicionais que fornecem acesso a estatísticas acumuladas; elas são descritas em [Tabela 27.2](monitoring-stats.md#MONITORING-STATS-VIEWS-TABLE "Table 27.2. Collected Statistics Views").
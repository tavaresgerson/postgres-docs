## 53.1. Visão geral [#](#VIEWS-OVERVIEW)

[Tabela 53.1](views-overview.md#VIEW-TABLE) lista as visualizações do sistema. Mais documentação detalhada de cada catálogo segue abaixo. Exceto onde indicado, todas as visualizações descritas aqui são somente leitura.

**Tabela 53.1. Visões do sistema**



<table border="1" class="table" summary="System Views">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    View Name
   </th>
   <th>
    Propósito
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <a class="link" href="view-pg-aios.md" title="53.2. pg_aios">
     <code class="structname">
      pg_aios
     </code>
    </a>
   </td>
   <td>
    Conexões de E/S asíncronas em uso
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-available-extensions.md" title="53.3. pg_available_extensions">
     <code class="structname">
      pg_available_extensions
     </code>
    </a>
   </td>
   <td>
    extensões disponíveis
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-available-extension-versions.md" title="53.4. pg_available_extension_versions">
     <code class="structname">
      pg_available_extension_versions
     </code>
    </a>
   </td>
   <td>
    versões disponíveis de extensões
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-backend-memory-contexts.md" title="53.5. pg_backend_memory_contexts">
     <code class="structname">
      pg_backend_memory_contexts
     </code>
    </a>
   </td>
   <td>
    contextos de memória de backend
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-config.md" title="53.6. pg_config">
     <code class="structname">
      pg_config
     </code>
    </a>
   </td>
   <td>
    parâmetros de configuração em tempo de compilação
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-cursors.md" title="53.7. pg_cursors">
     <code class="structname">
      pg_cursors
     </code>
    </a>
   </td>
   <td>
    mouses abertos
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-file-settings.md" title="53.8. pg_file_settings">
     <code class="structname">
      pg_file_settings
     </code>
    </a>
   </td>
   <td>
    resumo dos conteúdos do arquivo de configuração
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-group.md" title="53.9. pg_group">
     <code class="structname">
      pg_group
     </code>
    </a>
   </td>
   <td>
    grupos de usuários de banco de dados
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-hba-file-rules.md" title="53.10. pg_hba_file_rules">
     <code class="structname">
      pg_hba_file_rules
     </code>
    </a>
   </td>
   <td>
    Resumo do conteúdo do arquivo de configuração de autenticação do cliente
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-ident-file-mappings.md" title="53.11. pg_ident_file_mappings">
     <code class="structname">
      pg_ident_file_mappings
     </code>
    </a>
   </td>
   <td>
    Resumo do arquivo de configuração de mapeamento do nome do usuário do cliente
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-indexes.md" title="53.12. pg_indexes">
     <code class="structname">
      pg_indexes
     </code>
    </a>
   </td>
   <td>
    índice
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-locks.md" title="53.13. pg_locks">
     <code class="structname">
      pg_locks
     </code>
    </a>
   </td>
   <td>
    trancas atualmente mantidas ou aguardadas
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-matviews.md" title="53.14. pg_matviews">
     <code class="structname">
      pg_matviews
     </code>
    </a>
   </td>
   <td>
    visões materializadas
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-policies.md" title="53.15. pg_policies">
     <code class="structname">
      pg_policies
     </code>
    </a>
   </td>
   <td>
    políticas
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-prepared-statements.md" title="53.16. pg_prepared_statements">
     <code class="structname">
      pg_prepared_statements
     </code>
    </a>
   </td>
   <td>
    declarações preparadas
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-prepared-xacts.md" title="53.17. pg_prepared_xacts">
     <code class="structname">
      pg_prepared_xacts
     </code>
    </a>
   </td>
   <td>
    transações preparadas
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-publication-tables.md" title="53.18. pg_publication_tables">
     <code class="structname">
      pg_publication_tables
     </code>
    </a>
   </td>
   <td>
    publicações e informações de suas tabelas associadas
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-replication-origin-status.md" title="53.19. pg_replication_origin_status">
     <code class="structname">
      pg_replication_origin_status
     </code>
    </a>
   </td>
   <td>
    informações sobre as origens da replicação, incluindo o progresso da replicação
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-replication-slots.md" title="53.20. pg_replication_slots">
     <code class="structname">
      pg_replication_slots
     </code>
    </a>
   </td>
   <td>
    informações sobre o slot de replicação
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-roles.md" title="53.21. pg_roles">
     <code class="structname">
      pg_roles
     </code>
    </a>
   </td>
   <td>
    rôres de banco de dados
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-rules.md" title="53.22. pg_rules">
     <code class="structname">
      pg_rules
     </code>
    </a>
   </td>
   <td>
    regras
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-seclabels.md" title="53.23. pg_seclabels">
     <code class="structname">
      pg_seclabels
     </code>
    </a>
   </td>
   <td>
    etiquetas de segurança
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-sequences.md" title="53.24. pg_sequences">
     <code class="structname">
      pg_sequences
     </code>
    </a>
   </td>
   <td>
    sequências
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-settings.md" title="53.25. pg_settings">
     <code class="structname">
      pg_settings
     </code>
    </a>
   </td>
   <td>
    configurações de parâmetros
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-shadow.md" title="53.26. pg_shadow">
     <code class="structname">
      pg_shadow
     </code>
    </a>
   </td>
   <td>
    usuários de banco de dados
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-shmem-allocations.md" title="53.27. pg_shmem_allocations">
     <code class="structname">
      pg_shmem_allocations
     </code>
    </a>
   </td>
   <td>
    alocações de memória compartilhada
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-shmem-allocations-numa.md" title="53.28. pg_shmem_allocations_numa">
     <code class="structname">
      pg_shmem_allocations_numa
     </code>
    </a>
   </td>
   <td>
    Mapas de nós NUMA para alocações de memória compartilhada
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-stats.md" title="53.29. pg_stats">
     <code class="structname">
      pg_stats
     </code>
    </a>
   </td>
   <td>
    estatísticas do planejador
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-stats-ext.md" title="53.30. pg_stats_ext">
     <code class="structname">
      pg_stats_ext
     </code>
    </a>
   </td>
   <td>
    estatísticas do planejador estendido
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-stats-ext-exprs.md" title="53.31. pg_stats_ext_exprs">
     <code class="structname">
      pg_stats_ext_exprs
     </code>
    </a>
   </td>
   <td>
    estatísticas de planejador estendido para expressões
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-tables.md" title="53.32. pg_tables">
     <code class="structname">
      pg_tables
     </code>
    </a>
   </td>
   <td>
    mesas
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-timezone-abbrevs.md" title="53.33. pg_timezone_abbrevs">
     <code class="structname">
      pg_timezone_abbrevs
     </code>
    </a>
   </td>
   <td>
    abreviações de fuso horário
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-timezone-names.md" title="53.34. pg_timezone_names">
     <code class="structname">
      pg_timezone_names
     </code>
    </a>
   </td>
   <td>
    nomes de fuso horário
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-user.md" title="53.35. pg_user">
     <code class="structname">
      pg_user
     </code>
    </a>
   </td>
   <td>
    usuários de banco de dados
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-user-mappings.md" title="53.36. pg_user_mappings">
     <code class="structname">
      pg_user_mappings
     </code>
    </a>
   </td>
   <td>
    mapas de usuários
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-views.md" title="53.37. pg_views">
     <code class="structname">
      pg_views
     </code>
    </a>
   </td>
   <td>
    visões
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="view-pg-wait-events.md" title="53.38. pg_wait_events">
     <code class="structname">
      pg_wait_events
     </code>
    </a>
   </td>
   <td>
    eventos de espera
   </td>
  </tr>
 </tbody>
</table>






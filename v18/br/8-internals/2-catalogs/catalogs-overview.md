## 52.1. Visão geral [#](#CATALOGS-OVERVIEW)

[Tabela 52.1](catalogs-overview.md#CATALOG-TABLE) lista os catálogos do sistema. Mais documentação detalhada de cada catálogo segue abaixo.

A maioria dos catálogos do sistema é copiada do banco de dados de modelo durante a criação do banco de dados e, posteriormente, são específicos do banco de dados. Alguns catálogos são compartilhados fisicamente em todos os bancos de dados de um clúster; esses são mencionados nas descrições dos catálogos individuais.

**Tabela 52.1. Catálogos do sistema**



<table>
 <thead>
  <tr>
   <th>
    Catalog Name
   </th>
   <th>
    Propósito
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <a class="link" href="catalog-pg-aggregate.md" title="52.2. pg_aggregate">
     <code>
      pg_aggregate
     </code>
    </a>
   </td>
   <td>
    funções agregadas
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-am.md" title="52.3. pg_am">
     <code>
      pg_am
     </code>
    </a>
   </td>
   <td>
    métodos de acesso de relações
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-amop.md" title="52.4. pg_amop">
     <code>
      pg_amop
     </code>
    </a>
   </td>
   <td>
    operadores de métodos de acesso
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-amproc.md" title="52.5. pg_amproc">
     <code>
      pg_amproc
     </code>
    </a>
   </td>
   <td>
    funções de suporte para métodos de acesso
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-attrdef.md" title="52.6. pg_attrdef">
     <code>
      pg_attrdef
     </code>
    </a>
   </td>
   <td>
    valores padrão da coluna
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-attribute.md" title="52.7. pg_attribute">
     <code>
      pg_attribute
     </code>
    </a>
   </td>
   <td>
    colunas da tabela (
    <span class="quote">
     “
     <span class="quote">
      atributos
     </span>
     ”
    </span>
    )
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
     <code>
      pg_authid
     </code>
    </a>
   </td>
   <td>
    identificadores de autorização ( papéis)
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-auth-members.md" title="52.9. pg_auth_members">
     <code>
      pg_auth_members
     </code>
    </a>
   </td>
   <td>
    identificador de autorização relações de filiação
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-cast.md" title="52.10. pg_cast">
     <code>
      pg_cast
     </code>
    </a>
   </td>
   <td>
    casts (conversões de tipos de dados)
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
     <code>
      pg_class
     </code>
    </a>
   </td>
   <td>
    tabelas, índices, sequências, visualizações (
    <span class="quote">
     “
     <span class="quote">
      relações
     </span>
     ”
    </span>
    )
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-collation.md" title="52.12. pg_collation">
     <code>
      pg_collation
     </code>
    </a>
   </td>
   <td>
    colunações (informações de localização)
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-constraint.md" title="52.13. pg_constraint">
     <code>
      pg_constraint
     </code>
    </a>
   </td>
   <td>
    restrições de verificação, restrições únicas, restrições de chave primária, restrições de chave estrangeira
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-conversion.md" title="52.14. pg_conversion">
     <code>
      pg_conversion
     </code>
    </a>
   </td>
   <td>
    informações de conversão de codificação
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-database.md" title="52.15. pg_database">
     <code>
      pg_database
     </code>
    </a>
   </td>
   <td>
    bases de dados dentro deste clúster de bases de dados
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-db-role-setting.md" title="52.16. pg_db_role_setting">
     <code>
      pg_db_role_setting
     </code>
    </a>
   </td>
   <td>
    configurações por papel e por banco de dados
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-default-acl.md" title="52.17. pg_default_acl">
     <code>
      pg_default_acl
     </code>
    </a>
   </td>
   <td>
    privilegios padrão para tipos de objeto
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-depend.md" title="52.18. pg_depend">
     <code>
      pg_depend
     </code>
    </a>
   </td>
   <td>
    dependências entre objetos do banco de dados
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-description.md" title="52.19. pg_description">
     <code>
      pg_description
     </code>
    </a>
   </td>
   <td>
    descrições ou comentários sobre objetos de banco de dados
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-enum.md" title="52.20. pg_enum">
     <code>
      pg_enum
     </code>
    </a>
   </td>
   <td>
    definições de rótulo e valor de enum
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-event-trigger.md" title="52.21. pg_event_trigger">
     <code>
      pg_event_trigger
     </code>
    </a>
   </td>
   <td>
    eventos desencadeadores
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-extension.md" title="52.22. pg_extension">
     <code>
      pg_extension
     </code>
    </a>
   </td>
   <td>
    extensões instaladas
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-foreign-data-wrapper.md" title="52.23. pg_foreign_data_wrapper">
     <code>
      pg_foreign_data_wrapper
     </code>
    </a>
   </td>
   <td>
    definições de wrappers de dados estrangeiros
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-foreign-server.md" title="52.24. pg_foreign_server">
     <code>
      pg_foreign_server
     </code>
    </a>
   </td>
   <td>
    definições de servidores estrangeiros
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-foreign-table.md" title="52.25. pg_foreign_table">
     <code>
      pg_foreign_table
     </code>
    </a>
   </td>
   <td>
    informações adicionais sobre a mesa estrangeira
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-index.md" title="52.26. pg_index">
     <code>
      pg_index
     </code>
    </a>
   </td>
   <td>
    informações adicionais do índice
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-inherits.md" title="52.27. pg_inherits">
     <code>
      pg_inherits
     </code>
    </a>
   </td>
   <td>
    hierarquia de herança de tabela
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-init-privs.md" title="52.28. pg_init_privs">
     <code>
      pg_init_privs
     </code>
    </a>
   </td>
   <td>
    privilégios iniciais do objeto
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-language.md" title="52.29. pg_language">
     <code>
      pg_language
     </code>
    </a>
   </td>
   <td>
    linguagens para escrever funções
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-largeobject.md" title="52.30. pg_largeobject">
     <code>
      pg_largeobject
     </code>
    </a>
   </td>
   <td>
    páginas de dados para objetos grandes
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-largeobject-metadata.md" title="52.31. pg_largeobject_metadata">
     <code>
      pg_largeobject_metadata
     </code>
    </a>
   </td>
   <td>
    metadados para objetos grandes
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-namespace.md" title="52.32. pg_namespace">
     <code>
      pg_namespace
     </code>
    </a>
   </td>
   <td>
    esquema
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-opclass.md" title="52.33. pg_opclass">
     <code>
      pg_opclass
     </code>
    </a>
   </td>
   <td>
    classes de operadores de método de acesso
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-operator.md" title="52.34. pg_operator">
     <code>
      pg_operator
     </code>
    </a>
   </td>
   <td>
    operadores
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-opfamily.md" title="52.35. pg_opfamily">
     <code>
      pg_opfamily
     </code>
    </a>
   </td>
   <td>
    métodos de acesso famílias de operadores
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-parameter-acl.md" title="52.36. pg_parameter_acl">
     <code>
      pg_parameter_acl
     </code>
    </a>
   </td>
   <td>
    parâmetros de configuração para os quais foram concedidos privilégios
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-partitioned-table.md" title="52.37. pg_partitioned_table">
     <code>
      pg_partitioned_table
     </code>
    </a>
   </td>
   <td>
    informações sobre a chave de partição das tabelas
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-policy.md" title="52.38. pg_policy">
     <code>
      pg_policy
     </code>
    </a>
   </td>
   <td>
    políticas de segurança de linha
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
     <code>
      pg_proc
     </code>
    </a>
   </td>
   <td>
    funções e procedimentos
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-publication.md" title="52.40. pg_publication">
     <code>
      pg_publication
     </code>
    </a>
   </td>
   <td>
    publicações para replicação lógica
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-publication-namespace.md" title="52.41. pg_publication_namespace">
     <code>
      pg_publication_namespace
     </code>
    </a>
   </td>
   <td>
    esquema para mapeamento de publicação
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-publication-rel.md" title="52.42. pg_publication_rel">
     <code>
      pg_publication_rel
     </code>
    </a>
   </td>
   <td>
    relação com mapeamento de publicação
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-range.md" title="52.43. pg_range">
     <code>
      pg_range
     </code>
    </a>
   </td>
   <td>
    informações sobre os tipos de alcance
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-replication-origin.md" title="52.44. pg_replication_origin">
     <code>
      pg_replication_origin
     </code>
    </a>
   </td>
   <td>
    origens de replicação registradas
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-rewrite.md" title="52.45. pg_rewrite">
     <code>
      pg_rewrite
     </code>
    </a>
   </td>
   <td>
    regras de reescrita de consultas
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-seclabel.md" title="52.46. pg_seclabel">
     <code>
      pg_seclabel
     </code>
    </a>
   </td>
   <td>
    etiquetas de segurança em objetos de banco de dados
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-sequence.md" title="52.47. pg_sequence">
     <code>
      pg_sequence
     </code>
    </a>
   </td>
   <td>
    informações sobre sequências
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-shdepend.md" title="52.48. pg_shdepend">
     <code>
      pg_shdepend
     </code>
    </a>
   </td>
   <td>
    dependências em objetos compartilhados
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-shdescription.md" title="52.49. pg_shdescription">
     <code>
      pg_shdescription
     </code>
    </a>
   </td>
   <td>
    comentários sobre objetos compartilhados
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-shseclabel.md" title="52.50. pg_shseclabel">
     <code>
      pg_shseclabel
     </code>
    </a>
   </td>
   <td>
    etiquetas de segurança em objetos de banco de dados compartilhados
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-statistic.md" title="52.51. pg_statistic">
     <code>
      pg_statistic
     </code>
    </a>
   </td>
   <td>
    estatísticas do planejador
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-statistic-ext.md" title="52.52. pg_statistic_ext">
     <code>
      pg_statistic_ext
     </code>
    </a>
   </td>
   <td>
    estatísticas de planejador estendido (definição)
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-statistic-ext-data.md" title="52.53. pg_statistic_ext_data">
     <code>
      pg_statistic_ext_data
     </code>
    </a>
   </td>
   <td>
    estatísticas de planejador estendido (estatísticas construídas)
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-subscription.md" title="52.54. pg_subscription">
     <code>
      pg_subscription
     </code>
    </a>
   </td>
   <td>
    assinaturas de replicação lógica
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-subscription-rel.md" title="52.55. pg_subscription_rel">
     <code>
      pg_subscription_rel
     </code>
    </a>
   </td>
   <td>
    estado de relação para assinaturas
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-tablespace.md" title="52.56. pg_tablespace">
     <code>
      pg_tablespace
     </code>
    </a>
   </td>
   <td>
    espaços de tabela dentro deste clúster de banco de dados
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-transform.md" title="52.57. pg_transform">
     <code>
      pg_transform
     </code>
    </a>
   </td>
   <td>
    transforma (conversão de tipo de dados para linguagem procedural)
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-trigger.md" title="52.58. pg_trigger">
     <code>
      pg_trigger
     </code>
    </a>
   </td>
   <td>
    desencadeadores
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-ts-config.md" title="52.59. pg_ts_config">
     <code>
      pg_ts_config
     </code>
    </a>
   </td>
   <td>
    configurações de pesquisa de texto
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-ts-config-map.md" title="52.60. pg_ts_config_map">
     <code>
      pg_ts_config_map
     </code>
    </a>
   </td>
   <td>
    mapas de correspondência de tokens das configurações de pesquisa de texto
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-ts-dict.md" title="52.61. pg_ts_dict">
     <code>
      pg_ts_dict
     </code>
    </a>
   </td>
   <td>
    dicionários de busca de texto
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-ts-parser.md" title="52.62. pg_ts_parser">
     <code>
      pg_ts_parser
     </code>
    </a>
   </td>
   <td>
    parâmetros de busca de texto
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-ts-template.md" title="52.63. pg_ts_template">
     <code>
      pg_ts_template
     </code>
    </a>
   </td>
   <td>
    modelos de pesquisa de texto
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-type.md" title="52.64. pg_type">
     <code>
      pg_type
     </code>
    </a>
   </td>
   <td>
    tipos de dados
   </td>
  </tr>
  <tr>
   <td>
    <a class="link" href="catalog-pg-user-mapping.md" title="52.65. pg_user_mapping">
     <code>
      pg_user_mapping
     </code>
    </a>
   </td>
   <td>
    mapas de usuários para servidores estrangeiros
   </td>
  </tr>
 </tbody>
</table>






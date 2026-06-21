# Parte V. Programação de Servidor

Esta parte trata da extensão das funcionalidades do servidor com funções definidas pelo usuário, tipos de dados, gatilhos, etc. Estes são tópicos avançados que devem ser abordados apenas após a compreensão de toda a outra documentação do usuário sobre PostgreSQL. Os capítulos posteriores desta parte descrevem as linguagens de programação do lado do servidor disponíveis na distribuição PostgreSQL, bem como questões gerais relacionadas à programação do lado do servidor. É essencial ler pelo menos as seções anteriores de [Capítulo 36] (cobrindo funções) antes de mergulhar no material sobre programação do lado do servidor.

**Índice**

* [36. Extensão do SQL][(extend.md)]

+ [36.1. Como a Extensibilidade Funciona][(extend-how.md)]
+ [36.2. O Sistema de Tipos do PostgreSQL][(extend-type-system.md)]
+ [36.3. Funções Definidas pelo Usuário][(xfunc.md)]
+ [36.4. Procedimentos Definidos pelo Usuário][(xproc.md)]
+ [36.5. Funções do Idioma de Consulta (SQL)][(xfunc-sql.md)]
+ [36.6. Sobrecarga de Funções][(xfunc-overload.md)]
+ [36.7. Categorias de Volatilidade das Funções][(xfunc-volatility.md)]
+ [36.8. Funções de Linguagem Procedimental][(xfunc-pl.md)]
+ [36.9. Funções de Linguagem Interna][(xfunc-internal.md)]
+ [36.10. Funções de Linguagem C][(xfunc-c.md)]
+ [36.11. Informações de Otimização de Funções][(xfunc-optimization.md)]
+ [36.12. Agregados Definidos pelo Usuário][(xaggr.md)]
+ [36.13. Tipos Definidos pelo Usuário][(xtypes.md)]
+ [36.14. Operadores Definidos pelo Usuário][(xoper.md)]
+ [36.15. Informações de Otimização de Operadores][(xoper-optimization.md)]
+ [36.16. Interação de Extensões com Índices][(xindex.md)]
+ [36.17. Embalagem de Objetos Relacionados em uma Extensão][(extend-extensions.md)]
+ [36.18. Infraestrutura de Construção de Extensões][(extend-pgxs.md)]

* [37. Gatilhos](triggers.md)

+ [37.1. Visão geral do comportamento do gatilho][(trigger-definition.md)]
+ [37.2. Visibilidade das alterações dos dados][(trigger-datachanges.md)]
+ [37.3. Escrever funções de gatilho em C][(trigger-interface.md)]
+ [37.4. Um exemplo completo de gatilho][(trigger-example.md)]

* [38. Gatilhos de evento](event-triggers.md)

+ [38.1. Visão geral do comportamento do gatilho de evento][(event-trigger-definition.md)]
+ [38.2. Escrever funções de gatilho de evento em C][(event-trigger-interface.md)]
+ [38.3. Um exemplo completo de gatilho de evento][(event-trigger-example.md)]
+ [38.4. Um exemplo de gatilho de evento de reescrita de tabela][(event-trigger-table-rewrite-example.md)]
+ [38.5. Um exemplo de gatilho de evento de login em banco de dados][(event-trigger-database-login-example.md)]

* Sistema de Regras (rules.md)

+ [39.1. Árvores de Consulta](querytree.md)
+ [39.2. Visualizações e o Sistema de Regras](rules-views.md)
+ [39.3. Visualizações Materializadas](rules-materializedviews.md)
+ [39.4. Regras sobre `INSERT`, `UPDATE` e `DELETE`](rules-update.md)
+ [39.5. Regras e Privilégios](rules-privileges.md)
+ [39.6. Regras e Status de Comando](rules-status.md)
+ [39.7. Regras versus Deslizadores](rules-triggers.md)

* [40. Linguagens Processuais](xplang.md)

+ [40.1. Instalação de Linguagens Procedimentais](xplang-install.md)

* [41. PL/pgSQL — Linguagem Procedimental SQL](plpgsql.md)

+ [41.1. Visão geral](plpgsql-overview.md)
+ [41.2. Estrutura do PL/pgSQL](plpgsql-structure.md)
+ [41.3. Declarações](plpgsql-declarations.md)
+ [41.4. Expressões](plpgsql-expressions.md)
+ [41.5. Declarações básicas](plpgsql-statements.md)
+ [41.6. Estruturas de controle](plpgsql-control-structures.md)
+ [41.7. Cursors](plpgsql-cursors.md)
+ [41.8. Gerenciamento de transações](plpgsql-transactions.md)
+ [41.9. Erros e mensagens](plpgsql-errors-and-messages.md)
+ [41.10. Funções de gatilho](plpgsql-trigger.md)
+ [41.11. PL/pgSQL sob o véu](plpgsql-implementation.md)
+ [41.12. Dicas para o desenvolvimento em PL/pgSQL](plpgsql-development-tips.md)
+ [41.13. Portando do Oracle PL/SQL](plpgsql-porting.md)

* [42. PL/Tcl — Linguagem Procedimental Tcl](pltcl.md)

+ [42.1. Visão geral](pltcl-overview.md)
+ [42.2. Funções e argumentos PL/Tcl](pltcl-functions.md)
+ [42.3. Valores de dados em PL/Tcl](pltcl-data.md)
+ [42.4. Dados globais em PL/Tcl](pltcl-global.md)
+ [42.5. Acesso a bancos de dados em PL/Tcl](pltcl-dbaccess.md)
+ [42.6. Funções de gatilho em PL/Tcl](pltcl-trigger.md)
+ [42.7. Funções de gatilho de evento em PL/Tcl](pltcl-event-trigger.md)
+ [42.8. Tratamento de erros em PL/Tcl](pltcl-error-handling.md)
+ [42.9. Subtransações explícitas em PL/Tcl](pltcl-subtransactions.md)
+ [42.10. Gerenciamento de transações](pltcl-transactions.md)
+ [42.11. Configuração de PL/Tcl](pltcl-config.md)
+ [42.12. Nomes de procedimentos Tcl](pltcl-procnames.md)

* [43. PL/Perl — Linguagem Procedimental Perl](plperl.md)

+ [43.1. Funções e Argumentos PL/Perl](plperl-funcs.md)
+ [43.2. Valores de Dados em PL/Perl](plperl-data.md)
+ [43.3. Funções Integrante](plperl-builtins.md)
+ [43.4. Valores Globais em PL/Perl](plperl-global.md)
+ [43.5. PL/Perl Confiável e Não Confiável](plperl-trusted.md)
+ [43.6. Gatilhos PL/Perl](plperl-triggers.md)
+ [43.7. Gatilhos de Evento PL/Perl](plperl-event-triggers.md)
+ [43.8. PL/Perl Sob o Cobertizo](plperl-under-the-hood.md)

* [44. PL/Python — Linguagem Procedimental em Python](plpython.md)

+ [44.1. Funções PL/Python](plpython-funcs.md)
+ [44.2. Valores de dados](plpython-data.md)
+ [44.3. Compartilhamento de dados](plpython-sharing.md)
+ [44.4. Blocos de código anônimo](plpython-do.md)
+ [44.5. Funções de gatilho](plpython-trigger.md)
+ [44.6. Acesso a banco de dados](plpython-database.md)
+ [44.7. Subtransações explícitas](plpython-subtransaction.md)
+ [44.8. Gerenciamento de transações](plpython-transactions.md)
+ [44.9. Funções utilitárias](plpython-util.md)
+ [44.10. Python 2 vs. Python 3](plpython-python23.md)
+ [44.11. Variáveis de ambiente](plpython-envar.md)

* [45. Interface de programação do servidor](spi.md)

+ [45.1. Funções de Interface](spi-interface.md)
+ [45.2. Funções de Suporte de Interface](spi-interface-support.md)
+ [45.3. Gerenciamento de Memória](spi-memory.md)
+ [45.4. Gerenciamento de Transações](spi-transaction.md)
+ [45.5. Visibilidade das Alterações de Dados](spi-visibility.md)
+ [45.6. Exemplos](spi-examples.md)

* [46. Processos de trabalho em segundo plano](bgworker.md)
* [47. Decodificação lógica](logicaldecoding.md)

+ [47.1. Exemplos de Decodificação Lógica][(logicaldecoding-example.md)]
+ [47.2. Conceitos de Decodificação Lógica][(logicaldecoding-explanation.md)]
+ [47.3. Interface do Protocolo de Replicação em Streaming][(logicaldecoding-walsender.md)]
+ [47.4. Interface SQL de Decodificação Lógica][(logicaldecoding-sql.md)]
+ [47.5. Catálogos do Sistema Relacionados à Decodificação Lógica][(logicaldecoding-catalogs.md)]
+ [47.6. Plugins de Saída de Decodificação Lógica][(logicaldecoding-output-plugin.md)]
+ [47.7. Escritores de Saída de Decodificação Lógica][(logicaldecoding-writer.md)]
+ [47.8. Suporte a Replicação Síncrona para Decodificação Lógica][(logicaldecoding-synchronous.md)]
+ [47.9. Streaming de Grandes Transações para Decodificação Lógica][(logicaldecoding-streaming.md)]
+ [47.10. Suporte a Compromisso de Duas Fases para Decodificação Lógica][(logicaldecoding-two-phase-commits.md)]

* [48. Rastreamento do progresso da replicação](replication-origins.md)
* [49. Módulos de Arquivo](archive-modules.md)

+ [49.1. Funções de Inicialização](archive-module-init.md)
+ [49.2. Retornos de chamada do módulo de arquivo](archive-module-callbacks.md)

* [Módulos de Validação OAuth][(oauth-validators.md)]

+ [50.1. Projetando com Segurança um Módulo de Validação][(oauth-validator-design.md)]
+ [50.2. Funções de Inicialização][(oauth-validator-init.md)]
+ [50.3. Retornos de Chamada do Validador OAuth][(oauth-validator-callbacks.md)]
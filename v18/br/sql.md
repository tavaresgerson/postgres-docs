# Parte II. A Linguagem SQL

Esta parte descreve o uso da linguagem SQL no PostgreSQL. Começamos descrevendo a sintaxe geral do SQL, depois como criar tabelas, como preencher o banco de dados e como consultá-lo. A parte do meio lista os tipos de dados disponíveis e as funções para uso em comandos SQL. Por último, abordamos vários aspectos importantes para ajustar um banco de dados.

As informações estão organizadas de forma que um usuário novato possa segui-las do início ao fim e obter um entendimento completo dos tópicos, sem precisar fazer referência repetidamente. Os capítulos são destinados a serem autocontidos, para que os usuários avançados possam ler os capítulos individualmente conforme sua escolha. As informações são apresentadas em forma narrativa com unidades temáticas. Os leitores que procuram uma descrição completa de um comando específico são incentivados a revisar o [Parte VI][(reference.md "Part VI. Reference")].

Os leitores devem saber como se conectar a um banco de dados PostgreSQL e emitir comandos SQL. Os leitores que não estão familiarizados com esses problemas são incentivados a ler [Parte I][(tutorial.md "Part I. Tutorial")] primeiro. Os comandos SQL são normalmente inseridos usando o terminal interativo PostgreSQL psql, mas outros programas que possuem funcionalidades semelhantes também podem ser usados.

**Índice**

* [4. Sintaxe SQL](sql-syntax.md)

+ [4.1. Estrutura Lexical](sql-syntax-lexical.md)
+ [4.2. Expressões de Valor](sql-expressions.md)
+ [4.3. Chamando Funções](sql-syntax-calling-funcs.md)

* [5. Definição de dados](ddl.md)

+ [5.1. Fundamentos da tabela](ddl-basics.md)
+ [5.2. Valores padrão](ddl-default.md)
+ [5.3. Colunas de identidade](ddl-identity-columns.md)
+ [5.4. Colunas geradas](ddl-generated-columns.md)
+ [5.5. Restrições](ddl-constraints.md)
+ [5.6. Colunas do sistema](ddl-system-columns.md)
+ [5.7. Modificação de tabelas](ddl-alter.md)
+ [5.8. Privilegios](ddl-priv.md)
+ [5.9. Políticas de segurança de linha](ddl-rowsecurity.md)
+ [5.10. Esquemas](ddl-schemas.md)
+ [5.11. Herança](ddl-inherit.md)
+ [5.12. Partição de tabela](ddl-partitioning.md)
+ [5.13. Dados externos](ddl-foreign-data.md)
+ [5.14. Outros objetos do banco de dados](ddl-others.md)
+ [5.15. Rastreamento de dependências](ddl-depend.md)

* [Manipulação de dados](dml.md)

+ [6.1. Inserindo Dados][(dml-insert.md)]
+ [6.2. Atualizando Dados][(dml-update.md)]
+ [6.3. Excluindo Dados][(dml-delete.md)]
+ [6.4. Retornando Dados de Linhas Modificadas][(dml-returning.md)]

* [7. Perguntas](queries.md)

+ [7.1. Visão geral](queries-overview.md)
+ [7.2. Expressões de tabela](queries-table-expressions.md)
+ [7.3. Listas selecionadas](queries-select-lists.md)
+ [7.4. Combinando consultas (`UNION`, `INTERSECT`, `EXCEPT`)](queries-union.md)
+ [7.5. Ordenação de linhas (`ORDER BY`)](queries-order.md)
+ [7.6. `LIMIT` e `OFFSET`(queries-limit.md)
+ [7.7. `VALUES` Listas](queries-values.md)
+ [7.8. `WITH` Consultas (Expressões de tabela comum)](queries-with.md)

* [Tipos de dados][(datatype.md)]

+ [8.1. Tipos Numéricos](datatype-numeric.md)
+ [8.2. Tipos Monetários](datatype-money.md)
+ [8.3. Tipos de Caracteres](datatype-character.md)
+ [8.4. Tipos de Dados Binários](datatype-binary.md)
+ [8.5. Tipos de Data/Hora](datatype-datetime.md)
+ [8.6. Tipo Booleano](datatype-boolean.md)
+ [8.7. Tipos Enumerados](datatype-enum.md)
+ [8.8. Tipos Geométricos](datatype-geometric.md)
+ [8.9. Tipos de Endereço de Rede](datatype-net-types.md)
+ [8.10. Tipos de String de Bits](datatype-bit.md)
+ [8.11. Tipos de Busca de Texto](datatype-textsearch.md)
+ [8.12. Tipo UUID](datatype-uuid.md)
+ [8.13. Tipo XML](datatype-xml.md)
+ [8.14. Tipos JSON](datatype-json.md)
+ [8.15. Arrays](arrays.md)
+ [8.16. Tipos Compostos](rowtypes.md)
+ [8.17. Tipos de Intervalo](rangetypes.md)
+ [8.18. Tipos de Domínio](domains.md)
+ [8.19. Tipos de Identificador de Objeto](datatype-oid.md)
+ [8.20. Tipo `pg_lsn`](datatype-pg-lsn.md)
+ [8.21. Tipos Pseudo](datatype-pseudo.md)

* [9. Funções e Operadores](functions.md)

+ [9.1. Operadores Lógicos][(functions-logical.md)]
+ [9.2. Funções e Operadores de Comparação][(functions-comparison.md)]
+ [9.3. Funções e Operadores Matemáticos][(functions-math.md)]
+ [9.4. Funções e Operadores de String][(functions-string.md)]
+ [9.5. Funções e Operadores de String Binária][(functions-binarystring.md)]
+ [9.6. Funções e Operadores de String de Bits][(functions-bitstring.md)]
+ [9.7. Contagem de Padrão][(functions-matching.md)]
+ [9.8. Funções e Operadores de Formatação de Tipo de Dados][(functions-formatting.md)]
+ [9.9. Funções e Operadores de Data/Hora][(functions-datetime.md)]
+ [9.10. Funções de Suporte a Enum][(functions-enum.md)]
+ [9.11. Funções e Operadores Geométricos][(functions-geometry.md)]
+ [9.12. Funções e Operadores de Endereço de Rede][(functions-net.md)]
+ [9.13. Funções e Operadores de Busca de Texto][(functions-textsearch.md)]
+ [9.14. Funções de UUID][(functions-uuid.md)]
+ [9.15. Funções e Operadores XML][(functions-xml.md)]
+ [9.16. Funções e Operadores JSON][(functions-json.md)]
+ [9.17. Funções e Operadores de Manipulação de Sequência][(functions-sequence.md)]
+ [9.18. Expressões Condicionais][(functions-conditional.md)]
+ [9.19. Funções e Operadores de Array][(functions-array.md)]
+ [9.20. Funções e Operadores de Intervalo/Multiintervalo][(functions-range.md)]
+ [9.21. Funções de Agregação][(functions-aggregate.md)]
+ [9.22. Funções e Operadores de Janela][(functions-window.md)]
+ [9.23. Funções de Suporte a Fusão][(functions-merge-support.md)]
+ [9.24. Expressões de Subconsulta][(functions-subquery.md)]
+ [9.25. Comparação de Linhas e Arrays][(functions-comparisons.md)]
+ [9.26. Funções de Retorno de Conjunto][(functions-srf.md)]
+ [9.27. Funções e Operadores de Informações do Sistema][(functions-info.md)]
+ [9.28. Funções e Operadores de Administração de Sistema][(functions-admin.md)]
+ [9.29. Funções e Operadores de Triplo][(functions-trigger.md)]
+ [9.30. Funções e Operadores de Triplo Trigger][(functions-event-triggers.md)]
+ [9.31. Funções e Operadores de Informações Estatísticas][(functions-statistics.md)]

* [10. Conversão de Tipo](typeconv.md)

+ [10.1. Visão geral](typeconv-overview.md)
+ [10.2. Operadores](typeconv-oper.md)
+ [10.3. Funções](typeconv-func.md)
+ [10.4. Armazenamento de valores](typeconv-query.md)
+ [10.5. `UNION`, `CASE` e construções relacionadas](typeconv-union-case.md)
+ [10.6. Colunas de saída `SELECT`(typeconv-select.md)

* [11. Índices](indexes.md)

+ [11.1. Introdução][(indexes-intro.md)]
+ [11.2. Tipos de índice][(indexes-types.md)]
+ [11.3. Índices de múltiplas colunas][(indexes-multicolumn.md)]
+ [11.4. Índices e `ORDER BY`[(indexes-ordering.md)]
+ [11.5. Combinando múltiplos índices][(indexes-bitmap-scans.md)]
+ [11.6. Índices exclusivos][(indexes-unique.md)]
+ [11.7. Índices em expressões][(indexes-expressional.md)]
+ [11.8. Índices parciais][(indexes-partial.md)]
+ [11.9. Scaneamento exclusivo de índices e índices de cobertura][(indexes-index-only-scans.md)]
+ [11.10. Classes de operador e famílias de operadores][(indexes-opclass.md)]
+ [11.11. Índices e colatações][(indexes-collations.md)]
+ [11.12. Examinando o uso de índices][(indexes-examine.md)]

* [Pesquisa de texto completo](textsearch.md)

+ [12.1. Introdução][(textsearch-intro.md)]
+ [12.2. Tabelas e Índices][(textsearch-tables.md)]
+ [12.3. Controle da Pesquisa de Texto][(textsearch-controls.md)]
+ [12.4. Recursos Adicionais][(textsearch-features.md)]
+ [12.5. Parsers][(textsearch-parsers.md)]
+ [12.6. Dicionários][(textsearch-dictionaries.md)]
+ [12.7. Exemplo de Configuração][(textsearch-configuration.md)]
+ [12.8. Testando e Depuração da Pesquisa de Texto][(textsearch-debugging.md)]
+ [12.9. Tipos de Índice Preferidos para Pesquisa de Texto][(textsearch-indexes.md)]
+ [12.10. Suporte ao psql][(textsearch-psql.md)]
+ [12.11. Limitações][(textsearch-limitations.md)]

* Controle de Concorrência (mvcc.md)

+ [13.1. Introdução][(mvcc-intro.md)]
+ [13.2. Isolamento de Transação][(transaction-iso.md)]
+ [13.3. Alojamento Explicito][(explicit-locking.md)]
+ [13.4. Verificação de Consistência de Dados ao Nível da Aplicação][(applevel-consistency.md)]
+ [13.5. Tratamento de Falha de Serialização][(mvcc-serialization-failure-handling.md)]
+ [13.6. Caveats][(mvcc-caveats.md)]
+ [13.7. Alojamento e Índices][(locking-indexes.md)]

* Dicas de desempenho (performance-tips.md)

+ [14.1. Uso de `EXPLAIN`](using-explain.md)
+ [14.2. Estatísticas Utilizadas pelo Planejador](planner-stats.md)
+ [14.3. Controle do Planejador com Cláusulas Explicitas `JOIN`](explicit-joins.md)
+ [14.4. Preenchimento de um Banco de Dados](populate.md)
+ [14.5. Configurações Não Duraveis](non-durability.md)

* Consulta paralela (parallel-query.md)

+ [15.1. Como funciona a consulta paralela][(how-parallel-query-works.md)]
+ [15.2. Quando a consulta paralela pode ser usada?][(when-can-parallel-query-be-used.md)]
+ [15.3. Planos paralelos][(parallel-plans.md)]
+ [15.4. Segurança paralela][(parallel-safety.md)]
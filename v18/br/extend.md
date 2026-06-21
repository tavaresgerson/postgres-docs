## Capítulo 36. Extensão do SQL

**Índice**

* [36.1. Como a Extensibilidade Funciona](extend-how.md)
* [36.2. O Sistema de Tipos do PostgreSQL](extend-type-system.md)

+ [36.2.1. Tipos de Base](extend-type-system.md#EXTEND-TYPE-SYSTEM-BASE)
+ [36.2.2. Tipos de Contêiner](extend-type-system.md#EXTEND-TYPE-SYSTEM-CONTAINER)
+ [36.2.3. Domínios](extend-type-system.md#EXTEND-TYPE-SYSTEM-DOMAINS)
+ [36.2.4. Pseudo-Tipos](extend-type-system.md#EXTEND-TYPE-SYSTEM-PSEUDO)
+ [36.2.5. Tipos Polimorficos](extend-type-system.md#EXTEND-TYPES-POLYMORPHIC)

* [36.3. Funções Definidas pelo Usuário](xfunc.md)
* [36.4. Procedimentos Definidos pelo Usuário](xproc.md)
* [36.5. Funções do Idioma de Consulta (SQL)](xfunc-sql.md)

+ [36.5.1. Argumentos para Funções SQL](xfunc-sql.md#XFUNC-SQL-FUNCTION-ARGUMENTS)
+ [36.5.2. Funções SQL em Tipos Básicos](xfunc-sql.md#XFUNC-SQL-BASE-FUNCTIONS)
+ [36.5.3. Funções SQL em Tipos Compostos](xfunc-sql.md#XFUNC-SQL-COMPOSITE-FUNCTIONS)
+ [36.5.4. Funções SQL com Parâmetros de Saída](xfunc-sql.md#XFUNC-OUTPUT-PARAMETERS)
+ [36.5.5. Procedimentos SQL com Parâmetros de Saída](xfunc-sql.md#XFUNC-OUTPUT-PARAMETERS-PROC)
+ [36.5.6. Funções SQL com Número Variável de Argumentos](xfunc-sql.md#XFUNC-SQL-VARIADIC-FUNCTIONS)
+ [36.5.7. Funções SQL com Valores Padrão para Argumentos](xfunc-sql.md#XFUNC-SQL-PARAMETER-DEFAULTS)
+ [36.5.8. Funções SQL como Fontes de Tabela](xfunc-sql.md#XFUNC-SQL-TABLE-FUNCTIONS)
+ [36.5.9. Funções SQL que Retornam Conjuntos](xfunc-sql.md#XFUNC-SQL-FUNCTIONS-RETURNING-SET)
+ [36.5.10. Funções SQL que Retornam `TABLE`](xfunc-sql.md#XFUNC-SQL-FUNCTIONS-RETURNING-TABLE)
+ [36.5.11. Funções SQL Polimorfas](xfunc-sql.md#XFUNC-SQL-POLYMORPHIC-FUNCTIONS)
+ [36.5.12. Funções SQL com Colagens](xfunc-sql.md#XFUNC-SQL-COLLATIONS)

* [36.6. Sobrecarga de Função](xfunc-overload.md)
* [36.7. Categorias de Volatilidade de Função](xfunc-volatility.md)
* [36.8. Funções de Linguagem Procedimental](xfunc-pl.md)
* [36.9. Funções Internacionais](xfunc-internal.md)
* [36.10. Funções em Linguagem C](xfunc-c.md)

+ [36.10.1. Carregamento Dinâmico][(xfunc-c.md#XFUNC-C-DYNLOAD)
+ [36.10.2. Tipos Básicos em Funções em Linguagem C][(xfunc-c.md#XFUNC-C-BASETYPE)
+ [36.10.3. Convenções de Chamada da Versão 1][(xfunc-c.md#XFUNC-C-V1-CALL-CONV)
+ [36.10.4. Escrevendo Código][(xfunc-c.md#XFUNC-C-CODE)
+ [36.10.5. Compilando e Ligando Funções Carregadas Dinamicamente][(xfunc-c.md#DFUNC)
+ [36.10.6. Orientações sobre a Estabilidade da API e ABI do Servidor][(xfunc-c.md#XFUNC-API-ABI-STABILITY-GUIDANCE)
+ [36.10.7. Argumentos de Tipo Composto][(xfunc-c.md#XFUNC-C-COMPOSITE-TYPE-ARGS)
+ [36.10.8. Retornando Linhas (Tipos Compostos)][(xfunc-c.md#XFUNC-C-RETURNING-ROWS)
+ [36.10.9. Retornando Conjuntos][(xfunc-c.md#XFUNC-C-RETURN-SET)
+ [36.10.10. Argumentos Polimorfos e Tipos de Retorno][(xfunc-c.md#XFUNC-C-POLYMORPHIC)
+ [36.10.11. Memória Compartilhada][(xfunc-c.md#XFUNC-SHARED-ADDIN)
+ [36.10.12. LWLocks][(xfunc-c.md#XFUNC-ADDIN-LWLOCKS)
+ [36.10.13. Eventos de Aguarda Personalizados][(xfunc-c.md#XFUNC-ADDIN-WAIT-EVENTS)
+ [36.10.14. Pontos de Injeção][(xfunc-c.md#XFUNC-ADDIN-INJECTION-POINTS)
+ [36.10.15. Estatísticas Cumulativas Personalizadas][(xfunc-c.md#XFUNC-ADDIN-CUSTOM-CUMULATIVE-STATISTICS)
+ [36.10.16. Usando C++ para Extensibilidade][(xfunc-c.md#EXTEND-CPP)

* [36.11. Informações de Otimização de Função](xfunc-optimization.md)
* [36.12. Agregados Definidos pelo Usuário](xaggr.md)

+ [36.12.1. Modo de Agregação de Movimento](xaggr.md#XAGGR-MOVING-AGGREGATES)
+ [36.12.2. Agregados Polimorfos e Variadicos](xaggr.md#XAGGR-POLYMORPHIC-AGGREGATES)
+ [36.12.3. Agregados de Conjunto Ordenado](xaggr.md#XAGGR-ORDERED-SET-AGGREGATES)
+ [36.12.4. Agregação Parcial](xaggr.md#XAGGR-PARTIAL-AGGREGATES)
+ [36.12.5. Funções de Suporte para Agregados](xaggr.md#XAGGR-SUPPORT-FUNCTIONS)

* [36.13. Tipos Definidos pelo Usuário](xtypes.md)

+ [36.13.1. CONSIDERACAO DE TOAST][(xtypes.md#XTYPES-TOAST)

* [36.14. Operadores Definidos pelo Usuário](xoper.md)
* [36.15. Informações de Otimização do Operador](xoper-optimization.md)

+ [36.15.1. `COMMUTATOR`](xoper-optimization.md#XOPER-COMMUTATOR)
+ [36.15.2. `NEGATOR`](xoper-optimization.md#XOPER-NEGATOR)
+ [36.15.3. `RESTRICT`](xoper-optimization.md#XOPER-RESTRICT)
+ [36.15.4. `JOIN`](xoper-optimization.md#XOPER-JOIN)
+ [36.15.5. `HASHES`](xoper-optimization.md#XOPER-HASHES)
+ [36.15.6. `MERGES`](xoper-optimization.md#XOPER-MERGES)

* [36.16. Interação de extensões com índices](xindex.md)

+ [36.16.1. Métodos de índice e classes de operadores](xindex.md#XINDEX-OPCLASS)
+ [36.16.2. Estratégias de métodos de índice](xindex.md#XINDEX-STRATEGIES)
+ [36.16.3. Rotinas de suporte a métodos de índice](xindex.md#XINDEX-SUPPORT)
+ [36.16.4. Um exemplo](xindex.md#XINDEX-EXAMPLE)
+ [36.16.5. Classes de operadores e famílias de operadores](xindex.md#XINDEX-OPFAMILY)
+ [36.16.6. Dependências do sistema em relação a classes de operadores](xindex.md#XINDEX-OPCLASS-DEPENDENCIES)
+ [36.16.7. Ordem dos operadores](xindex.md#XINDEX-ORDERING-OPS)
+ [36.16.8. Características especiais das classes de operadores](xindex.md#XINDEX-OPCLASS-FEATURES)

* [36.17. Objetos relacionados ao acondicionamento em uma extensão](extend-extensions.md)

+ [36.17.1. Arquivos de extensão](extend-extensions.md#EXTEND-EXTENSIONS-FILES)
+ [36.17.2. Realocação de extensão](extend-extensions.md#EXTEND-EXTENSIONS-RELOCATION)
+ [36.17.3. Tabelas de configuração de extensão](extend-extensions.md#EXTEND-EXTENSIONS-CONFIG-TABLES)
+ [36.17.4. Atualizações de extensão](extend-extensions.md#EXTEND-EXTENSIONS-UPDATES)
+ [36.17.5. Instalação de extensões usando scripts de atualização](extend-extensions.md#EXTEND-EXTENSIONS-UPDATE-SCRIPTS)
+ [36.17.6. Considerações de segurança para extensões](extend-extensions.md#EXTEND-EXTENSIONS-SECURITY)
+ [36.17.7. Exemplo de extensão](extend-extensions.md#EXTEND-EXTENSIONS-EXAMPLE)

* [36.18. Edifício de extensão de infraestrutura](extend-pgxs.md)

Nas seções a seguir, discutiremos como você pode estender o PostgreSQL SQL, adicionando:

* funções (a partir de [Seção 36.3](xfunc.md))
* agregados (a partir de [Seção 36.12](xaggr.md))
* tipos de dados (a partir de [Seção 36.13](xtypes.md))
* operadores (a partir de [Seção 36.14](xoper.md))
* classes de operadores para índices (a partir de [Seção 36.16](xindex.md))
* pacotes de objetos relacionados (a partir de [Seção 36.17](extend-extensions.md))
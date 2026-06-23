## Capítulo 58. Escrevendo um Wrapper de Dados Estrangeiro

**Índice**

* [58.1. Funções de Wrapper de Dados Estrangeiro](fdw-functions.md)
* [58.2. Rotinas de Callback de Wrapper de Dados Estrangeiro](fdw-callbacks.md)

+ [58.2.1. Rotinas FDW para varredura de tabelas estrangeiras][(fdw-callbacks.md#FDW-CALLBACKS-SCAN)
+ [58.2.2. Rotinas FDW para varredura de junções estrangeiras][(fdw-callbacks.md#FDW-CALLBACKS-JOIN-SCAN)
+ [58.2.3. Rotinas FDW para planejamento do processamento pós-varredura/junção][(fdw-callbacks.md#FDW-CALLBACKS-UPPER-PLANNING)
+ [58.2.4. Rotinas FDW para atualização de tabelas estrangeiras][(fdw-callbacks.md#FDW-CALLBACKS-UPDATE)
+ [58.2.5. Rotinas FDW para `TRUNCATE`][(fdw-callbacks.md#FDW-CALLBACKS-TRUNCATE)
+ [58.2.6. Rotinas FDW para bloqueio de linhas][(fdw-callbacks.md#FDW-CALLBACKS-ROW-LOCKING)
+ [58.2.7. Rotinas FDW para `EXPLAIN`][(fdw-callbacks.md#FDW-CALLBACKS-EXPLAIN)
+ [58.2.8. Rotinas FDW para `ANALYZE`][(fdw-callbacks.md#FDW-CALLBACKS-ANALYZE)
+ [58.2.9. Rotinas FDW para `IMPORT FOREIGN SCHEMA`][(fdw-callbacks.md#FDW-CALLBACKS-IMPORT)
+ [58.2.10. Rotinas FDW para execução paralela][(fdw-callbacks.md#FDW-CALLBACKS-PARALLEL)
+ [58.2.11. Rotinas FDW para execução assíncrona][(fdw-callbacks.md#FDW-CALLBACKS-ASYNC)
+ [58.2.12. Rotinas FDW para redefinição de caminhos][(fdw-callbacks.md#FDW-CALLBACKS-REPARAMETERIZE-PATHS)

* [58.3. Funções de Ajudas para Wrapper de Dados Estrangeiro](fdw-helpers.md)
* [58.4. Planejamento de Consulta do Wrapper de Dados Estrangeiro](fdw-planning.md)
* [58.5. Bloqueio de Linha em Wrapper de Dados Estrangeiro](fdw-row-locking.md)

Todas as operações em uma tabela estrangeira são manipuladas através de seu wrapper de dados estrangeiro, que consiste em um conjunto de funções que o servidor principal chama. O wrapper de dados estrangeiro é responsável por buscar dados da fonte de dados remota e devolvê-los ao executor do PostgreSQL. Se a atualização de tabelas estrangeiras deve ser suportada, o wrapper também deve lidar com isso. Este capítulo descreve como escrever um novo wrapper de dados estrangeiro.

Os wrappers de dados estrangeiros incluídos na distribuição padrão são boas referências ao tentar escrever a sua própria. Consulte o subdiretório `contrib` da árvore de origem. A página de referência [CREATE FOREIGN DATA WRAPPER](sql-createforeigndatawrapper.md "CREATE FOREIGN DATA WRAPPER") também tem alguns detalhes úteis.

Nota

O padrão SQL especifica uma interface para escrever wrappers de dados externos. No entanto, o PostgreSQL não implementa essa API, porque o esforço para acomodá-la no PostgreSQL seria grande, e a API padrão não ganhou ampla adoção de qualquer maneira.
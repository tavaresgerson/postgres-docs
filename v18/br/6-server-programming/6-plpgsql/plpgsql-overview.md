## 41.1. Visão geral [#](#PLPGSQL-OVERVIEW)

* [41.1.1. Vantagens de usar PL/pgSQL](plpgsql-overview.md#PLPGSQL-ADVANTAGES)
* [41.1.2. Tipos de dados de argumentos e resultados suportados](plpgsql-overview.md#PLPGSQL-ARGS-RESULTS)

PL/pgSQL é uma linguagem procedural carregável para o sistema de banco de dados PostgreSQL. Os objetivos de design do PL/pgSQL foram criar uma linguagem procedural carregável que

* pode ser usado para criar funções, procedimentos e gatilhos,
* adiciona estruturas de controle ao idioma SQL,
* pode realizar cálculos complexos,
* herda todos os tipos, funções, procedimentos e operadores definidos pelo usuário,
* pode ser definido para ser confiável pelo servidor,
* é fácil de usar.

As funções criadas com PL/pgSQL podem ser usadas em qualquer lugar onde funções embutidas poderiam ser usadas. Por exemplo, é possível criar funções de cálculo condicional complexas e, posteriormente, usá-las para definir operadores ou usá-las em expressões de índice.

Em PostgreSQL 9.0 e versões posteriores, o PL/pgSQL é instalado por padrão. No entanto, ainda é um módulo carregável, portanto, administradores que estão preocupados com a segurança podem optar por removê-lo.

### 41.1.1. Vantagens do uso do PL/pgSQL [#](#PLPGSQL-ADVANTAGES)

O SQL é a linguagem que o PostgreSQL e a maioria dos outros bancos de dados relacionais utilizam como linguagem de consulta. É portátil e fácil de aprender. Mas cada declaração SQL deve ser executada individualmente pelo servidor do banco de dados.

Isso significa que sua aplicação cliente deve enviar cada consulta ao servidor do banco de dados, esperar que ela seja processada, receber e processar os resultados, realizar algum cálculo e, em seguida, enviar mais consultas ao servidor. Tudo isso implica em comunicação entre processos e também implicará em sobrecarga de rede se seu cliente estiver em uma máquina diferente do servidor do banco de dados.

Com o PL/pgSQL, você pode agrupar um bloco de cálculo e uma série de consultas *dentro* do servidor de banco de dados, obtendo assim o poder de uma linguagem procedural e a facilidade de uso do SQL, mas com economias consideráveis no sobrecarga de comunicação cliente/servidor.

* Os deslocamentos extras entre o cliente e o servidor são eliminados
* Os resultados intermediários que o cliente não precisa não precisam ser mapeados ou transferidos entre o servidor e o cliente
* Pode-se evitar múltiplas rodadas de análise de consulta

Isso pode resultar em um aumento considerável do desempenho em comparação com uma aplicação que não utiliza funções armazenadas.

Além disso, com PL/pgSQL, você pode usar todos os tipos de dados, operadores e funções do SQL.

### 41.1.2. Tipos de dados de argumento e resultado suportados [#](#PLPGSQL-ARGS-RESULTS)

As funções escritas em PL/pgSQL podem aceitar como argumentos qualquer tipo de dados escalar ou de matriz que o servidor suporte, e podem retornar um resultado de qualquer um desses tipos. Elas também podem aceitar ou retornar qualquer tipo composto (tipo de linha) especificado por nome. É também possível declarar uma função PL/pgSQL como aceitando `record`, o que significa que qualquer tipo composto fará como entrada, ou como retornando `record`, o que significa que o resultado é um tipo de linha cujas colunas são determinadas pela especificação na consulta de chamada, conforme discutido em [Seção 7.2.1.4](queries-table-expressions.md#QUERIES-TABLEFUNCTIONS).

As funções PL/pgSQL podem ser declaradas para aceitar um número variável de argumentos usando o marcador `VARIADIC`. Isso funciona exatamente da mesma maneira que para funções SQL, conforme discutido em [Seção 36.5.6](xfunc-sql.md#XFUNC-SQL-VARIADIC-FUNCTIONS).

As funções PL/pgSQL também podem ser declaradas para aceitar e retornar os tipos polimórficos descritos em [Seção 36.2.5](extend-type-system.md#EXTEND-TYPES-POLYMORPHIC), permitindo, assim, que os tipos de dados reais manipulados pela função variem de chamada para chamada. Exemplos aparecem em [Seção 41.3.1](plpgsql-declarations.md#PLPGSQL-DECLARATION-PARAMETERS).

As funções PL/pgSQL também podem ser declaradas para retornar um "conjunto" (ou tabela) de qualquer tipo de dados que possa ser retornado como uma única instância. Tal função gera sua saída executando `RETURN NEXT` para cada elemento desejado do conjunto de resultados, ou usando `RETURN QUERY` para emitir o resultado da avaliação de uma consulta.

Por fim, uma função PL/pgSQL pode ser declarada para retornar `void` se não tiver um valor de retorno útil. (Alternativamente, ela poderia ser escrita como um procedimento nesse caso.)

As funções PL/pgSQL também podem ser declaradas com parâmetros de saída no lugar de uma especificação explícita do tipo de retorno. Isso não adiciona nenhuma capacidade fundamental à linguagem, mas muitas vezes é conveniente, especialmente para retornar múltiplos valores. A notação `RETURNS TABLE` também pode ser usada no lugar de `RETURNS SETOF`.

Exemplos específicos aparecem em [Seção 41.3.1](plpgsql-declarations.md#PLPGSQL-DECLARATION-PARAMETERS) e [Seção 41.6.1](plpgsql-control-structures.md#PLPGSQL-STATEMENTS-RETURNING).
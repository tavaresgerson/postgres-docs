## Capítulo 9. Funções e Operadores

**Índice**

* [9.1. Operadores Lógicos](functions-logical.md)
* [9.2. Funções e Operadores de Comparação](functions-comparison.md)
* [9.3. Funções e Operadores Matemáticos](functions-math.md)
* [9.4. Funções e Operadores de String](functions-string.md)

+ [9.4.1. `format`](functions-string.md#FUNCTIONS-STRING-FORMAT)

* [9.5. Funções e operadores de string binária](functions-binarystring.md)
* [9.6. Funções e operadores de string de bits](functions-bitstring.md)
* [9.7. Contagem de padrões](functions-matching.md)

+ [9.7.1. `LIKE`](functions-matching.md#FUNCTIONS-LIKE)
+ [9.7.2. `SIMILAR TO` Expressões Regulares](functions-matching.md#FUNCTIONS-SIMILARTO-REGEXP)
+ [9.7.3. Expressões Regulares POSIX](functions-matching.md#FUNCTIONS-POSIX-REGEXP)

* [9.8. Funções de formatação de tipo de dados](functions-formatting.md)
* [9.9. Funções e operadores de data/hora](functions-datetime.md)

+ [9.9.1. `EXTRACT`, `date_part`](functions-datetime.md#FUNCTIONS-DATETIME-EXTRACT)
+ [9.9.2. `date_trunc`](functions-datetime.md#FUNCTIONS-DATETIME-TRUNC)
+ [9.9.3. `date_bin`](functions-datetime.md#FUNCTIONS-DATETIME-BIN)
+ [9.9.4. `AT TIME ZONE` e `AT LOCAL`](functions-datetime.md#FUNCTIONS-DATETIME-ZONECONVERT)
+ [9.9.5. Data/Hora Atual](functions-datetime.md#FUNCTIONS-DATETIME-CURRENT)
+ [9.9.6. Atrasos na Execução](functions-datetime.md#FUNCTIONS-DATETIME-DELAY)

* [9.10. Funções de suporte de enumeração](functions-enum.md)]
* [9.11. Funções e operadores geométricos](functions-geometry.md)]
* [9.12. Funções e operadores de endereço de rede](functions-net.md)]
* [9.13. Funções e operadores de busca de texto](functions-textsearch.md)]
* [9.14. Funções UUID](functions-uuid.md)]
* [9.15. Funções XML](functions-xml.md)

+ [9.15.1. Produção de conteúdo XML](functions-xml.md#FUNCTIONS-PRODUCING-XML)
+ [9.15.2. Predicados XML](functions-xml.md#FUNCTIONS-XML-PREDICATES)
+ [9.15.3. Processamento de XML](functions-xml.md#FUNCTIONS-XML-PROCESSING)
+ [9.15.4. Mapeamento de tabelas para XML](functions-xml.md#FUNCTIONS-XML-MAPPING)

* [9.16. Funções e operadores JSON](functions-json.md)

+ [9.16.1. Processamento e criação de dados JSON](functions-json.md#FUNCTIONS-JSON-PROCESSING)
+ [9.16.2. A linguagem de caminho SQL/JSON](functions-json.md#FUNCTIONS-SQLJSON-PATH)
+ [9.16.3. Funções de consulta SQL/JSON](functions-json.md#SQLJSON-QUERY-FUNCTIONS)
+ [9.16.4. JSON_TABLE](functions-json.md#FUNCTIONS-SQLJSON-TABLE)

* [9.17. Funções de Manipulação de Sequência](functions-sequence.md)
* [9.18. Expressões Condicionais](functions-conditional.md)

+ [9.18.1. `CASE`](functions-conditional.md#FUNCTIONS-CASE)
+ [9.18.2. `COALESCE`](functions-conditional.md#FUNCTIONS-COALESCE-NVL-IFNULL)
+ [9.18.3. `NULLIF`](functions-conditional.md#FUNCTIONS-NULLIF)
+ [9.18.4. `GREATEST` e `LEAST`](functions-conditional.md#FUNCTIONS-GREATEST-LEAST)

* [9.19. Funções e Operadores de Array](functions-array.md)
* [9.20. Funções e Operadores de Gama/Múltiplo Gama](functions-range.md)
* [9.21. Funções Agregadas](functions-aggregate.md)
* [9.22. Funções de Janela](functions-window.md)
* [9.23. Funções de Suporte de Fusão](functions-merge-support.md)
* [9.24. Expressões de Subconsultas](functions-subquery.md)

+ [9.24.1. `EXISTS`](functions-subquery.md#FUNCTIONS-SUBQUERY-EXISTS)
+ [9.24.2. `IN`](functions-subquery.md#FUNCTIONS-SUBQUERY-IN)
+ [9.24.3. `NOT IN`](functions-subquery.md#FUNCTIONS-SUBQUERY-NOTIN)
+ [9.24.4. `ANY`/`SOME`](functions-subquery.md#FUNCTIONS-SUBQUERY-ANY-SOME)
+ [9.24.5. `ALL`](functions-subquery.md#FUNCTIONS-SUBQUERY-ALL)
+ [9.24.6. Comparação de uma única linha](functions-subquery.md#FUNCTIONS-SUBQUERY-SINGLE-ROW-COMP)

* [9.25. Comparação de linhas e arrays](functions-comparisons.md)

+ [9.25.1. `IN`](functions-comparisons.md#FUNCTIONS-COMPARISONS-IN-SCALAR)
+ [9.25.2. `NOT IN`](functions-comparisons.md#FUNCTIONS-COMPARISONS-NOT-IN)
+ [9.25.3. `ANY`/`SOME` (matriz)(functions-comparisons.md#FUNCTIONS-COMPARISONS-ANY-SOME)
+ [9.25.4. `ALL` (matriz)(functions-comparisons.md#FUNCTIONS-COMPARISONS-ALL)
+ [9.25.5. Comparação do construtor de linhas](functions-comparisons.md#ROW-WISE-COMPARISON)
+ [9.25.6. Comparação de tipos compostos](functions-comparisons.md#COMPOSITE-TYPE-COMPARISON)

* [9.26. Definir funções de retorno](functions-srf.md)
* [9.27. Funções e operadores de informações do sistema](functions-info.md)

+ [9.27.1. Funções de Informações de Sessão](functions-info.md#FUNCTIONS-INFO-SESSION)
+ [9.27.2. Funções de Consultas de Privilegios de Acesso](functions-info.md#FUNCTIONS-INFO-ACCESS)
+ [9.27.3. Funções de Consultas de Visibilidade do Esquema](functions-info.md#FUNCTIONS-INFO-SCHEMA)
+ [9.27.4. Funções de Informações do Catálogo do Sistema](functions-info.md#FUNCTIONS-INFO-CATALOG)
+ [9.27.5. Funções de Informações e Endereçamento de Objetos](functions-info.md#FUNCTIONS-INFO-OBJECT)
+ [9.27.6. Funções de Informações de Comentários](functions-info.md#FUNCTIONS-INFO-COMMENT)
+ [9.27.7. Funções de Verificação da Validade dos Dados](functions-info.md#FUNCTIONS-INFO-VALIDITY)
+ [9.27.8. Funções de ID de Transação e Informações de Escaneamento](functions-info.md#FUNCTIONS-INFO-SNAPSHOT)
+ [9.27.9. Funções de Informações de Transação Comprovada](functions-info.md#FUNCTIONS-INFO-COMMIT-TIMESTAMP)
+ [9.27.10. Funções de Dados de Controle](functions-info.md#FUNCTIONS-INFO-CONTROLDATA)
+ [9.27.11. Funções de Informações de Versão](functions-info.md#FUNCTIONS-INFO-VERSION)
+ [9.27.12. Funções de Informações de Resumo do WAL](functions-info.md#FUNCTIONS-INFO-WAL-SUMMARY)

* [9.28. Funções de Administração de Sistema](functions-admin.md)

+ [9.28.1. Funções de Configurações de Configuração](functions-admin.md#FUNCTIONS-ADMIN-SET)
+ [9.28.2. Funções de Sinalização do Servidor](functions-admin.md#FUNCTIONS-ADMIN-SIGNAL)
+ [9.28.3. Funções de Controle de Backup](functions-admin.md#FUNCTIONS-ADMIN-BACKUP)
+ [9.28.4. Funções de Controle de Recuperação](functions-admin.md#FUNCTIONS-RECOVERY-CONTROL)
+ [9.28.5. Funções de Sincronização de Instantâneo](functions-admin.md#FUNCTIONS-SNAPSHOT-SYNCHRONIZATION)
+ [9.28.6. Funções de Gerenciamento de Replicação](functions-admin.md#FUNCTIONS-REPLICATION)
+ [9.28.7. Funções de Gerenciamento de Objeto de Banco de Dados](functions-admin.md#FUNCTIONS-ADMIN-DBOBJECT)
+ [9.28.8. Funções de Manutenção de Índices](functions-admin.md#FUNCTIONS-ADMIN-INDEX)
+ [9.28.9. Funções de Acesso Genérico a Arquivo](functions-admin.md#FUNCTIONS-ADMIN-GENFILE)
+ [9.28.10. Funções de Fechamento Consultivo](functions-admin.md#FUNCTIONS-ADVISORY-LOCKS)

* [9.29. Funções de gatilho](functions-trigger.md)
* [9.30. Funções de gatilho de evento](functions-event-triggers.md)

+ [9.30.1. Captura de alterações no final do comando](functions-event-triggers.md#PG-EVENT-TRIGGER-DDL-COMMAND-END-FUNCTIONS)
+ [9.30.2. Processamento de objetos descartados por um comando DDL](functions-event-triggers.md#PG-EVENT-TRIGGER-SQL-DROP-FUNCTIONS)
+ [9.30.3. Tratamento de um evento de reescrita de tabela](functions-event-triggers.md#PG-EVENT-TRIGGER-TABLE-REWRITE-FUNCTIONS)

* [9.31. Funções de Informação Estatística](functions-statistics.md)

+ [9.31.1. Inspeção de listas de MCV](functions-statistics.md#FUNCTIONS-STATISTICS-MCV)

O PostgreSQL oferece um grande número de funções e operadores para os tipos de dados embutidos. Este capítulo descreve a maioria deles, embora funções especiais adicionais apareçam em seções relevantes do manual. Os usuários também podem definir suas próprias funções e operadores, conforme descrito em [Parte V](server-programming.md). Os comandos psql `\df` e `\do` podem ser usados para listar todas as funções e operadores disponíveis, respectivamente.

A notação usada ao longo deste capítulo para descrever os tipos de dados de argumento e resultado de uma função ou operador é a seguinte:

```
repeat ( text, integer ) → text
```

que diz que a função `repeat` recebe um argumento de texto e um inteiro e retorna um resultado do tipo texto. A seta para a direita também é usada para indicar o resultado de um exemplo, assim:

```
repeat('Pg', 4) → PgPgPgPg
```

Se você está preocupado com a portabilidade, note que a maioria das funções e operadores descritos neste capítulo, com exceção dos operadores aritméticos e de comparação mais triviais e algumas funções explicitamente marcadas, não são especificados pelo padrão SQL. Parte dessa funcionalidade estendida está presente em outros sistemas de gerenciamento de banco de dados SQL, e, em muitos casos, essa funcionalidade é compatível e consistente entre as várias implementações.
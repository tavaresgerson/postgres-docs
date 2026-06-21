## Capítulo 34. ECPG — SQL embutido em C

**Índice**

* [34.1. O Conceito](ecpg-concept.md)
* [34.2. Gerenciamento de Conexões de Banco de Dados](ecpg-connect.md)

+ [34.2.1. Conectar ao servidor de banco de dados](ecpg-connect.md#ECPG-CONNECTING)
+ [34.2.2. Escolher uma conexão](ecpg-connect.md#ECPG-SET-CONNECTION)
+ [34.2.3. Fechar uma conexão](ecpg-connect.md#ECPG-DISCONNECT)

* [34.3. Executando comandos SQL](ecpg-commands.md)

+ [34.3.1. Elaboração de instruções SQL](ecpg-commands.md#ECPG-EXECUTING)
+ [34.3.2. Uso de cursor](ecpg-commands.md#ECPG-CURSORS)
+ [34.3.3. Gerenciamento de transações](ecpg-commands.md#ECPG-TRANSACTIONS)
+ [34.3.4. Elaboração preparada](ecpg-commands.md#ECPG-PREPARED)

* [34.4. Usando variáveis de hospedagem](ecpg-variables.md)

+ [34.4.1. Visão geral](ecpg-variables.md#ECPG-VARIABLES-OVERVIEW)
+ [34.4.2. Declarar seções](ecpg-variables.md#ECPG-DECLARE-SECTIONS)
+ [34.4.3. Recuperação de resultados de consulta](ecpg-variables.md#ECPG-RETRIEVING)
+ [34.4.4. Mapeamento de tipos de dados SQL não primitivos](ecpg-variables.md#ECPG-VARIABLES-TYPE-MAPPING)
+ [34.4.5. Tratamento de tipos de dados SQL não primitivos](ecpg-variables.md#ECPG-VARIABLES-NONPRIMITIVE-SQL)
+ [34.4.6. Indicadores](ecpg-variables.md#ECPG-INDICATORS)

* [34.5. SQL dinâmico](ecpg-dynamic.md)

+ [34.5.1. Executar declarações sem um conjunto de resultados](ecpg-dynamic.md#ECPG-DYNAMIC-WITHOUT-RESULT)
+ [34.5.2. Executar uma declaração com parâmetros de entrada](ecpg-dynamic.md#ECPG-DYNAMIC-INPUT)
+ [34.5.3. Executar uma declaração com um conjunto de resultados](ecpg-dynamic.md#ECPG-DYNAMIC-WITH-RESULT)

* [34.6. Biblioteca pgtypes](ecpg-pgtypes.md)

+ [34.6.1. Strings de caractere](ecpg-pgtypes.md#ECPG-PGTYPES-CSTRINGS)
+ [34.6.2. O tipo numérico](ecpg-pgtypes.md#ECPG-PGTYPES-NUMERIC)
+ [34.6.3. O tipo de data](ecpg-pgtypes.md#ECPG-PGTYPES-DATE)
+ [34.6.4. O tipo de marca de tempo](ecpg-pgtypes.md#ECPG-PGTYPES-TIMESTAMP)
+ [34.6.5. O tipo de intervalo](ecpg-pgtypes.md#ECPG-PGTYPES-INTERVAL)
+ [34.6.6. O tipo decimal](ecpg-pgtypes.md#ECPG-PGTYPES-DECIMAL)
+ [34.6.7. Valores de errno de pgtypeslib](ecpg-pgtypes.md#ECPG-PGTYPES-ERRNO)
+ [34.6.8. Constantes especiais de pgtypeslib](ecpg-pgtypes.md#ECPG-PGTYPES-CONSTANTS)

* [34.7. Usando Áreas de Descrição](ecpg-descriptors.md)

+ [34.7.1. Áreas de Descrição SQL nomeadas](ecpg-descriptors.md#ECPG-NAMED-DESCRIPTORS)
+ [34.7.2. Áreas de Descrição SQL](ecpg-descriptors.md#ECPG-SQLDA-DESCRIPTORS)

* [34.8. Gerenciamento de Erros](ecpg-errors.md)

+ [34.8.1. Retornos de chamada](ecpg-errors.md#ECPG-WHENEVER)
+ [34.8.2. sqlca](ecpg-errors.md#ECPG-SQLCA)
+ [34.8.3. `SQLSTATE` vs. `SQLCODE`[(ecpg-errors.md#ECPG-SQLSTATE-SQLCODE)]

* [34.9. Diretrizes do pré-processador](ecpg-preproc.md)

+ [34.9.1. Incluir arquivos](ecpg-preproc.md#ECPG-INCLUDE)
+ [34.9.2. Diretíves define e undef](ecpg-preproc.md#ECPG-DEFINE)
+ [34.9.3. Diretíves ifdef, ifndef, elif, else e endif](ecpg-preproc.md#ECPG-IFDEF)

* [34.10. Processamento de programas com SQL embutido](ecpg-process.md)
* [34.11. Funções de biblioteca](ecpg-library.md)
* [34.12. Objetos grandes](ecpg-lo.md)
* [34.13. Aplicações em C++](ecpg-cpp.md)

+ [34.13.1. Alcance das variáveis de host](ecpg-cpp.md#ECPG-CPP-SCOPE)
+ [34.13.2. Desenvolvimento de aplicativos em C++ com módulo C externo](ecpg-cpp.md#ECPG-CPP-AND-C)

* [34.14. Comandos SQL embutidos](ecpg-sql-commands.md)

+ [ALLOCATE DESCRIPTOR](ecpg-sql-allocate-descriptor.md) — alocar uma área de descritor SQL
+ [CONNECT](ecpg-sql-connect.md) — estabelecer uma conexão com o banco de dados
+ [DEALLOCATE DESCRIPTOR](ecpg-sql-deallocate-descriptor.md) — liberar uma área de descritor SQL
+ [DECLARE](ecpg-sql-declare.md) — definir um cursor
+ [DECLARE STATEMENT](ecpg-sql-declare-statement.md) — declarar o identificador de declaração SQL
+ [DESCRIBE](ecpg-sql-describe.md) — obter informações sobre uma declaração preparada ou conjunto de resultados
+ [DISCONNECT](ecpg-sql-disconnect.md) — encerrar uma conexão com o banco de dados
+ [EXECUTE IMMEDIATE](ecpg-sql-execute-immediate.md) — preparar e executar dinamicamente uma declaração
+ [GET DESCRIPTOR](ecpg-sql-get-descriptor.md) — obter informações de uma área de descritor SQL
+ [OPEN](ecpg-sql-open.md) — abrir um cursor dinâmico
+ [PREPARE](ecpg-sql-prepare.md) — preparar uma declaração para execução
+ [SET AUTOCOMMIT](ecpg-sql-set-autocommit.md) — definir o comportamento de autocommit da sessão atual
+ [SET CONNECTION](ecpg-sql-set-connection.md) — selecionar uma conexão com o banco de dados
+ [SET DESCRIPTOR](ecpg-sql-set-descriptor.md) — definir informações em uma área de descritor SQL
+ [TYPE](ecpg-sql-type.md) — definir um novo tipo de dados
+ [VAR](ecpg-sql-var.md) — definir uma variável
+ [WHENEVER](ecpg-sql-whenever.md) — especificar a ação a ser tomada quando uma declaração SQL causa uma condição específica de classe

* [34.15. Modo de compatibilidade Informix](ecpg-informix-compat.md)

+ [34.15.1. Tipos adicionais](ecpg-informix-compat.md#ECPG-INFORMIX-TYPES)
+ [34.15.2. Declarações SQL incorporadas adicionais/faltantes](ecpg-informix-compat.md#ECPG-INFORMIX-STATEMENTS)
+ [34.15.3. Áreas de descritor SQLDA compatíveis com Informix](ecpg-informix-compat.md#ECPG-INFORMIX-SQLDA)
+ [34.15.4. Funções adicionais](ecpg-informix-compat.md#ECPG-INFORMIX-FUNCTIONS)
+ [34.15.5. Constantes adicionais](ecpg-informix-compat.md#ECPG-INFORMIX-CONSTANTS)

* [34.16. Modo de compatibilidade Oracle](ecpg-oracle-compat.md)
* [34.17. Internos](ecpg-develop.md)

Este capítulo descreve o pacote de SQL embutido para PostgreSQL. Foi escrito por Linus Tolke (`<linus@epact.se>`) e Michael Meskes (`<meskes@postgresql.org>`). Originalmente, foi escrito para funcionar com C. Também funciona com C++, mas ainda não reconhece todas as construções do C++.

Essa documentação é bastante incompleta. Mas, como essa interface é padronizada, informações adicionais podem ser encontradas em muitos recursos sobre SQL.
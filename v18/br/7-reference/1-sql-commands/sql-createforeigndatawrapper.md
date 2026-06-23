## CRIAR O WRAPPER DE DADOS ESTRANGEIRO

CREATE FOREIGN DATA WRAPPER — definir um novo wrapper de dados externos

## Sinopse

```
CREATE FOREIGN DATA WRAPPER name
    [ HANDLER handler_function | NO HANDLER ]
    [ VALIDATOR validator_function | NO VALIDATOR ]
    [ OPTIONS ( option 'value' [, ... ] ) ]
```

## Descrição

`CREATE FOREIGN DATA WRAPPER` cria um novo wrapper de dados externos. O usuário que define um wrapper de dados externos se torna seu proprietário.

O nome do wrapper de dados estrangeiros deve ser único dentro do banco de dados.

Somente superusuários podem criar wrappers de dados estrangeiros.

## Parâmetros

*`name`*: O nome do wrapper de dados estrangeiro a ser criado.

`HANDLER handler_function`: *`handler_function`* é o nome de uma função previamente registrada que será chamada para recuperar as funções de execução para tabelas externas. A função de manipulador não deve receber argumentos e seu tipo de retorno deve ser `fdw_handler`.

É possível criar um wrapper de dados estrangeiro sem uma função de manipulador, mas as tabelas estrangeiras que utilizam esse wrapper só podem ser declaradas, não acessadas.

`VALIDATOR validator_function`: *`validator_function`* é o nome de uma função previamente registrada que será chamada para verificar as opções genéricas fornecidas ao wrapper de dados externos, bem como as opções para servidores externos, mapeamentos de usuários e tabelas externas usando o wrapper de dados externos. Se não for especificado nenhuma função validadora ou `NO VALIDATOR`, as opções não serão verificadas no momento da criação. (Os wrappers de dados externos possivelmente ignorarão ou rejeitarão especificações de opções inválidas no momento da execução, dependendo da implementação.) A função validadora deve receber dois argumentos: um do tipo `text[]`, que conterá o array de opções conforme armazenado nos catálogos do sistema, e um do tipo `oid`, que será o OID do catálogo do sistema que contém as opções. O tipo de retorno é ignorado; a função deve relatar opções inválidas usando a função `ereport(ERROR)`.

`OPTIONS ( option 'value' [, ... ] )`: Esta cláusula especifica as opções para o novo wrapper de dados externos. Os nomes e valores permitidos são específicos para cada wrapper de dados externos e são validados usando a função de validação do wrapper de dados externos. Os nomes das opções devem ser exclusivos.

## Notas

A funcionalidade de dados externos do PostgreSQL ainda está em desenvolvimento ativo. A otimização de consultas é primitiva (e, na maioria das vezes, é deixada para o wrapper também). Assim, há um espaço considerável para melhorias futuras de desempenho.

## Exemplos

Crie um wrapper de dados estrangeiros inútil `dummy`:

```
CREATE FOREIGN DATA WRAPPER dummy;
```

Crie um wrapper de dados estrangeiros `file` com a função de manipulador `file_fdw_handler`:

```
CREATE FOREIGN DATA WRAPPER file HANDLER file_fdw_handler;
```

Crie um wrapper de dados estrangeiros `mywrapper` com algumas opções:

```
CREATE FOREIGN DATA WRAPPER mywrapper
    OPTIONS (debug 'true');
```

## Compatibilidade

`CREATE FOREIGN DATA WRAPPER` está em conformidade com a ISO/IEC 9075-9 (SQL/MED), com a exceção de que as cláusulas `HANDLER` e `VALIDATOR` são extensões e as cláusulas padrão `LIBRARY` e `LANGUAGE` não são implementadas no PostgreSQL.

Observe, no entanto, que a funcionalidade SQL/MED como um todo ainda não está em conformidade.

## Veja também

[WRAPPER DE DADOS EXTERNO](sql-alterforeigndatawrapper.md "ALTER FOREIGN DATA WRAPPER"), [DROP WRAPPER DE DADOS EXTERNO](sql-dropforeigndatawrapper.md "DROP FOREIGN DATA WRAPPER"), [Criação de SERVIDOR](sql-createserver.md "CREATE SERVER"), [MAPEAMENTO DE USUÁRIO CRIADO](sql-createusermapping.md "CREATE USER MAPPING"), [TABELA DE DADOS EXTERNO CRIADA](sql-createforeigntable.md "CREATE FOREIGN TABLE")
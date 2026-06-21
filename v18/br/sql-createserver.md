## CRIAR SERVIDOR

CREATE SERVER — definir um novo servidor externo

## Sinopse

```
CREATE SERVER [ IF NOT EXISTS ] server_name [ TYPE 'server_type' ] [ VERSION 'server_version' ]
    FOREIGN DATA WRAPPER fdw_name
    [ OPTIONS ( option 'value' [, ... ] ) ]
```

## Descrição

`CREATE SERVER` define um novo servidor estrangeiro. O usuário que define o servidor se torna seu proprietário.

Um servidor estrangeiro geralmente encapsula as informações de conexão que um wrapper de dados estrangeiro usa para acessar um recurso de dados externo. Informações de conexão adicionais específicas para o usuário podem ser especificadas por meio de mapeamentos de usuário.

O nome do servidor deve ser único dentro do banco de dados.

Para criar um servidor, é necessário o privilégio `USAGE` no wrapper de dados externos que está sendo utilizado.

## Parâmetros

`IF NOT EXISTS`: Não exija um erro se um servidor com o mesmo nome já existir. Neste caso, é emitido um aviso. Observe que não há garantia de que o servidor existente seja algo parecido com o que teria sido criado.

*`server_name`*: O nome do servidor estrangeiro a ser criado.

*`server_type`*: Tipo de servidor opcional, potencialmente útil para wrappers de dados estrangeiros.

*`server_version`*: Versão opcional do servidor, potencialmente útil para wrappers de dados estrangeiros.

*`fdw_name`*: O nome do wrapper de dados estrangeiro que gerencia o servidor.

`OPTIONS ( option 'value' [, ... ] )`: Esta cláusula especifica as opções para o servidor. As opções definem normalmente os detalhes de conexão do servidor, mas os nomes e valores reais dependem do wrapper de dados externos do servidor.

## Notas

Ao usar o módulo [dblink][(dblink.md "F.11. dblink — connect to other PostgreSQL databases")], o nome de um servidor externo pode ser usado como argumento da função [dblink_connect][(contrib-dblink-connect.md "dblink_connect")] para indicar os parâmetros de conexão. É necessário ter o privilégio `USAGE` no servidor externo para poder usá-lo dessa maneira.

Se o servidor estrangeiro suportar o pushdown de classificação, é necessário que ele tenha a mesma ordem de classificação do servidor local.

## Exemplos

Crie um servidor `myserver` que utilize o wrapper de dados externos `postgres_fdw`:

```
CREATE SERVER myserver FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host 'foo', dbname 'foodb', port '5432');
```

Veja [postgres_fdw](postgres-fdw.md "F.38. postgres_fdw — access data stored in external PostgreSQL servers") para mais detalhes.

## Compatibilidade

`CREATE SERVER` está em conformidade com a ISO/IEC 9075-9 (SQL/MED).

## Veja também

[ALTERAR SERVIDOR](sql-alterserver.md "ALTER SERVER"), [DROP SERVIDOR](sql-dropserver.md "DROP SERVER"), [CREATE WRAPPER DE DADOS ESTRANGEIRO](sql-createforeigndatawrapper.md "CREATE FOREIGN DATA WRAPPER"), [CREATE Tabela DE DADOS ESTRANGEIRO](sql-createforeigntable.md "CREATE FOREIGN TABLE"), [MAPEAR USUÁRIO](sql-createusermapping.md "CREATE USER MAPPING")
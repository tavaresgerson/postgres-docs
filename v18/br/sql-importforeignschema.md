## IMPORTAR SCHEMA EXTERNO

IMPORTAR ESCELA EXTERNA — importar definições de tabela de um servidor externo

## Sinopse

```
IMPORT FOREIGN SCHEMA remote_schema
    [ { LIMIT TO | EXCEPT } ( table_name [, ...] ) ]
    FROM SERVER server_name
    INTO local_schema
    [ OPTIONS ( option 'value' [, ... ] ) ]
```

## Descrição

`IMPORT FOREIGN SCHEMA` cria tabelas externas que representam tabelas existentes em um servidor externo. As novas tabelas externas serão de propriedade do usuário que emite o comando e são criadas com as definições e opções corretas de coluna para corresponder às tabelas remotas.

Por padrão, todas as tabelas e visualizações existentes em um esquema específico no servidor externo são importadas. Opcionalmente, a lista de tabelas pode ser limitada a um subconjunto especificado, ou tabelas específicas podem ser excluídas. As novas tabelas externas são criadas em todos os esquemas de destino, que já devem existir.

Para usar `IMPORT FOREIGN SCHEMA`, o usuário deve ter privilégio `USAGE` no servidor estrangeiro, bem como privilégio `CREATE` no esquema de destino.

## Parâmetros

*`remote_schema`*: O esquema remoto a ser importado. O significado específico de um esquema remoto depende do wrapper de dados estrangeiro em uso.

`LIMIT TO ( table_name [, ...] )`: Importe apenas tabelas estrangeiras que correspondam a um dos nomes de tabela fornecidos. As outras tabelas existentes no esquema estrangeiro serão ignoradas.

`EXCEPT ( table_name [, ...] )`: Exclua as tabelas estrangeiras especificadas da importação. Todas as tabelas existentes no esquema estrangeiro serão importadas, exceto as listadas aqui.

*`server_name`*: O servidor estrangeiro a ser importado.

*`local_schema`*: O esquema no qual as tabelas estrangeiras importadas serão criadas.

`OPTIONS ( option 'value' [, ...] )`: Opções a serem usadas durante a importação. Os nomes e valores das opções permitidas são específicos para cada wrapper de dados estrangeiro.

## Exemplos

Importe as definições da tabela de um esquema remoto `foreign_films` no servidor `film_server`, criando as tabelas externas no esquema local `films`:

```
IMPORT FOREIGN SCHEMA foreign_films
    FROM SERVER film_server INTO films;
```

Como acima, mas importe apenas as duas tabelas `actors` e `directors` (se existirem):

```
IMPORT FOREIGN SCHEMA foreign_films LIMIT TO (actors, directors)
    FROM SERVER film_server INTO films;
```

## Compatibilidade

O comando `IMPORT FOREIGN SCHEMA` está de acordo com o padrão SQL, exceto que a cláusula `OPTIONS` é uma extensão do PostgreSQL.

## Veja também

[Crie uma tabela estrangeira](sql-createforeigntable.md "CREATE FOREIGN TABLE"), [Crie servidor][(sql-createserver.md "CREATE SERVER")
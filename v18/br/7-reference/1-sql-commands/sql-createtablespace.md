## CRIAR TABLESPACE

CREATE TABLESPACE — definir um novo tablespace

## Sinopse

```
CREATE TABLESPACE tablespace_name
    [ OWNER { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER } ]
    LOCATION 'directory'
    [ WITH ( tablespace_option = value [, ... ] ) ]
```

## Descrição

`CREATE TABLESPACE` registra um novo espaço de tabela em nível de grupo. O nome do espaço de tabela deve ser distinto do nome de qualquer espaço de tabela existente no grupo de bancos de dados.

Um espaço de tabela permite que os superusuários definam um local alternativo no sistema de arquivos onde os arquivos de dados que contêm objetos do banco de dados (como tabelas e índices) podem residir.

Um usuário com privilégios apropriados pode passar *`tablespace_name`* para `CREATE DATABASE`, `CREATE TABLE`, `CREATE INDEX` ou `ADD CONSTRAINT` para ter os arquivos de dados desses objetos armazenados dentro do espaço de tabela especificado.

### Aviso

Um espaço de tabela não pode ser usado de forma independente do clúster no qual é definido; veja [Seção 22.6](manage-ag-tablespaces.md).

## Parâmetros

*`tablespace_name`*: O nome do tablespace a ser criado. O nome não pode começar com `pg_`, pois tais nomes são reservados para tablespaces de tabelas do sistema.

*`user_name`*: O nome do usuário que possuirá o espaço de tabelas. Se omitido, o padrão é o usuário que executa o comando. Apenas usuários superusuários podem criar espaços de tabelas, mas eles podem atribuir a propriedade dos espaços de tabelas a usuários não superusuários.

*`directory`*: O diretório que será utilizado para o espaço de tabela. O diretório deve existir (`CREATE TABLESPACE` não o criará), deve estar vazio e deve ser de propriedade do usuário do sistema PostgreSQL. O diretório deve ser especificado por um nome de caminho absoluto.

*`tablespace_option`*: Um parâmetro de espaço de tabelas a ser definido ou redefinido. Atualmente, os únicos parâmetros disponíveis são `seq_page_cost`, `random_page_cost`, `effective_io_concurrency` e `maintenance_io_concurrency`. Definir esses valores para um espaço de tabelas específico substituirá a estimativa usual do planejador do custo de leitura de páginas de tabelas nesse espaço de tabelas, e quantas operações de E/S concorrentes são emitidas, conforme estabelecido pelos parâmetros de configuração do mesmo nome (consulte [seq_page_cost](runtime-config-query.md#GUC-SEQ-PAGE-COST), [random_page_cost](runtime-config-query.md#GUC-RANDOM-PAGE-COST), [effective_io_concurrency](runtime-config-resource.md#GUC-EFFECTIVE-IO-CONCURRENCY), [maintenance_io_concurrency](runtime-config-resource.md#GUC-MAINTENANCE-IO-CONCURRENCY)). Isso pode ser útil se um espaço de tabelas estiver localizado em um disco que é mais rápido ou mais lento que o restante do subsistema de E/S.

## Notas

`CREATE TABLESPACE` não pode ser executado dentro de um bloco de transação.

## Exemplos

Para criar um espaço de tabela `dbspace` na localização do sistema de arquivos `/data/dbs`, primeiro crie o diretório usando as facilidades do sistema operacional e defina a propriedade correta:

```
mkdir /data/dbs
chown postgres:postgres /data/dbs
```

Em seguida, emita o comando de criação do tablespace dentro do PostgreSQL:

```
CREATE TABLESPACE dbspace LOCATION '/data/dbs';
```

Para criar um espaço de tabela de propriedade de um usuário de banco de dados diferente, use um comando como este:

```
CREATE TABLESPACE indexspace OWNER genevieve LOCATION '/data/indexes';
```

## Compatibilidade

`CREATE TABLESPACE` é uma extensão do PostgreSQL.

## Veja também

[CREATE DATABASE](sql-createdatabase.md "CREATE DATABASE"), [CREATE TABLE](sql-createtable.md "CREATE TABLE"), [CREATE INDEX](sql-createindex.md "CREATE INDEX"), [DROP TABLESPACE](sql-droptablespace.md "DROP TABLESPACE"), [ALTER TABLESPACE](sql-altertablespace.md "ALTER TABLESPACE")
## 22.1. Visão geral [#](#MANAGE-AG-OVERVIEW)

Um pequeno número de objetos, como nomes de role, banco de dados e tablespace, são definidos no nível do clúster e armazenados no tablespace `pg_global`. Dentro do clúster existem vários bancos de dados, que são isolados uns dos outros, mas podem acessar objetos de nível de clúster. Dentro de cada banco de dados existem vários esquemas, que contêm objetos como tabelas e funções. Portanto, a hierarquia completa é: clúster, banco de dados, esquema, tabela (ou algum outro tipo de objeto, como uma função).

Ao se conectar ao servidor de banco de dados, o cliente deve especificar o nome do banco de dados em sua solicitação de conexão. Não é possível acessar mais de um banco de dados por conexão. No entanto, os clientes podem abrir múltiplas conexões para o mesmo banco de dados ou diferentes bancos de dados. A segurança em nível de banco de dados tem dois componentes: controle de acesso (consulte [Seção 20.1] [(auth-pg-hba-conf.md "20.1. The pg_hba.conf File")]), gerenciado no nível da conexão, e controle de autorização (consulte [Seção 5.8] [(ddl-priv.md "5.8. Privileges")]), gerenciado via sistema de concessão. Os wrappers de dados externos (consulte [postgres_fdw] [(postgres-fdw.md "F.38. postgres_fdw — access data stored in external PostgreSQL servers")]) permitem que objetos dentro de um banco de dados atuem como proxies para objetos em outros bancos de dados ou clusters. O módulo dblink mais antigo (consulte [dblink] [(dblink.md "F.11. dblink — connect to other PostgreSQL databases")]) oferece uma capacidade semelhante. Por padrão, todos os usuários podem se conectar a todos os bancos de dados usando todos os métodos de conexão.

Se um clúster de servidores PostgreSQL for planejado para conter projetos ou usuários não relacionados que, na maior parte das vezes, não devem estar cientes uns dos outros, é recomendável colocá-los em bancos de dados separados e ajustar as autorizações e controles de acesso de acordo. Se os projetos ou usuários estiverem inter-relacionados e, portanto, devem ser capazes de usar os recursos uns dos outros, eles devem ser colocados no mesmo banco de dados, mas provavelmente em esquemas separados; isso fornece uma estrutura modular com isolamento de namespace e controle de autorização. Mais informações sobre a gestão de esquemas estão em [Seção 5.10][(ddl-schemas.md "5.10. Schemas")].

Embora múltiplas bases de dados possam ser criadas dentro de um único clúster, é aconselhável considerar cuidadosamente se os benefícios superam os riscos e as limitações. Em particular, o impacto que ter um WAL compartilhado (ver [Capítulo 28] [(wal.md "Chapter 28. Reliability and the Write-Ahead Log")]) tem nas opções de backup e recuperação. Embora as bases de dados individuais no clúster sejam isoladas quando consideradas da perspectiva do usuário, elas estão intimamente ligadas do ponto de vista do administrador de banco de dados.

Os bancos de dados são criados com o comando `CREATE DATABASE` (consulte [Seção 22.2][(manage-ag-createdb.md "22.2. Creating a Database")]) e destruídos com o comando `DROP DATABASE` (consulte [Seção 22.5][(manage-ag-dropdb.md "22.5. Destroying a Database")]). Para determinar o conjunto de bancos de dados existentes, examine o catálogo do sistema `pg_database`, por exemplo

```
SELECT datname FROM pg_database;
```

O comando meta (app-psql.md "psql") do programa [psql][(app-psql.md "psql")] e a opção de linha de comando `\l` também são úteis para listar os bancos de dados existentes.

### Nota

O padrão SQL chama os bancos de dados de "catálogos", mas na prática não há diferença.
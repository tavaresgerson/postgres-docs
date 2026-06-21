## 22.2. Criando um banco de dados [#](#MANAGE-AG-CREATEDB)

Para criar um banco de dados, o servidor PostgreSQL deve estar ativo e funcionando (consulte [Seção 18.3][(server-start.md "18.3. Starting the Database Server")]).

Os bancos de dados são criados com o comando SQL [CREATE DATABASE](sql-createdatabase.md "CREATE DATABASE"):

```
CREATE DATABASE name;
```

onde *`name`* segue as regras usuais para identificadores SQL. O papel atual automaticamente se torna o proprietário do novo banco de dados. É o privilégio do proprietário de um banco de dados remover-lo posteriormente (o que também remove todos os objetos nele, mesmo que tenham um proprietário diferente).

A criação de bancos de dados é uma operação restrita. Veja [Seção 21.2][(role-attributes.md "21.2. Role Attributes")] para saber como conceder permissão.

Como você precisa estar conectado ao servidor do banco de dados para executar o comando `CREATE DATABASE`, a questão permanece sobre como o *primeiro* banco de dados em qualquer local pode ser criado. O primeiro banco de dados é sempre criado pelo comando `initdb` quando a área de armazenamento de dados é inicializada. (Veja [Seção 18.2][(creating-cluster.md "18.2. Creating a Database Cluster")]. Este banco de dados é chamado `postgres`. Portanto, para criar o primeiro banco de dados "ordinário", você pode se conectar ao `postgres`.

Dois bancos de dados adicionais, `template1` e `template0`, também são criados durante a inicialização do grupo de bancos de dados. Sempre que um novo banco de dados é criado dentro do grupo, `template1` é essencialmente clonado. Isso significa que quaisquer alterações que você fizer em `template1` são propagadas para todos os bancos de dados posteriormente criados. Por isso, evite criar objetos em `template1` a menos que você queira que eles sejam propagados para todos os bancos de dados recém-criados. `template0` é destinado como uma cópia pura do conteúdo original de `template1`. Pode ser clonado em vez de `template1` quando é importante criar um banco de dados sem quaisquer adições locais. Mais detalhes aparecem em [Seção 22.3][(manage-ag-templatedbs.md "22.3. Template Databases")].

Como uma conveniência, há um programa que você pode executar a partir do shell para criar novos bancos de dados, `createdb`.

```
createdb dbname
```

`createdb` não faz mágica. Ele se conecta ao banco de dados `postgres` e emite o comando `CREATE DATABASE`, exatamente como descrito acima. A página de referência [createdb](app-createdb.md "createdb") contém os detalhes de invocação. Note que `createdb` sem quaisquer argumentos criará um banco de dados com o nome do usuário atual.

### Nota

[Capítulo 20](client-authentication.md "Chapter 20. Client Authentication") contém informações sobre como restringir quem pode se conectar a um banco de dados específico.

Às vezes, você quer criar um banco de dados para outra pessoa, e fazer dela a proprietária do novo banco de dados, para que ela possa configurá-lo e gerenciá-lo por si mesma. Para isso, use um dos seguintes comandos:

```
CREATE DATABASE dbname OWNER rolename;
```

do ambiente SQL, ou:

```
createdb -O rolename dbname
```

a partir da concha. Apenas o superusuário pode criar um banco de dados para outra pessoa (ou seja, para um papel do qual você não é membro).
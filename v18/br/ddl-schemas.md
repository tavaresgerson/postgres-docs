## 5.10. Esquemas [#](#DDL-SCHEMAS)

* [5.10.1. Criando um Esquema][(ddl-schemas.md#DDL-SCHEMAS-CREATE)]
* [5.10.2. O Esquema Público][(ddl-schemas.md#DDL-SCHEMAS-PUBLIC)]
* [5.10.3. O Caminho de Pesquisa do Esquema][(ddl-schemas.md#DDL-SCHEMAS-PATH)]
* [5.10.4. Esquemas e Privilegios][(ddl-schemas.md#DDL-SCHEMAS-PRIV)]
* [5.10.5. O Esquema do Catálogo do Sistema][(ddl-schemas.md#DDL-SCHEMAS-CATALOG)]
* [5.10.6. Padrões de Uso][(ddl-schemas.md#DDL-SCHEMAS-PATTERNS)]
* [5.10.7. Portabilidade][(ddl-schemas.md#DDL-SCHEMAS-PORTABILITY)]

Um clúster de banco de dados PostgreSQL contém um ou mais bancos de dados nomeados. Papéis e alguns outros tipos de objetos são compartilhados em todo o clúster. Uma conexão de cliente com o servidor só pode acessar dados em um único banco de dados, o especificado na solicitação de conexão.

### Nota

Os usuários de um clúster não têm necessariamente o privilégio de acessar todos os bancos de dados no clúster. A partilha de nomes de papéis significa que não podem haver diferentes papéis com nomes, por exemplo, `joe` em dois bancos de dados no mesmo clúster; mas o sistema pode ser configurado para permitir o acesso de `joe` apenas a alguns dos bancos de dados.

Um banco de dados contém um ou mais *schemas* nomeados, que, por sua vez, contêm tabelas. Os schemas também contêm outros tipos de objetos nomeados, incluindo tipos de dados, funções e operadores. Dentro de um esquema, dois objetos do mesmo tipo não podem ter o mesmo nome. Além disso, tabelas, sequências, índices, visualizações, visualizações materializadas e tabelas externas compartilham o mesmo espaço de nomes, de modo que, por exemplo, um índice e uma tabela devem ter nomes diferentes se estiverem no mesmo esquema. O mesmo nome de objeto pode ser usado em diferentes esquemas sem conflito; por exemplo, `schema1` e `myschema` podem conter tabelas nomeadas `mytable`. Ao contrário dos bancos de dados, os schemas não são rigidamente separados: um usuário pode acessar objetos em qualquer um dos schemas no banco de dados ao qual está conectado, se tiver privilégios para fazê-lo.

Há várias razões pelas quais alguém pode querer usar esquemas:

* Permitir que muitos usuários usem um banco de dados sem interferir uns com os outros.
* Organizar os objetos do banco de dados em grupos lógicos para torná-los mais gerenciáveis.
* Aplicativos de terceiros podem ser colocados em esquemas separados para que não colidem com os nomes de outros objetos.

Os esquemas são análogos aos diretórios no nível do sistema operacional, exceto que os esquemas não podem ser aninhados.

### 5.10.1. Criar um Esquema [#](#DDL-SCHEMAS-CREATE)

Para criar um esquema, use o comando [CREATE SCHEMA](sql-createschema.md "CREATE SCHEMA"). Dê ao esquema um nome de sua escolha. Por exemplo:

```
CREATE SCHEMA myschema;
```

Para criar ou acessar objetos em um esquema, escreva um *nome qualificado* que consiste no nome do esquema e no nome da tabela separados por um ponto:

```
schema.table
```

Isso funciona em qualquer lugar onde se espera um nome de tabela, incluindo os comandos de modificação de tabela e os comandos de acesso a dados discutidos nos capítulos seguintes. (Por economia de palavras, falaremos apenas de tabelas, mas as mesmas ideias se aplicam a outros tipos de objetos com nome, como tipos e funções.)

Na verdade, a sintaxe ainda mais geral

```
database.schema.table
```

também pode ser usado, mas atualmente isso é apenas para conformidade pro forma com o padrão SQL. Se você escrever um nome de banco de dados, ele deve ser o mesmo do banco de dados ao qual você está conectado.

Para criar uma tabela no novo esquema, use:

```
CREATE TABLE myschema.mytable (
 ...
);
```

Para descartar um esquema se ele estiver vazio (todos os objetos nele foram descartados), use:

```
DROP SCHEMA myschema;
```

Para descartar um esquema que inclui todos os objetos contidos, use:

```
DROP SCHEMA myschema CASCADE;
```

Veja [Seção 5.15][(ddl-depend.md "5.15. Dependency Tracking")] para uma descrição do mecanismo geral por trás disso.

Muitas vezes, você vai querer criar um esquema de propriedade de outra pessoa (já que essa é uma das maneiras de restringir as atividades dos seus usuários a namespaces bem definidos). A sintaxe para isso é:

```
CREATE SCHEMA schema_name AUTHORIZATION user_name;
```

Você pode até omitir o nome do esquema, nesse caso, o nome do esquema será o mesmo do nome do usuário. Veja [Seção 5.10.6] para saber como isso pode ser útil.

Os nomes de esquema que começam com `pg_` são reservados para fins de sistema e não podem ser criados por usuários.

### 5.10.2. O Esquema Público [#](#DDL-SCHEMAS-PUBLIC)

Nas seções anteriores, criamos tabelas sem especificar quaisquer nomes de esquema. Por padrão, tais tabelas (e outros objetos) são colocados automaticamente em um esquema chamado “public”. Cada nova base de dados contém tal esquema. Assim, o seguinte é equivalente:

```
CREATE TABLE products ( ... );
```

e:

```
CREATE TABLE public.products ( ... );
```

### 5.10.3. O caminho de pesquisa do esquema [#](#DDL-SCHEMAS-PATH)

Os nomes qualificados são tediosos de escrever, e muitas vezes é melhor não inserir um nome específico de esquema em aplicativos de qualquer maneira. Portanto, as tabelas são frequentemente referenciadas por *nomes não qualificados*, que consistem apenas no nome da tabela. O sistema determina qual tabela é a pretendida seguindo um *caminho de busca*, que é uma lista de esquemas a serem verificados. A primeira tabela que corresponde ao caminho de busca é considerada a desejada. Se não houver correspondência no caminho de busca, um erro é relatado, mesmo que nomes de tabelas correspondentes existam em outros esquemas no banco de dados.

A capacidade de criar objetos com nomes semelhantes em diferentes esquemas complica a escrita de uma consulta que faça referência exatamente aos mesmos objetos todas as vezes. Isso também abre o potencial para os usuários alterarem o comportamento das consultas de outros usuários, maliciosamente ou acidentalmente. Devido à prevalência de nomes não qualificados em consultas e ao seu uso nos recursos internos do PostgreSQL, adicionar um esquema ao `search_path` confia efetivamente em todos os usuários que têm privilégio `CREATE` nesse esquema. Quando você executa uma consulta comum, um usuário malicioso capaz de criar objetos em um esquema do seu caminho de pesquisa pode assumir o controle e executar funções SQL arbitrárias como se você as tivesse executado.

O primeiro esquema nomeado no caminho de busca é chamado de esquema atual. Além de ser o primeiro esquema pesquisado, é também o esquema em que novas tabelas serão criadas se o comando `CREATE TABLE` não especificar um nome de esquema.

Para mostrar o caminho de pesquisa atual, use o seguinte comando:

```
SHOW search_path;
```

Na configuração padrão, isso retorna:

```
 search_path
--------------
 "$user", public
```

O primeiro elemento especifica que um esquema com o mesmo nome do usuário atual deve ser pesquisado. Se tal esquema não existir, a entrada é ignorada. O segundo elemento se refere ao esquema público que já vimos.

O primeiro esquema no caminho de busca que existe é o local padrão para criar novos objetos. É por isso que, por padrão, os objetos são criados no esquema público. Quando os objetos são referenciados em qualquer outro contexto sem qualificação de esquema (modificação de tabela, modificação de dados ou comandos de consulta), o caminho de busca é percorrido até que um objeto correspondente seja encontrado. Portanto, na configuração padrão, qualquer acesso não qualificado pode novamente se referir apenas ao esquema público.

Para colocar nosso novo esquema no caminho, usamos:

```
SET search_path TO myschema,public;
```

(Omitimos o `$user` aqui porque não temos necessidade imediata dele.) E, em seguida, podemos acessar a tabela sem qualificação do esquema:

```
DROP TABLE mytable;
```

Além disso, uma vez que `myschema` é o primeiro elemento no caminho, novos objetos seriam criados por padrão nele.

Também poderíamos ter escrito:

```
SET search_path TO myschema;
```

Então, não temos mais acesso ao esquema público sem qualificação explícita. Não há nada de especial sobre o esquema público, exceto que ele existe por padrão. Ele também pode ser descartado.

Veja também [Seção 9.27][(functions-info.md "9.27. System Information Functions and Operators")] para outras maneiras de manipular o caminho de pesquisa do esquema.

O caminho de busca funciona da mesma maneira para nomes de tipos de dados, nomes de funções e nomes de operadores, assim como para nomes de tabelas. Os nomes de tipo de dados e de função podem ser qualificados exatamente da mesma maneira que os nomes de tabelas. Se você precisar escrever um nome de operador qualificado em uma expressão, há uma disposição especial: você deve escrever

```
OPERATOR(schema.operator)
```

Isso é necessário para evitar ambiguidade sintática. Um exemplo é:

```
SELECT 3 OPERATOR(pg_catalog.+) 4;
```

Na prática, geralmente se baseia no caminho de busca para operadores, para não ter que escrever algo tão feio quanto isso.

### 5.10.4. Esquemas e Privilegios [#](#DDL-SCHEMAS-PRIV)

Por padrão, os usuários não podem acessar quaisquer objetos em esquemas que não possuam. Para permitir isso, o proprietário do esquema deve conceder o privilégio `USAGE` no esquema. Por padrão, todos têm esse privilégio no esquema `public`. Para permitir que os usuários usem os objetos em um esquema, podem ser necessários privilégios adicionais, conforme apropriado para o objeto.

Também é possível permitir que um usuário crie objetos em um esquema de outra pessoa. Para permitir isso, o privilégio `CREATE` no esquema precisa ser concedido. Em bancos de dados atualizados a partir do PostgreSQL 14 ou versões anteriores, todos têm esse privilégio no esquema `public`. Alguns [padrões de uso][(ddl-schemas.md#DDL-SCHEMAS-PATTERNS "5.10.6. Usage Patterns")] exigem a revogação desse privilégio:

```
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
```

(O primeiro "público" é o esquema, o segundo "público" significa "todos os usuários". No primeiro sentido, é um identificador, no segundo sentido, é uma palavra-chave, daí a diferenciação da grafia; lembre-se das diretrizes do [Seção 4.1.1][(sql-syntax-lexical.md#SQL-SYNTAX-IDENTIFIERS "4.1.1. Identifiers and Key Words")].])

### 5.10.5. O Esquema do Catálogo do Sistema [#](#DDL-SCHEMAS-CATALOG)

Além dos esquemas criados pelo usuário `public` e `pg_catalog`, cada banco de dados contém um esquema `pg_catalog`, que contém as tabelas do sistema e todos os tipos de dados, funções e operadores embutidos. `pg_catalog` sempre faz parte efetivamente do caminho de busca. Se não for nomeado explicitamente no caminho, ele é pesquisado implicitamente *antes* de pesquisar os esquemas do caminho. Isso garante que os nomes embutidos sempre serão encontrados. No entanto, você pode colocar explicitamente `pg_catalog` no final do seu caminho de busca, se preferir que os nomes definidos pelo usuário substituam os nomes embutidos.

Como os nomes das tabelas do sistema começam com `pg_`, é melhor evitar tais nomes para garantir que você não sofra um conflito se alguma versão futura definir uma tabela do sistema com o mesmo nome que sua tabela. (Com o caminho de busca padrão, uma referência não qualificada ao nome da sua tabela seria resolvida como a tabela do sistema em vez disso.) As tabelas do sistema continuarão a seguir a convenção de ter nomes que começam com `pg_`, para que não haja conflito com nomes de tabela de usuário não qualificados, desde que os usuários evitem o prefixo `pg_`.

### 5.10.6. Padrões de Uso [#](#DDL-SCHEMAS-PATTERNS)

Os esquemas podem ser usados para organizar seus dados de várias maneiras. Um *padrão seguro de uso de esquema* impede que usuários não confiáveis mudem o comportamento das consultas de outros usuários. Quando um banco de dados não usa um padrão seguro de uso de esquema, os usuários que desejam consultar esse banco de dados de forma segura teriam que tomar medidas de proteção no início de cada sessão. Especificamente, eles começariam cada sessão definindo `search_path` como uma string vazia ou, de outra forma, removendo esquemas que são legítimos por usuários não superusuários de `search_path`. Existem alguns padrões de uso facilmente suportados pela configuração padrão:

* Constrinja os usuários comuns a esquemas privados. Para implementar esse padrão, primeiro garanta que nenhum esquema tenha privilégios públicos `CREATE`. Em seguida, para cada usuário que precisa criar objetos não temporários, crie um esquema com o mesmo nome do usuário, por exemplo, `CREATE SCHEMA alice AUTHORIZATION alice`. (Lembre-se de que o caminho de busca padrão começa com `$user`, que resolve para o nome do usuário. Portanto, se cada usuário tiver um esquema separado, eles acessam seus próprios esquemas por padrão.) Esse padrão é um padrão seguro de uso de esquemas, a menos que um usuário não confiável seja o proprietário do banco de dados ou tenha sido concedido `ADMIN OPTION` em um papel relevante, caso em que não existe nenhum padrão seguro de uso de esquemas.

Em PostgreSQL 15 e versões posteriores, a configuração padrão suporta esse padrão de uso. Em versões anteriores ou quando se usa um banco de dados que foi atualizado a partir de uma versão anterior, você precisará remover o privilégio público `CREATE` do esquema `public` (problema `REVOKE CREATE ON SCHEMA public FROM PUBLIC`). Em seguida, considere auditar o esquema `public` para objetos com nomes semelhantes aos do esquema `pg_catalog`.
* Remova o esquema público do caminho de busca padrão, modificando [`postgresql.conf`](config-setting.md#CONFIG-SETTING-CONFIGURATION-FILE "19.1.2. Parameter Interaction via the Configuration File") ou emitindo `ALTER ROLE ALL SET search_path = "$user"`. Em seguida, conceda privilégios para criar no esquema público. Apenas nomes qualificados escolherão objetos do esquema público. Embora referências de tabela qualificadas sejam aceitáveis, chamadas a funções no esquema público [serão inseguras ou não confiáveis](typeconv-func.md "10.3. Functions"). Se você criar funções ou extensões no esquema público, use o primeiro padrão. Caso contrário, como o primeiro padrão, isso é seguro, a menos que um usuário não confiável seja o proprietário do banco de dados ou tenha sido concedido `ADMIN OPTION` em um papel relevante.
* Mantenha o caminho de busca padrão e conceda privilégios para criar no esquema público. Todos os usuários acessam o esquema público implicitamente. Isso simula a situação em que os esquemas não estão disponíveis, proporcionando uma transição suave do mundo não consciente de esquemas. No entanto, esse não é um padrão seguro. É aceitável apenas quando o banco de dados tem um único usuário ou alguns usuários mutuamente confiáveis. Em bancos de dados atualizados a partir do PostgreSQL 14 ou anteriores, isso é o padrão padrão.

Para qualquer padrão, para instalar aplicações compartilhadas (tabelas que serão usadas por todos, funções adicionais fornecidas por terceiros, etc.), coloque-as em esquemas separados. Lembre-se de conceder privilégios apropriados para permitir que os outros usuários acessem-nas. Os usuários podem então se referir a esses objetos adicionais qualificando os nomes com o nome do esquema, ou podem colocar os esquemas adicionais em seu caminho de pesquisa, conforme sua escolha.

### 5.10.7. Portabilidade [#](#DDL-SCHEMAS-PORTABILITY)

No padrão SQL, a noção de objetos no mesmo esquema pertencentes a diferentes usuários não existe. Além disso, algumas implementações não permitem que você crie esquemas que tenham um nome diferente do de seu proprietário. De fato, os conceitos de esquema e usuário são quase equivalentes em um sistema de banco de dados que implementa apenas o suporte básico de esquema especificado no padrão. Portanto, muitos usuários consideram que nomes qualificados realmente consistem em `user_name.table_name`. É assim que o PostgreSQL se comportará efetivamente se você criar um esquema por usuário para cada usuário.

Além disso, não há conceito de esquema `public` no padrão SQL. Para conformidade máxima com o padrão, você não deve usar o esquema `public`.

Claro, alguns sistemas de banco de dados SQL podem não implementar esquemas ou fornecer suporte a namespaces, permitindo (possivelmente limitado) acesso entre bancos. Se você precisar trabalhar com esses sistemas, a máxima portabilidade seria alcançada não usando esquemas.
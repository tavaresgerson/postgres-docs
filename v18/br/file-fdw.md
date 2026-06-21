## F.15. file_fdw — acesso a arquivos de dados no sistema de arquivos do servidor [#](#FILE-FDW)

O módulo `file_fdw` fornece o wrapper de dados externos `file_fdw`, que pode ser usado para acessar arquivos de dados no sistema de arquivos do servidor, ou para executar programas no servidor e ler suas saídas. O arquivo de dados ou a saída do programa deve estar em um formato que possa ser lido por `COPY FROM`; consulte [COPY](sql-copy.md "COPY") para detalhes. O acesso aos arquivos de dados é atualmente apenas de leitura.

Uma tabela estrangeira criada usando este wrapper pode ter as seguintes opções:

`filename`: Especifica o arquivo a ser lido. As passagens relativas são relativas ao diretório de dados. Deve ser especificado `filename` ou `program`, mas não ambos.

`program`: Especifica o comando a ser executado. A saída padrão deste comando será lida como se `COPY FROM PROGRAM` fosse usado. Deve ser especificado `program` ou `filename`, mas não ambos.

`format`: Especifica o formato de dados, o mesmo que a opção `FORMAT` do `COPY`.

`header`: Especifica se os dados têm uma linha de cabeçalho, o mesmo que a opção `COPY` do `HEADER`.

`delimiter`: Especifica o caractere delimitador de dados, o mesmo que a opção `COPY` do `DELIMITER`.

`quote`: Especifica o caractere de citação de dados, o mesmo que a opção `COPY` de `QUOTE`.

`escape`: Especifica o caractere de escape de dados, o mesmo que a opção `COPY` do `ESCAPE`.

`null`: Especifica a cadeia de texto nulo de dados, o mesmo que a opção `NULL` do `COPY`.

`default`: Especifica a string que representa um valor padrão, o mesmo que a opção `COPY` do `DEFAULT`.

`encoding`: Especifica o codificação de dados, o mesmo que a opção `COPY` do `ENCODING`.

`on_error`: Especifica como se comportar ao encontrar um erro ao converter o valor de entrada de uma coluna para seu tipo de dados, o mesmo que a opção `ON_ERROR` de `COPY`.

`reject_limit`: Especifica o número máximo de erros tolerados ao converter o valor de entrada de uma coluna para seu tipo de dados, o mesmo que a opção `REJECT_LIMIT` de `COPY`.

`log_verbosity`: Especifica a quantidade de mensagens emitidas por `file_fdw`, o mesmo que a opção `LOG_VERBOSITY` de `COPY`.

Observe que, embora o `COPY` permita especificar opções como o `HEADER`, sem um valor correspondente, a sintaxe da opção de tabela estrangeira exige que um valor esteja presente em todos os casos. Para ativar as opções do `COPY` normalmente escritas sem um valor, você pode passar o valor VERDADEIRO, uma vez que todas essas opções são Booleans.

Uma coluna de uma tabela estrangeira criada usando este wrapper pode ter as seguintes opções:

`force_not_null`: Esta é uma opção booleana. Se verdadeira, especifica que os valores da coluna não devem ser correspondidos com a string nula (ou seja, a opção `null` do nível de tabela). Isso tem o mesmo efeito que listar a coluna na opção `FORCE_NOT_NULL` de `COPY`.

`force_null`: Esta é uma opção booleana. Se verdadeira, especifica que os valores da coluna que correspondem à string nula são retornados como `NULL`, mesmo que o valor seja citado. Sem esta opção, apenas os valores não citados que correspondem à string nula são retornados como `NULL`. Isso tem o mesmo efeito que listar a coluna na opção `COPY` de `FORCE_NULL`.

A opção `COPY` de `FORCE_QUOTE` atualmente não é suportada por `file_fdw`.

Essas opções só podem ser especificadas para uma tabela estrangeira ou suas colunas, não nas opções do wrapper de dados estrangeiros `file_fdw`, nem nas opções de mapeamento de servidor ou usuário usando o wrapper.

Para alterar as opções de nível de tabela, é necessário ser um superusuário ou ter os privilégios do papel `pg_read_server_files` (para usar um nome de arquivo) ou do papel `pg_execute_server_program` (para usar um programa), por razões de segurança: apenas certos usuários devem ser capazes de controlar qual arquivo é lido ou qual programa é executado. Em princípio, os usuários regulares poderiam ser autorizados a alterar as outras opções, mas isso não é suportado atualmente.

Ao especificar a opção `program`, tenha em mente que a string de opção é executada pelo shell. Se você precisar passar quaisquer argumentos para o comando que vêm de uma fonte não confiável, você deve ter cuidado para remover ou escapar quaisquer caracteres que possam ter um significado especial para o shell. Por razões de segurança, é melhor usar uma string de comando fixa ou, pelo menos, evitar passar qualquer entrada do usuário nela.

Para uma tabela estrangeira que utiliza `file_fdw`, `EXPLAIN` mostra o nome do arquivo a ser lido ou do programa a ser executado. Para um arquivo, a menos que `COSTS OFF` seja especificado, o tamanho do arquivo (em bytes) também é mostrado.

**Exemplo F.1. Criar uma tabela estrangeira para logs CSV do PostgreSQL**

Um dos usos óbvios para `file_fdw` é tornar o log de atividade do PostgreSQL disponível como uma tabela para consulta. Para isso, primeiro você deve estar [registrando em um arquivo CSV,][(runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-CSVLOG "19.8.4. Using CSV-Format Log Output")], que aqui chamaremos de `pglog.csv`. Primeiro, instale `file_fdw` como uma extensão:

```
CREATE EXTENSION file_fdw;
```

Em seguida, crie um servidor estrangeiro:

```
CREATE SERVER pglog FOREIGN DATA WRAPPER file_fdw;
```

Agora você está pronto para criar a tabela de dados estrangeiro. Usando o comando `CREATE FOREIGN TABLE`, você precisará definir as colunas da tabela, o nome do arquivo CSV e seu formato:

```
CREATE FOREIGN TABLE pglog (
  log_time timestamp(3) with time zone,
  user_name text,
  database_name text,
  process_id integer,
  connection_from text,
  session_id text,
  session_line_num bigint,
  command_tag text,
  session_start_time timestamp with time zone,
  virtual_transaction_id text,
  transaction_id bigint,
  error_severity text,
  sql_state_code text,
  message text,
  detail text,
  hint text,
  internal_query text,
  internal_query_pos integer,
  context text,
  query text,
  query_pos integer,
  location text,
  application_name text,
  backend_type text,
  leader_pid integer,
  query_id bigint
) SERVER pglog
OPTIONS ( filename 'log/pglog.csv', format 'csv' );
```

Isso é tudo — agora você pode consultar seu log diretamente. Na produção, é claro, você precisaria definir uma maneira de lidar com a rotação do log.

  

**Exemplo F.2. Criar uma tabela estrangeira com uma opção em uma coluna**

Para definir a opção `force_null` para uma coluna, use a palavra-chave `OPTIONS`.

```
CREATE FOREIGN TABLE films (
 code char(5) NOT NULL,
 title text NOT NULL,
 rating text OPTIONS (force_null 'true')
) SERVER film_server
OPTIONS ( filename 'films/db.csv', format 'csv' );
```

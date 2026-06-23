## reindexdb

reindexdb — reindexar um banco de dados PostgreSQL

## Sinopse

`reindexdb` [*`connection-option`*...] [*`option`*...] [ `-S` | `--schema` *`schema`* ] ... [ `-t` | `--table` *`table`* ] ... [ `-i` | `--index` *`index`* ] ... [ `-s` | `--system` ] [ *`dbname`* | `-a` | `--all` ]

## Descrição

reindexdb é uma ferramenta para reconstruir índices em um banco de dados PostgreSQL.

reindexdb é um wrapper em torno do comando SQL `REINDEX`(sql-reindex.md "REINDEX"). Não há diferença efetiva entre reindexar bancos de dados por meio deste utilitário e por meio de outros métodos para acessar o servidor.

## Opções

reindexdb aceita os seguintes argumentos de linha de comando:

`-a` `--all`: Reindexe todos os bancos de dados.

`--concurrently`: Use a opção `CONCURRENTLY`. Veja [REINDEX](sql-reindex.md "REINDEX"), onde todas as advertências desta opção são explicadas em detalhes.

`[-d] dbname`: Especifica o nome do banco de dados que será reindexado, quando `-a`/`--all` não é usado. Se isso não for especificado, o nome do banco de dados é lido da variável de ambiente `PGDATABASE`. Se isso não for definido, o nome do usuário especificado para a conexão é usado. O *`dbname`* pode ser uma [string de conexão](libpq-connect.md#LIBPQ-CONNSTRING "32.1.1. Connection Strings"). Se assim for, os parâmetros da string de conexão substituirão quaisquer opções de linha de comando conflitantes.

`-e` `--echo`: Repita os comandos que o reindexdb gera e envia ao servidor.

`-i index` `--index=index`: Recrie apenas *`index`*. Múltiplos índices podem ser recriados escrevendo múltiplos interruptores `-i`.

`-j njobs` `--jobs=njobs`: Execute os comandos de reindexação em paralelo, executando os comandos de *`njobs`* simultaneamente. Esta opção pode reduzir o tempo de processamento, mas também aumenta a carga no servidor de banco de dados.

O reindexdb abrirá *`njobs`* conexões ao banco de dados, então certifique-se de que sua configuração [max_connections](runtime-config-connection.md#GUC-MAX-CONNECTIONS) é alta o suficiente para acomodar todas as conexões.

Observe que essa opção é incompatível com a opção `--system`.

`-q` `--quiet`: Não exiba mensagens de progresso.

`-s` `--system`: Reindex apenas os catálogos do sistema do banco de dados.

`-S schema` `--schema=schema`: Reindex *`schema`* apenas. Múltiplos esquemas podem ser reindexados escrevendo vários interruptores `-S`.

`-t table` `--table=table`: Reindex apenas *`table`*. Múltiplas tabelas podem ser reindexadas escrevendo múltiplos `-t` switches.

`--tablespace=tablespace`: Especifica o tablespace onde os índices são reconstruídos. (Esse nome é processado como um identificador com aspas duplas.)

`-v` `--verbose`: Imprimir informações detalhadas durante o processamento.

`-V` `--version`: Imprimir a versão do reindexdb e sair.

`-?` `--help`: Mostrar ajuda sobre os argumentos da linha de comando do comando reindexdb e sair.

reindexdb também aceita os seguintes argumentos de linha de comando para os parâmetros de conexão:

`-h host` `--host=host`: Especifica o nome do host da máquina em que o servidor está sendo executado. Se o valor começar com uma barra, ele é usado como o diretório para o socket de domínio Unix.

`-p port` `--port=port`: Especifica a porta TCP ou a extensão de arquivo de soquete de domínio Unix local em que o servidor está ouvindo conexões.

`-U username` `--username=username`: Nome do usuário para se conectar como.

`-w` `--no-password`: Nunca emita um prompt de senha. Se o servidor exigir autenticação por senha e uma senha não estiver disponível por outros meios, como um arquivo `.pgpass`, a tentativa de conexão falhará. Esta opção pode ser útil em trabalhos em lote e scripts onde nenhum usuário está presente para inserir uma senha.

`-W` `--password`: Reindex o reindexdb para solicitar uma senha antes de se conectar a um banco de dados.

Essa opção nunca é essencial, pois o reindexdb solicitará automaticamente uma senha se o servidor exigir autenticação por senha. No entanto, o reindexdb desperdiçará uma tentativa de conexão descobrindo que o servidor deseja uma senha. Em alguns casos, vale a pena digitar `-W` para evitar a tentativa extra de conexão.

`--maintenance-db=dbname`: Quando o `-a`/`--all` é usado, conecte-se a este banco de dados para coletar a lista de bancos de dados a serem reindexados. Se não for especificado, o banco de dados `postgres` será usado, ou se este não existir, `template1` será usado. Isso pode ser uma [string de conexão](libpq-connect.md#LIBPQ-CONNSTRING). Se for assim, os parâmetros da string de conexão substituirão quaisquer opções de linha de comando conflitantes. Além disso, os parâmetros da string de conexão, exceto o próprio nome do banco de dados, serão reutilizados ao se conectar a outros bancos de dados.

## Meio Ambiente

`PGDATABASE` `PGHOST` `PGPORT` `PGUSER`: Parâmetros de conexão padrão

`PG_COLOR`: Especifica se a cor deve ser usada nas mensagens de diagnóstico. Os valores possíveis são `always`, `auto` e `never`.

Esse utilitário, como a maioria dos outros utilitários do PostgreSQL, também utiliza as variáveis de ambiente suportadas pelo libpq (consulte a [Seção 32.15](libpq-envars.md)).

## Diagnósticos

Em caso de dificuldade, consulte [REINDEX](sql-reindex.md) e [psql](app-psql.md) para discussões sobre problemas potenciais e mensagens de erro. O servidor de banco de dados deve estar em execução no host alvo. Além disso, quaisquer configurações de conexão padrão e variáveis de ambiente usadas pela biblioteca de interface libpq serão aplicadas.

## Exemplos

Para reindexar o banco de dados `test`:

```
$ reindexdb test
```

Para reindexar a tabela `foo` e o índice `bar` em um banco de dados denominado `abcd`:

```
$ reindexdb --table=foo --index=bar abcd
```

## Veja também

[REINDEX](sql-reindex.md "REINDEX")

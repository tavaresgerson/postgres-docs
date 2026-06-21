## clusterdb

clusterdb — agrupe um banco de dados PostgreSQL

## Sinopse

`clusterdb` [*`connection-option`*...] [*`option`*...] [ `--table` | `-t` *`table`* ] ... [ *`dbname`* | `-a` | `--all` ]

## Descrição

O clusterdb é uma ferramenta para reclasificar tabelas em um banco de dados PostgreSQL. Ele encontra tabelas que já foram reclasificadas e as reclasifica novamente no mesmo índice que foi usado anteriormente. As tabelas que nunca foram reclasificadas não são afetadas.

clusterdb é um wrapper em torno do comando SQL [CLUSTER](sql-cluster.md "CLUSTER"). Não há diferença efetiva entre agrupar bancos de dados por meio deste utilitário e por meio de outros métodos para acessar o servidor.

## Opções

clusterdb aceita os seguintes argumentos de linha de comando:

`-a` `--all`: Agrupe todas as bases de dados.

`[-d] dbname`: Especifica o nome do banco de dados a ser agrupado, quando `-a`/`--all` não é usado. Se isso não for especificado, o nome do banco de dados é lido da variável de ambiente `PGDATABASE`. Se isso não for definido, o nome de usuário especificado para a conexão é usado. O *`dbname`* pode ser uma [string de conexão](libpq-connect.md#LIBPQ-CONNSTRING "32.1.1. Connection Strings"). Se assim for, os parâmetros da string de conexão substituirão quaisquer opções de linha de comando conflitantes.

`-e` `--echo`: Repita os comandos que o clusterdb gera e envia para o servidor.

`-q` `--quiet`: Não exiba mensagens de progresso.

`-t table` `--table=table`: Apenas o grupo *`table`*. Várias tabelas podem ser agrupadas escrevendo vários interruptores `-t`.

`-v` `--verbose`: Imprimir informações detalhadas durante o processamento.

`-V` `--version`: Imprimir a versão do clusterdb e sair.

`-?` `--help`: Mostrar ajuda sobre os argumentos da linha de comando do comando clusterdb e sair.

O clusterdb também aceita os seguintes argumentos de linha de comando para os parâmetros de conexão:

`-h host` `--host=host`: Especifica o nome do host da máquina em que o servidor está sendo executado. Se o valor começar com uma barra, ele é usado como o diretório para o socket de domínio Unix.

`-p port` `--port=port`: Especifica a porta TCP ou a extensão de arquivo de soquete de domínio Unix local em que o servidor está ouvindo conexões.

`-U username` `--username=username`: Nome do usuário para se conectar como.

`-w` `--no-password`: Nunca emita um prompt de senha. Se o servidor exigir autenticação por senha e uma senha não estiver disponível por outros meios, como um arquivo `.pgpass`, a tentativa de conexão falhará. Esta opção pode ser útil em trabalhos em lote e scripts onde nenhum usuário está presente para inserir uma senha.

`-W` `--password`: Forçar o clusterdb a solicitar uma senha antes de se conectar a um banco de dados.

Essa opção nunca é essencial, pois o clusterdb solicitará automaticamente uma senha se o servidor exigir autenticação por senha. No entanto, o clusterdb desperdiçará uma tentativa de conexão descobrindo que o servidor deseja uma senha. Em alguns casos, vale a pena digitar `-W` para evitar a tentativa extra de conexão.

`--maintenance-db=dbname`: Quando o `-a`/`--all` for usado, conecte-se a este banco de dados para coletar a lista de bancos de dados para agrupar. Se não for especificado, o banco de dados `postgres` será usado, ou se este não existir, `template1` será usado. Isso pode ser uma [string de conexão](libpq-connect.md#LIBPQ-CONNSTRING). Se for assim, os parâmetros da string de conexão substituirão quaisquer opções de linha de comando conflitantes. Além disso, os parâmetros da string de conexão, exceto o próprio nome do banco de dados, serão reutilizados ao se conectar a outros bancos de dados.

## Meio Ambiente

`PGDATABASE` `PGHOST` `PGPORT` `PGUSER`: Parâmetros de conexão padrão

`PG_COLOR`: Especifica se a cor deve ser usada nas mensagens de diagnóstico. Os valores possíveis são `always`, `auto` e `never`.

Esse utilitário, como a maioria dos outros utilitários do PostgreSQL, também utiliza as variáveis de ambiente suportadas pelo libpq (consulte a [Seção 32.15](libpq-envars.md)).

## Diagnósticos

Em caso de dificuldade, consulte [CLUSTER](sql-cluster.md) e [psql](app-psql.md) para discussões sobre problemas potenciais e mensagens de erro. O servidor de banco de dados deve estar em execução no host alvo. Além disso, quaisquer configurações de conexão padrão e variáveis de ambiente usadas pela biblioteca de interface libpq serão aplicadas.

## Exemplos

Para agrupar o banco de dados `test`:

```
$ clusterdb test
```

Para agrupar uma única tabela `foo` em um banco de dados denominado `xyzzy`:

```
$ clusterdb --table=foo xyzzy
```

## Veja também

[CLUSTER](sql-cluster.md "CLUSTER")

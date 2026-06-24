## vacuumdb

vacuumdb — coleta e analisa um banco de dados PostgreSQL

## Sinopse

`vacuumdb` [*`connection-option`*...] [*`option`*...] [ `-t` | `--table` *`table`* [( *`column`* [,...] )] ] ] ... [ *`dbname`* | `-a` | `--all` ]

`vacuumdb` [*`connection-option`*...] [*`option`*...] [ `-n` | `--schema` *`schema`* ] ... [ *`dbname`* | `-a` | `--all` ]

`vacuumdb` [*`connection-option`*...] [*`option`*...] [ `-N` | `--exclude-schema` *`schema`* ] ... [ *`dbname`* | `-a` | `--all` ]

## Descrição

O vacuumdb é uma ferramenta para limpar um banco de dados PostgreSQL. O vacuumdb também gerará estatísticas internas usadas pelo otimizador de consultas do PostgreSQL.

vacuumdb é um wrapper em torno do comando SQL `VACUUM` (sql-vacuum.md "VACUUM"). Não há diferença efetiva entre a limpeza e a análise de bancos de dados por meio deste utilitário e por meio de outros métodos para acessar o servidor.

## Opções

vacuumdb aceita os seguintes argumentos de linha de comando:

`-a` `--all`: Vácuo em todas as bases de dados.

`--buffer-usage-limit size`: Especifica o tamanho do buffer de acesso de anel (glossary.md#GLOSSARY-BUFFER-ACCESS-STRATEGY "Buffer Access Strategy")*(glossary.md#GLOSSARY-BUFFER-ACCESS-STRATEGY) para uma determinada invocação do vacuumdb. Esse tamanho é usado para calcular o número de buffers compartilhados que serão reutilizados como parte dessa estratégia. Veja [VACUUM](sql-vacuum.md).

`[-d] dbname` `[--dbname=]dbname`: Especifica o nome do banco de dados a ser limpo ou analisado, quando `-a`/`--all` não é usado. Se isso não for especificado, o nome do banco de dados é lido da variável de ambiente `PGDATABASE`. Se isso não estiver definido, o nome do usuário especificado para a conexão é usado. O *`dbname`* pode ser uma [string de conexão](libpq-connect.md#LIBPQ-CONNSTRING "32.1.1. Connection Strings"). Se assim for, os parâmetros da string de conexão substituirão quaisquer opções de linha de comando conflitantes.

`--disable-page-skipping`: Desabilitar o desvio de páginas com base no conteúdo do mapa de visibilidade.

`-e` `--echo`: Repita os comandos que o vacuumdb gera e envia para o servidor.

`-f` `--full`: Realize a aspiração "total".

`-F` `--freeze`: "Congela" agressivamente tuplas.

`--force-index-cleanup`: Sempre remova entradas de índice que apontam para tuplas mortas.

`-j njobs` `--jobs=njobs`: Execute os comandos de vácuo ou análise em paralelo, executando os comandos *`njobs`* simultaneamente. Esta opção pode reduzir o tempo de processamento, mas também aumenta a carga no servidor de banco de dados.

O vacuumdb abrirá conexões *`njobs`* para o banco de dados, então certifique-se de que sua configuração [max_connections](runtime-config-connection.md#GUC-MAX-CONNECTIONS) é alta o suficiente para acomodar todas as conexões.

Observe que o uso deste modo em conjunto com a opção `-f` (`FULL`) pode causar falhas de travamento se certos catálogos do sistema forem processados em paralelo.

`--min-mxid-age mxid_age`: Execute apenas os comandos de vácuo ou análise em tabelas com uma idade de multixact ID de pelo menos *`mxid_age`*. Esta configuração é útil para priorizar as tabelas a serem processadas para evitar o envolvimento de ID multixact (consulte [Seção 24.1.5.1](routine-vacuuming.md#VACUUM-FOR-MULTIXACT-WRAPAROUND)).

Para os fins desta opção, a idade multixact do ID de uma relação é a maior das idades da relação principal e da tabela TOAST associada, se houver. Como os comandos emitidos pelo vacuumdb também processarão a tabela TOAST para a relação, se necessário, não é necessário considerá-la separadamente.

`--min-xid-age xid_age`: Execute apenas os comandos de vácuo ou análise em tabelas com uma idade de ID de transação de pelo menos *`xid_age`*. Esta configuração é útil para priorizar as tabelas a serem processadas para evitar o enrolamento de ID de transação (consulte [Seção 24.1.5](routine-vacuuming.md#VACUUM-FOR-WRAPAROUND)).

Para os fins desta opção, a idade do ID de transação de uma relação é a maior das idades da relação principal e da tabela TOAST associada, se houver. Como os comandos emitidos pelo vacuumdb também processarão a tabela TOAST para a relação, se necessário, não é necessário considerá-la separadamente.

`--missing-stats-only`: Analise apenas as relações que não possuem estatísticas para uma coluna, expressão de índice ou objeto de estatísticas estendidas. Quando usado com `--analyze-in-stages`, esta opção impede que o vacuumdb substitua temporariamente as estatísticas existentes por estatísticas geradas com alvos de estatísticas mais baixos, evitando assim escolhas temporariamente piores do otimizador de consultas.

Essa opção só pode ser usada em conjunto com `--analyze-only` ou `--analyze-in-stages`.

Observe que o `--missing-stats-only` requer privilégios do `SELECT` no [`pg_statistic`](catalog-pg-statistic.md "52.51. pg_statistic") e [`pg_statistic_ext_data`](catalog-pg-statistic-ext-data.md "52.53. pg_statistic_ext_data"), que são restritos a superusuários por padrão.

`-n schema` `--schema=schema`: Limpe ou analise todas as tabelas em *`schema`* apenas. Múltiplos esquemas podem ser aspirados escrevendo múltiplos interruptores `-n`.

`-N schema` `--exclude-schema=schema`: Não limpe ou analise nenhuma tabela em *`schema`*. Múltiplos esquemas podem ser excluídos escrevendo múltiplos `-N` switches.

`--no-index-cleanup`: Não remova entradas de índice que apontam para tuplas mortas.

`--no-process-main`: Ignorar a relação principal.

`--no-process-toast`: Ignorar a tabela TOAST associada à tabela de vácuo, se houver.

`--no-truncate`: Não corte páginas vazias no final da tabela.

`-P parallel_workers` `--parallel=parallel_workers`: Especifique o número de trabalhadores paralelos para *vazio paralelo*. Isso permite que o vácuo utilize múltiplos CPUs para processar índices. Veja [VACUUM](sql-vacuum.md "VACUUM").

`-q` `--quiet`: Não exiba mensagens de progresso.

`--skip-locked`: Ignorar relações que não podem ser bloqueadas imediatamente para processamento.

`-t table [ (column [,...]) ]` `--table=table [ (column [,...]) ]`: Limpe ou analise apenas *`table`*. Os nomes das colunas só podem ser especificados em conjunto com as opções `--analyze` ou `--analyze-only`. Várias tabelas podem ser limpas escrevendo múltiplos interruptores `-t`.

DICA

Se você especificar colunas, provavelmente terá que escapar as chaves da shell. (Veja os exemplos abaixo.)

`-v` `--verbose`: Imprimir informações detalhadas durante o processamento.

`-V` `--version`: Imprimir a versão do vacuumdb e sair.

`-z` `--analyze`: Calcule também estatísticas para uso pelo otimizador.

`-Z` `--analyze-only`: Calcule apenas estatísticas para uso pelo otimizador (sem vácuo).

`--analyze-in-stages`: Calcule apenas estatísticas para uso pelo otimizador (sem vácuo), como `--analyze-only`. Execute três etapas de análise; a primeira etapa utiliza a estatística alvo mais baixa possível (ver [default_statistics_target](runtime-config-query.md#GUC-DEFAULT-STATISTICS-TARGET)) para produzir estatísticas utilizáveis mais rapidamente, e as etapas subsequentes constroem as estatísticas completas.

Essa opção é útil apenas para analisar um banco de dados que atualmente não possui estatísticas ou que possui estatísticas totalmente incorretas, como se ele fosse recém-populado a partir de um dump restaurado ou por `pg_upgrade`. Esteja ciente de que executar essa opção em um banco de dados com estatísticas existentes pode fazer com que as escolhas do otimizador de consulta se tornem temporariamente piores devido aos objetivos de estatísticas baixos das fases iniciais.

`-?` `--help`: Mostrar ajuda sobre os argumentos da linha de comando do comando vacuumdb e sair.

O vacuumdb também aceita os seguintes argumentos de linha de comando para os parâmetros de conexão:

`-h host` `--host=host`: Especifica o nome do host da máquina em que o servidor está sendo executado. Se o valor começar com uma barra, ele é usado como o diretório para o socket de domínio Unix.

`-p port` `--port=port`: Especifica a porta TCP ou a extensão de arquivo de soquete de domínio Unix local em que o servidor está ouvindo conexões.

`-U username` `--username=username`: Nome do usuário para se conectar como.

`-w` `--no-password`: Nunca emita um prompt de senha. Se o servidor exigir autenticação por senha e uma senha não estiver disponível por outros meios, como um arquivo `.pgpass`, a tentativa de conexão falhará. Esta opção pode ser útil em trabalhos em lote e scripts onde nenhum usuário está presente para inserir uma senha.

`-W` `--password`: Forçar o vacuumdb a solicitar uma senha antes de se conectar a um banco de dados.

Essa opção nunca é essencial, pois o vacuumdb solicitará automaticamente uma senha se o servidor exigir autenticação por senha. No entanto, o vacuumdb desperdiçará uma tentativa de conexão descobrindo que o servidor deseja uma senha. Em alguns casos, vale a pena digitar `-W` para evitar a tentativa extra de conexão.

`--maintenance-db=dbname`: Quando o `-a`/`--all` for usado, conecte-se a este banco de dados para coletar a lista de bancos de dados a serem vacúoados. Se não for especificado, o banco de dados `postgres` será usado, ou se este não existir, `template1` será usado. Isso pode ser uma [string de conexão](libpq-connect.md#LIBPQ-CONNSTRING). Se for assim, os parâmetros da string de conexão substituirão quaisquer opções de linha de comando conflitantes. Além disso, os parâmetros da string de conexão, exceto o próprio nome do banco de dados, serão reutilizados ao se conectar a outros bancos de dados.

## Meio Ambiente

`PGDATABASE` `PGHOST` `PGPORT` `PGUSER`: Parâmetros de conexão padrão

`PG_COLOR`: Especifica se a cor deve ser usada em mensagens de diagnóstico. Os valores possíveis são `always`, `auto` e `never`.

Esse utilitário, como a maioria dos outros utilitários do PostgreSQL, também utiliza as variáveis de ambiente suportadas pelo libpq (consulte a [Seção 32.15](libpq-envars.md)).

## Diagnósticos

Em caso de dificuldade, consulte [VACUUM](sql-vacuum.md) e [psql](app-psql.md) para discussões sobre problemas potenciais e mensagens de erro. O servidor de banco de dados deve estar em execução no host alvo. Além disso, quaisquer configurações de conexão padrão e variáveis de ambiente usadas pela biblioteca de interface libpq serão aplicadas.

## Exemplos

Para limpar o banco de dados `test`:

```
$ vacuumdb test
```

Para limpar e analisar para o otimizador um banco de dados chamado `bigdb`:

```
$ vacuumdb --analyze bigdb
```

Para limpar uma única tabela `foo` em um banco de dados chamado `xyzzy`, e analisar uma única coluna `bar` da tabela para o otimizador:

```
$ vacuumdb --analyze --verbose --table='foo(bar)' xyzzy
```

Para limpar todas as tabelas nos esquemas `foo` e `bar` em um banco de dados chamado `xyzzy`:

```
$ vacuumdb --schema='foo' --schema='bar' xyzzy
```

## Veja também

[VACUUM](sql-vacuum.md "VACUUM")

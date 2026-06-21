## pg_test_fsync

pg_test_fsync — determinar o mais rápido `wal_sync_method` para PostgreSQL

## Sinopse

`pg_test_fsync` [*`option`*...]

## Descrição

O pg_test_fsync é destinado a lhe dar uma ideia razoável do que é o método de sincronização [wal_sync_method](runtime-config-wal.md#GUC-WAL-SYNC-METHOD) no seu sistema específico, além de fornecer informações de diagnóstico no caso de um problema identificado de I/O. No entanto, as diferenças mostradas pelo pg_test_fsync podem não fazer nenhuma diferença significativa no desempenho real do banco de dados, especialmente porque muitos servidores de banco de dados não são limitados em velocidade por seus logs de pré-escrita. O pg_test_fsync relata o tempo médio da operação de sincronização de arquivo em microsegundos para cada `wal_sync_method`, que também pode ser usado para informar esforços para otimizar o valor de [commit_delay](runtime-config-wal.md#GUC-COMMIT-DELAY).

## Opções

pg_test_fsync aceita as seguintes opções de linha de comando:

`-f` `--filename`: Especifica o nome do arquivo para escrever dados de teste. Este arquivo deve estar no mesmo sistema de arquivos que o diretório `pg_wal` ou será colocado. (`pg_wal` contém os arquivos WAL.) O padrão é `pg_test_fsync.out` no diretório atual.

`-s` `--secs-per-test`: Especifica o número de segundos para cada teste. Quanto mais tempo por teste, maior a precisão do teste, mas mais tempo leva para ser executado. O padrão é de 5 segundos, o que permite que o programa seja concluído em menos de 2 minutos.

`-V` `--version`: Imprimir a versão do pg_test_fsync e sair.

`-?` `--help`: Mostrar ajuda sobre os argumentos da linha de comando do comando pg_test_fsync e sair.

## Meio Ambiente

A variável de ambiente `PG_COLOR` especifica se é necessário usar cor nas mensagens de diagnóstico. Os valores possíveis são `always`, `auto` e `never`.

## Veja também

[postgres](app-postgres.md "postgres")

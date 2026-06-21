## pg_checksums

pg_checksums — habilite, desabilite ou verifique os checksums de dados em um clúster de banco de dados PostgreSQL

## Sinopse

`pg_checksums` [*`option`*...] [[ `-D` | `--pgdata` ]*`datadir`*]

## Descrição

pg_checksums verifica, habilita ou desabilita os checksums de dados em um clúster PostgreSQL. O servidor deve ser desligado corretamente antes de executar o pg_checksums. Ao verificar os checksums, o status de saída é zero se não houver erros de checksum, e não nulo se pelo menos uma falha de checksum for detectada. Ao habilitar ou desabilitar os checksums, o status de saída é não nulo se a operação falhar.

Ao verificar os checksums, cada arquivo no clúster é verificado. Ao habilitar os checksums, cada bloco de arquivo de relação com um checksum alterado é reescrito no local. Desabilitando os checksums, apenas o arquivo `pg_control` é atualizado.

## Opções

As opções de linha de comando disponíveis são as seguintes:

`-D directory` `--pgdata=directory`: Especifica o diretório onde o cluster de banco de dados é armazenado.

`-c` `--check`: Verifica os checksums. Este é o modo padrão, se nada mais for especificado.

`-d` `--disable`: Desabilita verificações de checksum.

`-e` `--enable`: Habilita verificações de checksum.

`-f filenode` `--filenode=filenode`: Valide apenas os checksums na relação com o filenode *`filenode`*.

`-N` `--no-sync`: Por padrão, `pg_checksums` aguardará que todos os arquivos sejam escritos com segurança no disco. Esta opção faz com que `pg_checksums` retorne sem aguardar, o que é mais rápido, mas significa que um posterior falha do sistema operacional pode deixar o diretório de dados atualizado corrompido. Geralmente, esta opção é útil para testes, mas não deve ser usada em uma instalação de produção. Esta opção não tem efeito ao usar `--check`.

`-P` `--progress`: Habilitar relatórios de progresso. Ao ativar essa opção, será entregue um relatório de progresso ao verificar ou habilitar checksums.

`--sync-method=method`: Quando configurado para `fsync`, que é o padrão, `pg_checksums` abrirá e sincronizará recursivamente todos os arquivos no diretório de dados. A busca por arquivos seguirá links simbólicos para o diretório WAL e cada espaço de tabela configurado.

Em Linux, `syncfs` pode ser usado para pedir ao sistema operacional que sincronize todos os sistemas de arquivos que contêm o diretório de dados, os arquivos WAL e cada espaço de tabela. Consulte [recovery_init_sync_method][(runtime-config-error-handling.md#GUC-RECOVERY-INIT-SYNC-METHOD)] para obter informações sobre as advertências a serem observadas ao usar `syncfs`.

Esta opção não tem efeito quando o `--no-sync` é usado.

`-v` `--verbose`: Habilitar saída detalhada. Lista todos os arquivos verificados.

`-V` `--version`: Imprimir a versão dos pg_checksums e sair.

`-?` `--help`: Mostrar ajuda sobre os argumentos da linha de comando do comando pg_checksums e sair.

## Meio Ambiente

`PGDATA`: Especifica o diretório onde o cluster de banco de dados é armazenado; pode ser sobrescrito usando a opção `-D`.

`PG_COLOR`: Especifica se a cor deve ser usada nas mensagens de diagnóstico. Os valores possíveis são `always`, `auto` e `never`.

## Notas

Habilitar verificações de checksum em um grande clúster pode levar um tempo considerável. Durante essa operação, o clúster ou outros programas que escrevem no diretório de dados não devem ser iniciados, pois isso pode causar perda de dados.

Ao usar uma configuração de replicação com ferramentas que realizam cópias diretas de blocos de arquivos de relação (por exemplo, [pg_rewind][(app-pgrewind.md "pg_rewind")]), habilitar ou desabilitar verificações de checksum pode levar a corrupções de página na forma de checksums incorretos se a operação não for realizada de forma consistente em todos os nós. Ao habilitar ou desabilitar verificações de checksum em uma configuração de replicação, é recomendável, portanto, parar todos os clústeres antes de alterná-los consistentemente. Também é seguro destruir todos os backups, realizar a operação no primário e, finalmente, recriar os backups do zero.

Se o pg_checksums for interrompido ou eliminado ao habilitar ou desabilitar as verificações de checksum, a configuração de verificação de checksum do cluster permanece inalterada, e o pg_checksums pode ser executado novamente para realizar a mesma operação.
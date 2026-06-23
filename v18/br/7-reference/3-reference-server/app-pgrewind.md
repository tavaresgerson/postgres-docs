## pg_rewind

pg_rewind — sincronizar um diretório de dados do PostgreSQL com outro diretório de dados que foi criado a partir dele

## Sinopse

`pg_rewind` [*`option`*...] { `-D` | `--target-pgdata` } *`directory`* { `--source-pgdata=directory` | `--source-server=connstr` }

## Descrição

O pg_rewind é uma ferramenta para sincronizar um clúster PostgreSQL com outra cópia do mesmo clúster, após as linhas do tempo dos clústeres terem divergido. Um cenário típico é trazer um servidor primário antigo de volta ao ar após o failover como um standby que segue o novo primário.

Após um rewind bem-sucedido, o estado do diretório de dados de destino é análogo a um backup de base do diretório de dados de origem. Ao contrário de fazer um novo backup de base ou usar uma ferramenta como o rsync, o pg_rewind não requer a comparação ou cópia de blocos de relação não alterados no clúster. Apenas os blocos alterados dos arquivos de relação existentes são copiados; todos os outros arquivos, incluindo novos arquivos de relação, arquivos de configuração e segmentos WAL, são copiados na íntegra. Como tal, a operação de rewind é significativamente mais rápida do que outras abordagens quando o banco de dados é grande e apenas uma pequena fração de blocos difere entre os clústeres.

O pg_rewind examina os históricos de linha do tempo dos clusters de origem e destino para determinar o ponto em que eles divergiram e espera encontrar o WAL no diretório `pg_wal` do cluster de destino, alcançando até o ponto de divergência. O ponto de divergência pode ser encontrado na linha do tempo do destino, na linha do tempo da origem ou em seu antepassado comum. No cenário típico de falha de sobrevivência, onde o cluster de destino é desligado pouco depois da divergência, isso não é um problema, mas se o cluster de destino estiver em operação por um longo período após a divergência, seus arquivos WAL antigos podem não estar mais presentes. Neste caso, você pode copiá-los manualmente do arquivo WAL para o diretório `pg_wal`, ou executar o pg_rewind com a opção `-c` para recuperá-los automaticamente do arquivo WAL. O uso do pg_rewind não é limitado à sobrevivência, por exemplo, um servidor de espera pode ser promovido, executado algumas transações de escrita e, em seguida, revertido para se tornar novamente de espera.

Após executar o pg_rewind, a reprodução do WAL precisa ser concluída para que o diretório de dados esteja em um estado consistente. Quando o servidor alvo for iniciado novamente, ele entrará na recuperação de arquivo e reproduzirá todos os WAL gerados no servidor de origem a partir do último ponto de verificação antes do ponto de divergência. Se parte do WAL não estiver mais disponível no servidor de origem quando o pg_rewind for executado, e, portanto, não puder ser copiado pela sessão do pg_rewind, ele deve ser disponibilizado quando o servidor alvo for iniciado. Isso pode ser feito criando um arquivo `recovery.signal` no diretório de dados do servidor alvo e configurando um comando de restauração adequado (runtime-config-wal.md#GUC-RESTORE-COMMAND) em `postgresql.conf`.

O pg_rewind exige que o servidor de destino tenha a opção [wal_log_hints](runtime-config-wal.md#GUC-WAL-LOG-HINTS) habilitada em `postgresql.conf` ou que os checksums de dados estejam habilitados quando o clúster foi inicializado com o initdb (o padrão). [full_page_writes](runtime-config-wal.md#GUC-FULL-PAGE-WRITES) também deve ser definido para `on`, mas é habilitado por padrão.

### Aviso: Falhas durante o rewindamento

Se o pg_rewind falhar durante o processamento, é provável que a pasta de dados do alvo não esteja em um estado que possa ser recuperado. Nesse caso, é recomendável fazer um novo backup fresco.

Como o pg_rewind copia os arquivos de configuração inteiramente da fonte, pode ser necessário corrigir a configuração usada para a recuperação antes de reiniciar o servidor alvo, especialmente se o alvo for reintroduzido como um standby da fonte. Se você reiniciar o servidor após a operação de rewind ter sido concluída, mas sem configurar a recuperação, o alvo pode novamente divergir do primário.

O pg_rewind falhará imediatamente se encontrar arquivos que não pode escrever diretamente. Isso pode acontecer, por exemplo, quando o servidor de origem e o servidor de destino utilizam o mesmo mapeamento de arquivos para chaves e certificados SSL de leitura somente. Se tais arquivos estiverem presentes no servidor de destino, é recomendável removê-los antes de executar o pg_rewind. Após realizar o rewind, alguns desses arquivos podem ter sido copiados da origem, no caso, pode ser necessário remover os dados copiados e restaurar o conjunto de links usados antes do rewind.

## Opções

pg_rewind aceita os seguintes argumentos de linha de comando:

`-D directory` `--target-pgdata=directory`: Esta opção especifica o diretório de dados de destino que é sincronizado com a fonte. O servidor de destino deve ser desligado corretamente antes de executar o pg_rewind

`--source-pgdata=directory`: Especifica o caminho do sistema de arquivos para o diretório de dados do servidor de origem para sincronizar com o alvo. Esta opção exige que o servidor de origem seja desligado corretamente.

`--source-server=connstr`: Especifica uma cadeia de conexão libpq para se conectar ao servidor PostgreSQL de origem a ser sincronizado. A conexão deve ser uma conexão normal (não de replicação) com um papel que tenha permissões suficientes para executar as funções usadas pelo pg_rewind no servidor de origem (consulte a seção Notas para detalhes) ou um papel de superusuário. Esta opção exige que o servidor de origem esteja em execução e aceitando conexões.

`-R` `--write-recovery-conf`: Crie `standby.signal` e adicione as configurações de conexão ao `postgresql.auto.conf` no diretório de saída. O nome do banco de dados será registrado apenas se o nome do banco de dados foi especificado explicitamente na string de conexão ou na [variável de ambiente](libpq-envars.md "32.15. Environment Variables"). `--source-server` é obrigatório com esta opção.

`-n` `--dry-run`: Faça tudo, exceto modificar o diretório de destino.

`-N` `--no-sync`: Por padrão, `pg_rewind` aguardará que todos os arquivos sejam escritos com segurança no disco. Esta opção faz com que `pg_rewind` retorne sem aguardar, o que é mais rápido, mas significa que um posterior falha do sistema operacional pode deixar o diretório de dados corrompido. Geralmente, esta opção é útil para testes, mas não deve ser usada em uma instalação de produção.

`-P` `--progress`: Habilita o relatório de progresso. Ao ativar essa opção, será entregue um relatório de progresso aproximado ao copiar dados do cluster de origem.

`-c` `--restore-target-wal`: Use `restore_command` definido na configuração do cluster de destino para recuperar arquivos WAL do arquivo WAL se esses arquivos não estiverem mais disponíveis no diretório `pg_wal`.

`--config-file=filename`: Use o arquivo de configuração principal especificado para o clúster de destino. Isso afeta o pg_rewind quando ele usa internamente o comando postgres para a operação de rewind neste clúster (ao recuperar `restore_command` com a opção `-c/--restore-target-wal` e quando forçando a conclusão da recuperação de falha).

`--debug`: Imprima saída de depuração verbose que é principalmente útil para desenvolvedores que depuram o pg_rewind.

`--no-ensure-shutdown`: O pg_rewind exige que o servidor alvo seja desligado limpo antes de ser rewindado. Por padrão, se o servidor alvo não for desligado limpo, o pg_rewind inicia o servidor alvo no modo de usuário único para completar a recuperação de falha primeiro e o para. Ao passar esta opção, o pg_rewind ignora isso e sai imediatamente se o servidor não for desligado limpo. Espera-se que os usuários lidem com a situação por conta própria nesse caso.

`--sync-method=method`: Quando configurado para `fsync`, que é o padrão, o `pg_rewind` abrirá e sincronizará recursivamente todos os arquivos no diretório de dados. A busca por arquivos seguirá links simbólicos para o diretório WAL e cada espaço de tabela configurado.

Em Linux, `syncfs` pode ser usado para pedir ao sistema operacional que sincronize todos os sistemas de arquivos que contêm o diretório de dados, os arquivos WAL e cada espaço de tabela. Consulte [recovery_init_sync_method](runtime-config-error-handling.md#GUC-RECOVERY-INIT-SYNC-METHOD) para obter informações sobre as advertências a serem observadas ao usar `syncfs`.

Esta opção não tem efeito quando o `--no-sync` é usado.

`-V` `--version`: Exibir informações da versão, e então sair.

`-?` `--help`: Mostrar ajuda e, em seguida, sair.

## Meio Ambiente

Quando a opção `--source-server` é usada, o pg_rewind também utiliza as variáveis de ambiente suportadas pelo libpq (consulte a [Seção 32.15](libpq-envars.md)).

A variável de ambiente `PG_COLOR` especifica se é necessário usar cor nas mensagens de diagnóstico. Os valores possíveis são `always`, `auto` e `never`.

## Notas

Ao executar o pg_rewind usando um clúster online como fonte, um papel que tenha permissões suficientes para executar as funções usadas pelo pg_rewind no clúster fonte pode ser usado em vez de um superusuário. Aqui está como criar tal papel, denominado `rewind_user` aqui:

```
CREATE USER rewind_user LOGIN;
GRANT EXECUTE ON function pg_catalog.pg_ls_dir(text, boolean, boolean) TO rewind_user;
GRANT EXECUTE ON function pg_catalog.pg_stat_file(text, boolean) TO rewind_user;
GRANT EXECUTE ON function pg_catalog.pg_read_binary_file(text) TO rewind_user;
GRANT EXECUTE ON function pg_catalog.pg_read_binary_file(text, bigint, bigint, boolean) TO rewind_user;
```

### Como Funciona

A ideia básica é copiar todas as alterações do nível do sistema de arquivos do cluster de origem para o cluster de destino:

1. Escanear o log WAL do clúster de destino, começando a partir do último ponto de verificação antes do ponto em que o histórico de linha de tempo do clúster de origem se ramificou do clúster de destino. Para cada registro WAL, registrar cada bloco de dados que foi tocado. Isso gera uma lista de todos os blocos de dados que foram alterados no clúster de destino, após o clúster de origem se ramificar. Se alguns dos arquivos WAL não estiverem mais disponíveis, tente executar novamente o pg_rewind com a opção `-c` para procurar os arquivos ausentes no arquivo WAL.
2. Copiar todos os blocos alterados do clúster de origem para o clúster de destino, usando acesso direto ao sistema de arquivos (`--source-pgdata`) ou SQL (`--source-server`). Os arquivos de relação estão agora em um estado equivalente ao momento do último ponto de verificação concluído antes do ponto em que as linhas de tempo WAL do clúster de origem e de destino divergiram, além do estado atual do clúster de origem de quaisquer blocos alterados no clúster de destino após essa divergência.
3. Copiar todos os outros arquivos, incluindo novos arquivos de relação, segmentos WAL, `pg_xact` e arquivos de configuração do clúster de origem para o clúster de destino. Da mesma forma que os backups básicos, o conteúdo dos diretórios `pg_dynshmem/`, `pg_notify/`, `pg_replslot/`, `pg_serial/`, `pg_snapshots/`, `pg_stat_tmp/` e `pg_subtrans/` é omitido dos dados copiados do clúster de origem. Os arquivos `backup_label`, `tablespace_map`, `pg_internal.init`, `postmaster.opts`, `postmaster.pid` e `.DS_Store`, bem como qualquer arquivo ou diretório que comece com `pgsql_tmp`, são omitidos.
4. Criar um arquivo `backup_label` para iniciar a reprodução WAL no ponto de verificação criado no failover e configurar o arquivo `pg_control` com uma LSN de consistência mínima definida como o resultado de `pg_current_wal_insert_lsn()` ao reverter de uma fonte ao vivo ou o último LSN de verificação de ponto ao reverter de uma fonte parada.
5. Ao iniciar o alvo, o PostgreSQL reinterpreta todos os WAL necessários, resultando em um diretório de dados em um estado consistente.
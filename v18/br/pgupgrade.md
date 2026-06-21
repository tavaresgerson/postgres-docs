## pg_upgrade

pg_upgrade — atualizar uma instância do servidor PostgreSQL

## Sinopse

`pg_upgrade` `-b` *`oldbindir`* [`-B` *`newbindir`*] `-d` *`oldconfigdir`* `-D` *`newconfigdir`* [*`option`*...]

## Descrição

O pg_upgrade (anteriormente chamado de pg_migrator) permite que os dados armazenados em arquivos de dados do PostgreSQL sejam atualizados para uma versão principal mais recente do PostgreSQL, sem o processo de exportação/restauração de dados normalmente necessário para atualizações de versão principal, por exemplo, de 12.14 para 13.10 ou de 14.9 para 15.5. Não é necessário para atualizações de versão menor, por exemplo, de 12.7 para 12.8 ou de 14.1 para 14.5.

As principais versões do PostgreSQL adicionam regularmente novos recursos que frequentemente alteram o layout das tabelas do sistema, mas o formato de armazenamento de dados interno raramente muda. O pg_upgrade utiliza esse fato para realizar atualizações rápidas, criando novas tabelas do sistema e simplesmente reutilizando os arquivos de dados do usuário antigos. Se uma futura versão principal alterar o formato de armazenamento de dados de uma maneira que torne o formato de dados antigo ilegível, o pg_upgrade não será utilizável para tais atualizações. (A comunidade tentará evitar tais situações.)

O pg_upgrade faz o possível para garantir que os antigos e novos clusters sejam binariamente compatíveis, por exemplo, verificando configurações de tempo de compilação compatíveis, incluindo binários de 32/64 bits. É importante que quaisquer módulos externos também sejam binariamente compatíveis, embora isso não possa ser verificado pelo pg_upgrade.

O pg_upgrade suporta atualizações de 9.2.X e versões posteriores para a versão atual do PostgreSQL, incluindo versões de instantâneo e beta.

### Aviso

Atualizar um clúster faz com que o destino execute código arbitrário da escolha dos superusuários de origem. Certifique-se de que os superusuários de origem são confiáveis antes de atualizar.

## Opções

pg_upgrade aceita os seguintes argumentos de linha de comando:

`-b` *`bindir`* `--old-bindir=`*`bindir`*: o antigo diretório executável do PostgreSQL; variável de ambiente `PGBINOLD`

`-B` *`bindir`* `--new-bindir=`*`bindir`*: o novo diretório executável do PostgreSQL; o padrão é o diretório onde o pg_upgrade reside; variável de ambiente `PGBINNEW`

`-c` `--check`: verifique apenas os agrupamentos, não altere nenhum dado

`-d` *`configdir`* `--old-datadir=`*`configdir`*: o diretório antigo de configuração do cluster de banco de dados; variável de ambiente `PGDATAOLD`

`-D` *`configdir`* `--new-datadir=`*`configdir`*: o novo diretório de configuração do cluster de banco de dados; variável de ambiente `PGDATANEW`

`-j njobs` `--jobs=njobs`: número de conexões e processos/threads simultâneos a serem utilizados

`-k` `--link`: use hard links em vez de copiar arquivos para o novo clúster

`-N` `--no-sync`: Por padrão, `pg_upgrade` aguardará que todos os arquivos do clúster atualizado sejam escritos com segurança no disco. Esta opção faz com que `pg_upgrade` retorne sem aguardar, o que é mais rápido, mas significa que um posterior falha do sistema operacional pode deixar o diretório de dados corrompido. Geralmente, esta opção é útil para testes, mas não deve ser usada em uma instalação de produção.

`-o` *`options`* `--old-options` *`options`*: opções a serem passadas diretamente para o comando antigo `postgres`; múltiplas invocações de opção são anexadas

`-O` *`options`* `--new-options` *`options`*: opções a serem passadas diretamente para o novo comando `postgres`; múltiplas invocações de opção são anexadas

`-p` *`port`* `--old-port=`*`port`*: o antigo número do portfólio; variável de ambiente `PGPORTOLD`

`-P` *`port`* `--new-port=`*`port`*: o novo número de porta do grupo; variável de ambiente `PGPORTNEW`

`-r` `--retain`: retém arquivos SQL e logs mesmo após a conclusão bem-sucedida

`-s` *`dir`* `--socketdir=`*`dir`*: diretório a ser usado para sockets do postmaster durante a atualização; o diretório de trabalho padrão é o diretório atual; variável de ambiente `PGSOCKETDIR`

`-U` *`username`* `--username=`*`username`*: nome do usuário de instalação do cluster; variável de ambiente `PGUSER`

`-v` `--verbose`: habilite o registro interno detalhado

`-V` `--version`: exibição das informações da versão, em seguida, saia

`--clone`: Use a clonagem eficiente de arquivos (também conhecida como “reflinks” em alguns sistemas) em vez de copiar os arquivos para o novo clúster. Isso pode resultar em uma cópia quase instantânea dos arquivos de dados, proporcionando as vantagens de velocidade de `-k`/`--link`, deixando o antigo clúster intocado.

O clonamento de arquivos só é suportado em alguns sistemas operacionais e sistemas de arquivos. Se ele for selecionado, mas não suportado, o comando pg_upgrade falhará. Atualmente, é suportado no Linux (kernel 4.5 ou posterior) com Btrfs e XFS (em sistemas de arquivos criados com suporte ao reflink), e no macOS com APFS.

`--copy`: Copie os arquivos para o novo clúster. Este é o padrão. (Veja também `--link`, `--clone`, `--copy-file-range` e `--swap`).

`--copy-file-range`: Use a chamada de sistema `copy_file_range` para uma cópia eficiente. Em alguns sistemas de arquivos, isso resulta em resultados semelhantes ao `--clone`, compartilhando blocos físicos do disco, enquanto em outros ainda pode copiar blocos, mas faz isso por meio de um caminho otimizado. Atualmente, é suportada no Linux e no FreeBSD.

`--no-statistics`: Não restaure as estatísticas do antigo clúster para o novo clúster.

`--set-char-signedness=`*`option`*: Configure manualmente a assinatura de caracteres padrão dos novos clusters. Os valores possíveis são `signed` e `unsigned`.

No C, a configuração padrão de sinalização do tipo `char` (quando não especificada explicitamente) varia entre as plataformas. Por exemplo, `char` tem como padrão `signed char` em CPUs x86, mas `unsigned char` em CPUs ARM.

A partir do PostgreSQL 18, os clusters de banco de dados mantêm seu próprio ajuste padrão de sinalização de caracteres, que pode ser usado para garantir um comportamento consistente em plataformas com diferentes configurações padrão de sinalização de caracteres. Por padrão, o pg_upgrade preserva o ajuste de sinalização de caracteres ao fazer uma atualização a partir de um cluster existente. No entanto, ao fazer uma atualização a partir do PostgreSQL 17 ou versões anteriores, o pg_upgrade adota a sinalização de caracteres da plataforma na qual foi construído.

Essa opção permite que você defina explicitamente a assinatura de caráter padrão para o novo clúster, substituindo quaisquer valores herdados. Existem dois cenários específicos em que essa opção é relevante:

* Se você planeja migrar para uma plataforma diferente após a atualização, não deve usar esta opção. O comportamento padrão é o correto neste caso. Em vez disso, realize a atualização na plataforma original sem esta bandeira, e depois migre o clúster posteriormente. Esta é a abordagem recomendada e mais segura. * Se você já migrou o clúster para uma plataforma com diferentes assinaturas de caracteres (por exemplo, de um sistema baseado em x86 para um sistema baseado em ARM), deve usar esta opção para especificar a assinatura de caracteres que corresponde à assinatura de caracteres padrão da plataforma original. Além disso, é essencial não modificar nenhum arquivo de dados entre a migração dos arquivos de dados e a execução de `pg_upgrade`. `pg_upgrade` deve ser a primeira operação que inicia o clúster na nova plataforma.

`--swap`: Mova os diretórios de dados do antigo clúster para o novo clúster. Em seguida, substitua os arquivos de catálogo pelos gerados para o novo clúster. Este modo pode superar `--link`, `--clone`, `--copy` e `--copy-file-range`, especialmente em clústeres com muitas relações.

No entanto, esse modo cria muitos arquivos de lixo no antigo clúster, o que pode prolongar a etapa de sincronização de arquivos se `--sync-method=syncfs` for usado. Portanto, é recomendável usar `--sync-method=fsync` com `--swap`.

Além disso, uma vez que a etapa de transferência de arquivo comece, o antigo clúster será destrutivamente modificado e, portanto, não será mais seguro para iniciar. Consulte [Passo 17](pgupgrade.md#PGUPGRADE-STEP-REVERT) para obter detalhes.

`--sync-method=`*`method`*: Quando configurado para `fsync`, que é o padrão, `pg_upgrade` abrirá e sincronizará recursivamente todos os arquivos no diretório de dados do clúster atualizado. A busca por arquivos seguirá links simbólicos para o diretório WAL e cada espaço de tabela configurado.

Em Linux, `syncfs` pode ser usado para pedir ao sistema operacional que sincronize todos os sistemas de arquivos que contêm o diretório de dados do clúster atualizado, seus arquivos WAL e cada espaço de tabela. Consulte [recovery_init_sync_method](runtime-config-error-handling.md#GUC-RECOVERY-INIT-SYNC-METHOD) para obter informações sobre as advertências a serem observadas ao usar `syncfs`.

Esta opção não tem efeito quando o `--no-sync` é usado.

`-?` `--help`: mostrar ajuda, depois sair

## Uso

Estes são os passos para realizar uma atualização com o pg_upgrade:

### Nota

Os passos para atualizar [*[clusters de replicação lógica][(glossary.md#GLOSSARY-LOGICAL-REPLICATION-CLUSTER "Logical replication cluster")*]](glossário.md#GLÓSSICA-REPLICAÇÃO-CLUSTERS) não são abordados aqui; consulte [Seção 29.13](logical-replication-upgrade.md) para obter detalhes.

1. **Opcionalmente, mova o antigo cluster**

Se você estiver usando um diretório de instalação específico para uma versão, por exemplo, `/opt/PostgreSQL/18`, você não precisa mover o antigo cluster. Todos os instaladores gráficos usam diretórios de instalação específicos para uma versão.

Se o diretório de instalação não for específico para a versão, por exemplo, `/usr/local/pgsql`, é necessário mover o diretório atual de instalação do PostgreSQL para que ele não interfira com a nova instalação do PostgreSQL. Uma vez que o servidor PostgreSQL atual seja desligado, é seguro renomear o diretório de instalação do PostgreSQL; assumindo que o diretório antigo é `/usr/local/pgsql`, você pode fazer:

```
mv /usr/local/pgsql /usr/local/pgsql.old
```

para renomear o diretório.
2. **Para instalações de origem, compile a nova versão**

Monte a nova fonte do PostgreSQL com as `configure` que são compatíveis com o antigo cluster. O pg_upgrade verificará `pg_controldata` para garantir que todas as configurações sejam compatíveis antes de iniciar a atualização. 3. **Instale os novos binários do PostgreSQL**

Instale os binários e os arquivos de suporte do novo servidor. O pg_upgrade está incluído em uma instalação padrão.

Para instalações de fonte, se você deseja instalar o novo servidor em um local personalizado, use a variável `prefix`:

4. **Inicialize o novo clúster PostgreSQL**

Inicialize o novo clúster usando `initdb`. Novamente, use as bandeiras compatíveis `initdb` que correspondem ao clúster antigo. Muitos instaladores pré-construídos fazem essa etapa automaticamente. Não é necessário iniciar o novo clúster.

Muitas extensões e módulos personalizados, sejam eles do `contrib` ou de outra fonte, utilizam arquivos de objeto compartilhado (ou DLLs), por exemplo, `pgcrypto.so`. Se o antigo clúster utilizasse esses arquivos, arquivos de objeto compartilhado que correspondam ao novo binário do servidor devem ser instalados no novo clúster, geralmente por meio de comandos do sistema operacional. Não carregue as definições do esquema, por exemplo, `CREATE EXTENSION pgcrypto`, porque essas serão duplicadas do antigo clúster. Se as atualizações da extensão estiverem disponíveis, o pg_upgrade informará isso e criará um script que pode ser executado posteriormente para atualizá-las.

Copie quaisquer arquivos de pesquisa de texto completo personalizados (dicionário, sinônimo, tesauro, palavras irrelevantes) do antigo para o novo clúster.
7. **Ajuste a autenticação**

`pg_upgrade` se conectará aos servidores antigos e novos várias vezes, então você pode querer definir a autenticação em `peer` em `pg_hba.conf` ou usar um arquivo `~/.pgpass` (consulte [Seção 32.16](libpq-pgpass.md "32.16. The Password File")).

Certifique-se de que ambos os servidores de banco de dados estão parados, usando, em Unix, por exemplo:

```
pg_ctl -D /opt/PostgreSQL/12 stop
pg_ctl -D /opt/PostgreSQL/18 stop
```

ou no Windows, usando os nomes de serviço adequados:

```
NET STOP postgresql-12
NET STOP postgresql-18
```

As réplicas de streaming e os servidores de espera do envio de registros devem estar em execução durante esse desligamento para receber todas as alterações.
9. **Prepare-se para atualizações dos servidores de espera**

Se você está atualizando servidores de espera usando os métodos descritos na seção [Passo 11](pgupgrade.md#PGUPGRADE-STEP-REPLICAS), verifique se os servidores de espera antigos estão atualizados executando pg_controldata contra os clusters primário e de espera antigos. Verifique se os valores de “Localização do ponto de verificação mais recente” correspondem em todos os clusters. Além disso, certifique-se de que `wal_level` não está definido como `minimal` no arquivo `postgresql.conf` no novo cluster primário.

Sempre execute o binário pg_upgrade do novo servidor, não o antigo. O pg_upgrade requer a especificação dos diretórios de dados e diretórios executáveis (`bin`) dos clusters antigo e novo. Você também pode especificar valores de usuário e porta, e se deseja que os arquivos de dados sejam vinculados, clonados ou trocados em vez do comportamento de cópia padrão.

Se você usar o modo de ligação, a atualização será muito mais rápida (sem cópia de arquivos) e usará menos espaço em disco, mas você não poderá acessar seu antigo clúster assim que começar o novo clúster após a atualização. O modo de ligação também exige que os diretórios de dados do antigo e do novo clúster estejam no mesmo sistema de arquivos. (As tabelas e `pg_wal` podem estar em sistemas de arquivos diferentes.) O modo de clonagem oferece as mesmas vantagens de velocidade e espaço em disco, mas não faz com que o antigo clúster seja inutilizável assim que o novo clúster for iniciado. O modo de clonagem também exige que os diretórios de dados do antigo e do novo sejam no mesmo sistema de arquivos. Este modo só está disponível em certos sistemas operacionais e sistemas de arquivos. O modo de troca pode ser o mais rápido se houver muitas relações, mas você não poderá acessar seu antigo clúster assim que o passo de transferência de arquivos começar. O modo de troca também exige que os diretórios de dados do antigo e do novo sejam no mesmo sistema de arquivos.

Definir `--jobs` para 2 ou superior permite que o pg_upgrade processe vários bancos de dados e espaços de tabela em paralelo. Um bom ponto de partida é o número de núcleos da CPU na máquina. Esta opção pode reduzir substancialmente o tempo de atualização para servidores com vários bancos de dados e espaços de tabelas.

Para usuários do Windows, você deve estar logado em uma conta administrativa e, em seguida, executar o pg_upgrade com diretórios com aspas, por exemplo:

```
pg_upgrade.exe
        --old-datadir "C:/Program Files/PostgreSQL/12/data"
        --new-datadir "C:/Program Files/PostgreSQL/18/data"
        --old-bindir "C:/Program Files/PostgreSQL/12/bin"
        --new-bindir "C:/Program Files/PostgreSQL/18/bin"
```

Uma vez iniciado, `pg_upgrade` verificará se os dois clusters são compatíveis e, em seguida, realizará a atualização. Você pode usar `pg_upgrade --check` para realizar apenas as verificações, mesmo que o servidor antigo ainda esteja em execução. `pg_upgrade --check` também descreverá quaisquer ajustes manuais que você precisará fazer após a atualização. Se você vai usar o modo link, clone, copiar faixa de arquivo ou swap, você deve usar a opção `--link`, `--clone`, `--copy-file-range` ou `--swap` com `--check` para habilitar verificações específicas do modo. `pg_upgrade` requer permissão de escrita no diretório atual.

Obviamente, ninguém deve acessar os clusters durante a atualização. O pg_upgrade por padrão executa servidores na porta 50432 para evitar conexões não intencionais do cliente. Você pode usar o mesmo número de porta para ambos os clusters ao fazer uma atualização, porque os clusters antigos e novos não serão executados ao mesmo tempo. No entanto, ao verificar um servidor antigo em execução, os números de porta antigos e novos devem ser diferentes.

Se ocorrer um erro durante a restauração do esquema do banco de dados, `pg_upgrade` será encerrado e você terá que voltar ao antigo clúster conforme descrito em [Passo 17](pgupgrade.md#PGUPGRADE-STEP-REVERT) abaixo. Para tentar `pg_upgrade` novamente, você precisará modificar o antigo clúster para que o restauro do esquema do pg_upgrade seja bem-sucedido. Se o problema for um módulo `contrib`, você pode precisar desinstalar o módulo `contrib` do antigo clúster e instalá-lo no novo clúster após a atualização, assumindo que o módulo não está sendo usado para armazenar dados do usuário.

Se você usou o modo de link e tem servidores de replicação em streaming (consulte [Seção 26.2.5](warm-standby.md#STREAMING-REPLICATION)) ou Log-Shipping (consulte [Seção 26](warm-standby.md)) em standby, você pode seguir estes passos para atualizá-los rapidamente. Você não executará o pg_upgrade nos servidores de standby, mas sim o rsync no primário. Não inicie nenhum servidor ainda.

Se você não usou o modo de link, não tem ou não quer usar rsync, ou quer uma solução mais fácil, ignore as instruções nesta seção e simplesmente recrie os servidores de espera assim que o pg_upgrade for concluído e o novo primário estiver em funcionamento.

1. **Instale os novos binários do PostgreSQL nos servidores de espera**

Certifique-se de que os novos binários e arquivos de suporte estejam instalados em todos os servidores de espera.
2. **Certifique-se de que os novos diretórios de dados de espera *não* existam**

Certifique-se de que os novos diretórios de dados de espera *não* existam ou estejam vazios. Se o initdb foi executado, exclua os novos diretórios de dados dos servidores de espera.
3. **Instale os arquivos de objeto de extensão compartilhados**

Instale os mesmos arquivos de objeto de extensão compartilhados nos novos standby que você instalou no novo clúster primário.
4. **Pare os servidores de standby**

Se os servidores de espera ainda estiverem em execução, pare-os agora usando as instruções acima.
5. **Salve os arquivos de configuração**

Salve quaisquer arquivos de configuração dos diretórios de configuração dos antigos standby que você precisa manter, por exemplo, `postgresql.conf` (e quaisquer arquivos incluídos por ele), `postgresql.auto.conf`, `pg_hba.conf`, pois esses serão sobrescritos ou removidos na próxima etapa.
6. **Execute o rsync**

Ao usar o modo de ligação, os servidores de espera podem ser rapidamente atualizados usando o rsync. Para isso, em um diretório no servidor principal que esteja acima dos diretórios do antigo e do novo clúster de bancos de dados, execute o seguinte no *principal* para cada servidor de espera:

```
rsync --archive --delete --hard-links --size-only --no-inc-recursive old_cluster new_cluster remote_dir
```

onde `old_cluster` e `new_cluster` estão relacionados ao diretório atual no primário, e `remote_dir` está *acima* dos diretórios antigos e novos de cluster no standby. A estrutura de diretórios sob os diretórios especificados no primário e nos standby deve corresponder. Consulte a página do manual do rsync para obter detalhes sobre a especificação do diretório remoto, por exemplo:

```
rsync --archive --delete --hard-links --size-only --no-inc-recursive /opt/PostgreSQL/12 \
      /opt/PostgreSQL/18 standby.example.com:/opt/PostgreSQL
```

Você pode verificar o que o comando fará usando a opção `--dry-run` do rsync. Embora o rsync deva ser executado no principal por pelo menos um standby, é possível executar o rsync em um standby atualizado para atualizar outros standbys, desde que o standby atualizado não tenha sido iniciado.

O que isso faz é registrar os links criados pelo modo de ligação do pg_upgrade que conectam arquivos nos antigos e novos clústeres no servidor principal. Em seguida, ele encontra arquivos correspondentes no antigo clúster do standby e cria links para eles no novo clúster do standby. Arquivos que não foram vinculados no principal são copiados do principal para o standby. (Eles geralmente são pequenos.) Isso fornece atualizações rápidas do standby. Infelizmente, o rsync inutiliza a cópia de arquivos associados a tabelas temporárias e não registradas, porque esses arquivos normalmente não existem em servidores de standby.

Se você tiver tablespaces, você precisará executar um comando similar de rsync para cada diretório de tablespace, por exemplo:

```
rsync --archive --delete --hard-links --size-only --no-inc-recursive /vol1/pg_tblsp/PG_12_201909212 \
      /vol1/pg_tblsp/PG_18_202307071 standby.example.com:/vol1/pg_tblsp
```

Se você tiver reposicionado `pg_wal` fora dos diretórios de dados, o rsync também deve ser executado nesses diretórios.
7. **Configure a replicação em streaming e o envio de logs dos servidores de standby**

Configure os servidores para log shipping. (Você não precisa executar `pg_backup_start()` e `pg_backup_stop()` ou fazer um backup do sistema de arquivos, pois os sobres e os standby ainda estão sincronizados com o principal.) Se o antigo principal estiver antes da versão 17.0, então nenhum dos slots do principal será copiado para o novo standby, então todos os slots do antigo standby devem ser recriados manualmente. Se o antigo principal estiver na versão 17.0 ou posterior, então apenas os slots lógicos do principal serão copiados para o novo standby, mas outros slots do antigo standby não serão copiados, então devem ser recriados manualmente.
12. **Restaure o `pg_hba.conf`**

Se você modificou `pg_hba.conf`, restaure suas configurações originais. Também pode ser necessário ajustar outros arquivos de configuração no novo clúster para corresponder ao antigo clúster, por exemplo, `postgresql.conf` (e quaisquer arquivos incluídos por ele) e `postgresql.auto.conf`.
13. **Inicie o novo servidor**

O novo servidor pode agora ser iniciado com segurança, e em seguida, qualquer servidor de reserva rsync.

Se algum processamento pós-upgrade for necessário, o pg_upgrade emitirá avisos conforme o processo for concluído. Ele também gerará arquivos de script que devem ser executados pelo administrador. Os arquivos de script se conectarão a cada banco de dados que precisa de processamento pós-upgrade. Cada script deve ser executado usando:

```
psql --username=postgres --file=script.sql postgres
```

Os scripts podem ser executados em qualquer ordem e podem ser excluídos uma vez que tenham sido executados.

### Atenção

Em geral, não é seguro acessar tabelas referenciadas em scripts de reconstrução até que os scripts de reconstrução tenham sido executados completamente; fazer isso pode resultar em resultados incorretos ou em desempenho ruim. Tabelas que não são referenciadas em scripts de reconstrução podem ser acessadas imediatamente.

A menos que a opção `--no-statistics` seja especificada, o `pg_upgrade` transferirá a maioria das estatísticas do otimizador do antigo clúster para o novo clúster. Isso não transfere todas as estatísticas, como as criadas explicitamente com [CREATE STATISTICS](sql-createstatistics.md "CREATE STATISTICS"), estatísticas personalizadas adicionadas por uma extensão ou estatísticas coletadas pelo sistema de estatísticas cumulativas.

Como nem todas as estatísticas são transferidas pelo `pg_upgrade`, você será instruído a executar comandos para regenerar essas informações no final da atualização. Você pode precisar definir os parâmetros de conexão para corresponder ao seu novo clúster.

Primeiro, use `vacuumdb --all --analyze-in-stages --missing-stats-only` para gerar rapidamente estatísticas mínimas de otimizador para relações sem nenhuma. Em seguida, use `vacuumdb --all --analyze-only` para garantir que todas as relações tenham estatísticas cumulativas atualizadas para o gatilho de vácuo e análise. Para ambos os comandos, o uso de `--jobs` pode acelerar o processo. Se `vacuum_cost_delay` estiver definido com um valor não nulo, isso pode ser ignorado para acelerar a geração de estatísticas usando `PGOPTIONS`, por exemplo, `PGOPTIONS='-c vacuum_cost_delay=0' vacuumdb ...`. 16. **Excluir o cluster antigo**

Uma vez que você esteja satisfeito com a atualização, pode excluir os diretórios de dados do antigo clúster executando o script mencionado quando o `pg_upgrade` for concluído. (A exclusão automática não é possível se você tiver espaços de tabela definidos pelo usuário dentro do diretório de dados antigo.) Você também pode excluir os diretórios de instalação antigos (por exemplo, `bin`, `share`).

Se, após executar `pg_upgrade`, você desejar voltar ao antigo cluster, há várias opções:

* Se a opção `--check` foi usada, o antigo clúster não foi modificado; ele pode ser reiniciado.
* Se nem a opção `--link` nem a opção `--swap` foi usada, o antigo clúster não foi modificado; ele pode ser reiniciado.
* Se a opção `--link` foi usada, os arquivos de dados podem ser compartilhados entre o antigo e o novo clúster:

+ Se o `pg_upgrade` foi abortado antes do início da vinculação, o antigo clúster não foi modificado; ele pode ser reiniciado.
+ Se você *não* iniciou o novo clúster, o antigo clúster não foi modificado, exceto que, quando o início da vinculação foi iniciado, um sufixo `.old` foi anexado ao `$PGDATA/global/pg_control`. Para reutilizar o antigo clúster, remova o sufixo `.old` do `$PGDATA/global/pg_control`; então, você pode reiniciar o antigo clúster.
+ Se você iniciou o novo clúster, ele foi escrito em arquivos compartilhados e não é seguro usar o antigo clúster. O antigo clúster precisará ser restaurado a partir do backup neste caso.
* Se a opção `--swap` foi usada, o antigo clúster pode ser modificado de forma destrutiva:

+ Se `pg_upgrade` interromper antes de informar que o antigo grupo não é mais seguro para iniciar, o antigo grupo não foi modificado; ele pode ser reiniciado.
+ Se `pg_upgrade` tiver relatado que o antigo grupo não é mais seguro para iniciar, o antigo grupo foi destrutivamente modificado. O antigo grupo precisará ser restaurado a partir do backup neste caso.

## Meio Ambiente

Algumas variáveis de ambiente podem ser usadas para fornecer configurações padrão para opções de linha de comando:

`PGBINOLD`: O antigo diretório executável do PostgreSQL; opção `-b`/`--old-bindir`.

`PGBINNEW`: O novo diretório executável do PostgreSQL; opção `-B`/`--new-bindir`.

`PGDATAOLD`: O diretório antigo de configuração do cluster de banco de dados; opção `-d`/`--old-datadir`.

`PGDATANEW`: O novo diretório de configuração do cluster de banco de dados; opção `-D`/`--new-datadir`.

`PGPORTOLD`: O antigo número do portfólio; opção `-p`/`--old-port`.

`PGPORTNEW`: O novo número de porta do grupo; opção `-P`/`--new-port`.

`PGSOCKETDIR`: Diretório a ser utilizado para sockets do postmaster durante a atualização; opção `-s`/`--socketdir`.

`PGUSER`: Nome do usuário de instalação do cluster; opção `-U`/`--username`.

## Notas

O pg_upgrade cria vários arquivos de trabalho, como esquemas, armazenados em `pg_upgrade_output.d` no diretório do novo clúster. Cada execução cria um novo subdiretório com um nome que contém um timestamp formatado de acordo com o ISO 8601 (`%Y%m%dT%H%M%S`), onde todos os arquivos gerados são armazenados. `pg_upgrade_output.d` e seus arquivos contidos serão removidos automaticamente se o pg_upgrade for concluído com sucesso; mas, no caso de problemas, os arquivos lá podem fornecer informações úteis para depuração.

O pg_upgrade lança postmasters de curta duração nos diretórios de dados antigos e novos. Por padrão, os arquivos temporários de soquete Unix para comunicação com esses postmasters são feitos no diretório de trabalho atual. Em algumas situações, o nome do caminho do diretório atual pode ser muito longo para ser um nome de soquete válido. Nesse caso, você pode usar a opção `-s` para colocar os arquivos de soquete em algum diretório com um nome de caminho mais curto. Por segurança, certifique-se de que esse diretório não seja legível ou modificável por outros usuários. (Isso não é suportado no Windows.)

Todos os casos de falha, reconstrução e reindexação serão relatados pelo pg_upgrade se afetarem sua instalação; scripts pós-upgrade para reconstruir tabelas e índices serão gerados automaticamente. Se você estiver tentando automatizar a atualização de muitos clusters, você deve descobrir que clusters com esquemas de banco de dados idênticos requerem os mesmos passos pós-upgrade para todas as atualizações de clusters; isso ocorre porque os passos pós-upgrade são baseados nos esquemas do banco de dados, e não nos dados do usuário.

Para testes de implantação, crie uma cópia apenas de esquema do antigo clúster, insira dados fictícios e faça a atualização.

O pg_upgrade não suporta a atualização de bancos de dados que contêm colunas de tabela usando esses tipos de dados de sistema de referência de OID `reg*`:



<table border="0" class="simplelist" summary="Simple list">
 <tr>
  <td>
   <code class="type">
    regcollation
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="type">
    regconfig
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="type">
    regdictionary
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="type">
    regnamespace
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="type">
    regoper
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="type">
    regoperator
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="type">
    regproc
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="type">
    regprocedure
   </code>
  </td>
 </tr>
</table>







(`regclass`, `regrole` e `regtype` podem ser atualizados.)

Se você deseja usar o modo de link e não quiser que seu antigo clúster seja modificado quando o novo clúster for iniciado, considere usar o modo de clonagem. Se isso não estiver disponível, faça uma cópia do antigo clúster e atualize-o no modo de link. Para fazer uma cópia válida do antigo clúster, use `rsync` para criar uma cópia suja do antigo clúster enquanto o servidor estiver em execução, depois desligue o servidor antigo e execute `rsync --checksum` novamente para atualizar a cópia com quaisquer alterações para torná-la consistente. (`--checksum` é necessário porque `rsync` tem apenas granularidade de tempo de modificação de arquivo de um segundo.) Você pode querer excluir alguns arquivos, por exemplo, `postmaster.pid`, conforme documentado em [Seção 25.3.4](continuous-archiving.md#BACKUP-LOWLEVEL-BASE-BACKUP "25.3.4. Making a Base Backup Using the Low Level API"). Se seu sistema de arquivos suportar instantâneos de sistema de arquivos ou cópias de arquivo de cópia por escrita, você pode usá-las para fazer um backup do antigo clúster e dos espaços de tabela, embora o instantâneo e as cópias devem ser criados simultaneamente ou enquanto o servidor de banco de dados está fora de operação.

## Veja também

[initdb](app-initdb.md "initdb"), [pg_ctl](app-pg-ctl.md "pg_ctl"), [pg_dump](app-pgdump.md "pg_dump"), [postgres](app-postgres.md "postgres")
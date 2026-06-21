## pg_combinebackup

pg_combinebackup — reconstruir um backup completo a partir de um backup incremental e backups dependentes

## Sinopse

`pg_combinebackup` [*`option`*...] [*`backup_directory`*...]

## Descrição

O pg_combinebackup é usado para reconstruir um backup completo sintético a partir de um [backup incremental][(continuous-archiving.md#BACKUP-INCREMENTAL-BACKUP "25.3.3. Making an Incremental Backup")] e dos backups anteriores dos quais depende.

Especifique todos os backups necessários na linha de comando, do mais antigo ao mais recente. Ou seja, o primeiro diretório de backup deve ser o caminho para o backup completo, e o último deve ser o caminho para o backup incremental final que você deseja restaurar. O backup reconstruído será escrito no diretório de saída especificado pela opção `-o`.

O pg_combinebackup tentará verificar se os backups que você especifica formam uma cadeia de backups legal a partir da qual um backup completo correto pode ser reconstruído. No entanto, ele não é projetado para ajudá-lo a acompanhar quais backups dependem de quais outros backups. Se você remover um ou mais dos backups anteriores nos quais seu backup incremental depende, não poderá restaurá-lo. Além disso, o pg_combinebackup apenas tenta verificar se os backups têm a relação correta entre si, não se cada backup individual está intacto; para isso, use [pg_verifybackup][(app-pgverifybackup.md "pg_verifybackup")].

Como a saída do pg_combinebackup é um backup completo sintético, ele pode ser usado como entrada para uma futura invocação do pg_combinebackup. O backup completo sintético seria especificado na linha de comando em vez da cadeia de backups de que foi reconstruído.

## Opções

`-d` `--debug`: Imprima muitas saídas de registro de depuração em `stderr`.

`-k` `--link`: Use links hard em vez de copiar arquivos para o backup sintético. A reconstrução do backup sintético pode ser mais rápida (sem cópia de arquivos) e usar menos espaço em disco, mas deve-se ter cuidado ao usar o diretório de saída, porque quaisquer modificações nesse diretório (por exemplo, iniciar o servidor) também podem afetar os diretórios de entrada. Da mesma forma, as alterações nos diretórios de entrada (por exemplo, iniciar o servidor no backup completo) podem afetar o diretório de saída. Assim, essa opção é melhor usada quando os diretórios de entrada são apenas cópias que serão removidas após o pg_combinebackup ter sido concluído.

Requer que os backups de entrada e o diretório de saída estejam no mesmo sistema de arquivos.

Se um manifesto de backup não estiver disponível ou não contiver o checksum do tipo correto, os links duros ainda serão criados, mas o arquivo também será lido bloco a bloco para o cálculo do checksum.

`-n` `--dry-run`: A opção `-n`/`--dry-run` instrui o `pg_combinebackup` a descobrir o que seria feito sem, na verdade, criar o diretório alvo ou quaisquer arquivos de saída. É particularmente útil em combinação com `--debug`.

`-N` `--no-sync`: Por padrão, o `pg_combinebackup` aguardará que todos os arquivos sejam escritos com segurança no disco. Esta opção faz com que o `pg_combinebackup` retorne sem aguardar, o que é mais rápido, mas significa que um posterior falha do sistema operacional pode deixar o backup de saída corrompido. Geralmente, esta opção é útil para testes, mas não deve ser usada ao criar uma instalação de produção.

`-o outputdir` `--output=outputdir`: Especifica o diretório de saída para o qual o backup completo sintético deve ser escrito. Atualmente, este argumento é necessário.

`-T olddir=newdir` `--tablespace-mapping=olddir=newdir`: Recoloca o tablespace no diretório *`olddir`* para *`newdir`* durante o backup. *`olddir`* é o caminho absoluto do tablespace como ele existe no backup final especificado na linha de comando, e *`newdir`* é o caminho absoluto a ser usado para o tablespace no backup reconstruído. Se qualquer um dos caminhos precisar conter um sinal de igual (`=`), preceda-o com uma barra invertida. Esta opção pode ser especificada várias vezes para vários tablespaces.

`--clone`: Use a clonagem eficiente de arquivos (também conhecida como "reflinks" em alguns sistemas) em vez de copiar os arquivos para o novo diretório de dados, o que pode resultar em uma cópia quase instantânea dos arquivos de dados.

Se um manifesto de backup não estiver disponível ou não contiver o checksum do tipo correto, a clonagem de arquivos será usada para copiar o arquivo, mas o arquivo também será lido bloco a bloco para o cálculo do checksum.

A clonagem de arquivos só é suportada em alguns sistemas operacionais e sistemas de arquivos. Se ela for selecionada, mas não suportada, o comando pg_combinebackup falhará. Atualmente, ela é suportada no Linux (kernel 4.5 ou posterior) com Btrfs e XFS (em sistemas de arquivos criados com suporte ao reflink), e no macOS com APFS.

`--copy`: Realize uma cópia regular de arquivo. Este é o padrão. (Veja também `--copy-file-range`, `--clone` e `-k`/`--link`).

`--copy-file-range`: Use a chamada de sistema `copy_file_range` para uma cópia eficiente. Em alguns sistemas de arquivos, isso resulta em resultados semelhantes ao `--clone`, compartilhando blocos físicos do disco, enquanto em outros, ainda pode copiar blocos, mas faz isso por meio de um caminho otimizado. Atualmente, é suportada no Linux e no FreeBSD.

Se um manifesto de backup não estiver disponível ou não contiver o checksum do tipo correto, o `copy_file_range` será usado para copiar o arquivo, mas o arquivo também será lido bloco a bloco para o cálculo do checksum.

`--manifest-checksums=algorithm`: Assim como [pg_basebackup](app-pgbasebackup.md "pg_basebackup"), o pg_combinebackup escreve um manifesto de backup no diretório de saída. Esta opção especifica o algoritmo de verificação de checksum que deve ser aplicado a cada arquivo incluído no manifesto de backup. Atualmente, os algoritmos disponíveis são `NONE`, `CRC32C`, `SHA224`, `SHA256`, `SHA384` e `SHA512`. O padrão é `CRC32C`.

`--no-manifest`: Desabilita a geração de um manifesto de backup. Se esta opção não for especificada, um manifesto de backup para o backup reconstruído será escrito no diretório de saída.

`--sync-method=method`: Quando configurado para `fsync`, que é o padrão, `pg_combinebackup` abrirá e sincronizará recursivamente todos os arquivos no diretório de backup. Quando o formato simples é usado, a busca por arquivos seguirá links simbólicos para o diretório WAL e cada espaço de tabela configurado.

Em Linux, `syncfs` pode ser usado para pedir ao sistema operacional que sincronize todo o sistema de arquivos que contém o diretório de backup. Quando o formato simples é usado, `pg_combinebackup` também sincronizará os sistemas de arquivos que contêm os arquivos WAL e cada espaço de tabela. Consulte [recovery_init_sync_method][(runtime-config-error-handling.md#GUC-RECOVERY-INIT-SYNC-METHOD)] para obter informações sobre as advertências a serem consideradas ao usar `syncfs`.

Esta opção não tem efeito quando o `--no-sync` é usado.

`-V` `--version`: Imprime a versão do pg_combinebackup e encerra.

`-?` `--help`: Mostra ajuda sobre os argumentos da linha de comando do comando pg_combinebackup e sai.

## Limitações

`pg_combinebackup` não recompõe os checksums de página ao escrever o diretório de saída. Portanto, se algum dos backups usados para reconstrução foram feitos com checksums desativados, mas o backup final foi feito com checksums ativados, o diretório resultante pode conter páginas com checksums inválidos.

Para evitar esse problema, é recomendável fazer um novo backup completo após alterar o estado do checksum do clúster usando [pg_checksums][(app-pgchecksums.md "pg_checksums")]. Caso contrário, você pode desativar e, em seguida, reativá-los opcionalmente os checksums no diretório produzido por `pg_combinebackup` para corrigir o problema.

## Meio Ambiente

Esse utilitário, como a maioria dos outros utilitários do PostgreSQL, utiliza as variáveis de ambiente suportadas pelo libpq (consulte a Seção 32.15 [(libpq-envars.md "32.15. Environment Variables")]).

A variável de ambiente `PG_COLOR` especifica se a cor deve ser usada nas mensagens de diagnóstico. Os valores possíveis são `always`, `auto` e `never`.

## Veja também

[pg_basebackup](app-pgbasebackup.md "pg_basebackup")

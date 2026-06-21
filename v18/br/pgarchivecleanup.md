## pg_archivecleanup

pg_archivecleanup — limpar arquivos de arquivo WAL do PostgreSQL

## Sinopse

`pg_archivecleanup` [*`option`*...] *`archivelocation`* *`oldestkeptwalfile`*

## Descrição

O pg_archivecleanup é projetado para ser usado como um `archive_cleanup_command` para limpar arquivos de arquivos WAL ao executar como um servidor de espera (consulte [Seção 26.2][(warm-standby.md "26.2. Log-Shipping Standby Servers")]). O pg_archivecleanup também pode ser usado como um programa autônomo para limpar arquivos de arquivos WAL.

Para configurar um servidor de espera para usar pg_archivecleanup, coloque isso em seu arquivo de configuração `postgresql.conf`:

```
archive_cleanup_command = 'pg_archivecleanup archivelocation %r'
```

onde *`archivelocation`* é o diretório a partir do qual os arquivos de segmento WAL devem ser removidos.

Quando usado dentro de [archive_cleanup_command][(runtime-config-wal.md#GUC-ARCHIVE-CLEANUP-COMMAND)], todos os arquivos WAL que logicamente precedem o valor do argumento `%r` serão removidos de *`archivelocation`*. Isso minimiza o número de arquivos que precisam ser retidos, preservando a capacidade de reinício em caso de falha. O uso deste parâmetro é apropriado se o *`archivelocation`* for uma área de preparação transitória para este servidor de espera específico, mas *não* quando o *`archivelocation`* é destinado como uma área de arquivo WAL de longo prazo, ou quando múltiplos servidores de espera estão recuperando da mesma localização de arquivo.

Quando usado como um programa independente, todos os arquivos WAL que logicamente precedem o *`oldestkeptwalfile`* serão removidos de *`archivelocation`*. Neste modo, se você especificar um nome de arquivo `.partial` ou `.backup`, então apenas o prefixo do arquivo será usado como o *`oldestkeptwalfile`*. Este tratamento do nome de arquivo `.backup` permite que você remova todos os arquivos WAL arquivados antes de um backup específico da base sem erro. Por exemplo, o seguinte exemplo removerá todos os arquivos mais antigos do nome de arquivo WAL `000000010000003700000010`:

```
pg_archivecleanup -d archive 000000010000003700000010.00000020.backup

pg_archivecleanup:  keep WAL file "archive/000000010000003700000010" and later
pg_archivecleanup:  removing file "archive/00000001000000370000000F"
pg_archivecleanup:  removing file "archive/00000001000000370000000E"
```

O pg_archivecleanup assume que *`archivelocation`* é um diretório legível e gravável pelo usuário que possui o servidor.

## Opções

pg_archivecleanup aceita os seguintes argumentos de linha de comando:

`-b` `--clean-backup-history`: Remova também os arquivos de histórico de backup. Consulte [Seção 25.3.2](continuous-archiving.md#BACKUP-BASE-BACKUP "25.3.2. Making a Base Backup") para obter detalhes sobre os arquivos de histórico de backup.

`-d` `--debug`: Imprima muitas saídas de registro de depuração em `stderr`.

`-n` `--dry-run`: Imprima os nomes dos arquivos que seriam removidos em `stdout` (realiza uma execução seca).

`-V` `--version`: Imprimir a versão do pg_archivecleanup e sair.

`-x extension` `--strip-extension=extension`: Forneça uma extensão que será removida de todos os nomes de arquivo antes de decidir se eles devem ser excluídos. Isso é tipicamente útil para limpar arquivos que foram comprimidos durante o armazenamento e, portanto, tiveram uma extensão adicionada pelo programa de compressão. Por exemplo: `-x .gz`.

`-?` `--help`: Mostrar ajuda sobre os argumentos da linha de comando do comando pg_archivecleanup e sair.

## Meio Ambiente

A variável de ambiente `PG_COLOR` especifica se a cor deve ser usada nas mensagens de diagnóstico. Os valores possíveis são `always`, `auto` e `never`.

## Notas

O pg_archivecleanup é projetado para funcionar com o PostgreSQL 8.0 e versões posteriores quando usado como um utilitário independente, ou com o PostgreSQL 9.0 e versões posteriores quando usado como um comando de limpeza de arquivos de arquivação.

O pg_archivecleanup é escrito em C e possui um código-fonte fácil de modificar, com seções especificamente designadas para ser modificadas de acordo com suas próprias necessidades.

## Exemplos

Em sistemas Linux ou Unix, você pode usar:

```
archive_cleanup_command = 'pg_archivecleanup -d /mnt/standby/archive %r 2>>cleanup.log'
```

onde o diretório do arquivo está localizado fisicamente no servidor de espera, de modo que o `archive_command` o está acessando através do NFS, mas os arquivos são locais no servidor de espera. Isso fará:

* produzir saída de depuração em `cleanup.log`
* remover arquivos que não são mais necessários do diretório do arquivo